fetch-trends skill

Example

Input:
{
  "query": "climate policy",
  "time_window": "P30D"
}

Output:
{
  "trends": [
    {"topic": "carbon tax", "score": 0.82, "samples": ["...sample text..."]}
  ],
  "meta": {"source": "openclaw-mock"}
}
