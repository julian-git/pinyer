from math import cos, sin, pi
from local_config import RootDir, pinya_dir
import sys 
sys.path.append(RootDir + 'python/util/')
from xml_common import xml_position, xml_head
from relations import *


def ring(period, i, r, pinya_rect_dim, xml_id, position_in_ring, coo_of):
    """
    create the xml elements in the outer rings of pinya.
    period = k if the ring has 2pi/k symmetry
    i: the index of the ring; also, how many people are between each of the rays at 2pi j / k
    r: the radius of the ring
    pinya_rect_dim: The dimensions of the box to place, of the form {w:20 h:30}
    init_xml_id: The first free id for an xml element

    returns:
    xml: the string with the xml representation
    xml_id: the next free id number
    position_in_ring: The dictionary telling the id of an element at the position (j, s)
    coo_of: the coordinates of an element with a certain id
    """
    xml = ''
    dyn_props = ''
    for j in range(2*period):
        for m in range(i+1):
            a = 2 * pi * ( j  + m / float(i + 1) ) / float(2*period)
            xml_id = xml_id + 1
            if m == 0:
                if j%2 == 0:
                    c = 'ma'  # Ma
                    role = 'ma'
                else:
                    c = 'vent'  # Vent
                    role = 'vent'
            else:
                c = 'pinya'       # Quesito
                role = 'pinya'
            x=round(r*cos(a), 2)
            y=round(r*sin(a), 2)
            angle = round(a*180/pi, 2)
            xml += xml_position.substitute(_x=x, _y=y, \
                                           _rx=-0.5*pinya_rect_dim['w'], _ry=-0.5*pinya_rect_dim['h'], \
                                           _rw=pinya_rect_dim['w'], _rh=pinya_rect_dim['h'], \
                                           _angle=angle, \
                                           _xml_id=xml_id,\
                                           #_xml_text = str([i,j,m]), \
                                           _xml_text=xml_id, \
                                           _class=c, \
                                           _name=xml_id, \
                                           _index_props=[i,j,m])
            position_in_ring[i,j,m] = dict([('xml_id', xml_id), \
                                                ('role', role), \
                                                #('xml_text', role), \
                                                ('xml_text', xml_id), \
                                                ('x', x), \
                                                ('y', y), \
                                                ('angle', angle)])
            coo_of[xml_id] = [x,y]
    return [xml, xml_id, position_in_ring, coo_of]


def rings(rd, xml, xml_id, coo_of):
    """
    make as many rings of pinya as the ringdata rd specifies
    """
    r = rd['start_radius']
    position_in_ring = dict()
    for i in range(rd['start_n_in_slice'], rd['end_n_in_slice']+1):
        [_xml, xml_id, position_in_ring, coo_of] = \
            ring(rd['period'], i, r, rd['pinya_rect_dim'], xml_id, position_in_ring, coo_of) 
        xml += _xml
        r += rd['radius_offset']
    return [xml, xml_id, position_in_ring, coo_of]

def baix(i, j, bd, pibg, xml, xml_id, coo_of):
    """
    make the rectangle and text of a baix
    """
    xml_id = xml_id + 1
    [x,y] = bd['baix_pos']
    xml += xml_position.substitute(_x=x, \
                                   _y=y, \
                                   _rx = bd['baix_rect_dim']['x'], \
                                   _ry = bd['baix_rect_dim']['y'], \
                                   _rw = bd['baix_rect_dim']['w'], \
                                   _rh = bd['baix_rect_dim']['h'], \
                                   _angle = bd['baix_rect_dim']['angle'], \
                                   _xml_id=xml_id,\
                                   #_xml_text = str([i,j]), \
                                   _xml_text=xml_id, \
                                   _class='baix', \
                                   _name=xml_id, \
                                   _index_props=[i,j])
    pibg[i,j] = dict([('xml_id', xml_id), \
                                      ('role', 'baix'), \
                                      #('xml_text', 'baix'), \
                                      ('xml_text', xml_id), \
                                      ('x', x), \
                                      ('y', y), \
                                      ('angle', bd['baix_rect_dim']['angle'])])
    coo_of[xml_id] = [x,y]
    return [xml, xml_id, pibg, coo_of]

