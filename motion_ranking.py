import random
from time import sleep
import time
from preprocessing import *

class MotionRanking:

    def __init__(self, team_to_id):
        self.team_to_id = team_to_id
        self.matchup = {}
        self.team_to_ranking = {}
        self.unmatching_id_list = []
        self.result_list = []
        self.get_matchups()
        self.get_motion_ranking()
        self.return_motion_to_debate()

    def get_matchups(self):
        col_1 = matchup_sheet.col_values(1)
        del col_1[0:1]
        col_2 = matchup_sheet.col_values(2)
        del col_2[0:1]
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
            for j in range(3):
                if prop_team_ranking[j] == '3' or opp_team_ranking[j] == '3':
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

            self.result_list.append(str(prop_team_list[i]) + ' and ' + str(opp_team_list[i]) + ' are debating Motion ' + str(int(motion_number_to_return_list[0]) + 1))

    def loop(self):
        previous_form = motion_ranking_sheet.get_all_values()
        while len(self.result_list) != len(self.matchup):
            if previous_form != motion_ranking_sheet.get_all_values():
                motion_ranking = MotionRanking({'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'})
                previous_form = motion_ranking_sheet.get_all_values()
                self.result_list = motion_ranking.result_list

motion_ranking = MotionRanking({'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'})