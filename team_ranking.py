import sys
from get_google_sheets import *

team_ranking_result_sheet = sheet.worksheet_by_title('Team Ranking')
team_status_list = team_sheet.get_col(3, include_tailing_empty=False)
del team_status_list[0:1]
status_list = ['ESL', 'Novice']

class TeamRanking:

    def __init__(self, round, number_of_rounds):
        self.round_sheet = sheet.worksheet_by_title('Round ' + str(round))
        self.number_of_rounds = number_of_rounds
        self.round_row_list = []
        self.team_to_score = {}
        self.team_to_result = {}
        self.no_ballot_team_list = []
        self.get_score_and_result()
        self.populate_row_list_dictionary()

        if self.check_if_all_ballots_are_in():
            self.team_to_win = {}
            self.team_to_loss = {}
            self.team_to_average = {}
            self.team_to_win_count = {}
            self.team_to_win_count_and_average = {}
            self.win_count_list = []
            self.score_list = []
            self.average_list = []
            self.ranking_number_list = []
            self.ranked_team_list = []
            self.ranked_team_to_row = {}
            self.status_to_team = {}
        else:
            sys.exit()

    def get_score_and_result(self):
        for i in range(1, number_of_teams + 1):
            self.round_row_list.append(self.round_sheet.get_row(i + 1, include_tailing_empty=False))

    def populate_row_list_dictionary(self):
        for row in self.round_row_list:
            team = row[0]
            if team not in self.team_to_score:
                self.team_to_score[team] = [int(row[1: 2][0])]
            if team not in self.team_to_result:
                self.team_to_result[team] = [row[2: 4]]

    def check_if_all_ballots_are_in(self):
        for team in team_list:
            if team not in self.team_to_score:
                self.no_ballot_team_list.append(team)
        if len(self.no_ballot_team_list) > 0:
            print('Error: The following team/teams do(es) not have ballot(s): ' + str(self.no_ballot_team_list))
            return False
        return True

    def write_average_to_sheet(self):
        team_ranking_result_sheet.update_col(1, self.ranking_number_list)
        team_ranking_result_sheet.update_col(2, self.ranked_team_list)
        team_ranking_result_sheet.update_col(self.number_of_rounds + 4, self.average_list)

    def write_score_to_sheet(self):
        team_ranking_result_sheet.update_values('C1', self.score_list)

    def write_win_count_to_sheet(self):
        team_ranking_result_sheet.update_col(self.number_of_rounds + 3, self.win_count_list)

    def convert(self, tuple, dictionary):
        dictionary = dict(tuple)
        return dictionary

    def populate_ranked_team_to_row_dictionary(self):
        for i in range(2, number_of_teams + 2):
            if team_ranking_result_sheet.get_row(i, include_tailing_empty=False)[1] not in self.ranked_team_to_row:
                self.ranked_team_to_row[team_ranking_result_sheet.get_row(i, include_tailing_empty=False)[1]] = team_ranking_result_sheet.get_row(i, include_tailing_empty=False)[1 : self.number_of_rounds + 4]

    def rank_on_status(self):
        for i in range(number_of_teams):
            if team_status_list[i] not in self.status_to_team:
                self.status_to_team[team_status_list[i]] = []
            self.status_to_team[team_status_list[i]].append(team_list[i])
        for key, value in self.status_to_team.items():
            if key == 'ESL' and len(self.status_to_team[key]) > 0:
                ESL_team_ranking_result_sheet = sheet.add_worksheet('ESL Team Ranking',rows = 1000, cols = 26) 
                ESL_ranking_number_list = []
                ESL_row_header_list = ['RANKING', 'ESL TEAM']
                ESL_team_row = []
            
                for i in range(self.number_of_rounds):
                    ESL_row_header_list.append('ROUND ' + str(i + 1))
                
                ESL_row_header_list = ESL_row_header_list + ['WINS', 'AVERAGE']

                for team in self.ranked_team_to_row:
                    for ESL_team in value:
                        if ESL_team == team:
                            ESL_team_row.append(self.ranked_team_to_row[team])

                for i in range(len(ESL_team_row)):
                    ESL_ranking_number_list.append(i + 1)

                ESL_team_ranking_result_sheet.update_row(1, ESL_row_header_list)
                ESL_team_ranking_result_sheet.update_col(1, ESL_ranking_number_list, 1)
                ESL_team_ranking_result_sheet.update_values('B2', ESL_team_row)
                DataRange('A1','Z1', worksheet=ESL_team_ranking_result_sheet).apply_format(bold)


            if key == 'Novice' and len(self.status_to_team[key]) > 0:
                novice_team_ranking_result_sheet = sheet.add_worksheet('Novice Team Ranking',rows = 1000, cols = 26) 
                novice_ranking_number_list = []
                novice_row_header_list = ['RANKING', 'NOVICE TEAM']
                novice_team_row = []
            
                for i in range(self.number_of_rounds):
                    novice_row_header_list.append('ROUND ' + str(i + 1))
                
                novice_row_header_list = novice_row_header_list + ['WINS', 'AVERAGE']

                for team in self.ranked_team_to_row:
                    for novice_team in value:
                        if novice_team == team:
                            novice_team_row.append(self.ranked_team_to_row[team])

                for i in range(len(novice_team_row)):
                    novice_ranking_number_list.append(i + 1)

                novice_team_ranking_result_sheet.update_row(1, novice_row_header_list)
                novice_team_ranking_result_sheet.update_col(1, novice_ranking_number_list, 1)
                novice_team_ranking_result_sheet.update_values('B2', novice_team_row)
                DataRange('A1','Z1', worksheet=novice_team_ranking_result_sheet).apply_format(bold)

    def loop(self):

        for i in range(1, self.number_of_rounds + 1):
            team_ranking = TeamRanking(i, self.number_of_rounds)
            if i != 1:
                for team in team_list:
                    self.team_to_score[team] = self.team_to_score[team] + team_ranking.team_to_score[team]
                    self.team_to_result[team] = self.team_to_result[team] + team_ranking.team_to_result[team]

        for i in range(number_of_teams):
            if team_list[i] not in self.team_to_average:
                self.team_to_average[team_list[i]] = sum(self.team_to_score[team_list[i]])/self.number_of_rounds
            if team_list[i] not in self.team_to_win:
                self.team_to_win[team_list[i]] = [round[0] for round in self.team_to_result[team_list[i]]]
            if team_list[i] not in self.team_to_loss:
                self.team_to_loss[team_list[i]] = [round[1] for round in self.team_to_result[team_list[i]]]

        for team in team_list:
            if team not in self.team_to_win_count:
                self.team_to_win_count[team] = len([result for result in self.team_to_win[team] if result != 'None'])
            if team not in self.team_to_win_count_and_average:
                self.team_to_win_count_and_average[team] = [self.team_to_win_count[team]] + [self.team_to_average[team]]

        sorted_win_count_and_average_list = sorted(self.team_to_win_count_and_average.items(), key=lambda x: (x[1], x[1][1]), reverse=True)

        self.team_to_win_count_and_average = self.convert(sorted_win_count_and_average_list, self.team_to_win_count_and_average)

        self.ranking_number_list.append('RANKING')
        self.ranked_team_list.append('TEAM')
        counter = 1
        round_column_header_list = []
        for round in range(1, self.number_of_rounds + 1):
            round_column_header_list = round_column_header_list + ['Round ' + str(round)]
        self.score_list.append(round_column_header_list)
        self.win_count_list.append('WINS')
        self.average_list.append('AVERAGE')

        for team in self.team_to_win_count_and_average:
            self.ranking_number_list.append(counter)
            self.ranked_team_list.append(team)
            self.win_count_list.append(self.team_to_win_count[team])
            self.score_list.append(self.team_to_score[team])
            self.average_list.append(self.team_to_average[team])
            counter += 1
        
        self.write_score_to_sheet()
        self.write_win_count_to_sheet()
        self.write_average_to_sheet()

        DataRange('A1','Z1', worksheet=team_ranking_result_sheet).apply_format(bold)

        self.populate_ranked_team_to_row_dictionary()
        self.rank_on_status()

team_ranking_result_sheet.clear('A1')
team_ranking = TeamRanking(1, 4)
team_ranking.loop()

# REPL