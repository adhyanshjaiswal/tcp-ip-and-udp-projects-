import socket
import os
import hashlib

# Client settings
server_ip = "127.0.0.1"  # Change to server's IP if needed
server_port = 5001
buffer_size = 4096

# Path to the image being sent
image_path = r"D:\pine academy\aujus technology\image transfer to different folder\image.jpg"

# Verify the file exists
if not os.path.exists(image_path):
    print(f"❌ File not found: {image_path}")
    exit()

# Compute MD5 hash for verification
def compute_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while chunk := file.read(buffer_size):
            hasher.update(chunk)
    return hasher.hexdigest()

md5_hash = compute_md5(image_path)
file_size = os.path.getsize(image_path)

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Send file size
client_socket.send(f"{file_size:16}".encode())

# Send the image
with open(image_path, "rb") as file:
    while chunk := file.read(buffer_size):
        client_socket.send(chunk)

# Send MD5 hash for verification
client_socket.send(md5_hash.encode())

print(f"✅ Image sent successfully! MD5 Hash: {md5_hash}")

client_socket.close()
