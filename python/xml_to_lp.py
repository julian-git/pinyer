import xml.dom.minidom
from local_config import pinya_dir
from math import sin, cos, pi
from local_config import pos_splitter, field_name_splitter

lp = []
coos = dict()

cids=() #11,77) # print debug info for these

def xml_to_lp(xmlfilename):
    xml_to_lp_impl(xmlfilename)
    return '\n'.join(lp)

def xml_to_lp_impl(xmlfilename):
    f = open(xmlfilename, 'r')
    dom = xml.dom.minidom.parseString(f.read())
    handleXML(dom.documentElement)

def handleXML(xml):
    printAttr('lp', xml, ('xmlns', 'xmlns:xlink', 'viewBox'))
    for child in xml.childNodes:
        if child.nodeName == 'title':
            handleTitle(child)
        if child.nodeName == 'pinya':
            handlePinya(child)
        if child.nodeName == 'relations':
            handleRelations(child)
    lp.append('</lp>')

def handleTitle(titles):
    pass

def handlePinya(pinya):
    lp.append('<g id="pinya">')
    for child in pinya.childNodes:
        if child.nodeName == 'position_group':
            handlePositionGroup(child)
        elif child.nodeName == 'position':
            handlePosition(child)
    lp.append('</g>')

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
    lp.append('</g>')

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
    
def handlePositions(positions):
    ids = []
    for position in positions:
        ids += handlePosition(position)
    return ids

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
    lp.append('</g>')
    return ids

def handleRect(rect):
    printAttr('rect', rect, ('id', 'class', 'width', 'height', 'x', 'y'))
    lp.append('</rect>')
    id = int(rect.getAttribute('id').split(pos_splitter)[0])
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
    lp.append('</g>')

def handleText(text):
    printAttr('text', text, ('id', 'class', 'text-anchor'))
    lp.append(getText(text.childNodes))
    lp.append('</text>')

def handleRelations(relations):
    lp.append('<g id="relations">')
    for child in relations.childNodes:
        if child.nodeName == 'relation':
            handleRelation(child)
    lp.append('</g>')

def handleRelation(relation):
    d = []
    d.append('<path class="' + relation.getAttribute('pos_type_list') + \
                 '" pos_list="' + relation.getAttribute('pos_list') + '" d="')
    first = True
    for pos in relation.getAttribute('pos_list').split(pos_splitter):
        if not first:
            d.append('L')
        else:
            d.append('M')
            first = False
        d.append(str(coos[int(pos)][0]) + ',' + str(coos[int(pos)][1]))
    d.append('"/>')
    lp.append(''.join(d))

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def write_lp(pinya_name):
    f = open('../www/' + pinya_dir + '/' + pinya_name + '.pinya.lp', 'w')
    f.write(xml_to_lp('../www/' + pinya_dir + '/' + pinya_name + '.pinya.xml'))


if __name__=='__main__':
    write_lp('cvg.3de9f')
#    import cProfile
#    cProfile.run('run()', 'xml_to_lp.stats')


