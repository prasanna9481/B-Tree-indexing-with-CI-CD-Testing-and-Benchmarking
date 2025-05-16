#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
using namespace std;

const int BPLUS_ORDER = 4;

class LeafNode;

class Node {
public:
    virtual ~Node() {}
    virtual bool isLeaf() const = 0;
};

class LeafNode : public Node {
public:
    vector<int> keys;
    vector<int> values;
    LeafNode* next;

    LeafNode() : next(nullptr) {}

    bool isLeaf() const override { return true; }

    bool isFull() const {
        return keys.size() >= BPLUS_ORDER;
    }

    void insert(int key, int value) {
        auto it = lower_bound(keys.begin(), keys.end(), key);
        int idx = it - keys.begin();
        if (it != keys.end() && *it == key) {
            values[idx] = value;
        } else {
            keys.insert(it, key);
            values.insert(values.begin() + idx, value);
        }
    }

    void remove(int key) {
        auto it = lower_bound(keys.begin(), keys.end(), key);
        int idx = it - keys.begin();
        if (it != keys.end() && *it == key) {
            keys.erase(it);
            values.erase(values.begin() + idx);
        }
    }

    int* lookup(int key) {
        auto it = lower_bound(keys.begin(), keys.end(), key);
        int idx = it - keys.begin();
        if (it != keys.end() && *it == key) {
            return &values[idx];
        }
        return nullptr;
    }

    int* lowerbound(int key) {
        auto it = lower_bound(keys.begin(), keys.end(), key);
        int idx = it - keys.begin();
        if (it != keys.end()) {
            return &values[idx];
        }
        return nullptr;
    }
};

class InternalNode : public Node {
public:
    vector<int> keys;
    vector<Node*> children;

    bool isLeaf() const override { return false; }

    bool isFull() const {
        return children.size() > BPLUS_ORDER;
    }
};

class BPlusTree {
private:
    Node* root;

    LeafNode* findLeaf(int key) {
        Node* node = root;
        while (!node->isLeaf()) {
            InternalNode* internal = static_cast<InternalNode*>(node);
            int i = upper_bound(internal->keys.begin(), internal->keys.end(), key) - internal->keys.begin();
            node = internal->children[i];
        }
        return static_cast<LeafNode*>(node);
    }

public:
    BPlusTree() {
        root = new LeafNode();
    }

    void insert(int key, int value) {
        LeafNode* leaf = findLeaf(key);
        leaf->insert(key, value);
        // Splitting not implemented here yet
    }

    void remove(int key) {
        LeafNode* leaf = findLeaf(key);
        leaf->remove(key);
    }

    string lookup(int key) {
        LeafNode* leaf = findLeaf(key);
        int* result = leaf->lookup(key);
        return result ? to_string(*result) : "null";
    }

    string lowerbound(int key) {
        LeafNode* leaf = findLeaf(key);
        int* result = leaf->lowerbound(key);
        if (result) return to_string(*result);
        if (leaf->next) return to_string(leaf->next->values[0]);
        return "null";
    }
};

BPlusTree tree;

string handle_command(const string& line) {
    stringstream ss(line);
    string op;
    ss >> op;

    if (op == "insert") {
        vector<int> args;
        int x;
        while (ss >> x) args.push_back(x);
        for (size_t i = 0; i < args.size(); i += 2)
            tree.insert(args[i], args[i + 1]);
        return "ok";
    } else if (op == "remove") {
        int x;
        while (ss >> x) tree.remove(x);
        return "ok";
    } else if (op == "lookup") {
        int k;
        ss >> k;
        return tree.lookup(k);
    } else if (op == "lowerbound") {
        int k;
        ss >> k;
        return tree.lowerbound(k);
    }
    return "unknown command";
}

int main() {
    string line;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        cout << handle_command(line) << endl;
    }
    return 0;
}
