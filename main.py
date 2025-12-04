import numpy as np
import pygame as pg
import sys, threading, time, random, json

ORANGE = (200, 150, 0)
RED = (255, 0, 0)
BABY_BLUE = (0, 255, 255)


"""
NOTES

"""

SCALE_FACTOR = 10 # number of pixels that corresponds to 1m
WAVE_SPEED = 100 # pixels/sec


waves_list = []

start = False
run = False


print("""
      
      -- How to use --
      /help for a list of commands
      
      """)


# handles setup commands
def setup_cmds():

    #        width, height, fps, time, res (particles per pixel)
    consts = [1600, 800,    60,    0.5,     1]

    setup_cmd = input("Do you want to select settings?(y/n)\n>> ")

    if setup_cmd.strip().lower() == "y":
        
        consts[0] = float(input("Width in pixels\n>> "))
        consts[1] = float(input("Height in pixels\n>> "))
        consts[2] = float(input("FPS goal\n>> "))
        consts[3] = float(input("Timestep\n>> "))
        consts[4] = float(input("Res of waves\n>> "))

        print("Settings applied")

    if setup_cmd.strip().lower() == "n":
        
        print("Default settings applied")

    return consts

# handles live commands
def live_cmds():
    
    while True:
        cmd = input(">> ")

        try:

            if cmd.strip().lower() == "/help":
                print("""
                    -- List of Commands --
                    
                    - Use _ if you want to keep the default value
                    - ID, sine = sine wave, long = longitudinal wave
                    
                    Start the Simulation:
                    /start
                    
                    Load Preset
                    /load 'preset name'
                    
                    Save Preset
                    /save 'preset name'
                    
                    Clear All Waves
                    /cls
                    
                    Version
                    /version
                    
                    
                    Create Wave:
                    /w 'name' 'ID' 'direction' 'wave_length' 'frequency' 'amplitude' 'delta'
                    
                    Draw Wave:
                    /w-d 'name' 'color (RGB)' 'particle_size' 'y offset'
                    
                    Update Wave:
                    /w-update 'name' 'attribute' 'new value'
                    
                    Delete Wave: 
                    /w-delete 'name'
                    
                    Wipe Wave (keep the wave but remove it from the visualisation):
                    /w-wipe 'name'
                    
                    Add Waves:
                    /w-add 'number of waves' 'name new wave' 'ID' 'name wave 1' 'name wave 2' ... 'name wave n'
                    
                    Show Current Waves:
                    /w-list
                    
                    Show Wave Attributes:
                    /w-attributes 'name'
                
                    """)

    # Program Commands
        # Start Simulation
            elif cmd.strip().lower().split(" ")[0] == "/start":
                global run
                run = True
                
        # Save Preset
            elif cmd.strip().lower().split(" ")[0] == "/save":
                
                name = cmd.split(" ")[1]
                
                waves_list_packed = []
                
                for wave in waves_list:

                    x = wave.__dict__.copy()
                    x.pop("noise_class", None)
                    x.pop("x_pos", None)
                    
                    waves_list_packed.append(x)
                
                with open(f"presets/{name}.json", "w") as f:
                    json.dump(waves_list_packed, f, indent=4)
                    
        # Load Preset
            elif cmd.strip().lower().split(" ")[0] == "/load":
                
                name = cmd.split(" ")[1]
                
                
                for i in range(len(waves_list)):
                        
                    waves_list.pop()
                
                
                with open(f"presets/{name}.json", "r") as f:
                    waves_list_packed = json.load(f)
                    
                waves_to_add = unpack_preset(waves_list_packed)
                
                for wave in waves_to_add:
                    
                    waves_list.append(wave)

        # Clear All Waves
            elif cmd.strip().lower() == "/cls":
                
                for i in range(len(waves_list)):
                    
                    waves_list.pop()

        # Version
            elif cmd.strip().lower() == "/version":
                
                with open(f"data/info.json", "r") as f:
                    info = json.load(f)
                    
                print(f"Version: {info[0]["version"]}")


    # Wave creation and manipulation
        # Create Wave
            elif cmd.strip().lower().split(" ")[0] == "/w":

                name = cmd.split(" ")[1]
                ID = cmd.split(" ")[2]

                if ID == "sine":
                    wave = wave_object(name=name, ID=0)

                if ID == "long":
                    wave = wave_object(name=name, ID=2)

                try:
                    if cmd.split(" ")[3] != "_":
                        direction = cmd.split(" ")[3]
                        wave.direction = direction
                except: pass

                try:
                    if cmd.split(" ")[4] != "_":
                        velocity = float(cmd.split(" ")[4])
                        wave.velocity = velocity
                except: pass

                try:
                    if cmd.split(" ")[5] != "_":
                        frequency = float(cmd.split(" ")[5])
                        wave.frequency = frequency
                except: pass
                    
                try:
                    if cmd.split(" ")[6] != "_":
                        amplitude = float(cmd.split(" ")[6])
                        wave.amplitude = amplitude
                except: pass    
                    
                try:
                    if cmd.split(" ")[7] != "_":
                        delta = float(cmd.split(" ")[7])
                        wave.delta = delta
                except: pass
                
                waves_list.append(wave)

        # Draw Wave
            elif cmd.strip().lower().split(" ")[0] == "/w-d":

                name = cmd.split(" ")[1]

                for k, wave in enumerate(waves_list):
                    if wave.name == name:

                        i = 0

                        try:
                            if cmd.split(" ")[2] != "_":
                                r = int(cmd.split(" ")[2])
                                g = int(cmd.split(" ")[3])
                                b = int(cmd.split(" ")[4])
                                wave.color = (r, g, b)
                            else: i = -2
                        except: pass

                        try:
                            if cmd.split(" ")[5 + i] != "_":
                                particle_size = float(cmd.split(" ")[5 + i])
                                wave.particle_size = particle_size
                        except: pass
                        
                        try:
                            if cmd.split(" ")[6 + i] != "_":
                                y_offset = float(cmd.split(" ")[6 + i])
                                wave.y_offset = y_offset
                        except: pass

                        wave.draw = True

        # Update Wave
            elif cmd.strip().lower().split(" ")[0] == "/w-update":
                
                name = cmd.split(" ")[1]
                
                attribute = cmd.split(" ")[2]
                new_value = cmd.split(" ")[3]
                
                for wave, wave in enumerate(waves_list):
                
                    if wave.name == name:
                
                        if attribute == "name":
                            wave.name = new_value
                        
                        if attribute == "direction":
                            wave.direction = new_value
                            
                        if attribute == "velocity":
                            wave.velocity = float(new_value)
                            wave.update_wave_length()
                            
                        if attribute == "frequency":
                            wave.frequency = float(new_value)
                            wave.update_wave_length()
                            
                        if attribute == "amplitude":
                            wave.amplitude = float(new_value)
                            
                        if attribute == "delta":
                            wave.delta = float(new_value)
                            
                        if attribute == "color":
                            r = int(cmd.split(" ")[3])
                            g = int(cmd.split(" ")[4])
                            b = int(cmd.split(" ")[5])
                            wave.color = (r, g, b)
                            
                        if attribute == "particle_size":
                            wave.particle_size = int(new_value)
                            
                        if attribute == "y_offset":
                            wave.y_offset = float(new_value)
                            
        # Delete Wave
            elif cmd.strip().lower().split(" ")[0] == "/w-delete":
                
                name = cmd.split(" ")[1]
                
                for wave in waves_list:
                
                    if wave.name == name:
                    
                        waves_list.remove(wave)

        # Wipe Wave
            elif cmd.strip().lower().split(" ")[0] == "/w-wipe":
                
                name = cmd.split(" ")[1]
                
                for wave in waves_list:
                
                    if wave.name == name:
                    
                        wave.draw = False
        
        # Add Waves
            elif cmd.strip().lower().split(" ")[0] == "/w-add":

                no = int(cmd.split(" ")[1])

                name_new_wave = cmd.split(" ")[2]

                i = cmd.split(" ")[3]

                if i == "sine": i = 0
                if i == "long": i = 2

                wave_name_to_add = []

                for wave in range(3, no + 3):

                    name = cmd.split(" ")[wave]

                    wave_name_to_add.append(name)

                wave = wave_object(name=name_new_wave, wave_name_to_add=wave_name_to_add, ID=i)

                waves_list.append(wave)
                
        # Show Current Waves
            elif cmd.strip().lower().split(" ")[0] == "/w-list":
                
                print("Existing waves")
                
                for wave in waves_list:
                    
                    print(f"{wave.name} - drawn: {wave.draw}")
                    
        # Show Wave Attributes
            elif cmd.strip().lower().split(" ")[0] == "/w-attributes":
                
                name = cmd.split(" ")[1]
                
                for wave in waves_list:
                
                    if wave.name == name and (wave.ID == 0 or wave.ID == 2):
                        
                        print(f"Direction: {wave.direction}")
                        print(f"Velocity: {wave.velocity}")
                        print(f"Frequency: {wave.frequency}")
                        print(f"Amplitude: {wave.amplitude}")
                        print(f"Wave Length: {wave.wave_length}")
                        print(f"Delta: {wave.delta}")
                        print(f"Color: {wave.color}")
                        print(f"Particle Size: {wave.particle_size}")
                        print(f"Y Offset: {wave.y_offset}")
                        
                    if wave.name == name and (wave.ID == 1 or wave.ID == 3):
                        
                        print(f"Names of Waves Added: {wave.wave_name_to_add}")
                        print(f"Color: {wave.color}")
                        print(f"Particle Size: {wave.particle_size}")
                        print(f"Y Offset: {wave.y_offset}")
                        
        # Play Wave
            elif cmd.strip().lower().split(" ")[0] == "/w-play":
                
                name = cmd.split(" ")[1]
                
                for wave in waves_list:

                    pass
                
                    #if wave.name == name: play(wave)

        # Demos
            elif cmd.strip().lower().split(" ")[0] == "/d1":

                basic_waves = [
                    wave_object(name="y1", ID=0), 
                    wave_object(name="y2", direction="negative", ID=0),
                    wave_object(name="ya", wave_name_to_add=["y1", "y2"], color=(200, 150, 0), y_offset=300, ID=1)
                    ]
                
                for wave in basic_waves:

                    wave.draw = True

                    waves_list.append(wave)
                
                run = True

        except Exception as e:
            print("Command not Valid")
            print(e)

