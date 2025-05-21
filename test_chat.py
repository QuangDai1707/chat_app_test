#!/usr/bin/env python3
import pexpect
import sys
import time

def run_command(child, command, expected_output=None):
    print(f"\nExecuting command: {command}")
    child.sendline(command)
    if expected_output:
        # Wait for output containing the expected string
        child.expect([expected_output, "command\(h for help\)>"])
        print(f"Output: {child.before.decode()}{child.after.decode()}")
    else:
        child.expect("command\(h for help\)>")
        print(f"Output: {child.before.decode()}{child.after.decode()}")

def test_chat_program():
    try:
        # Start two instances of the chat program
        print("Starting test sequence...")
        
        user1 = pexpect.spawn('./chat_program')
        user2 = pexpect.spawn('./chat_program')
        
        # Wait for initial prompts
        print("Waiting for initial prompts...")
        user1.expect("command\(h for help\)>")
        user2.expect("command\(h for help\)>")
        
        # User 1 login
        print("\nUser 1 logging in...")
        run_command(user1, "login")
        user1.expect("ID:")
        user1.sendline("user1")
        user1.expect("Password:")
        user1.sendline("pass1")
        user1.expect("login complete")
        
        # User 2 login
        print("\nUser 2 logging in...")
        run_command(user2, "login")
        user2.expect("ID:")
        user2.sendline("user2")
        user2.expect("Password:")
        user2.sendline("pass2")
        user2.expect("login complete")
        
        # User 1 sends message
        print("\nUser 1 sending message...")
        run_command(user1, "send", "send complete")
        run_command(user1, "Hello from User 1!")
        
        # User 2 sends message
        print("\nUser 2 sending message...")
        run_command(user2, "send", "send complete")
        run_command(user2, "Hello from User 2!")
        
        # User 1 logout
        print("\nUser 1 logging out...")
        run_command(user1, "logout", "logout complete")
        
        # User 2 logout
        print("\nUser 2 logging out...")
        run_command(user2, "logout", "logout complete")
        
        # Quit both programs
        run_command(user1, "quit", "quit")
        run_command(user2, "quit", "quit")
        
        print("\nTest sequence completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during test: {e}")
        return False
    finally:
        # Clean up processes
        try:
            user1.terminate()
            user2.terminate()
        except:
            pass

if __name__ == "__main__":
    success = test_chat_program()
    sys.exit(0 if success else 1) 