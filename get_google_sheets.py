# simple, intuitive python library to access google spreadsheets through the Google Sheets API v4
import pygsheets
# DataRange specifies a range of cells in the sheet. DataRange is for storing/manipulating a range of data in worksheet. This class can be used for group operations, e.g. changing format of all cells in a given range. 
from pygsheets.datarange import DataRange

# open Google Sheet
sheet = pygsheets.authorize(service_account_file='motion_ranking.json').open('Motion Ranking')

team_sheet = sheet.worksheet_by_title('Team')
# list of teams
team_list = team_sheet.get_col(1, include_tailing_empty=False)
# delete the column header
del team_list[0:1]
# global variable of the number of teams
number_of_teams = len(team_list)

# used for bolding cells
bold = team_sheet.cell('A1')
bold.set_text_format('bold', True)