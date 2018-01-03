import pandas as pd
import json
import datetime
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from geoencoder.grid_encoder import GridEncoder
from geoencoder.location import Location
import numpy as np

class GeoFeaturizer():
    def __init__(self):
        self.address_to_data = self.get_address_to_data_dict()
        self.blockchain_info = json.load(open("data/blockchaininfo.json"))
        self.hours, self.addresses = self.get_hours_and_addresses()
        self.probability_grids=  self.get_probability_grids()
        self.hour_encodings = np.array(pd.get_dummies(pd.Series(self.hours)))
        self.data_train, self.data_test, self.labels_train, self.labels_test = train_test_split(self.hour_encodings, self.probability_grids, random_state=42,
                                                                            test_size=0.20)
    def get_address_to_data_dict(self):
        geocoded_data = pd.read_csv("data/geocoded.tsv", sep="\t")
        geocoded_data.set_index("address", inplace=True)
        address_to_data = geocoded_data.to_dict("index")
        return address_to_data

    def get_hours_and_addresses(self):
        addresses, hours, = [], []
        for info in self.blockchain_info.values():
            if info != None:
                if len(info["txs"]) != 0:
                    address = info["address"]
                    time = info["txs"][0]["time"]
                    parsed_time = datetime.datetime.utcfromtimestamp(time)
                    hour = parsed_time.hour
                    addresses.append(address)
                    hours.append(hour)
        return hours, addresses

    def get_probability_grids(self, resolution=180):
        grid_encoder = GridEncoder(resolution)
        encodings = []
        for address in self.addresses:
            geodata = self.address_to_data[address]
            location = Location(geodata["bottom"], geodata["top"], geodata["left"], geodata["right"])
            encoding = grid_encoder.encode(location)
            encodings.append(encoding.flatten())
        return np.array(encodings)


