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
teamid_sheet = sheet.get_worksheet(1)
matchup_sheet = sheet.get_worksheet(2)
motion_ranking_sheet = sheet.get_worksheet(3)
motion_ranking_result_sheet = sheet.get_worksheet(4)

# preprocessing uses teamid_sheet
# email_automator uses number_of_teams, team_list, and email_list

proposition_list = team_sheet.col_values(1)
del proposition_list[0:1]
team_list = proposition_list
number_of_teams = len(team_list)

opposition_list = team_sheet.col_values(2)
del opposition_list[0:1]
email_list = opposition_list