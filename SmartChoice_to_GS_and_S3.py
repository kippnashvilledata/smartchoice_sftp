import paramiko
import csv
from paramiko import SSHClient
import tkinter.filedialog
import pysftp as sftp
# this module is new - you will need to pip install this
import pygsheets
import pandas as pd
import numpy as np
import boto3
import json

#connection to SFTP
client = SSHClient()
client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
client.connect('sftp.smartchoiceschools.com',22, 'kippnashville', 'baitVAMcask')
sftp = client.open_sftp()

##### connect to SFTP - SmartChoice files and download them to local drive #####

#!you will need to change the localpath to the path you will use to store the sftp files!#

#application submissions export
localpath=  '/home/KIPPNashvilleData/smartchoice_application_export.csv'
remotepath= '/SISData/2025DataTeamApplicationSubmissionsExport.csv'
sftp.get(remotepath, localpath)

#lottery and enrollment export 23-24
#localpath2= '/home/KIPPNashvilleData/smartchoice_lottery_enrollment_export_2324.csv'
#remotepath2= '/SISData/2023DataTeamLotteryandEnrollmentExport2023.csv'
#sftp.get(remotepath2, localpath2)

#lottery and enrollment export 24-25
localpath3= '/home/KIPPNashvilleData/smartchoice_lottery_enrollment_export_2425.csv'
remotepath3= '/SISData/2024DataTeamLotteryandEnrollmentExport2024.csv'
sftp.get(remotepath3, localpath3)



#connect to googlesheets API#
# you have this file saved as credntials-sheet.json in your drive. you will need to rename it creds.json and store it in the the same pathway as your python script#

# scope = ['https://spreadsheets.google.com/spreadsheets', 'https://www.googleapis.com/auth/drive']
# gc = pygsheets.authorize(service_file='client_secret.json')
# gc = pygsheets.authorize(client_secret = "/home/KIPPNashvilleData/creds.json")
gc = pygsheets.authorize(service_file = "/home/KIPPNashvilleData/creds.json")



#master application tracker googlesheet#
master_applications = gc.open("Master Application Tracker")
application_submmissions = pd.read_csv('/home/KIPPNashvilleData/smartchoice_application_export.csv', encoding = "ISO-8859-1")
application_submmissions = application_submmissions.replace(np.nan, '', regex = True)
#tab - 'Application_Submissions'
pci = master_applications[0]
pci.set_dataframe(application_submmissions,(1,2))



#master enrollment tracker sy 24-25 googlesheet#
master_enrollment_2425 = gc.open("Master Enrollment Tracker 24-25")
enrollment_export2425 = pd.read_csv('/home/KIPPNashvilleData/smartchoice_lottery_enrollment_export_2425.csv', encoding = "ISO-8859-1")
enrollment_export2425 = enrollment_export2425.replace(np.nan, '', regex = True)
#tab - 'Lottery_and_Enrollment'
pci = master_enrollment_2425[0]
pci.set_dataframe(enrollment_export2425,(1,1))


#pull in aws credentials
aws_config = json.load(open("credentials_s3.json"))["awss3"]
access_key_id = aws_config["access_key_id"]
access_secret_key = aws_config["access_secret_key"]
bucket_name = aws_config["bucket_name"]

s3 = boto3.resource('s3', aws_access_key_id=access_key_id,
                    aws_secret_access_key = access_secret_key,
                   )
s3.meta.client.upload_file('/home/KIPPNashvilleData/smartchoice_application_export.csv',"kippnashville","smartchoice/2024DataTeamApplicationSubmissionsExport.csv")












