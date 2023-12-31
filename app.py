from flask import Flask,render_template,request
import numpy as np
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import joblib



def preprocess(t):
    p=PorterStemmer()
    text = re.sub('[^a-zA-Z]',' ',t)
    text = text.lower()
    text = text.split()
    text = [p.stem(i) for i in text]
    text = ' '.join(text)
    return text

cv = joblib.load('cv')
model = joblib.load('model')


app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
        message = request.form['text']
        message = preprocess(message)
        data = [message]
        vect = cv.transform(data).toarray()
        prediction = model.predict(vect)
        print(prediction)
        
    return render_template('result.html',pred = prediction,msg=message)

@app.route('/piechart')
def piechart():
    return render_template('piechart.html')

@app.route('/about')
def about():
    return render_template('about.html')






if __name__=='__main__':
    app.run(debug=True)