import sys

# Dictionary to simulate a set
data_set = {}

def handle_command(command):
    parts = command.split()
    if parts[0] == "insert":
        tuples = parts[1:]
        assert len(tuples) % 2 == 0
        for i in range(0, len(tuples), 2):
            data_set[int(tuples[i])] = int(tuples[i+1])
        return "ok"
    elif parts[0] == "remove":
        keys = parts[1:]
        assert len(keys) > 0
        for key in keys:
            if int(key) in data_set:
                del data_set[int(key)]
        return "ok"
    elif parts[0] == "lookup":
        key = int(parts[1])
        return data_set[key] if key in data_set else "null"
    elif parts[0] == "lowerbound":
        key = int(parts[1])
        keys = list(data_set.keys())
        keys.sort()
        for k in keys:
            if k >= key:
                return data_set[k]
        return "null"
    else:
        return "unknown command"

if __name__ == "__main__":
    for line in sys.stdin:
        command = line.strip()
        if command:
            print(handle_command(command))
            sys.stdout.flush()
