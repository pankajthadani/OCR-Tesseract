import os
from flask import Flask, render_template, request
from PIL import Image
import sys
import pyocr
import pyocr.builders
import re
import json

__author__ = 'K_K_N'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def ocr(image_file):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))
    # Ex: Will use tool 'libtesseract'

    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    lang = langs[1]
    print("Will use lang '%s'" % (lang))

    txt = tool.image_to_string(
        Image.open(image_file),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    ektp_no = re.search( r'[?:nik\s*:\s*](\d{1,20})\s*', txt, re.I)
    #print ektp_no
    data = {}
    if ektp_no:
    #    print "ektp_no.group() : ", ektp_no.group()
        data['ektp'] = ektp_no.group().strip()
    else:
        data['ektp'] = 'Error'
            
    return json.dumps(data)

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        #Return JSON
        #print txt
        #file.delete(destination)

    return ocr(destination) 
    #return json.dumps(txt)

if __name__ == "__main__":
    app.run(port=4555, debug=True)

