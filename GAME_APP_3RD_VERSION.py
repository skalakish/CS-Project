import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import sqlite3
import hashlib
import random
import heapq
# Global list to store instances of cryptocurrencies
global cryptolist
cryptolist = []

# Class to Model a cryptocurrency:
class CryptoCurrency():
    def __init__(self, name, startprice, drift, volatility, N , jump_chance, jump_magnitude) -> None:
        # Initialize attributes of the cryptocurrency
        self.startprice = startprice
        self.drift = drift
        self.volatility = volatility
        self.simulation_no = N
        self.jump_chance = jump_chance
        self.jump_magnitude = jump_magnitude
        self.name = name
        self.prices = []
# Method to simulate profit fluctuations in th crypto currency
    def simulation_engine(self):
        prices = [self.startprice]
        volatility = self.volatility

        for _ in range(1, self.simulation_no):
            # Random walk
            dt = 1  # Assuming each step is one time unit
            random_change = np.random.normal(self.drift * dt, volatility * np.sqrt(dt))
            
            # Volatility clustering
            recent_change = np.log(prices[-1] / prices[-2]) if len(prices) > 1 else 0
            volatility = volatility * 0.9 + 0.1 * abs(recent_change)  # Example of EWMA

            # Jump logic
            if np.random.rand() < self.jump_chance:
                jump = np.random.normal(0, self.jump_magnitude)
            else:
                jump = 0

            new_price = prices[-1] * np.exp(random_change + jump)
            prices.append(new_price)

        self.prices = prices
# Method to get the next price in simulated data
    def get_next_price(self, index):
        if index < len(self.prices) :
            return self.prices[index]
        return None
# Class to manage plotting the cryptocurrency prices    
class PlotApp():
    def __init__(self, app, root_window, master, chosen_crypto, total_points,  frame_display, profitengine = None):
        self.app = app
        self.profit_engine  = ProfitEngine(frame_display, self)
        self.root_window = root_window
        self.master = master
        self.chosen_crypto = chosen_crypto
        self.total_points = total_points
        self.current_index = 0

        self.plot_paused = True

        # Create a figure and a plot element
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.x = np.linspace(1, self.total_points , self.total_points)
        self.y = np.full((365,), chosen_crypto.prices[0])  # Start with all zeros
        

        self.line, = self.ax.plot(self.x, self.y, 'r-')  # Red line

        # Embed the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column=0, sticky = "NSEW")

#Button to pause / unpause simulation
        self.unpause_button = tk.Button(master, text="Start simulation", command=self.unpause_plot)
        self.unpause_button.grid(row = 1, column=1)

        self.update_plot()  # Start the plot update loop
# Method to pause the plot
    def pause_plot(self):
        self.plot_paused = True
# Method to unpause the plot and start simulation
    def unpause_plot(self):
        if self.plot_paused == True:
            self.plot_paused = False
            self.update_plot()
# Method to update the plot with new data points
    def update_plot(self):
        global current_price
        if not self.plot_paused and self.current_index < self.total_points:
            new_data = self.chosen_crypto.get_next_price(self.current_index)
            if new_data is not None:
                buffer = 100
                self.y[self.current_index] = new_data
                current_price = new_data
                self.current_index += 1
                self.line.set_ydata(self.y)
                self.ax.set_ylim(min(self.y) - buffer, max(self.y) + buffer)
                self.canvas.draw()

          # Call the update_heaps method of profit_engine to update heaps
                self.profit_engine.update_heaps(new_data)
 # Schedule the update_plot method to be called again after 100ms
            self.master.after(100, self.update_plot)
        elif self.current_index == self.total_points:
  # If simulation is completed, calculate game result
            self.profit_engine.calculate_game_result(self.app)

# Class to manage financial aspects of the game
class ProfitEngine():
    def __init__(self, frame, graphplotter) -> None:
# Initialize profit engine with required attributes
        self.graph_plotter = graphplotter
        self.min_heap = []  # Min heap to track minimum prices
        self.max_heap = []  # Max heap to track maximum prices

        self.capital = tk.DoubleVar(value=10000) # Variable to track capital
        self.capital_for_checking = 10000  # Initial capital for checking

        self.investment_quantity = tk.DoubleVar(value=0) # Variable to track investment quantity

        self.gains = tk.DoubleVar(value=0)# Variable to track gains
# Buttons for buying and selling
        self.buy_button = tk.Button(frame, text="BUY", command=self.invest)
        self.buy_button.grid(column=0, row=1, columnspan=2)

        self.sell_button = tk.Button(frame, text="SELL", command=self.sell)
        self.sell_button.grid(column=0, row=2, columnspan=2)