def crossa(i, j, bd, pibg, xml, xml_id, coo_of):
    """
    make the rectangle and text of a crossa
    """
    xml_id = xml_id + 1
    [x,y] = bd['crossa_pos']
    alpha = bd['crossa_rect_dim']['angle']
    if j[-1] == '2':
        y = -y
        alpha = -alpha
    xml += xml_position.substitute(_x=x, \
                                   _y=y, \
                                   _rx = bd['crossa_rect_dim']['x'], \
                                   _ry = bd['crossa_rect_dim']['y'], \
                                   _rw = bd['crossa_rect_dim']['w'], \
                                   _rh = bd['crossa_rect_dim']['h'], \
                                   _angle = alpha, \
                                   _xml_id=xml_id,\
                                   #_xml_text = str([i,j]), \
                                   _xml_text=xml_id, \
                                   _class='crossa', \
                                   _name=xml_id, \
                                   _index_props=[i,j])
    pibg[i,j] = dict([('xml_id', xml_id), \
                          ('role', 'crossa'), \
                          #('xml_text', 'crossa'), \
                          ('xml_text', xml_id), \
                          ('x', x), \
                          ('y', y), \
                          ('angle', alpha)])
    coo_of[xml_id] = [x,y]
    return [xml, xml_id, pibg, coo_of]

def contrafort(i, j, bd, pibg, xml, xml_id, coo_of):
    """
    make the rectangle and text of a contrafort
    """
    xml_id = xml_id + 1
    [x,y] = bd['contrafort_pos']
    xml += xml_position.substitute(_x=x, \
                                   _y=y, 
                                   _rx = bd['contrafort_rect_dim']['x'], \
                                   _ry = bd['contrafort_rect_dim']['y'], \
                                   _rw = bd['contrafort_rect_dim']['w'], \
                                   _rh = bd['contrafort_rect_dim']['h'], \
                                   _angle = bd['contrafort_rect_dim']['angle'], \
                                   _xml_id=xml_id,\
                                   #_xml_text = str([i,j]), \
                                   _xml_text=xml_id, \
                                   _class='contrafort', \
                                   _name=xml_id, \
                                   _index_props=[i,j])
    pibg[i,j] = dict([('xml_id', xml_id), \
                          ('role', 'contrafort'), \
                          #('xml_text', 'contrafort'), \
                          ('xml_text', xml_id), \
                          ('x', x), \
                          ('y', y), \
                          ('angle', bd['contrafort_rect_dim']['angle'])])
    coo_of[xml_id] = [x,y]
    return [xml, xml_id, pibg, coo_of]

def agulla(i, j, bd, pibg, xml, xml_id, coo_of):
    """
    make the rectangle and text of an agulla
    """
    xml_id = xml_id + 1
    [x,y] = bd['agulla_pos']
    xml += xml_position.substitute(_x=x, \
                                   _y=y, 
                                   _rx = bd['agulla_rect_dim']['x'], \
                                   _ry = bd['agulla_rect_dim']['y'], \
                                   _rw = bd['agulla_rect_dim']['w'], \
                                   _rh = bd['agulla_rect_dim']['h'], \
                                   _angle = bd['agulla_rect_dim']['angle'], \
                                   _xml_id=xml_id,\
                                   #_xml_text = str([i,j]), \
                                   _xml_text=xml_id, \
                                   _class='agulla', \
                                   _name=xml_id, \
                                   _index_props=[i,j])
    pibg[i,j] = dict([('xml_id', xml_id), \
                          ('role', 'agulla'), \
                          #('xml_text', 'agulla'), \
                          ('xml_text', xml_id), \
                          ('x', x), \
                          ('y', y), \
                          ('angle', bd['agulla_rect_dim']['angle'])])
    coo_of[xml_id] = [x,y]
    return [xml, xml_id, pibg, coo_of]

def lateral(i, j, bd, pibg, xml, xml_id, coo_of):
    """
    make the rectangle and text of a lateral
    """
    xml_id = xml_id + 1
    [x,y] = bd['lateral_pos']
    alpha = bd['lateral_rect_dim']['angle']
    if j[-1] == '2':
        y = -y
        alpha = -alpha
    xml += xml_position.substitute(_x=x, \
                                   _y=y, \
                                   _rx = bd['lateral_rect_dim']['x'], \
                                   _ry = bd['lateral_rect_dim']['y'], \
                                   _rw = bd['lateral_rect_dim']['w'], \
                                   _rh = bd['lateral_rect_dim']['h'], \
                                   _angle = alpha, \
                                   _xml_id=xml_id,\
                                   #_xml_text = str([i,j]), \
                                   _xml_text=xml_id, \
                                   _class='lateral', \
                                   _name=xml_id, \
                                   _index_props=[i,j])
    pibg[i,j] = dict([('xml_id', xml_id), \
                          ('role', 'lateral'), \
                          #('xml_text', 'crossa'), \
                          ('xml_text', xml_id), \
                          ('x', x), \
                          ('y', y), \
                          ('angle', alpha)])
    coo_of[xml_id] = [x,y]
    return [xml, xml_id, pibg, coo_of]

