from math import cos, sin, pi
from html_common import svg_rect, svg_head
from local_config import tolerances

def ring(period, i, r, pinya_rect_dim, init_svg_id, position_in_ring, coo_of):
    """
    create the svg elements in the outer rings.
    period = k if the ring has 2pi/k symmetry
    i: the index of the ring; also, how many people are between each of the rays at 2pi j / k
    r: the radius of the ring
    pinya_rect_dim: The dimensions of the box to place, of the form {w:20 h:30}
    init_svg_id: The first free id for an svg element

    returns:
    svg: the string with the svg representation
    svg_id: the next free id number
    position_in_ring: The dictionary telling the id of an element at the position (j, s)
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
            angle = round(a*180/pi, 2)
            svg += svg_rect.substitute(_x=x, _y=y, \
                                           _rx=-0.5*pinya_rect_dim['w'], _ry=-0.5*pinya_rect_dim['h'], \
                                           _rw=pinya_rect_dim['w'], _rh=pinya_rect_dim['h'], \
                                           _angle=angle, \
                                           _svg_id=svg_id,\
                                           _svg_text = str([i,j,m]), \
                                           #_svg_text=svg_id, \
                                           _class=c, \
                                           _name=svg_id, \
                                           _index_props=[i,j,m])
            position_in_ring[i,j,m] = dict([('svg_id', svg_id), \
                                           ('role', role), \
                                           ('svg_text', role), \
                                           ('x', x), \
                                           ('y', y), \
                                           ('angle', angle)])
            coo_of[svg_id] = [x,y]
    return [svg, svg_id, position_in_ring, coo_of]


def make_rings(rd, svg, svg_id, coo_of):
    r = rd['start_radius']
    position_in_ring = dict()
    for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
        [_svg, svg_id, position_in_ring, coo_of] = \
            ring(rd['period'], i, r, rd['pinya_rect_dim'], svg_id, position_in_ring, coo_of) 
        svg += _svg
        r += rd['radius_offset']
    return [svg, svg_id, position_in_ring, coo_of]

def make_baix(i, j, bd, svg, svg_id, coo_of):
    svg_id = svg_id + 1
    [x,y] = [0,0]
    svg += svg_rect.substitute(_x=bd['baix_pos']['x'], \
                                   _y=bd['baix_pos']['y'],  \
                                   _rx = bd['baix_rect_dim']['x'], \
                                   _ry = bd['baix_rect_dim']['y'], \
                                   _rw = bd['baix_rect_dim']['w'], \
                                   _rh = bd['baix_rect_dim']['h'], \
                                   _angle = bd['baix_rect_dim']['angle'], \
                                   _svg_id=svg_id,\
                                   _svg_text = str([i,j]), \
                                   #_svg_text=svg_id, \
                                   _class='b', \
                                   _name=svg_id, \
                                   _index_props=[i,j])
    coo_of[svg_id] = [x,y]
    return [svg, svg_id, coo_of]

def make_crossa(i, j, bd, svg, svg_id, coo_of):
    svg_id = svg_id + 1
    [x,y] = bd['crossa_pos']
    if j%2 == 0:
        x = -x
    svg += svg_rect.substitute(_x=x, \
                                   _y=y, \
                                   _rx = bd['crossa_rect_dim']['x'], \
                                   _ry = bd['crossa_rect_dim']['y'], \
                                   _rw = bd['crossa_rect_dim']['w'], \
                                   _rh = bd['crossa_rect_dim']['h'], \
                                   _angle = bd['crossa_rect_dim']['angle'], \
                                   _svg_id=svg_id,\
                                   _svg_text = str([i,j]), \
                                   #_svg_text=svg_id, \
                                   _class='cr', \
                                   _name=svg_id, \
                                   _index_props=[i,j])
    coo_of[svg_id] = [x,y]
    return [svg, svg_id, coo_of]

def make_contrafort(i, j, bd, svg, svg_id, coo_of):
    svg_id = svg_id + 1
    [x,y] = bd['contrafort_pos']
    svg += svg_rect.substitute(_x=x, \
                                   _y=y, 
                                   _rx = bd['contrafort_rect_dim']['x'], \
                                   _ry = bd['contrafort_rect_dim']['y'], \
                                   _rw = bd['contrafort_rect_dim']['w'], \
                                   _rh = bd['contrafort_rect_dim']['h'], \
                                   _angle = bd['contrafort_rect_dim']['angle'], \
                                   _svg_id=svg_id,\
                                   _svg_text = str([i,j]), \
                                   #_svg_text=svg_id, \
                                   _class='co', \
                                   _name=svg_id, \
                                   _index_props=[i,j])
    coo_of[svg_id] = [x,y]
    return [svg, svg_id, coo_of]

def make_baix_group(bd, i, svg, svg_id, position_of_baix, coo_of):
    [svg, svg_id, baix, coo_of] = make_baix(i, 0, bd, svg, svg_id, coo_of)
    [svg, svg_id, crossa1, coo_of] = make_crossa(i, 1, bd, svg, svg_id, coo_of)
    [svg, svg_id, crossa2, coo_of] = make_crossa(i, 2, bd, svg, svg_id, coo_of)
    [svg, svg_id, contrafort, coo_of] = make_contrafort(i, 3, bd, svg, svg_id, coo_of)

    position_of_baix[index, 0] = baix
    position_of_baix[index, 1] = crossa1
    position_of_baix[index, 2] = crossa2
    position_of_baix[index, 3] = contrafort

    return [svg, svg_id, position_of_baix, coo_of]

def make_baixos(bd, svg, svg_id, coo_of):
    position_of_baix = dict()
    for i in range(bd['number']):
        [svg, svg_id, position_of_baix, coo_of] = \
            make_baix_group(bd, i, svg, svg_id, position_of_baix, coo_of)
    return [svg, svg_id, position_of_baix, coo_of]

def make_pinya(rd, bd, svg):
    svg += '<g id="pos">'
    svg_id = 0
    coo_of = dict()
    [svg, svg_id, position_in_ring, coo_of] = make_rings(rd, svg, svg_id, coo_of)
    [svg, svg_id, position_of_baix, coo_of] = make_baixos(bd, svg, svg_id, coo_of)
    svg += '</g>' 
    return [svg, position_in_ring, coo_of]


def make_ring_relations(rd, position_in_ring):
    relations = []
    # the default values for all relations created in this function
    rel0 = dict([('pos_list', None), \
                     ('relation_type', 1), \
                     ('field_name', 'shoulder_height'), \
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
            rel['pos_list'] = \
                str(position_in_ring[i,j,0]['svg_id']) + '_' + \
                str(position_in_ring[i+1,j,0]['svg_id'])
            rel['pos_type'] = pt
            relations.append(rel)

    # next, the relations in the quesitos
    # of these, first the shoulder_height relations between different rings
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']):
            for m in range(1, i+1):
                rel = rel0.copy()
                rel['pos_list'] = \
                    str(position_in_ring[i,j,m]['svg_id']) + '_' + \
                    str(position_in_ring[i+1,j,m]['svg_id'])
                rel['pos_type'] = 'p'
                relations.append(rel) # quesito

                rel1 = rel.copy()
                rel1['pos_list'] = \
                    str(position_in_ring[i,j,m]['svg_id']) + '_' + \
                    str(position_in_ring[i+1,j,m+1]['svg_id'])
                relations.append(rel1) # quesito

    # next, the relations for the shoulder_width
    rel0['relation_type'] = 3
    rel0['field_name'] = 'shoulder_width'
    rel0['fparam1'] = tolerances['width']
    rel0['pos_type'] = 'p'
    for j in range(2*rd['period']):
        for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
            rel = rel0.copy()
            rel['pos_list'] = str(position_in_ring[i,j,1]['svg_id'])
            for m in range(2, i+1):
                rel['pos_list'] += '_' + str(position_in_ring[i,j,m]['svg_id'])
            relations.append(rel)

    return relations

def make_relations_svg(relations, coo_of):
    relations_svg = '<g id="rels">'
    for rel in relations:
        pos_list = rel['pos_list'].split('_')
        fpi = int(pos_list[0])
        if len(pos_list) > 1:
            tpi = int(pos_list[1])
        else:
            tpi = fpi
        if rel['relation_type'] == 1:
            relations_svg += '<path class="' + rel['pos_type'] + '" d="M' + \
                str(coo_of[fpi][0]) + ',' + \
                str(coo_of[tpi][1]) + 'L' + \
                str(coo_of[fpi][0]) + ',' + \
                str(coo_of[tpi][1]) + '"/>'
        elif rel['relation_type'] == 3:
            relations_svg += '<path class="' + rel['pos_type'] + '" d="M' + \
                str(coo_of[fpi][0]) + ',' + \
                str(coo_of[fpi][1])
            for pos in pos_list[1:]:
                relations_svg += 'L' + \
                    str(coo_of[int(pos)][0]) + ',' + \
                    str(coo_of[int(pos)][1])
            relations_svg += '"/>'
                
        else:
            raise RuntimeError('drawing of relation not implemented')
    return relations_svg + '</g>'

def tresde8f():
    # data for the rings of the pinya
    rd = dict([('period', 3), ('start_n_in_slice', 1), ('end_n_in_slice', 3), \
                   ('start_radius', 100), ('radius_offset', 35), \
                   ('pinya_rect_dim', dict([('w',20),('h',40)]))])
    r = rd['start_radius'] + (rd['end_n_in_slice'] - rd['start_n_in_slice']) * rd['radius_offset']

    #data for the baixos and crosses
    bd = dict([('number', 3), ('baix_rect_dim', dict([('w', 20), ('h', 40)]))])

    # start the svg
    svg = svg_head.substitute(_vx=-r-40, _vy=-r-40, _vw=2*r+80, _vh=2*r+80) 

    # go!
    [svg, position_in_ring, coo_of] = make_pinya(rd, bd, svg)
    relations = make_ring_relations(rd, position_in_ring)
    svg += make_relations_svg(relations, coo_of) + '</svg>'
    return [svg, position_in_ring, relations]

def save_tresde8f_relations():
    [svg, position_in_ring, relations] = tresde8f()
    from db_interaction import get_db, write_positions, write_relations
    db = get_db()
    c = db.cursor()
    c.execute("delete from castell_position where castell_type_id = 3")
    c.execute("delete from castell_relation where castell_type_id = 3")
    write_positions(db, 3, position_in_ring)
    write_relations(db, 3, relations)
    db.commit()
    
if __name__ == "__main__":
    save_tresde8f_relations()
#    print tresde8f()
