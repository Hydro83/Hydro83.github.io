import io
import os

# Open the file in read-only ("r") mode
with open("tracknumber.txt", "r") as file:
    # Read the number from the tracknumber.txt file
    brojtraka = int(file.read())

# Increment the existing track number by 1
brojtraka += 1

# User input without newline using print instead of io.write
print("Datum trake #", brojtraka, " u formatu Oct 15, 2023: ", end="")
datum = input()

print("Opis trake #", brojtraka, " Za novi red uneti & : ", end="")
opis = input()
opis = opis.replace("&", "<br>")  # Replace "&" with HTML format for newline

print("Bandcamp link trake #", brojtraka, " : ", end="")
bc = input()

print("Youtube link trake #", brojtraka, " : ", end="")
yt = input()

# Write all the input to the mp3/brojnovetrake.txt file
tracktxt = f'<div><h1>Mire - Goa#{brojtraka}</h1><i>Release date: {datum}</i><br><br>{opis}<br><br><a href="mp3/Mire-Goa{brojtraka}.mp3" download="Mire-Goa{brojtraka}.mp3"><img src="mp3.svg"></a><a href="{yt}"><img src="ytgray.svg"></a><a href="{bc}"><img src="bcgray.svg"></a></div>'
with open(f"mp3/{brojtraka}.txt", "w") as file:
    file.write(tracktxt)

# Update the tracknumber.txt file with the incremented track number
with open("tracknumber.txt", "w") as file:
    file.write(str(brojtraka))

print(f"\nSnimljen je fajl {brojtraka}.txt u folder mp3/ i updateovan je fajl tracknumber.txt sa novim brojem traka\n")

# Pause the script before running github commit
print(f"Pre nastavka sa github commit-om kopiraj u mp3/ folder fajlove {brojtraka}.jpg sa dimenzijama 500x500px, i Mire-Goa{brojtraka}.mp3 i pritisni ENTER za nastavak")
input()

# Perform github commit
os.system('git add --all')
os.system('git commit -m "Initial commit"')
os.system('git push -u origin main')
input()