def baix_group(bd, i, xml, xml_id, pibg, coo_of):
    """
    the group consists of the baix, two crosses, one contrafort and an agulla
    """
    [xml, xml_id, pibg, coo_of] = baix(i, 'baix', bd, pibg, xml, xml_id, coo_of)
    [xml, xml_id, pibg, coo_of] = crossa(i, 'crossa1', bd, pibg, xml, xml_id, coo_of)
    [xml, xml_id, pibg, coo_of] = crossa(i, 'crossa2', bd, pibg, xml, xml_id, coo_of)
    [xml, xml_id, pibg, coo_of] = contrafort(i, 'contrafort', bd, pibg, xml, xml_id, coo_of)
    [xml, xml_id, pibg, coo_of] = agulla(i, 'agulla', bd, pibg, xml, xml_id, coo_of)
    [xml, xml_id, pibg, coo_of] = lateral(i, 'lateral1', bd, pibg, xml, xml_id, coo_of)
    [xml, xml_id, pibg, coo_of] = lateral(i, 'lateral2', bd, pibg, xml, xml_id, coo_of)
    return [xml, xml_id, pibg, coo_of]

def baixos(bd, xml, xml_id, coo_of):
    """
    make as many groups of baixos as the symmetry of the castells demands
    """
    position_in_baix_group = dict()
    for i in range(bd['number']):
        alpha = i * 2.0 * pi / bd['number']
        x = round(bd['radius'] * cos(alpha), 2)
        y = round(bd['radius'] * sin(alpha), 2)
        xml += '<position_group id="baixos_gp_' + str(i) + \
            '" transform="translate(' + \
            str(x) + ' ' + \
            str(y) + ') rotate(' + \
            str(round(180 / pi * alpha, 2)) + ')">'
        [xml, xml_id, position_in_baix_group, coo_of] = \
            baix_group(bd, i, xml, xml_id, position_in_baix_group, coo_of)
        xml += '</position_group>\n'
    return [xml, xml_id, position_in_baix_group, coo_of]

def pc(i, j, index, pcd, pipcg, xml, xml_id, coo_of):
    """
    make one portacrossa
    """
    xml_id = xml_id + 1
    [x,y] = pcd[index + '_pos']
    dims  = pcd[index + '_dim']
    alpha = dims['angle']
    xml += xml_position.substitute(_x=x, \
                                   _y=y, \
                                   _rx = dims['x'], \
                                   _ry = dims['y'], \
                                   _rw = dims['w'], \
                                   _rh = dims['h'], \
                                   _angle = alpha, \
                                   _xml_id=xml_id,\
                                   #_xml_text = str([i,j]), \
                                   _xml_text=xml_id, \
                                   _class='portacrossa', \
                                   _name=xml_id, \
                                   _index_props=[i,j])
    pipcg[i,j] = dict([('xml_id', xml_id), \
                           ('role', 'portacrossa'), \
                           #('xml_text', 'portacrossa'), \
                           ('xml_text', xml_id), \
                           ('x', x), \
                           ('y', y), \
                           ('angle', alpha)])
    coo_of[xml_id] = [x,y]
    return [xml, xml_id, pipcg, coo_of]
                                   

def portacrossa_group(pcd, i, xml, xml_id, pipcg, coo_of):
    """
    make a group of one portacrossa (pc_c) and two laterals (pc_i, pc_d)
    """
    [xml, xml_id, pipcg, coo_of] = pc(i, 0, 'pc_c', pcd, pipcg, xml, xml_id, coo_of)
#    [xml, xml_id, pipcg, coo_of] = pc(i, 1, 'pc_i', pcd, pipcg, xml, xml_id, coo_of)
#    [xml, xml_id, pipcg, coo_of] = pc(i, 2, 'pc_d', pcd, pipcg, xml, xml_id, coo_of)
    return [xml, xml_id, pipcg, coo_of]

