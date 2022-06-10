# motion-ranking
made by: Frank Chiu

This is, in effect, many projects combined together into one. Initially, it started off as a simple project to help debate tournaments allocate the motions to debate for the Asian Parliamentary format by allowing teams to submit their rankings and returning the motions they are debating based on comparing their rankings with that of their opponents. Gradually, it expanded to an entire suite to help organize and run tournaments, including the functionality of preprocessing random and unique team ids, automating emails, motion ranking, team ranking, a REPL for tournament brackets, a visualization tool for tournament brackets, etc.

Technologies this program uses include the Google Sheets API (pygsheets), MIME, and smtplib.

The Google Sheets this program interacts with is: https://docs.google.com/spreadsheets/d/1Oc3Nhj1CgxcMAJXk08IJQ0E9S4YqE8Eqnb7wqY_UZQ0/edit?usp=sharing

To be specific, here is what each file does:

1. get_google_sheets.py is in charge of interacting with the Google Sheets API and reading from the Google Sheets. It also does some small formatting setup, for example, for bolding Google Sheets cells.

2. preprocessing.py is in charge of assigning each team a random and unique id. On the Google Sheets, it reads in the team list from "Team" (information sheet the tournament director should input information on). Then, after it generates the mapping from the teams to their id, it writes that mapping into "Team To ID." Note that you only need to run the class once to generate the mapping, and that mapping would be important as a parameter to pass into other classes as a login function and user verification. The function convert_id_to_team() allows you to check which team an id belongs to.

3. email_automator.py automates emails. For this program, it reads in the emails from "Team" and sends teams their random and unique ids generated by preprocessing.py. Therefore, the team_to_id variable needs to be updated correctly after running preprocessing.py. Of course, this is extensible and could be used to send any other emails in an efficient, error-free way.

4. motion_ranking.py is in charge of assigning team matchups the motions they are debating by comparing the rankings by the teams that are against each other in the matchup. The class takes in the team to id mapping from preprocessing.py. It reads in the matchup from "Matchup" that the tournament director needs to update before each round. From "Motion Ranking," it then reads in the team, team id, and their rankings for each motion. Note that this sheet comes from a Google Form (https://docs.google.com/forms/d/e/1FAIpQLSdeVHTyKLob-mo_EaKs8XsPKKC5b8aKCo5cLXEcwiySNnFrzQ/viewform) that debaters respond to input their rankings. This program runs on loop, so it checks, with ten second intervals, whether the sheet has been updated (whether a new Google Form has been filled out) and uses that information accordingly. A rundown of what the program does: it first checks whether the matchups are valid as a safeguard. Then, it reads in information from "Motion Ranking" to retrieve teams and their rankings. There are two caveats here: (1) If a team fills in an id that doesn't match their team, this fails the login/user verification, so an error is thrown (2) If any one of the teams in a matchup did not submit their rankings yet, the program raises a warning and skips over that pairing. For all the valid pairings, their rankings are compared against each other and the motion to debate is calculated. The algorithm is simple: Each team gives a ranking of 1 to 3 for 3 motions, with 1 being the most preferred and 3 being the veto. All motions with 3s are scrapped immediately. From there, if both teams give 1 to a motion, that motion is debated. In the case of a tie (ranking of 1 and 2 for 2 separate motions), a random motion is selected. After calculating the results, the program writes it into "Motion Ranking Results." It writes in the proposition and opposition teams, the motions, countdown timers of 15 minutes until rounds start, and motions each team vetoed (gave a ranking of 3 to). These statistics are all essential for running a debate tournament. Again, this program runs on loop until all the valid matchups have motions assigned and written into "Motion Ranking Results." This public spreedsheet could now be viewed by all teams, judges, and all other relevant participants.

5. team_ranking.py is the full package to run a debate tournament and assign rankings, but it is extensible to run other tournaments as well. On the Google Sheets, there are results to be manually inputted for each round, team, and matchup by judges, including team scores and who they won/lost against. If you want to add more rounds, just add a new Google Sheet with the title "Round #" and change the second number of the parameter for TeamRanking to the total number of rounds. For example, if you have 6 rounds, you would put "TeamRanking(1, 6)." After these results are inputted for all the rounds, the program reads in the results and writes the final rankings into new Google Sheets. If the results and ballots aren't all in, the program throws a warning. After it reads in all the results, it processes a team's performance collectively across all rounds and ranks them primarily on wins and secondarily on their score. It then writes the results into "Team Ranking" with information including their ranking, team name, score for each round, number of wins, and their average score. In addition, it also does ranking based on team status, for example, ESL and Novice. On the Google Sheets "Team," if a team has a special status, it must be indicated. The program would read in this information and create sub-rankings for each category and create new Google Sheets to write into. For example, "ESL Team Ranking" and "Novice Team Ranking" are new Google Sheets created by the program to rank subcategories. There is also a get_results() function where you could pass in the team name as a parameter and get the wins and losses they have.

6. REPL.py is an interactive REPL to input the results of teams for outrounds in debate, but it could be applied to any other tournament with an elimination style, including professional sports like the NBA, NFL, etc. There is both a manual and automated component. Right now, the program works on outrounds with either 16 or 8 teams, and an error is thrown if the number of teams that are in the outrounds read in from the Google Sheets "Outrounds" is not the correct number of teams. In the future, this program could be expanded to take into account more team numbers. After that, the REPL would prompt the user for an input: "Use this to simulate a tournament. To manually input results, type manual. To autogenerate results, type auto." If the user types "manual," the program displays the matchup and seeding and the user is prompted to type in the team that won that matchup for each matchup and each round until we reach the champion. Note that the input is not case-sensitive, so the program finds the team that most closely approximates the input as the team that won. So if the team that won is "Golden State Warriors," inputs like "gold," "state," "warriors," "w," etc. all work. If the user types "auto," the program simulates the outrounds, with win probabilities being based on the team weights it reads in from "Outrounds," and returns the results for each matchup in each elimination round and finally the champion. At any point in the program if you type "quit" the REPL stops.

7. bracket_visualizer.py is a visualization tool for tournament brackets. Right now, it works on outrounds with either 16 or 8 teams, and an error is thrown if the number of teams that are in the outrounds read in from the Google Sheets "Outrounds" is not the correct number of teams. In the future, this program could be expanded to take into account more team numbers. Intuitively after you run the program you get a visualization of the bracket, and the terminal prompts you to update the round and matchups within with the team that won. Note that the input is not case-sensitive, so the program finds the team that most closely approximates the input as the team that won. So if the team that won is "Golden State Warriors," inputs like "gold," "state," "warriors," "w," etc. all work. To revise a previous input, just type in the correct team that won and the bracket would be visually updated. This process repeats until the entire bracket is complete and a winner is determined.

![bracket_visualizer_example]('https://github.com/frankchiu12/tournament/blob/main/bracket_visualizer_example.png')

Have fun running a tournament :)