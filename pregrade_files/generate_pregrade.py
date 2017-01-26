"""
Generates a pregrade.sml file from all of the files in sml_files
"""


import os

print_string = ""


files = [f for f in os.listdir(os.path.join(os.getcwd(), "sml_files")) if '.sml' in f]

for file in files:
	content = ''
	with open(os.path.join("sml_files", file), 'r') as f:
		content = f.read()

	section_header = "(*** %s $+%s ***)\n" %(file, file)

	section_footer = "\n(*** %s $-%s ***)\n\n" %(file, file)

	print_string = print_string + section_header + content + section_footer

with open("pregrade.sml", 'w+') as f:
	f.write(print_string)