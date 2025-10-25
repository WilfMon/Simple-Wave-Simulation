import numpy as np
import pygame as pg
import sys, threading, time



"""
NOTES

- 100 pixels = 1m

"""



waves_list = []
axis_list = []

start = False
run = False

def setup_cmds():

    #       width height fps time res
    consts = [1200, 800, 60, 1, 1]

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

def live_cmds():
    
    while True:
        cmd = input(">> ")

        if cmd.strip().lower() == "/help":
            print("""
                -- List of Commands --
                
                - Use _ if you want to keep the default value
                  
                Start the Simulation:
                /start
                  
                Create Wave:
                /w 'name' 'direction' 'wave_lengh' 'frequency' 'amplitude' 'delta'
                
                Draw Wave:
                /w-d 'name' 'color (RGB)' 'particle_size' 'y offset'
                  
                Update Wave:
                /w-update 'name' 'attribute' 'new value'
                
                Delete Wave: 
                /w-delete 'name'
                  
                Wipe Wave (keep the wave but remove it from the visualisation):
                /w-wipe 'name'
                
                Add Waves: (max 10)
                /w-add 'number of waves' 'name new wave' 'name wave 1' 'name wave 2' ... 'name wave n'
                  
                Show Current Waves:
                /w-list
                  
                Draw Axis:
                /a-d 'name'
                
                Create Basic Setup:
                /basic
                """)

    # Start Simulation
        if cmd.strip().lower().split(" ")[0] == "/start":
            global run
            run = True

    # Create Wave
        if cmd.strip().lower().split(" ")[0] == "/w":

            name = cmd.split(" ")[1]

            wave = sine_wave(name=name)
            axis = axis_for_wave(name=name)


            try:
                if cmd.split(" ")[2] != "_":
                    direction = cmd.split(" ")[2]
                    wave.direction = direction
            except: pass

            try:
                if cmd.split(" ")[3] != "_":
                    wave_lengh = float(cmd.split(" ")[3])
                    wave.wave_len = wave_lengh
            except: pass

            try:
                if cmd.split(" ")[4] != "_":
                    frequency = float(cmd.split(" ")[4])
                    wave.freq = frequency
            except: pass
                
            try:
                if cmd.split(" ")[5] != "_":
                    amplitude = float(cmd.split(" ")[5])
                    wave.A = amplitude
            except: pass    
                
            try:
                if cmd.split(" ")[6] != "_":
                    delta = float(cmd.split(" ")[6])
                    wave.delta = delta
            except: pass
            
            waves_list.append(wave)
            axis_list.append(axis)

    # Draw Wave
        if cmd.strip().lower().split(" ")[0] == "/w-d":

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

                            axis_list[k].y_offset = y_offset
                    except: pass

                    wave.draw = True

    # Update Wave
        if cmd.strip().lower().split(" ")[0] == "/w-update":
            
            name = cmd.split(" ")[1]
            
            attribute = cmd.split(" ")[2]
            new_value = cmd.split(" ")[3]
            
            for wave, wave in enumerate(waves_list):
            
                if wave.name == name:
            
                    if attribute == "name":
                        wave.name = new_value
                    
                    if attribute == "direction":
                        wave.direction = new_value
                        
                    if attribute == "wave_lengh":
                        wave.wave_lengh = new_value
                        
                    if attribute == "frequency":
                        wave.frequency = new_value
                        
                    if attribute == "amplitude":
                        wave.amplitude = new_value
                        
                    if attribute == "delta":
                        wave.delta = new_value
                        
                    if attribute == "color":
                        r = int(cmd.split(" ")[3])
                        g = int(cmd.split(" ")[4])
                        b = int(cmd.split(" ")[5])
                        wave.color = (r, g, b)
                        
                    if attribute == "particle_size":
                        wave.particle_size = new_value
                        
                    if attribute == "y_offset":
                        wave.y_offset = new_value
                        axis_list[wave].y_offset = y_offset
                        
    # Delete Wave
        if cmd.strip().lower().split(" ")[0] == "/w-delete":
            
            name = cmd.split(" ")[1]
            
            for wave in waves_list:
            
                if wave.name == name:
                
                    waves_list.remove(wave)

    # Wipe Wave
        if cmd.strip().lower().split(" ")[0] == "/w-wipe":
            
            name = cmd.split(" ")[1]
            
            for wave in waves_list:
            
                if wave.name == name:
                
                    wave.draw = False
    
    # Add Waves
        if cmd.strip().lower().split(" ")[0] == "/w-add":

            no = int(cmd.split(" ")[1])

            name_new_wave = cmd.split(" ")[2]

            wave_name_to_add = []

            for wave in range(3, no + 3):

                name = cmd.split(" ")[wave]

                wave_name_to_add.append(name)

            wave = sine_wave_product(name=name_new_wave, wave_name_to_add=wave_name_to_add)

            waves_list.append(wave)
            
    # Show Current Waves
        if cmd.strip().lower().split(" ")[0] == "/w-list":
            
            print("Existing waves")
            for wave in waves_list:
                
                print(f"{wave.name} - drawn: {wave.draw}")

    # Draw Axis
        if cmd.strip().lower().split(" ")[0] == "/a-d":

            name = cmd.split(" ")[1]

            for axis in axis_list:
                if axis.name == name:

                    axis.draw = True

    # Create Basic Setup
        if cmd.strip().lower().split(" ")[0] == "/basic":
            
            basic_waves = [sine_wave(name="y1"), sine_wave(name="y2", direction="negative", y_offset=200), sine_wave_product(name="ya", wave_name_to_add=["y1", "y2"], color=(200, 150, 0), y_offset=300)]
            
            for wave in basic_waves:

                wave.draw = True

                waves_list.append(wave)
            
            run = True

    # Debugging
        if cmd.strip().lower().split(" ")[0] == "/debug1":

            basic_waves = [
                sine_wave(name="y1"), 
                sine_wave(name="y2", direction="negative", wave_lengh=30),
                sine_wave(name="y3", direction="positive", wave_lengh=30),
                sine_wave_product(name="ya", wave_name_to_add=["y1", "y2", "y3"], color=(200, 150, 0), y_offset=300)
                ]
            
            for wave in basic_waves:

                wave.draw = True

                waves_list.append(wave)
            
            run = True

        if cmd.strip().lower().split(" ")[0] == "/debug2":

            basic_waves = [
                sine_wave(name="y1", direction="positive", wave_lengh=30),
                sine_wave(name="y2", direction="negative", wave_lengh=36),
                sine_wave_product(name="ya", wave_name_to_add=["y1", "y2"], color=(200, 150, 0), y_offset=300)
                ]
            
            for wave in basic_waves:

                wave.draw = True

                waves_list.append(wave)
            
            run = True

        


