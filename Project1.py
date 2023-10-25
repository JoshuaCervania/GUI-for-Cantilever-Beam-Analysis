import tkinter as tk
import math

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cantilever Beam Analysis")
        self.inputs = GUI_inputs(self.root)
        self.outputs = GUI_outputs(self.root)
        self.calculations = Calculations(self.root, self.inputs, self.outputs)
        self.calculate_button = CalculateButton(self.root, self.calculations)

class GUI_inputs:
    def __init__(self, root):
        self.root = root
        self.cross_section()
        self.dimensions()
        self.point_loads()
        self.conc_moments()
        self.dist_load()
        self.poi()
        self.modulus()

    def cross_section(self):
        self.cross_section_frame = tk.LabelFrame(self.root, text="Cross Section")
        self.cross_section_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        self.cross_section_var = tk.StringVar()
        self.cross_section_var.set("Circular")

        self.circular_radio = tk.Radiobutton(self.cross_section_frame, text="Circular", variable=self.cross_section_var, value="Circular",
                                            command=self.update_dim)
        self.rectangular_radio = tk.Radiobutton(self.cross_section_frame, text="Rectangular", variable=self.cross_section_var,
                                               value="Rectangular", command=self.update_dim)

        self.circular_radio.grid(row=0, column=0)
        self.rectangular_radio.grid(row=0, column=1)

    def modulus(self):
        self.modulus_frame = tk.LabelFrame(self.root, text="Modulus of Elasticity")
        self.modulus_label = tk.Label(self.modulus_frame, text="E:")
        self.modulus_entry = tk.Entry(self.modulus_frame)
        self.modulus_entry.insert(0, 0)

        self.modulus_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.modulus_label.grid(row=0, column=0)
        self.modulus_entry.grid(row=0, column=1)

    def dimensions(self):
        self.dimensions_frame = tk.LabelFrame(self.root, text="Dimensions")
        self.d_label = tk.Label(self.dimensions_frame, text="Diameter:")
        self.d_entry = tk.Entry(self.dimensions_frame)
        self.d_entry.insert(0, 0)
        self.h_label = tk.Label(self.dimensions_frame, text="Height:")
        self.h_entry = tk.Entry(self.dimensions_frame)
        self.h_entry.insert(0, 0)
        self.w_label = tk.Label(self.dimensions_frame, text="Width:")
        self.w_entry = tk.Entry(self.dimensions_frame)
        self.w_entry.insert(0, 0)
        self.l_label = tk.Label(self.dimensions_frame, text="Length:")
        self.l_entry = tk.Entry(self.dimensions_frame)
        self.l_entry = tk.Entry(self.dimensions_frame)
        self.l_entry.insert(0, 0)
        self.update_button = tk.Button(self.dimensions_frame, text="Update Length", command=self.update_sliders)

        self.dimensions_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.d_label.grid(row=0, column=0)
        self.d_entry.grid(row=0, column=1)
        self.l_label.grid(row=1, column=0)
        self.l_entry.grid(row=1, column=1)
        self.update_button.grid(row=1, column=2)

    def update_dim(self):
        selection = self.cross_section_var.get()
        if selection == "Circular":
            self.h_label.grid_remove()
            self.h_entry.grid_remove()
            self.w_label.grid_remove()
            self.w_entry.grid_remove()
            self.d_label.grid(row=0, column=0)
            self.d_entry.grid(row=0, column=1)
            self.l_label.grid(row=1, column=0)
            self.l_entry.grid(row=1, column=1)
            self.update_button.grid(row=1, column=2)
        elif selection == "Rectangular":
            self.d_label.grid_remove()
            self.d_entry.grid_remove()
            self.h_label.grid(row=0, column=0)
            self.h_entry.grid(row=0, column=1)
            self.w_label.grid(row=1, column=0)
            self.w_entry.grid(row=1, column=1)
            self.l_label.grid(row=2, column=0)
            self.l_entry.grid(row=2, column=1)
            self.update_button.grid(row=2, column=2)

    def update_sliders(self):
        length_str = self.l_entry.get()

        if length_str.isdigit():
            self.length = int(length_str)

            self.a1_slider = tk.Scale(self.point_loads_frame, from_=0, to=self.length, orient="horizontal")
            self.a1_slider.grid(row=0, column=3)
            self.a2_slider = tk.Scale(self.point_loads_frame, from_=0, to=self.length, orient="horizontal")
            self.a2_slider.grid(row=1, column=3)
            self.a3_slider = tk.Scale(self.point_loads_frame, from_=0, to=self.length, orient="horizontal")
            self.a3_slider.grid(row=2, column=3)
            self.b1_slider = tk.Scale(self.conc_moments_frame, from_=0, to=self.length, orient="horizontal")
            self.b1_slider.grid(row=0, column=3)
            self.b2_slider = tk.Scale(self.conc_moments_frame, from_=0, to=self.length, orient="horizontal")
            self.b2_slider.grid(row=1, column=3)
            self.b3_slider = tk.Scale(self.conc_moments_frame, from_=0, to=self.length, orient="horizontal")
            self.b3_slider.grid(row=2, column=3)
            self.c1_slider = tk.Scale(self.dist_load_frame, from_=0, to=self.length, orient="horizontal")
            self.c1_slider.grid(row=0, column=3)
            self.c2_slider = tk.Scale(self.dist_load_frame, from_=0, to=self.length, orient="horizontal")
            self.c2_slider.grid(row=1, column=3)
            self.d1_slider = tk.Scale(self.poi_frame, from_=0, to=self.length, orient="horizontal")
            self.d1_slider.grid(row=0, column=1)

    def point_loads(self):
        self.point_loads_frame = tk.LabelFrame(self.root, text="Point Loads")
        self.P1_label = tk.Label(self.point_loads_frame, text="P1:")
        self.P1_entry = tk.Entry(self.point_loads_frame)
        self.P1_entry.insert(0, 0)
        self.a1_label = tk.Label(self.point_loads_frame, text="a1:")
        self.a1_slider = tk.Scale(self.point_loads_frame, from_=0, to=0, orient="horizontal")
        self.P2_label = tk.Label(self.point_loads_frame, text="P2:")
        self.P2_entry = tk.Entry(self.point_loads_frame)
        self.P2_entry.insert(0, 0)
        self.a2_label = tk.Label(self.point_loads_frame, text="a2:")
        self.a2_slider = tk.Scale(self.point_loads_frame, from_=0, to=0, orient="horizontal")
        self.P3_label = tk.Label(self.point_loads_frame, text="P3:")
        self.P3_entry = tk.Entry(self.point_loads_frame)
        self.P3_entry.insert(0, 0)
        self.a3_label = tk.Label(self.point_loads_frame, text="a3:")
        self.a3_slider = tk.Scale(self.point_loads_frame, from_=0, to=0, orient="horizontal")

        self.point_loads_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.P1_label.grid(row=0, column=0)
        self.P1_entry.grid(row=0, column=1)
        self.a1_label.grid(row=0, column=2)
        self.a1_slider.grid(row=0, column=3)
        self.P2_label.grid(row=1, column=0)
        self.P2_entry.grid(row=1, column=1)
        self.a2_label.grid(row=1, column=2)
        self.a2_slider.grid(row=1, column=3)
        self.P3_label.grid(row=2, column=0)
        self.P3_entry.grid(row=2, column=1)
        self.a3_label.grid(row=2, column=2)
        self.a3_slider.grid(row=2, column=3)

    def conc_moments(self):
        self.conc_moments_frame = tk.LabelFrame(self.root, text="Concentrated Moments")
        self.M1_label = tk.Label(self.conc_moments_frame, text="M1:")
        self.M1_entry = tk.Entry(self.conc_moments_frame)
        self.M1_entry.insert(0, 0)
        self.b1_label = tk.Label(self.conc_moments_frame, text="b1:")
        self.b1_slider = tk.Scale(self.conc_moments_frame, from_=0, to=0, orient="horizontal")
        self.M2_label = tk.Label(self.conc_moments_frame, text="M2:")
        self.M2_entry = tk.Entry(self.conc_moments_frame)
        self.M2_entry.insert(0, 0)
        self.b2_label = tk.Label(self.conc_moments_frame, text="b2:")
        self.b2_slider = tk.Scale(self.conc_moments_frame, from_=0, to=0, orient="horizontal")
        self.M3_label = tk.Label(self.conc_moments_frame, text="M3:")
        self.M3_entry = tk.Entry(self.conc_moments_frame)
        self.M3_entry.insert(0, 0)
        self.b3_label = tk.Label(self.conc_moments_frame, text="b3:")
        self.b3_slider = tk.Scale(self.conc_moments_frame, from_=0, to=0, orient="horizontal")

        self.conc_moments_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.M1_label.grid(row=0, column=0)
        self.M1_entry.grid(row=0, column=1)
        self.b1_label.grid(row=0, column=2)
        self.b1_slider.grid(row=0, column=3)
        self.M2_label.grid(row=1, column=0)
        self.M2_entry.grid(row=1, column=1)
        self.b2_label.grid(row=1, column=2)
        self.b2_slider.grid(row=1, column=3)
        self.M3_label.grid(row=2, column=0)
        self.M3_entry.grid(row=2, column=1)
        self.b3_label.grid(row=2, column=2)
        self.b3_slider.grid(row=2, column=3)

    def dist_load(self):
        self.dist_load_frame = tk.LabelFrame(self.root, text="Distributed Load")
        self.w1_label = tk.Label(self.dist_load_frame, text="W1:")
        self.w1_entry = tk.Entry(self.dist_load_frame)
        self.w1_entry.insert(0, 0)
        self.c1_label = tk.Label(self.dist_load_frame, text="c1:")
        self.c1_slider = tk.Scale(self.dist_load_frame, from_=0, to=0, orient="horizontal")
        self.c2_label = tk.Label(self.dist_load_frame, text="c2:")
        self.c2_slider = tk.Scale(self.dist_load_frame, from_=0, to=0, orient="horizontal")

        self.dist_load_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.w1_label.grid(row=0, column=0)
        self.w1_entry.grid(row=0, column=1)
        self.c1_label.grid(row=0, column=2)
        self.c1_slider.grid(row=0, column=3)
        self.c2_label.grid(row=1, column=2)
        self.c2_slider.grid(row=1, column=3)

    def poi(self):
        self.poi_frame = tk.LabelFrame(self.root, text="Point of Interest")
        self.d1_label = tk.Label(self.poi_frame, text="d1:")
        self.d1_slider = tk.Scale(self.poi_frame, from_=0, to=0, orient="horizontal")

        self.poi_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        self.d1_label.grid(row=0, column=0)
        self.d1_slider.grid(row=0, column=1)

