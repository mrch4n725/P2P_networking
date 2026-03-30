import tkinter as tk
from tkinter import ttk

WINDOW_SIZE = 400

#Basic window setup
root = tk.Tk()
root.title("P2P File Share")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}+50+50")
root.configure(bg="#121212")#dark background color for better aesthetics and reduced eye strain

#Styling
style = ttk.Style()
style.theme_use("clam")#using clam theme for better aesthetics in dark mode

style.configure("Heading.TLabel", font=("Helvetica", 18, "bold"), background="#121212", foreground="#ffffff")#heading color is set to white for better visibility against the dark background
style.configure("Form.TLabel", font=("JetBrains Mono", 12), background="#121212", foreground="#dddddd")#label color is set to a lighter shade for better visibility against the dark background
style.configure("Action.TButton", font=("Segoe UI", 12), background="#333333", foreground="#ffffff")#button color is set to a darker shade for better contrast
style.configure("TFrame", background="#121212")#entire background changes to black for dark mode

style.map("Action.TButton", background=[("active", "#555555")])#button color changes to a lighter shade when hovered for better user feedback

#entries
style.configure("TEntry", fieldbackground="#1e1e1e", foreground="#ffffff")#entry background is set to a dark shade for better aesthetics and reduced eye strain, text color is set to white for better visibility

#function to output connection info to console
def connect_client():
    ip = ip_entry.get()
    port = port_entry.get()
    print(f"Connecting to {ip}:{port}...")  # Placeholder for actual connection

def start_server():
    port = port_entry_server.get()
    print(f"Starting server on port {port}...")  # Placeholder for actual server start

# Frames
main = ttk.Frame(root, padding=10, style="TFrame")
client_frame = ttk.Frame(root, padding=10, style="TFrame")
client_frame.config(borderwidth=2, relief="raised")
server_frame = ttk.Frame(root, padding=10, style="TFrame")
server_frame.config(borderwidth=2, relief="raised")

# Use ONLY place (remove grid calls)
for frame in (main, client_frame, server_frame):
    frame.place(relwidth=1, relheight=1)

# Main frame content
title = ttk.Label(main, text="Choose an Action.", style="Heading.TLabel")
title.pack(pady=15)

subtitle = ttk.Label(main, text="Client or Server operation?", style="Form.TLabel")
subtitle.pack(pady=10)

# Button frame (NOW properly placed)
button_frame = ttk.Frame(main)
button_frame.pack(pady=10)

def show_frame(frame):
    frame.tkraise()

# Buttons (NOW functional)
ttk.Button(button_frame, text="Client", style="Action.TButton", command=lambda: show_frame(client_frame), cursor="hand2").grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Server", style="Action.TButton", command=lambda: show_frame(server_frame), cursor="hand2").grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Exit", style="Action.TButton", command=root.destroy, cursor="X_cursor").grid(row=0, column=2, padx=5)

#client frame content
client_label = ttk.Label(client_frame, text="Client Operations", style="Heading.TLabel")
client_label.pack(pady=20)

ttk.Label(client_frame, text="IP Address:", style="Form.TLabel").pack(pady=5)
ip_entry = ttk.Entry(client_frame)
ip_entry.pack(padx=10, pady=5)

ttk.Label(client_frame, text="Port:", style="Form.TLabel").pack(pady=5)
port_entry = ttk.Entry(client_frame)
port_entry.pack(padx=10, pady=5)

ttk.Button(client_frame, text="➡ Connect", style="Action.TButton", command=connect_client, cursor="watch").pack(pady=5)
ttk.Button(client_frame, text="⬅ Back", style="Action.TButton", command=lambda: show_frame(main)).pack(pady=5)


#server frame content
server_label = ttk.Label(server_frame, text="Server Operations", style="Heading.TLabel")
server_label.pack(pady=20)

ttk.Label(server_frame, text="Port:").pack(pady=5)
port_entry_server = ttk.Entry(server_frame)
port_entry_server.pack(pady=5)

ttk.Button(server_frame, text="⚡ Start Server", style="Action.TButton", command=start_server, cursor="watch").pack(pady=5)
ttk.Button(server_frame, text="⬅ Back", style="Action.TButton", command=lambda: show_frame(main)).pack(pady=5)


# Show main frame first
show_frame(main)

root.mainloop()