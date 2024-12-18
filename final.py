from flask import Flask,render_template,request,redirect,url_for
from tensorflow.keras.preprocessing import image
from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
import os
import mysql.connector

UPLOAD_FOLDER = 'static/file/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mydb=mysql.connector.connect(host='localhost',user='root',password='',database='ocr')
mycursor=mydb.cursor()
@app.route('/')
def home():
    return render_template('abcd.html')
    #return render_template('index1.html')
@app.route('/login')
def login():
    return render_template('index1.html')
@app.route('/home')
def about():
    return render_template('home.html')

@app.route("/Nnewuser")
def Nnewuser():
    return render_template('newuser.html')

@app.route("/user", methods=['GET', 'POST'])
def user():
    error = None
    global data1
    if request.method == 'POST':
        data1 = request.form.get('name')
        data2 = request.form.get('password')
        sql = "SELECT * FROM `reg` WHERE `name` = %s AND `password` = %s"
        val = (data1, data2)
        mycursor.execute(sql, val)
        account = mycursor.fetchall()
        print(account)
        if account:
            return render_template('index.html')
        else:
            return render_template('wrong.html')

@app.route("/Newuser", methods=['GET', 'POST'])
def Admin():
    if request.method == 'POST':
        name = request.form['name']
        email=request.form['email']
        password = request.form['password']
        cpassword=request.form['cpassword']

        insertQuery = "INSERT INTO reg VALUES ('" + name + "','" + email + "','" + password + "','" + cpassword + "')"
        mycursor.execute(insertQuery)
        mydb.commit()

    return render_template('index1.html')


classes = ['Bacterial Leaf Blight', 'Brown Spot', 'Healthy', 'Leaf Blast', 'Leaf Blight', 'Leaf Scald', 'Leaf Smut', 'Narrow Brown Spot']
sym = {'Bacterial Leaf Blight':'Pseudomonas savastanoi',
        'Brown Spot':'Magnaporthe grisea',
        'Healthy':'Cochliobolus miyabeanus',
        'Leaf Blast':'Burkholderia glumae',
        'Leaf Blight':'Dicladispa armigera',
        'Leaf Scald':'Tilletia horrida',
        'Leaf Smut':'Entyloma',
        'Narrow Brown Spot':'genus Sobemovirus'
        }
# Updated fertilizer information based on the provided classes
ferti = {'Bacterial Leaf Blight': 'For bacterial leaf blight, apply copper-based fungicides.',
         'Brown Spot': 'For brown spot disease, apply nitrogen-rich fertilizers such as urea.',
         'Healthy': 'No specific fertilizer recommendation for healthy plants.',
         'Leaf Blast': 'For leaf blast disease, apply potassium-rich fertilizers.',
         'Leaf Blight': 'For leaf blight disease, apply fungicides containing copper or chlorothalonil.',
         'Leaf Scald': 'For leaf scald disease, apply nitrogen-rich fertilizers in moderation.',
         'Leaf Smut': 'For leaf smut disease, apply phosphorus-rich fertilizers.',
         'Narrow Brown Spot': 'For narrow brown spot disease, apply nitrogen-rich fertilizers such as urea.'
        }
@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file1 = request.files['filename']
        imgfile = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(imgfile)
        model = load_model('model.h5')

        img_ = image.load_img(imgfile, target_size=(224, 224))
        img_array = image.img_to_array(img_)
        img_processed = np.expand_dims(img_array, axis=0)
        img_processed /= 255.
        prediction = model.predict(img_processed)
        print(prediction)
        index = np.argmax(prediction)
        result = str(classes[index]).title()
        sy = sym[result]
        fer = ferti[result]
        return render_template('index.html', msg = result, src = imgfile, view = 'style=display:block', msg1 = fer, msg2 = sy)

if __name__ == '__main__':
    app.run(debug=True,port=9000)

