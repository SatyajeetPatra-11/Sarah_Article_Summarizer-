# IISC Bengaluru Hackthon

The summarization tool first accepts input in three forms: topic title, user-provided content, or uploaded PDF. If a topic is given, relevant descriptions are scraped from Fox News, Fox Business, Fox Sports, and NDTV. Next, the data is fed into a fine-tuned BERT/Facebook summarizer model, followed by keyword extraction using spaCy. The tool then provides a summarized text along with keywords and links. For user-provided content or PDFs, the same process applies, followed by translation to Indian languages and optional voice reading.

![landing page](./imgs/Screenshot%202024-02-17%20124536.png)

## Output images

![by content](./imgs/Screenshot%20(282).png)
![](./imgs/Screenshot%20(283).png)
![](./imgs/Screenshot%20(284).png)
![](./imgs/Screenshot%20(285).png)
![](./imgs/Screenshot%20(286).png)
![](./imgs/Screenshot%20(287).png)
![](./imgs/Screenshot%20(288).png)


# instructions

- for backend

```
pip install -r requirements.txt
python3 app.py
```

- for frontend

```
cd frontend
npm install
npm run dev
```

- visit `http://localhost:5173` on your pc