# Label to display gains, capital and investment amount
        self.gains_display = tk.Label(frame, text="GAINS", font=("Roboto", 12), fg="white", bg="#263238")
        self.gains_display.grid(column=0, row=3)

        self.gains_display = tk.Label(frame, text="GAINS", textvariable=self.gains, font=("Roboto", 12), fg="white",
                                      bg="#263238")
        self.gains_display.grid(column=1, row=3)

        self.capital_display = tk.Label(frame, text="CAPITAL", font=("Roboto", 12), fg="white", bg="#263238")
        self.capital_display.grid(column=0, row=4)

        self.capital_display = tk.Label(frame, text="CAPITAL", textvariable=self.capital, font=("Roboto", 12),
                                        fg="white", bg="#263238")
        self.capital_display.grid(column=1, row=4) 

        self.investment_amount_display = tk.Label(frame, text="INVESTMENT AMOUNT", font=("Roboto", 12), fg="white",
                                                  bg="#263238")
        self.investment_amount_display.grid(column=0, row=5)

        self.investment_amount_display = tk.Label(frame, text="INVESTMENT AMOUNT", textvariable=self.investment_quantity,
                                                  font=("Roboto", 12), fg="white", bg="#263238")
        self.investment_amount_display.grid(column=1, row=5)

        self.game_over = False # Flag to indicate game over state
        
# Method to handle monetary input for investment
    def handle_monetary_input_invest(self): # this needs to be implemented in line with the GUI
        while True:
            try:
                money = float(simpledialog.askfloat("Input", "How much do you want to invest"))
            except:
                messagebox.showerror("Error", "Input a real number")
                return None
            if money > self.capital.get():
                messagebox.showerror("Error", "You cannot spend morre than you own")
                continue
            else:
                return money
            
 # Method to handle quantity input for selling
    def handle_quantity_input_sell(self): # this needs to be implemented in line with the GUI
        while True:
            try:
                quantity = float(simpledialog.askfloat("Input", "How much do you want to sell"))
            except:
                messagebox.showerror("Error", "Input a real number")
                return None
            if quantity > self.investment_quantity.get():
                messagebox.showerror("Error", " Oops! You cannot sell more than you have")
                continue
            else:
                return quantity

 
    # Method to invest in cryptocurrency
    def invest(self):
        try:
            if current_price:
                self.graph_plotter.pause_plot()
                investment_amount = self.handle_monetary_input_invest()
                if investment_amount:
                    if investment_amount > 0:
                        new_capital = self.capital.get() - investment_amount
                        self.capital.set(new_capital)
                        
                        new_quantity =   self.investment_quantity.get()  +  (investment_amount / current_price)
                        self.investment_quantity.set(new_quantity)
                        self.graph_plotter.unpause_plot()

                    else:
                        messagebox.showerror("Error", "You cannot invest zero")
        except NameError:
            messagebox.showerror("Error", "You must start the simulation before trading")


# Method to sell cryptocurrency
    def sell(self):
        try:
            if current_price:
                self.graph_plotter.pause_plot()
                quantity_to_sell = self.handle_quantity_input_sell()
                if quantity_to_sell:
                    if quantity_to_sell > 0:
                        new_gains = self.gains.get() + (current_price * quantity_to_sell)
                        self.gains.set(new_gains)
                        new_quantity = self.investment_quantity.get() - quantity_to_sell
                        self.investment_quantity.set(new_quantity)
                        self.graph_plotter.unpause_plot()
                    
                    else:
                        messagebox.showerror("Error", "You cannot sell zero")
        except NameError:
            messagebox.showerror("Error", "You must start the simulation before trading")
   # Method to sell cryptocurrency for checking winning condition
    def sell_for_checking_winning_condition(self):
        try:
            if current_price:
                quantity_to_sell = self.investment_quantity.get()
                if quantity_to_sell:
                    if quantity_to_sell > 0:
                        new_gains = self.gains.get() + (current_price * quantity_to_sell)
                        self.gains.set(new_gains)

                        new_quantity = self.investment_quantity.get() - quantity_to_sell
                        self.investment_quantity.set(new_quantity)
                    
        except NameError:
            messagebox.showerror("Error", "You must start the simulation before trading")

 # Method to update heaps with new price
    def update_heaps(self, price):
        heapq.heappush(self.min_heap, price)  # Push price to min heap
        heapq.heappush(self.max_heap, -price)  # Push negative price to max heap (to simulate max heap behavior)
 # Method to calculate game result
    def calculate_game_result(self, app):
        self.sell_for_checking_winning_condition()
        current_capital  = self.capital.get() + self.gains.get()
        if current_capital > self.capital_for_checking:
            messagebox.showinfo("Information", "Congrats!!!  You won")
        else:
            messagebox.showinfo("Information", "Sorry, You lost, better luck next time")
        app.statistics_window(self.gains.get())

        

