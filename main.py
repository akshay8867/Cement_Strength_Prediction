from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
from predictFromModel import prediction
import streamlit as st
import pandas as pd
import numpy as np
from enum import Enum
from io import BytesIO, StringIO
from typing import Union
# import flask_monitoringdashboard as dashboard
# from predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
# dashboard.bind(app)
CORS(app)










@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_data,result = pred.predictionFromModel()
            return Response(json_data)
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)


@app.route("/train", methods=['POST'])
@cross_origin()

def trainRouteClient():
    try:
        if request.json['folder_path'] is not None:
            path=request.json['folder_path']
            print(path)
            train_valObj = train_validation(path)
            df=train_valObj.train_validation()

            trainModelObj = trainModel()  # object initialization
            training_msg=trainModelObj.trainingModel()  # training the model for the files in the table
    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

port = int(os.getenv("PORT",5001))
if __name__ == "__main__":
    # st.title('Cement Strength Prediction')
    # option = st.selectbox('Do you want to train the model or predict?', ('None', 'Training', 'Prediction', 'Mobile phone'))
    # if option == 'Training':
    #     trainRouteClient()
    #
    # if option == 'Prediction':
    #     predictRouteClient()


    host='0.0.0.0'
    httpd = simple_server.make_server( host,port, app)
    print("Serving on %s %d" % ( host,port))
    httpd.serve_forever()


