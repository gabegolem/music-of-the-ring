# pip install python-osc
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("172.20.10.3", 8000)
client.send_message("/boxing/data_reading", [123, 0.5])
print("Sent test message")
