from math import cos, sin, pi
from html_common import svg_rect, svg_head

def ring(period, i, r, rect_dim, init_svg_id, position_id_at):
    """
    create the svg elements in the outer rings.
    period = k if the ring has 2pi/k symmetry
    i: the index of the ring; also, how many people are between each of the rays at 2pi j / k
    r: the radius of the ring
    rect_dim: The dimensions of the box to place, of the form {w:20 h:30}
    init_svg_id: The first free id for an svg element

    returns:
    svg: the string with the svg representation
    svg_id: the next free id number
    position_id_at: The dictionary telling the id of an element at the position (j, s)
    """
    svg = ''
    dyn_props = ''
    svg_id = init_svg_id
    for j in range(2*period):
        for m in range(i+1):
            a = 2 * pi * ( j  + m / float(i + 1) ) / float(2*period)
            svg_id = svg_id + 1
            if m == 0:
                if j%2 == 0:
                    c = 'ma'
                else:
                    c = 'vent'
            else:
                c = 'quesito'
            svg = svg + svg_rect.substitute(_x=round(r*cos(a), 2), _y=round(r*sin(a), 2), \
                                                _rx=-0.5*rect_dim['w'], _ry=-0.5*rect_dim['h'], \
                                                _rw=rect_dim['w'], _rh=rect_dim['h'], \
                                                _alpha=a*180/pi, \
                                                _svg_id=svg_id, _class=c, _name=svg_id, \
                                                _index_props=[i,j,m])
            position_id_at[i,j,m] = svg_id
    return [svg, svg_id, position_id_at]


def make_rings(rd):
    r = rd['start_radius'] + (rd['end_n_in_slice'] - rd['start_n_in_slice']) * rd['radius_offset']
    svg = svg_head.substitute(_vx=-r-40, _vy=-r-40, _vw=2*r+80, _vh=2*r+80)
    svg_id = 0
    r = rd['start_radius']
    position_id_at = dict()
    for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
        [_svg, svg_id, position_id_at] = ring(rd['period'], i, r, rd['rect_dim'], svg_id, position_id_at) 
        svg = svg + _svg
        r += rd['radius_offset']
    return [svg + '</svg>', position_id_at]

def make_ring_relations(rd, position_id_at, tolerance):
    relations = []
    print position_id_at
    # first, the relations between rengles de mans and rengles de vents
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            relations.append(dict([('from_pos_id', position_id_at[i,j,0]), \
                                       ('to_pos_id', position_id_at[i+1,j,0]), \
                                       ('relation_type', 1), \
                                       ('field_name', 'shoulder_height'), \
                                       ('fparam1', tolerance)]))
    return relations

def make_relations_svg(relations):
    return str(relations)

def tresde8f():
    ring_data = dict([('period', 3), ('start_n_in_slice', 1), ('end_n_in_slice', 3), \
                      ('start_radius', 100), ('radius_offset', 35), \
                      ('rect_dim', dict([('w',20),('h',40)]))])
    [svg, position_id_at] = make_rings(ring_data) 
    tolerance = 5 # the tolerance in height between successive mans and vents
    relations = make_ring_relations(ring_data, position_id_at, tolerance)
    relations_svg = make_relations_svg(relations)
    return svg + relations_svg

if __name__ == "__main__":
    print tresde8f()
