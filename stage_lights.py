#This is the code for a concert stage lights only

#Let's commence by importing the necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation

#Now let's create a class for ligts. This class has attribute like color, position, direction, intensity, distribution
# as per the the given instructions in the assignment.
#  
class Light:
    def __init__(self, color, position, direction, intensity, distribution):
        self.color = color
        self.position = position
        self.direction = direction
        self.intensity = intensity
        self.distribution = distribution
        self.cone = None
    
    def calculate_cone(self):
        # This piece of code is to calulate the light cone based on the spread attribute
        top_y = self.distribution[0][1]
        bottom_y = self.distribution[-1][1]

        # Now let's adjust the intensity based on the y-coordinate
        intensity_factor = (bottom_y - self.position[1]) / (bottom_y - top_y)
        self.intensity *= intensity_factor

        # This is to start from y_axis 620 and end at 0
        new_distribution = [[x, y - (top_y - bottom_y)] for x, y in self.distribution]
        self.distribution = new_distribution
    
    #This code is to change the colors of lights on the stage randomly 
    def blink(self):
        self.color = random.choice(['cyan', 'purple', 'purple', 'pink', 'red', 'blue'])


#Now let's create another class for the stage 
class Stage:
    def __init__(self, figsize=(9, 13), backdrop_file=None):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_aspect("equal")
        self.title = "CONCERT STAGE LIGHTS VIEW"
        self.lights = []
        self.cones = []

    #To add lights on plot
    def add_light(self, light):
        self.lights.append(light)
        spread = np.array(light.distribution)
        cone = self.ax.fill(spread[:, 0], spread[:, 1], color=light.color, alpha=0.4)[0]
        light.cone = cone
        self.cones.append(cone)
    
    
    #To amimate the lights 
    def animate_lights(self, frame):
        for light in self.lights:
            light.blink()
            cone_color = light.color
            light.cone.set_color(cone_color)

            light.calculate_cone()  # Calculate the light cone with adjusted intensity

    #To simulate lights
    def simulate_lights(self):
        #Animate lights on and disply them on plot
        self.animation = FuncAnimation(self.fig, self.animate_lights, interval=100)
        plt.suptitle(self.title, fontsize=18)
        plt.show()

# Create the Stage instance
stage = Stage(backdrop_file="bakground_image_audience.jpg")

# Let's create lights to be displayed on the plot
lights = [
    Light(color='green', position=[250, 390], direction=90, intensity=1,
          distribution=[[230, 600], [270, 600], [270, 610], [230, 610]]),
    Light(color='yellow', position=[350, 390], direction=90, intensity=1,
          distribution=[[330, 600], [370, 600], [370, 610], [330, 610]]),
    Light(color='red', position=[350, 200], direction=90, intensity=1,
          distribution=[[330, 600], [370, 600], [430, 200], [270, 200]]),
    Light(color='blue', position=[250, 200], direction=90, intensity=1,
          distribution=[[230, 600], [270, 600], [330, 200], [170, 200]]),
    Light(color='orange', position=[150, 390], direction=90, intensity=1,
          distribution=[[130, 600], [170, 600], [170, 610], [130, 610]]),
    Light(color='purple', position=[150, 200], direction=90, intensity=1,
          distribution=[[130, 600], [170, 600], [230, 200], [70, 200]]),
    Light(color='pink', position=[450, 200], direction=90, intensity=1,
          distribution=[[430, 600], [470, 600], [530, 200], [370, 200]])
          
]
# Add lights to the stage
for light in lights:
    stage.add_light(light)
    
# Now let's call teh simulate the lights function to display the stage and lights
stage.simulate_lights()
