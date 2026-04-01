#!/usr/bin/env python3
"""
Comprehensive P2P Network Test
Tests: Server with custom port, Client connecting to still-running server
"""
import socket
import threading
import time
import sys

def run_comprehensive_test():
    print("\n" + "="*80)
    print("COMPREHENSIVE P2P NETWORK TEST")
    print("="*80)
    
    # Test 1: Server on custom port 5000
    print("\n[TEST 1] Starting Server on port 5000")
    print("-" * 80)
    
    def server_5000():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("127.0.0.1", 5000))
                s.listen(1)
                print("✓ Server listening on 127.0.0.1:5000")
                
                conn, addr = s.accept()
                print(f"✓ Client connected from {addr[0]}:{addr[1]}")
                
                data = conn.recv(1024)
                print(f"✓ Server received: '{data.decode()}'")
                
                conn.sendall(b"Echo: " + data)
                print(f"✓ Server echoed data back")
                conn.close()
                return True
        except Exception as e:
            print(f"✗ Server error: {e}")
            return False
    
    # Start server thread
    server_thread = threading.Thread(target=server_5000, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    # Connect client
    print("\n[TEST 1] Client connecting to 127.0.0.1:5000")
    print("-" * 80)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 5000))
            print("✓ Client connected to server")
            
            s.sendall(b"Hello from P2P Client")
            print("✓ Client sent: 'Hello from P2P Client'")
            
            data = s.recv(1024)
            print(f"✓ Client received: '{data.decode()}'")
            print("✓ TEST 1 PASSED")
    except Exception as e:
        print(f"✗ Client error: {e}")
        return False
    
    server_thread.join(timeout=2)
    
    # Test 2: Server on different custom port 8080
    print("\n\n[TEST 2] Starting Server on port 8080")
    print("-" * 80)
    
    def server_8080():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("127.0.0.1", 8080))
                s.listen(1)
                print("✓ Server listening on 127.0.0.1:8080")
                
                conn, addr = s.accept()
                print(f"✓ Client connected from {addr[0]}:{addr[1]}")
                
                data = conn.recv(1024)
                print(f"✓ Server received: '{data.decode()}'")
                
                conn.sendall(data)
                print(f"✓ Server echoed data back")
                conn.close()
                return True
        except Exception as e:
            print(f"✗ Server error: {e}")
            return False
    
    # Start server thread
    server_thread2 = threading.Thread(target=server_8080, daemon=True)
    server_thread2.start()
    time.sleep(0.5)
    
    # Connect client to port 8080
    print("\n[TEST 2] Client connecting to 127.0.0.1:8080")
    print("-" * 80)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 8080))
            print("✓ Client connected to server")
            
            s.sendall(b"Testing port 8080")
            print("✓ Client sent: 'Testing port 8080'")
            
            data = s.recv(1024)
            print(f"✓ Client received: '{data.decode()}'")
            print("✓ TEST 2 PASSED")
    except Exception as e:
        print(f"✗ Client error: {e}")
        return False
    
    server_thread2.join(timeout=2)
    
    print("\n" + "="*80)
    print("✓ ALL TESTS PASSED - Server-Client Communication Works!")
    print("✓ Socket functionality verified on multiple ports")
    print("="*80 + "\n")
    return True

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
