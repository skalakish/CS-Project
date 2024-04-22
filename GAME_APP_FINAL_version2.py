# Import all the relevant LIbraries
import sqlite3
import hashlib
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure




#5590163
CRYPTOLIST = [] # global variable to store all the crypto currencies and their prices after initialisation
#5590163


#5590163
class MaxHeap():
    """Maintain a max heap for efficient maximum element retrieval."""
    #5589546
    def __init__(self) -> None:
        """Initialize an empty list to store heap elements"""
        self.heap = []

    def insert(self, item):
        """Append the new item to the heap and then heapify from that position."""
        self.heap.append(item)
        self.heapify(len(self.heap) - 1)

    def heapify(self, index):
        """Recursively adjust the heap to maintain the max-heap property."""
        parent_index = (index - 1) // 2
        # If current node is greater than its parent, swap them
        if self.heap[index] > self.heap[parent_index] and parent_index >= 0:
            self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
            self.heapify(parent_index)

    def remove(self):
        """Remove the maximum element from the heap."""
        if len(self.heap) == 0:
            raise Exception("Empty Heap")
        # Swap the last element with the root, then restore heap property from the root down
        self.heap[-1], self.heap[0] = self.heap[0], self.heap[-1]
        item = self.heap.pop()
        if self.heap:
            self.heapify_down(0)
        return item
    #5589546
    def heapify_down(self, index):
        """Restore the max-heap property by sifting down the element at index."""
        largest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        size = len(self.heap)
        
        # Find the largest among the node and its children
        if left_child < size and self.heap[left_child] > self.heap[largest]:
            largest = left_child
        if right_child < size and self.heap[right_child] > self.heap[largest]:
            largest = right_child
        # If the largest is not the node itself, swap and continue sifting down
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self.heapify_down(largest)

    def peek(self):
        """Return the maximum value from the heap without removing it."""
        if self.heap:
            return self.heap[0]
        else:
            raise Exception("Empty Heap")
#5590163


#5590163
class MinHeap():
    """Maintain a min heap for efficient minimum element retrieval."""
    #5589546
    def __init__(self) -> None:
        """Initialize an empty list to store heap elements."""
        self.heap = []

    def insert(self, item):
        """Append the new item to the heap and then heapify from that position."""
        self.heap.append(item)
        self.heapify(len(self.heap) - 1)

    def heapify(self, index):
        """Recursively adjust the heap to maintain the min-heap property."""
        parent_index = (index - 1) // 2
        # If current node is less than its parent, swap them
        if self.heap[index] < self.heap[parent_index] and parent_index >= 0:
            self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
            self.heapify(parent_index)

    def remove(self):
        """Remove the minimum element from the heap."""
        if len(self.heap) == 0:
            raise Exception("Empty Heap")
        # Swap the last element with the root, then restore heap property from the root down
        self.heap[-1], self.heap[0] = self.heap[0], self.heap[-1]
        item = self.heap.pop()
        if self.heap:
            self.heapify_down(0)
        return item
    #5589546
    def heapify_down(self, index):
        """Restore the min-heap property by sifting down the element at index."""
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        size = len(self.heap)

        # Find the smallest among the node and its children
        if left_child < size and self.heap[left_child] < self.heap[smallest]:
            smallest = left_child
        if right_child < size and self.heap[right_child] < self.heap[smallest]:
            smallest = right_child
        # If the smallest is not the node itself, swap and continue sifting down
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.heapify_down(smallest)

    def peek(self):
        """Return the minimum value from the heap without removing it."""
        if self.heap:
            return self.heap[0]
        else:
            raise Exception("Empty Heap")
#5590163


