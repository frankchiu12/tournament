import pygsheets
from pygsheets.datarange import DataRange

sheet = pygsheets.authorize(service_account_file='motion_ranking.json').open('Motion Ranking')

team_sheet = sheet.worksheet_by_title('Team')
team_list = team_sheet.get_col(1, include_tailing_empty=False)
del team_list[0:1]
number_of_teams = len(team_list)

bold = team_sheet.cell('A1')
bold.set_text_format('bold', True)