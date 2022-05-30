import sys
from get_google_sheets import *

team_ranking_result_sheet = sheet.get_worksheet(9)
team_status_list = team_sheet.col_values(3)
ESL_team_ranking_result_sheet = sheet.get_worksheet(10)
del team_status_list[0:1]
status_list = ['ESL', 'Novice']

class TeamRanking:

    def __init__(self, round, number_of_rounds):
        # sheets containing results for each given round
        self.round_sheet = sheet.get_worksheet(round + 4)
        self.number_of_rounds = number_of_rounds
        # list of rows for each round sheet
        self.round_row_list = []
        # maps from team to list of scores for each round sheet
        self.team_to_score = {}
        # maps from team to list of results for each round sheet
        self.team_to_result = {}
        # list of teams that don't have a ballot
        self.no_ballot_team_list = []
        self.get_score_and_result()
        self.populate_row_list_dictionary()

        if self.check_if_all_ballots_are_in():
            self.team_to_average = {}
            self.team_to_win = {}
            self.team_to_loss = {}
            self.team_to_win_count = {}
            self.team_to_win_count_and_average = {}
            # TODO: replace with instance variables
            self.win_count_list = []
            # list of scores to write into team_ranking_result_sheet
            self.score_list = []
            # ranked list of teams
            self.average_list = []
            self.ranking_number_list = []
            self.ranked_team_list = []
            self.ranked_team_to_row = {}
            self.status_to_team = {}
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
            if team not in self.team_to_score:
                # int(row[1: 2][0]) is the score
                score_list = []
                score_list.append(int(row[1: 2][0]))
                self.team_to_score[team] = score_list
            if team not in self.team_to_result:
                # row[2: 4] is the win and lost column
                result_list = []
                result_list.append(row[2: 4])
                self.team_to_result[team] = result_list

    # checks if all the ballots for the teams in the matchup are in
    def check_if_all_ballots_are_in(self):
        for team in team_list:
            if team not in self.team_to_score:
                self.no_ballot_team_list.append(team)
        if len(self.no_ballot_team_list) > 0:
            print('Error: The following team/teams do(es) not have ballot(s): ' + str(self.no_ballot_team_list))
            return False
        return True

    # TODO: write to entire column

    # write the ranking, teams, and averages to team_ranking_result_sheet
    def write_average_to_sheet(self):
        team_ranking_result_sheet.update_cell(1, 1, 'RANKING')
        team_ranking_result_sheet.update_cell(1, 2, 'TEAM')
        team_ranking_result_sheet.update_cell(1, self.number_of_rounds + 4, 'AVERAGE')
        team_ranking_result_sheet.update('A2', self.ranking_number_list)
        team_ranking_result_sheet.update('B2', self.ranked_team_list)
        team_ranking_result_sheet.update(str(chr(ord('@')+self.number_of_rounds + 4)) + str(2) + ':' + str(chr(ord('@')+self.number_of_rounds + 4)) + str(number_of_teams + 1), self.average_list)

    # write the round and scores to team_ranking_result_sheet
    def write_score_to_sheet(self):
        for round in range(self.number_of_rounds):
            team_ranking_result_sheet.update_cell(1, round + 3, 'ROUND ' + str(round + 1))
        team_ranking_result_sheet.update('C2', self.score_list)

    # TODO: write to entire column

    def write_win_count_to_sheet(self):
        team_ranking_result_sheet.update_cell(1, 7, 'WINS')
        team_ranking_result_sheet.update(str(chr(ord('@')+self.number_of_rounds + 3)) + str(2) + ':' + str(chr(ord('@')+self.number_of_rounds + 3)) + str(number_of_teams + 1), self.win_count_list)

    # converts a list of tuples into a dictionary
    def convert(self, tuple, dictionary):
        dictionary = dict(tuple)
        return dictionary

    def populate_ranked_team_to_row_dictionary(self):
        for i in range(2, number_of_teams + 2):
            if team_ranking_result_sheet.row_values(i)[1] not in self.ranked_team_to_row:
                self.ranked_team_to_row[team_ranking_result_sheet.row_values(i)[1]] = team_ranking_result_sheet.row_values(i)[1 : self.number_of_rounds + 4]

    def rank_on_status(self):
        for i in range(number_of_teams):
            if team_status_list[i] not in self.status_to_team:
                self.status_to_team[team_status_list[i]] = []
            self.status_to_team[team_status_list[i]].append(team_list[i])
        for key, value in self.status_to_team.items():
            if key == 'ESL':
                ESL_team_row = []
                for team in self.ranked_team_to_row:
                    for ESL_team in value:
                        if ESL_team == team:
                            ESL_team_row.append(self.ranked_team_to_row[team])
                ESL_team_ranking_result_sheet.update('B2:' + str(chr(ord('@')+self.number_of_rounds + 4)) + str(len(ESL_team_row) + 1), ESL_team_row)

    # iterate through each round to get the wins and averages to rank on
    def loop(self):

        # iterate through 4 rounds
        for i in range(1, self.number_of_rounds + 1):
            team_ranking = TeamRanking(i, self.number_of_rounds)
            if i != 1:
                for team in team_list:
                    self.team_to_score[team] = self.team_to_score[team] + team_ranking.team_to_score[team]
                    self.team_to_result[team] = self.team_to_result[team] + team_ranking.team_to_result[team]

        # maps from team to average, win, and loss
        for i in range(number_of_teams):
            # average
            if team_list[i] not in self.team_to_average:
                self.team_to_average[team_list[i]] = sum(self.team_to_score[team_list[i]])/self.number_of_rounds
            # win
            if team_list[i] not in self.team_to_win:
                self.team_to_win[team_list[i]] = [round[0] for round in self.team_to_result[team_list[i]]]
            # loss
            if team_list[i] not in self.team_to_loss:
                self.team_to_loss[team_list[i]] = [round[1] for round in self.team_to_result[team_list[i]]]

        for team in team_list:
            if team not in self.team_to_win_count:
                self.team_to_win_count[team] = len([result for result in self.team_to_win[team] if result != 'None'])

        for team in team_list:
            if team not in self.team_to_win_count_and_average:
                self.team_to_win_count_and_average[team] = [self.team_to_win_count[team]] + [self.team_to_average[team]]

        sorted_win_count_and_average_list = sorted(self.team_to_win_count_and_average.items(), key=lambda x: (x[1], x[1][1]), reverse=True)

        self.team_to_win_count_and_average = self.convert(sorted_win_count_and_average_list, self.team_to_win_count_and_average)

        # list of scores and teams to write into team_ranking_result_sheet, and the iteration is sorted

        counter = 1
        for team in self.team_to_win_count_and_average:
            self.ranking_number_list.append([counter])
            self.ranked_team_list.append([team])
            self.win_count_list.append([self.team_to_win_count[team]])
            self.score_list.append(self.team_to_score[team])
            self.average_list.append([self.team_to_average[team]])
            counter += 1

        self.write_score_to_sheet()
        self.write_win_count_to_sheet()
        self.write_average_to_sheet()
        team_ranking_result_sheet.format('A1:H1', {'textFormat': {'bold': True}})

        print('The ranking for the teams is as follows: \n')
        counter = 1
        for team in self.team_to_win_count_and_average:
            print(str(counter) + '. ' + str(team))
            counter = counter + 1

        self.populate_ranked_team_to_row_dictionary()
        self.rank_on_status()

team_ranking = TeamRanking(1, 4)
team_ranking.loop()

# REPL, status (win), panda