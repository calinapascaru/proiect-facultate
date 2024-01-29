import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TemperatureControlApp:
    def __init__(self, master):
        self.master = master
        master.title("Interactive Temperature Control System")

        # Initializare variabile
        self.desired_temperature = tk.DoubleVar(value=25.0)
        self.current_temperature = tk.DoubleVar(value=25.0)
        self.adjustment_step_size = tk.DoubleVar(value=0.1)
        self.iteration_count = 0

        # Creeaza elem. GUI//incepem sa facem butoanele
        self.create_widgets()

        # Creeaza o figura pt graficul temp
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky=tk.NSEW)

        # Param.simulare
        self.simulation_interval = 1000  # Update every 1 second
        self.simulation_running = False


        # Initializare grafic
        self.update_graph()

    def create_widgets(self):
        # Scale si nume pt setarea temp dorite
        ttk.Label(self.master, text="Desired Temperature:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Scale(self.master, from_=10.0, to=30.0, orient=tk.HORIZONTAL, variable=self.desired_temperature,
                  command=self.update_desired_temperature, length=200).grid(row=0, column=1, padx=10, pady=10,
                                                                            sticky=tk.W)

        # Afisare temp actuala
        ttk.Label(self.master, text="Current Temperature:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self.master, textvariable=self.current_temperature, width=10).grid(row=1, column=1, padx=10, pady=10,
                                                                                     sticky=tk.W)

        # Buton pt ajustare temp
        ttk.Button(self.master, text="Adjust Temperature", command=self.adjust_temperature).grid(row=2, column=0,
                                                                                                 columnspan=2, pady=10)

        # Label si entry box pt setare si afisare temperatura dorita
        ttk.Label(self.master, text="Desired Temperature:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.desired_temp_entry = ttk.Entry(self.master, textvariable=self.desired_temperature, width=8)
        self.desired_temp_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        ttk.Button(self.master, text="Set Desired Temperature", command=self.set_desired_temperature).grid(row=3,
                                                                                                           column=2,
                                                                                                           padx=10,
                                                                                                           pady=10,
                                                                                                           sticky=tk.W)

        # Buton pt resetare la default settings
        ttk.Button(self.master, text="Default Settings", command=self.reset_to_default).grid(row=5, column=0,
                                                                                             columnspan=2, pady=10)
        # Buton pentru ajustare temp
        ttk.Button(self.master, text="Adjust Temperature", command=self.adjust_temperature).grid(row=2, column=0,
                                                                                                 columnspan=2, pady=10)
        # Eticheta and scale pentru setare buton adjustment step size
        ttk.Label(self.master, text="Adjustment Step Size:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Scale(self.master, from_=0.1, to=1.0, orient=tk.HORIZONTAL, variable=self.adjustment_step_size,
                  command=self.update_step_size, length=200).grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

    def reset_to_default(self):
        # Reseteaza toate setarile la default value
        self.desired_temperature.set(25.0)
        self.current_temperature.set(25.0)
        self.simulation_interval = 1000
        self.simulation_running = False
        self.update_graph()
        messagebox.showinfo("Temperature Control", "Settings reset to default values.")

    def update_step_size(self, value):
        # Updateaza adjustment step size
        self.adjustment_step_size.set(round(float(value), 1))

    def update_desired_temperature(self, value):
        # Updateaza temperatura dorita si rescrie graficul
        self.desired_temperature.set(round(float(value) * 2) / 2)  # Round to nearest 0.5
        self.update_graph()

    def update_graph(self):
        # Updateaza graficul bazat pe temp actuala si cea dorita
        self.ax.clear()
        self.ax.plot([1, 2], [self.current_temperature.get(), self.desired_temperature.get()], marker='o')
        self.ax.set_title('Temperature Control Simulation')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Temperature (°C)')
        self.canvas.draw()

    def adjust_temperature(self):
        # Incepe sau opreste simularea bazata pe click
        if not self.simulation_running:
            self.simulation_running = True
            self.iteration_count = 0  # Reset iteration count
            self.simulate_temperature_control()

    def set_desired_temperature(self):
        # Seteaza temp dorita in functie de entry box
        try:
            new_desired_temp = round(float(self.desired_temp_entry.get()) * 2) / 2  # Round to nearest 0.5
            self.desired_temperature.set(new_desired_temp)
            messagebox.showinfo("Temperature Control", f"Desired temperature set to {new_desired_temp:.1f}°C")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

        self.update_graph()

    def simulate_temperature_control(self):
        # Simuleaza controlul temperaturii si updateaza graficul
        step = self.adjustment_step_size.get()
        self.iteration_count += 1

        if self.current_temperature.get() < self.desired_temperature.get():
            # daca temp curenta este mai mica, creste-o pana la temp dorita
            self.current_temperature.set(
                min(round(self.current_temperature.get() + step, 1), self.desired_temperature.get()))
        elif self.current_temperature.get() > self.desired_temperature.get():
            # daca temp curenta este mai mare, descreste-o pana la temp dorita
            self.current_temperature.set(
                max(round(self.current_temperature.get() - step, 1), self.desired_temperature.get()))

        self.update_graph()

        if self.current_temperature.get() == self.desired_temperature.get():
            # daca temp se potriveste, opreste simularea
            self.simulation_running = False
            messagebox.showinfo("Temperature Control", f"Temperature stabilized in {self.iteration_count} iterations.")
        elif self.simulation_running:
            self.master.after(self.simulation_interval, self.simulate_temperature_control)

def run_temperature_control_app():
    root = tk.Tk()
    app = TemperatureControlApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_temperature_control_app()
