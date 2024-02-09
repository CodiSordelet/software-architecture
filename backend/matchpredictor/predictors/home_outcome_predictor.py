from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Prediction, Predictor

class PointsTable:
    def __init__(self):
        self.points_dict = {}

    def points_for(self, team):
        return self.points_dict.get(team.name, 0)

    def record_win(self, team):
        self.__add_points(team, 3)

    def record_draw(self, team):
        self.__add_points(team, 1)

    def __add_points(self, team, points):
        previous_points = self.points_dict.get(team.name, 0)
        self.points_dict[team.name] = previous_points + points
        
        
        
def calculate_table(results):
    table = PointsTable()

    for result in results:
        if result.outcome == Outcome.HOME:
            table.record_win(result.fixture.home_team)
        elif result.outcome == Outcome.AWAY:
            table.record_win(result.fixture.away_team)
        else:
            table.record_draw(result.fixture.home_team)
            table.record_draw(result.fixture.away_team)
            
    return table
        
        
class HomeOutcomePredictor(Predictor):
    def __init__(self, table):
        self.table = table


    def predict(self, fixture):
        #if the team is home and it wins then return home 
        #if the team is away and it wins return away
        #if it is a draw then return draw
        home_points = self.table.points_for(fixture.home_team)
        away_points = self.table.points_for(fixture.away_team)

        if home_points > away_points and fixture.home_team.name < fixture.away_team.name:
            return Prediction(Outcome.HOME)
        elif home_points < away_points and fixture.home_team.name > fixture.away_team.name :
            return Prediction(Outcome.AWAY)
        else:
            return Prediction(Outcome.DRAW)
        
        
        



def train_home_outcome_predictor(results):
    return HomeOutcomePredictor(calculate_table(results))
        
        
    
        