class GUI_outputs:
    def __init__(self, root):
        self.root = root
        self.cs_area()
        self.shear_moment()
        self.crit_stress()
        self.max_deflection()

    def cs_area(self):
        self.cs_area_frame = tk.LabelFrame(self.root, text="Cross Sectional Area")
        self.cs_area_label = tk.Label(self.cs_area_frame, text="Area:")
        self.cs_area_entry = tk.Entry(self.cs_area_frame)

        self.cs_area_frame.grid(row=2, column=3, columnspan=3, padx=10, pady=10, sticky="w")
        self.cs_area_label.grid(row=0, column=0)
        self.cs_area_entry.grid(row=0, column=1)

    def shear_moment(self):
        self.shear_moment_frame = tk.LabelFrame(self.root, text="Shear and Moment @ POI")
        self.shear_label = tk.Label(self.shear_moment_frame, text="Shear:")
        self.shear_entry = tk.Entry(self.shear_moment_frame)
        self.moment_label = tk.Label(self.shear_moment_frame, text="Moment:")
        self.moment_entry = tk.Entry(self.shear_moment_frame)

        self.shear_moment_frame.grid(row=3, column=3, columnspan=3, padx=10, pady=10, sticky="w")
        self.shear_label.grid(row=0, column=0)
        self.shear_entry.grid(row=0, column=1)
        self.moment_label.grid(row=1, column=0)
        self.moment_entry.grid(row=1, column=1)

    def crit_stress(self):
        self.crit_stress_frame = tk.LabelFrame(self.root, text="Critical Stress")
        self.crit_stress_label = tk.Label(self.crit_stress_frame, text="Stress:")
        self.crit_stress_entry = tk.Entry(self.crit_stress_frame)

        self.crit_stress_frame.grid(row=4, column=3, columnspan=3, padx=10, pady=10, sticky="w")
        self.crit_stress_label.grid(row=0, column=0)
        self.crit_stress_entry.grid(row=0, column=1)

    def max_deflection(self):
        self.max_deflection_frame = tk.LabelFrame(self.root, text="Max Deflection")
        self.max_deflection_label = tk.Label(self.max_deflection_frame, text="Deflection:")
        self.max_deflection_entry = tk.Entry(self.max_deflection_frame)

        self.max_deflection_frame.grid(row=5, column=3, columnspan=3, padx=10, pady=10, sticky="w")
        self.max_deflection_label.grid(row=0, column=0)
        self.max_deflection_entry.grid(row=0, column=1)


