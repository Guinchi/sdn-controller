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


Commands:
  add_node N ; Add switch N to the topology
  remove_node N ; Delete node N and its links
  add_link U V [cap] ; Create undirected link U—V (default cap = 1)
  remove_link U V ; Remove Link
  fail_link U V ; Mark link down (simulate failure)
  restore_link U V ; Bring a failed link up
  inject_flow SRC DST [size] [priority] [critical] ; Install a flow • size (default 1) • priority flag ⇒ high‑priority • critical flag ⇒ store backup path
  show ; 	Open / refresh the visualization window
  help ; List commands
  exit ; Quit the CLI



Example:
  add_node A
  add_node B
  add_node C
  add_link A B 10
  add_link B C 10
  add_link A C 5
  inject_flow A C 2
  show

  fail_link A C
  show

  restore_link A C
  show
  exit
