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
        global sample_rate
        sample_rate = wav_file.getframerate()

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
root_note = input("Insert root note (c, c#, d, d#...): ")
if root_note == "c":
    root_note = 48
elif root_note == "c#":
    root_note = 49
elif root_note == "d":
    root_note = 50
elif root_note == "d#":
    root_note = 51
elif root_note == "e":
    root_note = 52
elif root_note == "f":
    root_note = 53
elif root_note == "f#":
    root_note = 54
elif root_note == "g":
    root_note = 55
elif root_note == "g#":
    root_note = 56
elif root_note == "a":
    root_note = 57
elif root_note == "a#":
    root_note = 58
else: 
    root_note = 59

input_file_path = input("Wav file name to edit: ")
output_file = input_file_path[: -4] + "_" + str(bpm) + "bpm_1_8" + input_file_path[-4:]
output_file_short = input_file_path[: -4] + "_" + str(bpm) + "bpm_1_16" + input_file_path[-4:]
left_samples, right_samples = read_stereo_wav(input_file_path)

final_length_of_sample_1_8 = round(((((60000 / bpm) / 2 * 1000) / 1000) * (sample_rate / 1000)))
final_length_of_sample_1_16 = round(((((60000 / bpm) / 4 * 1000) / 1000) * (sample_rate / 1000)))

first_nonzero_index_left = find_first_nonzero_index(left_samples)
first_nonzero_index_right = find_first_nonzero_index(right_samples)

print("First nonzero index in left channel:", first_nonzero_index_left)
print("First nonzero index in right channel:", first_nonzero_index_right)

# Find which channel comes to non 0 value sample first and cut from that sample both channels
min_index = min(first_nonzero_index_left, first_nonzero_index_right) -1
# Remove all silence from beginning to first non zero value, leaving one zero value at beginning to avoid clicks
left_samples = left_samples[min_index:]
right_samples = right_samples[min_index:]
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

# Shorten the sample to bpm and choosen 1/8 or 1/16 beat
left_samples_long = left_samples[:final_length_of_sample_1_8]
right_samples_long = right_samples[:final_length_of_sample_1_8]
left_samples_short = left_samples[:final_length_of_sample_1_16]
right_samples_short = right_samples[:final_length_of_sample_1_16]

# Fadeout to zero last 660 samples of a file
# Linearly decrease the last 10 values from 1 to 0
for i in range(660):
    left_samples_long[-(i + 1)] = left_samples_long[-(i + 1)] * fadeout_linear[i]
    right_samples_long[-(i + 1)] = right_samples_long[-(i + 1)] * fadeout_linear[i]
    left_samples_short[-(i + 1)] = left_samples_short[-(i + 1)] * fadeout_linear[i]
    right_samples_short[-(i + 1)] = right_samples_short[-(i + 1)] * fadeout_linear[i]

def create_stereo_wav(left_channel, right_channel, output_file):
    # Set the parameters for the WAV file
    sample_width = 2  # 16-bit audio
    frame_rate = sample_rate
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



create_stereo_wav(left_samples_long, right_samples_long, output_file)
create_stereo_wav(left_samples_short, right_samples_short, output_file_short)
sfz_filename = input_file_path[: -4] + "_" + str(bpm) + "bpm.sfz"
sfz_file = open(sfz_filename, "w")
sfz_file.write("<region> pitch_keycenter=" + str(root_note) + " lovel=0 hivel=127 lokey=" + str(root_note) + "  hikey=" + str(root_note) + "  sample=" + output_file + "\n<region> pitch_keycenter=" + str(root_note + 12) + "  lovel=0 hivel=127 lokey=" + str(root_note + 12) + "  hikey=" + str(root_note + 12) + "  sample=" + output_file_short)
sfz_file.close()
print ("Edited file created:", output_file)
print ("Edited file created:", output_file_short)
input("Press ENTER to exit")
