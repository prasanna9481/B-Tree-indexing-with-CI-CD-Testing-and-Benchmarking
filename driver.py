import sys
import subprocess
import difflib

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 driver.py <test_input_file> <sut_command> [sut_args...]")
        sys.exit(1)

    # Read test input file
    test_input_file = sys.argv[1]
    try:
        with open(test_input_file, 'r') as f:
            test_lines = f.readlines()
    except IOError as e:
        print(f"Error reading test input file: {e}")
        sys.exit(1)

    # Start SUT process
    sut_command = sys.argv[2:]
    try:
        sut_process = subprocess.Popen(sut_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=sys.stderr, text=True)
    except Exception as e:
        print(f"Error starting SUT: {e}")
        sys.exit(1)

    # Process each question/answer pair
    for i in range(0, len(test_lines), 2):
        question = test_lines[i].strip()
        expected_answer = test_lines[i + 1].strip() if i + 1 < len(test_lines) else ""
        
        try:
            # Send question to SUT and capture output
            sut_process.stdin.write(question + "\n")
            sut_process.stdin.flush()
            actual_answer = sut_process.stdout.readline().strip()

            # Check if SUT crashed before reading output
            ret_code = sut_process.poll()
            if ret_code is not None:
                print(f"SUT crashed when handling line {i+1} with question '{question}' with return code {ret_code}")
                sys.exit(1)

            # Check if output matches expected answer
            if actual_answer != expected_answer:
                # Generate and print diff
                diff = difflib.unified_diff(
                    [expected_answer], [actual_answer], 
                    fromfile='expected', tofile='actual', lineterm=''
                )
                print(f"Mismatch found, for input in line {i+1}:")
                print(f"Question: {question}")
                print("\n".join(diff))
                sut_process.terminate()
                sys.exit(1)

        except Exception as e:
            print(f"Error during communication with SUT: {e}")
            sut_process.terminate()
            sys.exit(1)

    # Check if SUT process is still running (no crashes)
    ret_code = sut_process.poll()
    if ret_code is not None:
        print(f"SUT terminated unexpectedly with return code {ret_code}")
    else:
        print("All tests passed.")

    sut_process.terminate()

if __name__ == "__main__":
    main()
