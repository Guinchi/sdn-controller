"""
Simplified SDN controller – entry point
Author : Diego Albertini
Student ID : 890302124

SHA‑256 watermark (890302124 + "NeoDDaBRgX5a9"):
c71113166c53deab112639414771caff4e55ae1eea2c8cf5b6a6dcb83bc33cc1
"""

import argparse
from controller.topology import Topology
from controller.policies import PolicyEngine
from controller.visualiser import Visualiser
from controller.cli import ControllerCLI

class SDNController:
    def __init__(self):
        self.topo = Topology()
        self.policies = PolicyEngine(self.topo)
        self.viz = Visualiser(self.topo, self.policies)

    # — façade exposed to CLI — #
    def add_node(self, n):                self.topo.add_node(n)
    def remove_node(self, n):             self.topo.remove_node(n)
    def add_link(self, u, v, cap=1):      self.topo.add_link(u, v, cap)
    def remove_link(self, u, v):          self.topo.remove_link(u, v)
    def inject_flow(self,*a,**kw):        return self.policies.install_flow(*a, **kw)
    def fail_link(self, u, v):            self.topo.fail_link(u, v); self.policies.recompute_all()
    def restore_link(self, u, v):         self.topo.restore_link(u, v)
    def show(self):                       self.viz.draw()


def main():
    p = argparse.ArgumentParser(description="Launch SDN controller CLI")
    p.add_argument("-i", "--interactive", action="store_true",
                   help="Start interactive shell (recommended)")
    if p.parse_args().interactive:
        ControllerCLI(SDNController()).cmdloop()
    else:
        print("Run with -i for interactive mode.")

if __name__ == "__main__":
    main()