#5590163
class CryptoCurrency():
    """Class for simulating cryptocurrency price movements.
    
    This class initializes a cryptocurrency with its parameters that define its price behaviour

    Instance Varible:
    self.startprice -- Initial price of the cryptocurrency
    self.drift -- Expected return of the cryptocurrency per time unit
    self.volatility -- Standard deviation of the cryptocurrency's returns
    self.simulation_no -- Number of price points to simulate
    self.jump_chance -- Probability of a price jump occurring at each step
    self.jump_magnitude -- Standard deviation of the jump size
    self.name  -- name of the cryptocurrency
    self.prices -- this holds the prices of the cryptocurrency

    Public Methods:
    simulation_engine
    get_next_price
    """
    def __init__(self, name, startprice, drift, volatility, N, jump_chance, jump_magnitude) -> None:
        """Initialize the cryptocurrency with all the necessary parameters."""
        self.startprice = startprice  
        self.drift = drift 
        self.volatility = volatility  
        self.simulation_no = N  
        self.jump_chance = jump_chance  
        self.jump_magnitude = jump_magnitude  
        self.name = name  
        self.prices = []  

    def simulation_engine(self):
        """Simulate the price of the cryptocurrency using a stochastic model.
        
        This method generates a price for the cryptocurrency an appends it to its 
        prices variable
        """
        prices = [self.startprice]  # Start with the initial price
        volatility = self.volatility  # Initial volatility

        for _ in range(1, self.simulation_no):
            dt = 1  # Assuming each step is one time unit
            # Generate a random price change based on normal distribution
            random_change = np.random.normal(self.drift * dt, volatility * np.sqrt(dt))
            
            # Implement volatility clustering (EWMA - Exponentially Weighted Moving Average)
            recent_change = np.log(prices[-1] / prices[-2]) if len(prices) > 1 else 0
            volatility = volatility * 0.9 + 0.1 * abs(recent_change)  # Adjust volatility based on recent change

            # Jump logic: randomly determine if a jump occurs at this step
            if np.random.rand() < self.jump_chance:
                jump = np.random.normal(0, self.jump_magnitude)  # Size of the jump
            else:
                jump = 0  # No jump

            # Calculate the new price and append it to the list
            new_price = prices[-1] * np.exp(random_change + jump)
            prices.append(new_price)

        self.prices = prices  # Store the completed list of simulated prices

    def get_next_price(self, index):
        """Retrieve the next price from the list of simulated prices."""
        if index < len(self.prices):
            return self.prices[index]
        return None  # Return None if the requested index is out of range
#5590163


#5590163
#5588504
class PlotApp():
    """Class for ploting and animating cryptocurrency price movements.
    
    This class initialises a matplotlib graph object(animated) which is placed in a tkinter widget
    The class also has methods for pausing and  unpausing the plotting of the graph
    There is aslo the update plot method which cretes the animation effect of the graph

    Instance Variables:
    self.app  -- a reference to the main app itself(an App object)
    self.profit_engine -- a variable to strore the profit engine
    self.root_window -- the window on which  self.master exists
    self.master -- a variable that stores the frame on which the graph would be placed
    self.chosen_crypto -- a variable to stoe the chosen cryprtocurrency
    self.total_points -- a variable that strores the number of time points
    self.current_index -- an index desinged to keep track of the current price being plotted based on the prices attribute of cryptocurrencies
    self.plot_paused -- This creates a varible to keep track of the graph state(paused or unpaused)
    self.fig -- a figure object which is like the base of the plot
    self.ax = self.fig.add_subplot(111) -- This adds a subplot which sets the number of rows and columns in our plot which is one
    self.x --  an x-axis on the self.ax object
    self.y --  an y-axis on the self.ax object
    self.line, --  the line of the graph which is a plot of the y and x axis with a red colour
    self.canvas --  a frame(a tkinter object) to hold the matplotlib object(fig) which would allow it to be integrated with tkinter
    self.startsimulation_button --  initialise the button to start the simulation 

    Public Methods:
    pause_plot
    unpause_plot
    update_plot
    """
    
    #5588504
    def __init__(self, app, root_window, master, chosen_crypto, total_points,  frame_display, profitengine = None):
        """ initialise the plot app with all the necessary parameters."""
        self.app = app
        self.profit_engine  = ProfitEngine(frame_display, self)
        self.root_window = root_window 
        self.master = master
        self.chosen_crypto = chosen_crypto 
        self.total_points = total_points
        self.current_index = 0

        self.plot_paused = True

        # This creates a figure and a plot element 
        self.fig = Figure() 
        self.ax = self.fig.add_subplot(111) # This adds a subplot which sets the number of rows and columns in our plot which is one
        self.ax.set_xlabel("Time in Days(days)")# set the label for the x axis
        self.ax.set_ylabel(f"{chosen_crypto.name} prices($)")# set the lable for y axis
        self.x = np.linspace(1, self.total_points , self.total_points) #This creates a linespace or grid on the x axis from 1 to 365
        self.y = np.full((365,), chosen_crypto.prices[0])  #This creates a linespace that conains only the initial price of the cryptocurrency
        

        self.line, = self.ax.plot(self.x, self.y, 'r-')  # This sets the line of the graph to be a plot of the y and x axis and make the colour red

        # Embed the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw() # create the graph
        self.canvas.get_tk_widget().grid(row = 0, column=0, sticky = "NSEW")# set the position of the graph on the window


        self.startsimulation_button = tk.Button(master, text="Start simulation", command=self.unpause_plot)
        self.startsimulation_button.grid(row = 1, column=1)# set the position of the button

        self.update_plot()  # Start the plot update loop which will create the animation effect
    #5588504
    
        
    #5590163
    def pause_plot(self):
        """ pause the plot when called."""
        self.plot_paused = True # set the plot paused variable to true which will pause the plot
    #5590163

    #5590163
    def unpause_plot(self):
        """unpause the plot when called."""
        if self.plot_paused == True:# check if the plot_paused variable is true to prevent multiple clicks on the start simulation button from breakiing the game
            self.plot_paused = False
            self.update_plot()# start to update the plot with the next price
    #5590163

    #5590163
    def update_plot(self):
        """Updates the graph after a cetain period of time to create an animation effect.

        This is done by ensuring the plot is not paued
        then, retrieving the next price from the cryptocurrency
        then, setting  self.y to the new price and plotting it
        the process is repeated after 100 milliseconds to create the animation effect
        the function also check when the graph is done plotting which signals the end of the game
        """
    
    
        global CURRENT_PRICE 
        if not self.plot_paused and self.current_index < self.total_points: #ensure that the plot is actually paused  and if the current index is less than the total point which is 365
            new_data = self.chosen_crypto.get_next_price(self.current_index)# get the next_price using the get_next_price method
            if new_data is not None:
                buffer = 100 # set abuffer that will allow for auto adjustment of the scale of the y-axis
                self.y[self.current_index] = new_data # set the next y-data to the new price to create a an animation effect
                CURRENT_PRICE = new_data #  set the current price which would be used in the profit_engine for trading
                self.current_index += 1 
                self.line.set_ydata(self.y)
                self.ax.set_ylim(min(self.y) - buffer, max(self.y) + buffer) #adjust the scale to accomodate the changing price by changing the to and bottom of the axis and top by the buffer(100)
                self.canvas.draw()# plot the graph with the new data 

                
                self.profit_engine.update_heaps(new_data)# Update min and max heaps

            self.master.after(100, self.update_plot)# schedule the graph to update after 100 millisecond to create the animation effect
        elif self.current_index == self.total_points: #create a condition to end the game
            self.root_window.destroy() #  destroy the main game window
            self.profit_engine.calculate_game_result(self.app)# calculate the the result of the game
    #5590163
