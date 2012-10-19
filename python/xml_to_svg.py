import xml.dom.minidom
from local_config import pinya_dir
from math import sin, cos, pi
from local_config import text_splitter, numeric_splitter

svg = []
coos = dict()

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
    f = open(xmlfilename, 'r')
    dom = xml.dom.minidom.parseString(f.read())
    handleXML(dom.documentElement)

def handleXML(xml):
    printAttr('svg', xml, ('xmlns', 'xmlns:xlink', 'viewBox'))
    handleTitle(xml.getElementsByTagName('title')[0])
    handlePositions(xml.getElementsByTagName('positions')[0])
    handleRelations(xml.getElementsByTagName('relations')[0])
    svg.append('</svg>')

def handleTitle(titles):
    pass

def handlePositions(positions):
    svg.append('<g id="positions">')
    for child in positions.childNodes:
        if child.nodeName == 'position_group':
            handlePositionGroup(child)
        elif child.nodeName == 'position':
            handlePosition(child)
    svg.append('</g>')

def handlePositionGroup(group):
    ids = []
    printAttr('g', group, ('id', 'transform'))
    for child in group.childNodes:
        if child.nodeName == 'position':
            ids += handlePosition(child)
    [translation, angle] = extract_transform(group.getAttribute('transform'))
    for cid in cids:
        if cid in ids:
            print 'posgroup', cid, 'before', coos[cid], translation, angle
    for id in ids: 
        apply_transform(id, translation, angle)
    for cid in cids:
        if cid in ids:
            print 'posgroup', cid, 'result', coos[cid], translation, angle
    svg.append('</g>')

def extract_transform(transform):
    if transform is None:
        return [None, None]
    p1 = transform.index('translate(')
    t = transform[p1+10 : transform.index(')', p1+10)].split(' ')
    translation = [float(t[0]), float(t[1])]
    p2 = transform.index('rotate(')
    angle = float(transform[p2+7 : transform.index(')', p2+7)])
    return [translation, angle]

def apply_transform(id, translation, angle):
    coo = coos[id]
    if id in cids:
        print 'apply', translation, angle, 'to', id, coo
    if angle is not None:
        alpha = angle * pi/180
        coo = [coo[0] * cos(alpha) - coo[1] * sin(alpha), \
                     coo[0] * sin(alpha) + coo[1] * cos(alpha)]
    if translation is not None:
        coo = [coo[0] + translation[0], coo[1] + translation[1]]
    if id in cids:
        print 'result', id, coo
    coos[id] = [round(coo[0],2), round(coo[1], 2)]
    
def handlePosition(position):
    ids = []
    printAttr('g', position, ('id', 'transform'))
    for child in position.childNodes:
        if child.nodeName == 'rect':
            ids.append(handleRect(child))
        if child.nodeName == 'label':
            handleLabel(child)
    [translation, angle] = extract_transform(position.getAttribute('transform'))
    for cid in cids:
        if cid in ids:
            print 'before handlePOsition', cid, coos[cid], translation, angle
    for id in ids:
        apply_transform(id, translation, angle)
    for cid in cids:
        if cid in ids:
            print 'after handlePOsition', cid, coos[cid], translation, angle
    svg.append('</g>')
    return ids

def handleRect(rect):
    printAttr('rect', rect, ('id', 'class', 'width', 'height', 'x', 'y'))
    svg.append('</rect>')
    id = int(rect.getAttribute('id').split(numeric_splitter)[0])
    coos[id] = [float(rect.getAttribute('x')) + float(rect.getAttribute('width'))/2, \
                    float(rect.getAttribute('y')) + float(rect.getAttribute('height'))/2]
    if id in cids:
        print 'handleRect', id, coos[id]
    return id

def handleLabel(label):
    printAttr('g', label, ('transform',))
    for child in label.childNodes:
        if child.nodeName == 'text':
            handleText(child)
    svg.append('</g>')

def handleText(text):
    printAttr('text', text, ('id', 'class', 'text-anchor'))
    svg.append('${_' + getText(text.childNodes) + '}')
    svg.append('</text>')

def handleRelations(relations):
    svg.append('<g id="relations">')
    for child in relations.childNodes:
        if child.nodeName == 'relation':
            handleRelation(child)
    svg.append('</g>')

def handleRelation(relation):
    d = []
    d.append('<path class="' + \
                 relation.getAttribute('role_list').replace(text_splitter, numeric_splitter) + \
                 '" pos_list="' + \
                 relation.getAttribute('pos_list') + \
                 '" d="')
    first = True
    for pos in relation.getAttribute('pos_list').split(numeric_splitter):
        if not first:
            d.append('L')
        else:
            d.append('M')
            first = False
        d.append(str(coos[int(pos)][0]) + ',' + str(coos[int(pos)][1]))
    d.append('"/>')
    svg.append(''.join(d))

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def write_svg(castell_id_name):
    filename = '../www/' + pinya_dir + '/' + castell_id_name + '/pinya' 
    f = open(filename + '.svg', 'w')
    f.write(xml_to_svg(filename + '.xml'))


if __name__=='__main__':
    write_svg('cvg.3de9f')
#    import cProfile
#    cProfile.run('run()', 'xml_to_svg.stats')


