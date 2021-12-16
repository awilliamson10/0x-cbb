from datetime import *
from sportsipy.ncaab.teams import Teams
import pandas as pd
import numpy as np


def convert_height(height):
    height = str(height)
    height = height.split('-')
    if len(height) >= 2:
        return (int(height[0])*12)+int(height[1])
    else: return 0

def get_bench_limit(players):
    games_started = []
    for player in players:
        try:
            games_started.append(player.games_started)
        except:
            games_started.append(0)
    games_started.sort(reverse=True)
    return games_started[5]

def get_team_profiles(team):
    team_stats = pd.DataFrame(team.dataframe)
    df = pd.DataFrame()
    bench = pd.DataFrame()
    bench_thresh = get_bench_limit(team.roster.players)
    for player in team.roster.players:
        try:
            game_starts = player.games_started
        except:
            game_starts = 0
        player_stats = player.dataframe
        if player_stats.empty:
            df.append(pd.Series(0, index=df.columns), ignore_index=True)
            continue
        if game_starts <= bench_thresh:
            bench = bench.append(player_stats.loc['Career', :])
        else:
            df = df.append(player_stats.loc['Career', :])
    df = df.fillna(0)
    bench = bench.fillna(0)
    df['height'] = [convert_height(x) for x in df['height']]
    bench['height'] = [convert_height(x) for x in bench['height']]
    bench_combined = (bench.drop(['conference', 'position', 'team_abbreviation', 'player_id'], axis = 1).apply(lambda x: x.mean())).to_frame().T
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


def getStats(_year):
    teams = Teams(year = _year)
    all_teams_df = pd.DataFrame()
    for team in teams:
        all_teams_df = all_teams_df.append(get_team_profiles(team).transpose())
    all_teams_df = all_teams_df.reset_index(drop=True)
    remove_features = [
        'bench_player_id', 'bench_position', 'name', 'net_rating',
        'starter_1_conference', 'starter_1_player_id', 'starter_1_team_abbreviation',
        'starter_2_conference', 'starter_2_player_id', 'starter_2_team_abbreviation',
        'starter_3_conference', 'starter_3_player_id', 'starter_3_team_abbreviation',
        'starter_4_conference', 'starter_4_player_id', 'starter_4_team_abbreviation',
        'starter_5_conference', 'starter_5_player_id', 'starter_5_team_abbreviation',
    ]
    all_teams_df = all_teams_df.drop(remove_features, axis=1)
    remove_starters = ['starter_1_position', 'starter_2_position',
            'starter_3_position', 'starter_4_position',
            'starter_5_position']
    starter_cols = all_teams_df.filter(regex=("starter.*"))
    starter_cols = starter_cols.drop(remove_starters, axis = 1)
    starter_cols = starter_cols.fillna(0).astype('float')
    bench_cols = all_teams_df.filter(regex=("bench.*"))
    bench_cols = bench_cols.fillna(0).astype('float')
    all_teams_df['starter_1_position'] = all_teams_df['starter_1_position'].astype(str)
    all_teams_df['starter_2_position'] = all_teams_df['starter_2_position'].astype(str)
    all_teams_df['starter_3_position'] = all_teams_df['starter_3_position'].astype(str)
    all_teams_df['starter_4_position'] = all_teams_df['starter_4_position'].astype(str)
    all_teams_df['starter_5_position'] = all_teams_df['starter_5_position'].astype(str)
    all_teams_df = all_teams_df.drop(list(starter_cols.columns.append(bench_cols.columns)), axis = 1)
    all_teams_df = all_teams_df.join(starter_cols)
    all_teams_df = all_teams_df.join(bench_cols)
    return all_teams_df
