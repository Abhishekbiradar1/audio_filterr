import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

# Define the desktop and temp directory paths
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
temp_dir = os.path.join(desktop_path, 'temp')

input_file = os.path.abspath(sys.argv[1])
cutoff = float(sys.argv[2])
output_file = os.path.join(temp_dir, f"filtered_{os.path.basename(input_file)}")

print("this is start")

print("Input file:", input_file)
print("Cutoff frequency:", cutoff)

# Load the .wav file
sample_rate, data = wavfile.read(input_file)
# If stereo, convert to mono by averaging the channels
if data.ndim > 1:
    data = data.mean(axis=1)

# Plot the original signal
plt.figure(figsize=(10, 4))
plt.plot(data)
plt.title('Original Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.savefig(os.path.join(temp_dir, 'original_signal.png'))
plt.close()

# Perform Fourier Transform
ft_data = np.fft.fft(data)

# Get the frequency bins
frequencies = np.fft.fftfreq(len(data), 1/sample_rate)

# Plot the magnitude of the Fourier Transform
plt.figure(figsize=(10, 4))
plt.plot(frequencies[:len(frequencies)//2], np.abs(ft_data)[:len(frequencies)//2])
plt.title('Magnitude of Fourier Transform')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.savefig(os.path.join(temp_dir, 'fft_magnitude.png'))
plt.close()

# Create a mask for the frequencies to keep (low-pass filter)
mask = np.abs(frequencies) < cutoff

# Apply the mask to the Fourier Transform data
filtered_ft_data = ft_data * mask

# Plot the filtered magnitude of the Fourier Transform
plt.figure(figsize=(10, 4))
plt.plot(frequencies[:len(frequencies)//2], np.abs(filtered_ft_data)[:len(frequencies)//2])
plt.title('Filtered Magnitude of Fourier Transform')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.savefig(os.path.join(temp_dir, 'filtered_fft_magnitude.png'))
plt.close()

# Perform the inverse Fourier Transform
filtered_data = np.fft.ifft(filtered_ft_data)

# Plot the filtered signal
plt.figure(figsize=(10, 4))
plt.plot(filtered_data.real)
plt.title('Filtered Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.savefig(os.path.join(temp_dir, 'filtered_signal.png'))
plt.close()

# Save the filtered data as a new .wav file
filtered_data_real = np.real(filtered_data).astype(np.int16)
wavfile.write(output_file, sample_rate, filtered_data_real)
print("this is end")
