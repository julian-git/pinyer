from math import cos, sin, pi
from html_common import svg_rect, svg_head

def ring(period, i, r, rect_dim, init_svg_id, position_at, coo_of):
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
    position_at: The dictionary telling the id of an element at the position (j, s)
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
                    role = 'ma'
                else:
                    c = 'vt'  # Vent
                    role = 'vent'
            else:
                c = 'q'       # Quesito
                role = 'pinya'
            x=round(r*cos(a), 2)
            y=round(r*sin(a), 2)
            alpha = round(a*180/pi, 2)
            svg = svg + svg_rect.substitute(_x=x, _y=y, \
                                                _rx=-0.5*rect_dim['w'], _ry=-0.5*rect_dim['h'], \
                                                _rw=rect_dim['w'], _rh=rect_dim['h'], \
                                                _alpha=alpha, \
                                                _svg_id=svg_id, _class=c, _name=svg_id, \
                                                _index_props=[i,j,m])
            position_at[i,j,m] = dict([('svg_id', svg_id), \
                                           ('role', role), \
                                           ('svg_text', role), \
                                           ('x', x), \
                                           ('y', y), \
                                           ('angle', alpha)])
            coo_of[svg_id] = [x,y]
    return [svg, svg_id, position_at, coo_of]


def make_rings(rd):
    r = rd['start_radius'] + (rd['end_n_in_slice'] - rd['start_n_in_slice']) * rd['radius_offset']
    svg = svg_head.substitute(_vx=-r-40, _vy=-r-40, _vw=2*r+80, _vh=2*r+80) 
    svg += '<g id="pos">'
    svg_id = 0
    r = rd['start_radius']
    position_at = dict()
    coo_of = dict()
    for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
        [_svg, svg_id, position_at, coo_of] = \
            ring(rd['period'], i, r, rd['rect_dim'], svg_id, position_at, coo_of) 
        svg += _svg
        r += rd['radius_offset']
    svg += '</g>'
    return [svg, position_at, coo_of]

def make_ring_relations(rd, position_at, tolerances):
    relations = []
    # the default values for all relations created in this function
    rel0 = dict([('from_pos_id', None), \
                     ('to_pos_id', None), \
                     ('relation_type', 1), \
                     ('field_name', 'shoulder_height'), \
                     ('pos_list', None), \
                     ('fparam1', tolerances['height']), \
                     ('pos_type', None)])

    # first, the relations between rengles de mans and rengles de vents
    for j in range(2*rd['period']):
        if j%2 == 0:
            pt = 'ma'  # Ma
        else:
            pt = 'vt'  # Vent
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            rel = rel0.copy()
            rel['from_pos_id'] = position_at[i,j,0]['svg_id']
            rel['to_pos_id'] = position_at[i+1,j,0]['svg_id']
            rel['pos_type'] = pt
            relations.append(rel)

    # next, the relations in the quesitos
    # of these, first the shoulder_height relations between different rings
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            for m in range(1, i+1):
                rel = rel0.copy()
                rel['from_pos_id'] = position_at[i,j,m]['svg_id']
                rel['to_pos_id'] = position_at[i+1,j,m]['svg_id']
                rel['pos_type'] = 'p'
                relations.append(rel) # quesito

                rel1 = rel.copy()
                rel1['to_pos_id'] = position_at[i+1,j,m+1]['svg_id']
                relations.append(rel1) # quesito

    # next, the relations for the shoulder_width
    rel0['relation_type'] = 3
    rel0['field_name'] = 'shoulder_width'
    rel0['fparam1'] = tolerances['width']
    rel0['pos_type'] = 'p'
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
            rel = rel0.copy()
            rel['pos_list'] = str(position_at[i,j,1]['svg_id'])
            for m in range(2, i+1):
                rel['pos_list'] += '_' + str(position_at[i,j,m]['svg_id'])
            relations.append(rel)

    return relations

def make_relations_svg(relations, coo_of):
    relations_svg = '<g id="rels">'
    for rel in relations:
        if rel['relation_type'] == 1:
            relations_svg += '<path class="' + rel['pos_type'] + '" d="M' + \
                str(coo_of[rel['from_pos_id']][0]) + ',' + \
                str(coo_of[rel['from_pos_id']][1]) + 'L' + \
                str(coo_of[rel['to_pos_id']][0]) + ',' + \
                str(coo_of[rel['to_pos_id']][1]) + '"/>'
        elif rel['relation_type'] == 3:
            pos_list = rel['pos_list'].split('_')
            relations_svg += '<path class="' + rel['pos_type'] + '" d="M' + \
                str(coo_of[int(pos_list[0])][0]) + ',' + \
                str(coo_of[int(pos_list[0])][1])
            for pos in pos_list[1:]:
                relations_svg += 'L' + \
                    str(coo_of[int(pos)][0]) + ',' + \
                    str(coo_of[int(pos)][1])
            relations_svg += '"/>'
                
        else:
            raise RuntimeError('drawing of relation not implemented')
    return relations_svg + '</g>'

def tresde8f():
    ring_data = dict([('period', 3), ('start_n_in_slice', 1), ('end_n_in_slice', 3), \
                      ('start_radius', 100), ('radius_offset', 35), \
                      ('rect_dim', dict([('w',20),('h',40)]))])
    [svg, position_at, coo_of] = make_rings(ring_data) 
    # the tolerance in height between successive mans, vents, and pinya,
    # and in width between adjacent pinya in the same ring
    tolerances = dict([('height', 5), ('width', 6)])
    relations = make_ring_relations(ring_data, position_at, tolerances)
    svg += make_relations_svg(relations, coo_of) + '</svg>'
    return [svg, position_at, relations]

def save_tresde8f_relations():
    [svg, position_at, relations] = tresde8f()
    from db_interaction import get_db, write_positions, write_relations
    db = get_db()
    c = db.cursor()
    c.execute("delete from castell_position where castell_type_id = 3")
    c.execute("delete from castell_relation where castell_type_id = 3")
    write_positions(db, 3, position_at)
    write_relations(db, 3, relations)
    db.commit()
    
if __name__ == "__main__":
#     save_tresde8f_relations()
    print tresde8f()
