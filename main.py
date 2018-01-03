from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LinearRegression
from utils.featurizer import GeoFeaturizer
from sklearn.multioutput import MultiOutputRegressor


class Model():
    def __init__(self):
        self.featurizer = GeoFeaturizer()
        self.base_model =  MultiOutputRegressor(LinearRegression())

    def train(self):
        print(self.featurizer.data_train.shape)
        print(self.featurizer.labels_train.shape)
        self.base_model.fit(self.featurizer.data_train, self.featurizer.labels_train)

    def print_score(self):
        print(self.base_model.score(self.featurizer.data_test, self.featurizer.labels_test))

if __name__=="__main__":
    model = Model()
    model.train()
    model.print_score()
