
# general
MIN_THRESH      = 50
MAX_THRESH      = 500

# aqi
BAD             = 50
MODERATE        = 100
SEVERE          = 150
UNHEALTHY       = 200
VERY_UNHEALTHY  = 300
HAZARDOUS       = 500

# residue
RES_DECADENCE   = 1.8

# audio generation
WAVETABLE_SIZE  = 8192
SAMPLE_RATE     = 44100
BPM             = 120
SIGN_NUM        = 4
SIGN_DEN        = 4


def convert(index):

    if index == "pm25" or index == "pm10":
        MIN_THRESH      = 12
        MAX_THRESH      = 500
        BAD             = 12
        MODERATE        = 35
        SEVERE          = 55
        UNHEALTHY       = 150
        VERY_UNHEALTHY  = 250
        HAZARDOUS       = 500
