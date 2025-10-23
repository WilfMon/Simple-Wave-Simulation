import numpy as np
import pygame as pg
import sys

# Set up display
pg.init()

WIDTH, HEIGHT = 1200, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Simple Wave Simulation")


FRAME_RATE_GOAL = 60
TIME_STEP_FACTOR = 0.5

RES = 0.5
WAVE_RANGE =  WIDTH - 2*(WIDTH / 10)

# for positions of particles along x
x_pos_particles = np.arange(0, WIDTH - 2*(WIDTH / 10) + 1, RES)
#print(x_pos_particles)



class sine_wave():
        
    def __init__(
            self, 
            direction="positive", 
            wave_len=WAVE_RANGE / 8, 
            freq=0.5, 
            A=20,
            delta=np.pi / 2
            ):
        
        self.direction = direction
        self.wave_len = wave_len
        self.freq = freq
        self.A = A
        self.delta = delta

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
        
    def calc_sine_wave(self, t, x=x_pos_particles, color=(255, 0, 0), particle_size=1, y_offset=100):

        pos_array = []

        for i in x:

            pos_array.append([self.x_sine(i), self.y_sine(i, t)])

        return (pos_array, color, particle_size, y_offset)
    


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

    def draw_sine_waves(self, *waves):

        for wave in waves:

            #print(x_array[1], x_array[2], x_array[3])

            for i in range(len(wave[0])):

                pg.draw.circle(
                    screen, 
                    wave[1],
                    (wave[0][i][0], wave[0][i][1] + wave[3]), # position of particle
                    wave[2]
                    ) 
            


clock = pg.time.Clock()
t = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # black screen
    screen.fill((0, 0, 0))
    
    # main logic

    y1 = sine_wave()
    y2 = sine_wave(direction="negative")

    y_12 = add_wave()

    ya = sine_wave(wave_len=(WAVE_RANGE / 30), freq=0.6, A=36)
    ya2 = sine_wave(wave_len=(WAVE_RANGE / 30), freq=0.6, A=36, direction="negative")

    yb = sine_wave(wave_len=(WAVE_RANGE / 4), A=30)
    yb2 = sine_wave(wave_len=(WAVE_RANGE / 4), A=30, direction="negative")

    y_ab = add_wave()

    visulalisation = draw_pygame()
    visulalisation.draw_sine_waves(
        y1.calc_sine_wave(t, color=(0, 255, 255)),
        y2.calc_sine_wave(t, color=(0, 255, 255)),

        y_12.calc_wave(y1.calc_sine_wave(t), y2.calc_sine_wave(t), y_offset=200, color=(0, 0, 255)),

        ya.calc_sine_wave(t, y_offset=450),
        ya2.calc_sine_wave(t, y_offset=450),
        yb.calc_sine_wave(t, y_offset=450),
        yb2.calc_sine_wave(t, y_offset=450),

        y_ab.calc_wave(ya.calc_sine_wave(t), ya2.calc_sine_wave(t), yb.calc_sine_wave(t), yb2.calc_sine_wave(t), y_offset=650)
    )

    # Update display
    t += TIME_STEP_FACTOR / FRAME_RATE_GOAL
    pg.display.flip()
    clock.tick(FRAME_RATE_GOAL)
    #print(f"frame: {int(t * 60)}")

# Quit Pygame
pg.quit()
sys.exit()