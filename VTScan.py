################################################################
# Name: Daniel Pena
#
# Date: 6/29/2022
# Program: Virus Total File Scanner
# Purpose: Script that uses VirusTotal's API
# to scan a list of file hashes and output the results to a file
#################################################################


import requests
import os
from os import path

#Takes user intput to take a file
def inputfile():
    fileName = input("Please input a file to scan: ")
    file_Validation(fileName)

#Checks to see if the file exsits
def file_Validation(fileName):
    try:
        ScanFile = open(fileName, 'r').readlines()
        scan(ScanFile)
    except FileNotFoundError:
        print("File not found please try again")
        inputfile()

#Takes the apikey from system varible, Then takes the hash from the file and sends a request
def scan(ScanFile):
    apikey = os.environ.get('VTAPIKey')
    for file in ScanFile:
        resource = str(file)
        VT_Url = requests.get('https://www.virustotal.com/vtapi/v2/file/report?apikey='+apikey+'&resource='+resource)
        json_response = VT_Url.json()
        response_code = int(json_response.get("response_code"))
        print(response_code)

        #IF THE HASH IS NOT FOUND IN VT DATABASE
        if response_code == 0:
            print(resource + ": HASH NOT FOUND")
            Write_File()

        #IF THE HASH IS FOUND IN VT DATABASE
        #IF THE HASH IS BAD
        elif response_code == 1:
            prmalink = str(json_response.get("prmalink"))
            totalAV = str(json_response.get("total"))
            positive_score = int(json_response.get("positives"))
            output = "Hash : " + resource + "\n" + "Total AV Engines Scaned: " + totalAV  + "\n" + "Num AV Engines Detected File Malicous: " +str(positive_score) + "\n" + "Link: " + prmalink
            if positive_score >= 1:
                print( "Hash is malicious")
                print(output)
                Write_File(output)

            #IF THE HASH IS GOOD
            else:
                print("Hash is non-malicious")
                print(output)
                Write_File(output)
        #IF USER DOES NOT HAVE ANY PROPER PRIVLIGES OR APIKEY IS BAD
        else:
            print("Forbiden or something went wrong with the apikey")


def Write_File(response):
    with open("log.txt", "a") as f:
        f.write(response)
#CLEARS THE FILE
def clean_File():
    with open("log.txt", "w") as f:
            pass

def main():
    clean_File()
    inputfile()

main()
