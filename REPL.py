from get_google_sheets import *
import random
import os
term_size = os.get_terminal_size()

outrounds_sheet = sheet.worksheet_by_title('Outrounds')
# list of teams in the order of their seed (deleting the column header)
team_and_seed_list = outrounds_sheet.get_col(1, include_tailing_empty=False)
# list of weights
weight_list = outrounds_sheet.get_col(2, include_tailing_empty=False)
team_to_weight = {}
weight_to_team = {}
matchup = {}

def check_if_seeding_valid():
    if len(team_and_seed_list) == 16 or len(team_and_seed_list) == 8:
        return True

def populate_team_to_weight_and_weight_to_team_dictionaries():
    for i in range(len(team_and_seed_list)):
        if team_and_seed_list[i] not in team_to_weight:
            team_to_weight[team_and_seed_list[i]] = int(weight_list[i])
    for team, weight in team_to_weight.items():
        if weight not in weight_to_team:
            weight_to_team[weight] = team

def get_and_populate_matchup():
    for i in range(int(len(team_and_seed_list)/2)):      
        # i + 1 because you want to start at 1      
        if i + 1 not in matchup:
            matchup[i + 1] = []
        # you add the team counting from the beginning and the end of the team_and_seed_list with the same index (for example: 1 and 16, 2 and 15, 3 and 14, etc.)
        list_to_add = [team_and_seed_list[i], team_and_seed_list[len(team_and_seed_list) - i - 1]]
        random.shuffle(list_to_add)
        matchup[i + 1] = matchup[i + 1] + list_to_add

def determine_winner_manual():
    for i in range(1, int(len(matchup)) + 1):
        print('\n' + 'For the matchup between seed ' + str(i) + ' and seed ' + str(len(matchup)*2 - int(i - 1)) + ', we have teams ' + str(matchup[i]) + '. Who won?')
        y = input('\n' + 'team> ')
        # if the input does not match any of the teams in the matchup
        while not any(y.lower() in team.lower() for team in matchup[i]):
            print('Your input does not match any of the teams. Try again.')
            y = input('\n' + 'team> ')
        # store the first team that matches the input
        team_to_return = next((team for team in matchup[i] if y.lower() in team.lower()), None)
        matchup[i] = team_to_return
        # if the length of the dictionary is 1 and the list of that key is greater than 1 (the list has not been altered yet)
        if len(matchup) == 1 and len(matchup[1]) > 1:
            print(str(team_to_return) + ' is the CHAMPION! \n')
        else:
            print(str(team_to_return) + ' has won the matchup.')

    # redo matchup
    if len(matchup) == 1:
        matchup[1] = [matchup[1]]
    for i in range(1, int(len(matchup)/2 + 1)):
        matchup[i] = [matchup[i], matchup[len(matchup) - i + 1]]

    half_of_matchup_number = int(len(matchup)/2)
    if half_of_matchup_number == 0:
        half_of_matchup_number = 1

    # if the key is greater than half of the matchups left, you pop the key
    for i in matchup.copy():
        if i > half_of_matchup_number:
            matchup.pop(i)

    if len(matchup) > 1:
        print('\n' + '=' * term_size.columns + '\n')
        print('Next round!')
        print('\n' + '=' * term_size.columns)
        determine_winner_manual()
    # need to call determine_winner_manual() one last time for the finals
    if len(matchup) == 1 and len(matchup[1]) > 1:
        print('\n' + '=' * term_size.columns + '\n')
        print('Next round!')
        print('\n' + '=' * term_size.columns)
        determine_winner_manual()

def determine_winner_auto():
    for i in range(1, len(matchup) + 1):
        team_list = matchup[i]
        # sorted based on weights so the higher seeded team is the first item in the list
        sorted_team_list = sorted(team_list, key=lambda x: team_to_weight[x], reverse=True)
        # weight_difference is guaranteed to be positive because of the sorting
        weight_difference = team_to_weight[sorted_team_list[0]] - team_to_weight[sorted_team_list[1]]
        probability = 0

        # assign win probabilities based on the weight_difference
        if weight_difference >= 50:
            probability = 99
        elif weight_difference >= 40:
            probability = 95
        elif weight_difference >= 30:
            probability = 90
        elif weight_difference >= 20:
            probability = 80
        elif weight_difference >= 10:
            probability = 70
        elif weight_difference >= 5:
            probability = 60
        elif weight_difference >= 0:
            probability = 50

        RNG = random.randint(1, 100)
        if RNG < probability:
            matchup[i] = sorted_team_list[0]
        else:
            matchup[i] = sorted_team_list[1]

    # redo matchup
    if len(matchup) == 1:
        matchup[1] = [matchup[1]]
    for i in range(1, int(len(matchup)/2 + 1)):
        matchup[i] = [matchup[i], matchup[len(matchup) - i + 1]]

    half_of_matchup_number = int(len(matchup)/2)
    if half_of_matchup_number == 0:
        half_of_matchup_number = 1

    # if the key is greater than half of the matchups left, you pop the key
    for i in matchup.copy():
        if i > half_of_matchup_number:
            matchup.pop(i)
    
    print(matchup)

    if len(matchup) > 1:
        determine_winner_auto()
    # need to call determine_winner_auto() one last time for the finals
    if len(matchup) == 1 and len(matchup[1]) > 1:
        determine_winner_auto()

def main():
    # clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n' + 'Use this to simulate a tournament. To manually input results, type manual. To autogenerate results, type auto.')
    x = input('\n' + 'command> ')

    if x == 'auto':
        print('\n' + '=' * term_size.columns + '\n')
        print(matchup)
        determine_winner_auto()
        print('\n' + '=' * term_size.columns + '\n')
        print(str(matchup[1][0]) + ' is the CHAMPION! \n')
    elif x == 'manual':
        determine_winner_manual()
    else:
        print('That command does not exist. Redoing...')
        main()

if __name__ == '__main__':
    if check_if_seeding_valid():
        populate_team_to_weight_and_weight_to_team_dictionaries()
        get_and_populate_matchup()
        main()
    else:
        print('The number of teams is not valid.')
