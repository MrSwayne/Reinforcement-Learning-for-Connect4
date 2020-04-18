<<<<<<< HEAD
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
        plt.ylabel("Win rate %")
        plt.legend()
        plt.savefig(self.title + ".png")
        plt.show()


y_data = [56, 65, 62, 77]
x_data = [0, 1000, 2000, 3000]

tic_x = [0,50,100,150,200,250,300,350,400,450,500]
tic_y = [26,46,47,33,37,44,44,34,40,36,35]

tic2_y = [25,50,50,50,50,50,50,50,50,50,50]

for i in range(len(tic_y)):
    tic_y[i] *= 2
    tic2_y[i] *= 2

tduct_x = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900, 950,1000,1050,1100,1200,1250,1300,1350,1400,1450,1500,1550,1600,1650,1700]
tduct_y = [54,59,66,86,  95, 85, 96, 94, 80, 85, 85, 78, 77, 106,105,95,111, 93,110, 104, 91,  99,  114, 94,  81,  102, 98,  96,  105, 119, 105, 101, 103, 114]

uct_x = []
uct_y = [144,139,130,110,105,137,102,103,118,113,109,118,121,92,93,127,89,105,89,92,106,99,84]

for i in range(len(tduct_x)):
    tduct_y[i] = tduct_y[i] / 2
#    uct_y[i] = uct_y[i] / 2

x2 = [50,61,49,53,66,62,64,62,64,74,59,70,77,68,74,76,61,50,59,51,62,61,71,69,71,64,57,65,71,71]
y2 = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900]

y = [26.04, 24.2, 22.08, 23.46, 27.51, 23.79, 23.11]
x = [0,400,900,1400,1900,2400,2900]





#td200, e=1, l0.9 vs AB6
TTT_TD_X_1 = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000,3100,3200,3300,3400,3500,3600,3700,3800,3900,4000,4100,4200,4300,4400,4500,4600,4700,4800,4900,5000]
TTT_TD_Y_1 = [47,51,79,82,80,64,72,76,94,93,90,85,86,93,95,95,85,90,70,80,92,80,77,81,81,90,94,69,49,52,85,83,87,82,87,82,81,87,88,85,82,72,83,83,87,76,77,91,85,89,83]

#td 200, e=0.5, l0.9 vs AB6
TTT_TD_X_2 = TTT_TD_X_1
TTT_TD_Y_2 = [46,56,78,78,73,75,68,63,62,72,78,75,74,85,76,69,77,66,67,79,60,73,70,71,76,79,79,74,82,69,77,83,74,79,69,85,70,79,79,74,78,81,65,76,77,87,72,76,71,81,73]

#td200, e=1,
TTT_TD_X_3 = [0,100,200,300,400,500,600,700,2500,3000,5000]
TTT_TD_Y_3 = [45,100,11,0,100,0,81,100,100,100,100]

harry = Plotter("TD200 vs AB6 TTT e5 first move")
harry.plot(TTT_TD_X_3, TTT_TD_Y_3, "TDUCT200", 'b')

'''

td_200_v_ab6_x = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500]
td_200_v_ab6_y = [52,91,35,97,60,63,71,66,79,76,88,70,77,80,81,79]
harry = Plotter("TD200 v AB6 TTT")
harry.plot(td_200_v_ab6_x, td_200_v_ab6_y, "TD200", 'b')
'''


#data = np.column_stack((tes_x, tesauro_data))

'''
harry = Plotter("TD200 VS AB4 TTT")
harry.plot(tic_x,tic_y, "TDUCT100", 'r')
harry.plot(tic_x,tic2_y, "TDUCT10", 'b')
'''

#harry = Plotter("TDUCT100 vs UCT500")

#harry.plot(tduct_x, tduct_y, "TDUCT", 'r')
#harry.plot(tduct_x, uct_y, "UCT", 'y')

#harry.plot(y2, x2, "TDUCT100", 'b')
#harry.plot(x, y, "TDUCT", 'r')
#harry.plot(x_data, y_data, "TDUCT", 'r')
#harry.plot(td_mx_x, td_mx_y, "TDUCT", 'r')
#harry.plot(wr_x, wr_y, "TDUCT", 'r')
##harry.plot(td_x, td_data, "TDUCT", 'b')
#harry.plot(data2, "MCTS_TD")
harry.show()
=======
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
        plt.ylabel("States Visited")
        plt.ticklabel_format(style='plain')
        plt.legend()
        plt.savefig(self.title + ".png")
        plt.show()


y_data = [56, 65, 62, 77]
x_data = [0, 1000, 2000, 3000]

tic_x = [0,50,100,150,200,250,300,350,400,450,500]
tic_y = [26,46,47,33,37,44,44,34,40,36,35]

tic2_y = [25,50,50,50,50,50,50,50,50,50,50]

for i in range(len(tic_y)):
    tic_y[i] *= 2
    tic2_y[i] *= 2

