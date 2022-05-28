from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from preprocessing import *
from color import *

team_to_id = {'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'}

for i in range(len(sheet_team_list)):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('motionranking@gmail.com', 'motionrankingchiu#12')
    msg = MIMEMultipart()

    # all this could change
    msg['Subject'] = 'Your Unique Team ID for Team ' + str(sheet_team_list[i])
    msg.attach(MIMEText('Dear debater:' + '\n' + '\n' + 'This is your unique team id for Team ' + str(sheet_team_list[i]) + '. Please do not share it with anyone else since you would need this to verify your identity when you rank motions!' + '\n' + '\n' + 'TEAM ID: ' + str(team_to_id[sheet_team_list[i]]) + '\n' + '\n' + 'Sincerely, [insert org comm or competition name]'))

    to = [str(sheet_email_list[i])]
    smtp.sendmail(from_addr="motionranking@gmail.com",
                to_addrs=to, msg=msg.as_string())
    smtp.quit()