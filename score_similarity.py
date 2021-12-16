import re
from datetime import *
from sportsipy.ncaab.teams import Teams
import pandas as pd
import numpy as np
from collections import Counter
from math import sqrt, floor
from sklearn import preprocessing


remove_features = [
    'bench_conference', 'bench_player_id', 'bench_position', 'name', 'net_rating',
    'starter_1_conference', 'starter_1_player_id', 'starter_1_team_abbreviation',
    'starter_2_conference', 'starter_2_player_id', 'starter_2_team_abbreviation',
    'starter_3_conference', 'starter_3_player_id', 'starter_3_team_abbreviation',
    'starter_4_conference', 'starter_4_player_id', 'starter_4_team_abbreviation',
    'starter_5_conference', 'starter_5_player_id', 'starter_5_team_abbreviation',
]

string_features = [
    'abbreviation', 'conference', 'starter_1_position', 'starter_2_position',
    'starter_3_position', 'starter_4_position', 'starter_5_position', 
]


def get_bench_limit(players):
    games_started = []
    for player in players:
        games_started.append(player.games_started)
    games_started.sort(reverse=True)
    return games_started[5]


def convert_height(height):
    height = str(height)
    height = height.split('-')
    return (int(height[0])*12)+int(height[1])


def get_team_profiles(team):
    team_stats = pd.DataFrame(team.dataframe)
    df = pd.DataFrame()
    bench = pd.DataFrame()
    bench_thresh = get_bench_limit(team.roster.players)
    for player in team.roster.players:
        if player.games_started <= bench_thresh:
            bench = bench.append(player.dataframe.loc['Career', :])
        else:
            df = df.append(player.dataframe.loc['Career', :])
    df = df.fillna(0)
    bench = bench.fillna(0)
    df['height'] = [convert_height(x) for x in df['height']]
    bench['height'] = [convert_height(x) for x in bench['height']]
    bench_combined = (bench.drop(['conference', 'position', 'team_abbreviation', 'player_id'], axis = 1).apply(lambda x: x.mean())).to_frame().T
    bench_combined['conference'] = ''
    bench_combined['position'] = 'bench'
    bench_combined['team_abbreviation'] = team.abbreviation
    bench_combined['player_id'] = 'bench'
    team_stats = team_stats.join(bench_combined.set_index("team_abbreviation").add_prefix("bench_")).transpose()
    starters = pd.DataFrame(df)
    starters.index = np.arange(1, len(starters) + 1)
    for index, row in starters.iterrows():
        name = team.abbreviation
        row = row.add_prefix(f"starter_{index}_").rename(name, axis = 0)
        team_stats = team_stats.append(row.to_frame())
    return team_stats


def string_compare_teams(x, y):
    string_scores = []
    if x['abbreviation'] == y['abbreviation']:
        string_scores.append(1)
    else:
        string_scores.append(0)
    if x['conference'] == y['conference']:
        string_scores.append(1)
    else:
        string_scores.append(0)
    r = re.compile("^starter*")
    x_positions = x[(list(filter(r.match, x.index.tolist())))].to_string()
    y_positions = y[(list(filter(r.match, y.index.tolist())))].to_string()
    x_positions = sorted(x_positions)
    y_positions = sorted(y_positions)
    string_scores.append(len(list((Counter(x_positions) & Counter(y_positions)).elements()))/5)
    return string_scores


def manhattan(a, b):
    if a is None or b is None:
        return 0
    return 1-sum(abs(val1-val2) for val1, val2 in zip([a],[b]))


def numeric_compare_teams(x,y):
    numeric_features = []
    for feature in list(x.index):
        if feature not in string_features:
            numeric_features.append(manhattan(x[feature], y[feature]))
    return numeric_features


def team_similarity(team_one, teams, idx):
    similarity_scores = pd.Series(dtype=object)
    team_one_abbr = team_one['abbreviation']
    for index, team_two in teams.iterrows():
        print(f"{idx}.{index}/{len(teams)} teams scored", end='\r')
        team_two_abbr = team_two['abbreviation']
        if team_one_abbr == team_two_abbr: team_two_abbr = team_two_abbr+'.'
        team_match = team_one.to_frame(name=team_one_abbr).join(team_two.to_frame(name=team_two_abbr))
        x = team_match.loc[:,team_one_abbr].fillna(0)
        y = team_match.loc[:,team_two_abbr].fillna(0)
        team_two_abbr = team_two_abbr.replace('.', '')
        scores = pd.Series(string_compare_teams(x[string_features], y[string_features]) + numeric_compare_teams(x,y), name=team_two_abbr)
        similarity_scores = pd.concat([similarity_scores, scores], axis = 1)
    return similarity_scores


def score_similarity(_year, teams):
    league = pd.DataFrame()
    min_max_scaler = preprocessing.MinMaxScaler()
    print("Grabbing latest team data...", end='\r')
    teams_numeric = teams.loc[:,(column for column in teams.columns if column not in string_features)]
    teams_numeric = teams_numeric.fillna(0)
    min_max_scaler = preprocessing.MinMaxScaler()
    teams_numeric_scaled = min_max_scaler.fit_transform(teams_numeric)
    teams_numeric_scaled = pd.DataFrame(teams_numeric_scaled, columns = teams_numeric.columns)
    teams_engineered = teams.loc[:,string_features].join(teams_numeric_scaled)
    for idx, team in teams_engineered.iterrows():
        team_scores = team_similarity(team, teams_engineered, idx)
        team_scores = team_scores.drop(0, axis=1)
        allteam_scores = []
        for col in team_scores.iteritems():
            allteam_scores.append([col[1].name,sum(col[1])/len(col[1])])
        scores_df = pd.DataFrame(allteam_scores)
        scores_df = scores_df.set_index(0)
        scores_df_one = scores_df.rename({1: team['abbreviation']}, axis = 1)
        league = league.join(scores_df_one, how='right')
    print(f"All teams scored.....", end='\r')
    return league
