from collections import defaultdict, deque
import itertools

class Flow:
    _ids = itertools.count()
    def __init__(self, src, dst, size, prio, critical, path, backup):
        self.id      = next(self._ids)
        self.src     = src
        self.dst     = dst
        self.size    = size
        self.prio    = prio
        self.critical = critical
        self.path    = path
        self.backup  = backup

class PolicyEngine:
    """Installs flow rules & recomputes them on link failure."""
    def __init__(self, topo):
        self.topo = topo
        self.flows = {}                 # id ➜ Flow
        self.round_robin = defaultdict(deque)  # (src,dst) ➜ deque(paths)

    # ───────────────────────────── install flow ──────────────────────────────
    def install_flow(self, src, dst, size=1, priority=False, critical=False):
        paths = self.topo.shortest_paths(src, dst, k=2)
        if not paths:
            raise ValueError("No path available")

        # -- load balancing: remember equal‑cost paths in a deque
        paths_t = [tuple(p) for p in paths]
        key = (src, dst)
        if key not in self.round_robin or set(self.round_robin[key]) != set(paths_t):
            self.round_robin[key] = deque(paths_t)
        path = list(self.round_robin[key][0]) 
        self.round_robin[key].rotate(-1)

        backup = paths[1] if critical and len(paths) > 1 else None
        f = Flow(src, dst, size, priority, critical, path, backup)
        self.flows[f.id] = f
        self._apply_util_change(path, size)
        return f.id

    # ───────────────────────────── recomputation ─────────────────────────────
    def recompute_all(self):
        """Re‑route every flow after a failure."""
        # reset utilisations
        for _, _, d in self.topo.G.edges(data=True):
            d["util"] = 0

        for f in self.flows.values():
            paths = self.topo.shortest_paths(f.src, f.dst, k=2)
            if not paths:                     # path lost
                continue
            if f.critical and len(paths) > 1:
                f.backup = paths[1]
            f.path = paths[0]
            self._apply_util_change(f.path, f.size)

    # ─────────────────────────── helper methods ──────────────────────────────
    def _apply_util_change(self, path, delta):
        for u, v in zip(path[:-1], path[1:]):
            self.topo.G[u][v]["util"] += delta
