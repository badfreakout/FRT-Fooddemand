#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import pickle
import os
import requests


# In[2]:


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "hCMz6CxbIjqc0zt22E-RcxZE6_TY9D9i9jY-w-ga2nGW"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


# In[3]:


from flask import Flask,request, render_template
app=Flask(__name__,template_folder="templates")
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')
@app.route('/home', methods=['GET'])
def about():
    return render_template('home.html')
@app.route('/pred',methods=['GET'])
def page():
    return render_template('upload.html')


# In[4]:


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    print("[INFO] loading model...")
    #model = pickle.load(open('fdemand.pkl', 'rb'))
    input_features = [int(x) for x in request.form.values()]
    features_value = [[np.array(input_features)]]
    print(features_value)

    payload_scoring = {"input_data":[{"field": [['homepage_featured', 'emailer_for_promotion', 'op_area', 'cuisine',
       'city_code', 'region_code', 'category']],"values": [input_features ]}]}
    
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/09a04c27-91d1-4cb3-8be9-fd567865ce20/predictions?version=2022-01-21', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions =response_scoring.json()
    print(predictions)
    print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])
    pred = int(predictions['predictions'][0]['values'][0][0])

    #prediction = model.predict(features_value)
    #output=prediction[0]    
    #print(output)
    print(pred)
    return render_template('upload.html', prediction_text=pred)


# In[ ]:


if __name__ == '__main__':
      app.run(debug=False)


# In[ ]:




