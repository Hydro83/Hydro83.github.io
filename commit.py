import os

input("Commit changes to github? Press ENTER")

os.system('git add --all')
os.system('git commit -m "Initial commit"')
os.system('git push -u origin main')

input("Press Enter to exit...")