"""
Some of the reviews are entered via Qualtrics. Qualtrics provides a form for each review to be used by multiple reviewers.
Once the reviews are collected, it can output the results as a CSV file.

You are to read in the CSV file and input the result of the review to the database.

You can assume the csv file to be as follows:
•Each column correspond to the answer of the question. The questions are ordered by the ordering assigned

•Each row is a response for a person.

"""

import csv


def qualtricsParser(filename):
    file = open(filename)
    #Read in question name and match it to col
