# This is the code for a concert stage for mythical rock band Spinal Tap
# Let's commence by importing the necessary libraries
import configparser
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
from PIL import Image

# Now let's create a class for ligts. This class has attribute like color, position, direction, intensity, distribution
# as per the the given instructions in the assignment.
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
        self.color = random.choice(['cyan', 'purple', 'purple', 'pink', 'red', 'blue', 'yellow'])

#Let's create another class for to set the Backdrop for the stage view
class Backdrop:
    def __init__(self, filepath):
        self.image = Image.open(filepath).convert("RGBA")

    def display(self, ax):
        ax.imshow(self.image, extent=[0, 600, 0, 400], aspect="auto")

#Let's create another class for smoke_machine
class SmokeMachine:
    def __init__(self, position, direction, intensity):
        self.position = position
        self.direction = direction
        self.intensity = intensity
        self.smoke_particles = []
   
    #This will first calculate smoke
    def calculate_smoke(self):
        self.smoke_particles.clear()

        # Based on the intensity calculate the number of smoke particles
        num_particles = int(self.intensity * 100)

        # With random positions and directions generate smoke particles 
        for _ in range(num_particles):
            # Calculate the random position within the smoke machine's vicinity
            pos_x = np.random.uniform(low=240, high=280)
            pos_y = np.random.uniform(low=400, high=500)
            position = [pos_x, pos_y]

            # Now let's calculate the random direction within the smoke machine's direction range
            dir_range = np.radians(self.direction + np.random.normal(scale=10))
            direction = [np.cos(dir_range), np.sin(dir_range)]

            #Now add the smoke particle to the list
            self.smoke_particles.append((position, direction))

#This will diffuse the smoke using moore neighborhood approch
    def diffuse_smoke(self, neighborhood='moore', intensity_decay=0.6):
        new_particles = []
        for particle in self.smoke_particles:
            pos, direction = particle
            if neighborhood == 'moore':

                # Implement Moore neighborhood diffusion rules
                new_pos_x = pos[0] + np.random.choice([-1, 0, 1])
                new_pos_y = pos[1] + np.random.choice([-1, 0, 1])

            elif neighborhood == 'van_neumann':
                # Implement Von Neumann neighborhood diffusion rules
                move_directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
                move_direction = random.choice(move_directions)
                new_pos_x = pos[0] + move_direction[0]
                new_pos_y = pos[1] + move_direction[1]

            else:
                raise ValueError('Invalid neighborhood type')

            new_pos = [new_pos_x, new_pos_y]
            new_dir = direction  # Direction remains unchanged during diffusion
            new_intensity = np.linalg.norm(new_dir) * intensity_decay  # Decay the intensity

            new_particles.append((new_pos, new_dir, new_intensity))

        self.smoke_particles = new_particles
    
    #To generate smoke 
    def generate_smoke(self, neighborhood='moore'):
        self.smoke_particles.clear()
        self.calculate_smoke()

        # Diffuse the smoke particles
        self.diffuse_smoke(neighborhood)

    def plot_smoke(self, ax):
        for particle in self.smoke_particles:
            pos, direction, intensity = particle  # Unpack the intensity value
            color = (intensity, intensity, intensity)
            ax.scatter(pos[0], pos[1], color=color)

# Now let's create another class for the stage.
# I have created a script in a .txt file where I have added a name form backdrop image
# and  defined some lights with color with differnt position, direction, intensity and distribution.
# In this class I have also impleted the logic to read the backdrop image and lights parameter
# from the choreography.txt file. I have not included the audience in .txt file 
# because the number of audience is quite high, so I preferd to create audience on using a for loop
# that will create 200 random audience on the stage e.g
# for _ in range(200) 
# x = random.uniform(20, 500)
# y = random.uniform(200, 380)
# stage.add_people(x, y) 