#5590163


#5590163            
class ProfitEngine():
    """Class for handling all the trading of cryptocurrency.
    
    Instance Variables:
    self.graph_plotter -- initialise the Plot_app object used int he game
    self.min_heap -- Min heap to track minimum prices
    self.max_heap -- Max heap to track maximum prices
    self.capital -- initialise a tk.Doublevar(a float value that can be displayed on screen) to store the capital
    self.capital_for_checking 
    self.investment_quantity -- initialise a tk.Doublevar(a float value that can be displayed on screen) to store the investment quantity
    self.gains  -- initialise a tk.Doublevar(a float value that can be displayed on screen) to store the gains or profit made
    self.buy_button -- initialise buy button
    self.sell_button -- initialise sell button 
    self.gains_label -- initialise a label that will identify  self.gains on screen
    self.gains_display -- initialise the label that will hold the self.gains varible
    self.capital_label -- initialise a label that will identify the self.capital on screen
    self.capital_display -- nitialise the label that will hold the self.capital varible
    self.investment_amount_label -- initialise a label that will identify self.investment_quantity on screen
    self.investment_amount_display -- nitialise the label that will hold the self.ivestment_quantity varible

    Class Methods:
    handle_monetary_input_invest -- this handles the input and all the error checking for the ivest method
    handle_quantity_input_sell -- this handles the input and all the error checking for the sell method
    invest -- this method handles all the calculation involed with buying cryptocurrency
    sell -- this method handles all the calculation involed with selling cryptocurrency
    sell_for_checking_winning_condition -- this method sells all the leftover cryptocurrency at the end of the game
    update_heaps -- this updates the min and max heaps
    calculate_game_result -- this decides the outcome of the game(win or loss)
    """

    def __init__(self, frame, graphplotter) -> None:
        """ initialise the object with all its necessary parameters."""
        self.graph_plotter = graphplotter
        self.min_heap = MinHeap() 
        self.max_heap = MaxHeap() 

        self.capital = tk.DoubleVar(value=10000)
        self.capital_for_checking = 10000
        self.investment_quantity = tk.DoubleVar(value=0) 
        self.gains = tk.DoubleVar(value=0) 

        # initialise buy button
        self.buy_button = tk.Button(frame, text="BUY", command=self.invest)
        self.buy_button.grid(column=0, row=1, columnspan=2)

        # initialise sell button
        self.sell_button = tk.Button(frame, text="SELL", command=self.sell)
        self.sell_button.grid(column=0, row=2, columnspan=2)

        # initialise a label that will identify the gains on screen
        self.gains_label = tk.Label(frame, text="GAINS", font=("Roboto", 12), fg="white", bg="#263238")
        self.gains_label.grid(column=0, row=3)

        # initialise the label that will hold the gains varible
        self.gains_display = tk.Label(frame, text="GAINS", textvariable=self.gains, font=("Roboto", 12), fg="white",bg="#263238")
        self.gains_display.grid(column=1, row=3)

        # initialise a label that will identify the capital on screen
        self.capital_label = tk.Label(frame, text="CAPITAL", font=("Roboto", 12), fg="white", bg="#263238")
        self.capital_label.grid(column=0, row=4)

        # initialise the label that will hold the capital varible
        self.capital_display = tk.Label(frame, text="CAPITAL", textvariable=self.capital, font=("Roboto", 12),fg="white", bg="#263238")
        self.capital_display.grid(column=1, row=4)

        # initialise a label that will identify the investment amount on screen
        self.investment_quantity_label = tk.Label(frame, text="INVESTMENT AMOUNT", font=("Roboto", 12), fg="white", bg="#263238")
        self.investment_quantity_label.grid(column=0, row=5)

        # initialise the label that will hold the investment amount varible
        self.investment_quantity_display = tk.Label(frame, text="INVESTMENT AMOUNT", textvariable=self.investment_quantity, font=("Roboto", 12), fg="white", bg="#263238")
        self.investment_quantity_display.grid(column=1, row=5)

    def handle_monetary_input_invest(self):
        """Continuously prompt the user to input the amount of money they wish to invest."""
        while True:
            try:
                # Attempt to convert user input into a float. This is expected to be the amount they want to invest.
                money = float(simpledialog.askfloat("Input", "How much do you want to invest"))
            except:
                # If the conversion fails (due to invalid input), show an error and prompt again.
                messagebox.showerror("Error", "Input a real number")
                return None  # Return None to indicate failure to get a valid input
            if money > self.capital.get():
                # Check if the user has enough capital to make the investment
                messagebox.showerror("Error", "You cannot spend more than you own")
                continue  # Continue prompting if they don't have enough capital
            else:
                # If the amount is valid and the user has enough capital, return the amount to be invested
                return money

    def handle_quantity_input_sell(self):
        """Continuously prompt the user to input the quantity of their investment they wish to sell."""
        while True:
            try:
                # Attempt to convert user input into a float. This is expected to be the quantity they want to sell.
                quantity = float(simpledialog.askfloat("Input", "How much do you want to sell"))
            except:
                # If the conversion fails (due to invalid input), show an error and prompt again.
                messagebox.showerror("Error", "Input a real number")
                return None  # Return None to indicate failure to get a valid input
            if quantity > self.investment_quantity.get():
                # Check if the user has enough of the investment quantity to sell
                messagebox.showerror("Error", "Oops! You cannot sell more than you have")
                continue  # Continue prompting if they don't have enough quantity to sell
            else:
                # If the amount is valid and within the user's holdings, return the quantity to be sold
                return quantity

    def invest(self):
        """ Attempt to perform an investment trade."""
        try:
            if CURRENT_PRICE:
                # Pause the plot updates to process the investment without interruption
                self.graph_plotter.pause_plot()
                # Request the amount to invest from the user
                investment_amount = self.handle_monetary_input_invest()
                if investment_amount:
                    # Check if the user tries to invest a non-zero amount
                    if investment_amount > 0:
                        # Calculate the new capital after investing and update the capital variable
                        new_capital = self.capital.get() - investment_amount
                        self.capital.set(new_capital)
                        
                        # Calculate the new quantity of the investment based on the current price and update it
                        new_quantity = self.investment_quantity.get() + (investment_amount / CURRENT_PRICE)
                        self.investment_quantity.set(new_quantity)
                        # Resume plot updates after the investment is processed
                        self.graph_plotter.unpause_plot()
                    else:
                        # Show error if the investment amount is zero
                        messagebox.showerror("Error", "You cannot invest zero")
                        self.graph_plotter.unpause_plot()
        except NameError:
            # Error if trying to invest before the simulation has started
            messagebox.showerror("Error", "You must start the simulation before trading")

    def sell(self):
        """Attempt to perform a selling trade."""
        try:
            if CURRENT_PRICE:
                # Pause the plot updates to process the selling without interruption
                self.graph_plotter.pause_plot()
                # Request the quantity to sell from the user
                quantity_to_sell = self.handle_quantity_input_sell()
                if quantity_to_sell:
                    # Check if the user tries to sell a non-zero quantity
                    if quantity_to_sell > 0:
                        # Calculate the new gains from selling and update the gains variable
                        new_gains = self.gains.get() + (CURRENT_PRICE * quantity_to_sell)
                        self.gains.set(new_gains)
                        # Calculate the new remaining investment quantity and update it
                        new_quantity = self.investment_quantity.get() - quantity_to_sell
                        self.investment_quantity.set(new_quantity)
                        # Resume plot updates after the selling is processed
                        self.graph_plotter.unpause_plot()
                    else:
                        # Show error if the selling quantity is zero
                        messagebox.showerror("Error", "You cannot sell zero")
                        self.graph_plotter.unpause_plot()
        except NameError:
            # Error if trying to sell before the simulation has started
            messagebox.showerror("Error", "You must start the simulation before trading")

    def sell_for_checking_winning_condition(self):
        """Sell all remaining investments to check the final winning condition."""
        try:
            if CURRENT_PRICE:
                # Get the total quantity currently invested
                quantity_to_sell = self.investment_quantity.get()
                if quantity_to_sell:
                    if quantity_to_sell > 0:
                        # Calculate the final gains from selling all remaining investments
                        new_gains = self.gains.get() + (CURRENT_PRICE * quantity_to_sell)
                        self.gains.set(new_gains)

                        # Set the remaining investment quantity to zero
                        new_quantity = self.investment_quantity.get() - quantity_to_sell
                        self.investment_quantity.set(new_quantity)
                        
        except NameError:
            # Error if trying to perform final check before the simulation has started
            messagebox.showerror("Error", "You must start the simulation before trading")

    def update_heaps(self, price):
        """update the min and max heaps."""
        self.min_heap.insert(price)  # update the min heap with each price from the plot app
        self.max_heap.insert(price)  # update the max heap with each price from the plot app 

    def calculate_game_result(self, app):
        """ announce the game winner and call the statistics window."""
        self.sell_for_checking_winning_condition()# sell the rest of the cyptocurrency at the end of the game
        current_capital  = self.capital.get() + self.gains.get()# add up the gains and the remaining capital
        if current_capital > self.capital_for_checking: # check if profit was made
            messagebox.showinfo("Information", "Congrats!!!  You won")# display winning message
        else:
            messagebox.showinfo("Information", "Sorry, You lost, better luck next time")# display loss message
        app.statistics_window(self.min_heap, self.max_heap, self.gains.get())#call the statistics window
