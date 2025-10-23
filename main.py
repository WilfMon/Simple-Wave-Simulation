import numpy as np
import pygame as pg
import sys, threading, time



waves_list = []
waves_to_draw = []

start = False
run = False

def console():
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
                /d 'name' 'color (RGB)' 'particle_size' 'y offset'
                  
                Update Wave:
                /w-update 'name' 'attribute' 'new value'
                
                Delete Wave: 
                /w-delete 'name'
                
                Show Current Waves:
                /w-list
                
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

            a = sine_wave(name=name)

            try:
                if cmd.split(" ")[2] != "_":
                    direction = cmd.split(" ")[2]
                    a.direction = direction
            except: pass

            try:
                if cmd.split(" ")[3] != "_":
                    wave_lengh = float(cmd.split(" ")[3])
                    a.wave_len = wave_lengh
            except: pass

            try:
                if cmd.split(" ")[4] != "_":
                    frequency = float(cmd.split(" ")[4])
                    a.freq = frequency
            except: pass
                
            try:
                if cmd.split(" ")[5] != "_":
                    amplitude = float(cmd.split(" ")[5])
                    a.A = amplitude
            except: pass    
                
            try:
                if cmd.split(" ")[6] != "_":
                    delta = float(cmd.split(" ")[6])
                    a.delta = delta
            except: pass
            
            waves_list.append(a)

    # Draw Wave
        if cmd.strip().lower().split(" ")[0] == "/d":

            name = cmd.split(" ")[1]

            for wave in waves_list:
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

                    waves_to_draw.append(wave)

    # Update Wave
        if cmd.strip().lower().split(" ")[0] == "/w-update":
            
            name = cmd.split(" ")[1]
            
            attribute = cmd.split(" ")[2]
            new_value = cmd.split(" ")[3]
            
            for i, wave in enumerate(waves_list):
            
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
                        
                    waves_list[i] = wave
                    
                    try:
                        waves_to_draw[i] = wave
                    except:
                        pass      
        
    # Delete Wave
        if cmd.strip().lower().split(" ")[0] == "/w-delete":
            
            name = cmd.split(" ")[1]
            
            for wave in waves_list:
            
                if wave.name == name:
                
                    waves_list.remove(wave)
                    
                    try:
                        waves_to_draw.remove(wave)
                    except:
                        pass
    
    # Show Current Waves
        if cmd.strip().lower().split(" ")[0] == "/w-list":
            
            print("Existing waves")
            for i in waves_list:
                
                print(f"- {i.name}")
                
            print("Drawn waves")
            for i in waves_to_draw:
                
                print(f"- {i.name}")

    # Create Basic Setup
        if cmd.strip().lower().split(" ")[0] == "/basic":
            
            basic_waves = [sine_wave(name="y1"), sine_wave(name="y2", direction="negative", y_offset=200)]
            
            for wave in basic_waves:
                waves_list.append(wave)
                waves_to_draw.append(wave)
            
            run = True


console_thread = threading.Thread(target=console, daemon=True)
console_thread.start()



WIDTH, HEIGHT = 1200, 800

FRAME_RATE_GOAL = 60
FIXED_DT = 1 / FRAME_RATE_GOAL
TIME_STEP_FACTOR = 1

RES = 0.5
WAVE_RANGE =  WIDTH - 2*(WIDTH / 10)

# for positions of particles along x
x_pos_particles = np.arange(0, WIDTH - 2*(WIDTH / 10) + 1, RES)



class sine_wave():
        
    def __init__(
            self, 
            name,
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
    


class add_wave():
    def __init__(self):
        pass

    def calc_wave(self, *waves, color=(255, 0, 0), particle_size=1, y_offset=100):

        pos_array = np.zeros((len(x_pos_particles), 2), dtype=int)

        for wave in waves:

            for i in range(len(wave[0])):

                pos_array[i][0] = x_pos_particles[i] + WIDTH / 10
                pos_array[i][1] = pos_array[i][1] + wave[0][i][1]

        
        return (pos_array, color, particle_size, y_offset)
        


class draw_pygame():
    def __init__(self):
        pass

    def create_particles(self, *waves):

        for wave in waves:

            for i in range(len(wave[0])):

                pg.draw.circle(
                    screen, 
                    wave[1],
                    (wave[0][i][0], wave[0][i][1] + wave[3]), # position of particle
                    wave[2]
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


    for wave in waves_to_draw:

        visulalisation = draw_pygame()
        visulalisation.create_particles(
            wave.calc_sine_wave(t)
        )

    """
    # main logic
    y1 = sine_wave()
    y2 = sine_wave(delta=2.1, A=10, wave_len=50, freq=1.2)

    y_12 = add_wave()

    ya = sine_wave(wave_len=(WAVE_RANGE / 30), freq=0.6, A=36)
    ya2 = sine_wave(wave_len=(WAVE_RANGE / 30), freq=0.6, A=36, direction="negative")

    yb = sine_wave(wave_len=(WAVE_RANGE / 4), A=30)
    yb2 = sine_wave(wave_len=(WAVE_RANGE / 4), A=30, direction="negative")

    y_ab = add_wave()

    visulalisation = draw_pygame()
    visulalisation.create_particles(
        y1.calc_sine_wave(t, color=(0, 255, 255)),
        y2.calc_sine_wave(t, color=(0, 255, 255)),

        y_12.calc_wave(y1.calc_sine_wave(t), y2.calc_sine_wave(t), y_offset=200, color=(0, 0, 255)),

        ya.calc_sine_wave(t, y_offset=450),
        ya2.calc_sine_wave(t, y_offset=450),
        yb.calc_sine_wave(t, y_offset=450),
        yb2.calc_sine_wave(t, y_offset=450),

        y_ab.calc_wave(ya.calc_sine_wave(t), ya2.calc_sine_wave(t), yb.calc_sine_wave(t), yb2.calc_sine_wave(t), y_offset=650)
    )
    """
    

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