def portacrossa(pcd, xml, xml_id, coo_of):
    """
    make as many groups of portacrossa as the symmetry says to
    """
    position_in_portacrossa = dict()
    for i in range(pcd['number']): 
        alpha = (i * 2.0 + 1.0) * pi / pcd['number']
        x = round(pcd['radius'] * cos(alpha), 2)
        y = round(pcd['radius'] * sin(alpha), 2)
        xml += '<position_group id="portacrossa_gp_' + str(i) + \
            '" transform="translate(' + \
            str(x) + ' ' + \
            str(y) + ') rotate(' + \
            str(round(180 / pi * alpha, 2)) + ')">'
        [xml, xml_id, position_in_portacrossa, coo_of] = \
            portacrossa_group(pcd, i, xml, xml_id, position_in_portacrossa, coo_of)
        xml += '</position_group>\n'         
    return [xml, xml_id, position_in_portacrossa, coo_of]

def segons(sd, xml, xml_id, coo_of):
    """
    make as many segons as the symmetry of the castells demands
    """
    position_in_segons = dict()
    for i in range(sd['number']):
        alpha = i * 2.0 * pi / sd['number']
        x = round(sd['radius'] * cos(alpha), 2)
        y = round(sd['radius'] * sin(alpha), 2)
        [xml, xml_id, position_in_segons, coo_of] = \
            segon(i, x, y, round(180 / pi * alpha, 2), sd, \
                      position_in_segons, xml, xml_id, coo_of)
    return [xml, xml_id, position_in_segons, coo_of]

def segon(i, x, y, angle, sd, pis, xml, xml_id, coo_of):
    """
    make the rectangle and text of a segon
    """
    xml_id = xml_id + 1
    xml += xml_position.substitute(_x=x, \
                                   _y=y, 
                                   _rx = sd['segon_rect_dim']['x'], \
                                   _ry = sd['segon_rect_dim']['y'], \
                                   _rw = sd['segon_rect_dim']['w'], \
                                   _rh = sd['segon_rect_dim']['h'], \
                                   _angle = angle, \
                                   _xml_id=xml_id,\
                                   #_xml_text = str([i,j]), \
                                   _xml_text=xml_id, \
                                   _class='segon', \
                                   _name=xml_id, \
                                   _index_props=i)
    pis[i] = dict([('xml_id', xml_id), \
                       ('role', 'segon'), \
                       #('xml_text', 'agulla'), \
                       ('xml_text', xml_id), \
                       ('x', x), \
                       ('y', y), \
                       ('angle', angle)])
    coo_of[xml_id] = [x,y]
    return [xml, xml_id, pis, coo_of]


def pinya(rd, bd, pcd, sd, xml):
    xml_id = 0
    coo_of = dict()
    [xml, xml_id, position_in_ring, coo_of] = rings(rd, xml, xml_id, coo_of)
    [xml, xml_id, position_in_baix_group, coo_of] = baixos(bd, xml, xml_id, coo_of)
    [xml, xml_id, position_in_portacrossa, coo_of] = portacrossa(pcd, xml, xml_id, coo_of)
    sd['radius'] = rd['start_radius'] + \
        (rd['end_n_in_slice'] - rd['start_n_in_slice'] + 1.5) * rd['radius_offset']
    [xml, xml_id, position_in_segons, coo_of] = segons(sd, xml, xml_id, coo_of)
    return [xml, position_in_ring, position_in_baix_group, \
                position_in_portacrossa, position_in_segons, coo_of]


