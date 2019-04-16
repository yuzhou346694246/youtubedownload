from flask import Flask,request,url_for,render_template

app = Flask(__name__)

#url_for('static',fi)

@app.route("/", methods=['GET','POST'])
def index():
    #return "Hello Dongge!"
    if request.method == 'GET':
        return render_template('index.html')
    else:
        pass