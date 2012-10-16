import xml.dom.minidom
from local_config import pinya_dir
from math import sin, cos, pi
from local_config import numeric_splitter, text_splitter, pos_types
from db_interaction import get_db, castellers_of_type, get_avg_shoulder_width
from ineqs import relation_ineq

lp = []

cids=() #11,77) # print debug info for these

def xml_to_lp(xmlfilename):
    ineqs = []
    obj = dict()
    [ineqs, obj] = xml_to_lp_impl(xmlfilename, ineqs, obj)
    var_string = []
    obj_string = []
    for var, coeff in obj.iteritems():
        if coeff > 0:
            obj_string.append('+ ' + str(coeff) + ' ' + var)
            var_string.append(' ' + var)
        elif coeff < 0:
            obj_string.append(str(coeff) + ' ' + var)
            var_string.append(' ' + var)
    return 'maximize\n' + \
        ' '.join(obj_string) + \
        '\nsubject to\n' + \
        '\n'.join(ineqs) + \
        '\nbinary\n' + \
        ' '.join(var_string)
        

def xml_to_lp_impl(xmlfilename, ineqs, obj):
    f = open(xmlfilename, 'r')
    dom = xml.dom.minidom.parseString(f.read())
    return handleXML(dom.documentElement, ineqs, obj)

def handleXML(xml, ineqs, obj):
    lp.append('subject to\n')
    castell_id_name = xml.getElementsByTagName("castell")[0].getAttribute("castell_id_name")
    colla_id_name = xml.getElementsByTagName("colla")[0].getAttribute("colla_id_name")
    relations = xml.getElementsByTagName("relations")[0]
    (cot, aux_data) = castellers(colla_id_name)
    for child in relations.childNodes:
        if child.nodeName == 'relation':
            [ineqs, obj] = handleRelation(child, cot, aux_data, ineqs, obj)
    return [ineqs, obj]

def castellers(colla_id_name):
    db = get_db()
    aux_data = dict([('avg_shoulder_width', get_avg_shoulder_width(db, colla_id_name))])
    cot = dict()
    for role in pos_types:
        cot[role] = castellers_of_type(db, colla_id_name, role)
    return (cot, aux_data)

def handleRelation(relation, cot, aux_data, ineqs, obj):
    field_names = [str(f) for f in relation.getAttribute('field_names').split(text_splitter)]
    pos_list = [int(p) for p in relation.getAttribute('pos_list').split(numeric_splitter)]
    role_list = [r for r in str(relation.getAttribute('role_list')).split(text_splitter)]
    coeff_list = [float(c) for c in relation.getAttribute('coeff_list').split(numeric_splitter)]
    relation_type = relation.getAttribute('relation_type')
    xmlsense = relation.getAttribute('sense')
    if xmlsense == 'le':
        sense = '<='
    else:
        sense = '>='
    rhs = float(relation.getAttribute('rhs'))
    [ineqs, obj] = relation_ineq(relation_type, cot, pos_list, role_list, coeff_list, field_names, sense, rhs, aux_data, ineqs, obj)
    return [ineqs, obj]

def write_lp(pinya_name):
    f = open('../www/' + pinya_dir + '/' + pinya_name + '/pinya.lp', 'w')
    f.write(xml_to_lp('../www/' + pinya_dir + '/' + pinya_name + '/pinya.xml'))


if __name__=='__main__':
    write_lp('cvg.3de9f')
#    import cProfile
#    cProfile.run('run()', 'xml_to_lp.stats')