class StageChoreography:
    def __init__(self, figsize=(9, 13), backdrop_file=None):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_aspect("equal")
        self.title = "CONCERT STAGE VIEW"
        self.lights = []
        self.cones = []
        self.people = []
        self.smoke_machine = None
        self.pops = []
        self.animation = None

        self.backdrop = None
        if backdrop_file is not None:
            self.perform_choreography(backdrop_file)#pass the backdrop file address

    def perform_choreography(self, filepath):
        config = configparser.ConfigParser() # Creating an istance of ConfigParser
        # ConfigParser is used to handle configuration files in the INI file format,
        # which consists of sections, each containing key-value pairs. Our .txt file is in the same format format. 
        config.optionxform = str  # Preserve case sensitivity of section names
        config.read(filepath) # Read the .txt file which is in the same the directory 

        # Load backdrop image from the choregraphy.txt file
        backdrop_filepath = config.get('Backdrop', 'filepath')
        self.backdrop = Backdrop(backdrop_filepath)

        # Load lights form the choregraphy.txt file
        light_sections = [section for section in config.sections() if section != 'Backdrop']
        for section in light_sections:
            color = config.get(section, 'color')
            position = eval(config.get(section, 'position'))
            direction = config.getint(section, 'direction')
            intensity = config.getfloat(section, 'intensity')
            distribution = eval(config.get(section, 'distribution'))
            light = Light(color, position, direction, intensity, distribution)
            self.add_light(light)

    #Now let's create a method to add lights on plot
    def add_light(self, light):
        self.lights.append(light)
        spread = np.array(light.distribution)
        cone = self.ax.fill(spread[:, 0], spread[:, 1], color=light.color, alpha=0.4)[0]
        light.cone = cone
        self.cones.append(cone)
    
    # Here is the method to add pops/singers/audience on the stage
    def add_pop(self, x, y, color='YELLOW'):
        pop = self.ax.text(x, y, "P", fontsize=20, color=color)
        self.pops.append(pop)
    
    # This mehtod is to amimate the lights 
    def animate_lights(self, frame):
        for light in self.lights:
            light.blink()
            cone_color = light.color
            light.cone.set_color(cone_color)

            light.calculate_cone()  # Calculate the light cone with adjusted intensity

        # This loop is to move the pops on the stage randomly
        for pop in self.pops:
            x, y = pop.get_position()
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            x += dx
            y += dy
            pop.set_position((x, y))

        # Now let's plot the elements on the stage
        self.ax.clear()
        self.ax.set_xlim([0, 540])
        self.ax.set_ylim([150, 620])
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('white')

        # Now for displaying the backdrop image
        if self.backdrop is not None:
            self.backdrop.display(self.ax)  
        
        # Now let's add an image for the front stage
        if self.backdrop is not None:
            self.backdrop.display(self.ax)  # Display the backdrop image
            backdrop_image = Image.open("image_for_stage.jpg")
            self.ax.imshow(backdrop_image, extent=[0, 580, 410, 610])

        for cone in self.cones:
            self.ax.add_patch(cone)

        for pop in self.pops:
            self.ax.text(pop.get_position()[0], pop.get_position()[1], "🎤", fontsize=20, color='BLACK')

        self.smoke_machine.generate_smoke('moore')
        self.smoke_machine.plot_smoke(self.ax)

    # To simulate lights
    def simulate_lights(self):
        self.smoke_machine = SmokeMachine([250, 420], 90, 0.5)

        # Animate lights on and disply them on plot
        self.animation = FuncAnimation(self.fig, self.animate_lights, interval=100)

        plt.suptitle(self.title, fontsize=18)
        plt.show()

# Create the Stage instance
stage = StageChoreography()

choreography = input('Please select the configuration you want to load. \n1 for Configuration 1 \n2 for configuration 2\n')
if(choreography == "1"):
    stage.perform_choreography('choreography1.txt')
elif(choreography == "2"):
    stage.perform_choreography('choreography2.txt')
else:
    print("Loading default configuration")
    stage.perform_choreography('choreography1.txt')




# Add 200 random people (audience)
for _ in range(200):
    x = random.uniform(20, 500)
    y = random.uniform(200, 380)
    stage.add_pop(x, y)

# Add 12 pops on the stage (singers)
for _ in range(12):
    x = random.uniform(0, 500)
    y = random.uniform(400, 600)
    stage.add_pop(x, y)
stage.simulate_lights()

