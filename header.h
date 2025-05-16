#ifndef bprash_h
#define bprash_h

#include <iostream>
#include <vector>
using namespace std;

struct Node {
    bool isLeaf;
    int degree;
    vector<int> keys;
    vector<double> values;         // only for leaf nodes
    vector<Node*> children;        // only for internal nodes
    Node* next;                    // for leaf chaining

    Node(bool leaf, int deg);
    void insert(int key, double value);
    Node* split();
    double* lookup(int key);
    double* lowerbound(int key);
    void remove(int key);
    void print();
};

struct BPlusTree {
    Node* root;
    int degree;

    BPlusTree(int deg);
    void insert(int key, double value);
    void remove(int key);
    double* lookup(int key);
    double* lowerbound(int key);
};

#endif