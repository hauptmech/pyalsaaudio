#!/usr/bin/env python

# Simple test script that plays (some) wav files

from __future__ import print_function

import sys
import wave
import getopt
import alsaaudio

def play(device, f):    

    
    periodsize = device.getperiodsize() 
    data = f.readframes(periodsize)
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(periodsize)


def usage():
    print('usage: playwav.py [-d <device>] <file>', file=sys.stderr)
    sys.exit(2)

if __name__ == '__main__':

    device = 'default'

    opts, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in opts:
        if o == '-d':
            device = a

    if not args:
        usage()
        
    f = wave.open(args[0], 'rb')

    dataformat = 0
    # 8bit is unsigned in wav files
    if f.getsampwidth() == 1:
        dataformat = alsaaudio.PCM_FORMAT_U8
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        dataformat = alsaaudio.PCM_FORMAT_S16_LE
    elif f.getsampwidth() == 3:
        dataformat = alsaaudio.PCM_FORMAT_S24_LE
    elif f.getsampwidth() == 4:
        dataformat = alsaaudio.PCM_FORMAT_S32_LE
    else:
        raise ValueError('Unsupported format')



    device = alsaaudio.PCM(
                device=device,
                rate=f.getframerate(),
                latency=499952,
                channels=f.getnchannels(),
                fmt=dataformat
            )


    play(device, f)

    f.close()
