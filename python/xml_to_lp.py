import xml.dom.minidom
from local_config import pinya_dir
from math import sin, cos, pi
from local_config import numeric_splitter, text_splitter

lp = []
obj = dict()

cids=() #11,77) # print debug info for these

def xml_to_lp(xmlfilename):
    xml_to_lp_impl(xmlfilename)
    obj_string = []
    var_string = []
    for var, coeff in obj.iteritems():
        if coeff > 0:
            obj.append('+ ' + coeff + ' ' + var)
            var_string.append(' ' + var)
        elif coeff < 0:
            obj.append(coeff + ' ' + var)
            var_string.append(' ' + var)
    return 'maximize\n' + \
        ' '.join(obj_string) + \
        '\n'.join(lp) + \
        'binary\n' + \
        var_string

def xml_to_lp_impl(xmlfilename):
    f = open(xmlfilename, 'r')
    dom = xml.dom.minidom.parseString(f.read())
    handleXML(dom.documentElement)

def handleXML(xml):
    lp.append('subject to\n')
    for child in xml.childNodes:
        if child.nodeName == 'relation':
            handleRelation(child)

def handleRelation(relation):
    field_names = relation.getAttribute('field_names').split(text_splitter)
    pos_list = relation.getAttribute('pos_list').split(numeric_splitter)
    coeff_list = relation.getAttribute('coeff_list').split(numeric_splitter)
    

    d = []
    d.append('<path class="' + relation.getAttribute('pos_type_list') + \
                 '" pos_list="' + relation.getAttribute('pos_list') + '" d="')
    first = True
    for pos in relation.getAttribute('pos_list').split(numeric_splitter):
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


