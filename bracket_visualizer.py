from get_google_sheets import *
import math
import sys
import copy
import os

outrounds_sheet = sheet.worksheet_by_title('Outrounds')
# list of teams in the order of their seed (deleting the column header)
team_and_seed_list = outrounds_sheet.get_col(1, include_tailing_empty=False)
number_of_teams = len(team_and_seed_list)
# log base 2 + 1
number_of_rounds = int(math.log(number_of_teams, 2)) + 1
# this is the order of seeding that appears on the bracket visualizer
seed_label_list_16 = ['1', '16', '8', '9', '4', '13', '5', '12', '2', '15', '7', '10', '3', '14', '6', '11']
seed_label_list_8 = ['1', '8', '4', '5', '3', '6', '2', '7']
# number of dashes for the connecting lines
if number_of_teams == 16:
    number_of_dashes = 22
elif number_of_teams == 8:
    number_of_dashes = 25

class Bracket:

    def __init__(self):
        self.populate_team_in_seed_label_order_list()
        self.populate_column()

    # populate list with teams in order of the seed_label_list
    def populate_team_in_seed_label_order_list(self):
        self.team_in_seed_label_order_list = ['x'] * number_of_teams
        if number_of_teams == 16:
            for i in range(number_of_teams):
                self.team_in_seed_label_order_list[seed_label_list_16.index(str(i + 1))] = team_and_seed_list[i]
        elif number_of_teams == 8:
            for i in range(number_of_teams):
                self.team_in_seed_label_order_list[seed_label_list_8.index(str(i + 1))] = team_and_seed_list[i]

    # populate all the information to write to the REPL
    def populate_column(self):
        self.column = []
        # populate each column with the correct number of dash lines
        for i in range(0, number_of_rounds):
            self.column.append([])
            # second column would have 2^3 or 8 dash lines
            for j in range(2 ** (number_of_rounds - i - 1)):
                self.column[i].append('-' * number_of_dashes)
        # first column is the teams
        self.column[0] = self.team_in_seed_label_order_list

    def show(self):
        # make a copy so the recursive call doesn't alter the original lists
        self.columns_copy = copy.deepcopy(self.column)
        if number_of_teams == 16:
            self.seed_label_list_copy = seed_label_list_16.copy()
        elif number_of_teams == 8:
            self.seed_label_list_copy = seed_label_list_8.copy()

        # use sys.stdout to do it on the same line
        sys.stdout.write('Seed ')
        for i in range(1, number_of_rounds + 1):
            sys.stdout.write(('Round ' + str(i)).rjust(number_of_dashes + 3))
        print('\n')
        self.recurse(number_of_rounds - 1, 0)

    # tree of recursive calls
    def recurse(self, round_number, tail):
        # first column
        if round_number == 0:
            if tail == -1:
                print(str(self.seed_label_list_copy.pop(0)).rjust(4) + self.columns_copy[0].pop(0).rjust(number_of_dashes + 3) + ' \\')
            elif tail == 1:
                print(str(self.seed_label_list_copy.pop(0)).rjust(4) + self.columns_copy[0].pop(0).rjust(number_of_dashes + 3) + ' /')
        else:
            self.recurse(round_number - 1, -1)
            # writes for \
            if tail == -1:
                print(''.rjust(4) + ''.rjust((number_of_dashes + 3) * round_number) + self.columns_copy[round_number].pop(0).rjust(number_of_dashes + 3) + ' \\')
            # writes for /
            elif tail == 1:
                print(''.rjust(4) + ''.rjust((number_of_dashes + 3) * round_number) + self.columns_copy[round_number].pop(0).rjust(number_of_dashes + 3) + ' /')
            else:
                print(''.rjust(4) + ''.rjust((number_of_dashes + 3) * round_number) + self.columns_copy[round_number].pop(0).rjust(number_of_dashes + 3))
            self.recurse(round_number - 1, 1)

    def update(self, round, team_inputted):
        # store the first team that matches the input
        team_to_return = next((team for team in self.column[round - 2] if team_inputted.lower() in team.lower()), None)
        try:
            # index of the team_to_return in self.column[round - 2]
            index = self.column[round - 2].index(team_to_return)
            # set the next column to the team that won
            self.column[round - 1][int(index/2)] = self.column[round - 2][index]
        except:
            print('Your input does not match any of the teams. Try again.')
            return False
        if '-' * number_of_dashes in self.column[round - 1]:
            return False
        return True

def main():
    # clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    bracket = Bracket()
    bracket.show()
    for i in range(2, number_of_rounds + 1):
        updated = False
        while not updated:
            print('\n')
            sys.stdout.write('Update round '+str(i)+': ')
            x = input()
            # if the input is quit, quit
            if x == 'quit':
                return
            updated = bracket.update(i, x)
            os.system('cls' if os.name == 'nt' else 'clear')
            bracket.show()
    print('\n' + str(bracket.column[-1][0]) + ' won!' + '\n')

if __name__ == '__main__':
    main()