import xml.dom.minidom
from local_config import pinya_dir, numeric_splitter, text_splitter, pos_types
from db_interaction import get_db, castellers_of_type, db_avg_shoulder_width
from ineqs import relation_ineq, castellers_in_position_ineqs


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
            obj_string.append('- ' + str(-coeff) + ' ' + var)
            var_string.append(' ' + var)
    return '\n'.join(('maximize', \
                          ' '.join(obj_string), \
                          'subject to', \
                          '\n'.join(ineqs), \
                          'binary', \
                          ' '.join(var_string)))


def xml_to_lp_impl(xmlfilename, ineqs, obj):
    f = open(xmlfilename, 'r')
    dom = xml.dom.minidom.parseString(f.read())
    return handleXML(dom.documentElement, ineqs, obj)


def handleXML(xml, ineqs, obj):
    castell_id_name = xml.getElementsByTagName('castell')[0].getAttribute('castell_id_name')
    colla_id_name = xml.getElementsByTagName('colla')[0].getAttribute('colla_id_name')

    db = get_db()
    (cot, aux_data) = castellers(db, colla_id_name)

    pos_with_role = dict()
    for child in xml.getElementsByTagName('positions')[0].childNodes:
        if child.nodeName == 'position':
            pos_with_role = RoleOfPosition(child, pos_with_role)

    for child in xml.getElementsByTagName('relations')[0].childNodes:
        if child.nodeName == 'relation':
            [ineqs, obj] = handleRelation(child, cot, aux_data, ineqs, obj)

    ineqs = IneqsOfPositions(db, cot, ineqs, pos_with_role)
    return [ineqs, obj]


def RoleOfPosition(position, pos_with_role):
    role = position.getAttribute('role')
    try:
        pos_with_role[role].append(position.getAttribute('id'))
    except KeyError:
        pos_with_role[role] = [position.getAttribute('id')]
    return pos_with_role


def IneqsOfPositions(db, cot, ineqs, pos_with_role):
    castellers_in_position = dict()
    for role, positions in pos_with_role.iteritems():
        for pos in positions:
            castellers_in_position[pos] = cot[role]
    [ineqs, pos_of_casteller] = castellers_in_position_ineqs(castellers_in_position, ineqs)
    return ineqs


def castellers(db, colla_id_name):
    aux_data = dict([('avg_shoulder_width', db_avg_shoulder_width(db, colla_id_name))])
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
    sense = '<='
    if relation.getAttribute('sense') != 'le':
        sense = '>='
    rhs = float(relation.getAttribute('rhs'))

    return relation_ineq(relation_type, cot, pos_list, role_list, coeff_list, field_names, sense, rhs, aux_data, ineqs, obj)


def handlePositions(db, cot, ineqs, positions):
    castellers_in_position = dict()
    print "handlePos"
    for role, pos_list in positions.iteritems():
        print role, pos_list
        for pos in set(pos_list):
            try:
                castellers_in_position[pos] += cot[role]
            except KeyError:
                castellers_in_position[pos] = cot[role]
    [ineqs, pos_of_casteller] = castellers_in_position_ineqs(castellers_in_position, ineqs)
    return ineqs

def write_lp(castell_id_name):
    filename = '../www/' + pinya_dir + '/' + castell_id_name + '/pinya'
    f = open(filename + '.lp', 'w')
    f.write(xml_to_lp(filename + '.xml'))


if __name__=='__main__':
    write_lp('cvg.3de9f')
#    import cProfile
#    cProfile.run("write_lp('cvg.3de9f')", 'xml_to_lp.stats')


