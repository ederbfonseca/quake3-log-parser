'''
File name: quake3-log-parser.py
Author: Eder Fonseca
Created: Jul 7th, 2024
Version: 0.2
Description: 

The project should implement the following functionalities:

Read the log file
Group the game data of each match
Collect kill data

'''
# re module provides regular expression matching operations
import re
# defaultdict creates a dictionary with zeros, where the default value for any non-existing key is set to zero.
from collections import defaultdict

###
# In some games, suicide is not considered a kill because it is not seen as a brave act.
# Because of that, you can choose if you want to increment the suicides to the killer score.
#
# suicide_count = 1 : suicide will be incremented in the killer score
# suicide_count = 0 : suicide will be NOT incremented in the killer score
#
# defaul value: 1
#####
suicide_count = 1

def parse_log_file(file_path):
    # read the log file in file path
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # list of games
    games = []
    # dict of kills, killers, killed and means
    current_game = None

    for line in lines:
        #Every InitGame means a new game begin
        if "InitGame:" in line:
            # If is the first time (current_game == None), we don't need to save the current_game
            if current_game is not None:
                # add the current_game to the games list
                games.append(current_game)
            # create a game structure, with total_kills, players names, and kills numbers for each player
            current_game = {
                # Total kills in the game
                "total_kills": 0,
                # players is a set of players who played the game. This set is a collection of unique elements
                "players": set(),
                # dict with the tuple <player: # of kills>
                "kills": defaultdict(int),
                # dict with the tuple <means: # of kills>
                "kills_by_means": defaultdict(int)
            }
        # Each expression that contains "Kill:" means a kill and we need to extract the information
        elif "Kill:" in line and current_game is not None:
            # Increment the number of the kills in the current game
            current_game["total_kills"] += 1
            # match with the regular expression: "Kill: " + digit + digit + digit : <killer> "killed" <killed> "by" <means>
            match = re.search(r'Kill: \d+ \d+ \d+: (.+) killed (.+) by (.+)', line)
            if match:
                # get the tuple <killer, killed, means>
                killer, killed, means = match.groups()
                # Increment the number of kills means in the current game
                current_game["kills_by_means"][means] += 1
                # Required when <world> kill a player, that player loses -1 kill score
                if killer == '<world>':
                    current_game["kills"][killed] -= 1
                else:
                    # Add the killer to a set of players
                    current_game["players"].add(killer)
                    
                    # If suicide counts or it is not a suicide, increments the killer score,
                    # but if suicide does not count and killer is equal killed, not increment the score
                    if suicide_count != 0 or killer != killed:
                        # Increment the killer score
                        current_game["kills"][killer] += 1
                    
                    # Add the killed to a set of players
                    current_game["players"].add(killed)
    
    # if the file don't start with InitGame and after the last interation
    if current_game is not None:
        # add the current_game to the games list
        games.append(current_game)

    return games

def print_report(games):
    # for each game, print the structure
    for i, game in enumerate(games, 1):
        print(f"game_{i}:")
        print(f"  total_kills: {game['total_kills']}")
        print(f"  players: {list(game['players'])}")
        print(f"  kills: {dict(game['kills'])}")
        # Bonus: report of deaths grouped by death cause for each match.
        print(f"  kills_by_means: {dict(game['kills_by_means'])}")
        print()

def main():
    # log file must be in the same directory of this script
    file_path = 'qgames.log'
    games = parse_log_file(file_path)
    print_report(games)

if __name__ == "__main__":
    main()