constants = setup_cmds()

live_cmd_thread = threading.Thread(target=live_cmds, daemon=True)
live_cmd_thread.start()



WIDTH = constants[0]
HEIGHT = constants[1]

FRAME_RATE_GOAL = constants[2]
TIME_STEP_FACTOR = constants[3]

RES = constants[4]

WAVE_RANGE =  WIDTH - 2*(WIDTH / 10)

# for positions of particles along x
x_pos_particles = np.arange(0, WAVE_RANGE + 1, RES)



class sine_wave():
        
    def __init__(
            self, 
            name,
            ID=0,
            draw=False,
            direction="positive", 
            wave_lengh=WAVE_RANGE / 8, 
            frequency=0.5, 
            amplitude=20,
            delta=np.pi / 2,
            color=(255, 0, 0),
            particle_size=2,
            y_offset=100,
            ):
        
        self.name = name
        self.ID = ID
        self.draw = draw

        self.direction = direction
        self.wave_len = wave_lengh
        self.freq = frequency
        self.A = amplitude
        self.delta = delta

        self.color = color
        self.particle_size = particle_size
        self.y_offset = y_offset

# functions for simple sine waves
    def x_sine(self, i):
        return i + WIDTH / 10

    def y_sine(self, x, t):

        # calculate w: angular frequency, k: wavenumber
        w = 2*np.pi * self.freq
        k = w / (self.wave_len * self.freq)
        
        if self.direction == "positive":
            return self.A * np.cos(k * x - w * t + self.delta)
        
        if self.direction == "negative":
            return self.A * np.cos(k * x + w * t + self.delta)
        
    def calc_sine_wave(self, t, x=x_pos_particles):

        pos_array = []

        for i in x:

            pos_array.append([self.x_sine(i), self.y_sine(i, t)])

        return (pos_array, self.color, self.particle_size, self.y_offset)
    


