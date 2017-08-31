from util import *
from forecast import *

# Read historical games from CSV
games = Util.read_games("data/nfl_games.csv")

# Forecast every game
Forecast.forecast(games)

# Evaluate our forecasts against Elo
Util.evaluate_forecasts(games)
