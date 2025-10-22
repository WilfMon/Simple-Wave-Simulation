import numpy as np
import pygame as pg
import sys



# Set up display
pg.init()

WIDTH, HEIGHT = 1200, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Simple Wave Simulation")


RES = 4
# for positions of particles along x
number_particles = np.arange(1, WIDTH - 2*(WIDTH / 10) + 1, RES)



class sine_wave():
    
    # class for handling pulse logic
    class sine_wave_pulse():
        def __init__(self, pulse_lengh):
            
            self.pulse_lengh = pulse_lengh
            
        def draw_string_pulse(self, y_offset, n, color=(255, 0, 0), particle_size=2):
            
            for i in n:
                pg.draw.circle(
                    screen, 
                    color,
                    (i + WIDTH / 10, y_offset), # position of particle
                    particle_size
                    )
                
        
        
    def __init__(self, direction="positive", wave_len=100, freq=0.5, A=20):
        
        self.direction = direction
        self.wave_len = wave_len
        self.freq = freq
        self.A = A
        
        self.pulse = sine_wave.sine_wave_pulse(self)

# functions for simple sine waves
    def x_sine(self, i):
        return i + WIDTH / 10

    def y_sine(self, x, t):

        # calculate w: angular frequency, k: wavenumber
        w = 2*np.pi * self.freq
        k = w / (self.wave_len * self.freq)
        
        if self.direction == "positive":
            return self.A * np.cos(k * x - w * t)
        
        if self.direction == "negative":
            return self.A * np.cos(k * x + w * t)
        
    def draw_wave(self, x, t, y_offset, color=(255, 0, 0), particle_size=2):
        
        pg.draw.circle(
            screen, 
            color,
            (self.x_sine(x), self.y_sine(x, t) + y_offset), # position of particle
            particle_size
            ) 

# functions for pulses of waves
    def draw_pulse(self, x_arr, t, y_offset, color=(255, 0, 0), particle_size=2):
        
        
        
        for x in x_arr:
            pg.draw.circle(
                screen, 
                color,
                (self.x_sine(x), self.y_sine(x, t) + y_offset), # position of particle
                particle_size
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

    i_wave = sine_wave()
    r_wave = sine_wave(direction="negative")
    for i in number_particles:
        
        i_wave.draw_wave(i, t, y_offset=100, color=(255, 0, 0))
        
        r_wave.draw_wave(i, t, y_offset=100, color=(0, 0, 255))
        
    for i in number_particles:
        
        # control how far down the screen the wave is displayed
        y_offset = 200
        
        x = r_wave.x_sine(i)
        y = r_wave.y_sine(i, t) + i_wave.y_sine(i, t) + y_offset
        
        pg.draw.circle(screen, (0, 255, 0), (x, y), 2)
        
    
    pulse_lengh = 200
    
    p_list = []
    
    tc = int(t * 60)
    
    if tc == int((WIDTH - 2*(WIDTH / 10)) / RES - pulse_lengh - 1):
        t = - pulse_lengh / 60
        tc = - pulse_lengh
    
    for i in range(0 + tc, pulse_lengh + tc):
        
        p_list.append(number_particles[i])

    pulse = sine_wave()
    pulse.draw_pulse(p_list, t, y_offset=400)
    
    pulse_on_line = sine_wave().sine_wave_pulse(pulse_lengh=pulse_lengh).draw_string_pulse(n=number_particles, y_offset=600)
        

    # Update display
    t += 1 / 60
    pg.display.flip()
    clock.tick(60)

# Quit Pygame
pg.quit()
sys.exit()