from math import cos, sin, pi
from html_common import svg_rect, svg_head

def ring(period, i, r, rect_dim, init_svg_id, position_id_at, coo_of):
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
    coo_of: the coordinates of an element with a certain id
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
                    c = 'ma'  # Ma
                else:
                    c = 'vt'  # Vent
            else:
                c = 'q'       # Quesito
            x=round(r*cos(a), 2)
            y=round(r*sin(a), 2)
            svg = svg + svg_rect.substitute(_x=x, _y=y, \
                                                _rx=-0.5*rect_dim['w'], _ry=-0.5*rect_dim['h'], \
                                                _rw=rect_dim['w'], _rh=rect_dim['h'], \
                                                _alpha=a*180/pi, \
                                                _svg_id=svg_id, _class=c, _name=svg_id, \
                                                _index_props=[i,j,m])
            position_id_at[i,j,m] = svg_id
            coo_of[svg_id] = [x,y]
    return [svg, svg_id, position_id_at, coo_of]


def make_rings(rd):
    r = rd['start_radius'] + (rd['end_n_in_slice'] - rd['start_n_in_slice']) * rd['radius_offset']
    svg = svg_head.substitute(_vx=-r-40, _vy=-r-40, _vw=2*r+80, _vh=2*r+80) 
    svg += '<g id="pos">'
    svg_id = 0
    r = rd['start_radius']
    position_id_at = dict()
    coo_of = dict()
    for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
        [_svg, svg_id, position_id_at, coo_of] = \
            ring(rd['period'], i, r, rd['rect_dim'], svg_id, position_id_at, coo_of) 
        svg += _svg
        r += rd['radius_offset']
    svg += '</g>'
    return [svg, position_id_at, coo_of]

def make_ring_relations(rd, position_id_at, tolerance):
    relations = []

    # first, the relations between rengles de mans and rengles de vents
    for j in range(2*rd['period']):
        if j%2 == 0:
            pt = 'ma'  # Ma
        else:
            pt = 'vt'  # Vent
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            relations.append(dict([('from_pos_id', position_id_at[i,j,0]), \
                                       ('to_pos_id', position_id_at[i+1,j,0]), \
                                       ('relation_type', 1), \
                                       ('field_name', 'shoulder_height'), \
                                       ('fparam1', tolerance), \
                                       ('pos_type', pt)]))

    # next, the relations in the quesitos
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            for m in range(1, i+1):
                relations.append(dict([('from_pos_id', position_id_at[i,j,m]), \
                                           ('to_pos_id', position_id_at[i+1,j,m]), \
                                           ('relation_type', 1), \
                                           ('field_name', 'shoulder_height'), \
                                           ('fparam1', tolerance), \
                                           ('pos_type', 'q')])) # quesito
                relations.append(dict([('from_pos_id', position_id_at[i,j,m]), \
                                           ('to_pos_id', position_id_at[i+1,j,m+1]), \
                                           ('relation_type', 1), \
                                           ('field_name', 'shoulder_height'), \
                                           ('fparam1', tolerance), \
                                           ('pos_type', 'q')])) # quesito
    return relations

def make_relations_svg(relations, coo_of):
    relations_svg = '<g id="rels">'
    for rel in relations:
        relations_svg += '<path class="' + rel['pos_type'] + '" d="M' + \
            str(coo_of[rel['from_pos_id']][0]) + ',' + \
            str(coo_of[rel['from_pos_id']][1]) + 'L' + \
            str(coo_of[rel['to_pos_id']][0]) + ',' + \
            str(coo_of[rel['to_pos_id']][1]) + '"/>'
    return relations_svg + '</g>'

def tresde8f():
    ring_data = dict([('period', 3), ('start_n_in_slice', 1), ('end_n_in_slice', 3), \
                      ('start_radius', 100), ('radius_offset', 35), \
                      ('rect_dim', dict([('w',20),('h',40)]))])
    [svg, position_id_at, coo_of] = make_rings(ring_data) 
    tolerance = 5 # the tolerance in height between successive mans and vents
    relations = make_ring_relations(ring_data, position_id_at, tolerance)
    relations_svg = make_relations_svg(relations, coo_of)
    return svg + relations_svg + '</svg>'

if __name__ == "__main__":
     print tresde8f()
