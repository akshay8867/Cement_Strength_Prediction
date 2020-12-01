from sklearn.model_selection import train_test_split
from data_ingestion.data_loader import Data_getter
from data_preprocessing import preprocessing
from data_preprocessing import clustering
from best_model_finder import tuner
from file_operations import file_methods
from application_logging import logger

class trainModel:
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')

    def trainingModel(self):
        self.log_writer.log(self.file_object,'Start of Training')

        try:


            data_getter=Data_getter(self.file_object,self.log_writer)
            data=data_getter.get_data()
            # print(data.head())
            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            # print(type(preprocessor))
            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)
            # print(is_null_present)
            if (is_null_present):
                data = preprocessor.impute_missing_values(data)
            X, Y = preprocessor.separate_label_feature(data, label_column_name='Concrete_compressive _strength')
            X = preprocessor.logTransformation(X)
            kmeans = clustering.KMeansClustering(self.file_object, self.log_writer)
            number_of_clusters=kmeans.elbow_plot(X)

            ## Now add the cluster label to the data
            X=kmeans.create_clusters(X,number_of_clusters)
            X['Labels'] = Y

            list_of_clusters=X['Cluster'].unique()
        # """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""
            for i in list_of_clusters:
                cluster_data=X[X['Cluster']==i]
                cluster_features=cluster_data.drop(columns=['Cluster','Labels'],axis=1)
                cluster_label=cluster_data['Labels']
                x_train,x_test,y_train,y_test=train_test_split(cluster_features,cluster_label,test_size=1/3,random_state=36)
                x_train_scaled=preprocessor.standardScalingData(x_train)
                x_test_scaled=preprocessor.standardScalingData(x_test)
                print(x_train_scaled.shape)
                model_finder=tuner.ModelFinder(self.file_object,self.log_writer)
                # print(type(model_finder))

                best_model_name,best_model=model_finder.get_best_model(x_train_scaled,y_train,x_test_scaled,y_test)
                print(best_model_name)
                file_op=file_methods.File_Operation(self.file_object,self.log_writer)
                save_model=file_op.save_model(best_model,best_model_name + str(i))
            self.log_writer.log(self.file_object, 'Successful End of Training')
            self.file_object.close()
            return 'Successful End of Training'
        except Exception as e:
            self.log_writer.log(self.file_object,'Unsuccessful End of Training')
            self.file_object.close()
            raise e




























