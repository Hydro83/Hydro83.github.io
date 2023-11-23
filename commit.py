import os
# Function to handle Git commit

os.system('git add --all')
os.system('git commit -m "Initial commit"')
os.system('git push -u origin main')

print("Git changes committed successfully.")
