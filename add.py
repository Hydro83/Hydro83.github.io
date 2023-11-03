import os

# Get the user input for broj_trake
broj_trake = input("Track number: ")

# Prompt the user to input the release date
release_date = input("Release Date in format (Oct 15, 2023): ")

# Prompt the user to input the track description
track_description = input("Track Description: ")

# Prompt the user to input the Bandcamp link
bandcamp = input("Bandcamp Link: ")

# Prompt the user to input the YouTube link
youtube = input("YouTube Link: ")

# Check if broj_trake is odd or even
if int(broj_trake) % 2 == 0:
    pozadina = "parna"
else:
    pozadina = "neparna"

# Function to replace "display: block;" with "display: none;"
def replace_display_block(filename):
    with open(filename, "r", encoding="utf-8") as file:
        filedata = file.read()

    # Replace "display: block;" with "display: none;"
    filedata = filedata.replace("display: block;", "display: none;")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(filedata)

# Function to insert a line after a specific line
def insert_after_line(filename, line_to_insert_after, line_to_insert):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line)
            if line.strip() == line_to_insert_after:
                file.write(line_to_insert + "\n")

# Function to replace content after "<!--Starting image-->" with the provided image tag
def replace_starting_image(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(filename, "w", encoding="utf-8") as file:
        found_starting_image = False
        for line in lines:
            if found_starting_image:
                # Replace the content one line after "<!--Starting image-->"
                file.write('<img id="myImage" src="mp3/{}.jpg">'.format(broj_trake) + "\n")
                found_starting_image = False
            else:
                file.write(line)

            # Check if the current line contains "<!--Starting image-->"
            if "<!--Starting image-->" in line:
                found_starting_image = True

# Function to replace content after "<!--Starting track-->" with the provided audio source tag
def replace_starting_track(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(filename, "w", encoding="utf-8") as file:
        found_starting_track = False
        for line in lines:
            if found_starting_track:
                # Replace the content one line after "<!--Starting track-->"
                file.write('<source src="mp3/Mire-Goa{}.mp3" type="audio/mpeg">'.format(broj_trake) + "\n")
                found_starting_track = False
            else:
                file.write(line)

            # Check if the current line contains "<!--Starting track-->"
            if "<!--Starting track-->" in line:
                found_starting_track = True

# Replace "display: block;" with "display: none;" in index.html
replace_display_block("index.html")

# Replace "display: block;" with "display: none;" in mobile.html
replace_display_block("mobile.html")

# Define the line to insert
new_line = f"document.getElementById('desc{broj_trake}').style.display = 'none';"

# Insert the new line after "//Hide all divs" in index.html
insert_after_line("index.html", "//Hide all divs", new_line)

# Insert the new line after "//Hide all divs" in mobile.html
insert_after_line("mobile.html", "//Hide all divs", new_line)

# Define the line to insert in the meni section
meni_line = f'<div class="{pozadina}"><a href="#" onclick="changeAudioAndImage(this); changeDescription(\'desc{broj_trake}\');">Mire - Goa#{broj_trake}</a></div>'

# Insert the new line under "<!--meni-->" in index.html
insert_after_line("index.html", "<!--meni-->", meni_line)

# Insert the new line under "<!--meni-->" in mobile.html
insert_after_line("mobile.html", "<!--meni-->", meni_line)

# Define the line to insert in the Track description section
track_description_line = f'<div id="desc{broj_trake}" style="display: block;"><h1>Mire - Goa#{broj_trake}</h1><i>Release date: {release_date}</i><br><br>{track_description}<br><br><hr><br>To download this track right click on <a href="mp3/Mire-Goa{broj_trake}.mp3">this link</a> and choose Save link as...<br><br>You can also listen to this track on:<br><br><a href="{bandcamp}"><img src="bcgray.svg"></a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="{youtube}"><img src="ytgray.svg"></a></div>'

# Insert the new line under "<!--Track description-->" in index.html
insert_after_line("index.html", "<!--Track description-->", track_description_line)

# Insert the new line under "<!--Track description-->" in mobile.html
insert_after_line("mobile.html", "<!--Track description-->", track_description_line)

# Replace content after "<!--Starting image-->" in index.html
replace_starting_image("index.html")

# Replace content after "<!--Starting image-->" in mobile.html
replace_starting_image("mobile.html")

# Replace content after "<!--Starting track-->" in index.html
replace_starting_track("index.html")

# Replace content after "<!--Starting track-->" in mobile.html
replace_starting_track("mobile.html")

print(f"Please copy your Mire-Goa{broj_trake}.mp3 and {broj_trake}.jpg files in /mp3 folder before continuing with git commit")

input("Press Enter to continue...")

os.system('git add --all')
os.system('git commit -m "Initial commit"')
os.system('git push -u origin main')

input("Press Enter to exit...")