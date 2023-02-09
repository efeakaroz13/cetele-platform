"""
Çetele Official Python Backend
Author:Efe Akaröz
by Kentel

"""

from flask import Flask,render_template,request,redirect
import os
import json


app = Flask(__name__)
@app.route("/")
def index():
    language = request.cookies.get("lang")
    if language == None:
        lang="en"
    if language =="tr":
        lang= "tr"
    else:
        lang="en"
    if lang == "en":
        return render_template("index_en.html",lang="en")
    if lang =="tr":
        return render_template("index_tr.html",lang="tr")


if __name__ == "__main__":
    app.run(debug=True,port=1313)
