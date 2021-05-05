from tkinter import *
import tkinter.ttk as ttk
from math import *

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
            error = False
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
                y = 0
                error = True
                self.parent.create_text(400, 200, text=str(e) + " at x=" + str(x), font="Consolas 20")



            # setup code

            x = x / self.scale
            y = y / self.scale

            y = self.winy/2 - y
            x = x + self.winx/2

            self.x = x

            if self.show_vertecies:
                self.parent.create_rectangle(x-3, y-3, x+3, y+3, fill="orange", outline="")
            Line(self.parent, x, y, error=error)
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
    def __init__(self, parent, x, y, error=False):
        self.parent = parent
        self.x = x
        self.y = y
        self.error = error
        global line_list
        line_list.append(self)

    def create_line(self, color):
        try:
            index = line_list.index(self) + 1
            next_line = line_list[index]
            if not self.error and not next_line.error:
                self.line = self.parent.create_line(self.x, self.y, next_line.x, next_line.y, fill=color)
        except:
            pass

    def delete(self):
        try:
            self.parent.delete(self.line)
            del self
        except:
            pass