bitcoin = CryptoCurrency(
    startprice=2000,     # Starting price of Bitcoin
    drift=0.0002,         # Daily percentage drift
    volatility=0.01,      # Daily volatility
    N=365,               # Number of simulations
    jump_chance=0.05,     # Chance of a price jump occurring
    jump_magnitude=0.005,    # Magnitude of the price jump
    name = "Bitcoin"
)

# Instance for Ethereum
ethereum = CryptoCurrency(
    startprice=1500,      # Starting price of Ethereum
    drift=0.0003,         # Daily percentage drift
    volatility=0.02,      # Daily volatility
    N=365,               # Number of simulations
    jump_chance=0.05,     # Chance of a price jump occurring
    jump_magnitude=0.005,   # Magnitude of the price jump
    name = "Ethereum"
)

# Instance for Ripple
litecoin = CryptoCurrency(
    startprice=1000,       # Starting price of Ripple
    drift=0.0004,         # Daily percentage drift
    volatility=0.005,     # Daily volatility
    N=365,               # Number of simulations
    jump_chance=0.05,     # Chance of a price jump occurring
    jump_magnitude=0.005,    # Magnitude of the price jump
    name = "Litecoin"
)


#initialize all the data for the cryptocurrencies
bitcoin.simulation_engine()
litecoin.simulation_engine()
ethereum.simulation_engine()

cryptolist.append(litecoin)
cryptolist.append(bitcoin)
cryptolist.append(ethereum)

# Class to handle user authentication and registratio
class Login_handler():
    def __init__(self, app) -> None:
         # Initialize login handler with required attributes
        self.app = app
        #self.login_status = False
        self.conn = sqlite3.connect('user_credentials.db')
        self.cursor = self.conn.cursor()

 # Create users table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        self.conn.commit()
            
  # Method to hash the password
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

# Method to verify login credentials
    def verify_login(self, username, password):
        hashed_password = self.hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        return self.cursor.fetchone() is not None

 # Method to register a new user
    def register(self, username, password):
        hashed_password = self.hash_password(password)
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        self.conn.commit()
 # Method to handle user login
    def login(self, username, password, loadingscreen):
        loadingscreen = loadingscreen
        username = username
        password = password
        if self.verify_login(username, password): 
            messagebox.showinfo("Login Successful", "Welcome back, {}!".format(username))
            loadingscreen.destroy()
            self.app.loading_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
   # Method to register a new account          
    def register_account(self, username, password):
        username = username
        password = password
        if username and password:
            self.register(username, password)
            messagebox.showinfo("Registration Successful", "Account registered successfully!")
        else:
            messagebox.showerror("Registration Failed", "Please enter both username and password")
            pass




# Main application class

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.geometry("500x350")
        #self.title("Crypto Market Simulator")
        #self.configure(bg="#263238")
        self.login_handler = Login_handler(self)
        self.plot_paused = False
        self.withdraw()
        self.appsequence()
# Method to sequence the application
    def appsequence(self):
        self.login_screen()
   # Method to display login screen       
    def login_screen(self):
        login_window = tk.Toplevel(self)
        login_window.configure(bg="#263238")
        login_window.title("Login Screen")

        frame = tk.Frame(login_window, bg="#263238")
        frame.pack(pady=20, padx=60)

        label = tk.Label(frame, text="Login System", font=("Roboto", 24), fg="white", bg="#263238")
        label.pack(pady=12)

        frame_text_holders = tk.Frame(login_window, bg="#263238")
        frame_text_holders.pack()

        label_name = tk.Label(frame_text_holders, text = "Name ", font=("Roboto", 12), fg="white", bg="#263238")
        label_name.grid(row = 0, column = 0)


        entry1 = ttk.Entry(frame_text_holders)
        entry1.config(font=("Roboto", 12))
        entry1.grid(row = 0, column = 1)

        label_password = tk.Label(frame_text_holders, text = "Password ", font=("Roboto", 12), fg="white", bg="#263238")
        label_password.grid(row = 1, column = 0)

        

        entry2 = ttk.Entry(frame_text_holders, show="*")
        entry2.config(font=("Roboto", 12))
        entry2.grid(row = 1, column = 1)
        


        login_button = ttk.Button(frame, text="Login", command = lambda: self.login_handler.login(entry1.get(), entry2.get(), login_window))
        login_button.pack(pady=6)
  
        register_button = ttk.Button(frame, text="Register", command=lambda: self.login_handler.register_account(entry1.get(), entry2.get()))
        register_button.pack(pady=6)
    # Method to transition to loading window
    def transition_to_main(self, loading_window):
        loading_window.destroy()
        self.choose_crypto()
    # Method to create the loading screen      
    def loading_screen(self):
        loading_window = tk.Toplevel(self)
        loading_window.geometry("300x150")
        loading_window.title("Loading...")
        loading_window.resizable(False, False)

        label = tk.Label(loading_window, text="Loading, please wait...", font=("Roboto", 12))
        label.pack(pady=20)

        progressbar = ttk.Progressbar(loading_window, mode="indeterminate")
        progressbar.pack(pady=10)
        progressbar.start()

        loading_window.after(1000, lambda: self.transition_to_main(loading_window))
