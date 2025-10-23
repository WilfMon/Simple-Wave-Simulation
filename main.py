import numpy as np
import pygame as pg
import sys, threading



waves_list = []
waves_to_draw = []

def console():
    while True:
        cmd = input(">> ")

        if cmd.strip().lower() == "help":
            print("""
                -- List of Commands --
                  
                create a sine wave: /w 'name' 'direction' 'wave lengh' 'frequency' 'amplitude' 'delta'
                draw a wave: /d 'name' 'color (RGB)' 'particle size' 'y offset'
                  
                delete a wave: /w-delete 'name'
                  
                update properties of sine wave: /w-'name' 'property' 'value'

                """)
            

        if cmd.strip().lower().split(" ")[0] == "/w":

            name = cmd.split(" ")[1]

            a = sine_wave(name=name)

            try:
                direction = cmd.split(" ")[2]
                a.direction = direction
            except:
                pass

            try:
                wave_lengh = float(cmd.split(" ")[3])
                a.wave_len = wave_lengh
            except:
                pass

            try:
                frequency = float(cmd.split(" ")[4])
                a.freq = frequency
            except:
                pass
            
            try:
                amplitude = float(cmd.split(" ")[5])
                a.A = amplitude
            except:
                pass

            try:
                delta = float(cmd.split(" ")[6])
                a.delta = delta
            except:
                pass

            waves_list.append(a)

        if cmd.strip().lower().split(" ")[0] == "/d":

            name = cmd.split(" ")[1]

            for wave in waves_list:
                if wave.name == name:

                    try:
                        r = int(cmd.split(" ")[2])
                        g = int(cmd.split(" ")[3])
                        b = int(cmd.split(" ")[4])
                        wave.color = (r, g, b)
                    except:
                        pass

                    try:
                        particle_size = float(cmd.split(" ")[5])
                        wave.particle_size = particle_size
                    except:
                        pass

                    try:
                        y_offset = float(cmd.split(" ")[6])
                        wave.y_offset = y_offset
                    except:
                        pass

                    waves_to_draw.append(wave)

            
            


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
            wave_len=WAVE_RANGE / 8, 
            freq=0.5, 
            A=20,
            delta=np.pi / 2,
            color=(255, 0, 0),
            particle_size=2,
            y_offset=100,
            ):
        
        self.name = name
        self.direction = direction
        self.wave_len = wave_len
        self.freq = freq
        self.A = A
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