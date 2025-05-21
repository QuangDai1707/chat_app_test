#!/usr/bin/env python3
import subprocess
import time
import os
import signal
import sys
from typing import List, Dict
import threading
import queue
import random

class ChatClient:
    def __init__(self, client_id: int):
        self.client_id = client_id
        self.process = None
        self.command_queue = queue.Queue()
        self.is_running = False
        self.thread = None

    def start(self):
        self.process = subprocess.Popen(
            ['./chat_program'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.is_running = True
        self.thread = threading.Thread(target=self._client_loop)
        self.thread.daemon = True
        self.thread.start()

    def _client_loop(self):
        while self.is_running:
            try:
                cmd = self.command_queue.get(timeout=0.1)
                self._execute_command(cmd)
            except queue.Empty:
                continue

    def _execute_command(self, cmd: str):
        if not self.process:
            return

        if cmd == "login":
            self.process.stdin.write("login\n")
            self.process.stdin.write(f"user{self.client_id % 2 + 1}\n")  # Alternate between user1 and user2
            self.process.stdin.write(f"pass{self.client_id % 2 + 1}\n")
        elif cmd == "logout":
            self.process.stdin.write("logout\n")
        elif cmd == "send":
            self.process.stdin.write("send\n")
        self.process.stdin.flush()

    def stop(self):
        self.is_running = False
        if self.process:
            self.process.terminate()
            self.process.wait()

class Commander:
    def __init__(self, num_clients: int = 100):
        self.num_clients = num_clients
        self.clients: Dict[int, ChatClient] = {}
        self.start_time = None
        self.end_time = None

    def start_test(self):
        print(f"Starting performance test with {self.num_clients} clients...")
        self.start_time = time.time()

        # Spawn all clients
        for i in range(self.num_clients):
            client = ChatClient(i)
            client.start()
            self.clients[i] = client
            time.sleep(0.01)  # Small delay to prevent overwhelming the system

        # Login all clients
        print("Logging in all clients...")
        for client in self.clients.values():
            client.command_queue.put("login")
        time.sleep(2)  # Wait for all logins to complete

    def send_command_to_all(self, command: str):
        print(f"Sending command '{command}' to all clients...")
        for client in self.clients.values():
            client.command_queue.put(command)
        time.sleep(1)  # Wait for commands to complete

    def stop_test(self):
        print("Stopping all clients...")
        for client in self.clients.values():
            client.stop()
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"Test completed in {duration:.2f} seconds")

def main():
    commander = Commander(num_clients=100)
    
    try:
        commander.start_test()
        
        while True:
            print("\nAvailable commands:")
            print("1. send - Send message from all clients")
            print("2. logout - Logout all clients")
            print("3. exit - End the test")
            
            cmd = input("Enter command: ").strip().lower()
            
            if cmd == "exit":
                break
            elif cmd == "send":
                commander.send_command_to_all("send")
            elif cmd == "logout":
                commander.send_command_to_all("logout")
            else:
                print("Invalid command")
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        commander.stop_test()

if __name__ == "__main__":
    main() 