import tkinter as TK

class Selector():

    def __init__(self):

        self.options = {"MCTS": [
            "Learning Rate",
            "Exploration Rate",
            "Discount Factor",
            "Number of Simulations"

        ], "TDMCTS": [
            "Learning Rate",
            "Exploration Rate",
            "Discount Factor",
            "Number of Simulations"

        ], "Minimax": [
            "Depth"

        ], "Random": []}

        self.values = {}


    def show_algorithm_options(self, algorithm):

        pos = 1

        self.values["Algorithm"] = algorithm
        for paramater in self.options[algorithm]:
            lbl = TK.Label(self.window, text=paramater)
            lbl.grid(column=0, row=pos)

            entry_var = TK.StringVar()
            entry = TK.Entry(self.window, width=10, textvariable= entry_var)
            self.values[paramater] = entry_var

            entry.grid(column=1, row=pos)

            pos += 1


    def create_gui(self):
        self.window = TK.Tk()
        self.window.title("Settings")
        self.window.geometry('350x200')

        option_var = TK.StringVar(self.window)
        option_var.set("TDMCTS")


        option_menu = TK.OptionMenu(self.window, option_var, *list(self.options.keys()), command=self.show_algorithm_options)
        option_menu.grid(column=0, row=0)


    def draw(self):
        self.create_gui()
        self.window.mainloop()



menu = Selector()
menu.draw()
