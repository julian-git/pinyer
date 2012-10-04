import xml.dom.minidom

def printAttr(tag, elem, attr_list):
    print '<' . tag . ' '
    for a in attr_list:
        print a . '="' . elem.getAttribute(a) . '" '
    print '>\n'

def xml_to_svg(xmlfilename):
    f = open(xmlfilename, 'r')
    dom = xml.dom.minidom.parseString(read(f))
    handleXML(dom)

def handleXML(xml):
    printAttr('svg', xml, ('xmlns', 'xmlns:xlink', 'viewbox'))
    handleTitle(xml.getElementsByTagName('title'))
    handlePinya(xml.getElementsByTagName('pinya'))
    print '</svg>\n'

def handlePinya(pinya):
    print '<pinya>\n'
    handlePositionGroups(pinya.getElementsByTagName('position_group'))
    handlePositions(pinya.getElementsByTagName('position'))
    print '</pinya>\n'

def handlePositionGroups(groups):
    for group in groups:
        printAttr('g', group, ('id', 'transform'))
        handlePositions(group.getElementsByTagName('position'))
        print '</g>\n'

def handlePositions(positions):
    for position in positions:
        printAttr('g', position, ('id', 'transform'))
        handleRects(position.getElementsByTagName('rect'))
        handleLabels(position.getElementsByTagName('label'))
        print '</g>\n'

def handleRects(rects):
    for rect in rects:
        printAttr('rect', rect, ('id', 'class', 'width', 'height', 'x', 'y'))
        print '</rect>\n'

def handleLabels(labels):
    for label in labels:
        printAttr('g', label, ('transform'))
        handleText(label.getElementsByTagName('text'))
        print '</g>\n'

def handleText(texts):
    for text in texts:
        printAttr('text', text, ('id', 'class', 'text-anchor'))
        print getText(text.childNodes)
        print '</text>\n'

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ’’.join(rc)

if __name__ == "__main__":
    xml_to_svg('../www/tresde8f.pinya.xml')
