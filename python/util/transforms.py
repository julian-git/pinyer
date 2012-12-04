from math import sin, cos, pi

def extract_transform(transform):
    if transform is None:
        return [None, None]
    p1 = transform.index('translate(')
    t = transform[p1+10 : transform.index(')', p1+10)].split(' ')
    translation = [float(t[0]), float(t[1])]
    p2 = transform.index('rotate(')
    angle = float(transform[p2+7 : transform.index(')', p2+7)])
    return [translation, angle]

def make_transform(translation, angle):
    return 'translate(' + str(translation[0]) + ',' + str(translation[1]) + ') ' + \
        'rotate(' + str(angle) + ')'

def apply_transform(id, translation, angle, coos):
    coo = coos[id]
    if angle is not None:
        alpha = angle * pi/180
        coo = [coo[0] * cos(alpha) - coo[1] * sin(alpha), \
                     coo[0] * sin(alpha) + coo[1] * cos(alpha)]
    if translation is not None:
        coo = [coo[0] + translation[0], coo[1] + translation[1]]
    coos[id] = [round(coo[0],2), round(coo[1], 2)]
    return coos

def view_mapping(translation):
    return translation
#    return [translation[0], round(translation[1]/1.2, 2)]
