import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PlotApp:
    """Class for plotting and animating cryptocurrency price movements."""

    def __init__(self, app, root_window, master, chosen_crypto, total_points, frame_display, profitengine=None):
        """Initialize the plot app with all the necessary parameters."""
        self.app = app
        self.profit_engine = profitengine
        self.root_window = root_window
        self.master = master
        self.chosen_crypto = chosen_crypto
        self.total_points = total_points
        self.current_index = 0
        self.plot_paused = True

        # Create figure and subplot
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Time in Days(days)")
        self.ax.set_ylabel(f"{chosen_crypto.name} prices($)")

        # Create initial x and y data
        self.x = np.linspace(1, self.total_points, self.total_points)
        self.y = np.full((self.total_points,), chosen_crypto.prices[0])

        # Plot initial data
        self.line, = self.ax.plot(self.x, self.y, 'r-')

        # Embed the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="NSEW")

        # Initialize button to start the simulation
        self.startsimulation_button = tk.Button(master, text="Start simulation", command=self.unpause_plot)
        self.startsimulation_button.grid(row=1, column=1)

        # Start the plot update loop
        self.update_plot()

    def pause_plot(self):
        """Pause the plot when called."""
        self.plot_paused = True

    def unpause_plot(self):
        """Unpause the plot when called."""
        if self.plot_paused:
            self.plot_paused = False
            self.update_plot()

    def update_plot(self):
        """Update the plot with new data points."""
        if not self.plot_paused:
            # Update data points here
            # Example: self.y = new_data_points()
            # Update plot
            self.line.set_ydata(self.y)
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()
            # Schedule the next update recursively
            self.master.after(1000, self.update_plot)
            
# app = PlotApp(app, root_window, master, chosen_crypto, total_points, frame_display, profitengine
