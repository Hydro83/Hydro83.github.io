import wave
import numpy as np
import struct
import matplotlib.pyplot as plt
import os

# Populate notes array with notes that are played in wav file until ENTER is pressed
notes = []
i = 0
while i >= 0:
    notes.append(input("Insert notes that are used (c, c#, b...). Insert 'full' for a whole octave or press ENTER to end: "))
    if notes[i] == "": 
        del notes[-1]
        break
    elif notes[i] == "c":
        notes[i] = 48
    elif notes[i] == "c#":
        notes[i] = 49
    elif notes[i] == "d":
        notes[i] = 50
    elif notes[i] == "d#":
        notes[i] = 51
    elif notes[i] == "e":
        notes[i] = 52
    elif notes[i] == "f":
        notes[i] = 53
    elif notes[i] == "f#":
        notes[i] = 54
    elif notes[i] == "g":
        notes[i] = 55
    elif notes[i] == "g#":
        notes[i] = 56
    elif notes[i] == "a":
        notes[i] = 57
    elif notes[i] == "a#":
        notes[i] = 58
    elif notes[i] == "b":
        notes[i] = 59
    elif notes[i] == "full":
        # Full octave - 12 notes
        notes = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
        break
    else:
        print("Wrong note inserted")
        quit()
    i = i + 1

# Sort notes from lowest to highest
notes = sorted(notes)

# How much notes are inserted
num_of_notes = len(notes)

# How menu octaves are played
num_of_octaves = input("How many octaves are used? 1, 2 or 3 ")

# Add more octaves to notes list or not if only 1 octave is played
if num_of_octaves == "1" or num_of_octaves == "2" or num_of_octaves == "3":
    print()
else:
    print("Wrong number of octaves")
    quit()

if int(num_of_octaves) == 2:
    x = 0
    while x < num_of_notes:
        notes.append(notes[x] + 12)
        x = x + 1
    notes = sorted(notes)

if int(num_of_octaves) == 3:
    x = 0
    while x < num_of_notes:
        notes.append(notes[x] + 12)
        notes.append(notes[x] + 24)
        x = x + 1
    notes = sorted(notes)

# How much notes are inserted after adding 2 or 3 octaves
num_of_notes = len(notes)

# Open wav file
file_path = input("Drag wav file here: ")
wav_file = wave.open(file_path, 'rb')
num_frames = wav_file.getnframes()
frames = wav_file.readframes(num_frames)
samples = np.frombuffer(frames, dtype=np.int16)
sample_rate = wav_file.getframerate()
left_channel = samples[::2] / 32768.0
right_channel = samples[1::2] / 32768.0

# Create list for cutted waves
left_channel_edited = []
right_channel_edited = []
x = 0
first_zero = 0
last_zero = 0

while x < num_of_notes:
    # Find first non zero value 
    for index, value in enumerate(left_channel):
        if value != 0:
            first_zero = index - 1
            break
    # Find last non zero value
    for index, value in enumerate(left_channel):
        if left_channel[index] != 0 and left_channel[index + 1] == 0 and left_channel[index + 2] == 0:
            last_zero = index + 1
            break
    # Cut one note and add it to left_channel_edited list
    left_channel_edited.append(left_channel[first_zero:last_zero])
    right_channel_edited.append(right_channel[first_zero:last_zero])
    # Add 2000 samples because of very quiet tail after note can be captured as a new note
    left_channel = left_channel[last_zero + 2000:]
    right_channel = right_channel[last_zero + 2000:]
    x = x + 1 

# Function for normalizing all notes
def normalize_values(numbers, max_abs_value):
    factor = 1 / max_abs_value
    normalized_numbers = []
    for x in numbers:
        if x != 0:
            normalized_numbers.append(x * factor)
        else:
            normalized_numbers.append(0)
    return normalized_numbers
# Add left and right channel, than find highest peek as max_abs_value than send left and right channel to normalize function
x = 0
while x < num_of_notes:
    combined_numbers = np.concatenate([left_channel_edited[x], right_channel_edited[x]])
    max_abs_value = max(map(abs, combined_numbers))
    left_channel_edited[x] = normalize_values(left_channel_edited[x], max_abs_value)
    right_channel_edited[x] = normalize_values(right_channel_edited[x], max_abs_value)
    x = x + 1

# FadeOut all the notes so there wont be any clicks at the sample end
# Fadeout list of 660 float number samples from 1 to 0
fadeout_length_in_samples = 660
fadeout_linear = np.linspace(0.0, 1.0, fadeout_length_in_samples).tolist()
x=0
while x < num_of_notes:
    for i in range(fadeout_length_in_samples):
        left_channel_edited[x][-(i + 1)] = left_channel_edited[x][-(i + 1)] * fadeout_linear[i]
        right_channel_edited[x][-(i + 1)] = right_channel_edited[x][-(i + 1)] * fadeout_linear[i]
    x = x + 1

# Function for writing wav and sfz file to disk
def create_stereo_wav(left_channel, right_channel, output_file):
    # Check if the lengths of the two channels match
    if len(left_channel) != len(right_channel):
        raise ValueError("The lengths of the left and right channels must be the same.")

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


# Create sfz File (same name as wav filename just with .sfz extension)
sfz_filename = file_path[: -4] + ".sfz"

# Call a function for making a wav file for all the notes
x=0
while x < num_of_notes:
    output_file = file_path[:-4] + "_" + str(notes[x]) + ".wav"
    # Remove directories, leave only name of the wav file for import in sfz file
    sfz_file1 = os.path.basename(output_file)
    create_stereo_wav(left_channel_edited[x], right_channel_edited[x], output_file)
    sfz_file = open(sfz_filename, "a")
    sfz_file.write("<region> pitch_keycenter="+ str(notes[x]) +" lovel=0 hivel=127 lokey=" + str(notes[x]) + " hikey=127 sample=" + sfz_file1 + "\n")
    sfz_file.close()
    x = x + 1

input("sfz and wav files saved. Press ENTER to exit program")