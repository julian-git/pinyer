from math import cos, sin, pi
from html_common import svg_rect, svg_head

def ring(period, n_in_slice, r, dim, init_svg_id):
    """
    create the svg elements in the outer rings.
    period = k if the ring has 2pi/k symmetry
    n_in_slice: how many people between each of the rays at 2pi j / k
    r: the radius of the ring
    dim: The dimensions of the box to place, of the form {w:20 h:30}
    """
    svg = ''
    dyn_props = ''
    svg_id = init_svg_id
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
                                                _rx=-0.5*dim['w'], _ry=-0.5*dim['h'],
                                                _rw=dim['w'], _rh=dim['h'], \
                                                _alpha=a*180/pi, \
                                                _svg_id=svg_id, _class=c, _name=svg_id, \
                                                _index_props=[j,s])
    return [svg, svg_id]


def make_rings(period, start_n_in_slice, end_n_in_slice, start_radius, radius_offset, dim):
    r = start_radius + (end_n_in_slice - start_n_in_slice) * radius_offset
    svg = svg_head.substitute(_vx=-r-40, _vy=-r-40, _vw=2*r+80, _vh=2*r+80)
    svg_id = 0
    r = start_radius
    for s in range(start_n_in_slice, end_n_in_slice+1):
        [_svg, svg_id] = ring(period, s, r, dim, svg_id) 
        svg = svg + _svg
        r += radius_offset
    return svg + '</svg>'

def tresde8f():
    return make_rings(3, 1, 3, 100, 50, dict([('w',20),('h',40)])) 


if __name__ == "__main__":
    print make_rings(2, 1, 1, 100, 50, dict([('w',20),('h',40)]))
