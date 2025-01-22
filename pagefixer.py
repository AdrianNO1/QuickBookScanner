"""
The OCR catches the page number as a piece of the text.
Some of those page numbers aren't captured by the OCR so this script is for filling in the gaps.
This script works best when the images have names that reflect the time or date, so the pages are in the correct order.
This script isn't really necessary and is optional.
"""

import os, json, re

data_files = os.listdir("data")
data_files = [os.path.join("data", data_file) for data_file in data_files]

wrongs = []

last_page = None
for data_file in data_files:
	with open(data_file, "r", encoding="utf-8") as f:
		data = json.load(f)
		if "page" not in data:
			continue
		try:
			int(data["page"])
			print("Page:", data["page"])
			last_page = int(data["page"])
		except:
			print("Invalid page number:", data["page"])
			print("Setting to", last_page+1)
			with open(data_file, "w", encoding="utf-8") as f:
				data["page"] = str(last_page+1)
				json.dump(data, f, indent=4)
			wrongs.append(data_file)
			last_page += 1

if len(wrongs) == 0:
	print("All good.")
else:
	print("Wrongs found but fixed:", len(wrongs))
	print("Files:", wrongs)