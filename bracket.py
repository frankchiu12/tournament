from get_google_sheets import *
import math
import sys
import copy
import os

outrounds_sheet = sheet.worksheet_by_title('Outrounds')
team_and_seed_list = outrounds_sheet.get_col(1, include_tailing_empty=False)
number_of_teams = len(team_and_seed_list)
number_of_rounds = int(math.log(number_of_teams, 2)) + 1
seed_label_list_16 = ['1', '16', '8', '9', '4', '13', '5', '12', '2', '15', '7', '10', '3', '14', '6', '11']
number_of_dashes = 25

class Bracket:

    def __init__(self):
        self.team_in_seed_label_order_list = ['x'] * number_of_teams
        for i in range(number_of_teams):
            self.team_in_seed_label_order_list[seed_label_list_16.index(str(i + 1))] = team_and_seed_list[i]

        self.columns = []
        for i in range(0, number_of_rounds):
            self.columns.append([])
            for j in range(2 ** (number_of_rounds - i - 1)):
                self.columns[i].append('-' * number_of_dashes)
        self.columns[0] = self.team_in_seed_label_order_list

    def show(self):
        self.columns_copy = copy.deepcopy(self.columns)
        self.seed_label_list_copy = seed_label_list_16.copy()

        sys.stdout.write('Seed ')
        for i in range(1, number_of_rounds + 1):
            sys.stdout.write(('Round ' + str(i)).rjust(number_of_dashes + 3))
        print('\n')
        self.recurse(number_of_rounds - 1, 0)

    def recurse(self, round_number, tail):
        if round_number == 0:
            if tail == -1:
                print(str(self.seed_label_list_copy.pop(0)).rjust(4) + self.columns_copy[0].pop(0).rjust(number_of_dashes + 3) + ' \\')
            elif tail == 1:
                print(str(self.seed_label_list_copy.pop(0)).rjust(4) + self.columns_copy[0].pop(0).rjust(number_of_dashes + 3) + ' /')
        else:
            self.recurse(round_number - 1, -1)
            if tail == -1:
                print(''.rjust(4) + ''.rjust((number_of_dashes + 3) * round_number) + self.columns_copy[round_number].pop(0).rjust(number_of_dashes + 3) + " \\")
            elif tail == 1:
                print(''.rjust(4) + ''.rjust((number_of_dashes + 3) * round_number) + self.columns_copy[round_number].pop(0).rjust(number_of_dashes + 3) + ' /')
            else:
                print(''.rjust(4)+''.rjust((number_of_dashes + 3)*round_number)+self.columns_copy[round_number].pop(0).rjust(number_of_dashes + 3))
            self.recurse(round_number - 1, 1)

    def update(self,rounds,teams):
        lowercase = [team.lower() for team in self.columns[rounds - 2]]
        for team in teams:
            try:
                index = lowercase.index(team.lower())
                self.columns[rounds-1][int(index/2)] = self.columns[rounds-2][index]
            except:
                return False
        if "-"*number_of_dashes in self.columns[rounds-1]:
            return False
        return True

def main():
    bracket = Bracket()
    os.system('cls' if os.name == 'nt' else 'clear')
    bracket.show()
    for i in range(2,number_of_rounds+1):
        updated = False
        while not updated:
            print("")
            sys.stdout.write("Update round "+str(i)+": ")
            teams = input().replace(", ",",").split(",")
            if teams[0] in ["Q","q","Quit","quit"]:
                return
            updated = bracket.update(i, teams)
            os.system('cls' if os.name == 'nt' else 'clear')
            bracket.show()
    print("")
    print(bracket.columns[-1][0]+" won!")

if __name__ == '__main__':
    main()