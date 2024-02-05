import wave
import numpy as np
import struct
import os

# Open wav file
file_path = input("Drag wav file here: ")
wav_file = wave.open(file_path, 'rb')
num_frames = wav_file.getnframes()
frames = wav_file.readframes(num_frames)
samples = np.frombuffer(frames, dtype=np.int16)
sample_rate = wav_file.getframerate()
left_channel = samples[::2] / 32768.0
right_channel = samples[1::2] / 32768.0


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
num_of_octaves = input("How many octaves are used? 1, 2 or 3: ")

# Add more octaves to notes list or not if only 1 octave is played
if num_of_octaves == "2":
    x = 0
    while x < num_of_notes:
        notes.append(notes[x] + 12)
        x = x + 1

if num_of_octaves == "3":
    x = 0
    while x < num_of_notes:
        notes.append(notes[x] + 12)
        notes.append(notes[x] + 24)
        x = x + 1
    
# add 128 to the end of notes list so the last note can span from lowkey to hikey (128-1)
notes.append(128)
notes = sorted(notes)
num_of_notes = len(notes) - 1

# Ask for BPM of a file
bpm = input("Bpm: ")
bpm = int(bpm)

# Ask for length of notes that are played
cutnotes = input("Notes length? (a) 1/2, (b) 1/4, (c) 1/8, (d) 1/16: ")
if cutnotes == "a":
    note_length = round(((((60000 / bpm) * 2 * 1000) / 1000) * (sample_rate / 1000)))
elif cutnotes == "b":
    note_length = round(((((60000 / bpm) * 1000) / 1000) * (sample_rate / 1000)))
elif cutnotes == "c":
    note_length = round(((((60000 / bpm) / 2 * 1000) / 1000) * (sample_rate / 1000)))
elif cutnotes == "d":
    note_length = round(((((60000 / bpm) / 4 * 1000) / 1000) * (sample_rate / 1000)))
else:
    print ("Wrong input!")
    quit()

print("Length of a note in samples: " + str(note_length))


# Fadeout list of 660 float number samples from 1 to 0
fade = input("How long the fadeout should be in samples (ENTER) for 660 samples: ")
if fade == "":
    fadeout_length_in_samples = 660
    fadeout_linear = np.linspace(0.0, 1.0, fadeout_length_in_samples).tolist()
else:
    fadeout_length_in_samples = int(fade)
    fadeout_linear = np.linspace(0.0, 1.0, fadeout_length_in_samples).tolist()


# Create sfz File (same name as wav filename just with .sfz extension)
sfz_filename = file_path[: -4] + ".sfz"
lovel = input("Lowest velocity (0-127): ")
hivel = input("Highest velocity (0-127): ")
# Remove directories, leave only name of the wav file for import in sfz file
sfz_file = open(sfz_filename, "a")


x = 0
while x < num_of_notes:
    
    
    # Cut one note and add it to left_channel_edited list
    left_channel_edited = left_channel[:note_length]
    right_channel_edited = right_channel[:note_length]
    left_channel_edited[0] = 0
    right_channel_edited[0] = 0    
    
    # Apply fade out to note
    for i in range(fadeout_length_in_samples):
        left_channel_edited[-(i + 1)] = left_channel_edited[-(i + 1)] * fadeout_linear[i]
        right_channel_edited[-(i + 1)] = right_channel_edited[-(i + 1)] * fadeout_linear[i]
    
    # Save wav file
    # Set the parameters for the WAV file
    sample_width = 2  # 16-bit audio
    frame_rate = sample_rate
    num_channels = 2  # Stereo
    output_file = file_path[:-4] + "_" + str(notes[x]) + ".wav"

    # Create a new wave file
    with wave.open(output_file, 'w') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)
        wav_file.setcomptype("NONE", "not compressed")

        # Combine left and right channels into interleaved samples
        interleaved_samples = []
        for left, right in zip(left_channel_edited, right_channel_edited):
            interleaved_samples.append(struct.pack("<h", int(left * 32767)))  # left channel
            interleaved_samples.append(struct.pack("<h", int(right * 32767)))  # right channel

        # Write the interleaved samples to the WAV file
        wav_file.writeframes(b''.join(interleaved_samples))

    # Remove directories, leave only name of the wav file for import in sfz file
    sfz_file1 = os.path.basename(output_file)
    sfz_file.write("<region> pitch_keycenter="+ str(notes[x]) +" lovel=" + lovel + " hivel=" + hivel + " lokey=" + str(notes[x]) + " hikey=" + str(notes[x+1] - 1) + " sample=" + sfz_file1 + "\n")

    # Remove used sample from main list
    left_channel = left_channel[note_length*2:]
    right_channel = right_channel[note_length*2:]

    x = x + 1
















#sfz_file.close()