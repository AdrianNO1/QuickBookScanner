"""
an alternate script for OCR.
not recommended because it's much slower and more expensive than using google cloud vision.
"""

from PIL import Image, ImageDraw
from openai import OpenAI
import io, os, json
import base64

client = OpenAI(api_key=os.environ["OPENAI_API_KEYt"])

def encode_image(image_path):
	with open(image_path, "rb") as image_file:
		return base64.b64encode(image_file.read()).decode('utf-8')




image_paths = os.listdir("pages")
image_paths = [os.path.join("pages", image_path) for image_path in image_paths]

i = 0
for image_path in image_paths:
	data_file = os.path.join("data", os.path.basename(image_path).replace(".jpg", ".json"))
	if os.path.exists(data_file):
		print("Skipping", os.path.basename(image_path))
		continue

	response = client.chat.completions.create(
		model="gpt-4o",
		messages=[
			{
			"role": "user",
			"content": [
				{
				"type": "text",
				"text": "You are an OCR engine. respond with the text in this image as a json object with a single key named \"text\" and the value as the text in the image.",
				},
				{
				"type": "image_url",
				"image_url": {
					"url":  f"data:image/jpeg;base64,{encode_image(image_path)}"
				},
				},
			],
			}
		],
		temperature=0,
		response_format={ "type": "json_object" }
	)

	jason = response.choices[0].message.content
	try:
		jason = json.loads(jason)
	except:
		print("Error parsing json")
		continue

	with open(data_file, "w", encoding="utf-8") as f:
		data_obj = {
			"text": jason["text"],
		}
		json.dump(data_obj, f, indent=4)

	i += 1
	print(i)