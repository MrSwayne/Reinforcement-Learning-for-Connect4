import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})

class Plotter:

    def __init__(self, title):
        self.title = title
        self.plots = []

    def plot(self, x, y, label, col):
        self.plots.append((x,y, label, col))

    def show(self):
        for x,y,label, col in self.plots:
            plt.plot(x, y, col, label=label)

        plt.xlabel("Episodes")
        plt.ylabel("Moves")
        plt.legend()
        plt.savefig(self.title + ".png")
        plt.show()


y_data = [56, 65, 62, 77]
x_data = [0, 1000, 2000, 3000]



x2 = [50,61,49,53,66,62,64,62,64,74,59,70,77,68,74,76,61,50,59,51,62,61,71,69,71,64,57,65,71,71]
y2 = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900]

y = [26.04, 24.2, 22.08, 23.46, 27.51, 23.79, 23.11]
x = [0,400,900,1400,1900,2400,2900]
#data = np.column_stack((tes_x, tesauro_data))


harry = Plotter("Moves td100_vs_200")

#harry.plot(y2, x2, "TDUCT100", 'b')
harry.plot(x, y, "TDUCT", 'r')
#harry.plot(x_data, y_data, "TDUCT", 'r')
#harry.plot(td_mx_x, td_mx_y, "TDUCT", 'r')
#harry.plot(wr_x, wr_y, "TDUCT", 'r')
##harry.plot(td_x, td_data, "TDUCT", 'b')
#harry.plot(data2, "MCTS_TD")
harry.show()
