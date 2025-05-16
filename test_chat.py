#!/usr/bin/env python3
import pexpect
import sys
import time

def run_command(child, command, expected_output=None, timeout=30):
    if command is not None:
        print(f"\nExecuting command: {command}")
        child.sendline(command)
    if expected_output:
        try:
            child.expect([expected_output, "command\(h for help\)>"] , timeout=timeout)
            print(f"Output: {child.before}{child.after}")
        except pexpect.TIMEOUT:
            print(f"Timeout waiting for: {expected_output}")
            print(f"Buffer: {child.before}")
            raise
    else:
        try:
            child.expect("command\(h for help\)>", timeout=timeout)
            print(f"Output: {child.before}{child.after}")
        except pexpect.TIMEOUT:
            print("Timeout waiting for command prompt")
            print(f"Buffer: {child.before}")
            raise

def test_chat_program():
    try:
        # Start two instances of the chat program
        print("Starting test sequence...")
        
        user1 = pexpect.spawn('./chat_program', encoding='utf-8', timeout=60)
        user2 = pexpect.spawn('./chat_program', encoding='utf-8', timeout=60)
        
        # Wait for initial prompts
        print("Waiting for initial prompts...")
        user1.expect("command\(h for help\)>")
        user2.expect("command\(h for help\)>")
        
        # User 1 login
        print("\nUser 1 logging in...")
        run_command(user1, "login", "ID:", timeout=60)
        user1.sendline("user1")
        run_command(user1, None, "Password:", timeout=60)
        user1.sendline("pass1")
        run_command(user1, None, "login complete", timeout=60)
        
        # User 2 login
        print("\nUser 2 logging in...")
        run_command(user2, "login", "ID:", timeout=60)
        user2.sendline("user2")
        run_command(user2, None, "Password:", timeout=60)
        user2.sendline("pass2")
        run_command(user2, None, "login complete", timeout=60)
        
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