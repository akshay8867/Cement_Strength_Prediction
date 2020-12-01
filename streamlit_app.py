
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
from predictFromModel import prediction
import streamlit as st
import pandas as pd



def trainRouteClient():
    try:

        user_input = st.text_input("Enter the name of folder containing files for training", "default")
        if user_input!="default":
            path=user_input
            # print(path)
            train_valObj = train_validation(path)
            df=train_valObj.train_validation()
            if len(df)>0:
                st.write("The processed data used for training")
                st.write(df)
            trainModelObj = trainModel()  # object initialization
            training_msg=trainModelObj.trainingModel()  # training the model for the files in the table
            if len(training_msg)>0:
                st.write(training_msg)

    except Exception as e:
        st.write("Error Occurred!:",e)

def predictRouteClient():
    try:
        user_input = st.text_input("Enter the name of folder containing files for prediction", "default")
        if user_input!="default":

            path=user_input

            pred_val = pred_validation(path) #object initialization


            df=pred_val.prediction_validation() #calling the prediction_validation function
            if len(df)>0:
                st.subheader("The Predicted cement strength for each input is")
                # st.write(df)

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_data,result = pred.predictionFromModel()
            if len(result)>0:
                df1=pd.concat([df,result],axis=1,ignore_index=True)
                df1.columns = list(df.columns.values) + list(result.columns.values)
                st.write(df1)
    except Exception as e:
        st.write("Error Occurred!:", e)


if __name__ == "__main__":
    st.title('Cement Strength Prediction')
    option = st.selectbox('Do you want to train the model or predict?', ('None', 'Training', 'Prediction', 'Mobile phone'))
    if option == 'Training':
        trainRouteClient()

    if option == 'Prediction':
        predictRouteClient()