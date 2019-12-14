import numpy as np
import keras as k
import time
import pathlib as p
import os.path
from os import path

class NeuralNet:

    def __init__(self, name):
        self.path = "NeuralNet/" + name + ".h5"
        self.gamma = 0.5
        self.model = self.init_model()

        if not os.path.exists(self.path):
            f = open(self.path, "w+")
            f.close()
        else:
            self.load_model()

    def init_model(self):
        model = k.models.Sequential()
        model.add(k.layers.Dense(80, input_dim=2, activation='relu'))
        model.add(k.layers.Dense(80, activation='relu'))
        model.add(k.layers.Dense(80, activation='relu'))
        model.add(k.layers.Dense(7, activation='softmax'))

        model.compile(loss='binary_crossentropy', optimizer= k.optimizers.Adam(learning_rate=0.0005), metrics=['accuracy'])
        return model

    def learn(self, state, next_state, action, reward):

        action_vector = self.model.predict(state)
        action_vector[0][action] = reward + self.gamma * np.argmax(self.model.predict(next_state))

      #  action_vector = self.model.predict(state)

        self.model.fit(state, action_vector, epochs=1)

    #    print("NN: ", action_vector, "\tMCTS: ", action)

    def save(self):
        self.model.save_weights(self.path)

    def load_model(self):
        self.model = self.init_model()

        try:
            self.model.load_weights(self.path)
        except:
            print("Error loading weights")

    def save_model(self):
        self.model.save_weights(self.path)