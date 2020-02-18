import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})
tesauro_data = [0, 42, 83, 122, 160, 201, 242, 277, 316, 353, 390, 429, 468, 501, 538, 577, 617, 655, 695, 734, 773, 812, 851, 890, 926, 965, 1003, 1039, 1076, 1113, 1153, 1192, 1232, 1266, 1301, 1339, 1378, 1415, 1454, 1493, 1532, 1571, 1611, 1647, 1686, 1726, 1766, 1805, 1844, 1883, 1922, 1961, 1999, 2038, 2077, 2117, 2152, 2191, 2230, 2269, 2309, 2349, 2386, 2425, 2462, 2501, 2538, 2577, 2614, 2653, 2689, 2725, 2764, 2797, 2836, 2873, 2902, 2941, 2976, 3015, 3053, 3090, 3130, 3169, 3203, 3242, 3281, 3320, 3359, 3396, 3436, 3473, 3512, 3551, 3591, 3627, 3666, 3705, 3742, 3779]

td_data = [0, 111156, 253691,396141,536662,678369,821038,965321,1100994,1233633,1398546]


tes_x = [i+1 for i in range(len(tesauro_data))]
td_x = [i * 10 for i in range(len(td_data))]


wr_x = [
    1,2,3,4,5,6
]

wr_y = [
    32/50 * 100,45/50 * 100,42/50 * 100,43/50 * 100,42/50 * 100,36/50 * 100
]


td_mx_x = [0, 100, 200, 300]
td_mx_y = [57, 74, 99, 100]



for _ in range(len(td_mx_y)):
  #  td_mx_y[_] /= 100
    pass

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
        plt.ylabel("Win Rate %")
        plt.legend()
        plt.savefig(self.title + ".png")
        plt.show()


data = np.column_stack((tes_x, tesauro_data))


harry = Plotter("TDUCT VS MINIMAX")
harry.plot(td_mx_x, td_mx_y, "TDUCT", 'r')
#harry.plot(wr_x, wr_y, "TDUCT", 'r')
##harry.plot(td_x, td_data, "TDUCT", 'b')
#harry.plot(data2, "MCTS_TD")
harry.show()
