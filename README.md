# Chat Program Test Automation

This project contains a simple chat program and its test automation in both C++ and Python.

## Prerequisites for Ubuntu

1. Install required packages:
```bash
sudo apt-get update
sudo apt-get install -y g++ make python3 python3-pip
```

2. Install Python dependencies (for Python test):
```bash
pip3 install pexpect
```

## Building the Programs

1. Build the chat program:
```bash
make clean
make
```

2. Build the C++ test program:
```bash
make test_chat
```

## Running the Tests

You can run either the C++ or Python version of the test:

1. C++ Test:
```bash
./test_chat
```

2. Python Test:
```bash
./test_chat.py
```

## Test Scenario

The test automation simulates two users:
1. Both users log in
2. User 1 sends a message to User 2
3. User 2 sends a message to User 1
4. Both users log out

## Project Structure

- `main.cpp` - The chat program implementation
- `test_chat.cpp` - C++ test automation
- `test_chat.py` - Python test automation
- `Makefile` - Build configuration

## Notes

- The chat program requires a Unix-like environment (Linux/macOS)
- Both test implementations (C++ and Python) provide the same functionality
- The C++ test uses POSIX APIs for process management
- The Python test uses the pexpect library for process interaction 