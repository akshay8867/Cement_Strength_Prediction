import shutil
import sqlite3
from datetime import datetime
import os
from os import listdir
import csv
from application_logging.logger import App_Logger
import pandas as pd

class dBOperation:
    """This class will be used for handling SQl operations"""
    def __init__(self):
        self.path='Training_Database/'
        self.badFilePath="Training_Raw_files_validated/Bad_Raw"
        self.goodFilePath="Training_Raw_files_validated/Good_Raw"
        self.logger=App_Logger()

    def dataBaseConnection(self,DatabaseName):
        try:
            conn=sqlite3.connect(self.path+DatabaseName +'.db')
            file=open("Training_Logs/DataBaseConnectionLog.txt",'a+')
            self.logger.log(file,"Opened %s database successfully" % DatabaseName)
            file.close()
        except Exception as e:
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % e)
            file.close()
            raise  Exception()
        return conn
    ## The reason we can use conn outside the try block because in python try and except does not lead to new scope

    def createTableDb(self,DataBaseName,column_names):

        """The try block will work only if the tables have been created"""
        try:
            conn=self.dataBaseConnection(DataBaseName)

            c=conn.cursor()
            c.execute("Select count(name) from sqlite_master where type='table' and name='Good_Raw_Data'")
            if c.fetchone()[0]==1:
                # print("hello")
                conn.close()
                file=open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file,"Tables created successfully!!")
                file.close()

                file=open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file,"Closed %s database successfully" % DataBaseName)
                file.close()
            else:
                for key in column_names.keys():
                    type=column_names[key]

                    try:
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                    except:
                        conn.execute('Create table Good_Raw_Data ({column_name} {dataType})'.format(column_name=key,dataType=type))
                conn.close()
                file=open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file,"Tables created successfully!!")
                file.close()


                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DataBaseName)
                file.close()
        except Exception as e:
            file=open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file,"Error while creating table: %s " % e)
            file.close()
            conn.close()

            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file,"Closed %s database successfully" % DataBaseName)
            file.close()
            raise e
    def insertIntoTableGoodData(self,Database):
        conn=self.dataBaseConnection(Database)
        goodFilePath=self.goodFilePath
        badFilePath=self.badFilePath
        onlyfiles=[f for f in os.listdir((goodFilePath))]
        log_file = open("Training_Logs/DbInsertLog.txt", 'a+')

        for file in onlyfiles:
            try:
                with open(goodFilePath + '/' + file,'r+') as f:
                    next(f)
                    reader=csv.reader(f,delimiter='\n')
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                self.logger.log(log_file," %s: File loaded successfully!!" % file)
                                conn.commit()
                            except Exception as e:
                                raise e
            except Exception as e:
                conn.rollback()
                self.logger.log(log_file,"Error while creating table: %s " % e)
                shutil.move(goodFilePath+'/' + file,badFilePath)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()
        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self,Database):
        self.fileName="InputFile.csv"
        self.fileFromDb='Training_FileFromDB/'
        log_file=open("Training_Logs/ExportToCsv.txt", 'a+')
        # self.fileName1 = "Input1.csv"
        try:
            conn=self.dataBaseConnection(Database)
            sql_select="SELECT *  FROM Good_Raw_Data"
            cursor=conn.cursor()
            cursor.execute(sql_select)
            results=cursor.fetchall()
            headers=[i[0] for i in cursor.description]
            df = pd.read_sql_query(sql_select, conn)

            # df=pd.DataFrame(results,columns=headers)
            df.drop_duplicates(inplace=True)



            if not os.path.isdir(self.fileFromDb):
                os.makedirs((self.fileFromDb))
            df.to_csv(self.fileFromDb + self.fileName,index=False)
            # df.to_csv()
            # csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''), delimiter=',',lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')
            # csvFile.writerow(headers)
            # csvFile.writerows(results)
            self.logger.log(log_file,"File exported successfully!!!")
            log_file.close()
            return df
        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" % e)
            log_file.close()











































