from db_interaction import *
from local_config import DoLogging, numeric_splitter, text_splitter

vars = dict()

def var(casteller_id, pos_id):
    """
    converts a pair of (casteller_id, position_id) into an integer optimization variable name
    """
    try:
        return vars[casteller_id, pos_id]
    except KeyError:
        v = 'c' + str(casteller_id) + 'p' + str(pos_id)
        vars[casteller_id, pos_id] = v
        return v

def sum_vars(pos_id, castellers, field_name = None, operator = '+ ', coeff = 1):
    """
    make the sum of all casteller indicator variables that involve the position pos.
    If field_name is None, use coeff(=1) as a coefficient; 
    else, use casteller[field_name] if this property exists in the dictionary casteller,
    If field_name does not happen to be a key of the casteller dictionary, 
    we directly use its value as a coefficient.
    """
    ineq = ''
    firstTerm = True
    for casteller in castellers:
        if firstTerm:
            firstTerm = False
        else:
            ineq += operator

        if field_name is not None:
            if field_name not in casteller: # then we use it as a constant coefficient
                ineq += stringify(coeff * field_name) + ' '
            else:
                ineq += stringify(coeff * casteller[field_name]) + ' '
        ineq += var(casteller['id'], pos_id)  + ' '
    return ineq

def stringify(val):
    if val>=0:
        return str(val)
    else:
        return '- ' + str(-val)

def combine_vars(from_pos_id, to_pos_id, from_castellers, to_castellers, field_names):
    """
    make the difference of two sets of casteller indicator variables.
    The coefficient of the first set is field_names[0], 
    the coefficient of the second set is field_names[1].
    """
    return sum_vars(from_pos_id, from_castellers, field_names[0]) + \
        '- ' + sum_vars(to_pos_id, to_castellers, field_names[1], '- ')



def castellers_in_position_ineqs(castellers_in_position, ineqs):
    """ 
    write the inequalities that say that in each position, there may be at most one casteller.
    Fill in pos_of_casteller
    """
    if DoLogging:
        print "castellers_in_position_ineqs"

    pos_of_casteller = dict() # The transposed array of castellers_in_position

    for pos_id, castellers in castellers_in_position.iteritems():
        position_ineq = '' # in position pos_id, there may be at most one casteller
        first_pos_ineq = True
        for casteller in castellers:
            casteller_id = casteller['id']
            v = var(casteller_id, pos_id)
            if first_pos_ineq:

                first_pos_ineq = False
            else:
                position_ineq += " + "
            position_ineq += v
            if casteller_id not in pos_of_casteller:
                pos_of_casteller[casteller_id] = []
            pos_of_casteller[casteller_id].append(pos_id)
        rel = " = 1"
#        if not is_essential_pos[pos_id]: # in this case, allow leaving the position empty
#            rel = " <= 1"
        ineq = "pos" + str(pos_id) + ": " + position_ineq + rel
        ineqs.append(ineq)

    for casteller_id, positions in pos_of_casteller.iteritems():
        casteller_ineq = '' # the casteller can be in at most one position
        first_cast_ineq = True
        for pos_id in positions:
            if first_cast_ineq:
                first_cast_ineq = False
            else:
                casteller_ineq += " + "
            casteller_ineq += var(casteller_id, pos_id)
        rel = " <= 1"
        label = "cas" + str(casteller_id) + ": "
        # is_position_prescribed = False
        # if casteller_id in prescribed: # decide whether to definitely include or exclude her
        #     if prescribed[casteller_id] == 0:
        #         rel = " = 0" # She won't participate
        #     else: # We fix the position where she must go
        #         is_position_prescribed = True
        #         for pos_id in positions:
        #             rel2 = " = 0" # usually, she won't go to the current position
        #             if pos_id == prescribed[casteller_id]:
        #                 rel2 = " = 1" # except when we're told she does
        #             ineqs.append(label + var(casteller_id, pos_id) + rel2)
        # if not is_position_prescribed:
        ineqs.append(label + casteller_ineq + rel)

    return [ineqs, pos_of_casteller]


