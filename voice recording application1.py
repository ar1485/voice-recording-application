import sounddevice as sd
import wave
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Recording parameters
fs = 44100  # Sample rate (Hz)
duration = 10  # Default duration for the recording (seconds)
channels = 2  # Number of audio channels (stereo)

# Initialize recording variables
recording = None
is_recording = False

def start_recording():
    global recording, is_recording
    is_recording = True
    # Start recording (non-blocking mode)
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='int16')
    status_label.config(text="Recording...")

def stop_recording():
    global is_recording
    if is_recording:
        sd.stop()  # Stop the recording
        status_label.config(text="Recording Stopped")
        is_recording = False
    else:
        messagebox.showwarning("Warning", "No active recording to stop.")

def save_recording():
    global recording
    if recording is None or is_recording:
        messagebox.showwarning("Warning", "No recording available to save.")
        return
    
    filename = file_entry.get()
    if not filename:
        messagebox.showwarning("Warning", "Please enter a file name.")
        return

    if not filename.endswith(".wav"):
        filename += ".wav"

    try:
        # Save the recorded data as a WAV file
        with wave.open(filename, 'w') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # Sample width in bytes
            wf.setframerate(fs)
            wf.writeframes(recording.tobytes())
        messagebox.showinfo("Success", f"Recording saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the file: {str(e)}")

# Create the tkinter GUI
root = tk.Tk()
root.title("Simple Voice Recorder")

# GUI components
file_label = tk.Label(root, text="Filename:")
file_label.grid(row=0, column=0, padx=10, pady=10)

file_entry = tk.Entry(root)
file_entry.grid(row=0, column=1, padx=10, pady=10)

start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.grid(row=1, column=0, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.grid(row=1, column=1, padx=10, pady=10)

save_button = tk.Button(root, text="Save Recording", command=save_recording)
save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

status_label = tk.Label(root, text="Idle", fg="blue")
status_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the tkinter event loop
root.mainloop()
