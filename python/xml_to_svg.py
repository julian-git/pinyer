import xml.dom.minidom

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
    handleTitle(xml.getElementsByTagName('title'))
    handlePinya(xml.getElementsByTagName('pinya'))
    svg.append('</svg>')

def handleTitle(titles):
    pass

def handlePinya(pinyas):
    for pinya in pinyas:
        svg.append('<g>')
        handlePositionGroups(pinya.getElementsByTagName('position_group'))
        handlePositions(pinya.getElementsByTagName('position'))
        svg.append('</g>')

def handlePositionGroups(groups):
    for group in groups:
        printAttr('g', group, ('id', 'transform'))
        handlePositions(group.getElementsByTagName('position'))
        svg.append('</g>')

def handlePositions(positions):
    for position in positions:
        printAttr('g', position, ('id', 'transform'))
        handleRects(position.getElementsByTagName('rect'))
        handleLabels(position.getElementsByTagName('label'))
        svg.append('</g>')

def handleRects(rects):
    for rect in rects:
        printAttr('rect', rect, ('id', 'class', 'width', 'height', 'x', 'y'))
        svg.append('</rect>')

def handleLabels(labels):
    for label in labels:
        printAttr('g', label, ('transform',))
        handleText(label.getElementsByTagName('text'))
        svg.append('</g>')

def handleText(texts):
    for text in texts:
        printAttr('text', text, ('id', 'class', 'text-anchor'))
        svg.append(getText(text.childNodes))
        svg.append('</text>')

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

if __name__=='__main__':
    f = open('tmp.svg', 'w')
    f.write(xml_to_svg('../www/tresde8f.pinya.xml'))

