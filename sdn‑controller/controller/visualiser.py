# controller/visualiser.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


class Visualiser:
    """
    Live‑updating topology window.
    Uses Matplotlib's GUI timer (FuncAnimation) – safe on Windows because
    all Tk calls stay in the main thread.
    """

    def __init__(self, topo, policies, refresh_ms: int = 1000):
        self.topo = topo
        self.policies = policies
        self.refresh_ms = refresh_ms

        # first figure
        self.fig, self.ax = plt.subplots()
        self.anim = None     # FuncAnimation handle
        self.pos = None      # spring‑layout cache

    # ─────────────────────────── public API (called from CLI) ──────────────
    def draw(self):
        """Open (or reopen) the window and ensure the auto‑refresh timer runs."""
        # Re‑create figure if user closed previous window
        if not plt.fignum_exists(self.fig.number):
            self.fig, self.ax = plt.subplots()
            self.anim = None     # need new timer
            self.pos = None

        # Kick off the animation timer once
        if self.anim is None:
            self.anim = animation.FuncAnimation(
                self.fig,                                            # figure
                lambda frame: self._render(),                       # update fn
                interval=self.refresh_ms, blit=False)

        # Do one immediate render and show the window
        self._render()
        plt.show(block=False)
        plt.pause(0.001)        # lets Tk flush events

    # ─────────────────────────── internal rendering ────────────────────────
    def _render(self):
        """Redraw the topology, link states, and utilisation on self.ax."""
        self.ax.clear()
        G = self.topo.G

        # Re‑layout only if node count changed
        if self.pos is None or len(self.pos) != len(G.nodes):
            self.pos = nx.spring_layout(G, seed=42)

        # Nodes
        nx.draw_networkx_nodes(
            G, self.pos, ax=self.ax, node_size=800, node_color="#ccccff"
        )

        # Edge lists
        up_edges   = [(u, v) for u, v, d in G.edges(data=True) if d["up"]]
        down_edges = [(u, v) for u, v, d in G.edges(data=True) if not d["up"]]

        # Width proportional to utilisation (min 1 px)
        width = [max(1, G[u][v]["util"]) for u, v in up_edges]

        # Draw edges
        nx.draw_networkx_edges(
            G, self.pos, edgelist=up_edges, width=width, ax=self.ax
        )
        nx.draw_networkx_edges(
            G, self.pos, edgelist=down_edges,
            style="dashed", edge_color="red", ax=self.ax
        )

        # Labels
        nx.draw_networkx_labels(G, self.pos, ax=self.ax)

        # Title / axes
        self.ax.set_title("SDN Topology – edge width = utilisation")
        self.ax.axis("off")

        # Tell Matplotlib the canvas changed
        self.fig.canvas.draw_idle()
