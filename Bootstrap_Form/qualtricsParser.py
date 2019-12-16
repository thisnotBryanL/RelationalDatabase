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

    #THIS IS THE AMOUNT OF ENTRY PER USER
    print('Responses = ',len(data['responses']))
    user_count = len(data['responses'])

    for i in range (len(data['responses'])):
        for j in range(len(qid_list)):

            print(data['responses'][i]['values'][qid_list[j]])
