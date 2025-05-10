import cmd, shlex

class ControllerCLI(cmd.Cmd):
    intro = "SDN controller CLI – type help or ? to list commands."
    prompt = "(sdn) "

    def __init__(self, ctrl):
        super().__init__()
        self.c = ctrl

    # ——— node & link ops ————————————————————————————————————————————————
    def do_add_node(self, line):
        """add_node <N>"""
        self.c.add_node(line.strip())

    def do_remove_node(self, line):
        """remove_node <N>"""
        self.c.remove_node(line.strip())

    def do_add_link(self, line):
        """add_link <U> <V> [capacity]"""
        u, v, *rest = shlex.split(line)
        cap = float(rest[0]) if rest else 1
        self.c.add_link(u, v, cap)

    def do_remove_link(self, line):
        """remove_link <U> <V>"""
        u, v = shlex.split(line)
        self.c.remove_link(u, v)

    def do_fail_link(self, line):
        """fail_link <U> <V>"""
        u, v = shlex.split(line)
        self.c.fail_link(u, v)

    # ——— flows ————————————————————————————————————————————————————————
    def do_inject_flow(self, line):
        """inject_flow <SRC> <DST> [size] [priority] [critical]"""
        args = shlex.split(line)
        src, dst = args[:2]
        size = float(args[2]) if len(args) > 2 else 1
        prio = "priority" in args
        crit = "critical" in args
        fid = self.c.inject_flow(src, dst, size, prio, crit)
        print(f"Flow {fid} installed.")

    # ——— visualisation & exit ——————————————————————————————————————————
    def do_show(self, _):
        """show – open / refresh topology window"""
        self.c.show()

    def do_EOF(self, _):
        print()               # newline on Ctrl‑D
        return True
    
    def do_restore_link(self, line):
        """restore_link <U> <V>"""
        u, v = shlex.split(line)
        self.c.restore_link(u, v)

    def do_exit(self, _):
        """exit – quit CLI"""
        return True
