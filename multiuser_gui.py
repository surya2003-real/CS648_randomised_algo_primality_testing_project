import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
import os
from rsa import RSAKeyGenerator, encrypt_data, decrypt_data

USERS_FILE = "users.json"

def load_users():
    """Load the registered users from a JSON file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save the users dictionary to a JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

class MultiUserEncryptionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-User Secure File Encryption with RSA")
        self.geometry("800x600")
        self.users = load_users()  # Dictionary mapping username to public key.
        self.create_widgets()

    def create_widgets(self):
        # Registration Frame
        reg_frame = tk.LabelFrame(self, text="User Registration")
        reg_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(reg_frame, text="Username:").pack(side="left", padx=5)
        self.reg_username_entry = tk.Entry(reg_frame)
        self.reg_username_entry.pack(side="left", padx=5)

        tk.Label(reg_frame, text="Bit Length:").pack(side="left", padx=5)
        self.reg_bit_length_entry = tk.Entry(reg_frame, width=8)
        self.reg_bit_length_entry.pack(side="left", padx=5)
        self.reg_bit_length_entry.insert(0, "16")  # For demo purposes

        tk.Button(reg_frame, text="Register User", command=self.register_user).pack(side="left", padx=5)

        # Encryption Frame
        # In create_widgets() within multiuser_gui.py
        enc_frame = tk.LabelFrame(self, text="File Encryption")
        enc_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(enc_frame, text="Select Username:").pack(side="left", padx=5)
        self.enc_username_var = tk.StringVar(enc_frame)
        # Set default: if there is a user, use it; otherwise, use a placeholder.
        default_user = next(iter(self.users)) if self.users else "Select User"
        self.enc_username_var.set(default_user)
        # Initialize OptionMenu with just the default value.
        self.enc_user_menu = tk.OptionMenu(enc_frame, self.enc_username_var, default_user)
        self.enc_user_menu.pack(side="left", padx=5)
        self.update_user_options()  # Update the OptionMenu with all registered users
        
        tk.Button(enc_frame, text="Encrypt File", command=self.encrypt_file).pack(side="left", padx=5)

        # Decryption Frame
        dec_frame = tk.LabelFrame(self, text="File Decryption")
        dec_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(dec_frame, text="Username:").pack(side="left", padx=5)
        self.dec_username_entry = tk.Entry(dec_frame)
        self.dec_username_entry.pack(side="left", padx=5)

        tk.Button(dec_frame, text="Select Private Key File", command=self.select_private_key).pack(side="left", padx=5)
        tk.Button(dec_frame, text="Decrypt File", command=self.decrypt_file).pack(side="left", padx=5)

        self.status_label = tk.Label(self, text="Status: Idle", anchor="w", justify="left")
        self.status_label.pack(fill="both", padx=10, pady=10)

        # Hold private key path for decryption.
        self.private_key_path = None

    def update_user_options(self):
        """Update the dropdown list of registered usernames."""
        # Clear the current menu
        menu = self.enc_user_menu["menu"]
        menu.delete(0, "end")
        
        # If there are users, add each one as an option
        if self.users:
            # Sort keys if you want a consistent order
            user_list = sorted(self.users.keys())
            for username in user_list:
                menu.add_command(
                    label=username,
                    command=lambda value=username: self.enc_username_var.set(value)
                )
            # Set default selection to the first username
            self.enc_username_var.set(user_list[0])
        else:
            # When no users are available, set a placeholder
            self.enc_username_var.set("Select User")



    def register_user(self):
        username = self.reg_username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return
        if username in self.users:
            messagebox.showerror("Error", "Username already exists.")
            return
        try:
            bit_length = int(self.reg_bit_length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid bit length.")
            return

        self.status_label.config(text="Generating RSA keys for user...")
        self.update_idletasks()
        rsa_gen = RSAKeyGenerator(bit_length=bit_length)
        public_key, private_key = rsa_gen.generate_keys()

        # Store public key (as a list for JSON compatibility).
        self.users[username] = list(public_key)
        save_users(self.users)
        self.update_user_options()  # update OptionMenu after registration

        # Prompt user to save their private key.
        file_path = filedialog.asksaveasfilename(
            title="Save Your Private Key", defaultextension=".key",
            filetypes=[("Key Files", "*.key")]
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write(str(private_key))
            messagebox.showinfo("Registration Complete", f"User '{username}' registered successfully.\nPrivate key saved to {file_path}")
            self.status_label.config(text=f"User '{username}' registered successfully.")
        else:
            messagebox.showwarning("Warning", "Private key not saved. Registration aborted.")
            # Remove user since private key wasn't saved.
            del self.users[username]
            save_users(self.users)
            self.update_user_options()
            self.status_label.config(text="Registration aborted.")


    def encrypt_file(self):
        username = self.enc_username_var.get().strip()
        if username not in self.users:
            messagebox.showerror("Error", "Selected user not found.")
            return

        public_key = tuple(self.users[username])
        file_path = filedialog.askopenfilename(title="Select a file to encrypt")
        if not file_path:
            return

        self.status_label.config(text="Encrypting file...")
        self.update_idletasks()
        with open(file_path, "rb") as f:
            data = f.read()

        encrypted_chunks = encrypt_data(data, public_key)
        enc_file = file_path + ".enc"
        with open(enc_file, "w") as f:
            for c in encrypted_chunks:
                f.write(str(c) + "\n")
        self.status_label.config(text=f"File encrypted and saved as:\n{enc_file}")

    def select_private_key(self):
        self.private_key_path = filedialog.askopenfilename(
            title="Select Your Private Key File", filetypes=[("Key Files", "*.key")]
        )
        if self.private_key_path:
            self.status_label.config(text=f"Private key file selected:\n{self.private_key_path}")

    def decrypt_file(self):
        username = self.dec_username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username for decryption.")
            return
        if not self.private_key_path:
            messagebox.showerror("Error", "Please select a private key file first.")
            return
        # Ask for encrypted file
        file_path = filedialog.askopenfilename(
            title="Select the encrypted file", filetypes=[("Encrypted Files", "*.enc")]
        )
        if not file_path:
            return

        # Read private key from file (expecting string representation of a tuple).
        try:
            with open(self.private_key_path, "r") as f:
                key_str = f.read().strip()
            private_key = eval(key_str)  # Use caution: eval() assumes trusted input.
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load private key: {e}")
            return

        self.status_label.config(text="Decrypting file...")
        self.update_idletasks()
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            encrypted_chunks = [int(line.strip()) for line in lines]
            decrypted_bytes = decrypt_data(encrypted_chunks, private_key)
        except OverflowError as oe:
            messagebox.showerror("Decryption Error", "Decryption failed. Incorrect private key or username may have been provided.")
            self.status_label.config(text="Decryption failed due to an incorrect key.")
            return
        except Exception as e:
            messagebox.showerror("Decryption Error", f"An error occurred during decryption: {e}")
            self.status_label.config(text="Decryption failed.")
            return

        dec_file = file_path.replace(".enc", ".dec")
        with open(dec_file, "wb") as f:
            f.write(decrypted_bytes)
        self.status_label.config(text=f"File decrypted and saved as:\n{dec_file}")


if __name__ == "__main__":
    app = MultiUserEncryptionApp()
    app.mainloop()
