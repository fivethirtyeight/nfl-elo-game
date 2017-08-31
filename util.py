import csv
import urllib2

class Util:

    @staticmethod
    def read_games(file):
        """ Initializes game objects from csv """
        games = [item for item in csv.DictReader(open(file))]

        # Uncommenting will grab the latest game results for 2017, update team ratings accordingly, and make forecasts for upcoming games
        #games += [item for item in csv.DictReader(urllib2.urlopen("https://projects.fivethirtyeight.com/nfl-api/2017/nfl_games_2017.csv"))]

        for game in games:
            game['season'], game['neutral'], game['playoff'] = int(game['season']), int(game['neutral']), int(game['playoff'])
            game['score1'], game['score2'] = int(game['score1']) if game['score1'] != '' else None, int(game['score2']) if game['score2'] != '' else None
            game['elo_prob1'], game['result1'] = float(game['elo_prob1']) if game['elo_prob1'] != '' else None, float(game['result1']) if game['result1'] != '' else None

        return games

    @staticmethod
    def evaluate_forecasts(games):
        """ Evaluates and scores forecasts in the my_prob1 field against those in the elo_prob1 field for each game """
        points_by_season = {}

        forecasted_games = [g for g in games if g['result1'] != None]
        upcoming_games = [g for g in games if g['result1'] == None and 'my_prob1' in g]

        # Evaluate forecasts and group by season
        for game in forecasted_games:

            # Skip unplayed games and ties
            if game['result1'] == None or game['result1'] == 0.5:
                continue

            if game['season'] not in points_by_season:
                points_by_season[game['season']] = 0.0

            # Calculate points for game
            elo_brier = (game['result1'] - game['elo_prob1']) * (game['result1'] - game['elo_prob1'])
            my_brier = (game['result1'] - game['my_prob1']) * (game['result1'] - game['my_prob1'])
            points = ((1.0 - my_brier) - (1.0 - elo_brier)) * 100
            if game['playoff'] == 1:
                points *= 2
            points_by_season[game['season']] += points

        # Print individual seasons
        for season in points_by_season:
            print "In %s, your forecasts would have %s %s points" % (season, "gained" if points_by_season[season] >= 0 else "lost", abs(round(points_by_season[season], 1)))

        # Print forecasts for upcoming games
        if len(upcoming_games) > 0:
            print "\nForecasts for upcoming games:"
            for game in upcoming_games:
                print "%s\t%s vs. %s\t\t%s%% (Elo)\t\t%s%% (You)" % (game['date'], game['team1'], game['team2'], int(round(100*game['elo_prob1'])), int(round(100*game['my_prob1'])))

        # Show overall performance
        avg = sum(points_by_season.values())/len(points_by_season.values())
        print "\nOn average, your forecasts would have %s %s points per season\n" % ("gained" if avg >= 0 else "lost", abs(round(avg, 1)))

