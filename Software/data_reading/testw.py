import win32pipe
import win32file
import pywintypes
import time

pipe_name = r'\\\\.\\pipe\\named_pipe'

# 1. Create the named pipe (Server side)
# PIPE_ACCESS_OUTBOUND means the server can write to the client
pipe_handle = win32pipe.CreateNamedPipe(
    pipe_name,
    win32pipe.PIPE_ACCESS_OUTBOUND,
    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
    1, # Max instances
    65536, # Out buffer size
    65536, # In buffer size
    0, # Default timeout
    None
)

print(f"Waiting for client connection on {pipe_name}...")

# 2. Wait for a client to connect (this call blocks)
win32pipe.ConnectNamedPipe(pipe_handle, None)
print("Client connected!")

# 3. Write data to the pipe
try:
    data = "Hello from the server via pywin32!\n"
    # win32file.WriteFile returns the error code and the number of bytes written
    win32file.WriteFile(pipe_handle, data.encode('utf-8'))
    print(f"Sent: {data.strip()}")
except pywintypes.error as e:
    print(f"WinAPI Error: {e}")
finally:
    # 4. Close the pipe handle
    win32file.CloseHandle(pipe_handle)
    print("Pipe handle closed.")
