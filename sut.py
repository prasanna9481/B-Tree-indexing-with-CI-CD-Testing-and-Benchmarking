from tree import BPlusTree
import sys

tree = BPlusTree()

def handle_command(cmd):
    parts = cmd.strip().split()
    if not parts:
        return ""

    op = parts[0]

    if op == 'insert':
        for i in range(1, len(parts), 2):
            k = int(parts[i])
            v = int(parts[i+1])
            tree.insert(k, v)
        return "ok"

    elif op == 'remove':
        for k in parts[1:]:
            tree.remove(int(k))
        return "ok"

    elif op == 'lookup':
        r = tree.lookup(int(parts[1]))
        return str(r) if r is not None else "null"

    elif op == 'lowerbound':
        r = tree.lowerbound(int(parts[1]))
        return str(r) if r is not None else "null"

    return "unknown command"

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        print(handle_command(line))
        sys.stdout.flush()
