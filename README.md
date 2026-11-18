# Mini Cook

A small multi-agent pipeline, built from scratch one step at a time to learn
how [Captain Cook](https://github.com/Flissel/Captain_cook) works. It uses a
local LLM through [Ollama](https://ollama.com).

| Step | Module | Concept |
| --- | --- | --- |
| 1 | `mini_captain/events.py` | Agents talk through immutable event messages |
| 2 | `mini_captain/bus.py` | Publish and subscribe |
| 3 | ledger | Append-only, hash-chained log |
| 4 | decomposer | Ollama splits a problem into tasks |
| 5 | gatekeeper | Rule checks before work runs |
| 6 | coordinator and workers | Route tasks by capability |
| 7 | supervisor | Retries, backoff, escalation |
| 8 | pipeline | Wire everything together and run a demo |

## Run the tests

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -q
```
