import gspread
from oauth2client.service_account import ServiceAccountCredentials
from uuid import uuid4

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name("motion_ranking.json", scopes)
file = gspread.authorize(credentials)
sheet = file.open("Motion Ranking")
team_sheet = sheet.get_worksheet(0)

team_list = team_sheet.col_values(1)
del team_list[0:1]
team_list = team_list
number_of_teams = len(team_list)
print(number_of_teams)