import win32pipe
import win32file
import pywintypes
import time

pipe_name = r'named_pipe.fifo'

print(f"Attempting to connect to pipe server at {pipe_name}...")

try:
    # Use CreateFile to open the client side of the pipe
    # GENERIC_READ access needed to read
    # OPEN_EXISTING mode to connect to an existing pipe
    handle = win32file.CreateFile(
        pipe_name,
        win32file.GENERIC_READ,
        0, None,
        win32file.OPEN_EXISTING,
        0, None
    )

    # Set the pipe to message mode so we can read discrete messages
    res = win32pipe.SetNamedPipeHandleState(
        handle,
        win32pipe.PIPE_READMODE_MESSAGE,
        None, None
    )

    if res == 0:
        print("SetNamedPipeHandleState failed.")

    print("Connection successful. Reading data...")
    
    # Read the data from the pipe
    # ReadFile returns (error_code, data_read_as_bytes)
    error_code, data = win32file.ReadFile(handle, 4096)
    
    if error_code == 0:
        print(f"Received: {data.decode('utf-8').strip()}")
    else:
        print(f"Error reading from pipe: {error_code}")

except pywintypes.error as e:
    # Error 2 means file not found (server not running/pipe not created)
    # Error 231 means all pipe instances are busy
    print(f"WinAPI Error connecting to pipe: {e}")
finally:
    if 'handle' in locals() and handle:
        win32file.CloseHandle(handle)
        print("Pipe handle closed.")

