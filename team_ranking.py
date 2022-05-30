import sys
from get_google_sheets import *

team_ranking_result_sheet = sheet.get_worksheet(9)

class TeamRanking:

    def __init__(self, round, number_of_rounds):
        # sheets contain results for each given round
        self.round_sheet = sheet.get_worksheet(round + 4)
        self.number_of_rounds = number_of_rounds
        # list of rows for each round sheet
        self.round_row_list = []
        # maps from team to list of rows for each round sheet
        self.round_row_list_dictionary = {}
        # list of teams that don't have a ballot
        self.unscored_team_list = []
        self.get_score_and_result()
        self.populate_row_list_dictionary()

        if self.check_if_all_results_are_in():
            self.sorted_row_list = []
            self.all_row_values = []
            self.team_to_row_list = {}
            self.team_to_average_list = {}
            self.team_to_score_list = []
            self.sorted_team_list = []
            self.sort_sheet()
        else:
            sys.exit()

    # read each round_sheet to get the scores and results
    def get_score_and_result(self):
        for i in range(1, len(self.round_sheet.get_all_values())):
            self.round_row_list.append(self.round_sheet.row_values(i + 1))

    # maps from team to the row of scores and results
    def populate_row_list_dictionary(self):
        for row in self.round_row_list:
            team = row[0]
            if team not in self.round_row_list_dictionary:
                # int(row[1: 2][0]) is the score
                self.round_row_list_dictionary[team] = int(row[1: 2][0])

    def check_if_all_results_are_in(self):
        for team in team_list:
            if team not in self.round_row_list_dictionary:
                self.unscored_team_list.append(team)
        if len(self.unscored_team_list) > 0:
            print('Error: The following team/teams do(es) not have ballots: ' + str(self.unscored_team_list))
            return False
        return True

    def sort_sheet(self):
        for team in team_list:
            self.sorted_row_list.append(self.round_row_list_dictionary[team])

    def write_score_to_sheet(self):
        for round in range(self.number_of_rounds):
            team_ranking_result_sheet.update_cell(1, round + 3, 'ROUND ' + str(round + 1))
        team_ranking_result_sheet.update('C2', self.team_to_score_list)

    def write_average_to_sheet(self):
        team_ranking_result_sheet.update_cell(1, 1, 'RANKING')
        team_ranking_result_sheet.update_cell(1, 2, 'TEAM')
        team_ranking_result_sheet.update_cell(1, self.number_of_rounds + 3, 'AVERAGE')
        for i in range(len(self.sorted_team_list)):
            team_ranking_result_sheet.update_cell(i + 2, 1, i + 2)
            team_ranking_result_sheet.update_cell(i + 2, 2, self.sorted_team_list[i])
            team_ranking_result_sheet.update_cell(i + 2, self.number_of_rounds + 3, self.team_to_average_list[self.sorted_team_list[i]])

    def convert(self, tuple, dictionary):
        dictionary = dict(tuple)
        return dictionary

    def loop(self):

        for i in range(1, 5):
            team_ranking = TeamRanking(i, 4)
            self.sorted_row_list = team_ranking.sorted_row_list
            self.all_row_values.append(self.sorted_row_list)

        for team in range(len(team_list)):
            if team_list[team] not in self.team_to_average_list:
                self.team_to_average_list[team_list[team]] = [sum(row[j] for row in self.all_row_values) for j in range(len(self.all_row_values[0]))][team]/self.number_of_rounds

        sorted_average_list = sorted(self.team_to_average_list.items(), key=lambda x: x[1], reverse=True)
        self.team_to_average_list = self.convert(sorted_average_list, self.team_to_average_list)

        for team in range(len(team_list)):
            if team_list[team] not in self.team_to_row_list:
                self.team_to_row_list[team_list[team]] = [x[team] for x in self.all_row_values]

        for team in self.team_to_average_list:
            self.team_to_score_list.append(self.team_to_row_list[team])
            self.sorted_team_list.append(team)

        self.write_score_to_sheet()
        self.write_average_to_sheet()

team_ranking = TeamRanking(1, 4)
team_ranking.loop()

# REPL, status, panda