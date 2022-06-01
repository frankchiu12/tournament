from get_google_sheets import *
# This module provides immutable UUID objects (the UUID class) and the functions uuid1(), uuid3(), uuid4(), uuid5() for generating version 1, 3, 4, and 5 UUIDs as specified in RFC 4122.
from uuid import uuid4

team_id_sheet = sheet.worksheet_by_title('Team To ID')

class PreProcessing:

    def __init__(self):
        self.team_to_id = {}
        self.matchup = {}
        self.generate_random_unique_id()
        self.write_to_team_id_sheet()

    # generate random and unique id for each team
    def generate_random_unique_id(self):
        is_unique = False
        not_unique_key_list = []

        # generate initialize id (maps from team to id)
        for team in team_list:
            id = str(uuid4().time_low)
            if team not in self.team_to_id:
                self.team_to_id[team] = id

        # check if the id is unique
        while not is_unique:
            if(len(not_unique_key_list) > 0):
                # remake id
                for team in not_unique_key_list:
                    id = str(uuid4().time_low)
                    if team not in self.team_to_id:
                        self.team_to_id[team] = id

            # maps from id to team
            flipped = {}
            not_unique_key_list = []

            for team, id in self.team_to_id.items():
                if id not in flipped:
                    flipped[id] = [team]
                else:
                    flipped[id].append(team)

            for team, id in self.team_to_id.items():
                if len(flipped[id]) > 1:
                    is_unique = False
                    flipped_value_split = flipped[id]
                    for flipped_value in flipped_value_split:
                        not_unique_key_list.append(flipped_value)
                    break
                else:
                    is_unique = True

        # NOTE: this list is important for the other classes!
        print(self.team_to_id)

    def write_to_team_id_sheet(self):
        team_list = ['TEAM']
        id_list = ['TEAM ID']

        for team, id in self.team_to_id.items():
            team_list.append(team)
            id_list.append(id)

        team_id_sheet.update_col(1, team_list)
        team_id_sheet.update_col(2, id_list)

        # bold the row headers
        DataRange('A1','B1', worksheet=team_id_sheet).apply_format(bold)

    # convert id to team to check if the id is valid (login/user verification)
    def convert_id_to_team(self, id_to_check):
        for team, id in self.team_to_id.items():
            if id == id_to_check:
                return team
        print('ERROR: The id does not exist.')

pre_processing = PreProcessing()