# Method to choose the cryptocurrency
    def choose_crypto(self):
        choice_window = tk.Toplevel(self)

        choice_label = tk.Label(choice_window, text="Choose a Crypto Currency", font=("Roboto", 24), fg="white", bg="#263238")
        choice_label.pack(pady=20)

        bitcoin_button = tk.Button(choice_window, text="BITCOIN", command=lambda: self.make_choice("Bitcoin", choice_window))
        bitcoin_button.pack()

        ethereum_button = tk.Button(choice_window, text="ETHEREUM", command=lambda: self.make_choice("Ethereum", choice_window))
        ethereum_button.pack()

        litecoin_button = tk.Button(choice_window, text="LITECOIN", command=lambda: self.make_choice("Litecoin", choice_window))
        litecoin_button.pack()

    # Method to didplay dialog box of choice made
    def make_choice(self, choice, window):
        global Crypto
        messagebox.showinfo("Choice", f"You chose {choice}")
        for cryptocurr in cryptolist:
            if cryptocurr.name == choice:
                Crypto = cryptocurr
                window.destroy()
                self.main_window()

#Method to End the game
    def end_game(self):
        self.destroy()
        

# Method to create and display the main window of the application
    def main_window(self):
     # Create a new top-level window
        main_window = tk.Toplevel(self)
    # Maximize the window
        main_window.state("zoomed")
     # Set the title of the window
        main_window.title("Main Window")
     # Set the background color of the window
        main_window.configure(bg="#263238")
       # Configure column 0 to resize with the window
        main_window.columnconfigure(0, weight =1)
  # Configure row 1 to resize with the window
        main_window.rowconfigure(1, weight =1)
        
# Create a frame to display information
        
        frame_display = tk.Frame(main_window, bg="#113238")
        frame_display.grid(column = 1, row =1 , sticky="NSEW")
        
 # Create a frame to display the graph
        frame_graph = tk.Frame(main_window, bg="#261038")
        frame_graph.grid(column = 0, row =1, sticky= "NSEW")
        # Configure the frame to resize with the window
        frame_graph.columnconfigure(0, weight = 1)
        frame_graph.rowconfigure(0, weight = 1)
        
# Create a label to display the title of the application
        label = tk.Label(main_window, text="Crypto Market Simulator", font=("Roboto", 24), fg="white", bg="#263238")
        label.grid(column = 0, row = 0, columnspan=3, sticky = "W")

  # Create a button to quit the game
        quit_game_button = ttk.Button(frame_display, text="Quit Game", command=lambda: self.end_game())
        quit_game_button.grid(column = 0, row = 0, columnspan=2)
# Initialize variables for profit engine and graph plotter
        profit_engine = None
        graph_plotter = PlotApp( self, main_window, frame_graph, Crypto, 365, frame_display, profit_engine)

# Method to display statistics window
    def statistics_window(self, profit_gained):
 # Create a new top-level window for statistics
        stats_window = tk.Toplevel(self)
        stats_window.title("Statistics")
        stats_window.geometry("400x300")

        #retrieve prices of the chosen cryptocurrency from the cryptocurrency class
        prices = Crypto.prices

        #sort prices to find highest and lowest
        highest_price = max(prices)
        lowest_price = min(prices)

        #display highest and lowest prices
        label_highest = tk.Label(stats_window, text=f"Highest Price: ${highest_price:.2f}")
        label_highest.pack(pady=10)

        label_lowest = tk.Label(stats_window, text=f"Lowest Price: ${lowest_price:.2f}")
        label_lowest.pack(pady=10)

        #display profit gained
        label_profit = tk.Label(stats_window, text=f"Profit Gained: ${profit_gained:.2f}")
        label_profit.pack(pady=10)

        



# Create an instance of the App class and run the main event loop
game = App()
game.mainloop()
