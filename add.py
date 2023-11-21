import os
from tkinter import Tk, Label, Entry, Button, StringVar, Text, Scrollbar, END

# Read the current track number from the file
with open("tracknumber.txt", "r") as file:
    broj_trake = int(file.read().strip())

# Increment the track number
broj_trake += 1

# Tkinter GUI
root = Tk()
root.title("Track Information")

# Set the width of the GUI window
root.geometry("1024x600")  # Adjust the height as needed

# Variables for user inputs
release_date_var = StringVar()
track_description_var = StringVar()
bandcamp_var = StringVar()
youtube_var = StringVar()

# Function to handle making changes to files
def make_changes():
    release_date = release_date_var.get()
    track_description = description_entry.get("1.0", END)  # Get text from Text widget
    bandcamp = bandcamp_var.get()
    youtube = youtube_var.get()

    # Replace newline characters with <br>
    track_description = track_description.replace("\n", "<br>")

    html = f'<div><h1>Mire - Goa#{broj_trake}</h1><i>Release date: {release_date}</i><br><br>{track_description}<br><br><a href="mp3/Mire-Goa{broj_trake}.mp3" download="Mire-Goa{broj_trake}.mp3"><img src="mp3.svg"></a><a href="{youtube}"><img src="ytgray.svg"></a><a href="{bandcamp}"><img src="bcgray.svg"></a></div>'
    
    # Write HTML with <br> to the file
    with open(f"mp3/{broj_trake}.txt", "w") as file:
        file.write(html)
# Save the incremented track number back to the file
    with open("tracknumber.txt", "w") as file:
        file.write(str(broj_trake))
    
    print(f"Changes made successfully. Please copy your Mire-Goa{broj_trake}.mp3 and {broj_trake}.jpg files into the /mp3 folder before continuing with Git commit")

# Function to handle Git commit
def git_commit():
    os.system('git add --all')
    os.system('git commit -m "Initial commit"')
    os.system('git push -u origin main')

    print("Git changes committed successfully.")

# GUI components
Label(root, text=f"Track#{broj_trake} release Date in format (Oct 15, 2023):").pack()
Entry(root, textvariable=release_date_var).pack()

Label(root, text="Track Description:").pack()
description_entry = Text(root, height=10, width=80)  # Adjust the height and width as needed
description_entry.pack()

Label(root, text="Bandcamp Link:").pack()
Entry(root, textvariable=bandcamp_var).pack()

Label(root, text="YouTube Link:").pack()
Entry(root, textvariable=youtube_var).pack()

# "Submit" button for making changes to files
Button(root, text="Submit", command=make_changes).pack()

# "Git Commit" button for committing Git changes
Button(root, text="Git Commit", command=git_commit).pack()

root.mainloop()
