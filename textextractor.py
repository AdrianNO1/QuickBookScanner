import os, json, re

"""
sorts the data files by page number and concatenates the text
"""

data_files = os.listdir("data")
data_files = [os.path.join("data", data_file) for data_file in data_files]

total_text = ""

def extract_number_from_end(input_string):
	# Regular expression pattern to match digits at the end of the string
	pattern = r'(\d+)$'
	
	# Search for the pattern in the input string
	match = re.search(pattern, input_string)
	
	if match:
		# Extract the number from the match
		number = int(match.group(1))
		
		# Remove the number from the original string
		string_without_number = re.sub(pattern, '', input_string)
		
		return string_without_number, number
	else:
		# If no number is found at the end, return the original string and None
		return input_string, None

def text_fixer(text):
	text = text.replace("<<", "«")
	text = text.replace(">>", "»")
	text = text.replace("-\n", "")

	text, page = extract_number_from_end(text)

	return text

while True:
	try:
		start_page = int(input("Enter the start page number (or leave blank): ") or 0)
		break
	except:
		print("Invalid input. Try again.")
while True:
	try:
		end_page = int(input("Enter the end page number (or leave blank): ") or 0)
		break
	except:
		print("Invalid input. Try again.")

datas = []
for data_file in data_files:
	with open(data_file, "r", encoding="utf-8") as f:
		datas.append(json.load(f))

datas = [data for data in datas if "page" in data]
datas = sorted(datas, key=lambda x: int(x["page"]))

if end_page == 0:
	end_page = int(datas[-1]["page"])

for data in datas:
	if (start_page or end_page) and (int(data["page"]) < start_page or int(data["page"]) > end_page):
		continue
	print("Page:", data["page"])
	if (len(total_text) > 1 and total_text[-1] == "-"):
		total_text = total_text[:-1] + text_fixer(data["full_text"])
	else:
		total_text += text_fixer(data["full_text"]) + " "

if start_page or end_page:
	fname = f"total_text_{start_page}-{end_page}.txt"
else:
	fname = "total_text.txt"

with open(fname, "w", encoding="utf-8") as f:
	f.write(total_text)
print("Text saved to", fname)