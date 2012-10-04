import xml.dom.minidom

def xml_to_svg(xmlfilename):
    f = open(xmlfilename, 'r')
    dom = xml.dom.minidom.parseString(read(f))
    print '<svg '
    handleXML(dom)
    print '</svg>\n'

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ’’.join(rc)

def handleXML(xml):
    print 'xmlns="' . xml.getAttribute('xmlns') . '" ' . \
        'xmlns:xlink="' . xml.getAttribute('xmlns:xlink') . '" ' . \
        'viewBox=" ' . xml.getAttribute('viewBox') . '">\n'
    handleTitle(xml.getElementsByTagName('title'))
    handlePinya(xml.getElementsByTagName('pinya'))

def handlePinya(pinya):
    print '<pinya>\n'
    handlePosition(xml.getElementsByTagName('position'))
    print '</pinya>\n'

def handlePosition(position):
    print '<g ' . \
        'id="' . position.getAttribute('id') . '" ' . \
        'transform="' . position.getAttribute('transform') . '">\n'
    handleRect(position.getElementsByTagName('rect'))
    handleLabel(position.getElementsByTagName('label'))
    print '</g>\n'

