import re

# Briši liniju posle komentara Hide all divs
def process_html_file(file_name, text_to_find):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    remove_line = False

    for line in lines:
        if remove_line:
            remove_line = False
        elif text_to_find in line:
            modified_lines.append(line)
            remove_line = True
        else:
            modified_lines.append(line)

    with open(file_name, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)

index_html_path = 'index.html'
mobile_html_path = 'mobile.html'
text_to_find = "//Hide all divs"
process_html_file(index_html_path, text_to_find)
process_html_file(mobile_html_path, text_to_find)
text_to_find = "<!--meni-->"
process_html_file(index_html_path, text_to_find)
process_html_file(mobile_html_path, text_to_find)
text_to_find = "<!--Track description-->"
process_html_file(index_html_path, text_to_find)
process_html_file(mobile_html_path, text_to_find)


# Zameni link ka default slici
tracknum = input('Track to delete: ')
tracknum = str(int(tracknum) - 1)

# Function to replace the line following a given text in a file
def process_html_file(file_name, text_to_find, replacement_text):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    replace_line = False

    for line in lines:
        if replace_line:
            modified_lines.append(replacement_text + '\n')
            replace_line = False
        elif text_to_find in line:
            modified_lines.append(line)
            replace_line = True
        else:
            modified_lines.append(line)

    with open(file_name, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)

index_html_path = 'index.html'
mobile_html_path = 'mobile.html'
text_to_find = "<!--Starting image-->"
replacement_text = '<img id="myImage" src="mp3/'+tracknum+'.jpg">'
process_html_file(index_html_path, text_to_find, replacement_text)
process_html_file(mobile_html_path, text_to_find, replacement_text)
text_to_find = "<!--Starting track-->"
replacement_text = '<source src="mp3/Mire-Goa'+tracknum+'.mp3" type="audio/mpeg">'
process_html_file(index_html_path, text_to_find, replacement_text)
process_html_file(mobile_html_path, text_to_find, replacement_text)


# Function to find and replace the first occurrence of "display: none;" with "display: block;"
def process_html_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        file_content = file.read()

    # Use regular expression to find the first occurrence of "display: none;"
    file_content = re.sub(r"display: none;", "display: block;", file_content, count=1)

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(file_content)

index_html_path = 'index.html'
mobile_html_path = 'mobile.html'
process_html_file(index_html_path)
process_html_file(mobile_html_path)