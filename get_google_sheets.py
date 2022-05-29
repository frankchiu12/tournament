from uuid import uuid4
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name("motion_ranking.json", scopes)
file = gspread.authorize(credentials)
sheet = file.open("Motion Ranking")
team_sheet = sheet.get_worksheet(0)
team_teamid_sheet = sheet.get_worksheet(1)
matchup_sheet = sheet.get_worksheet(2)
motion_ranking_sheet = sheet.get_worksheet(3)
motion_ranking_result_sheet = sheet.get_worksheet(4)

col_1 = team_sheet.col_values(1)
del col_1[0:1]
sheet_team_list = col_1

col_2 = team_sheet.col_values(2)
del col_2[0:1]
sheet_email_list = col_2