class sine_wave_product():

    def __init__(
            self,
            name,
            wave_name_to_add,
            ID=1,
            draw=False,
            color=(255, 0, 0),
            particle_size=2,
            y_offset=100,
            ):
        
        self.name = name
        self.ID = ID
        self.draw = draw

        self.wave_name_to_add = wave_name_to_add

        self.color = color
        self.particle_size = particle_size
        self.y_offset = y_offset

    def calc_wave_product(self, t, wave_list):

        pos_array = np.zeros((len(x_pos_particles), 2), dtype=int)

        waves_to_add = []

        for wave2 in wave_list:

            if wave2.name in set(self.wave_name_to_add):

                waves_to_add.append(wave2)

        for wave3 in waves_to_add:

            wave3 = wave3.calc_sine_wave(t)

            for i in range(len(wave3[0])):

                pos_array[i][0] = x_pos_particles[i] + WIDTH / 10
                pos_array[i][1] = pos_array[i][1] + wave3[0][i][1]

        
        return (pos_array, self.color, self.particle_size, self.y_offset)
        


class axis_for_wave():
    def __init__(
            self,
            name,
            draw=False,
            color=(155, 155, 155),
            start_pos_x=WIDTH / 10,
            end_pos_x=WIDTH - WIDTH / 10,
            y_offset=100
            ):
        
        self.name = name
        self.draw = draw

        self.color = color

        self.start_pos = (start_pos_x, y_offset)
        self.end_pos = (end_pos_x, y_offset)



class draw_pygame():
    def __init__(self):
        pass

    def draw_particles(self, *waves):

        for wave in waves:

            for i in range(len(wave[0])):

                pg.draw.circle(
                    screen, 
                    wave[1],
                    (wave[0][i][0], wave[0][i][1] + wave[3]), # position of particle
                    wave[2]
                    )
                
    def draw_axis(self, *axis):

        for ax in axis:

            pg.draw.line(
                        screen, 
                        color=ax.color,
                        start_pos=ax.start_pos,
                        end_pos=ax.end_pos
                        )



while not start:
    time.sleep(20 / 1000)
    
    if run:
        start = True

# Set up display
pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Simple Wave Simulation")

#print(len(x_pos_particles))

font = pg.font.Font(None, 20)

clock = pg.time.Clock()
t = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # black screen
    screen.fill((0, 0, 0))



    for wave in waves_list:

        if wave.draw:

            visulalisation = draw_pygame()

            if wave.ID == 0:
                visulalisation.draw_particles(wave.calc_sine_wave(t))

            if wave.ID == 1:
                visulalisation.draw_particles(wave.calc_wave_product(t, waves_list))

        
    for axis in axis_list:

        if axis.draw:
        
            visulalisation.draw_axis(axis)

    

    # Get the current FPS
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))

    screen.blit(fps_text, (10, 10))

    # Update display
    t += TIME_STEP_FACTOR / FRAME_RATE_GOAL
    pg.display.flip()
    clock.tick(FRAME_RATE_GOAL)
    #print(f"frame: {int(t * 60)}")

    particles = pg.sprite.Group()

# Quit Pygame
pg.quit()
sys.exit()