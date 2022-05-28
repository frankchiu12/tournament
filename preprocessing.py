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
ranking_result_sheet = sheet.get_worksheet(4)

col_1 = team_sheet.col_values(1)
del col_1[0:1]
sheet_team_list = col_1

class PreProcessing:

    def __init__(self):
        self.team_to_id = {}
        self.matchup = {}
        self.generate_random_id()
        self.write_to_google_sheet()

    def generate_random_id(self):

        flipped = {}
        is_unique = False
        not_unique_keys_to_change_list = []

        for team in sheet_team_list:
            unique_id = str(uuid4().time_low)
            if team not in self.team_to_id:
                self.team_to_id[team] = ''
            self.team_to_id[team] = unique_id

        while not is_unique:
            if(len(not_unique_keys_to_change_list) > 0):
                for team in not_unique_keys_to_change_list:
                    unique_id = str(uuid4().time_low)
                    if team not in self.team_to_id:
                        self.team_to_id[team] = ''
                    self.team_to_id[team] = unique_id

            not_unique_keys_to_change_list = []
            flipped = {}

            for key, value in self.team_to_id.items():
                if value not in flipped:
                    flipped[value] = [key]
                else:
                    flipped[value].append(key)

            for key, value in self.team_to_id.items():
                if len(flipped[value]) > 1:
                    is_unique = False
                    flipped_value_split = flipped[value]
                    for flipped_value in flipped_value_split:
                        not_unique_keys_to_change_list.append(flipped_value)
                    break
                else:
                    is_unique = True

        for key, value in self.team_to_id.items():
            print('\n' + str(key) + ' : ' + str(value) + '\n')
        
        print(self.team_to_id)

    def write_to_google_sheet(self):
        team_list = []
        id_list = []
        for key, value in self.team_to_id.items():
            team_list.append(key)
            id_list.append(value)
        team_teamid_sheet.update_cell(1, 1, 'TEAM')
        team_teamid_sheet.update_cell(1, 2, 'TEAM ID')
        for i in range (2, len(team_list) + 2):
            team_teamid_sheet.update_cell(i, 1, team_list[i-2])
        for i in range (2, len(id_list) + 2):
            team_teamid_sheet.update_cell(i, 2, id_list[i-2])

    def convert_id_to_name(self, id):
        for key, value in self.team_to_id.items():
            if value == id:
                return key
        print('That id does not exist')