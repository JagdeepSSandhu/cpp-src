from flask import Flask, render_template, request
from datetime import date, datetime
import google.auth
import os

from googleapiclient.discovery import build

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./sgsj-cpp-6a90831e84cc.json"
credentials, project = google.auth.default()
service = build('sheets', 'v4', credentials=credentials)

SPREADSHEET_ID = '1s5wucn6ivMbW6PNjqUCx-aBa4Ky7tg_pPxNXULtWbyU'
SAMPLE_RANGE_NAME = 'IDs!A2:A'

app = Flask(__name__)
print(__name__)

@app.route('/')
def home():
    current_date = date.today()
    return render_template('home.html', now=current_date)

@app.route('/test', methods=['POST'])
def mark():
    event = request.form['event'].strip()
    email = request.form['email'].lower().strip()
    if email == '':
        current_date = date.today()
        return render_template('home.html', now=current_date)
    else:
        return handleEmail(email, event)


def handleEmail(email, event):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='IDs!A2:C1000').execute()
    values = result.get('values', [])
    if not values:
        return 'No data in Spreadsheet'
    print(f"{len(values)} rows retrieved")
    import collections
    cnt = collections.Counter()
    for row in values:
        cnt[row[1].lower().strip()] += 1
    if cnt[email] == 0:
        record_with_email(email, event)
        return render_template('do_survey.html')
    if cnt[email] == 1:
        for row in values:
            if email == row[1].lower().strip():
                record_with_id(event, str(row[0]))
                if (event == 'Feb 5 - English Assessment Exam'):
                    return render_template('do_english_test.html')
                else:
                    return render_template('do_math_test.html')
    else:
        print("Got a child case")
        return render_template('child.html', email1=email, event1=event)


def record_with_email(email, event):
    body = {
        'values': [
                    [email, event, str(datetime.now())]
                  ]
    }
    sheet = service.spreadsheets()
    sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='Attendance-Email!A2:C2', valueInputOption="USER_ENTERED", body=body).execute()

def record_with_id(event, cpp_id):
    body = {
        'values': [
                    [cpp_id, event, str(datetime.now())]
                  ]
    }
    sheet = service.spreadsheets()
    sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='Attendance-ID!A2:C2', valueInputOption="USER_ENTERED", body=body).execute()


@app.route('/mark_second_stage', methods=['POST'])
def mark_second_stage():
    event = request.form['event'].strip()
    email = request.form['email'].lower().strip()
    fName = request.form['fName'].lower().strip()
    if email == '' or fName == '':
        current_date = date.today()
        return render_template('home.html', now=current_date)
    else:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='IDs!A2:C1000').execute()
        values = result.get('values', [])
        if not values:
            return 'No data in Spreadsheet'
        print(f"{len(values)} rows retrieved") 
        for row in values:
            if (email == row[1].lower() and fName == row[2].lower()):
                record_with_id(event, str(row[0]))
                return 'Thank you ' + row[2] + "! Your attendance is recorded. <br/> Your CPP ID is <b>" + str(row[0]) + "</b>."
        # No Match - do survey
        record_with_email(email, event)
        return render_template('do_survey.html')


@app.route('/getID', methods=['GET', 'POST'])
def getID(): 
    if request.method == 'GET':
        return render_template('get_id.html')
    else:
        email = request.form['email'].lower().strip()
        fName = request.form['fName'].lower().strip()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='IDs!A2:C1000').execute()
        values = result.get('values', [])
        if not values:
            return 'No data in Spreadsheet'
        print(f"{len(values)} rows retrieved")
        import collections
        cnt = collections.Counter()
        for row in values:
            cnt[row[1].lower().strip()] += 1
        if cnt[email] == 0:
            return render_template('do_survey.html')
        if cnt[email] == 1:
            for row in values:
                if email == row[1].lower().strip():
                    return "Your CPP ID is <b>" + str(row[0]) + "</b>."
        else:
            #Child 
            for row in values:
                if  fName == row[2].lower().strip() and email == row[1].lower().strip():
                    return "Your CPP ID is <b>" + str(row[0]) + "</b>."
            return render_template('do_survey.html')




if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
