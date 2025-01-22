# Quick Book Scanner 📚

Tired of wasting time on mind-numbing assigned reading? This tool converts your books to text so you can get an AI to summarize that 400-page novel about some guy staring at a green light across a lake. 🚀

## 🌟 Features

- Image to text conversion using Google Cloud Vision OCR
- Automatic page number detection
- Manual page correction functionality
- Text extraction by page range
- Get back to actually important stuff while "reading"

## 📋 Prerequisites

- Python 3.x
- Google Cloud Vision API credentials
- Any camera (even your phone works!)
- A book you'd rather not read

## 🔑 Google Cloud Setup

1. Create a Google Cloud Project
2. Enable the Cloud Vision API
3. Create a service account and download the credentials
4. Rename the downloaded file to `credentials.json` and place it in the project root

## 🚀 Installation

```bash
git clone https://github.com/AdrianNO1/QuickBookScanner
cd QuickBookScanner
pip install -r requirements.txt
```

## 📦 Requirements

```
google-cloud-vision>=3.4.4
google-auth-oauthlib>=1.0.0
google-auth>=2.22.0
Pillow>=10.0.0
openai>=1.3.0
```

## 📖 Usage

1. **Snap Those Pages**
   - Take pictures of each page (quality doesn't have to be perfect, google vision is surprisingly good)
   - Try to get page numbers in at least some of the shots
   - Dump all images in a folder named "pages"

2. **Let the Magic Happen**
   ```bash
   python lens.py
   ```

3. **Fill in any missing page numbers**
   ```bash
   python pagefixer.py
   ```

4. **Get Your Text**
   ```bash
   python textextractor.py
   ```

5. Feed the text to an LLM of your choice and get back to watching Netflix while your classmates are still on chapter 2! 🎬

---
*Because life's too short to read uninteresting translated Norwegian fiction - sorry not sorry, Trond!* 🤘
