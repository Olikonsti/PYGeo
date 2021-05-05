from tkinter import *
import tkinter.ttk as ttk
from PLOTTER import *

class GeoWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1000x800")
        self.title("PYGeo 1.1")

        self.canvas = GeoCanvas(self)

class GeoSettings(Tk):
    def __init__(self, geocanvas, color):
        self.geocanvas = geocanvas
        Tk.__init__(self)

        self.config(bg=color)
        self.geometry("700x500")
        self.resizable(False, False)
        self.title("PyGeo Settings")

        sim_amount = LabelFrame(self, text="Line Simulation Amount", width=300, height=100)
        sim_amount.place(x=0, y=0)
        f_1 = Frame(sim_amount)
        f_1.grid(row=1, column=1)
        Button(f_1, text="low\n(20)", command=lambda: self.sim_amount_(20), bg="lightgreen").grid(row=1, column=1)
        Button(f_1, text="middle\n(60)", command=lambda: self.sim_amount_(60), bg="green").grid(row=1, column=2)
        Button(f_1, text="high\n(100)", command=lambda: self.sim_amount_(100), bg="orange").grid(row=1, column=3)
        Button(f_1, text="ultra\n(200)", command=lambda: self.sim_amount_(200), bg="orangered").grid(row=1, column=4)
        sim_amount_custom = ttk.Entry(sim_amount)
        sim_enter = Button(sim_amount, text=">", command=lambda: self.sim_amount_(int(sim_amount_custom.get())))
        sim_enter.grid(row=2, column=2)
        sim_amount_custom.grid(row=2, column=1)

        sim_resolution = LabelFrame(self, text="Vertex Resolution")
        sim_resolution.place(x=180, y=0)
        Button(sim_resolution, text="low\n(0.25)", command=lambda: self.sim_resolution_(0.25), bg="lightgreen").pack(side=LEFT)
        Button(sim_resolution, text="middle\n(0.125)", command=lambda: self.sim_resolution_(0.125), bg="green").pack(side=LEFT)
        Button(sim_resolution, text="high\n(0.0625)", command=lambda: self.sim_resolution_(0.0625), bg="orange").pack(side=LEFT)
        Button(sim_resolution, text="ultra\n(0.03125)", command=lambda: self.sim_resolution_(0.03125), bg="orangered").pack(side=LEFT)
        Button(sim_resolution, text="extreme\n(0.015625)", command=lambda: self.sim_resolution_(0.015625), bg="red").pack(side=LEFT)
        Button(sim_resolution, text="TR-3990X\n(0.0078125)", command=lambda: self.sim_resolution_(0.0078125), bg="darkred").pack(side=LEFT)
        Button(sim_resolution, text="крах\n(0.00390625)", command=lambda: self.sim_resolution_(0.00390625), bg="darkgrey").pack(side=LEFT)

        Button(self, text="Vertecies\n", command=self.geocanvas.plotter.toggle_vertecies, bg="lightblue").place(x=610, y=17)

        Button(self, text="Change Appearence\n", command=self.geocanvas.change_mode, bg="grey").place(x=0, y=90)

        info = Label(self, text="PyGeo\n"
                                "Developer: Konstantin Ehmann\n"
                                "Website: http://kundv.org")
        info.place(x=300, y=300)




    def sim_resolution_(self, amount):
        self.geocanvas.plotter.resolution = amount
        self.geocanvas.plotter.clear()
        self.geocanvas.plotter.draw()

    def sim_amount_(self, amount):
        self.geocanvas.plotter.calc_amount = amount
        self.geocanvas.plotter.clear()
        self.geocanvas.plotter.draw()


class GeoCanvas(Canvas):
    def __init__(self, parent):

        self.mode = "light"
        self.bg = "#202020"



        self.parent = parent
        Canvas.__init__(self, parent, bg="white", height=3000, width=3000, highlightthickness=0)
        self.place(x=0, y=0)



        self.plotter = Plotter(self)

        self.function_frame = LabelFrame(self.parent, width=300, height=50, text="Function", bg="grey")
        self.function_frame.place(x=0, y=self.plotter.winy - 50)

        self.function_entry = ttk.Entry(self.function_frame)
        self.function_entry.place(x=0, y=2)

        self.enter_button = ttk.Button(self.function_frame, text="Run", command=self.run)
        self.enter_button.place(x=130, y=0)

        self.settings_button = ttk.Button(self.function_frame, text="Settings", command=self.open_settings)
        self.settings_button.place(x=210, y=0)

        self.parent.bind('<Return>', self.run)

        self.change_mode()

    def change_mode(self):
        print("changing appearence...\nplease wait")
        if self.mode == "dark":
            self.mode = "light"
            self.bg = "white"
            self.fg = "black"
            self.values = "lightgrey"

        else:
            self.mode = "dark"
            self.bg = "#202020"
            self.fg = "white"
            self.values = "#2B2B2B"

        try:
            self.settings.config(bg=self.bg)
        except:
            pass

        self.config(bg=self.bg)
        self.plotter.graph_color = self.fg
        self.plotter.grid_color = self.values

        self.plotter.clear()
        self.plotter.draw()

    def open_settings(self):
        self.settings = GeoSettings(self, self.bg)


    def unfocus(self):
        try:
            self.enter_button.focus()
        except:
            pass

    def run(self, event=None):
        self.enter_button.focus()
        self.plotter.clear()
        self.plotter.function = self.function_entry.get()
        self.plotter.draw()


    def update_fuction_frame(self):
        self.function_frame.place(x=0, y=self.plotter.winy - 50)



