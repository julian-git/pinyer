import xml.dom.minidom
from local_config import pinya_xml_dir, pinya_svg_dir

svg = []

def xml_to_svg(xmlfilename):
    xml_to_svg_impl(xmlfilename)
    return '\n'.join(svg)


def printAttr(tag, elem, attr_list):
    res = []
    res.append('<' + tag + ' ')
    for a in attr_list:
        res.append(a + '="' + elem.getAttribute(a) + '" ')
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
    for child in group.childNodes:
        if child.nodeName == 'position':
            handlePosition(child)
    svg.append('</g>')

def handlePositions(positions):
    for position in positions:
        handlePosition(position)

def handlePosition(position):
    printAttr('g', position, ('id', 'transform'))
    for child in position.childNodes:
        if child.nodeName == 'rect':
            handleRect(child)
        if child.nodeName == 'label':
            handleLabel(child)
    svg.append('</g>')

def handleRect(rect):
    printAttr('rect', rect, ('id', 'class', 'width', 'height', 'x', 'y'))
    svg.append('</rect>')

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
    write_svg('tresde8f')
#    import cProfile
#    cProfile.run('run()', 'xml_to_svg.stats')


