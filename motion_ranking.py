from get_google_sheets import *
import random
import sys
import time
from datetime import datetime, timedelta

matchup_sheet = sheet.worksheet_by_title('Matchup')
motion_ranking_sheet = sheet.worksheet_by_title('Motion Ranking')
motion_ranking_result_sheet = sheet.worksheet_by_title('Motion Ranking Result')

# master list of proposition teams (deleting the column header)
master_proposition_team_list = matchup_sheet.get_col(1, include_tailing_empty=False)[1:]
# master list of opposition teams (deleting the column header)
master_opposition_team_list = matchup_sheet.get_col(2, include_tailing_empty=False)[1:]

class MotionRanking:

    def __init__(self, team_to_id):
        self.team_to_id = team_to_id
        # list of team(s) that is/are in (an) invalid matchup(s)
        self.invalid_matchup_team_list = []
        self.matchup = {}
        # list of teams that have unmatching ids inputted (login/user verification)
        self.unmatching_id_team_list = []
        self.team_to_motion_ranking = {}
        self.motion_ranking_result_list = []

        self.check_if_matchup_is_valid()
        if len(self.invalid_matchup_team_list) > 0:
            print('There is/are invalid team(s) in the matchup: ' + str(self.invalid_matchup_team_list))
            sys.exit()

        self.populate_matchup_dictionary()
        self.populate_team_to_motion_ranking_dictionary()
        self.return_motion_to_debate()

    # check if the matchup is valid by checking if any team is repeated in any part in the bracket
    def check_if_matchup_is_valid(self):
        matchup_list = master_proposition_team_list + master_opposition_team_list
        for team in matchup_list:
            if matchup_list.count(team) > 1:
                if team not in self.invalid_matchup_team_list:
                    self.invalid_matchup_team_list.append(team)

    def populate_matchup_dictionary(self):
        for i in range(len(master_proposition_team_list)):
            if master_proposition_team_list[i] not in self.matchup:
                self.matchup[master_proposition_team_list[i]] = master_opposition_team_list[i]

    def populate_team_to_motion_ranking_dictionary(self):
        team_list = motion_ranking_sheet.get_col(2, include_tailing_empty=False)[1:]
        team_id_list = motion_ranking_sheet.get_col(3, include_tailing_empty=False)[1:]
        motion_1_ranking = motion_ranking_sheet.get_col(4, include_tailing_empty=False)[1:]
        motion_2_ranking = motion_ranking_sheet.get_col(5, include_tailing_empty=False)[1:]
        motion_3_ranking = motion_ranking_sheet.get_col(6, include_tailing_empty=False)[1:]
        matching_id_index_list = []

        # check if the id matches the team (login/user verification)
        for i in range(len(team_list)):
            if self.team_to_id[team_list[i]] != team_id_list[i]:
                self.unmatching_id_team_list.append(team_list[i])
            else:
                matching_id_index_list.append(i)

        # for all the teams with matching ids, we map from the team to their motion rankings
        for i in matching_id_index_list:
            if team_list[i] not in self.team_to_motion_ranking:
                self.team_to_motion_ranking[team_list[i]] = []
            self.team_to_motion_ranking[team_list[i]].append(motion_1_ranking[i])
            self.team_to_motion_ranking[team_list[i]].append(motion_2_ranking[i])
            self.team_to_motion_ranking[team_list[i]].append(motion_3_ranking[i])

    def return_motion_to_debate(self):
        proposition_team_list = []
        opposition_team_list = []
        proposition_team_ranking = {}
        opposition_team_ranking = {}

        for proposition, opposition in self.matchup.items():
            # if at least one of the teams in a matchup has an unmatching id, we don't return the motion they debate
            if len(self.unmatching_id_team_list) > 0:
                for unmatching_team in self.unmatching_id_team_list:
                    # if proposition or opposition are in self.unmatching_id_team_list
                    if proposition == unmatching_team.strip(''):
                        break
                    elif opposition == unmatching_team.strip(''):
                        break
                    # if the team hasn't submitted its motion ranking
                    elif proposition not in self.team_to_motion_ranking:
                        print('Team ' + str(proposition) + ' has not submitted its motion ranking.')
                        continue
                    elif opposition not in self.team_to_motion_ranking:
                        print('Team ' + str(opposition) + ' has not submitted its motion ranking.')
                        continue
                    else:
                        proposition_team_list.append(proposition)
                        opposition_team_list.append(opposition)
                print('Team(s) ' + str(self.unmatching_id_team_list) + ' has/have unmatching id(s).')
            # if the team hasn't submitted its motion ranking
            elif proposition not in self.team_to_motion_ranking:
                print('Team ' + str(proposition) + ' has not submitted its motion ranking.')
                continue
            elif opposition not in self.team_to_motion_ranking:
                print('Team ' + str(opposition) + ' has not submitted its motion ranking.')
                continue
            else:
                proposition_team_list.append(proposition)
                opposition_team_list.append(opposition)

        motion_number_to_write_list = ['MOTION']
        proposition_veto_list = ['PROPOSITION VETO']
        opposition_veto_list = ['OPPOSITION VETO']

        for i in range(len(proposition_team_list)):

            proposition_team_ranking = self.team_to_motion_ranking[proposition_team_list[i]]
            opposition_team_ranking = self.team_to_motion_ranking[opposition_team_list[i]]
            motion_number_to_return_list = []
            proposition_veto = ''
            opposition_veto = ''

            for j in range(3):
                # proposition veto
                if proposition_team_ranking[j] == '3':
                    proposition_veto = j + 1
                # opposition veto
                if opposition_team_ranking[j] == '3':
                    opposition_veto = j + 1
                # if both proposition and opposition rank a motion 1, return that motion
                elif proposition_team_ranking[j] == '1' and proposition_team_ranking[j] == opposition_team_ranking[j]:
                    motion_number_to_return_list.append(j + 1)
                    break
                # if there is a 1/2 split between two motions, add both motions
                elif proposition_team_ranking[j] != '3' and opposition_team_ranking[j] != '3':
                    motion_number_to_return_list.append(j + 1)

            # if there is a 1/2 split between two motions, choose randomly between them
            if len(motion_number_to_return_list) > 1:
                randomlist = [0, 1]
                motion_number_to_return_list = [motion_number_to_return_list[random.choice(randomlist)]]

            motion_number_to_write_list.append(motion_number_to_return_list[0])
            proposition_veto_list.append(proposition_veto)
            opposition_veto_list.append(opposition_veto)

            self.motion_ranking_result_list.append(str(proposition_team_list[i]) + ' and ' + str(opposition_team_list[i]) + ' are debating Motion ' + str(int(motion_number_to_return_list[0])))

            self.write_time_to_sheet(i+2)

        self.write_other_information_to_sheet(motion_number_to_write_list, proposition_veto_list, opposition_veto_list)
        # bold the row headers
        DataRange('A1','G1', worksheet=motion_ranking_result_sheet).apply_format(bold)

    def write_time_to_sheet(self, i):
        motion_ranking_result_sheet.update_value(str(chr(ord('@')+4)) + str(1), 'TIME STARTED')
        motion_ranking_result_sheet.update_value(str(chr(ord('@')+5)) + str(1), 'TIME LEFT')

        time = datetime.now() + timedelta(minutes=15)
        if motion_ranking_result_sheet.cell((i, 4)).value == '':
            motion_ranking_result_sheet.update_value(str(chr(ord('@')+4)) + str(i), str(time))
            motion_ranking_result_sheet.update_value(str(chr(ord('@')+5)) + str(i), '= IF(D' + str(i) + '-NOW() > 0, MINUTE(D' + str(i) + '-NOW()), 0)')

    def write_other_information_to_sheet(self, motion_number_to_write_list, proposition_veto_list, opposition_veto_list):
        if master_proposition_team_list[0] != 'PROPOSITION' and master_opposition_team_list[0] != 'OPPOSITION':
            master_proposition_team_list.insert(0, 'PROPOSITION')
            motion_ranking_result_sheet.update_col(1, master_proposition_team_list)
            master_opposition_team_list.insert(0, 'OPPOSITION')
            motion_ranking_result_sheet.update_col(2, master_opposition_team_list)

        motion_ranking_result_sheet.update_col(1, master_proposition_team_list)
        motion_ranking_result_sheet.update_col(2, master_opposition_team_list)
        motion_ranking_result_sheet.update_col(3, motion_number_to_write_list)
        motion_ranking_result_sheet.update_col(6, proposition_veto_list)
        motion_ranking_result_sheet.update_col(7, opposition_veto_list)

    def loop(self):
        previous_sheet = motion_ranking_sheet.get_all_values()
        while True:
            # if the motion_ranking_sheet changes, recalculate
            if previous_sheet != motion_ranking_sheet.get_all_values():
                motion_ranking = MotionRanking({'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'})
                previous_sheet = motion_ranking_sheet.get_all_values()
                self.motion_ranking_result_list = motion_ranking.motion_ranking_result_list
            # if the number of results is equal to the number of matchups, we have the correct number of results, so we end the loop
            if len(self.motion_ranking_result_list) == len(self.matchup):
                break
            # sleep for 10 seconds
            time.sleep(10)

motion_ranking_result_sheet.clear('A1')
motion_ranking = MotionRanking({'a': '2689101135', 'b': '2379289842', 'c': '2566987667', 'd': '3797752721', 'e': '852797324', 'f': '1911318538'})
motion_ranking.loop()