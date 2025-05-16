#include "header.h"
#include <sstream>

string handle_command(const string& command, BPlusTree& tree) {
    stringstream ss(command);
    string op;
    ss >> op;

    if (op == "insert") {
        int k; double v;
        while (ss >> k >> v)
            tree.insert(k, v);
        return "ok";
    } else if (op == "remove") {
        int k;
        while (ss >> k)
            tree.remove(k);
        return "ok";
    } else if (op == "lookup") {
        int k; ss >> k;
        double* val = tree.lookup(k);
        return val ? to_string(*val) : "null";
    } else if (op == "lowerbound") {
        int k; ss >> k;
        double* val = tree.lowerbound(k);
        return val ? to_string(*val) : "null";
    }
    return "unknown command";
}

int main() {
    BPlusTree tree(4);  // fixed degree 4
    string line;
    getline(cin, line);  // skip empty line or config
    while (getline(cin, line)) {
        if (line.empty()) continue;
        cout << handle_command(line, tree) << endl;
        cout.flush();
    }
    return 0;
}