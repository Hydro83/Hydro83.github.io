import wave
import numpy as np
import struct

def read_stereo_wav(file_path):
    """
    Read stereo WAV file and return left and right channel samples.

    Parameters:
    - file_path (str): Path to the WAV file.

    Returns:
    - tuple: Left and right channel samples as lists.
    """
    with wave.open(file_path, 'rb') as wav_file:
        if wav_file.getnchannels() != 2:
            raise ValueError("The provided WAV file is not stereo.")

        num_frames = wav_file.getnframes()
        frames = wav_file.readframes(num_frames)
        samples = np.frombuffer(frames, dtype=np.int16)

        left_channel = samples[::2] / 32768.0
        right_channel = samples[1::2] / 32768.0

    return left_channel.tolist(), right_channel.tolist()

def find_first_nonzero_index(channel):
    """
    Find the index of the first nonzero element in the channel.

    Parameters:
    - channel (list): Audio channel samples.

    Returns:
    - int or None: Index of the first nonzero element or None if all values are 0.
    """
    try:
        return next(index for index, value in enumerate(channel) if value != 0)
    except StopIteration:
        return None

# Fadeout list of 660 float number samples from 1 to 0
fadeout_length_in_samples = 660
fadeout_linear = np.linspace(0.0, 1.0, fadeout_length_in_samples).tolist()


# Example usage
bpm = input("Insert BPM: ")
bpm = int(bpm)
length = input("Length of output file - (1) 1/8 or (2) 1/16: ")
if length == "1":
    length = 2
else:
    length = 4

final_length_of_sample = round(((((60000 / bpm) / length * 1000) / 1000) * 44.1))
print("Total length of output file in samples will be:", final_length_of_sample)

input_file_path = input("Wav file name to edit: ")
output_file = input_file_path[: -4] + "_edited" + input_file_path[-4:]
left_samples, right_samples = read_stereo_wav(input_file_path)

first_nonzero_index_left = find_first_nonzero_index(left_samples)
first_nonzero_index_right = find_first_nonzero_index(right_samples)

print("First nonzero index in left channel:", first_nonzero_index_left)
print("First nonzero index in right channel:", first_nonzero_index_right)

# Find which channel comes to non 0 value sample first and cut from that sample both channels
min_index = min(first_nonzero_index_left, first_nonzero_index_right) -1
# Remove all silence from beginning to first non zero value, leaving one zero value at beginning to avoid clicks
left_samples = left_samples[min_index:]
right_samples = right_samples[min_index:]
# Shorten the sample to bpm and choosen 1/8 or 1/16 beat
left_samples = left_samples[:final_length_of_sample]
right_samples = right_samples[:final_length_of_sample]
# Normalize the volume
def normalize_values(numbers, max_abs_value):
    if max_abs_value == 0:
        return numbers
    
    factor = 1 / max_abs_value
    
    normalized_numbers = []
    for x in numbers:
        if x != 0:
            normalized_numbers.append(x * factor)
        else:
            normalized_numbers.append(0)
    
    return normalized_numbers

combined_numbers = left_samples + right_samples
max_abs_value = max(map(abs, combined_numbers))
left_samples = normalize_values(left_samples, max_abs_value)
right_samples = normalize_values(right_samples, max_abs_value)
# Fadeout to zero last 660 samples of a file
# Linearly decrease the last 10 values from 1 to 0
for i in range(660):
    left_samples[-(i + 1)] = left_samples[-(i + 1)] * fadeout_linear[i]
    right_samples[-(i + 1)] = right_samples[-(i + 1)] * fadeout_linear[i]

print ("Sample is normalized!")
print("Values of first 2 samples in left channel", left_samples[:2])
print("Values of first 2 samples in right channel", right_samples[:2])
print("Value of last sample in left channel", left_samples[-1])
print("Value of last sample in right channel", right_samples[-1])
print("Length of left channel in samples", len(left_samples))
print("Length of right channel in samples", len(right_samples))


def create_stereo_wav(left_channel, right_channel, output_file):
    # Check if the lengths of the two channels match
    if len(left_channel) != len(right_channel):
        raise ValueError("The lengths of the left and right channels must be the same.")

    # Set the parameters for the WAV file
    sample_width = 2  # 16-bit audio
    frame_rate = 44100
    num_channels = 2  # Stereo

    # Create a new wave file
    with wave.open(output_file, 'w') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)
        wav_file.setcomptype("NONE", "not compressed")

        # Combine left and right channels into interleaved samples
        interleaved_samples = []
        for left, right in zip(left_channel, right_channel):
            interleaved_samples.append(struct.pack("<h", int(left * 32767)))  # left channel
            interleaved_samples.append(struct.pack("<h", int(right * 32767)))  # right channel

        # Write the interleaved samples to the WAV file
        wav_file.writeframes(b''.join(interleaved_samples))

create_stereo_wav(left_samples, right_samples, output_file)
print ("Edited file created:", output_file)
input("Press ENTER to exit")
