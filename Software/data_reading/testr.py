import socket

UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on port {UDP_PORT}...")
print("Waiting for data...\n")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Received {len(data)} bytes from {addr}")
    print(f"Data: {data[:50]}...")  # Print first 50 bytes
    print("---")
