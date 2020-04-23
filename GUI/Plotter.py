
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



#Learning rate states

harry = Plotter("States Visited TDMCTS_Learning_rate")


x = [0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000, 5200, 5400, 5600, 5800, 6000, 6200, 6400, 6600, 6800, 7000, 7200, 7400, 7600, 7800, 8000, 8200, 8400, 8600, 8800, 9000, 9200, 9400, 9600, 9800, 10000]

y_a0 = [0,307773,	513181,	588401,	692031,	759846,	779517,794685,871175,940094, 1036117, 1159687, 1195458, 1229790, 1349763, 1523471, 1583391, 1738018, 1758428, 1818709, 1874399, 1892737, 1918457, 1964668, 1983723, 2016113, 2030805, 2039971, 2254563, 2315472, 2456691, 2603055, 2805546, 2932701, 2979490, 3061011, 3118436, 3124308, 3138891, 3178553, 3209724, 3334728, 3471004, 3587963 , 3640439 , 3667998 , 3702022 , 3717556 , 3724670 , 3740001 , 3798870 ]
y_a000005 = [	0, 390864,	778655,	1174581, 1565796,1963655,2337226,2732691,3122833,3492790,3873584,4267858,4660874,5050125,5432511,5820946,6206307,6587736,6987669,7384732,7768738,8147343,8527228,8919797,9299689,9674877, 10053975, 10448407, 10836779, 11203896, 11577506, 11788989, 11850991,	11862326, 11872127, 11881296, 11889682, 11896458, 11900492, 11905361, 12046898, 12076242, 12106115, 12133647, 12158464, 12177915, 12210211, 12236957, 12260870, 12279225, 12302797]
y_a0005=[0,305673,595619,802217,919602,919651,919727,919743,919762,919865,919943,921701,921701,996145,996270,996359,996362,996558,1075523,1329949,1578267,1800799,1963033,2129028,2240356,2365566,2610178,2813462,3003096,3106739,3188777,3580292,3972275,4364877,4754258,5153260,5550011,5942036,6321679,6697975,7082929,7471884,7857505,8238204,8633286,9033403,9432505,9841192,10236427,10409861,10500491]

y_a005 = []
y_a1 = [	0, 390349,	770861,	1130285,	1495558,    1848783,    2213462,    2589350,    2945203,    3297765,    3641453,    4008239,    4357299,    4725217,    5078530,    5432117,    5800541,    6166708,    6534999,    6887675,    7241406,    7604095,    7963265,    8318545,    8670800,    9027152,    9372992,    9728244,   10084833,   10437379,   10805491,   11167469,   11517191,	11873613,	12234932,	12599859,	12970279,   13347485,   13710928,   14081511,   14429017,   14787225,   15145304,   15496588,   15857973,   16220550,   16580052,   16939279,   17300237,   17650062,   18022345]

harry.plot(x, y_a1, "1.0a", "purple")
harry.plot(x, y_a0 , "0.0a", "r")
harry.plot(x, y_a0005 , "0.0005a", "b")
harry.plot(x, y_a000005 , "0.000005a", "g")




