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
        self.no_ballot_team_list = []
        self.get_score_and_result()
        self.populate_row_list_dictionary()

        if self.check_if_all_ballots_are_in():
            # list of rows of scores and results for one round in the same order of teams
            self.sorted_row_list = []
            # all of the sorted rows for all the rounds
            self.all_rows = []
            self.team_to_average = {}
            self.team_to_row = {}
            # list of scores to write into team_ranking_result_sheet
            self.score_list = []
            # ranked list of teams
            self.ranked_team_list = []
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

    # checks if all the ballots for the teams in the matchup are in
    def check_if_all_ballots_are_in(self):
        for team in team_list:
            if team not in self.round_row_list_dictionary:
                self.no_ballot_team_list.append(team)
        if len(self.no_ballot_team_list) > 0:
            print('Error: The following team/teams do(es) not have ballot(s): ' + str(self.no_ballot_team_list))
            return False
        return True

    # sort the rows of scores and results in the same order of teams so we could index easily without checking which row belongs to which team
    def sort_sheet(self):
        for team in team_list:
            self.sorted_row_list.append(self.round_row_list_dictionary[team])

    # write the round and scores to team_ranking_result_sheet
    def write_score_to_sheet(self):
        for round in range(self.number_of_rounds):
            team_ranking_result_sheet.update_cell(1, round + 3, 'ROUND ' + str(round + 1))
        team_ranking_result_sheet.update('C2', self.score_list)

    # TODO: write to entire column

    # write the ranking, teams, and averages to team_ranking_result_sheet
    def write_average_to_sheet(self):
        team_ranking_result_sheet.update_cell(1, 1, 'RANKING')
        team_ranking_result_sheet.update_cell(1, 2, 'TEAM')
        team_ranking_result_sheet.update_cell(1, self.number_of_rounds + 4, 'AVERAGE')
        for i in range(len(self.ranked_team_list)):
            # ranking
            team_ranking_result_sheet.update_cell(i + 2, 1, i + 1)
            # team
            team_ranking_result_sheet.update_cell(i + 2, 2, self.ranked_team_list[i])
            # average
            team_ranking_result_sheet.update_cell(i + 2, self.number_of_rounds + 4, self.team_to_average[self.ranked_team_list[i]])

    # converts a list of tuples into a dictionary
    def convert(self, tuple, dictionary):
        dictionary = dict(tuple)
        return dictionary

    # iterate through each round to get the wins and averages to rank on
    def loop(self):

        # iterate through 4 rounds
        for i in range(1, 5):
            team_ranking = TeamRanking(i, 4)
            self.sorted_row_list = team_ranking.sorted_row_list
            self.all_rows.append(self.sorted_row_list)

        # maps from team to average
        for i in range(number_of_teams):
            if team_list[i] not in self.team_to_average:
                self.team_to_average[team_list[i]] = [sum(row[j] for row in self.all_rows) for j in range(len(self.all_rows[0]))][i]/self.number_of_rounds

        # sort self.team_to_average dictionary by the average in descending order
        sorted_average_list = sorted(self.team_to_average.items(), key=lambda x: x[1], reverse=True)
        self.team_to_average = self.convert(sorted_average_list, self.team_to_average)

        # maps from team to row
        for i in range(number_of_teams):
            if team_list[i] not in self.team_to_row:
                self.team_to_row[team_list[i]] = [x[i] for x in self.all_rows]

        # list of scores and teams to write into team_ranking_result_sheet
        for team in self.team_to_average:
            self.score_list.append(self.team_to_row[team])
            self.ranked_team_list.append(team)

        self.write_score_to_sheet()
        self.write_average_to_sheet()
        team_ranking_result_sheet.format('A1:H1', {'textFormat': {'bold': True}})

team_ranking = TeamRanking(1, 4)
team_ranking.loop()

# REPL, status, panda, wins