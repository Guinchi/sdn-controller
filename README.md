# SDN Controller

Assignment 4 – Diego Albertini

Implements ECMP load‑balancing, QoS priorities, backup paths and
automatic re‑routing on link failures, with a live topology visualiser.

---

## 📦 Requirements

* Python 3.10 + (tested on 3.11)
* `networkx` ≥ 3.4  
* `matplotlib` ≥ 3.10

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install networkx matplotlib
