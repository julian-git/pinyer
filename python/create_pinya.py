from math import cos, sin, pi
from html_common import svg_rect

def ring(period, n_in_slice, r, dim):
    """
    create the svg elements in the outer rings.
    period = k if the ring has 2pi/k symmetry
    n_in_slice: how many people between each of the rays at 2pi j / k
    r: the radius of the ring
    dim: The dimensions of the box to place, of the form {w:20 h:30}
    """
    svg = ''
    svg_id = 0
    dyn_props = ''
    for j in range(2*period):
        for s in range(n_in_slice+1):
            a = 2 * pi * ( j  + (s)/float(n_in_slice + 1) ) / float(2*period)
            svg_id = svg_id + 1
            if s == 0:
                if j%2 == 0:
                    c = 'ma'
                else:
                    c = 'vent'
            else:
                c = 'quesito'
            svg = svg + svg_rect.substitute(_x=round(r*cos(a), 2), _y=round(r*sin(a), 2), \
                                                _w=dim['w'], _h=dim['h'], \
                                                _svg_id=svg_id, _class=c, _name=svg_id, _dyn_props=dyn_props)
    return svg


if __name__ == "__main__":
    print ring(2, 3, 100, dict([('w',20),('h',40)]))
