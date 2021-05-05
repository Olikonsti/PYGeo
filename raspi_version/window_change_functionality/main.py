from tkinter import *
import tkinter.ttk as ttk
from math import *



class GeoWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1000x800")
        self.title("PYGeo")

        self.canvas = GeoCanvas(self)

class GeoSettings(Toplevel):
    def __init__(self, geocanvas, color):
        self.geocanvas = geocanvas
        Toplevel.__init__(self)

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


line_list = []

class Plotter():
    def __init__(self, parent):
        self.parent = parent

        self.parent.update()

        self.winx = parent.parent.winfo_width()
        self.winy = parent.parent.winfo_height()


        self.two_graphes = False

        self.function = "y=sin(x)"
        self.function2 = "y2=cos(x)"

        self.graph_color = "black"
        self.grid_color = "lightgrey"

        self.zoom_factor = 0.003
        self.calc_amount = 100

        self.vertex_amount = 0

        self.show_vertecies = False
        self.axes_point_size = 5

        self.scale = 0.1
        self.scaling = True

        self.resolution = 0.125 / 2

        self.info = Label(parent, text=
        f"loading...", bg="lightgrey", justify=LEFT)
        self.info.place(x=0, y=0)

        self.bind_keys()
        self.draw()

    def update_window_x_y(self, event=None):
        #self.parent.parent.after(1000, self.update_window_x_y)

        if (self.winx != event.width) and (self.winy != event.height):

            self.winx = self.parent.parent.winfo_width()
            self.winy = self.parent.parent.winfo_height()

            self.parent.update_fuction_frame()

            self.clear()
            self.draw()

    def draw(self):
        global x, y

        self.parent.unfocus()
        self.draw_axis()



        if self.scale < 0.001:
            self.scale = 0.001

        if self.zoom_factor < 0.001:
            self.zoom_factor = 0.001

        middle_indicator = self.parent.create_rectangle(self.winx/2 - self.axes_point_size, self.winy/2 - self.axes_point_size, self.winx/2 + self.axes_point_size, self.winy/2 + self.axes_point_size, fill="red", outline="")

        i = 0

        y = 0

        self.vertex_amount = 0


        while True:

            self.vertex_amount += 1

            self.draw_axis_value(i)

            i = i + self.resolution

            #print(i)

            # setup code
            x = i - self.calc_amount/2



            # function
            try:
                exec("global x, y; " + self.function)
            except Exception as e:
                print(str(e))
                print("math failed")
                y = 0
                self.parent.create_text(self.winx/2, self.winy/2 - 100, text=e, font="Consolas 20")
                break



            # setup code
            x = x / self.scale
            y = y / self.scale

            y = self.winy/2 - y
            x = x + self.winx/2

            self.x = x
            if self.two_graphes:
                self.draw_second_graph()

            if self.show_vertecies:
                self.parent.create_rectangle(x-3, y-3, x+3, y+3, fill="orange", outline="")

            Line(self.parent, x, y)
            if i >= self.calc_amount:
                break

        for i in line_list:
            i.create_line(self.graph_color)
        self.parent.parent.update()

        self.info.config(text=
                         f"zoom_factor:  {round(self.zoom_factor, 3)} >Press Down to lower and Up to increase\n"
                         f"calc_amount:  {self.calc_amount}\n"
                         f"scale:        {round(self.scale, 4)} >Use mouse wheel\n"
                         f"mousewheel in scale mode:     {self.scaling} >Use M to change\n"
                         f"resolution:   {self.resolution}\n"
                         f"show_vertecies: {self.show_vertecies} >Press V to toggle\n"
                         f"vertex_amount: {self.vertex_amount}\n"
                         f"Press B to center graph")

    def draw_second_graph(self):
        x = self.x
        try:
            y2 = 0
            exec("global x, y2; " + self.function)
        except Exception as e:
            print(str(e))
            print("math failed")
            y2 = 0
            self.parent.create_text(self.winx / 2, self.winy / 2 - 100, text=e, font="Consolas 20")
            print("Y2" + str(y2))
        y2 = y2 / self.scale
        y2 = self.winy / 2 - y2
        if self.show_vertecies:
            self.parent.create_rectangle(x - 2, y2 - 2, x + 2, y2 + 2, fill="blue", outline="")
        Line(self.parent, x, y2)

    def draw_axis(self):
        try:
            self.parent.delete(self.y_axis)
        except:
            pass

        self.y_axis = self.parent.create_line(self.winx / 2, 0, self.winx / 2, self.winy / 2 + 2000, fill="grey")
        self.x_axis = self.parent.create_line(0, self.winy / 2, self.winx / 2 + 2000, self.winy / 2, fill="grey")

    def draw_axis_value(self, index):

        zerox = self.winx / 2
        zeroy = self.winy / 2

        pattern = 0
        pattern2 = 0

        place_scale = round(self.scale * 60)
        if self.scale < 0.01:
            place_scale = 1
            pattern2 = 0.5
        if place_scale == 0:
            pass
        else:
            if index % place_scale == pattern or index % place_scale == pattern2:

                # drawing grid
                self.parent.create_line(zerox + index / self.scale, 0, zerox + index / self.scale, 2000, fill=self.grid_color)
                self.parent.create_line(zerox - index / self.scale, 0, zerox - index / self.scale, 2000, fill=self.grid_color)
                self.parent.create_line(0, zeroy + index / self.scale, 2000, zeroy + index / self.scale, fill=self.grid_color)
                self.parent.create_line(0, zeroy - index / self.scale, 2000, zeroy - index / self.scale, fill=self.grid_color)

                # drawing numbers
                self.axis_valuex = self.parent.create_text(zerox + index / self.scale, zeroy, text=index, fill=self.graph_color)
                self.axis_valuey = self.parent.create_text(zerox, zeroy - index / self.scale, text=index, fill=self.graph_color)
                self.axis_valuex = self.parent.create_text(zerox - index / self.scale, zeroy, text="-" + str(index), fill=self.graph_color)
                self.axis_valuey = self.parent.create_text(zerox, zeroy + index / self.scale, text="-" + str(index), fill=self.graph_color)



    def bind_keys(self):
        self.parent.parent.bind('<m>', self.activate_swift)
        self.parent.parent.bind_all("<MouseWheel>", self.scroll)
        self.parent.parent.bind('<v>', self.toggle_vertecies)
        self.parent.parent.bind('<Up>', self.increase_zoom_factor)
        self.parent.parent.bind('<Down>', self.decrease_zoom_factor)
        self.parent.parent.bind('<b>', self.update_window_x_y)

    def activate_swift(self, event=None):
        if self.scaling:
            self.scaling = False
        else:
            self.scaling = True


    def clear(self):
        for i in line_list:
            i.delete()
        line_list.clear()

        self.parent.delete(ALL)


    def scroll(self, event=None):
        self.clear()

        if self.scaling:
            self.scale += -1*(event.delta/12000000)/self.zoom_factor
        else:
            self.winx += -1*(event.delta/2)

        self.draw()

    def toggle_vertecies(self, event=None):
        if self.show_vertecies:
            self.show_vertecies = False
        else:
            self.show_vertecies = True
        self.clear()
        self.draw()

    def increase_zoom_factor(self, event=None):
        self.zoom_factor += 0.001
        self.clear()
        self.draw()

    def decrease_zoom_factor(self, event=None):
        self.zoom_factor -= 0.001
        self.clear()
        self.draw()



class Line():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y
        global line_list
        line_list.append(self)

    def create_line(self, color):
        try:
            index = line_list.index(self) + 1
            next_line = line_list[index]
            self.line = self.parent.create_line(self.x, self.y, next_line.x, next_line.y, fill=color)
        except:
            pass

    def delete(self):
        try:
            self.parent.delete(self.line)
            del self
        except:
            pass


root = GeoWindow()

root.mainloop()