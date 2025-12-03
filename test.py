import numpy as np
import random


x_pos_particles = np.array([0, 1, 2, 3, 4])
frequency = 1
velocity = 1
direction = "positive"
amplitude = 10
delta = 0
WIDTH = 10

def calc_sine_wave_new(t, x=x_pos_particles):
        
    def y_sine(x, t):
        # calculate w: angular frequency, k: wavenumber
        w = 2*np.pi * frequency
        k = w / (velocity)
        
        if direction == "positive":
            return amplitude * np.cos(k * x - w * t + delta)
        
        if direction == "negative":
            return amplitude * np.cos(k * x + w * t + delta)

    pos_array = [x + WIDTH / 10, y_sine(x, t)]

    return pos_array

print(calc_sine_wave_new(0))