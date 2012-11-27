import xml.dom.minidom
from local_config import RootDir, pinya_dir, \
    text_splitter, numeric_splitter, drawSketch, \
    Debug, PinyaWhiteUnderlay, RelationsWhiteUnderlay, RelationCurvature
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
    [svg, role_of] = handleXML(dom.documentElement, svg, role_of)
    write_data(xmlfilename, role_of, '.roles')
    return svg

def write_data(xmlfilename, data, extension):
    aux = open(xmlfilename + extension, 'w')
    pickle.dump(data, aux)

def handleXML(xml, svg, role_of):
    coos = dict()
    svg = handleTitle(xml.getElementsByTagName('title')[0], svg)
    [coos, svg, role_of] = handlePositions(xml.getElementsByTagName('positions')[0], coos, svg, role_of)
    bb = bbox(coos)
    svg = handleRelations(xml.getElementsByTagName('relations')[0], coos, svg)
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
    return [svg_tmp, role_of]

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
        'x="0" y="0" ' + \
        'title="${_alt' + text.getAttribute('id') + '}" ' + \
        'onmouseover="Drop(evt)">' + \
        '${_' + label + '}' + \
        '</text>'
        #        label + ' ${_' + label + '} ${_c' + label + '}' + 

def handleRelations(relations, coos, svg):
    svg.append('<g id="relations">')
    for child in relations.childNodes:
        if child.nodeName == 'relation':
            svg = handleRelation(child, coos, svg)
    svg.append('</g>')
    return svg

def handleRelation(relation, coos, svg):
    d = []
    role_list = relation.getAttribute('role_list').replace(text_splitter, numeric_splitter)
    d.append('<path class="rel ' + role_list + \
                 '" pos_list="' + \
                 relation.getAttribute('pos_list') + \
                 '" d="')
    xtot = 0
    ytot = 0
    xcurr = 0
    ycurr = 0
    count = 0
    pos_list = relation.getAttribute('pos_list')
    for pos in pos_list.split(numeric_splitter):
        x = coos[int(pos)][0] 
        y = coos[int(pos)][1] 
        xtot += x
        ytot += y
        if count == 0:
            d.append('M')
        else:
            [xctrl, yctrl] = control_point(xcurr, ycurr, x, y)
            d.append('Q' + str(xctrl) + ',' + str(yctrl) + ' ')
        xcurr = x
        ycurr = y
        d.append(str(x) + ',' + str(y))
        count = count + 1 
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
    return svg

def control_point(x0, y0, x1, y1):
    xm = (x0+x1)/2.0
    ym = (y0+y1)/2.0
    return [round(xm + RelationCurvature*(y1-y0),2), \
                round(ym - RelationCurvature*(x1-x0),2)]

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


