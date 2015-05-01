#!/usr/bin/env python
import os

for f in os.listdir('videos'):
    if f.endswith(".wav.mp4"):
    	print f
        new_name = 'videos/' + f.split('.')[0] + '.mp4'
        os.rename('videos/' + str(f), new_name)