# unpacks the .json for wave presets
def unpack_preset(data):
    
    waves = []
    
    for wave_dict in data:
        
        if wave_dict["ID"] == 0 or wave_dict["ID"] == 2:
            wave_obj = wave_object(
                # basic information
                name=wave_dict["name"],
                ID=wave_dict["ID"],

                # drawing properties
                draw=wave_dict["draw"],
                particle_size=wave_dict["particle_size"],
                y_offset=wave_dict["y_offset"],
                color=wave_dict["color"],

                # wave properties for standard waves
                frequency=wave_dict["frequency"],
                wave_length=wave_dict["wave_length"],
                velocity=wave_dict["velocity"],
                direction=wave_dict["direction"],
                amplitude=wave_dict["amplitude"],
                delta=wave_dict["delta"],

                # extras
                noisy=wave_dict["noisy"],
            )
            
        elif wave_dict["ID"] == 1 or wave_dict["ID"] == 3:
            wave_obj = wave_object(
                # basic information
                name=wave_dict["name"],
                ID=wave_dict["ID"],

                # drawing properties
                draw=wave_dict["draw"],
                particle_size=wave_dict["particle_size"],
                y_offset=wave_dict["y_offset"],
                color=wave_dict["color"],
                
                # wave properties for wave addition
                wave_name_to_add=wave_dict["wave_name_to_add"],

                # extras
                noisy=wave_dict["noisy"],
            )
            
        waves.append(wave_obj)
        
    return waves