'''
#Exploration rate

x = [0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000]

y_e0 = [46, 41, 47, 49,41,44,46,58,59,51,34,45,43,42,49,49,42,47,51,48,39,54,47,45,39,42]
y_e10 = [2,1,2,2,0,3,1,1,11,0,3,5,3,0,1,6,4,2,1,7,0,3,0,3,15,12]
y_e05 = [46,53,60,63,59,58,48,51,67,60,49,61,60,57,59,69,57,71,65,66,51,53,64,65,58,66]
y_e0 = [46,41,47,49,41,44,46,38,40,51,34,45,43,42,46,48,42,49,51,44,39,54,47,45,39,42]
y_e075 = [29,31,46,48,49,38,51,41,40,46,51,53,35,57,53,59,19,49,43,55,55,50,46,58,49,53]
y_e1 = [19,32,32,14,18,31,25,32,25,27,28,37,38,36,16,36,35,36,34,38,34,33,38,30,39,41]
y_e025 = [52,71,57,66,68,67,70,66,61,69,65,74,69,67,70,69,69,73,75,77,73,65,73,77,83,66]

y_e01 = [53, 55, 67, 60, 70, 69, 66, 70, 67, 57, 68, 65, 62, 60, 61, 60, 69, 69, 73, 67, 66, 71, 64, 65, 64, 69]
y_e02 = [54, 60, 65, 69, 66, 68, 62, 73, 66, 69, 72, 70, 67, 72, 68, 69, 59, 68, 70, 64, 71, 65, 82, 69, 65, 72]
y_e03 = [50, 65, 67, 61, 62, 64, 68, 61, 61, 74, 73, 71, 73, 67, 74, 62, 65, 71, 73, 70, 60, 74, 71, 58, 71, 66]
harry = Plotter("Exploration rates TDMCTS")
#harry.plot(x, y_e0, "0.0e", 'r')
#harry.plot(x, y_e01, "0.1e", "navy")
#harry.plot(x, y_e02, "0.2e", "cyan")
#harry.plot(x, y_e025, "0.25e", 'magenta')
#harry.plot(x, y_e03, "0.3e", "darkorange")
#harry.plot(x, y_e05, "0.5e", 'y')
#harry.plot(x, y_e075, "0.75e", 'green')
#harry.plot(x, y_e1, "1.0e", 'black')
#harry.plot(x, y_e10, "10.0e", 'darkorchid')
'''
'''
#states

y_e075 = [0, 252073, 495237, 723056, 936743, 1182732, 1410155, 1624369, 1833986, 2035201, 2239255, 2460709, 2680676, 2919326, 3115230, 3336957, 3551249, 3779551, 4011158, 4237536, 4452172, 4672264, 4901960, 5128243, 5334830, 5551729]
y_e025 = [0, 305673, 595619, 802217, 919602, 919651, 919727, 919743, 919762, 919865, 919943, 921701, 921701, 996145, 996270, 996359, 996362, 996558, 1075523, 1329949, 1578267, 1800799, 1963033, 2129028, 2240356, 2365566]
y_e1 = [0,224876, 430693, 635693, 845897, 1046671, 1246522, 1445679, 1659574, 1847584, 2052374, 2239457, 2420763, 2605862, 2798303, 3003546, 3208599, 3393911, 3584797, 3773356,3974759, 4188104, 4378680, 4559218, 4744966, 4923223]
y_e10 = [0, 246346, 464455, 667352, 862999, 1059502, 1238155, 1432901, 1627999, 1800413, 1989953, 2160565, 2327048, 2510331, 2713225, 2888034, 3060141, 3238829, 3421540, 3584418, 3761008, 3937645, 4124257, 4288847, 4469666, 4619676 ]
y_e05 = [0, 299675, 590252, 874033, 1165941, 1425995, 1695583, 1968681, 2215802, 2455953, 2706504, 2940208, 3179092, 3402377, 3619097, 3832060, 4027781, 4251858, 4478073, 4680529, 4878067, 5029875, 5178508, 5334035, 5470619, 5611263]

x_e005 = [0, 200, 400, 600, 800, 1000, 1200,1400,1800,5000]
y_e005 = [0, 16036, 16036, 16036, 16039, 16041, 20374, 22560, 22560,22560]

harry = Plotter("States Visited TDMCTS")
harry.plot([0,200,5000], [0,4570,4570], "0.0e", "r")

#harry.plot(x_e005, y_e005, "0.05e", 'navy')
harry.plot(x, y_e025, "0.25e", 'magenta')
harry.plot(x, y_e05, "0.5e", 'y')
harry.plot(x, y_e075, "0.75e", 'green')
harry.plot(x, y_e1, "1.0e", 'black')
harry.plot(x, y_e10, "10.0e", 'cyan')
'''






#exploration_rate ttt
x = [0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000, 5200, 5400, 5600]

e025_y = [0,305673,595619,802217,919602,919651,919727,919743,919762,919865,919943,921701,921701,996145,996270,996359,996362,996558,1075523,1329949,1578267,1800799,2042823,2249360,2439793,2566097, 2698693, 2859224, 3037048]
x_3 = [0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200, 2400, 2600]
e05_y = [0, 301510, 558501, 793083, 1023561, 1200509, 1473263,1730349,2011082,2276328,2540873, 2763578, 2986135, 3238199]

x_2 = [0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800]
e1_y = [0, 224876, 430693, 635693,845897,1046671, 1246522, 1445679, 1659574, 1847584, 2052374, 2239457, 2420763, 2605862, 2798303, 3003546, 3208599, 3393911, 3584797, 3773356, 3974759, 4188104, 4378680, 4559218, 4744966]

x_4 = [0, 200, 6000]
e0_y = [0,1108,1108]
'''
harry = Plotter("Exploration rates TDMCTS")
harry.plot(x, e025_y, "0.25", 'r')
harry.plot(x_2, e1_y, "1.0", 'b')
harry.plot(x_3, e05_y, "0.5", 'g')
harry.plot(x_4, e0_y, "0.0", 'y')
'''
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

