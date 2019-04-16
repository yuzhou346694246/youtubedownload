from flask import Flask,request,url_for,render_template
#from __future__ import unicode_literals
import youtube_dl

app = Flask(__name__)

#url_for('static',fi)

@app.route("/", methods=['GET','POST'])
def index():
    #return "Hello Dongge!"
    if request.method == 'GET':
        return render_template('index.html')
    else:
        print(request.form['url'])
        download(request.form['url'])

def download(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])