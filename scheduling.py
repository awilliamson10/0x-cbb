import get_team_stats
import score_similarity
import prediction
import pymongo

client = pymongo.MongoClient("mongodb+srv://awill:jsxf3KLsr97F3xM@main-cluster.zwji6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

def save_data_to_mongo(data):
    db = client["cbb"]
    collection = db["games_today"]
    collection.delete_many({})
    data_dict = data.to_dict("records")
    response = collection.insert_many(data_dict)

if __name__ == "__main__":
  all_teams = get_team_stats.getStats(2022)
  league = score_similarity.score_similarity(2022, all_teams)
  todays_lines = prediction.predictToday(league)
  print(todays_lines)
  save_data_to_mongo(todays_lines)