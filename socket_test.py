import socket
import threading
import os
import tkinter as tk
from tkinter import ttk
import hashlib

WINDOW_SIZE = 400
CHUNK_SIZE = 65536 #64KB

#=======TKINTER GUI SETUP========#
root = tk.Tk()
root.title("P2P File Share")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}+50+50")
root.configure(bg="#121212")
theme_buttons = []

# Styling
style = ttk.Style()
style.theme_use("clam")

#======THEME SETUP========#
def set_theme(mode):
    if mode == "dark":
        style.theme_use("default")

        style.configure("TFrame", background="#121212")
        style.configure("Heading.TLabel", background="#121212", foreground="#ffffff")
        style.configure("Form.TLabel", background="#121212", foreground="#ffffff")

        style.configure("Action.TButton", background="#333333", foreground="#ffffff")
        style.configure("Action.TButton", background="#333333", foreground="#ffffff", font=("Segoe UI Emoji", 7), padding=(2, 5))
        style.map("Action.TButton", background=[("active", "#555555")])

        style.configure("TEntry", fieldbackground="#1e1e1e", foreground="#ffffff")

    elif mode == "light":
        style.theme_use("default")

        style.configure("TFrame", background="#f0f0f0")
        style.configure("Heading.TLabel", background="#f0f0f0", foreground="#000000")
        style.configure("Form.TLabel", background="#f0f0f0", foreground="#333333")

        style.configure("Action.TButton", background="#e0e0e0", foreground="#000000")
        style.configure("Action.TButton", background="#e0e0e0", foreground="#000000", font=("Segoe UI Emoji", 7), padding=(2, 5))
        style.map("Action.TButton", background=[("active", "#d0d0d0")])

        style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")


current_theme = "dark"
# Apply theme AFTER style exists
set_theme("dark")


def toggle_theme():
    global current_theme

    if current_theme == "light":
        set_theme("dark")
        current_theme = "dark"
        new_text = "☀"
    else:
        set_theme("light")
        current_theme = "light"
        new_text = "🌙"

    # Update all theme buttons
    for btn in theme_buttons:
        btn.config(text=new_text)

#=====Frame and widget setup========#
def create_theme_button(frame):
    btn = ttk.Button(frame, text="☀" if current_theme == "dark" else "🌙", style="Action.TButton", command=toggle_theme, width=2)
    
    btn.place(relx=0.98, y=5, anchor="ne")# top-right corner
    theme_buttons.append(btn)

#=======Networking code========#
def server_thread(host, port):
    print("{DEBUG} Server thread started on port")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f"[SERVER] Listening on {host}:{port}...")
            conn, addr = s.accept()
            with conn:
                print(f"[SERVER] Connected by {addr}")
                while True:
                    data = conn.recv(CHUNK_SIZE)
                    if not data:
                        break
                    print(f"[SERVER] Received: {data.decode()}")
                    conn.sendall(data)#echo data back
    except OSError as e:
            print(f"[SERVER] Error: {e}")

def client_thread(host, port):
    print("{DEBUG} Client thread started")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"[CLIENT] Connected to {host}:{port}")
            s.sendall(b"HELLO SERVER")#send test message
            data = s.recv(CHUNK_SIZE)
            print(f"[CLIENT] Received from server: {data.decode()}")
    except OSError as e:
        print(f"[CLIENT] Error: {e}")

def start_server():
    host = '127.0.0.1'  # Server always listens on localhost
    try:
        port = int(port_entry_server.get())
        threading.Thread(target=server_thread, args=(host, port), daemon=True).start()
    except ValueError:
        print("[SERVER] Please enter a valid port number.")

def connect_client():
    host = ip_entry.get()
    try:
        port = int(port_entry.get())
        threading.Thread(target=client_thread, args=(host, port), daemon=True).start()
    except ValueError:
        print("[GUI] Invalid port number!")


# Frames
main = ttk.Frame(root, padding=10, style="TFrame")
client_frame = ttk.Frame(root, padding=10, style="TFrame")
client_frame.config(borderwidth=2, relief="raised")
server_frame = ttk.Frame(root, padding=10, style="TFrame")
server_frame.config(borderwidth=2, relief="raised")
create_theme_button(main)#theming button is created for each frame to allow theme switching from any screen
create_theme_button(client_frame)#theming button is created for each frame to allow theme switching from any screen
create_theme_button(server_frame)#thememing button is created for each frame to allow theme switching from any screen


for frame in (main, client_frame, server_frame):
    frame.place(relwidth=1, relheight=1)


def show_frame(frame):
    frame.tkraise()


# Main frame content
title = ttk.Label(main, text="Choose an Action.", style="Heading.TLabel")
title.pack(pady=15)

subtitle = ttk.Label(main, text="Client or Server operation?", style="Form.TLabel")
subtitle.pack(pady=10)

button_frame = ttk.Frame(main)
button_frame.pack(pady=10)

# Buttons
ttk.Button(button_frame, text="Client", style="Action.TButton",
           command=lambda: show_frame(client_frame), cursor="hand2").grid(row=0, column=0, padx=5)

ttk.Button(button_frame, text="Server", style="Action.TButton",
           command=lambda: show_frame(server_frame), cursor="hand2").grid(row=0, column=1, padx=5)

ttk.Button(button_frame, text="Exit", style="Action.TButton",
           command=root.destroy, cursor="X_cursor").grid(row=0, column=2, padx=5)



# Client frame content
client_label = ttk.Label(client_frame, text="Client Operations", style="Heading.TLabel")
client_label.pack(pady=20)

ttk.Label(client_frame, text="IP Address:", style="Form.TLabel").pack(pady=5)
ip_entry = ttk.Entry(client_frame)
ip_entry.pack(padx=10, pady=5)

ttk.Label(client_frame, text="Port:", style="Form.TLabel").pack(pady=5)
port_entry = ttk.Entry(client_frame)
port_entry.pack(padx=10, pady=5)

ttk.Button(client_frame, text="➡ Connect", style="Action.TButton",
           command=connect_client, cursor="watch").pack(pady=5)

ttk.Button(client_frame, text="⬅ Back", style="Action.TButton",
           command=lambda: show_frame(main)).pack(pady=5)


# Server frame content
server_label = ttk.Label(server_frame, text="Server Operations", style="Heading.TLabel")
server_label.pack(pady=20)

ttk.Label(server_frame, text="Port:").pack(pady=5)
port_entry_server = ttk.Entry(server_frame)
port_entry_server.pack(pady=5)

ttk.Button(server_frame, text="⚡ Start Server", style="Action.TButton",
           command=start_server, cursor="watch").pack(pady=5)

ttk.Button(server_frame, text="⬅ Back", style="Action.TButton",
           command=lambda: show_frame(main)).pack(pady=5)


show_frame(main)
root.mainloop()
