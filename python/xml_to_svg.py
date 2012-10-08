import xml.dom.minidom
from local_config import pinya_xml_dir, pinya_svg_dir
from math import sin, cos

svg = []
coos = dict()

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
    for child in xml.childNodes:
        if child.nodeName == 'title':
            handleTitle(child)
        if child.nodeName == 'pinya':
            handlePinya(child)
        if child.nodeName == 'relations':
            handleRelations(child)
    svg.append('</svg>')

def handleTitle(titles):
    pass

def handlePinya(pinya):
    svg.append('<g id="pinya">')
    for child in pinya.childNodes:
        if child.nodeName == 'position_group':
            handlePositionGroup(child)
        elif child.nodeName == 'position':
            handlePosition(child)
    svg.append('</g>')

def handlePositionGroup(group):
    printAttr('g', group, ('id', 'transform'))
    transform = group.getAttribute('transform')
    p1 = transform.index('translate(')
    t = transform[p1+10 : transform.index(')', p1+10)].split(' ')
    translation = [float(t[0]), float(t[1])]
    p2 = transform.index('rotate(')
    angle = float(transform[p2+7 : transform.index(')', p2+7)])
    for child in group.childNodes:
        if child.nodeName == 'position':
            handlePosition(child, translation, angle)
    svg.append('</g>')

def handlePositions(positions):
    for position in positions:
        handlePosition(position)

def handlePosition(position, translation=None, angle=None):
    printAttr('g', position, ('id', 'transform'))
    for child in position.childNodes:
        if child.nodeName == 'rect':
            handleRect(child, translation, angle)
        if child.nodeName == 'label':
            handleLabel(child)
    svg.append('</g>')

def handleRect(rect, translation=None, angle=None):
    printAttr('rect', rect, ('id', 'class', 'width', 'height', 'x', 'y'))
    svg.append('</rect>')
    id = rect.getAttribute('id')
    coo = [float(rect.getAttribute('x')), \
               float(rect.getAttribute('y'))]
    if angle is not None:
        coo = [coo[0] * cos(angle) + coo[1] * sin(angle), \
                    - coo[0] * sin(angle) + coo[1] * cos(angle)]
    if translation is not None:
        coo = [coo[0] + translation[0], coo[1] + translation[1]]
    coos[id] = [round(coo[0],2), round(coo[1], 2)]

def handleLabel(label):
    printAttr('g', label, ('transform',))
    for child in label.childNodes:
        if child.nodeName == 'text':
            handleText(child)
    svg.append('</g>')

def handleText(text):
    printAttr('text', text, ('id', 'class', 'text-anchor'))
    svg.append(getText(text.childNodes))
    svg.append('</text>')

def handleRelations(relations):
    svg.append('<g id="relations">')
    for child in relations.childNodes:
        if child.nodeName == 'relation':
            handleRelation(child)
    svg.append('</g>')

def handleRelation(relation):
    d = getText(relation.childNodes)
    print relation.getAttribute('pos_list')
    print d

    svg.append('<path class="' + \
                   relation.getAttribute('pos_type_list') + \
                   '" d="' + \
                   getText(relation.childNodes) + \
                   '"/>')

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def write_svg(pinya_name):
    f = open('../www/' + pinya_svg_dir + pinya_name + '.pinya.svg', 'w')
    f.write(xml_to_svg('../www/' + pinya_xml_dir + pinya_name + '.pinya.xml'))


if __name__=='__main__':
    write_svg('tresde9f')
#    import cProfile
#    cProfile.run('run()', 'xml_to_svg.stats')


