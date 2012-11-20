import xml.dom.minidom
from local_config import RootDir, pinya_dir, \
    text_splitter, numeric_splitter, drawSketch, \
    Debug, PinyaWhiteUnderlay, RelationsWhiteUnderlay
from random import random
from string import replace
import pickle

import sys 
sys.path.append(RootDir + 'python/util/')
from transforms import extract_transform, make_transform, apply_transform, view_mapping


cids=() #11,77) # print debug info for these

def xml_to_svg(xmlfilename):
    svg = []
    svg = xml_to_svg_impl(xmlfilename, svg)
    return '\n'.join(svg)


def printAttr(tag, elem, attr_list, svg):
    res = []
    res.append('<' + tag)
    for a in attr_list:
        res.append(' ' + a + '="' + elem.getAttribute(a) + '"')
    res.append('>')
    svg.append(''.join(res))
    return svg

def xml_to_svg_impl(xmlfilename, svg):
    f = open(xmlfilename + '.xml', 'r')
    dom = xml.dom.minidom.parseString(f.read())
    role_of = dict()
    rel_list = []
    [svg, role_of, rel_list] = handleXML(dom.documentElement, svg, role_of, rel_list)
    write_data(xmlfilename, role_of, '.roles')
    write_data(xmlfilename, sorted(set([rel['role_list'] for rel in rel_list])), '.rel_types')
    return svg

def write_data(xmlfilename, data, extension):
    aux = open(xmlfilename + extension, 'w')
    pickle.dump(data, aux)

def handleXML(xml, svg, role_of, rel_list):
    coos = dict()
    svg = handleTitle(xml.getElementsByTagName('title')[0], svg)
    [coos, svg, role_of] = handlePositions(xml.getElementsByTagName('positions')[0], coos, svg, role_of)
    bb = bbox(coos)
    [svg, rel_list] = handleRelations(xml.getElementsByTagName('relations')[0], coos, svg, rel_list)
    bb['x'] -= 80
    bb['y'] -= 40
    bb['w'] += 160
    bb['h'] += 80
    xml.setAttribute('viewBox', ','.join([str(bb[arg]) for arg in ['x', 'y', 'w', 'h']]))
    svg_tmp = []
    svg_tmp = printAttr('svg', xml, ('xmlns', 'xmlns:xlink', 'viewBox'), svg_tmp)
    svg_tmp = [replace(svg_tmp[0], '/xml', '/svg')]
    for i in svg:
        svg_tmp.append(i)
    svg_tmp.append('</svg>')
    return [svg_tmp, role_of, rel_list]

def bbox(coos):
    xmin = 100000000
    xmax = -100000000
    ymin = 100000000
    ymax = -100000000
    for coo in coos.values():
        if coo[0] < xmin:
            xmin = coo[0]
        if coo[0] > xmax:
            xmax = coo[0]
        if coo[1] < ymin:
            ymin = coo[1]
        if coo[1] > ymax:
            ymax = coo[1]
    return dict([('x', xmin), ('y', ymin), ('w', xmax-xmin), ('h', ymax-ymin)])

def handleTitle(titles, svg):
    return svg

def handlePositions(positions, coos, svg, role_of):
    if Debug:
        print "handlePositions", coos
    svg.append('<g id="positions">')
    for child in positions.childNodes:
        if child.nodeName == 'position_group':
            [coos, svg, role_of] = handlePositionGroup(child, coos, svg, role_of)
        elif child.nodeName == 'position':
            [new_ids, coos, svg, role_of] = handlePosition(child, coos, svg, role_of)
#            ids += new_ids
        if Debug:
            print "in handlePositions; coos now", coos
    svg.append('</g>')
    return [coos, svg, role_of]

def handlePositionGroup(group, coos, svg, role_of):
    ids = []
    if Debug:
        print "handlePositionGroup", coos
    svg = printAttr('g', group, ('id', 'transform'), svg)
    for child in group.childNodes:
        if child.nodeName == 'position':
            [new_ids, coos, svg, role_of] = handlePosition(child, coos, svg, role_of)
            ids += new_ids
    [translation, angle] = extract_transform(group.getAttribute('transform'))
    new_translation = view_mapping(translation)
    group.setAttribute('transform', make_transform(new_translation, angle))
#    for cid in cids:
#        print 'posgroup', cid, 'before', coos[cid], translation, angle
    for id in ids: 
        coos = apply_transform(id, new_translation, angle, coos)
    for cid in cids:
        if cid in ids:
            print 'posgroup', cid, 'result', coos[cid], translation, angle
    svg.append('</g>')
    return [coos, svg, role_of]
    
