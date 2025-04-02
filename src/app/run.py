import tkinter as tk
from tkinter import messagebox

# Placeholder functions for social network operations
def add_user():
    username = entry_username.get()
    if username:
        messagebox.showinfo("Success", f"User '{username}' added to the network!")
        entry_username.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Please enter a username.")

def show_users():
    # Replace with actual logic to fetch users
    users = ["Alice", "Bob", "Charlie"]
    messagebox.showinfo("Users", f"Current users: {', '.join(users)}")

def send_message():
    sender = entry_sender.get()
    receiver = entry_receiver.get()
    message = entry_message.get("1.0", tk.END).strip()
    if sender and receiver and message:
        messagebox.showinfo("Success", f"Message sent from {sender} to {receiver}!")
        entry_sender.delete(0, tk.END)
        entry_receiver.delete(0, tk.END)
        entry_message.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Error", "Please fill in all fields.")

# Create the main window
root = tk.Tk()
root.title("Social Network GUI")

# Add user section
frame_add_user = tk.Frame(root)
frame_add_user.pack(pady=10)

label_username = tk.Label(frame_add_user, text="Username:")
label_username.pack(side=tk.LEFT, padx=5)

entry_username = tk.Entry(frame_add_user)
entry_username.pack(side=tk.LEFT, padx=5)

button_add_user = tk.Button(frame_add_user, text="Add User", command=add_user)
button_add_user.pack(side=tk.LEFT, padx=5)

# Show users section
button_show_users = tk.Button(root, text="Show Users", command=show_users)
button_show_users.pack(pady=10)

# Send message section
frame_send_message = tk.Frame(root)
frame_send_message.pack(pady=10)

label_sender = tk.Label(frame_send_message, text="Sender:")
label_sender.grid(row=0, column=0, padx=5, pady=5)

entry_sender = tk.Entry(frame_send_message)
entry_sender.grid(row=0, column=1, padx=5, pady=5)

label_receiver = tk.Label(frame_send_message, text="Receiver:")
label_receiver.grid(row=1, column=0, padx=5, pady=5)

entry_receiver = tk.Entry(frame_send_message)
entry_receiver.grid(row=1, column=1, padx=5, pady=5)

label_message = tk.Label(frame_send_message, text="Message:")
label_message.grid(row=2, column=0, padx=5, pady=5)

entry_message = tk.Text(frame_send_message, height=5, width=30)
entry_message.grid(row=2, column=1, padx=5, pady=5)

button_send_message = tk.Button(frame_send_message, text="Send Message", command=send_message)
button_send_message.grid(row=3, column=1, pady=10)

# Run the application
root.mainloop()