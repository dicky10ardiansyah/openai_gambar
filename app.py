import os
import cv2
import openai
import numpy as np
import base64
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, redirect

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods = ("GET","POST"))
def index():
    if request.method == "POST":
        text = request.form["text"]
        response = openai.Image.create(
            prompt = text,
            n = 1,
            size = "1024x1024",
            response_format = "b64_json"
        )
        im_bytes = base64.b64decode(response['data'][0]['b64_json'])
        im_arr = np.frombuffer(im_bytes, dtype = np.uint8)
        img = cv2.imdecode(im_arr, cv2.IMREAD_COLOR)
        cv2.imwrite(os.path.join("static/", "im.png"), img)
        return redirect(url_for("index"))
    return render_template("index.html")