import random
import sys
import time
from datetime import datetime, timedelta
from get_google_sheets import *

proposition_list = matchup_sheet.col_values(1)
del proposition_list[0:1]
opposition_list = matchup_sheet.col_values(2)
del opposition_list[0:1]

class MotionRanking:

    def __init__(self, team_to_id):
        self.team_to_id = team_to_id
        self.invalid_matchup_team_list = []
        self.matchup = {}
        self.unmatching_id_list = []
        self.team_to_motion_ranking = {}
        self.result_list = []

        self.check_if_matchup_is_valid()
        if len(self.invalid_matchup_team_list) > 0:
            print('There is/are invalid team(s) in the matchup: ' + str(self.invalid_matchup_team_list))
            sys.exit()

        self.populate_matchup_dictionary()
        self.get_motion_ranking()
        self.return_motion_to_debate()

    # check if the matchup is valid
    def check_if_matchup_is_valid(self):
        matchup_list = proposition_list + opposition_list
        for team in matchup_list:
            if matchup_list.count(team) > 1:
                if team not in self.invalid_matchup_team_list:
                    self.invalid_matchup_team_list.append(team)

    def populate_matchup_dictionary(self):
        for i in range(len(proposition_list)):
            if proposition_list[i] not in self.matchup:
                self.matchup[proposition_list[i]] = opposition_list[i]

    def get_motion_ranking(self):
        team_list = motion_ranking_sheet.col_values(2)
        del team_list[0:1]
        team_id_list = motion_ranking_sheet.col_values(3)
        del team_id_list[0:1]
        motion_1_ranking = motion_ranking_sheet.col_values(4)
        del motion_1_ranking[0:1]
        motion_2_ranking = motion_ranking_sheet.col_values(5)
        del motion_2_ranking[0:1]
        motion_3_ranking = motion_ranking_sheet.col_values(6)
        del motion_3_ranking[0:1]
        matching_id_index_list = []

        # check if the id matches the team (login/user verification)
        for i in range(len(team_list)):
            if self.team_to_id[team_list[i]] != team_id_list[i]:
                self.unmatching_id_list.append(team_list[i])
            else:
                matching_id_index_list.append(i)

        for i in matching_id_index_list:
            if team_list[i] not in self.team_to_motion_ranking:
                self.team_to_motion_ranking[team_list[i]] = []
            self.team_to_motion_ranking[team_list[i]].append(motion_1_ranking[i])
            self.team_to_motion_ranking[team_list[i]].append(motion_2_ranking[i])
            self.team_to_motion_ranking[team_list[i]].append(motion_3_ranking[i])

    def return_motion_to_debate(self):
        prop_team_list = []
        opp_team_list = []
        prop_team_ranking = {}
        opp_team_ranking = {}

        for proposition, opposition in self.matchup.items():
            # if at least one of the teams in a matchup has an unmatching id, we don't return the motion they are debating
            if len(self.unmatching_id_list) != 0:
                for unmatching_id in self.unmatching_id_list:
                    if proposition == unmatching_id.strip(''):
                        break
                    elif opposition != unmatching_id.strip(''):
                        break
                    else:
                        prop_team_list.append(proposition)
                        opp_team_list.append(opposition)
            # if the team hasn't submitted its motion ranking
            elif proposition not in self.team_to_motion_ranking:
                continue
            elif opposition not in self.team_to_motion_ranking:
                continue
            else:
                prop_team_list.append(proposition)
                opp_team_list.append(opposition)

        for i in range(len(prop_team_list)):
            motion_number_to_return_list = []
            prop_team_ranking = self.team_to_motion_ranking[prop_team_list[i]]
            opp_team_ranking = self.team_to_motion_ranking[opp_team_list[i]]
            prop_veto = ''
            opp_veto = ''

            for j in range(3):
                # prop veto
                if prop_team_ranking[j] == '3':
                    prop_veto = j + 1
                # opp veto
                if opp_team_ranking[j] == '3':
                    opp_veto = j + 1
                # if both prop and opp rank a motion 1, return that motion
                elif prop_team_ranking[j] == '1' and prop_team_ranking[j] == opp_team_ranking[j]:
                    motion_number_to_return_list.append(j + 1)
                    break
                # if there is a 1/2 split between two motions, add both motions
                elif prop_team_ranking[j] != '3' and opp_team_ranking[j] != '3':
                    motion_number_to_return_list.append(j + 1)

            if len(motion_number_to_return_list) > 1:
                randomlist = [0, 1]
                newlist = []
                newlist.append(motion_number_to_return_list[random.choice(randomlist)])
                motion_number_to_return_list = newlist

            self.write_to_result_sheets(prop_team_list[i], opp_team_list[i], str(int(motion_number_to_return_list[0])), prop_veto, opp_veto, i + 2)

            self.result_list.append(str(prop_team_list[i]) + ' and ' + str(opp_team_list[i]) + ' are debating Motion ' + str(int(motion_number_to_return_list[0])))

    def write_to_result_sheets(self, prop, opp, motion_number_to_return, prop_veto, opp_veto, i):
        motion_ranking_result_sheet.update_cell(1, 1, 'PROPOSITION')
        motion_ranking_result_sheet.update_cell(1, 2, 'OPPOSITION')
        motion_ranking_result_sheet.update_cell(1, 3, 'MOTION')
        motion_ranking_result_sheet.update_cell(1, 4, 'TIME STARTED')
        motion_ranking_result_sheet.update_cell(1, 5, 'TIME LEFT (MINUTES)')
        motion_ranking_result_sheet.update_cell(1, 6, 'PROPOSITION VETO')
        motion_ranking_result_sheet.update_cell(1, 7, 'OPPOSITION VETO')

        motion_ranking_result_sheet.update_cell(i, 1, prop)
        motion_ranking_result_sheet.update_cell(i, 2, opp)
        motion_ranking_result_sheet.update_cell(i, 3, motion_number_to_return)
        motion_ranking_result_sheet.update_cell(i, 6, prop_veto)
        motion_ranking_result_sheet.update_cell(i, 7, opp_veto)

        motion_ranking_result_sheet.format('A1:G1', {'textFormat': {'bold': True}})

        time = datetime.now() + timedelta(minutes=15)
        if motion_ranking_result_sheet.cell(i, 4).value == None:
            motion_ranking_result_sheet.update_cell(i, 4, str(time))
            motion_ranking_result_sheet.update_cell(i, 5, '= IF(D' + str(i) + '-NOW() > 0, MINUTE(D' + str(i) + '-NOW()), 0)')

    def loop(self):
        previous_sheet = motion_ranking_sheet.get_all_values()
        while True:
            # if the motion_ranking_sheet changed, recalculate
            if previous_sheet != motion_ranking_sheet.get_all_values():
                motion_ranking = MotionRanking({'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'})
                previous_sheet = motion_ranking_sheet.get_all_values()
                self.result_list = motion_ranking.result_list
            # if the number of results is equal to the number of matchups, we have the correct number of results, so we end the loop
            if len(self.result_list) == len(self.matchup):
                break
            # API constraints
            time.sleep(100)

motion_ranking = MotionRanking({'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'})
motion_ranking.loop()