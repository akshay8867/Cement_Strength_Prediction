import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

class Preprocessor:

    def __init__(self,file_object,logger_object):
        self.file_object=file_object
        self.logger_object=logger_object


    def remove_columns(self,data,columns):
        self.logger_object.log(self.file_object, 'Entered the remove_columns method of the Preprocessor class')
        self.data=data
        self.columns=columns
        try:
            self.useful_data = self.data.drop(labels=self.columns, axis=1)
            self.logger_object.log(self.file_object,
                               'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in remove_columns method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            raise Exception()

    def separate_label_feature(self, data, label_column_name):
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X=data.drop(columns=[label_column_name],axis=1)
            self.Y=data[label_column_name]
            self.logger_object.log(self.file_object,
                               'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X,self.Y

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')

            raise Exception()

    def dropUnnecessaryColumns(self, data, columnNameList):

        data = data.drop(columnNameList, axis=1)
        return data

    def replaceInvalidValuesWithNull(self, data):

        for column in data.columns:
            count = data[column][data[column] == '?'].count()
            if count!=0:
                data[column]=data[column].replace('?',np.nan)
        return data

    def is_null_present(self,data):
        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        self.cols_with_missing_values=[]
        self.cols=data.columns
        try:
            self.null_counts=data.isna().sum()
            for i in range(len(self.null_counts)):
                if self.null_counts[i] > 0:
                    self.null_present = True
                    self.cols_with_missing_values.append(self.cols[i])
            if self.null_present:
                self.dataframe_with_null=pd.DataFrame()
                self.dataframe_with_null['columns']=data.columns
                self.dataframe_with_null['missing_values_count']=np.asaarray(data.isna().sum())
                self.dataframe_with_null.to_csv('preprocessing_data/null_values.csv')
            self.logger_object.log(self.file_object,
                               'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present, self.cols_with_missing_values
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise e

    def standardScalingData(self,X):
        scaler=StandardScaler()
        X_scaled=scaler.fit_transform(X)
        return X_scaled

    def logTransformation(self,X):
        for column in X.columns:
            X[column] +=1
            X[column]=np.log(X[column])
        return X

    def impute_missing_values(self,data):
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data = data
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            self.new_array=imputer.fit_transform(self.data)
            self.new_data=pd.DataFrame(data=(self.new_array),columns=self.data.columns)
            self.logger_object.log(self.file_object,'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.new_data
        except Exception as e:

            self.logger_object.log(self.file_object,
                                   'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(
                                       e))

            self.logger_object.log(self.file_object,
                                   'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

    # def get_columns_with_zero_std_deviation(self, data):









































