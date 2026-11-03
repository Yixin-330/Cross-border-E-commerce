import httpx, json

payload = {
    "query": "Shopee 对违反禁限售政策的卖家会采取什么措施？",
    "platform": "shopee",
    "top_k": 5,
    # 可选：
    # "country": "id",
    # "mode": "auto",
    # "rerank": True,
    # "rerank_pool": 50,
  }

r = httpx.post(
    "http://127.0.0.1:8000/api/knowledge",
    json=payload,
    timeout=180,
  )
print("status:", r.status_code)
print(json.dumps(r.json(), ensure_ascii=False, indent=2))