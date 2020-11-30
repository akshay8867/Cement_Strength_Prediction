from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

class ModelFinder:
    def __init__(self,file_object,logger_object):
        self.file_object=file_object
        self.logger_object=logger_object
        self.linearReg=LinearRegression()
        self.RandomForestReg=RandomForestRegressor()

    def get_best_params_for_Random_Forest_Regressor(self,train_x,train_y):
        self.logger_object.log(self.file_object,
                               'Entered the RandomForestReg method of the Model_Finder class')
        try:
            self.param_grid_Random_forest_tree={'n_estimators':[10,20,30],
                                                'max_features':["auto","sqrt","log2"],
                                                "min_samples_split": [2,4,8],
                                                "bootstrap":[True,False]
                                                }
            self.grid=GridSearchCV(self.RandomForestReg,self.param_grid_Random_forest_tree,cv=5,verbose=3)
            self.grid.fit(train_x,train_y)
            # extracting the best parameters
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.max_features = self.grid.best_params_['max_features']
            self.min_samples_split = self.grid.best_params_['min_samples_split']
            self.bootstrap = self.grid.best_params_['bootstrap']

            # Creating the model with best params
            self.decisionTreeReg=RandomForestRegressor(n_estimators=self.n_estimators, max_features=self.max_features,
                                                         min_samples_split=self.min_samples_split, bootstrap=self.bootstrap)
            self.decisionTreeReg.fit(train_x,train_y)
            self.logger_object.log(self.file_object,
                                   'RandomForestReg best params: ' + str(
                                       self.grid.best_params_) + '. Exited the RandomForestReg method of the Model_Finder class')
            return self.decisionTreeReg

        except Exception as e:

            self.logger_object.log(self.file_object,

                                   'Exception occured in RandomForestReg method of the Model_Finder class. Exception message:  ' + str(

                                       e))

            self.logger_object.log(self.file_object,

                                   'RandomForestReg Parameter tuning  failed. Exited the knn method of the Model_Finder class')

            raise Exception()


    def get_best_params_for_linearReg(self,train_x,train_y):
        self.logger_object.log(self.file_object,
                               'Entered the get_best_params_for_linearReg method of the Model_Finder class')
        try:
            self.param_grid_linearReg={'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False]}
            self.grid = GridSearchCV(self.linearReg, self.param_grid_linearReg, verbose=3, cv=5)
            self.grid.fit(train_x, train_y)

            self.fit_intercept = self.grid.best_params_['fit_intercept']
            self.normalize = self.grid.best_params_['normalize']
            self.copy_X = self.grid.best_params_['copy_X']

            self.linReg=LinearRegression(fit_intercept=self.fit_intercept,normalize=self.normalize,copy_X=self.copy_X)
            self.linReg.fit(train_x, train_y)

            self.logger_object.log(self.file_object,
                                   'LinearRegression best params: ' + str(
                                       self.grid.best_params_) + '. Exited the get_best_params_for_linearReg method of the Model_Finder class')
            return self.linReg
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_linearReg method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'LinearReg Parameter tuning  failed. Exited the get_best_params_for_linearReg method of the Model_Finder class')
            raise Exception()

    def get_best_model(self, train_x, train_y, test_x, test_y):
        self.logger_object.log(self.file_object,
                               'Entered the get_best_model method of the Model_Finder class')
        try:
            self.LinearReg = self.get_best_params_for_linearReg(train_x, train_y)
            self.prediction_LinearReg = self.LinearReg.predict(test_x)  # Predictions using the LinearReg Model
            self.LinearReg_error = r2_score(test_y, self.prediction_LinearReg)

            self.randomForestReg =self.get_best_params_for_Random_Forest_Regressor(train_x,train_y)
            self.prediction_randomForestReg =self.randomForestReg.predict(test_x)
            self.prediction_randomForestReg_error = r2_score(test_y, self.prediction_randomForestReg)

            if self.LinearReg_error < self.prediction_randomForestReg_error:
                return 'LinearRegression',self.LinearReg
            else:
                return 'RandomForestRegressor',self.randomForestReg
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()














