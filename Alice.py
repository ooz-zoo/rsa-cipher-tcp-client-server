import socket
import pickle
import random
import tkinter as tk
from tkinter import messagebox
from threading import Thread

def is_probably_prime(n, k=5):
    """Test if a number is probably prime using Miller-Rabin test."""
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generate_rsa_keypair(bit_length=512):
    """Generate a RSA key pair using random prime numbers."""
    while True:
        p = random.getrandbits(bit_length)
        if is_probably_prime(p):
            break

    while True:
        q = random.getrandbits(bit_length)
        if is_probably_prime(q) and q != p:
            break

    n = p * q
    totient = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, totient)

    return n, totient, e, d

def int_to_string(n):
    """Convert an integer to a string using ASCII encoding."""
    result = ""
    while n > 0:
        result = chr(n % 128) + result
        n = n // 128
    return result

def print_ciphertext(ciphertext):
    #messagebox.showinfo("Ciphertext Received", f"Ciphertext: {ciphertext}")
    print(f"Ciphertext received: {ciphertext}")

def start_server():
    #we use "127.0.0.1" because the client and server are on the same machine,
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        update_status(f"Server Listening for connections on {HOST}:{PORT}...")

        conn, addr = s.accept()
        with conn:
            update_status(f"Connected by {addr}")

            n, totient, e, d = generate_rsa_keypair()
            public_key = (n, e)
            serialized_key = pickle.dumps(public_key)
            conn.sendall(serialized_key) 

            ciphertext = pickle.loads(conn.recv(1024))
            print_ciphertext(ciphertext)

            plaintext = int_to_string(pow(ciphertext, d, n))
            update_status(f"Message received: {plaintext}")

def update_status(message):
    status_label.config(text=message)

def clear_status():
    # Clear the status after the delay
    status_label.config(text="")


# GUI
alice_window = tk.Tk()
alice_window.title("Alice - Server")

# Background image
bg_image = tk.PhotoImage(file="see.png")  # Change the filename to your image file
bg_label = tk.Label(alice_window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

status_label = tk.Label(alice_window, text="Server not started", padx=100, pady=100)
status_label.pack()

start_button = tk.Button(alice_window, text="Start Server", command=lambda: Thread(target=start_server).start(),
                         font=("Arial", 12), bg="green", fg="white", activebackground="darkgreen", padx=10, pady=5)
start_button.pack()

alice_window.mainloop()
















