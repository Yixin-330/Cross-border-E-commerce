"""
Base Agent — shared logic for all Sub-Agents.

Supports two LLM providers selected by LLM_PROVIDER:
  - anthropic (default): Anthropic Messages API + tool_use structured output
  - deepseek: OpenAI-compatible Chat Completions + JSON mode structured output

If no provider key or SDK is available, the agent runs in mock mode.
"""
import json
import os
import re
from typing import Any, Callable

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None  # graceful fallback when package not installed

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # DeepSeek uses the OpenAI-compatible SDK

try:
    from jsonschema import validate as validate_json_schema
except ImportError:
    validate_json_schema = None

TOOLS_REGISTRY: dict[str, Callable] = {}


def register_tool(fn: Callable):
    """Decorator to register a tool for function-calling."""
    TOOLS_REGISTRY[fn.__name__] = fn
    return fn


def get_provider() -> str:
    provider = os.environ.get("LLM_PROVIDER", "anthropic").strip().lower()
    return provider if provider in ("anthropic", "deepseek") else "anthropic"


def default_model(provider: str) -> str:
    if provider == "deepseek":
        # Use the model ID available in your DeepSeek console; deepseek-chat is
        # a legacy alias on some accounts.
        return os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
    return os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")


def has_api_key() -> bool:
    provider = get_provider()
    if provider == "deepseek":
        key = os.environ.get("DEEPSEEK_API_KEY", "")
    else:
        key = os.environ.get("ANTHROPIC_API_KEY", "")
    return bool(key) and not key.startswith("sk-ant-xxx")


def _parse_json_content(text: str) -> dict:
    """Parse JSON, tolerating an accidental Markdown code fence."""
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


class BaseAgent:
    """Every Sub-Agent extends BaseAgent."""

    def __init__(self, name: str, system_prompt: str, model: str | None = None):
        self.name = name
        self.system_prompt = system_prompt
        self.provider = get_provider()
        self.model = model or default_model(self.provider)
        sdk_available = OpenAI is not None if self.provider == "deepseek" else Anthropic is not None
        self.use_mock = not has_api_key() or not sdk_available
        self._client = None
        self.temperature: float | None = None

    def get_tool_defs(self) -> list[dict]:
        """Override to return tool definitions for this agent."""
        return []

    def execute_tool(self, tool_name: str, args: dict) -> Any:
        """Run a registered tool by name."""
        fn = TOOLS_REGISTRY.get(tool_name)
        if fn:
            return fn(**args)
        raise ValueError(f"Unknown tool: {tool_name}")

    def _build_messages(self, input_text: str, context: list[dict] | None = None) -> list[dict]:
        msgs = []
        if context:
            msgs.extend(context)
        msgs.append({"role": "user", "content": input_text})
        return msgs

    def _get_client(self):
        if self._client is not None:
            return self._client
        if self.provider == "deepseek":
            if OpenAI is None:
                raise RuntimeError("openai package is not installed")
            self._client = OpenAI(
                api_key=os.environ.get("DEEPSEEK_API_KEY"),
                base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
                timeout=float(os.environ.get("LLM_TIMEOUT", "120")),
            )
        else:
            if Anthropic is None:
                raise RuntimeError("anthropic package is not installed")
            self._client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        return self._client

    def run(self, input_text: str, output_schema: dict | None = None,
            context: list[dict] | None = None) -> dict | str:
        """
        Run the agent with optional structured output.
        If no API key / SDK is available, runs in mock mode.
        """
        if self.use_mock:
            return self._run_mock(input_text, output_schema)
        if self.provider == "deepseek":
            return self._run_deepseek(input_text, output_schema, context)
        return self._run_anthropic(input_text, output_schema, context)

    def _run_anthropic(self, input_text: str, output_schema: dict | None,
                       context: list[dict] | None) -> dict | str:
        client = self._get_client()
        tools = self.get_tool_defs()
        extra_kwargs = {}
        if self.temperature is not None:
            extra_kwargs["temperature"] = self.temperature

        if output_schema:
            tools.append({
                "name": output_schema["name"],
                "description": f"Structured output for {self.name}",
                "input_schema": output_schema["schema"],
            })
            extra_kwargs["tool_choice"] = {"type": "any"}

        msgs = self._build_messages(input_text, context)
        response = client.messages.create(
            model=self.model,
            max_tokens=int(os.environ.get("LLM_MAX_TOKENS", "4096")),
            system=self.system_prompt,
            messages=msgs,
            tools=tools if tools else None,
            **extra_kwargs,
        )

        for block in response.content:
            if block.type == "tool_use":
                if output_schema and block.name == output_schema["name"]:
                    return block.input
                result = self.execute_tool(block.name, block.input)
                if not output_schema:
                    return result
                continue

        return response.content[0].text if response.content else ""

    def _run_deepseek(self, input_text: str, output_schema: dict | None,
                      context: list[dict] | None) -> dict | str:
        """OpenAI-compatible structured generation.

        Tool calling is intentionally not looped here yet; the data tools remain
        in the deterministic mock/tool layer. The output schema is enforced via
        JSON mode + a retry when parsing fails.
        """
        client = self._get_client()
        messages = [{"role": "system", "content": self.system_prompt}]
        if context:
            messages.extend(context)

        if output_schema:
            schema_text = json.dumps(output_schema["schema"], ensure_ascii=False)
            messages.append({
                "role": "user",
                "content": (
                    f"{input_text}\n\n"
                    "请严格输出 json 格式，不要输出 Markdown 代码块或解释。\n"
                    f"输出必须符合以下 JSON Schema：\n{schema_text}"
                ),
            })
        else:
            messages.append({"role": "user", "content": input_text})

        kwargs: dict = {
            "model": self.model,
            "messages": messages,
            "max_tokens": int(os.environ.get("LLM_MAX_TOKENS", "4096")),
        }
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if output_schema and os.environ.get("DEEPSEEK_JSON_MODE", "1") != "0":
            kwargs["response_format"] = {"type": "json_object"}

        last_error = None
        for _ in range(2):
            response = client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content or ""
            if not output_schema:
                return content
            try:
                data = _parse_json_content(content)
                if validate_json_schema is not None:
                    validate_json_schema(instance=data, schema=output_schema["schema"])
                return data
            except Exception as exc:
                last_error = exc
                messages.append({"role": "assistant", "content": content})
                messages.append({
                    "role": "user",
                    "content": "上一条输出不是合法 json 或不符合 Schema。请严格按给定 JSON Schema 重新输出，只输出 json。",
                })
                kwargs["messages"] = messages

        raise ValueError(f"模型未返回合法 JSON: {last_error}")

    def _run_mock(self, input_text: str, output_schema: dict | None = None) -> dict | str:
        """Mock mode: directly return structured data without calling an LLM."""
        if output_schema:
            return self._generate_mock_output(input_text, output_schema)
        return {"message": f"[{self.name}] Mock response for: {input_text[:80]}..."}

    def _generate_mock_output(self, input_text: str, schema: dict) -> dict:
        """Override in each Sub-Agent to return realistic mock data."""
        return {"mock": True, "note": f"Generated by {self.name} in mock mode"}
