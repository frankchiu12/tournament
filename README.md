# motion-ranking
made by: Frank Chiu

This is, in effect, many projects combined together into one. Initially, it started off as a simple project to help debate tournaments allocate the motions to debate for the Asian Parliamentary format by allowing teams to submit their ranking and returning the motions they are debating based on comparing their rankings with that of their opponents. Gradually, it expanded to an entire suite to help organize and run tournaments, including the functionality of preprocessing random and unique team ids, automating emails, motion ranking, team ranking, a REPL for tournament brackets, a visualization tool for tournament brackets, etc.

Technologies this program uses include the Google Sheets API (pygsheets), MIME, smtplib,

The Google Sheets this program interacts with is: https://docs.google.com/spreadsheets/d/1Oc3Nhj1CgxcMAJXk08IJQ0E9S4YqE8Eqnb7wqY_UZQ0/edit?usp=sharing

To be specific, here is what each file does:
1. get_google_sheets.py is in charge of interacting with the Google Sheets API and reading from the Google Sheets. It also does some small formatting setup, for example, for bolding Google Sheets cells.
2. preprocessing.py is in charge of assigning each team a random and unique id. On the Google Sheets, it reads in the team list from "Team" (information sheet the tournament director should input). Then, after it generates the mapping from the teams to their id, it writes it into the "Team To ID." Note that you only need it run it once to generate the mapping, and that mapping would be important as a parameter to pass into other classes as a mini login function and user verification. The function convert_id_to_team allows you to check which team an id belongs to.
3. email_automator.py automates emails. For this program, it reads in the emails from "Team" and sends teams their random and unique ids generated by preprocessing. Therefore, the team_to_id variable needs to be updated to be correct after running preprocessing.py. Of course, this is extensible and could be used to send any other emails in an efficient, error-free way.
4. motion_ranking.py is in charge of assigning team matchups to the motions they are debating by comparing the rankings by the teams that are against each other. The class takes in the team to id mapping from preprocessing.py. It reads in the matchup from "Matchup" that the tournament director needs to update before each round. From "Motion Ranking," it then reads in the team, team id, and their rankings for each motion. Note that this sheet comes from a Google Form (https://docs.google.com/forms/d/e/1FAIpQLSdeVHTyKLob-mo_EaKs8XsPKKC5b8aKCo5cLXEcwiySNnFrzQ/viewform). This program runs on loop, so it checks, with ten second intervals, whether the sheet has been updated (whether a new Google Form has been filled out) and uses that information accordingly. A rundown of what the program does: it first checks whether the matchups are valid as a safeguard. Then, it reads in information from "Motion Ranking" to retrieve teams and their rankings. There are two caveats here: (1) If a team fills in an id that doesn't make their team, this fails the login/user verification, so an error is thrown (2) If any one of the teams in a matchup did not submit their rankings yet, the program raises a warning and skips over the pair. For all the valid pairings, their rankings are compared against each other and the motion to debate is calculated. The algorithm is simple. Each team gives a ranking of 1 to 3 for 3 motions, with 1 being most preferred and 3 being the veto. All motions with 3 are scrapped immediately. From there, if both teams give 1 to a motion, that motion is debated. In the case of a tie (ranking of 1 and 2 for 2 separate motions), a random one is selected. After calculating the result, the program writes it into "Motion Ranking Results." It writes in the proposition and opposition team, the motion, a countdown timer of 15 minutes until the round starts, and which motion each respective team vetoed (gave a ranking of 3 to). These statistics are all essential for running a debate tournament. Again, this program runs on loop until all the valid matchups have a motion assigned and written into "Motion Ranking Results."
5. team_ranking.py is the full package to run a debate tournament and assign rankings, but it is extensible to run other things as well. On the Google Sheets, there are results to be manually inputted for each team and each matchup by judges, including their score and who they won/lost against. If you want to add more rounds, just add a new Google Sheet with "Round #" and change the second number of the parameter for TeamRanking to the total number of rounds. For example, if you have 6 rounds, you would put "TeamRanking(1, 6)." After each of these results are inputted, the program reads in the results and writes the final rankings into new Google Sheets. If the results and ballots aren't all in, the program throws a warning. After it reads in all the results, it processes a team's performance collectively across all rounds and ranks them primarily on wins and secondarily on their score. It then writes the results into "Team Ranking" with information including their ranking, team name, score for each round, number of wins, and their average score. In addition, it also does ranking based on team status, for example, ESL and Novice. On "Team," if a team has a special status, it must be indicated. The program would read in this information and create sub-rankings for each category and create new Google Sheets to write into. For example, "ESL Team Ranking" and "Novice Team Ranking" are new Google Sheets created by the program to rank subcategories. There is also a get_results() function where you could pass in the team name as a parameter and get the wins and losses they have.
6. REPL.py is an interactive REPL to input the results of teams for outrounds in debate, but it could be applied to any other tournament with an elimination style, including professional sports like the NBA, NFL, etc.

# TODO: finish