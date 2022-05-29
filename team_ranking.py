from preprocessing import *

team_ranking_result_sheet = sheet.get_worksheet(6)

class TeamRanking:

    def __init__(self, sheet_index):
        self.round_sheet = sheet.get_worksheet(sheet_index + 4)
        self.row_list = []
        self.row_list_dictionary = {}
        self.unranked_team_list = []
        self.sorted_row_list = []
        self.get_score_and_result()
        self.populate_row_list_dictionary()
        if self.check_if_all_results_are_in():
            self.sort_sheet()
            self.write_result_to_sheet()

    def get_score_and_result(self):
        for i in range(1, len(self.round_sheet.get_all_values())):
            self.row_list.append(self.round_sheet.row_values(i + 1))
    
    def populate_row_list_dictionary(self):
        for row in self.row_list:
            if row[0] not in self.row_list_dictionary:
                self.row_list_dictionary[row[0]] = row
    
    def check_if_all_results_are_in(self):
        for team in sheet_team_list:
            if team not in self.row_list_dictionary:
                self.unranked_team_list.append(team)
        if len(self.unranked_team_list) > 0:
            print('Error: The following team/teams do(es) not have ballots: ' + str(self.unranked_team_list))
            return False
        return True

    def sort_sheet(self):
        for team in sheet_team_list:
            self.sorted_row_list.append(self.row_list_dictionary[team])
        print(self.sorted_row_list)
    
    def write_result_to_sheet(self):
        team_ranking_result_sheet.update('A2:D7', self.sorted_row_list)

team_ranking = TeamRanking(1)