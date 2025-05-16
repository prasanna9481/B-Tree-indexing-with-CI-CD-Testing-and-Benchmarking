from bisect import bisect_right
from node import LeafNode, InternalNode  # taking node from same path

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
        sibling, sep_key = node.split()
        if node is self.root:
            new_root = InternalNode()
            new_root.keys = [sep_key]
            new_root.children = [node, sibling]
            self.root = new_root
            return
        parent = self._find_parent(self.root, node)
        parent.insert_child(sep_key, sibling)
        if parent.is_full():
            self._handle_split(parent)

    def _find_parent(self, current, target):
        if isinstance(current, LeafNode):
            return None
        for child in current.children:
            if child is target:
                return current
        for child in current.children:
            if isinstance(child, InternalNode):
                parent = self._find_parent(child, target)
                if parent:
                    return parent
        return None

    def lookup(self, key):
        return self._find_leaf(key).lookup(key)

    def lowerbound(self, key):
        leaf = self._find_leaf(key)
        val = leaf.lowerbound(key)
        return val if val is not None else (leaf.next.values[0] if leaf.next else None)

    def remove(self, key):
        self._find_leaf(key).delete(key)
