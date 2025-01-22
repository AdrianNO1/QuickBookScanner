import os, json, re

"""
A crude version of the text extractor which doesn't sort the files by page number
But if the filenames are already in the correct order,
which they typically are because of the way they are named, then this script should be fine.
"""

data_files = os.listdir("data")
data_files = [os.path.join("data", data_file) for data_file in data_files]

total_text = ""

def text_fixer(text):
	return text

datas = []
for data_file in data_files:
	with open(data_file, "r", encoding="utf-8") as f:
		datas.append(json.load(f))

for data in datas:
	total_text += text_fixer(data["text"]) + " "

fname = "total_text.txt"

with open(fname, "w", encoding="utf-8") as f:
	f.write(total_text)