# generate constants
constants = setup_cmds()

# start the commands thread to enable live commands
live_cmd_thread = threading.Thread(target=live_cmds, daemon=True)
live_cmd_thread.start()



# Global constants
WIDTH = constants[0]
HEIGHT = constants[1]

FRAME_RATE_GOAL = constants[2]
TIME_STEP_FACTOR = constants[3]

RES = constants[4]
NUM = int((WIDTH - WIDTH / 5) * constants[4])

WAVE_RANGE =  WIDTH - 2*(WIDTH / 10)
Y_RANGE = 50

# for positions of particles along x
x_pos_particles = np.linspace(0, WAVE_RANGE, NUM)

# create a noise map for longitudinal waves - uniform dist between -1 and 1
y_noise_map = np.array([((random.random() - 0.5) * 2 * Y_RANGE) for _ in x_pos_particles])

# class for creating a guass noise map
class noise_map():
    def __init__(self, tick=0):

        self.tick = tick
        self.noise_map = self.gauss_nosie_map()

    def gauss_nosie_map(self, scale=10):

        noise_map = np.random.normal(loc=0, scale=scale, size=x_pos_particles.shape)

        return noise_map


# Main class containing the wave object
class wave_object():
        
    def __init__(
            self, 

            # basic wave information
            name,
            ID=0,
            x_pos=None,

            # drawing properties
            draw=True,
            particle_size=2,
            y_offset=100,
            color=RED,

            # wave properties for standard waves
            direction="positive", 
            velocity=WAVE_SPEED,
            wave_length=0,
            frequency=1.0625, 
            amplitude=50,
            delta=np.pi / 2,

            # wave properties for wave addition
            wave_name_to_add=None,

            # extras
            noisy=False,
            ):
        
        self.name = name
        self.ID = ID
        self.x_pos = x_pos

        self.draw = draw
        self.color = color
        self.particle_size = particle_size
        self.y_offset = y_offset

        self.frequency = frequency
        self.wave_length = velocity / self.frequency
        self.velocity = velocity
        self.direction = direction
        self.amplitude = amplitude
        self.delta = delta

        self.wave_name_to_add = wave_name_to_add

        self.noisy = noisy

        self.noise_class = noise_map()



    # Functions for simple waves        
    def calc_sine_wave(self, t, x=x_pos_particles):
        
        def y_sine(x, t):
            # calculate w: angular frequency, k: wavenumber
            w = 2*np.pi * self.frequency
            k = w / (self.velocity)
            
            if self.direction == "positive":
                return self.amplitude * np.cos(k * x - w * t + self.delta)
            
            if self.direction == "negative":
                return self.amplitude * np.cos(k * x + w * t + self.delta)

        if self.noisy:
            pos_array = [x + WIDTH / 10, y_sine(x, t) + self.noise_class.noise_map]
            
            
        
        else:
            pos_array = [x + WIDTH / 10, y_sine(x, t)]

        self.x_pos = pos_array
    

        
    def calc_long_wave(self, t, x=x_pos_particles):
        
        def x_long(x, t):
            # calculate w: angular frequency, k: wavenumber
            w = 2*np.pi * self.frequency
            k = w / (self.velocity)
            
            if self.direction == "positive":
                return x + self.amplitude * np.cos(w * t - k * x ) + WIDTH / 10
            
            if self.direction == "negative":
                return x + self.amplitude * np.cos(w * t + k * x ) + WIDTH / 10

        pos_array = [x_long(x, t), y_noise_map]

        self.x_pos = pos_array
    

    # Functions for wave products
    def calc_sine_wave_product(self, wave_list):

        pos_array = np.zeros((2, len(x_pos_particles)))
        pos_array[0] = x_pos_particles + WIDTH / 10

        waves_to_add = []
        for wave in wave_list:
            
            if wave.name in set(self.wave_name_to_add):
                waves_to_add.append(wave)

        for wave in waves_to_add:

            pos_array[1] = pos_array[1] + wave.x_pos[1]
        
        self.x_pos = pos_array

    def calc_long_wave_product(self, t, wave_list):

        pos_array = np.zeros((2, len(x_pos_particles)))
        pos_array[1] = y_noise_map

        waves_to_add = []

        for wave in wave_list:

            if wave.name in set(self.wave_name_to_add):

                waves_to_add.append(wave)

        for wave in waves_to_add:

            pos_array[0] = pos_array[0] + wave.x_pos[0] / len(waves_to_add)
        
        self.x_pos = pos_array



