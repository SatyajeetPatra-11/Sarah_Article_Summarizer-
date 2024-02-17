from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS
import fitz
import summarize
import keyword_extractor
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from gtts import gTTS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def pdf_to_text(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page_number in range(len(pdf)):
            page = pdf.load_page(page_number)
            page_text = page.get_text()
            text += page_text
    return text


def get_link(keyword):
    links = []
    for j in search(keyword+' news', tld="co.in", num=10, stop=10, pause=5):
        links.append(j)
    return links[:2]


def get_content(query):
    links = []
    for j in search(query + " ndtv", tld="co.in", num=10, stop=10, pause=5):
        if not ("/topic/" in j or "/videos/" in j):
            if "ndtv.com" in j:
                links.append(j)

    if len(links) == 0:
        for j in search(query + " foxnews", tld="co.in", num=10, stop=10, pause=5):
            if not "/category/" in j:
                if "fox" in j:
                    links.append(j)

    url = links[0]
    print(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    p_tags = soup.find_all("p")

    p_tags = p_tags[1:-1]

    all_p_text = ""

    for p_tag in p_tags:
        if not (p_tag.find_parent("div", class_="caption") or p_tag.find("u")):
            all_p_text += p_tag.get_text() + " "

    return all_p_text


@app.route("/api/pdf", methods=["POST"])
def pdf_api_controller():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 403

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 403

    file_path = os.path.join(UPLOAD_FOLDER, "input.pdf")
    file.save(file_path)

    text = pdf_to_text(file_path)

    summary = summarize.recursive_summarize(text)
    keyword = keyword_extractor.extract_keywords(summary, max_keywords=2)

    keyword_link=[]
    for i in keyword:
        links=get_link(i)
        for link in links:
            keyword_link.append(link)

    return jsonify({"keyword": keyword, "summary": summary,"keyword-link":keyword_link})


@app.route("/api/title", methods=["GET"])
def title_api():
    title = request.args.get("title")

    text = get_content(title)
    summary = summarize.recursive_summarize(text)

    keyword = keyword_extractor.extract_keywords(summary, max_keywords=2)
    keyword = keyword_extractor.extract_keywords(summary, max_keywords=2)

    keyword_link=[]
    for i in keyword:
        links=get_link(i)
        for link in links:
            keyword_link.append(link)

    return jsonify({"keyword": keyword, "summary": summary,"keyword-link":keyword_link})


@app.route("/api/content", methods=["GET"])
def content_api():
    text = request.args.get("content")

    summary = summarize.recursive_summarize(text)

    keyword = keyword_extractor.extract_keywords(summary, max_keywords=2)
    keyword = keyword_extractor.extract_keywords(summary, max_keywords=2)

    keyword_link=[]
    for i in keyword:
        links=get_link(i)
        for link in links:
            keyword_link.append(link)

    return jsonify({"keyword": keyword, "summary": summary,"keyword-link":keyword_link})


@app.route("/api/translator", methods=["GET"])
def translator_api():
    to_lang = request.args.get("tolang")
    from_lang = "en"
    summary = request.args.get("summary")

    translator = Translator()

    text_to_translate = translator.translate(summary, src=from_lang, dest=to_lang)
    text = text_to_translate.text
    print(text)
    try:
        speak = gTTS(text=text, lang=to_lang, slow=False)
        file_path = os.path.join(UPLOAD_FOLDER, "translated_audio.mp3")
        speak.save(file_path)

    except:
        speak = gTTS(text="Audio Not supported", lang="en", slow=False)
        file_path = os.path.join(UPLOAD_FOLDER, "translated_audio.mp3")
        speak.save(file_path)

    audio_url = "http://127.0.0.1:5000/api/play"

    return jsonify({"translation": text, "audio_url": audio_url})


@app.route("/api/play", methods=["GET"])
def play_file():
    file_path = os.path.join(UPLOAD_FOLDER, "translated_audio.mp3")
    return send_file(file_path)


if __name__ == "__main__":
    app.run()
