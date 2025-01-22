"""
Uses google cloud vision to extract text from all the pages and saves the text and data in the data folder.
Also saves the images with bounding boxes in the bounding folder so you can see how well the OCR is working.
Will process each image in the pages folder and save the data in the data folder, printing the page number as it goes.
"""

import io, os, json
from google.cloud import vision
from PIL import Image, ImageDraw
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/cloud-vision']

if not os.path.exists("bounding"):
	os.makedirs("bounding")

if not os.path.exists("data"):
	os.makedirs("data")

if not os.path.exists("pages"):
	os.makedirs("pages")

def get_credentials(): # DELETE token.json if this throws an error to get a new token
	creds = None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)

		with open('token.json', 'w') as token:
			token.write(creds.to_json())
	return creds

credentials = get_credentials()
client = vision.ImageAnnotatorClient(credentials=credentials)



image_paths = os.listdir("pages")
image_paths = [os.path.join("pages", image_path) for image_path in image_paths]

for image_path in image_paths:
	data_file = os.path.join("data", os.path.basename(image_path).replace(".jpg", ".json"))
	if os.path.exists(data_file):
		print("Skipping", os.path.basename(image_path))
		continue

	with io.open(image_path, 'rb') as image_file:
		content = image_file.read()

	image = vision.Image(content=content)

	response = client.text_detection(image=image)
	texts = response.text_annotations

	if texts:
		all_text = texts[0].description
		output = all_text
	else:
		output = ""
	
	#with open("output.txt", "a", encoding="utf-8") as f:
	#	f.write(output + " <|sep|> ")

	pil_image = Image.open(image_path)

	draw = ImageDraw.Draw(pil_image)

	for text in texts[1:]:  # Skip the first element as it contains all text
		vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
		
		draw.polygon(vertices, outline='red')
		
		#print(f'\nWord: {text.description}')
		#print(f'Bounds: {vertices}')

	print("Page: ", text.description)

	with open(data_file, "w", encoding="utf-8") as f:
		def serialize_texts(texts):
			serialized_texts = []
			for text in texts:
				serialized_texts.append({
					"description": text.description,
					"bounding_poly": [
					{"x": vertex.x, "y": vertex.y} for vertex in text.bounding_poly.vertices
					]
				})
			return serialized_texts

		data_obj = {
			"full_text": output,
			"page": text.description,
			"mess": serialize_texts(texts),
		}
		json.dump(data_obj, f, indent=4)

	# Save the image with bounding boxes
	output_path = os.path.join("bounding", os.path.basename(image_path))
	pil_image.save(output_path)