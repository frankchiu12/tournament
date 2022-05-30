from get_google_sheets import *

teamid_sheet = sheet.get_worksheet(1)

class PreProcessing:

    def __init__(self):
        self.team_to_id = {}
        self.matchup = {}
        self.generate_random_unique_id()
        self.write_to_teamid_sheet()

    # generate random and unique id for each team
    def generate_random_unique_id(self):
        flipped = {}
        is_unique = False
        not_unique_key_list = []

        # generate intialize id
        for team in team_list:
            id = str(uuid4().time_low)
            if team not in self.team_to_id:
                self.team_to_id[team] = id

        # check if the id is unique
        while not is_unique:
            if(len(not_unique_key_list) > 0):
                for team in not_unique_key_list:
                    id = str(uuid4().time_low)
                    if team not in self.team_to_id:
                        self.team_to_id[team] = id

            flipped = {}
            not_unique_key_list = []

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
                        not_unique_key_list.append(flipped_value)
                    break
                else:
                    is_unique = True

        # NOTE: this list is important for the other classes!
        print(self.team_to_id)

    def write_to_teamid_sheet(self):
        team_list = []
        id_list = []

        for key, value in self.team_to_id.items():
            team_list.append(key)
            id_list.append(value)

        teamid_sheet.update_cell(1, 1, 'TEAM')
        teamid_sheet.update_cell(1, 2, 'TEAM ID')

        # TODO: update entire column
        for i in range (2, number_of_teams + 2):
            teamid_sheet.update_cell(i, 1, team_list[i-2])
            teamid_sheet.update_cell(i, 2, id_list[i-2])

    def convert_id_to_name(self, id):
        for key, value in self.team_to_id.items():
            if value == id:
                return key
        print('ERROR: The id does not exist.')