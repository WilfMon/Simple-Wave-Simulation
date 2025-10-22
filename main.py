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
x_pos_particles = np.arange(0, WIDTH - 2*(WIDTH / 10) + 1, RES)
print(x_pos_particles)



class sine_wave():
        
    def __init__(self, direction="positive", wave_len=100, freq=0.5, A=20):
        
        self.direction = direction
        self.wave_len = wave_len
        self.freq = freq
        self.A = A

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

# functions for simple pulses of waves
    def draw_pulse(self, x_arr, t, y_offset, color=(255, 0, 0), particle_size=2):
        
        for x in x_arr:
            pg.draw.circle(
                screen, 
                color,
                (self.x_sine(x), self.y_sine(x, t) + y_offset), # position of particle
                particle_size
                )
            
            
            
# class for handling pulse logic
class sine_wave_pulse():
    def __init__(self):
        self.particle_info_array = []
        
    # function to create values of the particles
    def draw_string_pulse(self, x1, x2, y_offset, color=(255, 0, 0), particle_size=2):
        
        for i in np.arange(x1, x2, RES):
            
            self.particle_info_array.append([i, y_offset, color, particle_size])
            
        #for i in range(len(self.particle_pos_array)):
            #print(self.particle_pos_array[i][0], "1")
    
    # functions to draw the particles and move them and even update time to zero
    def draw_pulse_moving(self, t, pulse_lengh=40):
        
        wave = sine_wave()
        
        # calculate where the pulse is along the particles
        new_t = False
        particle_pulse_array = []

        tc = int(t * 60)
        
        if tc == int((WIDTH - 2*(WIDTH / 10)) / RES - pulse_lengh - 1):
            new_t = - pulse_lengh / 60
        
        for i in range(tc, pulse_lengh + tc):
            particle_pulse_array.append(int(x_pos_particles[i]))
            
        print(particle_pulse_array)
        print(len(particle_pulse_array))
        
        particle_pos_array = []     
        for i in range(len(self.particle_info_array)):
            particle_pos_array.append(self.particle_info_array[i][0])
        
        particle_stationary_array = particle_pos_array.copy()
        
        # add the new positions into the list of the line
        for i in range(len(particle_pos_array)):
            #print(particle_pos_array[i])
            if particle_pos_array[i] == particle_pulse_array[0]:
            
                #print(particle_pos_array[i + pulse_lengh - 1], particle_pulse_array[-1])
                #print(np.argmax(particle_pos_array))
                #print(particle_pulse_array[-1] / RES)
                    
                i_of_pulse = np.arange(i, pulse_lengh + i) % len(particle_pos_array)
                
                print(i_of_pulse)
                print(len(i_of_pulse))
                particle_stationary_array = np.delete(particle_pos_array, i_of_pulse)
                    
                break
        
        # draw the new positions
        for i in range(len(self.particle_info_array)):
            
            if i < len(particle_stationary_array):
                
                x = particle_stationary_array[i]
                
                pg.draw.circle(
                    screen, 
                    self.particle_info_array[i][2],
                    (wave.x_sine(x), self.particle_info_array[i][1]), # position of particle
                    self.particle_info_array[i][3]
                    )
            
            if i < len(particle_pulse_array):
                
                x = particle_pulse_array[i]
                
                pg.draw.circle(
                    screen, 
                    self.particle_info_array[i][2],
                    (wave.x_sine(x), wave.y_sine(x, t) + self.particle_info_array[i][1]), # position of particle
                    self.particle_info_array[i][3]
                    )
        
        return new_t
                



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
    for i in x_pos_particles:
        
        i_wave.draw_wave(i, t, y_offset=100, color=(255, 0, 0))
        
        r_wave.draw_wave(i, t, y_offset=100, color=(0, 0, 255))
        
    for i in x_pos_particles:
        
        # control how far down the screen the wave is displayed
        y_offset = 200
        
        x = r_wave.x_sine(i)
        y = r_wave.y_sine(i, t) + i_wave.y_sine(i, t) + y_offset
        
        pg.draw.circle(screen, (0, 255, 0), (x, y), 2)

    
    
    pulse_on_line = sine_wave_pulse()
        
    pulse_on_line.draw_string_pulse(x1=0, x2=320, y_offset=600)
    pulse_on_line.draw_string_pulse(x1=320, x2=640, y_offset=600, particle_size=4)
    pulse_on_line.draw_string_pulse(x1=640, x2=960, y_offset=600)
    
    new_t = pulse_on_line.draw_pulse_moving(t)
    
    if new_t != False:
        t = new_t
        

    # Update display
    t += 1 / 60
    pg.display.flip()
    clock.tick(60)
    #print(f"frame: {int(t * 60)}")

# Quit Pygame
pg.quit()
sys.exit()