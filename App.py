from flask import Flask,request,url_for,render_template, send_file
#from __future__ import unicode_literals
import youtube_dl
import os
import multiprocessing

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



@app.route("/list")
def downloadList():
    '''
    列出下载列表
    '''
    tree = make_tree('./downloads')
    return render_template('list.html', tree=tree)


@app.route('/return-file', methods = ['GET'])
def returnFile():
    basedir = './downloads'
    try:
        path = os.path.join(basedir,request.args.get('path'))
        if os.path.exists(path) and os.path.isfile(path):
            return send_file(path,as_attachment=True)
    except KeyError:
        return "<h1>文件不存在</h1>"

####################以下为功能函数
def download(url):
    ydl_opts = {
        'format':'mp4',
        'outtmpl':'./downloads/%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def make_tree(path):
    tree = dict(name=os.path.basename(path),isdir=True, children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name,isdir=False))
    return tree