
import sys
from bisect import bisect_left, bisect_right



BPLUS_ORDER = 4   # Max children per internal node.  Leaves hold up to ORDER-1 kv pairs.

class LeafNode:
    def __init__(self):
        self.keys = []
        self.values = []
        self.next = None  # pointer to next leaf

    def is_full(self):
        return len(self.keys) >= BPLUS_ORDER

    def insert(self, key, value):
        idx = bisect_left(self.keys, key)
        if idx < len(self.keys) and self.keys[idx] == key:
            self.values[idx] = value
        else:
            self.keys.insert(idx, key)
            self.values.insert(idx, value)

    def split(self):
        mid = len(self.keys) // 2
        sibling = LeafNode()
        sibling.keys   = self.keys[mid:]
        sibling.values = self.values[mid:]
        self.keys      = self.keys[:mid]
        self.values    = self.values[:mid]
        sibling.next   = self.next
        self.next      = sibling
        # promote smallest key in sibling
        return sibling, sibling.keys[0]

    def delete(self, key):
        idx = bisect_left(self.keys, key)
        if idx < len(self.keys) and self.keys[idx] == key:
            self.keys.pop(idx)
            self.values.pop(idx)

    def lookup(self, key):
        idx = bisect_left(self.keys, key)
        if idx < len(self.keys) and self.keys[idx] == key:
            return self.values[idx]
        return None

    def lowerbound(self, key):
        idx = bisect_left(self.keys, key)
        if idx < len(self.keys):
            return self.values[idx]
        return None


class InternalNode:
    def __init__(self):
        self.keys = []       # separation keys
        self.children = []   # pointers to child nodes

    def is_full(self):
        return len(self.children) > BPLUS_ORDER

    def split(self):
        mid = len(self.keys) // 2
        sep = self.keys[mid]
        sibling = InternalNode()
        # keys right of sep go to sibling; sep is removed from parent-level keys
        sibling.keys     = self.keys[mid+1:]
        sibling.children = self.children[mid+1:]
        # shrink self
        self.keys     = self.keys[:mid]
        self.children = self.children[:mid+1]
        return sibling, sep

    def insert_child(self, key, child):
        idx = bisect_right(self.keys, key)
        self.keys.insert(idx, key)
        self.children.insert(idx+1, child)


class BPlusTree:
    def __init__(self):
        self.root = LeafNode()

    def _find_leaf(self, key):
        node = self.root
        while isinstance(node, InternalNode):
            idx = bisect_right(node.keys, key)
            node = node.children[idx]
        return node

    def insert(self, key, value):
        leaf = self._find_leaf(key)
        leaf.insert(key, value)
        if leaf.is_full():
            self._handle_split(leaf)

    def _handle_split(self, node):
        # split node, propagate up
        sibling, sep_key = node.split()
        if node is self.root:
            # new root
            new_root = InternalNode()
            new_root.keys = [sep_key]
            new_root.children = [node, sibling]
            self.root = new_root
            return
        # find parent
        parent = self._find_parent(self.root, node)
        parent.insert_child(sep_key, sibling)
        if parent.is_full():
            self._handle_split(parent)

    def _find_parent(self, current, target):
        # brute-force down the tree to find parent of target
        if isinstance(current, LeafNode):
            return None
        for child in current.children:
            if child is target:
                return current
        for child in current.children:
            if isinstance(child, InternalNode):
                p = self._find_parent(child, target)
                if p:
                    return p
        return None

    def lookup(self, key):
        leaf = self._find_leaf(key)
        return leaf.lookup(key)

    def lowerbound(self, key):
        leaf = self._find_leaf(key)
        # try in this leaf
        val = leaf.lowerbound(key)
        if val is not None:
            return val
        # otherwise scan next leaves
        nxt = leaf.next
        if nxt:
            return nxt.values[0]
        return None

    def remove(self, key):
        leaf = self._find_leaf(key)
        leaf.delete(key)

tree = BPlusTree()

def handle_command(cmd):
    parts = cmd.split()
    op = parts[0]

    if op == 'insert':
        assert (len(parts)-1) % 2 == 0
        for i in range(1, len(parts), 2):
            k = int(parts[i]); v = int(parts[i+1])
            tree.insert(k, v)
        return "ok"

    elif op == 'remove':
        assert len(parts) > 1
        for i in range(1, len(parts)):
            k = int(parts[i])
            tree.remove(k)
        return "ok"

    elif op == 'lookup':
        k = int(parts[1])
        r = tree.lookup(k)
        return str(r) if r is not None else "null"

    elif op == 'lowerbound':
        k = int(parts[1])
        r = tree.lowerbound(k)
        return str(r) if r is not None else "null"

    else:
        return "unknown command"


if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        print(handle_command(line))
        sys.stdout.flush()
