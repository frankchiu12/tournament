import random
import sys
from preprocessing import *

col_1 = matchup_sheet.col_values(1)
del col_1[0:1]
col_2 = matchup_sheet.col_values(2)
del col_2[0:1]

class MotionRanking:

    def __init__(self, team_to_id):
        self.team_to_id = team_to_id
        self.invalid_matchup_list = []
        self.matchup = {}
        self.team_to_ranking = {}
        self.unmatching_id_list = []
        self.result_list = []

        self.check_if_matchup_is_valid()
        if len(self.invalid_matchup_list) > 0:
            print('There is/are invalid team(s) in the matchup allocations: ' + str(self.invalid_matchup_list))
            sys.exit()

        self.get_matchups()
        self.get_motion_ranking()
        self.return_motion_to_debate()

    # check if the matchup is valid
    def check_if_matchup_is_valid(self):
        matchup_list = col_1 + col_2
        for team in matchup_list:
            if matchup_list.count(team) > 1:
                if team not in self.invalid_matchup_list:
                    self.invalid_matchup_list.append(team)

    def get_matchups(self):
        for i in range(len(col_1)):
            if col_1[i] not in self.matchup:
                self.matchup[col_1[i]] = col_2[i]

    def get_motion_ranking(self):
        col_2 = motion_ranking_sheet.col_values(2)
        del col_2[0:1]
        col_3 = motion_ranking_sheet.col_values(3)
        del col_3[0:1]
        col_4 = motion_ranking_sheet.col_values(4)
        del col_4[0:1]
        col_5 = motion_ranking_sheet.col_values(5)
        del col_5[0:1]
        col_6 = motion_ranking_sheet.col_values(6)
        del col_6[0:1]
        matching_id_index_list = []

        for i in range(len(col_2)):
            if self.team_to_id[col_2[i]] != col_3[i]:
                self.unmatching_id_list.append(col_2[i])
            else:
                matching_id_index_list.append(i)

        for i in matching_id_index_list:
            if col_2[i] not in self.team_to_ranking:
                self.team_to_ranking[col_2[i]] = []
            self.team_to_ranking[col_2[i]].append(col_4[i])
            self.team_to_ranking[col_2[i]].append(col_5[i])
            self.team_to_ranking[col_2[i]].append(col_6[i])

    def return_motion_to_debate(self):
        prop_team_list = []
        opp_team_list = []
        prop_team_ranking = {}
        opp_team_ranking = {}
        for key, value in self.matchup.items():
            if len(self.unmatching_id_list) != 0:
                for unmatching_id in self.unmatching_id_list:
                    if key != unmatching_id.strip('') and value != unmatching_id.strip(''):
                        prop_team_list.append(key)
                        opp_team_list.append(value)
            elif key not in self.team_to_ranking:
                continue
            else:
                prop_team_list.append(key)
                opp_team_list.append(value)

        for i in range(len(prop_team_list)):
            motion_number_to_return_list = []
            prop_team_ranking = self.team_to_ranking[prop_team_list[i]]
            opp_team_ranking = self.team_to_ranking[opp_team_list[i]]
            prop_veto = ''
            opp_veto = ''
            for j in range(3):
                if prop_team_ranking[j] == '3' or opp_team_ranking[j] == '3':
                    if prop_team_ranking[j] == '3':
                        prop_veto = j + 1
                    if opp_team_ranking[j] == '3':
                        opp_veto = j + 1
                    continue
                elif prop_team_ranking[j] == '1' and prop_team_ranking[j] == opp_team_ranking[j]:
                    motion_number_to_return_list.append(j)
                    break
                else:
                    motion_number_to_return_list.append(j)

            if len(motion_number_to_return_list) > 1:
                randomlist = [0, 1]
                motion_number_to_return_list = [random.choice(randomlist)]

            print(str(prop_team_list[i]) + ' and ' + str(opp_team_list[i]) + ' are debating Motion ' + str(int(motion_number_to_return_list[0]) + 1))

            self.write_to_result_sheets(prop_team_list[i], opp_team_list[i], str(int(motion_number_to_return_list[0]) + 1), prop_veto, opp_veto, i)

            self.result_list.append(str(prop_team_list[i]) + ' and ' + str(opp_team_list[i]) + ' are debating Motion ' + str(int(motion_number_to_return_list[0]) + 1))

    def write_to_result_sheets(self, prop, opp, motion_number_to_return, prop_veto, opp_veto, i):
        ranking_result_sheet.update_cell(1, 1, 'PROPOSITION')
        ranking_result_sheet.update_cell(1, 2, 'OPPOSITION')
        ranking_result_sheet.update_cell(1, 3, 'MOTION')
        ranking_result_sheet.update_cell(1, 5, 'PROPOSITION VETO')
        ranking_result_sheet.update_cell(1, 6, 'OPPOSITION VETO')
        ranking_result_sheet.update_cell(i + 2, 1, prop)
        ranking_result_sheet.update_cell(i + 2, 2, opp)
        ranking_result_sheet.update_cell(i + 2, 3, motion_number_to_return)
        ranking_result_sheet.update_cell(i + 2, 5, prop_veto)
        ranking_result_sheet.update_cell(i + 2, 6, opp_veto)

    def loop(self):
        previous_form = motion_ranking_sheet.get_all_values()
        while len(self.result_list) != len(self.matchup):
            if previous_form != motion_ranking_sheet.get_all_values():
                motion_ranking = MotionRanking({'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'})
                previous_form = motion_ranking_sheet.get_all_values()
                self.result_list = motion_ranking.result_list

motion_ranking = MotionRanking({'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'})

# email, timer