#5590163
#5588504
class Leaderboard:
    def __init__(self):
        self.conn = sqlite3.connect('leaderboard.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players
                               (id INTEGER PRIMARY KEY, username TEXT, capital REAL, gains REAL)''')
        self.conn.commit()

    def update_player_info(self, username, capital, gains):
        self.cursor.execute("INSERT OR REPLACE INTO players (username, capital, gains) VALUES (?, ?, ?)",
                            (username, capital, gains))
        self.conn.commit()

    def get_leaderboard(self):
        self.cursor.execute("SELECT username, capital, gains FROM players ORDER BY gains DESC")
        return self.cursor.fetchall()
#5588504
#5590163
class PlotAppForStatistics():
    """Class for plotting cryptocurrency price trend in the statistics window.
    
    Instance variables:
    self.master -- Master frame in the statistics window
    self.total_points --Total number of data points to display
    self.fig -- Create a figure for plotting
    self.ax -- Add a subplot to the figure
    self.x -- Generate x values (time points in days)
    self.y -- Prices passed from the cryptocurrency data(prices attribute)
    self.line, -- Plot the prices as a red line
    self.canvas -- Create a canvas for the figure which is like a tkinter placeholder
    """

    def __init__(self, prices, master, total_points=365):
        """Constructor for initializing the plotting application for statistical data."""
        self.master = master  # Master frame in the statistics window
        self.total_points = total_points  # Total number of data points to display
        
        # Create a matplotlib figure and a subplot
        self.fig = Figure()  # Create a figure for plotting
        self.ax = self.fig.add_subplot(111)  # Add a subplot to the figure
        self.ax.set_xlabel("Time in Days(days)")  # Set the x-axis label
        self.ax.set_ylabel(f"Crypto prices($)")  # Set the y-axis label
        self.x = np.linspace(1, self.total_points, self.total_points)  # Generate x values (time points in days)
        self.y = prices  # Prices passed from the cryptocurrency data
        
        # Create a line object to represent the cryptocurrency prices over time
        self.line, = self.ax.plot(self.x, self.y, 'r-')  # Plot the prices as a red line

        # Embed the matplotlib figure into the Tkinter interface
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)  # Create a canvas for the figure which is like a tkinter placeholder
        self.canvas.draw()  # Render the plot
        self.canvas.get_tk_widget().pack()  # Pack the canvas into the master widget
#5590163


#5590163
# Instance for bitcoin
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

# Instance for litecoin
litecoin = CryptoCurrency(
    startprice=1000,       # Starting price of Ripple
    drift=0.0004,         # Daily percentage drift
    volatility=0.005,     # Daily volatility
    N=365,               # Number of simulations
    jump_chance=0.05,     # Chance of a price jump occurring
    jump_magnitude=0.005,    # Magnitude of the price jump
    name = "Litecoin"
)
#5590163

#5590163
#initialize all the data for the cryptocurrencies
def initialise_crypto_prices(): 
    """Initialise all the cryptocurrencies' prices."""
    bitcoin.simulation_engine()
    litecoin.simulation_engine()
    ethereum.simulation_engine()


initialise_crypto_prices()# call the function to ensure that the game sarts withe cryptocurencies that have prices


# add the cryptocurrencies to the global variable
CRYPTOLIST.append(litecoin)
CRYPTOLIST.append(bitcoin)
CRYPTOLIST.append(ethereum)
#5590163


#5568363
class LoginHandler():
    """Class for handling login and registeration of users.
    
    Instance Variables:
    self.app -- a reference to the main application itself(an App object)
    self.conn -- Database file where user credentials are stored
    self.cursor -- Cursor for executing SQL queries

    Public Methods:
    hash_password 
    verify_login
    register
    login
    register_account
    """

    def __init__(self, app) -> None:
        """Initialize the login handler with a reference to the main app."""
        self.app = app  
        # Establish a connection to the SQLite database to store user credentials
        self.conn = sqlite3.connect('user_credentials.db')  # Database file where user credentials are stored
        self.cursor = self.conn.cursor()  # Cursor for executing SQL queries

        # Create a table for users if it doesn't already exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        self.conn.commit()  # Commit changes to the database

    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()  # Return the hexadecimal digest of the hashed password

    def verify_login(self, username, password):
        """Verify login credentials against the database."""
        hashed_password = self.hash_password(password)  # Hash the provided password
        # Execute SQL query to find a user with matching username and password
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        # Return True if a match is found, otherwise False
        return self.cursor.fetchone() is not None

    def register(self, username, password):
        """Register a new user with a username and hashed password."""
        hashed_password = self.hash_password(password)  # Hash the provided password
        # Insert new user credentials into the database
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        self.conn.commit()  # Commit the new entry to the database

    def login(self, username, password, loadingscreen):
        """Handle user login."""
        if self.verify_login(username, password):
            # If credentials are verified, show success message and transition to the next screen
            messagebox.showinfo("Login Successful", "Welcome back, {}!".format(username))
            loadingscreen.destroy()  # Close the loading screen
            self.app.loading_screen()  # Proceed to the main application loading screen
        else:
            # If login fails, show error message
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register_account(self, username, password):
        """Handle user registration."""
        if username and password:
            # If username and password are provided, register the account
            self.register(username, password)
            messagebox.showinfo("Registration Successful", "Account registered successfully!")
        else:
            # If username or password is missing, show error message
            messagebox.showerror("Registration Failed", "Please enter both username and password")
#5568363


#5590163
class App(tk.Tk):
    """Class for handling the base GUI of the application and the sequence of the app.
    
        This class inherits from the Tk moduke of tkinter
        Its initialisation creates GUI application upon which the extra windows of the game are based

    Instance Variable:
    self.login_handler -- this handles all th login processes and is integrated with the login_window method


    Public Methods:
    app_sequence
    login_window
    transition_to_main
    loading_screen
    choose_crypto
    make_choice
    end_game
    main_window
    quick_sort_prices 
    calculate_maximum_possible_profit
    replay_game 
    statistics_window 
    """
    #5590163    
    def __init__(self):
        """Initialise the Tk module(super class) and call the application sequence."""
        super().__init__()
        self.login_handler = LoginHandler(self)  # Initialize login handling
        self.withdraw()  #  hide the initial window created
        self.app_sequence()  # Start the application
    #5590163
    
    #5590163
    def app_sequence(self):
        """Start the application by showing the login screen."""
        self.login_window()
    #5590163


    #5568363     
    def login_window(self):
        """ Create a separate login window."""
        login_window = tk.Toplevel(self)
        login_window.configure(bg="#263238")
        login_window.title("Login Screen")

        # Frame for the login inputs
        frame = tk.Frame(login_window, bg="#263238")
        frame.pack(pady=20, padx=60)

        # Label as a header for the login system
        label = tk.Label(frame, text="Login System", font=("Roboto", 24), fg="white", bg="#263238")
        label.pack(pady=12)

        # Frame to hold text entries for username and password
        frame_text_holders = tk.Frame(login_window, bg="#263238")
        frame_text_holders.pack()

        # Label and entry for username
        label_name = tk.Label(frame_text_holders, text="Name", font=("Roboto", 12), fg="white", bg="#263238")
        label_name.grid(row=0, column=0)
        entry1 = ttk.Entry(frame_text_holders)
        entry1.config(font=("Roboto", 12))
        entry1.grid(row=0, column=1)

        # Label and entry for password
        label_password = tk.Label(frame_text_holders, text="Password", font=("Roboto", 12), fg="white", bg="#263238")
        label_password.grid(row=1, column=0)
        entry2 = ttk.Entry(frame_text_holders, show="*")
        entry2.config(font=("Roboto", 12))
        entry2.grid(row=1, column=1)

        # Buttons for login and registration
        login_button = ttk.Button(frame, text="Login", command=lambda: self.login_handler.login(entry1.get(), entry2.get(), login_window))
        login_button.pack(pady=6)
        register_button = ttk.Button(frame, text="Register", command=lambda: self.login_handler.register_account(entry1.get(), entry2.get()))
        register_button.pack(pady=6)
   
    def transition_to_main(self, loading_window):
        """Transition from the loading screen to main application window."""
        loading_window.destroy()  # Destroy the loading window
        self.choose_crypto()  # Proceed to cryptocurrency selection
        
    def loading_screen(self):
        """ Create a loading screen while the application processes or loads data."""
        loading_window = tk.Toplevel(self)
        loading_window.geometry("300x150")
        loading_window.title("Loading...")
        loading_window.resizable(False, False)

        label = tk.Label(loading_window, text="Loading, please wait...", font=("Roboto", 12))
        label.pack(pady=20)

        #create a loading bar
        progressbar = ttk.Progressbar(loading_window, mode="indeterminate")
        progressbar.pack(pady=10)
        progressbar.start()

        # Auto proceed to main app after a delay
        loading_window.after(1000, lambda: self.transition_to_main(loading_window))

    #5568363

    #5590163
    def choose_crypto(self):
        """ Allow the user to choose a cryptocurrency."""
        choice_window = tk.Toplevel(self)
        choice_window.resizable(False, False)
        initialise_crypto_prices()

        choice_label = tk.Label(choice_window, text="Choose a Crypto Currency", font=("Roboto", 24), fg="white", bg="#263238")
        choice_label.pack(pady=20)

        # Buttons for different cryptocurrencies
        bitcoin_button = tk.Button(choice_window, text="BITCOIN", command=lambda: self.make_choice("Bitcoin", choice_window))
        bitcoin_button.pack()
        ethereum_button = tk.Button(choice_window, text="ETHEREUM", command=lambda: self.make_choice("Ethereum", choice_window))
        ethereum_button.pack()
        litecoin_button = tk.Button(choice_window, text="LITECOIN", command=lambda: self.make_choice("Litecoin", choice_window))
        litecoin_button.pack()
    #5590163


    #5568363
    def make_choice(self, choice, window):
        """ Handle the selection of a cryptocurrency."""
        global CRYPTO # setting the global avriable
        window.destroy()  # Close the choice window
        messagebox.showinfo("Choice", f"You chose {choice}")
        for cryptocurrency in CRYPTOLIST:
            if cryptocurrency.name == choice:
                CRYPTO = cryptocurrency # set the chosen crypto cureency to the global Cryptovarible
                self.main_window()  # Open the main application window with the selected cryptocurrency

    def end_game(self):
        """ Terminate the application."""
        self.destroy()

    def main_window(self):
        """ Create and configure the main application window after a cryptocurrency has been chosen."""
        main_window = tk.Toplevel(self) # creating the window
        main_window.state("zoomed")
        main_window.title("Main Window")
        main_window.configure(bg="#263238")
        main_window.columnconfigure(0, weight=1)
        main_window.rowconfigure(1, weight=1)

        # Frames for displaying the controls
        frame_display = tk.Frame(main_window, bg="#113238")
        frame_display.grid(column=1, row=1, sticky="NSEW")

        # Frames for displaying the simulation 
        frame_graph = tk.Frame(main_window, bg="#261038")
        frame_graph.grid(column=0, row=1, sticky="NSEW")
        frame_graph.columnconfigure(0, weight=1)
        frame_graph.rowconfigure(0, weight=1)

        # Main application header
        label = tk.Label(main_window, text="Crypto Market Simulator", font=("Roboto", 24), fg="white", bg="#263238")
        label.grid(column=0, row=0, columnspan=3, sticky="W")

        # Quit game button
        quit_game_button = ttk.Button(frame_display, text="Quit Game", command=lambda: self.end_game())
        quit_game_button.grid(column=0, row=0, columnspan=2)

        # Initialize the profit engine and graph plotter with the chosen cryptocurrency
        profit_engine = None
        graph_plotter = PlotApp(self, main_window, frame_graph, CRYPTO, 365, frame_display, profit_engine)

    #5568363

    #5590163
    def quick_sort_prices(self, arr):
        """Quick sort algorithm implementation for sorting prices."""
        if len(arr) <= 1:
            return arr  # Base case: a list of zero or one elements is sorted, by definition
        else:
            pivot = arr[len(arr) // 2]  # Choose the middle element as pivot
            left, middle, right = [], [], []  # Lists for elements less than, equal to, and greater than pivot
            for x in arr:
                if x < pivot:
                    left.append(x)
                elif x == pivot:
                    middle.append(x)
                else:
                    right.append(x)
            return self.quick_sort_prices(left) + middle + self.quick_sort_prices(right)  # Recursively sort and concatenate
    #5590163

    #5590163
    def calculate_maximum_possible_profit(self, min, max):
        """Calculate the maximum possible profit based on minimum and maximum prices."""
        return ((10000 / min) * max) - 10000
    #5590163

    #5590163
    def replay_game(self, window):
        """Allow the user to replay the game by choosing a new cryptocurrency."""
        window.destroy()  # Close the current statistics window
        self.choose_crypto()  # Reopen the cryptocurrency selection window
    #5590163

    #5589546
    def statistics_window(self, minheap, maxheap, profit_gained):
        """Display statistical analysis of the simulation."""
        #set window configurations
        stats_window = tk.Toplevel(self)
        stats_window.title("Statistics")
        stats_window.geometry("800x600")
        stats_window.resizable(False, False)
    #5588904
        stats_window.title("Leaderboard")

        # Create Treeview widget to display leaderboard
        leaderboard_tree = ttk.Treeview(stats_window, columns=('Username', 'Capital', 'Gains'))
        leaderboard_tree.heading('#0', text='Rank')
        leaderboard_tree.heading('Username', text='Username')
        leaderboard_tree.heading('Capital', text='Capital')
        leaderboard_tree.heading('Gains', text='Gains')

        # Populate Treeview with leaderboard data
        leaderboard_data = self.leaderboard.get_leaderboard()
        for rank, (username, capital, gains) in enumerate(leaderboard_data, start=1):
            leaderboard_tree.insert('', 'end', text=str(rank), values=(username, capital, gains))

        leaderboard_tree.pack(expand=True, fill='both')
    #5588504
        prices = CRYPTO.prices  # Retrieve prices from the chosen cryptocurrency
        sortedprices = self.quick_sort_prices(prices)  # Sort prices for analysis

        highest_price = maxheap.peek()  # Get the highest price from the max heap
        lowest_price = minheap.peek()  # Get the lowest price from the min heap

        maxprofit = self.calculate_maximum_possible_profit(lowest_price, highest_price)  # Calculate maximum profit

        #5590163
        # Frames for displaying the controls
        frame_display = tk.Frame(stats_window, bg="#113238")
        frame_display.grid(column=1, row=0, sticky="NSEW")

        # Frames for displaying the graph of prices trend
        frame_graph = tk.Frame(stats_window, bg="#261038")
        frame_graph.grid(column=0, row=0, sticky="NSEW")
        #5590163
        
        # initialise the label that will hold the highest price varible
        label_highest = tk.Label(frame_display, text=f"Highest Price: ${highest_price:.2f}")
        label_highest.pack(pady=10)

        # label to display graphtitle
        label_graph_label = tk.Label(frame_graph, text="Simulation Prices Trend", font=("Roboto", 24), fg="white", bg="#263238")
        label_graph_label.pack()

        # initialise the label that will hold the lowest price varible
        label_lowest = tk.Label(frame_display, text=f"Lowest Price: ${lowest_price:.2f}")
        label_lowest.pack(pady=10)

        # initialise the label that will hold the profit gained varible
        label_profit = tk.Label(frame_display, text=f"Profit Gained: ${profit_gained:.2f}")
        label_profit.pack(pady=10)

        # initialise the label that will hold the maximum profit possible varible
        label_maximum_profit = tk.Label(frame_display, text=f"Max gains possible: ${maxprofit:.2f}")
        label_maximum_profit.pack(pady=10)

        #5590163
        #quit button
        quit_game_button = ttk.Button(frame_display, text="Quit Game", command=lambda: self.end_game())
        quit_game_button.pack(pady=10)

        #replay game button
        replay_game_button = ttk.Button(frame_display, text="Replay", command=lambda: self.replay_game(stats_window))
        replay_game_button.pack(pady=10)

        graph = PlotAppForStatistics(sortedprices, frame_graph, 365)  # Display a graphical representation of price trends
        #5590163
    #5589546
#5590163
 


#5590163
game = App() #game initialisation
game.mainloop() # call to run the game
#5590163
