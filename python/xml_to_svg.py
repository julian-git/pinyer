import xml.dom.minidom
from local_config import RootDir, pinya_dir, \
    text_splitter, numeric_splitter, drawSketch, \
    Debug
from random import random
import pickle

import sys 
sys.path.append(RootDir + 'python/util/')
from transforms import extract_transform, make_transform, apply_transform, view_mapping

svg = []
role_of = dict()

cids=() #11,77) # print debug info for these

def xml_to_svg(xmlfilename):
    xml_to_svg_impl(xmlfilename)
    return '\n'.join(svg)


def printAttr(tag, elem, attr_list):
    res = []
    res.append('<' + tag)
    for a in attr_list:
        res.append(' ' + a + '="' + elem.getAttribute(a) + '"')
    res.append('>')
    svg.append(''.join(res))

def xml_to_svg_impl(xmlfilename):
    f = open(xmlfilename + '.xml', 'r')
    dom = xml.dom.minidom.parseString(f.read())
    handleXML(dom.documentElement)
    g = open(xmlfilename + '.roles', 'w')
    pickle.dump(role_of, g)

def handleXML(xml):
    coos = dict()
    printAttr('svg', xml, ('xmlns', 'xmlns:xlink', 'viewBox'))
    handleTitle(xml.getElementsByTagName('title')[0])
    coos = handlePositions(xml.getElementsByTagName('positions')[0], coos)
    handleRelations(xml.getElementsByTagName('relations')[0], coos)
    svg.append('</svg>')

def handleTitle(titles):
    pass

def handlePositions(positions, coos):
    if Debug:
        print "handlePositions", coos
    svg.append('<g id="positions">')
    for child in positions.childNodes:
        if child.nodeName == 'position_group':
            coos = handlePositionGroup(child, coos)
        elif child.nodeName == 'position':
            [new_ids, coos] = handlePosition(child, coos)
#            ids += new_ids
        if Debug:
            print "in handlePositions; coos now", coos
    svg.append('</g>')
    return coos

def handlePositionGroup(group, coos):
    ids = []
    if Debug:
        print "handlePositionGroup", coos
    printAttr('g', group, ('id', 'transform'))
    for child in group.childNodes:
        if child.nodeName == 'position':
            [new_ids, coos] = handlePosition(child, coos)
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
    return coos
    
def handlePosition(position, coos):
    ids = []
    if Debug:
        print "handlePosition", position.getAttribute('id'), coos
    [translation, angle] = extract_transform(position.getAttribute('transform'))
    new_translation = view_mapping(translation)
    position.setAttribute('transform', make_transform(new_translation, angle))
    printAttr('g', position, ('id', 'transform'))
    extract_role(position)
    for child in position.childNodes:
        if child.nodeName == 'rect':
            [id, coos] = handleRect(child, coos)
            if Debug: 
                print "after handleRect:", coos
            ids.append(id)
        if child.nodeName == 'label':
            handleLabel(child)
    for cid in cids:
        if cid in ids:
            print 'before handlePOsition', cid, coos[cid], translation, angle
    for id in ids:
        coos = apply_transform(id, new_translation, angle, coos)
    for cid in cids:
        if cid in ids:
            print 'after handlePOsition', cid, coos[cid], translation, angle
    svg.append('</g>')
    return [ids, coos]

def handleRect(rect, coos):
    id = int(rect.getAttribute('id').split(numeric_splitter)[0])
    if drawSketch:
        svg.append('<g id="' + str(id) + '_casteller" ' + \
                       'class="' + rect.getAttribute('class') + '" ' + \
                       'transform="scale(.2 .2) rotate(-90)">')
        svg.append('${_rep' + str(id) + '}')
        svg.append('</g>')
    else:
        printAttr('rect', rect, ('id', 'class', 'width', 'height', 'x', 'y'))
        svg.append('</rect>')
    if Debug:
        print "in handleRect", rect.getAttribute('id'), id, coos
    coos[id] = [float(rect.getAttribute('x')) + float(rect.getAttribute('width'))/2, \
                    float(rect.getAttribute('y')) + float(rect.getAttribute('height'))/2]
#    coos[id][1] = round(coos[id][1]/2, 2)
    if Debug:
        print "in handleRect: coos now", coos
    return [id, coos]

def handleLabel(label):
    printAttr('g', label, ('transform',))
    for child in label.childNodes:
        if child.nodeName == 'text':
            handleText(child)
    svg.append('</g>')

def handleText(text):
    printAttr('text', text, ('id', 'class', 'text-anchor'))
    label = getText(text.childNodes)
    svg.append(label + ' ${_' + label + '} ${_c' + label + '}')
    svg.append('</text>')

def handleRelations(relations, coos):
    svg.append('<g id="relations">')
    for child in relations.childNodes:
        if child.nodeName == 'relation':
            handleRelation(child, coos)
    svg.append('</g>')

def handleRelation(relation, coos):
    d = []
    rel_class = relation.getAttribute('role_list').replace(text_splitter, numeric_splitter)
    d.append('<path class="rel ' + rel_class + \
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
    if len(pos_list.split(numeric_splitter)) == 2:
        d.append('<text class="rel ' + rel_class + '">${_rel' + pos_list + '}</text>')
    d.append('</g>')
    svg.append(''.join(d))

def extract_role(position):
    role_of[int(position.getAttribute('id'))] = str(position.getAttribute('role'))

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


