import matplotlib.pyplot as plt
import numpy as np
import pygame
from pygame.locals import *

# Function to plot the graph
def plot_graph(x, y):
    plt.plot(x,y)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Cryptocurrency Price Graph')
    plt.grid(True)
    plt.show()

# Function to handle user input and pause/unpause the graph
def handle_input():
    paused = False
    while True:
        for event in pygame.event.get():``
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    paused = not paused
                    if paused:
                        plt.pause(1e-15) # pause the graph
                    else:
                        plt.pause(0.01)  # Unpause the graph

#Generate some exaple data
x = np.lispace(0, 10, 100)
y = np.sin(x)

#Plot the graph
plot_graph(x, y)

#Initialize pygame for handling user input
pygame.init()
handle_input()
                