def handlePosition(position, coos, svg, role_of):
    ids = []
    if Debug:
        print "handlePosition", position.getAttribute('id'), coos
    [translation, angle] = extract_transform(position.getAttribute('transform'))
    new_translation = view_mapping(translation)
    position.setAttribute('transform', make_transform(new_translation, angle))
    svg = printAttr('g', position, ('id', 'transform'), svg)
    role_of = extract_role(position, role_of)
    for child in position.childNodes:
        if child.nodeName == 'rect':
            [id, coos, svg] = handleRect(child, coos, svg)
            if Debug: 
                print "after handleRect:", coos
            ids.append(id)
        if child.nodeName == 'label':
            svg = handleLabel(child, svg)
    for cid in cids:
        if cid in ids:
            print 'before handlePOsition', cid, coos[cid], translation, angle
    for id in ids:
        coos = apply_transform(id, new_translation, angle, coos)
    for cid in cids:
        if cid in ids:
            print 'after handlePOsition', cid, coos[cid], translation, angle
    svg.append('</g>')
    return [ids, coos, svg, role_of]

def handleRect(rect, coos, svg):
    id = int(rect.getAttribute('id').split(numeric_splitter)[0])
    if drawSketch:
        svg.append('<g id="' + str(id) + '_casteller" ' + \
                       'class="' + rect.getAttribute('class') + '" ' + \
                       'transform="scale(.2 .2) rotate(-90)">')
        svg.append('${_rep' + str(id) + '}')
        svg.append('</g>')
    else:
        svg = printAttr('rect', rect, ('id', 'class', 'width', 'height', 'x', 'y'), svg)
        svg.append('</rect>')
    if Debug:
        print "in handleRect", rect.getAttribute('id'), id, coos
    coos[id] = [float(rect.getAttribute('x')) + float(rect.getAttribute('width'))/2, \
                    float(rect.getAttribute('y')) + float(rect.getAttribute('height'))/2]
#    coos[id][1] = round(coos[id][1]/2, 2)
    if Debug:
        print "in handleRect: coos now", coos
    return [id, coos, svg]

def handleLabel(label, svg):
    svg = printAttr('g', label, ('transform',), svg)
    for child in label.childNodes:
        if child.nodeName == 'text':
            svg = handleText(child, svg)
    svg.append('</g>')
    return svg

def handleText(text, svg):
    if PinyaWhiteUnderlay:
        svg.append(writeText(text, 'whiteText'))
    svg.append(writeText(text))
    return svg

def writeText(text, extra_class = ''):
    label = getText(text.childNodes)
    return '<text id="' + text.getAttribute('id') + '" ' + \
        'class="' + text.getAttribute('class') + ' ' + \
        extra_class + '" ' + \
        'text-anchor="' + text.getAttribute('text-anchor') + '" ' + \
        'x="0" y="0">' + \
        label + ' ${_' + label + '} ${_c' + label + '}' + \
        '</text>'

def handleRelations(relations, coos, svg, rel_list):
    svg.append('<g id="relations">')
    for child in relations.childNodes:
        if child.nodeName == 'relation':
            [svg, rel_list] = handleRelation(child, coos, svg, rel_list)
    svg.append('</g>')
    return [svg, rel_list]

def handleRelation(relation, coos, svg, rel_list):
    d = []
    role_list = relation.getAttribute('role_list').replace(text_splitter, numeric_splitter)
    d.append('<path class="rel ' + role_list + \
                 '" pos_list="' + \
                 relation.getAttribute('pos_list') + \
                 '" d="')
    xtot = 0
    ytot = 0
    count = 0
    pos_list = relation.getAttribute('pos_list')
    for pos in pos_list.split(numeric_splitter):
        if count > 0:
            d.append('L')
        else:
            d.append('M')
        count = count + 1
        x = coos[int(pos)][0] + 5 * random()
        y = coos[int(pos)][1] + 5 * random()
        xtot += x
        ytot += y
        d.append(str(x) + ',' + str(y))
    d.append('"/>')
    svg.append(''.join(d))
    d = []
    xtot = round(xtot/count, 2)
    ytot = round(ytot/count, 2)
    d.append('<g transform="translate(' + str(xtot) + ' ' + str(ytot) + ')">')
    if RelationsWhiteUnderlay:
        d.append('<text class="rel whiteRelText ' + role_list + '" x="0" y="0">${_rel' + pos_list + '}</text>')
    d.append('<text class="rel ' + role_list + '" x="0" y="0">${_rel' + pos_list + '}</text>')
    d.append('</g>')
    svg.append(''.join(d))
    coeff_list = relation.getAttribute('coeff_list')
    field_names = relation.getAttribute('field_names')
    target_val = relation.getAttribute('target_val')
    min_tol = relation.getAttribute('min_tol')
    max_tol = relation.getAttribute('max_tol')
    rel_list.append(dict([\
                ('role_list', role_list), \
                    ('pos_list', pos_list), \
                    ('coeff_list', coeff_list), \
                    ('field_names', field_names), \
                    ('target_val', target_val), \
                    ('min_tol', min_tol), \
                    ('max_tol', max_tol) \
                    ]))
    return [svg, rel_list]

def extract_role(position, role_of):
    role_of[int(position.getAttribute('id'))] = str(position.getAttribute('role'))
    return role_of

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def write_svg(castell_id_name):
    filename = RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya' 
    f = open(filename + '.svg', 'w')
    f.write(xml_to_svg(filename))


if __name__=='__main__':
    write_svg('cvg.3de9f')
#    import cProfile
#    cProfile.run('run()', 'xml_to_svg.stats')


