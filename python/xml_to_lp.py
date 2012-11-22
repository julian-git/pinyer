import xml.dom.minidom
from local_config import RootDir, pinya_dir, \
    numeric_splitter, text_splitter, field_splitter, pos_types
import sys 
sys.path.append(RootDir + 'python/util/')
from db_interaction import get_db, castellers_of_type, db_avg_shoulder_width
from ineqs import relation_ineq, castellers_in_position_ineqs
import pickle

def xml_to_lp(xmlfilename):
    ineqs = []
    obj = dict()
    [ineqs, obj, vars, ineq_reps] = xml_to_lp_impl(xmlfilename, ineqs, obj)
    var_string = ' '.join(vars.values())
    obj_string = []
    # for var, coeff in obj.iteritems():
    #     if coeff > 0:
    #         obj_string.append('+ ' + str(coeff) + ' ' + var)
    #     elif coeff < 0:
    #         obj_string.append('- ' + str(-coeff) + ' ' + var)
    for var, coeff in obj.iteritems():
        obj_string.append(var)
        break
    return [ineqs, '\n'.join(('maximize', \
                          ' '.join(obj_string), \
                          'subject to', \
                          '\n'.join(ineqs), \
                          'binary', \
                          var_string, \
                         '\n')), \
                ineq_reps]

def xml_to_lp_impl(xmlfilename, ineqs, obj):
    f = open(xmlfilename + '.xml', 'r')
    dom = xml.dom.minidom.parseString(f.read())
    frel = open(xmlfilename + '.rels', 'w')
    return handleXML(dom.documentElement, ineqs, obj, frel)


def handleXML(xml, ineqs, obj, frel):
    castell_id_name = xml.getElementsByTagName('castell')[0].getAttribute('castell_id_name')
    colla_id_name = xml.getElementsByTagName('colla')[0].getAttribute('colla_id_name')

    db = get_db()
    (cot, aux_data) = castellers(db, colla_id_name)

    pos_with_role = dict()
    for child in xml.getElementsByTagName('positions')[0].childNodes:
        if child.nodeName == 'position':
            pos_with_role = RoleOfPosition(child, pos_with_role)
        elif child.nodeName == 'position_group':
            for child2 in child.childNodes:
                if child2.nodeName == 'position':
                    pos_with_role = RoleOfPosition(child2, pos_with_role)

    ineq_reps = []
    for child in xml.getElementsByTagName('relations')[0].childNodes:
        if child.nodeName == 'relation':
            [ineqs, obj, ineq_reps] = handleRelation(child, cot, aux_data, ineqs, obj, frel, ineq_reps)

    [ineqs, vars] = IneqsOfPositions(db, cot, ineqs, pos_with_role)
    return [ineqs, obj, vars, ineq_reps]


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
    [ineqs, pos_of_casteller, vars] = castellers_in_position_ineqs(castellers_in_position, ineqs)
    return [ineqs, vars]


def castellers(db, colla_id_name):
    aux_data = dict([('avg_shoulder_width', db_avg_shoulder_width(db, colla_id_name))])
    cot = dict()
    for role in pos_types:
        cot[role] = castellers_of_type(db, colla_id_name, role)
    return (cot, aux_data)

def extract_or_null(relation, field_name, convert_to_float=True):
    try:
        val = relation.getAttribute(field_name)
        if convert_to_float:
            return float(val)
        else:
            return val
    except ValueError:
        return None

def handleRelation(relation, cot, aux_data, ineqs, obj, frel, ineq_reps):
    field_names = [str(f) for f in relation.getAttribute('field_names').split(text_splitter)]
    pos_list = [int(p) for p in relation.getAttribute('pos_list').split(numeric_splitter)]
    role_list = [r for r in str(relation.getAttribute('role_list')).split(text_splitter)]
    coeff_list = [float(c) for c in relation.getAttribute('coeff_list').split(numeric_splitter)]
    relation_type = relation.getAttribute('relation_type')
    sense = '<='
    if relation.getAttribute('sense') != 'le':
        sense = '>='

    rhs = extract_or_null(relation, 'rhs')
    min_tol = extract_or_null(relation, 'min_tol')
    max_tol = extract_or_null(relation, 'max_tol')
    target_val = extract_or_null(relation, 'target_val')
    fresh_field = extract_or_null(relation, 'fresh_field', False)

    if target_val is not None:
        lo = target_val - min_tol
        hi = target_val + max_tol
        lo_hi = str(lo) + numeric_splitter + str(hi) 
        role_list = relation.getAttribute('role_list')
        pos_list = relation.getAttribute('pos_list')
        coeff_list = relation.getAttribute('coeff_list')
        field_names = relation.getAttribute('field_names')
        frel.write(field_splitter.join([role_list, pos_list, coeff_list, field_names, \
                                            lo_hi]) + '\n')
        rs = role_list.split(text_splitter)
        ps = pos_list.split(numeric_splitter)
        cs = coeff_list.split(numeric_splitter)
        fs = field_names.split(text_splitter)
        ineq_reps.append((role_list, build_ineq_rep(rs, ps, cs, fs, lo_hi)))

        [ineqs, obj] = relation_ineq(relation_type, cot, ps, rs, cs, fs, sense, rhs, target_val, min_tol, max_tol, fresh_field, aux_data, ineqs, obj)
    return [ineqs, obj, ineq_reps]

def build_ineq_rep(rs, ps, cs, fs, lo_hi):
    ineq_rep = []
    lo = lo_hi.split(numeric_splitter)[0]
    hi = lo_hi.split(numeric_splitter)[1]
    role_ct = dict()
    for role in rs:
        role_ct[role] = -1
    for i in range(len(rs)):
        role_ct[rs[i]] = role_ct[rs[i]] + 1
        multiplicity = ''
        if role_ct[rs[i]] >= 2:
            multiplicity = '_' + str(role_ct[rs[i]])
        if float(cs[i]) == 1:
            pass
        elif float(cs[i]) == -1:
            ineq_rep.append('-')
        else:
            ineq_rep.append(cs[i])
        
        ineq_rep.append(fs[i] + '[' + rs[i] + multiplicity + ']')
    ineq_rep.append('in [' + str(lo) + ', ' + str(hi) + ']')
    return ' '.join(ineq_rep)

def write_relations(frel, rel_list):
    for rel in rel_list:
        lo = float(rel['target_val']) - float(rel['min_tol'])
        hi = float(rel['target_val']) + float(rel['max_tol'])
        frel.write(field_splitter.join([\
                    text_splitter.join(rel['field_names']), \
                        numeric_splitter.join([str(p) for p in rel['pos_list']]), \
                        numeric_splitter.join([str(c) for c in rel['coeff_list']]),
                    str(lo) + numeric_splitter + str(hi) \
                    ]) + '\n')

def write_lp(castell_id_name):
    filename = RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya'
    [ineqs, lp_string, ineq_reps] = xml_to_lp(filename)

    f1 = open(filename + '.lp', 'w')
    f1.write(lp_string)

    f2 = open(filename + '.ineq_reps', 'w')
    pickle.dump(set(ineq_reps), f2)


if __name__=='__main__':
    write_lp('cvg.3de9f')
#    import cProfile
#    cProfile.run("write_lp('cvg.3de9f')", 'xml_to_lp.stats')


