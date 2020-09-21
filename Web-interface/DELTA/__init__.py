from flask import Flask, render_template ,request
import os


app = Flask(__name__)
UPLOAD_DIRECTORY = 'upload'



if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.route('/')
def homepage():
    return  render_template("index.html")

@app.route('/forms',methods=['GET','POST'])
def forms():
    if request.method == 'POST':
        data = request.form
        print(data)
        with open(os.path.join(UPLOAD_DIRECTORY, "test"), 'wb') as fp:
            fp.write(request.data)
    return render_template("forms.html")




@app.route('/data_entry/',methods=['GET','POST'])
def data_entry():

    return render_template("data_entry.html")

if __name__ == "__main__":
    app.run()
    
