import socket
import threading
import tkinter as tk
from tkinter import ttk
import platform


# ===== DPI for Windows =====
if platform.system() == "Windows":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

WINDOW_SIZE = 450
CHUNK_SIZE = 65536

# ===== TKINTER SETUP =====
root = tk.Tk()
root.title("P2P File Share")

#set window taskbar icon:
try:
    icon = tk.PhotoImage(file="fionn_logo.png")  # must be PNG or GIF
    root.iconphoto(True, icon)
except Exception as e:
    print(f"Failed to set icon: {e}")

root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}+50+50")
root.configure(bg="#121212")

theme_buttons = []
theme_labels = []

# ===== HELPERS =====
def add_label(frame, text, style_name, pady=5, pack=True):
    lbl = ttk.Label(frame, text=text, style=style_name)
    if pack:
        lbl.pack(pady=pady)
    theme_labels.append(lbl)
    return lbl

# ===== THEME =====
style = ttk.Style()
style.theme_use("alt")

def set_theme(mode):
    global btn_bg, btn_fg, btn_active_bg
    if mode == "dark":
        btn_bg = "#2b2b2b"
        btn_fg = "#ffffff"
        btn_active_bg = "#3a3a3a"
        style.configure("TFrame", background="#121212")
        style.configure("Heading.TLabel", background="#121212", foreground="#ffffff", font=("Segoe UI Emoji", 12))
        style.configure("Form.TLabel", background="#121212", foreground="#ffffff", font=("Segoe UI Emoji", 11))
        style.configure("Action.TButton",  background="#2b2b2b", foreground="#ffffff", font=("Segoe UI Emoji", 11), padding=(5,5))
        style.map("Action.TButton", background=[("active", "#3a3a3a"), ("pressed", "#1f1f1f")], foreground=[("disabled", "#888888")])
        style.configure("TEntry", fieldbackground="#1e1e1e", foreground="#ffffff")
    else:
        btn_bg = "#e0e0e0"
        btn_fg = "#000000"
        btn_active_bg = "#d0d0d0"
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Heading.TLabel", background="#f0f0f0", foreground="#000000", font=("Segoe UI Emoji", 12))
        style.configure("Form.TLabel", background="#f0f0f0", foreground="#333333", font=("Segoe UI Emoji", 11))

        style.configure("Action.TButton", background="#e0e0e0", foreground="#000000", font=("Segoe UI Emoji", 11), padding=(5,5))
        style.map("Action.TButton", background=[("active", "#d0d0d0"), ("pressed", "#c0c0c0")], foreground=[("disabled", "#888888")])
        style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")

current_theme = "dark"
set_theme(current_theme)

def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    set_theme(current_theme)
    for btn in theme_buttons:
        btn.config(text="🌙" if current_theme == "light" else "☀")

def create_theme_button(frame):
    btn = ttk.Button(frame, text="☀", command=toggle_theme, width=3)
    btn.place(relx=0.98, y=8, anchor="ne")
    theme_buttons.append(btn)

