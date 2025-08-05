import sys
import os
from os import path
sys.path.append(path.dirname((path.abspath(path.dirname(__file__)))))
cwd = os.getcwd()
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from Database import Database
from config.DatabaseConfig import *
import csv

def csvread(csvfile):    
    sql = "insert into AzQuiz (quiz, answer, hint) values "
    with open(csvfile, 'r', encoding='utf-8') as f:
        rows = csv.reader(f)
        for row in rows:
            sql += f"('{row[0]}', '{row[1]}','{row[2]}'), "
    sql = sql[:-2] + ";"
    return sql

csvfile = os.path.join(cwd, 'utils', 'src', 'azgag_v3.csv')
list = csvread(csvfile)

# db 입력
db = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT, db_name=DB_NAME)
print("DB 접속")

db.Connect()
db.execute(list)
db.close()