# Can You Beat FiveThirtyEight's NFL Predictions?

This repository contains code and data to accompany [FiveThirtyEight's NFL Forecasting game](https://projects.fivethirtyeight.com/2018-nfl-forecasting-game/). Specifically, it has:

* Historical NFL scores back to 1920 in `data/nfl_games.csv`, with FiveThirtyEight's Elo win probabilities for each game.
* Code to generate the Elo win probabilities contained in the data.
* Code to evaluate alternative forecasts against Elo using the historical data and the rules of our game.
* Game schedule and results from the [2018-19 season](https://projects.fivethirtyeight.com/nfl-api/2018/nfl_games_2018.csv).
* [Reader forecasts](https://projects.fivethirtyeight.com/nfl-api/2018/raw_user_forecasts.csv) from our 2018-19 forecasting game.
* [Reader forecasts](https://projects.fivethirtyeight.com/nfl-api/2017/raw_user_forecasts.csv) from our 2017-18 forecasting game.

Our goal in providing this repository is for people to be able to figure out how FiveThirtyEight's NFL Elo model and NFL forecasting game work and to provide a loose framework for evaluating forecasts against historical data. This repository does not include assistance in building a predictive model.

## Evaluating historical forecasts

`eval.py` is the only runnable script, and does the following:

1. Reads in the CSV of historical games. Each row includes a `elo_prob1` field, which is the probability that `team1` will win the game according to the Elo model.
2. Fills in a `my_prob1` field for every game using code in `forecast.py`. By default, these are filled in using the exact same Elo model.
3. Evaluates the probabilities stored in `my_prob1` against the ones in `elo_prob1`, and shows how those forecasts would have done in our game for every season since 1920.

Jump in by running `python eval.py`. You should see the following output:

```

On average, your forecasts would have gotten 645.16 points per season. Elo got 645.16 points per season.

```

This makes sense — right now it's just running FiveThirtyEight's Elo model against itself, so it gets the same number of points for every game.

Open up `forecast.py`, change the `HFA` (home-field advantage) parameter to 100, and rerun `python eval.py`. You should see:

```

On average, your forecasts would have gotten 604.59 points per season. Elo got 645.16 points per season.

```

OK, looks like changing home-field advantage from 65 to 100 points isn't a good idea. With that tweak, our generated probabilities perform worse historically than the official FiveThirtyEight Elo probabilities.

## Making 2018 forecasts

Inside the `Util.read_games` function, there are three lines you can uncomment to download the 2018 schedule and results to `data/nfl_games_2018.csv`. If you run `python eval.py` after uncommenting them, you'll see something like the following in the output:

```

Forecasts for upcoming games:
2018-09-06	PHI vs. ATL		65% (Elo)		69% (You)
2018-09-09	BAL vs. BUF		64% (Elo)		68% (You)
2018-09-09	NYG vs. JAX		42% (Elo)		46% (You)

```

The scripts are now maintaining Elo ratings through the 2018 season, and printing forecasts (both from `elo_prob1` and from `my_prob1`) for upcoming games. Note that our model is more confident in the home team in every game because we've adjusted the `HFA` parameter to 100.

## More

Have at it! Some ideas for further exploration:

* Tweak the Elo parameters and margin of victory multiplier and see what happens.
* Augment these Elo ratings with data from other sources to improve forecasts.
* Use this code as an example to build your own model using whatever language, framework or approach you'd like.
