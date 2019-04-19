from flask import Flask,request,url_for,render_template, send_file, redirect
#from __future__ import unicode_literals
import youtube_dl
import os
import multiprocessing
import hashlib

app = Flask(__name__)

hashfilenames = {}
#url_for('static',fi)

@app.route("/", methods=['GET','POST'])
def index():
    #return "Hello Dongge!"
    if request.method == 'GET':
        return render_template('index.html')
    else:
        print(request.form['url'])
        try:
            download(request.form['url'])
        except:
            return redirect('/')



@app.route("/list")
def downloadList():
    init_hashfilenames()
    '''
    列出下载列表
    '''
    tree = make_tree('./downloads')
    return render_template('list.html', tree=tree)

@app.route("/delete")
def delete():
    '''
    /delete?hash=xxx
    '''
    arg = request.args.get('hash')
    hashinfo = gethashinfo(arg)
    if hashinfo == None:
        return "<h1>文件不存在</h1>"
    path = hashinfo['path']
    try:
        remove(path)
        return redirect("/list")
    except FileNotFoundError:
        return "<h1>文件不存在</h1>"


@app.route('/return-file', methods = ['GET'])
def returnFile():
    basedir = './downloads'
    try:
        arg = request.args.get('hash')
        hashinfo = gethashinfo(arg)
        if hashinfo == None:
            return "<h1>文件不存在{}</h1>".format(hashfilenames)
        #path = os.path.join(basedir,request.args.get('path'))
        path = hashinfo['path']
        filename = hashinfo['filename']
        if os.path.exists(path) and os.path.isfile(path):
            print(path)
            return send_file(path,as_attachment=True)
            '''
            文件名中不能出现#号，否则就出错？这是为什么
            '''
        else:
            return "<h1>{}:{}</h1>".format(arg,path)
    except KeyError:
        return "<h1>文件不存在</h1>"

####################以下为功能函数
def download(url):
    ydl_opts = {
        #'format':'bestvideo',
        #'merge_output_format':'mp4', 后处理问题，有时候会出错 youtube 更新编码导致在最佳视频和最佳音频设置下，某些情况合并不成功
        'format': 'bestvideo+bestaudio/best',
        'outtmpl':'./downloads/%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def make_tree(path):
    tree = dict(name=os.path.basename(path),isdir=True, children=[],hashvalue=filename2hash(path))
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name,isdir=False,hashvalue=filename2hash(fn)))
    return tree


def filename2hash(name):
    md5 = hashlib.md5()
    md5.update(name.encode(encoding='UTF-8'))
    return md5.hexdigest()[:6]

def hash2filename(h,path):
    #basedir = './downloads'
    filenames = os.listdir(path)
    for filename in filenames:
        if os.path.isfile(filename):
            filename = os.path.join(path,filename)
            if filename2hash(filename) == h:
                return filename
        else:
            filename = os.path.join(path,filename)
            return hash2filename(h,filename)


def init_hashfilenames():
    global hashfilenames
    hashfilenames = {}
    def listdir(path):
        #if os.path.isfile(path):
        #    return None
        filenames = os.listdir(path)
        for filename in filenames:
            tpath = os.path.join(path,filename)
            if os.path.isdir(tpath):
                h = filename2hash(tpath)
                hashfilenames[h] = { 'filename':filename,'path':tpath}
                listdir(tpath)
            else:
                h = filename2hash(tpath)
                hashfilenames[h] = { 'filename':filename,'path':tpath}
    basedir = './downloads'
    listdir(basedir)


def gethashinfo(h):
    try:
        return hashfilenames[h]
    except KeyError:
        return None
                

def remove(path):
    '''
    采用递归的方式删除文件或目录
    原因：如果目录不为空，那么rmdir就会报错
    '''
    def t_remove(path):
        if os.path.isdir(path):
            for filename in os.listdir(path):
                t_path = os.path.join(path,filename)
                # if os.path.isdir(t_path):
                #     t_remove(path)
                #     os.rmdir(t_path)
                # else:
                #     os.remove(t_path)
                t_remove(t_path)
            os.rmdir(path)
        else:
            os.remove(path)
    t_remove(path)