class CalculateButton:
    def __init__(self, root, calculations):
        self.root = root
        self.calculations = calculations
        self.calculate_button = tk.Button(root, text="Calculate", command=self.update_outputs)
        self.calculate_button.grid(row=6, column=3, columnspan=3, padx=10, pady=10, sticky="w")

    def update_outputs(self):
        self.calculations.calculate_area()
        self.calculations.calculate_shear()
        self.calculations.calculate_moment()
        self.calculations.calculate_stress()
        self.calculations.calculate_deflection()

class Calculations:
    def __init__(self, root, inputs, outputs):
        self.root = root
        self.inputs = inputs
        self.outputs = outputs

    def calculate_area(self):
        cross_section_type = self.inputs.cross_section_var.get()
        if cross_section_type == "Circular":
            diameter = float(self.inputs.d_entry.get())
            area = math.pi * (diameter/2) ** 2
        elif cross_section_type == "Rectangular":
            height = float(self.inputs.h_entry.get())
            width = float(self.inputs.w_entry.get())
            area = height * width
        else:
            area = 0

        self.outputs.cs_area_entry.delete(0, tk.END)
        self.outputs.cs_area_entry.insert(0, str(area))

    def calculate_shear(self):
        if self.inputs.c1_slider.get() >= self.inputs.d1_slider.get() and self.inputs.c2_slider.get() >= self.inputs.d1_slider.get():
            disLoad = float(self.inputs.w1_entry.get())
            Coverage = float(self.inputs.c2_slider.get() - self.inputs.c1_slider.get())
            W = disLoad*Coverage
        elif self.inputs.c2_slider.get() >= self.inputs.d1_slider.get():
            disLoad = float(self.inputs.w1_entry.get())
            Coverage = float(self.inputs.c2_slider.get() - self.inputs.d1_slider.get())
            W = float(disLoad * Coverage)
        else:
            W = 0

        if self.inputs.a1_slider.get() >= self.inputs.d1_slider.get():
            P1 = float(self.inputs.P1_entry.get())
        else:
            P1 = 0

        if self.inputs.a2_slider.get() >= self.inputs.d1_slider.get():
            P2 = float(self.inputs.P2_entry.get())
        else:
            P2 = 0

        if self.inputs.a3_slider.get() >= self.inputs.d1_slider.get():
            P3 = float(self.inputs.P3_entry.get())
        else:
            P3 = 0

        Shear = float(W + P1 + P2 + P3)

        self.outputs.shear_entry.delete(0, tk.END)
        self.outputs.shear_entry.insert(0, str(Shear))

    def calculate_moment(self):
        if self.inputs.c1_slider.get() >= self.inputs.d1_slider.get() and self.inputs.c2_slider.get() >= self.inputs.d1_slider.get():
            disLoad = float(self.inputs.w1_entry.get())
            Coverage = float(self.inputs.c2_slider.get() - self.inputs.c1_slider.get())
            W = disLoad*Coverage
            dx = float((self.inputs.c2_slider.get()+self.inputs.c1_slider.get())/2)
            m7 = float(W*dx)
        elif self.inputs.c2_slider.get() >= self.inputs.d1_slider.get():
            disLoad = float(self.inputs.w1_entry.get())
            Coverage = float(self.inputs.c2_slider.get() - self.inputs.d1_slider.get())
            W = float(disLoad * Coverage)
            dx = float((self.inputs.d1_slider.get() + self.inputs.c2_slider.get()) / 2)
            m7 = float(W * dx)
        else:
            W = 0
            m7 = 0

        if self.inputs.a1_slider.get() >= self.inputs.d1_slider.get():
            P1 = float(self.inputs.P1_entry.get())
            m4 = float(P1*self.inputs.a1_slider.get())
        else:
            P1 = 0
            m4 = 0

        if self.inputs.a2_slider.get() >= self.inputs.d1_slider.get():
            P2 = float(self.inputs.P2_entry.get())
            m5 = float(P2 * self.inputs.a2_slider.get())
        else:
            P2 = 0
            m5 = 0

        if self.inputs.a3_slider.get() >= self.inputs.d1_slider.get():
            P3 = float(self.inputs.P3_entry.get())
            m6 = float(P3 * self.inputs.a3_slider.get())
        else:
            P3 = 0
            m6 = 0

        if self.inputs.b1_slider.get() >= self.inputs.d1_slider.get():
            m1 = float(self.inputs.M1_entry.get())
        else:
            m1 = 0

        if self.inputs.b2_slider.get() >= self.inputs.d1_slider.get():
            m2 = float(self.inputs.M2_entry.get())
        else:
            m2 = 0

        if self.inputs.b3_slider.get() >= self.inputs.d1_slider.get():
            m3 = float(self.inputs.M3_entry.get())
        else:
            m3 = 0

        Moment = float(m1 + m2 + m3 + m4 + m5 + m6 + m7)
        self.outputs.moment_entry.delete(0, tk.END)
        self.outputs.moment_entry.insert(0, str(Moment))

    def calculate_stress(self):
        cross_section_type = self.inputs.cross_section_var.get()
        if cross_section_type == "Circular":
            diameter = float(self.inputs.d_entry.get())
            yy = diameter/2
            ix = (math.pi * (diameter ** 4) / 64)
        elif cross_section_type == "Rectangular":
            height = float(self.inputs.h_entry.get())
            width = float(self.inputs.w_entry.get())
            yy = height/2
            ix = (width * (height ** 3)) / 12
        else:
            ix = 0

        disLoad = float(self.inputs.w1_entry.get())
        Coverage = float(self.inputs.c2_slider.get() - self.inputs.c1_slider.get())
        W = disLoad * Coverage
        dx = float((self.inputs.c2_slider.get() + self.inputs.c1_slider.get()) / 2)
        m7 = float(W * dx)

        P1 = float(self.inputs.P1_entry.get())
        m4 = float(P1 * self.inputs.a1_slider.get())

        P2 = float(self.inputs.P2_entry.get())
        m5 = float(P2 * self.inputs.a2_slider.get())

        P3 = float(self.inputs.P3_entry.get())
        m6 = float(P3 * self.inputs.a3_slider.get())

        m1 = float(self.inputs.M1_entry.get())

        m2 = float(self.inputs.M2_entry.get())

        m3 = float(self.inputs.M3_entry.get())

        M = float(m1 + m2 + m3 + m4 + m5 + m6 + m7)

        stress = ((yy) * M) / ix

        self.outputs.crit_stress_entry.delete(0, tk.END)
        self.outputs.crit_stress_entry.insert(0, str(stress))

    def calculate_deflection(self):
        cross_section_type = self.inputs.cross_section_var.get()
        if cross_section_type == "Circular":
            diameter = float(self.inputs.d_entry.get())
            yy = float(diameter/2)
            ix = float(math.pi * (diameter ** 4) / 64)
        elif cross_section_type == "Rectangular":
            height = float(self.inputs.h_entry.get())
            width = float(self.inputs.w_entry.get())
            yy = float(height/2)
            ix = float((width * (height ** 3)) / 12)
        else:
            ix = 0

        if not self.inputs.P1_entry.get() == 0:
            k1 = (int(self.inputs.P1_entry.get()) * (int(self.inputs.a1_slider.get() ** 2))) * (3 * int(self.inputs.l_entry.get()))
            q1 = float((6 * int(self.inputs.modulus_entry.get()) * ix))
            def1 = float((k1 - self.inputs.a1_slider.get()) / q1)
        else:
            def1 = 0

        if not self.inputs.P2_entry.get() == 0:
            k2 = (int(self.inputs.P2_entry.get()) * (int(self.inputs.a2_slider.get() ** 2))) * (3 * int(self.inputs.l_entry.get()))
            q2 = float((6 * int(self.inputs.modulus_entry.get()) * ix))
            def2 = float((k2 - self.inputs.a2_slider.get()) / q2)
        else:
            def2 = 0

        if not self.inputs.P3_entry.get() == 0:
            k3 = (int(self.inputs.P3_entry.get()) * (int(self.inputs.a3_slider.get() ** 2))) * (3 * int(self.inputs.l_entry.get()))
            q3 = float((6 * int(self.inputs.modulus_entry.get()) * ix))
            def3 = float((k3 - self.inputs.a3_slider.get()) / q3)
        else:
            def3 = 0

        if not self.inputs.M1_entry.get() == 0:
            def4 = float((int(self.inputs.M1_entry.get()) * int((self.inputs.b1_slider.get()) ** 2)) / (2 * int(self.inputs.modulus_entry.get()) * ix))
        else:
            def4 = 0

        if not self.inputs.M2_entry.get() == 0:
            def5 = float((int(self.inputs.M2_entry.get()) * int((self.inputs.b2_slider.get()) ** 2)) / (2 * int(self.inputs.modulus_entry.get()) * ix))
        else:
            def5 = 0

        if not self.inputs.M3_entry.get() == 0:
            def6 = float((int(self.inputs.M3_entry.get()) * int((self.inputs.b3_slider.get()) ** 2)) / (2 * int(self.inputs.modulus_entry.get()) * ix))
        else:
            def6 = 0

        if not self.inputs.w1_entry.get() == 0:
            disLoad = float(self.inputs.w1_entry.get())
            Coverage = float(self.inputs.c2_slider.get() - self.inputs.c1_slider.get())
            W = disLoad * Coverage
            K = float(W / (24 * int(self.inputs.modulus_entry.get()) * ix))
            P = float(4 * int(self.inputs.l_entry.get()) * (int((self.inputs.c2_slider.get()) ** 3) - (int(self.inputs.c1_slider.get()) ** 3)))
            Q = float((self.inputs.c2_slider.get() ** 4) - (self.inputs.c1_slider.get() ** 4))
            def7 = float(K * (P - Q))
        else:
            def7 = 0

        deflection = float(def1 + def2 + def3 + def4 + def5 + def6 + def7)


        self.outputs.max_deflection_entry.delete(0, tk.END)
        self.outputs.max_deflection_entry.insert(0, str(deflection))

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()