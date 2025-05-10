import networkx as nx
from itertools import pairwise

class Topology:
    """Graph wrapper tracking link capacity, utilisation and up/down state."""
    def __init__(self):
        self.G = nx.Graph()

    # ─────────────────────────────────── node ops ────────────────────────────
    def add_node(self, n):
        self.G.add_node(n)

    def remove_node(self, n):
        self.G.remove_node(n)

    # ─────────────────────────────────── link ops ────────────────────────────
    def add_link(self, u, v, capacity=1):
        self.G.add_edge(u, v,
                        capacity=capacity,
                        util=0,
                        up=True,
                        weight=1/capacity)   # inverse capacity = cost

    def remove_link(self, u, v):
        self.G.remove_edge(u, v)

    def fail_link(self, u, v):
        if self.G.has_edge(u, v):
            self.G[u][v]["up"] = False

    def restore_link(self, u, v):
        if self.G.has_edge(u, v):
            self.G[u][v]["up"] = True

    # ────────────────────────────────── path utils ───────────────────────────
    def _active_subgraph(self):
        return self.G.edge_subgraph(
            [(u, v) for u, v, d in self.G.edges(data=True) if d["up"]])

    def shortest_paths(self, src, dst, k=2):
        """Return up to *k* shortest link‑disjoint paths."""
        SG_view = self._active_subgraph()
        SG = nx.Graph(SG_view)
        if not nx.has_path(SG, src, dst):
            return []
        primary = nx.shortest_path(SG, src, dst, weight="weight")
        if k == 1:
            return [primary]
        # second path: remove primary edges to find disjoint backup
        SG.remove_edges_from(pairwise(primary))
        if nx.has_path(SG, src, dst):
            backup = nx.shortest_path(SG, src, dst, weight="weight")
            return [primary, backup]
        return [primary]
