import socket
import os
import hashlib

# Server settings
server_ip = "0.0.0.0"
server_port = 5001
buffer_size = 4096

# Folder to save the received image
save_folder = r"D:\pine academy\aujus technology\image transfer to different folder\server_received_images"
os.makedirs(save_folder, exist_ok=True)

# Start the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print(f"🖥️ Server listening on {server_ip}:{server_port}...")

# Accept client connection
conn, addr = server_socket.accept()
print(f"✅ Connected by {addr}")

# Receive file size
file_size = int(conn.recv(16).decode().strip())
print(f"📦 Expecting {file_size} bytes")

# File path to save the received image
save_path = os.path.join(save_folder, "image.jpg")

# Receive file data
received_bytes = 0
with open(save_path, "wb") as file:
    while received_bytes < file_size:
        chunk = conn.recv(buffer_size)
        if not chunk:
            break
        file.write(chunk)
        received_bytes += len(chunk)

print(f"📂 Image received and saved at: {save_path}")

# Receive and verify MD5 checksum
received_md5 = conn.recv(32).decode()
with open(save_path, "rb") as file:
    file_data = file.read()
computed_md5 = hashlib.md5(file_data).hexdigest()

if received_md5 == computed_md5:
    print(f"✅ Image integrity verified! MD5: {computed_md5}")
else:
    print(f"❌ Corrupted file! MD5 mismatch: Expected {received_md5}, Got {computed_md5}")

conn.close()
server_socket.close()
