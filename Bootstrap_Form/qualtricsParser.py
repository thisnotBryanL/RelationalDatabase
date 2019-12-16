"""
Some of the reviews are entered via Qualtrics. Qualtrics provides a form for each review to be used by multiple reviewers.
Once the reviews are collected, it can output the results as a CSV file.

You are to read in the CSV file and input the result of the review to the database.

You can assume the csv file to be as follows:
•Each column correspond to the answer of the question. The questions are ordered by the ordering assigned

•Each row is a response for a person.


******THE import button will call this function every time to reupdate the qualtrics survey count

"""


import requests
import zipfile
import json
import io, os
import sys

# Setting user Parameters
def qualtricsParser():
    try:
        apiToken = 'xXu7jFHNsSTtnh6z3rHiWYUYm9GzhJgu4Z1ZWrwd'
    except KeyError:
        print("set environment variable APIKEY")
        sys.exit(2)

    surveyId = "SV_beZBc55hPyvePeB"
    dataCenter = 'baylor.ca1'

    # Setting static parameters
    requestCheckProgress = 0.0
    progressStatus = "inProgress"
    url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(dataCenter, surveyId)
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
    }

    # Step 1: Creating Data Export
    data = {
            "format": "json",
           }

    downloadRequestResponse = requests.request("POST", url, json=data, headers=headers)

    try:
        progressId = downloadRequestResponse.json()["result"]["progressId"]
    except KeyError:
        sys.exit(2)

    isFile = None

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while progressStatus != "complete" and progressStatus != "failed" and isFile is None:
        requestCheckUrl = url + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        try:
            isFile = requestCheckResponse.json()["result"]["fileId"]
        except KeyError:
            1 == 1
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        progressStatus = requestCheckResponse.json()["result"]["status"]

    # step 2.1: Check for error
    # if progressStatus is "failed":
    #     raise Exception("export failed")

    fileId = requestCheckResponse.json()["result"]["fileId"]

    # Step 3: Downloading file
    requestDownloadUrl = url + fileId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall("MyQualtricsDownload")


    with open("MyQualtricsDownload/(TEST)Journalism project--Portfolio Review Form.json",'r') as myFile:
        data = json.load(myFile)

    qid_list = ["QID68_TEXT","QID69_TEXT","QID172807676","QID58","QID59","QID60","QID61",
                "QID55_TEXT","QID62","QID63","QID64","QID65","QID66","QID67_TEXT"]

    Qlist = [
        ["QID68_TEXT", "Student Baylor ID?", "12-16-2019"],
        ["QID69_TEXT","Portfolio Reviewer Name","12-16-2019"],
        ["QID172807676","Photo Resolution","12-16-2019"],
        ["QID58","Photo Editing","12-16-2019"],
        ["QID59","Photo Technique","12-16-2019"],
        ["QID60","Photo Variety","12-16-2019"],
        ["QUID61","Photo Creativity","12-16-2019"],
        ["QUID55_TEXT","Photo Comments","12-16-2019"],
        ["QID62","Video Quality","12-16-2019"],
        ["QID63","Video Editing","12-16-2019"],
        ["QID64","Video Technique","12-16-2019"],
        ["QID65","Video Effectiveness","12-16-2019"],
        ["QID66","Video Creativity","12-16-2019"],
        ["QID67_TEXT","Video Comment","12-16-2019"]
    ]

    # AnswerChoicesList = [
    #     ["QID68_TEXT", "12-15-2019", ANSWERLBL, VALUE]
    # ]

    '''
    for row in QList:
        sql = "INSERT INTO PortfolioReviewQ (label, question, startYear) VALUES (%s, %s, %s)"
        mycursor.execute(sql, row)

    sql = "INSERT INTO PortfolioResponses (label, startYear,baylorID,answer,dateOfReview,reviewerName) VALUES ( %s, %s,%s, %s, %s,%s)"
    '''
    '''
    #THIS IS THE AMOUNT OF ENTRY PER USER
    print('Responses = ',len(data['responses']))
    user_count = len(data['responses'])

    ResponseList = [['','','','','','']]


    for i in range (len(data['responses'])):
        for j in range(len(qid_list)):

            values = data['responses'][i]['values'][qid_list[j]]
            if j == 0:
                baylorID = values
                ResponseList[i][2] = baylorID
            elif j == 1:
                reviewerName = values
                ResponseList[i][5] = reviewerName

            if values == 1:
                newvalues = 'Above Average'
            elif values == 2 or values == 4:
                newvalues = 'Average'
            elif values == 3 or values == 5:
                newvalues = 'Below Average'
            else:
                newvalues = ''


            ResponseList[i][0] =  newvalues
            ResponseList[i][1] = "2019"
            ResponseList[i][4] = "12-16-2019"
            ResponseList[i][3]= values

            print(data['responses'][i]['values'][qid_list[j]],newvalues)

    '''