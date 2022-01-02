from sportsipy.ncaab.schedule import Schedule
from datetime import datetime
from sportsipy.ncaab.boxscore import Boxscores
import pickle
import pandas as pd
import numpy as np

filename = './svr_model.sav'
svr_model = pickle.load(open(filename, 'rb'))

games_today = Boxscores(datetime.today())
today = pd.DataFrame()
for game in games_today.games[datetime.today().strftime('%-m-%-d-%Y')]:
    matchup = {'home': game['home_abbr'].upper(), 'away': game['away_abbr'].upper()}
    today = today.append(matchup, ignore_index=True)


def mdy_to_date(d):
    return datetime.strptime(d, '%b %d, %Y').strftime('%-m-%-d-%Y')


def gameScoring(schedule, team, opponent, league_similarity):
    games = pd.DataFrame()
    for game in schedule:
        try:
            if(game.dataframe_extended is None):
                continue
            else:
                games = games.append(game.dataframe_extended)
        except: 
            print("no game data")
            continue
    if games.empty:
        print("games are empty")
        return pd.DataFrame()
    try:
        games['opponent'] = [x for x in list(games['losing_abbr'].to_numpy()) + list(games['winning_abbr'].to_numpy()) if x != team]
    except:
        print("error with abbrs")
        return pd.DataFrame()
    games = games.set_index('opponent', drop=False)
    drop_columns = ['location', 'losing_name', 'winning_name', 'winner', 'losing_abbr', 'winning_abbr', 'opponent', 'date']
    games = games.drop(drop_columns, axis = 1)
    scaled_games = pd.DataFrame()
    for game in games.iterrows():
        if game[0] not in league_similarity.index: 
            continue
        scaled_games = scaled_games.append(pd.to_numeric(game[1]) * league_similarity[opponent][game[0]])
    average_stats = scaled_games.mean(axis=0)
    return average_stats


def getGameTime(schedule):
    for gn in [i for i, s in enumerate(list(schedule)) if 'maryland' in str(s)]:
        if mdy_to_date(schedule[gn].date[5:]) == datetime.today().strftime('%-m-%-d-%Y'):
            return(schedule[gn].time)
    return 'NA'


def predictToday(league_similarity):
  test_set = pd.DataFrame()
  for matchup in today.iterrows():
    team = matchup[1][0]
    try:
        schedule = Schedule(team, year=2022)
    except:
        print("can't get schedule")
        continue
    opponent = matchup[1][1]
    if opponent not in league_similarity.index: 
        print("no similarity for opponent")
        continue
    temp = gameScoring(schedule, team, opponent, league_similarity)
    try:
        schedule = Schedule(opponent, year=2022)
    except:
        print("can't get schedule")
        continue
    temp2 = gameScoring(schedule, opponent, team, league_similarity)
    if (temp.empty or temp2.empty):
        print("empty")
        continue
    temp = temp.to_frame().T.join(temp2.to_frame().T, rsuffix="_opp")
    temp['team'] = team
    temp['opponent'] = opponent
    temp['time'] = getGameTime(schedule)
    test_set = test_set.append(temp)
  test_set.replace([np.inf, -np.inf], np.nan, inplace=True)
  test_set.fillna(0, inplace=True)
  predictions = pd.DataFrame()
  for i in range(0, len(test_set)):
    yhat = svr_model.predict([test_set.iloc[i,:158]])
    matchup = {'home': test_set.iloc[i,158], 'home_score': yhat[0][0], 'away': test_set.iloc[i,159], 'away_score': yhat[0][1],}
    predictions = predictions.append(matchup, ignore_index=True)
  betting_predictions = pd.DataFrame()
  i = 0
  for name in predictions[['home_score', 'away_score']].idxmax(axis=1):
    #print(f"{predictions.loc[i, 'home']} vs. {predictions.loc[i, 'away']} {predictions.loc[i, name[0:4]]} -{round((predictions.loc[i, ['home_score', 'away_score']].max() - predictions.loc[i, ['home_score', 'away_score']].min())*2)/2}")
    betline = {'home': predictions.loc[i, 'home'], 'away': predictions.loc[i, 'away'], 'prediction': f"{predictions.loc[i, 'home']} -{round((predictions.loc[i, ['home_score', 'away_score']].max() - predictions.loc[i, ['home_score', 'away_score']].min())*2)/2}" }
    betting_predictions = betting_predictions.append(betline, ignore_index=True)
    i += 1
  return betting_predictions  
  