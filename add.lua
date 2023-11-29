-- Otvori fajl u read only ("r") modu
file = io.open("tracknumber.txt", "r")
-- Pročitaj broj (n je za broj) iz tracknumber.txt fajla
brojtraka = file:read("n")
file:close()
-- Dodaj 1 na postojeći broj traka
brojtraka = brojtraka + 1

-- User input sa io.write da ne prelazi u novi red
io.write("Datum trake #" .. brojtraka .. " u formatu Oct 15, 2023: ")
datum = io.read()
io.write("Opis trake #" .. brojtraka .. " Za novi red uneti & : ")
opis = io.read()
opis = opis:gsub("%&", "<br>") -- Ukoliko ima karaktera za novi red "&" prebaciti ih u html format za novi red "<br>"
io.write("Bandcamp link trake #" .. brojtraka .. " : ")
bc = io.read()
io.write("Youtube link trake #" .. brojtraka .. " : ")
yt = io.read()

-- Upiši sve što je uneto u fajl mp3/brojnovetrake.txt
tracktxt = '<div><h1>Mire - Goa#'..brojtraka..'</h1><i>Release date: '..datum..'</i><br><br>'..opis..'<br><br><a href="mp3/Mire-Goa'..brojtraka..'.mp3" download="Mire-Goa'..brojtraka..'.mp3"><img src="mp3.svg"></a><a href="'..yt..'"><img src="ytgray.svg"></a><a href="'..bc..'"><img src="bcgray.svg"></a></div>'
file = io.open("mp3/"..brojtraka..".txt", "w")
file:write(tracktxt)
file:close()

-- Dodaj 1 na broj traka u fajlu tracknumber.txt
file = io.open("tracknumber.txt", "w")
file:write(brojtraka)
file:close()

print("\nSnimljen je fajl "..brojtraka..".txt u folder mp3/ i updateovan je fajl tracknumber.txt sa novim brojem traka\n")

-- Pauziraj skriptu pre pokretanja github commit-a
print("Pre nastavka sa github commit-om kopiraj u mp3/ folder fajlove "..brojtraka..".jpg sa dimenzijama 500x500px, i Mire-Goa"..brojtraka..".mp3 i pritisni ENTER za nastavak")
io.read()

-- Uradi github commit
os.execute('git add --all')
os.execute('git commit -m "Initial commit"')
os.execute('git push -u origin main')
io.read()

