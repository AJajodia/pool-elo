import json
import pandas as pd


def get_matches():
    with open('matches.json', 'r') as f:
        matches = json.load(f)
    return matches


def add_match(date, winner, loser):
    with open('matches.json', 'r') as f:
        matches = json.load(f)
    
    if date in matches:
        matches[date].append({'winner': winner, 'loser':loser})
    else:
        matches[date] = [{'winner': winner, 'loser':loser}]
    
    with open("matches.json", "w") as f:
        json.dump(matches, f, indent=4)
    
def get_expected(target_elo, other_elo):
    return (1+(10**((other_elo-target_elo)/400)))**(-1)

def get_elo(winner_elo, loser_elo, k):
    expected_winner = get_expected(winner_elo, loser_elo)
    expected_loser = get_expected(loser_elo, winner_elo)
    
    new_winner = int(winner_elo + (k * (1 - expected_winner)))
    new_loser = int(loser_elo + (k * (0 - expected_loser)))
    
    return new_winner, new_loser
    
def show_elo(print=False):
    with open('matches.json', 'r') as f:
        matches = json.load(f)
        
    elo = {
        'Anu': 1200,
        'Milo': 1200,
        'Theo': 1200,
        'Nyk': 1200,
        'Franky': 1200,
        'Hayden': 1200,
        'Brendon': 1200,
        'Aayushka': 1200,
    }
    
    for date in matches:
        if print:
            print(date + '\n')
        for match in matches[date]:
            winner, loser = match['winner'], match['loser']
            
            winner_elo, loser_elo = elo[winner], elo[loser]
            
            new_winner_elo, new_loser_elo = get_elo(winner_elo, loser_elo, k = 100)
            
            if print:
                print('----------------------')
                print(winner + ":", new_winner_elo)
                print(loser + ":", new_loser_elo)
                print('----------------------\n')
            
            elo[winner], elo[loser] = new_winner_elo, new_loser_elo
            
    return elo

def print_leaderboard():
    elo = show_elo()
    
    sorted_keys = sorted(elo, key=elo.get, reverse=True)
    
    for i, name in enumerate(sorted_keys):
        print(str(i+1)+" -", name + ":", elo[name])
    
    return None

def write_leaderboard():
    elo = show_elo()
    
    sorted_keys = sorted(elo, key=elo.get, reverse=True)
    
    
    with open('README.md', 'w') as f:
        f.write("# Pool Elo Leaderboard\n\n")
        f.write("## Current Elo Ratings\n\n")
        f.write("The following are the current Elo ratings for each player based on the matches played.\n\n")
        f.write("| Rank | Player   | Elo Rating |\n")
        f.write("|------|----------|------------|\n")
        for i, name in enumerate(sorted_keys):
            f.write("|" + str(i+1)+"|" + name + "|" + str(elo[name]) + "|" + "\n")
    
    return None

# def elo_to_df():
#     with open('matches.json', 'r') as f:
#         matches = json.load(f)
        
#     elo = {
#         'Anu': 1200,
#         'Milo': 1200,
#         'Theo': 1200,
#         'Nyk': 1200,
#         'Franky': 1200,
#         'Hayden': 1200,
#         'Brendon': 1200,
#     }
    
#     df = []
    
    
#     for date in matches:
#         for match in matches[date]:
#             winner, loser = match['winner'], match['loser']
            
#             winner_elo, loser_elo = elo[winner], elo[loser]
#             new_winner_elo, new_loser_elo = get_elo(winner_elo, loser_elo, k = 100)
            
#             elo[winner], elo[loser] = new_winner_elo, new_loser_elo
        
#         elo['date'] = date
        
#         print(elo)
        
#         df.append(elo)
        
#         print(df)
        
        
            
#     return pd.DataFrame.from_records(elo, index='date')
