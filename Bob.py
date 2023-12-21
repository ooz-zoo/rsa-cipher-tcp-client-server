import socket
import pickle
import tkinter as tk
from tkinter import messagebox

def string_to_int(s):
    """Convert a string to an integer using ASCII encoding."""
    result = 0
    for letter in s:
        result = result * 128 + ord(letter)
    return result

def int_to_string(n):
    """Convert an integer to a string using ASCII encoding."""
    result = ""
    while n > 0:
        result = chr(n % 128) + result
        n = n // 128
    return result

def send_message():
    HOST = "127.0.0.1"
    PORT = 65432

    message = message_entry.get()
    message = string_to_int(message)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        data = s.recv(1024)
        received_key = pickle.loads(data)
        print(f"Received public key: {received_key}")

        n, e = received_key

        if len(bin(message)[2:]) < n.bit_length():
            ciphertext = pow(message, e, n)
            serialized_ciphertext = pickle.dumps(ciphertext)
            s.sendall(serialized_ciphertext)
            messagebox.showinfo("Success", "Message sent successfully")
        else:
            messagebox.showerror("Error", "Message is too large for encryption")

# GUI for Bob
bob_window = tk.Tk()
bob_window.title("Bob - Client")

# Background image
bg_image = tk.PhotoImage(file="eee.png")  # Change the filename to your image file
bg_label = tk.Label(bob_window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

message_label = tk.Label(bob_window, text="Enter your message:")
message_label.pack()

message_entry = tk.Entry(bob_window, font=("Arial", 12))
message_entry.pack()

send_button = tk.Button(bob_window, text="Send Message", command=send_message,
                        font=("Arial", 12), bg="blue", fg="white", activebackground="darkblue", padx=10, pady=5)
send_button.pack()

bob_window.mainloop()











