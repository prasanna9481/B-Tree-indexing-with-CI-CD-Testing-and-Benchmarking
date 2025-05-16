from bisect import bisect_left, bisect_right

BPLUS_ORDER = 4

class LeafNode:
    def __init__(self):
        self.keys = []
        self.values = []
        self.next = None

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
        sibling.keys = self.keys[mid:]
        sibling.values = self.values[mid:]
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        sibling.next = self.next
        self.next = sibling
        return sibling, sibling.keys[0]

    def delete(self, key):
        idx = bisect_left(self.keys, key)
        if idx < len(self.keys) and self.keys[idx] == key:
            self.keys.pop(idx)
            self.values.pop(idx)

    def lookup(self, key):
        idx = bisect_left(self.keys, key)
        return self.values[idx] if idx < len(self.keys) and self.keys[idx] == key else None

    def lowerbound(self, key):
        idx = bisect_left(self.keys, key)
        return self.values[idx] if idx < len(self.keys) else None


class InternalNode:
    def __init__(self):
        self.keys = []
        self.children = []

    def is_full(self):
        return len(self.children) > BPLUS_ORDER

    def split(self):
        mid = len(self.keys) // 2
        sep = self.keys[mid]
        sibling = InternalNode()
        sibling.keys = self.keys[mid+1:]
        sibling.children = self.children[mid+1:]
        self.keys = self.keys[:mid]
        self.children = self.children[:mid+1]
        return sibling, sep

    def insert_child(self, key, child):
        idx = bisect_right(self.keys, key)
        self.keys.insert(idx, key)
        self.children.insert(idx+1, child)
