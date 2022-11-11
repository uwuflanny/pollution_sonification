
class measures:

    def init(self, index, data):
        
        pass

# general
min_thresh      = 50
max_thresh      = 500

# aqi
bad             = 50
moderate        = 100
severe          = 150
unhealthy       = 200
very_unhealthy  = 300
hazardous       = 500

# residue
RES_DECADENCE   = 1.8

# audio generation
WAVETABLE_SIZE  = 8192
SAMPLE_RATE     = 48000
BPM             = 120
SIGN_NUM        = 4
SIGN_DEN        = 4


def convert(index, data):

    global min_thresh, max_thresh, bad, moderate, severe, unhealthy, very_unhealthy, hazardous

    cap = 500 if max(data) <= 500 else max(data)
    max_thresh = cap
    hazardous = cap
    
    if index == "pm25":
        min_thresh      = 12
        bad             = 12
        moderate        = 35
        severe          = 55
        unhealthy       = 150
        very_unhealthy  = 250

    if index == "pm10":
        min_thresh      = 54
        bad             = 54
        moderate        = 154
        severe          = 254
        unhealthy       = 355
        very_unhealthy  = 424