# ===== NETWORKING =====
def server_thread(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                switch_frame_safe(connected_frame)
                root.after(0, lambda: connected_label.config(text=f"Client connected: {addr}"))
    except OSError as e:
        update_status(server_status, f"Server Error: {e}")

def client_thread(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            switch_frame_safe(connected_frame)
    except OSError as e:
        update_status(client_status, f"Connection Error: {e}")

def start_server():
    try:
        port = int(port_entry_server.get())
        threading.Thread(target=server_thread, args=('0.0.0.0', port), daemon=True).start()
    except ValueError:
        print("Invalid port")

def connect_client():
    try:
        port = int(port_entry.get())
        threading.Thread(target=client_thread, args=(ip_entry.get(), port), daemon=True).start()
    except ValueError:
        print("Invalid port")

# ===== FRAMES =====
main = ttk.Frame(root, padding=15)
client_frame = ttk.Frame(root, padding=15)
server_frame = ttk.Frame(root, padding=15)
connected_frame = ttk.Frame(root, padding=15)

for f in (main, client_frame, server_frame, connected_frame):
    f.place(relwidth=1, relheight=1)
    create_theme_button(f)

# ===== STATUS LABELS =====
client_status = add_label(client_frame, "Status: Not connected.", "Form.TLabel", pack=False)
client_status.place(x=10, rely=1.0, anchor="sw")

server_status = add_label(server_frame, "Status: Waiting...", "Form.TLabel", pack=False)
server_status.place(x=10, rely=1.0, anchor="sw")

# ===== HELPERS =====
def show_frame(frame):
    frame.tkraise()
def switch_frame_safe(frame):
    root.after(0, lambda: show_frame(frame))
def update_status(label, text):
    root.after(0, lambda: label.config(text=text))
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
def update_ip_label():
    ip_label_client.config(text=f"Your IP: {get_local_ip()}")
    ip_label_server.config(text=f"Your IP: {get_local_ip()}")
    root.after(5000, update_ip_label)

# ===== MAIN UI =====
add_label(main, "Choose an Action.", "Heading.TLabel", pady=20)
add_label(main, "Client or Server?", "Form.TLabel", pady=10)

button_frame = ttk.Frame(main)
button_frame.pack(pady=15, fill="x")
button_frame.columnconfigure((0,1,2), weight=1)  # columns equally expand

client_btn = tk.Button(button_frame, text="Client", command=lambda: show_frame(client_frame))
client_btn.grid(row=0, column=0, padx=5, sticky="ew")

server_btn = tk.Button(button_frame, text="Server", command=lambda: show_frame(server_frame))
server_btn.grid(row=0, column=1, padx=5, sticky="ew")

exit_btn = tk.Button(button_frame, text="Exit", command=root.destroy)
exit_btn.grid(row=0, column=2, padx=5, sticky="ew")

def rearrange_buttons(event):
    if event.width < 450:
        client_btn.grid_configure(row=0, column=0)
        server_btn.grid_configure(row=1, column=0)
        exit_btn.grid_configure(row=2, column=0)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=0)
        button_frame.columnconfigure(2, weight=0)
    else:
        client_btn.grid_configure(row=0, column=0)
        server_btn.grid_configure(row=0, column=1)
        exit_btn.grid_configure(row=0, column=2)
        button_frame.columnconfigure((0,1,2), weight=1)

main.bind("<Configure>", rearrange_buttons)

# ===== CLIENT UI =====
add_label(client_frame, "Client Operations", "Heading.TLabel", pady=20)
add_label(client_frame, "IP Address:", "Form.TLabel")
ip_entry = ttk.Entry(client_frame, justify="center")
ip_entry.pack(fill="x", padx=10)
add_label(client_frame, "Port:", "Form.TLabel")
port_entry = ttk.Entry(client_frame, justify="center")
port_entry.pack(fill="x", padx=10)
tk.Button(client_frame, text="🔌 Connect", command=connect_client).pack(pady=10)
tk.Button(client_frame, text="⬅️ Back", command=lambda: show_frame(main)).pack()

# ===== SERVER UI =====
add_label(server_frame, "Server Operations", "Heading.TLabel", pady=20)
add_label(server_frame, "Port:", "Form.TLabel")
port_entry_server = ttk.Entry(server_frame, justify="center")
port_entry_server.pack(fill="x", padx=10)
tk.Button(server_frame, text="⚡Start", command=start_server).pack(pady=10)
tk.Button(server_frame, text="⬅️ Back", command=lambda: show_frame(main)).pack()

# ===== CONNECTED FRAME =====
connected_label = add_label(connected_frame, "Connected!", "Heading.TLabel", pady=30)

# ===== IP LABELS =====
ip_label_client = add_label(client_frame, "", "Form.TLabel", pack=False)
ip_label_client.place(x=10, y=10)
ip_label_server = add_label(server_frame, "", "Form.TLabel", pack=False)
ip_label_server.place(x=10, y=10)
update_ip_label()

show_frame(main)
root.mainloop()