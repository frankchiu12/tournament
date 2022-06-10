from get_google_sheets import *
# This module is part of the legacy (Compat32) email API.
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# The smtplib module defines an SMTP client session object that can be used to send mail to any internet machine with an SMTP or ESMTP listener daemon.
import smtplib

# list of emails (deleting the column header)
email_list = team_sheet.get_col(2, include_tailing_empty=False)[1:]

# NOTE: need to update this variable based on the team_to_id dictionary from PreProcessing
team_to_id = {'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'}

for i in range(number_of_teams):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('motionranking@gmail.com', 'motionrankingchiu#12')
    msg = MIMEMultipart()

    msg['Subject'] = 'Your Unique Team ID for Team ' + str(team_list[i])
    msg.attach(MIMEText('Dear debater:' + '\n' + '\n' + 'This is your unique team id for Team ' + str(team_list[i]) + '. Please do not share it with anyone else since you would need this to verify your identity when you rank motions!' + '\n' + '\n' + 'TEAM ID: ' + str(team_to_id[team_list[i]]) + '\n' + '\n' + 'Sincerely, [insert org comm or competition name]'))

    to = [str(email_list[i])]
    smtp.sendmail(from_addr="motionranking@gmail.com", to_addrs=to, msg=msg.as_string())
    smtp.quit()