import xml.dom.minidom
from local_config import pinya_dir
from math import sin, cos, pi
from local_config import numeric_splitter, text_splitter, pos_types
from db_interaction import get_db, castellers_of_type

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
    castell_id_name = xml.getElementsByTagName("castell")[0].getAttr("castell_id_name")
    colla_id_name = xml.getElementsByTagName("colla")[0].getAttr("colla_id_name")
    cot = castellers(colla_id_name)
    for child in xml.childNodes:
        if child.nodeName == 'relation':
            handleRelation(child, cot)

def castellers(colla_id_name):
    db = get_db()
    cot = dict()
    for role in pos_types:
        cot[role] = castellers_of_type(db, colla_id_name, role)
    return cot

def handleRelation(relation, cot):
    field_names = relation.getAttribute('field_names').split(text_splitter)
    pos_list = relation.getAttribute('pos_list').split(numeric_splitter)
    role_list = relation.getAttribute('role_list').split(text_splitter)
    coeff_list = relation.getAttribute('coeff_list').split(numeric_splitter)
    relation_type = relation.getAttribute('relation_type')
    sense = relation.getAttribute('sense')

    rhs = relation.getAttribute('rhs')

    


def write_lp(pinya_name):
    f = open('../www/' + pinya_dir + '/' + pinya_name + '.pinya.lp', 'w')
    f.write(xml_to_lp('../www/' + pinya_dir + '/' + pinya_name + '.pinya.xml'))


if __name__=='__main__':
    write_lp('cvg.3de9f')
#    import cProfile
#    cProfile.run('run()', 'xml_to_lp.stats')