tduct_x = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900, 950,1000,1050,1100,1200,1250,1300,1350,1400,1450,1500,1550,1600,1650,1700]
tduct_y = [54,59,66,86,  95, 85, 96, 94, 80, 85, 85, 78, 77, 106,105,95,111, 93,110, 104, 91,  99,  114, 94,  81,  102, 98,  96,  105, 119, 105, 101, 103, 114]

uct_x = []
uct_y = [144,139,130,110,105,137,102,103,118,113,109,118,121,92,93,127,89,105,89,92,106,99,84]

for i in range(len(tduct_x)):
    tduct_y[i] = tduct_y[i] / 2
#    uct_y[i] = uct_y[i] / 2

x2 = [50,61,49,53,66,62,64,62,64,74,59,70,77,68,74,76,61,50,59,51,62,61,71,69,71,64,57,65,71,71]
y2 = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900]

y = [26.04, 24.2, 22.08, 23.46, 27.51, 23.79, 23.11]
x = [0,400,900,1400,1900,2400,2900]




'''
#td200, e=1, l0.9 vs AB6
TTT_TD_X_1 = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000,3100,3200,3300,3400,3500,3600,3700,3800,3900,4000,4100,4200,4300,4400,4500,4600,4700,4800,4900,5000]
TTT_TD_Y_1 = [47,51,79,82,80,64,72,76,94,93,90,85,86,93,95,95,85,90,70,80,92,80,77,81,81,90,94,69,49,52,85,83,87,82,87,82,81,87,88,85,82,72,83,83,87,76,77,91,85,89,83]

#td 200, e=0.5, l0.9 vs AB6
TTT_TD_X_2 = TTT_TD_X_1
TTT_TD_Y_2 = [46,56,78,78,73,75,68,63,62,72,78,75,74,85,76,69,77,66,67,79,60,73,70,71,76,79,79,74,82,69,77,83,74,79,69,85,70,79,79,74,78,81,65,76,77,87,72,76,71,81,73]

#td200, e=1,
TTT_TD_X_3 = [0,100,200,300,400,500,600,700,2500,3000,5000]
TTT_TD_Y_3 = [45,100,11,0,100,0,81,100,100,100,100]

harry = Plotter("TD200 vs AB6 TTT e5 first move")
harry.plot(TTT_TD_X_3, TTT_TD_Y_3, "TDUCT200", 'b')

'''



#exploration_rate
x = [0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000, 5200, 5400, 5600]

e025_y = [0,305673,595619,802217,919602,919651,919727,919743,919762,919865,919943,921701,921701,996145,996270,996359,996362,996558,1075523,1329949,1578267,1800799,2042823,2249360,2439793,2566097, 2698693, 2859224, 3037048]
x_3 = [0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200, 2400, 2600]
e05_y = [0, 301510, 558501, 793083, 1023561, 1200509, 1473263,1730349,2011082,2276328,2540873, 2763578, 2986135, 3238199]

x_2 = [0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800]
e1_y = [0, 224876, 430693, 635693,845897,1046671, 1246522, 1445679, 1659574, 1847584, 2052374, 2239457, 2420763, 2605862, 2798303, 3003546, 3208599, 3393911, 3584797, 3773356, 3974759, 4188104, 4378680, 4559218, 4744966]

x_4 = [0, 200, 6000]
e0_y = [0,1108,1108]

harry = Plotter("Exploration rates TDMCTS")
harry.plot(x, e025_y, "0.25", 'r')
harry.plot(x_2, e1_y, "1.0", 'b')
harry.plot(x_3, e05_y, "0.5", 'g')
harry.plot(x_4, e0_y, "0.0", 'y')
'''

td_200_v_ab6_x = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500]
td_200_v_ab6_y = [52,91,35,97,60,63,71,66,79,76,88,70,77,80,81,79]
harry = Plotter("TD200 v AB6 TTT")
harry.plot(td_200_v_ab6_x, td_200_v_ab6_y, "TD200", 'b')
'''


#data = np.column_stack((tes_x, tesauro_data))

'''
harry = Plotter("TD200 VS AB4 TTT")
harry.plot(tic_x,tic_y, "TDUCT100", 'r')
harry.plot(tic_x,tic2_y, "TDUCT10", 'b')
'''

#harry = Plotter("TDUCT100 vs UCT500")

#harry.plot(tduct_x, tduct_y, "TDUCT", 'r')
#harry.plot(tduct_x, uct_y, "UCT", 'y')

#harry.plot(y2, x2, "TDUCT100", 'b')
#harry.plot(x, y, "TDUCT", 'r')
#harry.plot(x_data, y_data, "TDUCT", 'r')
#harry.plot(td_mx_x, td_mx_y, "TDUCT", 'r')
#harry.plot(wr_x, wr_y, "TDUCT", 'r')
##harry.plot(td_x, td_data, "TDUCT", 'b')
#harry.plot(data2, "MCTS_TD")
harry.show()
>>>>>>> 391e228... graph time