def tresde9f():
    # data for the rings of the pinya
    rd = dict([('period', 3), ('start_n_in_slice', 1), ('end_n_in_slice', 3), \
                   ('start_radius', 100), ('radius_offset', 25), \
                   ('pinya_rect_dim', dict([('w',20),('h',40)]))])
    r = rd['start_radius'] + (rd['end_n_in_slice'] - rd['start_n_in_slice']) * rd['radius_offset']

    #data for the baixos and crosses
    bw2 = 10 # half the width of a baixos rectangle
    bh2 = 20 # half the height of a baixos rectangle
    cw2 = 8  # half the width of a crosses rectangle
    ch2 = 15 # half the height of a crosses rectangle
    lw2 = 8  # half the width of a lateral rectangle
    lh2 = 15 # half the height of a lateral rectangle
    bd = dict([('number', 3), \
                   ('radius', 40), \
                   ('baix_pos', \
                        [0,0]), \
                   ('baix_rect_dim', \
                        dict([('x', -bw2), ('y', -bh2), \
                                  ('w', 2*bw2), ('h', 2*bh2), ('angle', 0)])), \
                   ('crossa_pos', \
                        [0,30]), \
                   ('crossa_rect_dim', \
                        dict([('x', -cw2), ('y', -ch2), \
                                  ('w', 2*cw2), ('h', 2*ch2), ('angle', 90)])), \
                   ('contrafort_pos', \
                        [20,0]), \
                   ('contrafort_rect_dim', \
                        dict([('x', -cw2), ('y', -ch2), \
                                  ('w', 2*cw2), ('h', 2*ch2), ('angle', 0)])), \
                   ('agulla_pos', \
                        [-20,0]), \
                   ('agulla_rect_dim', \
                        dict([('x', -cw2), ('y', -ch2), \
                                  ('w', 2*cw2), ('h', 2*ch2), ('angle', 0)])), \
                   ('lateral_pos', \
                        [30,25]), \
                   ('lateral_rect_dim', \
                        dict([('x', -lw2), ('y', -lh2), \
                                  ('w', 2*lw2), ('h', 2*lh2), ('angle', 30)])) \
                   ])

    # data for the portacrossa 
    pcw2 = 8  # half the width of a portacrossa rectangle
    pch2 = 15 # half the height of a portacrossa rectangle
    pcw02 = 10  # half the width of a portacrossa rectangle
    pch02 = 20 # half the height of a portacrossa rectangle
    pcd = dict([('number', 3),  \
                    ('radius', 70), \
                    ('pc_c_dim', \
                        dict([('x', -pcw02), ('y', -pch02), \
                                  ('w', 2*pcw02), ('h', 2*pch02), ('angle', 0)])), \
                    ('pc_c_pos', \
                         [0,0]), \
                    ('pc_d_dim', \
                        dict([('x', -pcw2), ('y', -pch2), \
                                  ('w', 2*pcw2), ('h', 2*pch2), ('angle', 30)])), \
                    ('pc_d_pos', \
                         [-10,45]), \
                    ('pc_i_dim', \
                        dict([('x', -pcw2), ('y', -pch2), \
                                  ('w', 2*pcw2), ('h', 2*pch2), ('angle', -30)])), \
                    ('pc_i_pos', \
                         [-10,-45]) \
                    ])

    # data for the segons
    sw2 = 10 # half the width of a segons rectangle
    sh2 = 20 # half the height of a segons rectangle
    sd = dict([('number', 3),\
                   ('segons_pos', [50,0]),\
                   ('radius', 50), \
                   ('segon_rect_dim', \
                        dict([('x', -sw2), ('y', -sh2),\
                                  ('w', 2*sw2), ('h', 2*sh2), ('angle', 0)])) \
                   ])

    # start the xml
    xml = xml_head.substitute(_vx=-r-80, _vy=-r-40, _vw=2*r+160, _vh=2*r+80) 
    xml += '<title>Tres de nou amb folre</title>\n' + \
        '<castell castell_id_name="cvg.3de9f"/>\n' + \
        '<colla colla_id_name="cvg"/>\n'

    # go!
    xml += '<positions>'
    [xml, position_in_ring, position_in_baix_group, \
         position_in_portacrossa, position_in_segons, coo_of] = pinya(rd, bd, pcd, sd, xml)
    xml += '</positions>\n'

    relations = []
    relations = ring_relations(rd, position_in_ring, relations, has_folre = True) 
    relations = baix_crosses_relations(bd, position_in_baix_group, position_in_portacrossa, relations)
    relations = baix_agulla_relations(rd, position_in_baix_group, relations)
    relations = baix_contrafort_relations(rd, position_in_baix_group, relations)
    relations = segons_mans_relations(rd, position_in_ring, position_in_baix_group, position_in_segons, relations)
    relations = segons_vent_relations(rd, position_in_ring, position_in_baix_group, position_in_segons, relations)
    relations = segons_agulla_relations(rd, position_in_baix_group, position_in_segons, relations)
    relations = segons_baixos_relations(rd, position_in_baix_group, position_in_segons, relations)
    relations = segons_lateral_relations(rd, position_in_baix_group, position_in_segons, relations)

    xml += '\n<relations id="rels">\n'    
    xml += relations_xml(relations, coo_of)
    xml += '</relations>\n'

    xml += '</xml>'
    return [xml, position_in_ring, position_in_baix_group, position_in_portacrossa, relations]

def save_tresde9f_xml():
    [xml, position_in_ring, position_in_baix_group, \
         position_in_portacrossa, relations] = tresde9f()
    f = open('pinya.xml', 'w')
    f.write(xml)
    f.close()
    
if __name__ == "__main__":
    save_tresde9f_xml()
