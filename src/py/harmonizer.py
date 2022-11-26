
def get_harmonization(data):

    # scales
    major           = [0, 2, 4, 5, 7, 9, 11]
    minor           = [0, 2, 3, 5, 7, 8, 10]
    melodic_minor   = [0, 2, 3, 5, 7, 9, 11]
    harmonic_minor  = [0, 2, 3, 5, 7, 8, 11]

    scales = [
        major,
        minor,
        melodic_minor,
        harmonic_minor
    ]

    # get scale based on average aqi
    # avg = sum(data) / len(data)
    # scale = scales[(int)(-1 if avg // 50 > len(scales)-1 else avg // 50)]
    scale = major

    # voice scale and return, scale is multiplied in more octaves
    key = 36
    return [x + key + 12 for x in scale] + [x + key + 24 for x in scale] + [x + key + 36 for x in scale] + [x + key + 48 for x in scale]

    
    



    
