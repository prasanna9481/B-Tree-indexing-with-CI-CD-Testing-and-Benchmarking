#include "header.h"

Node::Node(bool leaf, int deg) {
    isLeaf = leaf;
    degree = deg;
    next = nullptr;
}

void Node::insert(int key, double value) {
    int i = 0;
    while (i < keys.size() && keys[i] < key) ++i;

    if (isLeaf) {
        if (i < keys.size() && keys[i] == key)
            values[i] = value;
        else {
            keys.insert(keys.begin() + i, key);
            values.insert(values.begin() + i, value);
        }
    } else {
        Node* child = children[i];
        child->insert(key, value);
        if (child->keys.size() == degree) {
            Node* sibling = child->split();
            keys.insert(keys.begin() + i, sibling->keys[0]);
            children.insert(children.begin() + i + 1, sibling);
        }
    }
}

Node* Node::split() {
    int mid = keys.size() / 2;
    Node* sibling = new Node(isLeaf, degree);

    sibling->keys.assign(keys.begin() + mid, keys.end());
    keys.resize(mid);

    if (isLeaf) {
        sibling->values.assign(values.begin() + mid, values.end());
        values.resize(mid);
        sibling->next = this->next;
        this->next = sibling;
    } else {
        sibling->children.assign(children.begin() + mid + 1, children.end());
        children.resize(mid + 1);
    }

    return sibling;
}

double* Node::lookup(int key) {
    int i = 0;
    while (i < keys.size() && key > keys[i]) ++i;
    if (isLeaf) {
        if (i < keys.size() && keys[i] == key) return &values[i];
        return nullptr;
    }
    return children[i]->lookup(key);
}

double* Node::lowerbound(int key) {
    int i = 0;
    while (i < keys.size() && keys[i] < key) ++i;
    if (isLeaf) {
        if (i < values.size()) return &values[i];
        if (next) return &next->values[0];
        return nullptr;
    }
    return children[i]->lowerbound(key);
}

void Node::remove(int key) {
    int i = 0;
    while (i < keys.size() && keys[i] < key) ++i;

    if (isLeaf) {
        if (i < keys.size() && keys[i] == key) {
            keys.erase(keys.begin() + i);
            values.erase(values.begin() + i);
        }
    } else {
        // Just pass deletion down to the appropriate child (no merge logic)
        if (i < children.size()) {
            children[i]->remove(key);
        }
    }
}

void Node::print() {
    if (isLeaf) {
        for (int i = 0; i < keys.size(); ++i)
            cout << "(" << keys[i] << ", " << values[i] << ") ";
        cout << endl;
    } else {
        for (Node* child : children)
            child->print();
    }
}

BPlusTree::BPlusTree(int deg) {
    degree = deg;
    root = new Node(true, deg);
}

void BPlusTree::insert(int key, double value) {
    root->insert(key, value);
    if (root->keys.size() == degree) {
        Node* newRoot = new Node(false, degree);
        newRoot->children.push_back(root);
        Node* sibling = root->split();
        newRoot->keys.push_back(sibling->keys[0]);
        newRoot->children.push_back(sibling);
        root = newRoot;
    }
}

double* BPlusTree::lookup(int key) {
    return root->lookup(key);
}

double* BPlusTree::lowerbound(int key) {
    return root->lowerbound(key);
}

void BPlusTree::remove(int key) {
    root->remove(key);
}