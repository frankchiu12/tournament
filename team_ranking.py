from get_google_sheets import *

team_ranking_result_sheet = sheet.get_worksheet(9)

class TeamRanking:

    def __init__(self, round, total_number_of_rounds):
        self.round_sheet = sheet.get_worksheet(round + 4)
        self.total_number_of_rounds = total_number_of_rounds
        self.row_list = []
        self.row_list_dictionary = {}
        self.unranked_team_list = []
        self.sorted_row_list = []
        self.all_row_values = []
        self.team_to_row = {}
        self.team_to_average = {}

        # optimizing
        self.team_to_row_list = {}
        self.team_to_average_list = {}
        self.get_score_and_result()
        self.populate_row_list_dictionary()
        if self.check_if_all_results_are_in():
            self.sort_sheet()
            #self.write_result_to_sheet(round)

    def get_score_and_result(self):
        for i in range(1, len(self.round_sheet.get_all_values())):
            self.row_list.append(self.round_sheet.row_values(i + 1))

    def populate_row_list_dictionary(self):
        for row in self.row_list:
            if row[0] not in self.row_list_dictionary:
                self.row_list_dictionary[row[0]] = int(row[1: 2][0])

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

    def write_result_to_sheet(self, round):
        team_ranking_result_sheet.update_cell(1, 1, 'TEAM')
        team_ranking_result_sheet.update_cell(1, round + 1, 'ROUND ' + str(round))
        for i in range(2, len(sheet_team_list) + 2):
            team_ranking_result_sheet.update_cell(i, 1, sheet_team_list[i - 2])
        # for i in range(2, len(sheet_team_list) + 2):
        #     team_ranking_result_sheet.update_cell(i, round + 1, int(self.sorted_row_list[i - 2][0]))

    def calculate_average_using_list():
        pass
    
    def calculate_average(self):
        for i in range(1, len(sheet_team_list) + 1):
            if sheet_team_list[i - 1] not in self.team_to_row:
                self.team_to_row[sheet_team_list[i - 1]] = team_ranking_result_sheet.row_values(i + 1)
        for i in range(1, len(sheet_team_list) + 1):
            if sheet_team_list[i - 1] not in self.team_to_average:
                self.team_to_average[sheet_team_list[i - 1]] = self.team_to_row[sheet_team_list[i - 1]][1: int(self.total_number_of_rounds + 1)]
        for team in sheet_team_list:
            self.team_to_average[team] = sum([int(i) for i in self.team_to_average[team]])/self.total_number_of_rounds

    def write_average_to_sheet(self):
        for i in range(2, len(sheet_team_list) + 2):
            team_ranking_result_sheet.update_cell(i, self.total_number_of_rounds + 2, self.team_to_average[sheet_team_list[i]])

    def loop(self):
        for i in range(1, 5):
            team_ranking = TeamRanking(i, 4)
            self.sorted_row_list = team_ranking.sorted_row_list
            self.all_row_values.append(self.sorted_row_list)
        
        for team in range(len(sheet_team_list)):


        for team in range(len(sheet_team_list)):
            if sheet_team_list[i] not in self.team_to_average_list:
                self.team_to_average_list[sheet_team_list[team]] = [sum(row[j] for row in self.all_row_values) for j in range(len(self.all_row_values[0]))][team]/self.total_number_of_rounds
        print(self.team_to_average_list)

team_ranking = TeamRanking(1, 4)
team_ranking.loop()

# REPL, status