# Function for updating simulation
def update_simulation(waves_list, t):
    
    for wave in waves_list:
        
        if wave.ID == 0:
            wave.calc_sine_wave(t)

        if wave.ID == 1:
            wave.calc_sine_wave_product(waves_list)

        if wave.ID == 2:
            wave.calc_long_wave(t)

        if wave.ID == 3:
            wave.calc_long_wave_product(t, waves_list)

# Functions for rendering
def draw(waves_list):
    
    def draw_particles(*waves):

        for wave in waves:

            for i in range(len(wave.x_pos[0])):
                
                pg.draw.circle(
                        screen, 
                        wave.color,
                        (wave.x_pos[0][i], wave.x_pos[1][i] + wave.y_offset), # position of particle
                        wave.particle_size
                        )

    def draw_line(*waves):

        points = []

        # create an array of points on the wave
        for wave in waves:

            for i in range(len(wave.x_pos[0])):

                points.append([wave.x_pos[0][i], wave.x_pos[1][i] + wave.y_offset])

        # draw the waves
        pg.draw.lines(
            screen,
            wave.color,
            False,
            points,
            wave.particle_size
        )
    
    for wave in waves_list:

        if wave.draw:

            if wave.ID == 0:
                draw_line(wave)

            if wave.ID == 1:
                draw_line(wave)

            if wave.ID == 2:
                draw_particles(wave)

            if wave.ID == 3:
                draw_particles(wave)


# Logic for GUI
while not start:
    time.sleep(20 / 1000)
    
    if run:
        start = True

# Set up display
pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Simple Wave Simulation")

font = pg.font.Font(None, 20)

# timing
clock = pg.time.Clock()
t = 0
tst = 0

UPDATE_RATE_GOAL = 1000
UPDATE_DT = 1.0 / UPDATE_RATE_GOAL

accumulator = 0.0
last_time = time.perf_counter()

update_simulation(waves_list, t)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # --- Timing ---
    now = time.perf_counter()
    update_run_time = now - last_time
    last_time = now
    accumulator += update_run_time
    
    # --- Simulation ---
    while accumulator >= UPDATE_DT:
        
        update_simulation(waves_list, t)

        t += TIME_STEP_FACTOR / UPDATE_RATE_GOAL
        
        accumulator -= UPDATE_DT



    # --- Rendering ---
    screen.fill((0, 0, 0))
    
    # Draw and update variables at the framerate
    draw(waves_list)

    # Get the current FPS
    ups_text = font.render(f"UPS: {UPDATE_RATE_GOAL}", True, (255, 255, 255))
    
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))

    screen.blit(ups_text, (10, 10))
    screen.blit(fps_text, (10, 25))
    
    pg.display.flip()
    clock.tick(FRAME_RATE_GOAL)

# Quit Pygame
pg.quit()
sys.exit()