def relation_ineq(relation_type, cot, pos_list, role_list, coeff_list, field_names, sense, rhs, target_val, min_tol, max_tol, fresh_field, aux_data, ineqs, obj): #, rel, castellers_in_position, aux_data, ineqs, obj):
    """
    write the inequalities that express relations between different positions in the castell.
    We always build an inequality that expresses the relation between the values in 
    field_names in from_pos_id and to_pos_id.
    In case that both from_pos_id and to_pos_id exist, we also implement that
    "pinyas have no holes": 
    this means that the position to_pos_id in the castell may not be filled, unless 
    the position from_pos_id is also filled.
    """ 
    if DoLogging:
        print "relation_ineq"

    fpi = pos_list[0]
    for casteller in cot[role_list[0]]:
        obj[var(casteller['id'], fpi)] = 1

    if fpi is not None and len(pos_list)>=2: # There are at least two positions to consider
        tpi = pos_list[1]
        for casteller in cot[role_list[1]]:
            obj[var(casteller['id'], tpi)] = 1

    if relation_type == 'val_tol': 
        # Ma can support segon:
        # value of field_names at position is at least fparam
        if rel['field_names'].find(text_splitter) > -1:
            raise RuntimeError('Expected only one property in ' + rel['field_names']) 
        label = text_splitter.join(field_names) + "_" + str(fpi) + ": "
        ineqs.append(label + \
                         sum_vars(fpi, cot[role_list[0]], field_names) + \
                         " >= " + \
                         str(rhs))

    elif relation_type in ('sum_in_interval', 'fresh_sum_in_interval', 'one_sided'): 
        # sum of values is at most rhs in absolute value
        if len(pos_list) == 0:
            raise RuntimeError('Expected pos_list to be nonempty, in sum_in_interval')
        label = text_splitter.join(field_names) + "_" + numeric_splitter.join([str(p) for p in pos_list]) + ': '
        ineq_str = ''
        pos_ct = -1
        for pos in pos_list:
            pos_ct = pos_ct + 1
            for c in cot[role_list[pos_ct]]:
                coeff = coeff_list[pos_ct] * c[field_names[pos_ct]]
                if coeff >= 0:
                    ineq_str += ' + '
                ineq_str += stringify(coeff) + ' ' + var(c['id'], pos) + ' '
                
        if relation_type in ('sum_in_interval', 'fresh_sum_in_interval'):
            if relation_type == 'fresh_sum_in_interval':
                _target_val = len(pos_list) * aux_data[fresh_field]
            else:
                _target_val = target_val
            ineqs.append(label + ineq_str + " >= " + str(_target_val - max_tol))
            ineqs.append(label + ineq_str + " <= " + str(_target_val + max_tol))

        else:
            ineq = label + ineq_str + ' ' + sense + ' ' + str(rhs)
            ineqs.append(ineq)

    else:
        raise RuntimeError('relation of type ' + relation_type + ' not implemented!')
    return [ineqs, obj]

def incompatibility_ineqs(db, colla_id_name, pos_of_casteller, relations, ineqs):
    """
    the database contains pairs of incompatible castellers in the colla.
    here we create the inequalities that express that no two incompatible
    castellers may be employed in any pair of positions related by a relation.
    """
    if DoLogging:
        print "write_incompatibility_ineqs"
    incompatible_castellers = db_incompatible_castellers(db, colla_id_name)
    for pair in incompatible_castellers:
        p0 = int(pair[0])
        p1 = int(pair[1])
        label = "incomp_" + str(p0) + "_" + str(p1) + ": "
        positions = pos_of_casteller[p0]
        positions.extend(pos_of_casteller[p1])
        positions = set(positions)
        for rel in relations:
            pos_list = rel['pos_list'].split(numeric_splitter)
            if rel['relation_type'] == 1 and len(pos_list)>=2:
                fpi = pos_list[0]
                tpi = pos_list[1]
                if fpi in positions and tpi in positions:
                    ineqs.append(label + var(p0, fpi) + " + " + var(p1, tpi) + " <= 1")
                    ineqs.append(label + var(p0, tpi) + " + " + var(p1, fpi) + " <= 1")
    return ineqs

# def ip_ineqs(castellers_in_position):
#     """
#     Create the linear inequalities that define the integer program to be solved.
#     Fill the dictionaries castellers_in_position, position_data and obj_val.
#     as a side effect, calculate the dictionary pos_of_casteller.
#     """
#     if DoLogging:
#         print "ip_ineqs"


#     obj = objective_function(castellers_in_position)

#     ineqs = []
#     [ineqs, pos_of_casteller] = \
#         castellers_in_position_ineqs(castellers_in_position, is_essential_pos, prescribed, ineqs)

#     relations = get_relations(db, castell_type_id_name)
#     aux_data = dict([('avg_shoulder_width', get_avg_shoulder_width(db, colla_id_name))])

#     [ineqs, obj] = relation_ineqs(relations, castellers_in_position, aux_data, ineqs, obj)
#     ineqs = incompatibility_ineqs(db, colla_id_name, pos_of_casteller, relations, ineqs)

#     return [castellers_in_position, obj, ineqs, relations]
