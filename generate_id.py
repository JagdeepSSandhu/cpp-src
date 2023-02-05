import google.auth
import os
from pprint import pprint
from googleapiclient.discovery import build
from datetime import datetime
from random import randrange

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./sgsj-cpp-6a90831e84cc.json"
credentials, project = google.auth.default()
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

CPPID_SHEET_ID = '1s5wucn6ivMbW6PNjqUCx-aBa4Ky7tg_pPxNXULtWbyU'
STUDENT_SURVEY_ID = '1CIeRC6JOvHHW5j223hGO5GaNj_YIBGDMT5ZzTib81Q4'
TUTOR_SURVEY_ID = '1C2ovfETla5A0DTQlyXF_oVsHdKkIuc3_7S3YdoF4EC4'

def process_students():
    #read the survey sheet
    result = sheet.values().get(spreadsheetId=STUDENT_SURVEY_ID, range='A2:D1000').execute()
    values = result.get('values', [])

    students_dic = {}
    for row in values:       
        #print(f"{row[0]}, {row[3].strip().lower()}-{row[1].strip().lower()}")
        key = f"{row[3].strip().lower()}-{row[1].strip().lower()}"
        students_dic[key] = [row[3].strip().lower(), row[1].strip().title(), row[2].strip().title(), "1"]
    #pprint(students_dic)
    
    #read the CPP-ID sheet
    result = sheet.values().get(spreadsheetId=CPPID_SHEET_ID, range="A2:E1000").execute()
    values = result.get('values', [])

    id_dic = {}
    for row in values:
        #print(f"{row[0]}, {row[1].strip().lower()}-{row[2].strip().lower()}")
        key0 = f"{row[1].strip().lower()}-{row[2].strip().lower()}"
        key1 = str(row[0])

        if key1 in id_dic:
            print(f"How the hell did the ID: {key1} get duplicated in the CPP-ID sheet")
        id_dic[key1] = key0
    #pprint(id_dic)

    count = 0
    for key in students_dic.keys():
        if key in id_dic.values():
            pass
        else:
            count += 1
            print (f'ADD: {count}' + str(students_dic[key]))
            new_id = '23' + str(randrange(10000))
            while (new_id in id_dic.keys()):
                new_id = '23' + str(randrange(10000))
            l = [new_id] + students_dic[key]
            add_to_cppid(l)


def process_tutor_volunteer():
    #read the survey sheet
    result = sheet.values().get(spreadsheetId=STUDENT_SURVEY_ID, range='A2:D1000').execute()
    values = result.get('values', [])

    tutor_dic = {} # used for both tutors and volunteers
    ###
    ### Done by hand - sore throat don't want to code more today
    ###


def add_to_cppid(row):  
    pprint(row)
    body = {
        'values': [ 
                    row
                  ]
    }
    sheet = service.spreadsheets()
    sheet.values().append(spreadsheetId=CPPID_SHEET_ID, range='IDs!A2:H2', valueInputOption="USER_ENTERED", body=body).execute()



process_students()