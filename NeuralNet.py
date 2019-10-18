import numpy as np
import mnist
import keras as k
import time
import pathlib as p

class NeuralNet:

    def __init__(self, path = None):
        self.alpha = 0.5
        self.epsilon = 0.5
        self.gamma = 1

        if path == None:
            self.model = self.init_model()
        else:
            self.model = self.load_model(path)

    def init_model(self):
        model = k.models.Sequential()
        model.add(k.layers.Conv2D())
        pass

    def load_model(self):
        pass




