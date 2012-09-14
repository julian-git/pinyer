from db_interaction import *
from local_config import DoLogging

def var(casteller_id, pos_id):
    """
    converts a pair of (casteller_id, position_id) into an integer optimization variable name
    """
    return "c" + str(casteller_id) + "p" + str(pos_id)

def sum_vars(pos_id, castellers_in_position, prop = None, operator=" + "):
    """
    make the sum of all casteller indicator variables that involve the position pos.
    If prop is None, use 1 as a coefficient; else, use casteller[prop] if this property exists in the dictionary casteller.
    If prop does not happen to be a key of the casteller dictionary, we directly use the value of prop as a coefficient.
    """
    ineq = ''
    castellers = castellers_in_position[pos_id]
    for casteller in castellers:
        if prop is not None:
            if prop not in casteller: # then we use it as a constant coefficient
                ineq = ineq + str(prop) + " "
            else:
                ineq = ineq + str(casteller[prop]) + " "
        ineq = ineq + var(casteller['id'], pos_id) + operator
    return ineq[:-3] 

def combine_vars(from_pos_id, to_pos_id, castellers_in_position, prop):
    """
    make the difference of two sets of casteller indicator variables, with coefficient given by prop
    """
    return sum_vars(from_pos_id, castellers_in_position, prop) + " - " + sum_vars(to_pos_id, castellers_in_position, prop, " - ")

def make_castellers_in_position_ineqs(castellers_in_position, is_essential_pos, prescribed):
    """ 
    make the inequalities that say that in each position, there may be at most one casteller.
    Fill in pos_of_casteller
    """
    if DoLogging:
        print "make_castellers_in_position_ineqs"

    obj_val = dict()
    ineqs = []
    pos_of_casteller = dict() # The transposed array of castellers_in_position

    for pos_id, castellers in castellers_in_position.iteritems():
        position_ineq = '' # in position pos_id, there may be at most one casteller
        for casteller in castellers:
            casteller_id = casteller['id']
            v = var(casteller_id, pos_id)
            obj_val[v] = casteller['strength']
            position_ineq = position_ineq + v + " + "
            if casteller_id not in pos_of_casteller:
                pos_of_casteller[casteller_id] = []
            pos_of_casteller[casteller_id].append(pos_id)
        rel = " = 1"
        if not is_essential_pos[pos_id]: # in this case, allow leaving the position empty
            rel = " <= 1"
        ineqs.append("pos" + str(pos_id) + ": " + position_ineq[:-3] + rel)

    for casteller_id, positions in pos_of_casteller.iteritems():
        casteller_ineq = '' # the casteller can be in at most one position
        for pos_id in positions:
            casteller_ineq = casteller_ineq + var(casteller_id, pos_id) + " + "
        rel = " <= 1"
        label = "cas" + str(casteller_id) + ": "
        is_position_prescribed = False
        if casteller_id in prescribed: # decide whether to definitely include or exclude her
            if prescribed[casteller_id] == 0:
                rel = " = 0" # She won't participate
            else: # We fix the position where she must go
                is_position_prescribed = True
                for pos_id in positions:
                    rel2 = " = 0" # usually, she won't go to the current position
                    if pos_id == prescribed[casteller_id]:
                        rel2 = " = 1" # except when we're told she does
                    ineqs.append(label + var(casteller_id, pos_id) + rel2)
        if not is_position_prescribed:
            ineqs.append(label + casteller_ineq[:-3] + rel)

    return [obj_val, ineqs, pos_of_casteller]


def make_relation_ineqs(relations, castellers_in_position, ineqs, aux_data):
    """
    make the inequalities that express relations between different positions in the castell.
    We always build an inequality that expresses the relation between the values in 
    field_name in from_pos_id and to_pos_id.
    In case that both from_pos_id and to_pos_id exist, we also implement that
    "pinyas have no holes": 
    this means that the position to_pos_id in the castell may not be filled, unless 
    the position from_pos_id is also filled.
    """ 
    if DoLogging:
        print "make_relation_ineqs"
    for rel in relations:
        pos_list = [int(p) for p in rel['pos_list'].split('_')]
        fpi = int(pos_list[0])
        if fpi is not None and len(pos_list)>=2:
            tpi = int(pos_list[1])
            # we implement "pinyas have no holes" using binary indicator variables y_pos_id
            # that are 1 if the position pos_id is filled, and 0 otherwise
            # To simplify the system, we don't create these indicator variables explicitly,
            # but substitute them by a call to sum_vars. So, in the comments below,
            # y_fpi = sum_vars(fpi, castellers_in_position)
            # y_tpi = sum_vars(tpi, castellers_in_position)
            label = "fill_" + str(fpi) + "_" + str(tpi) + ": "
            ineqs.append(label + sum_vars(fpi, castellers_in_position) + " - " + sum_vars(tpi, castellers_in_position, None, " - ") + " >= 0")

        if rel['relation_type'] == 1: 
            # If y_tpi = 1, then the constraint 
            #   0 <= x <= tolerance
            # must hold, where 
            #   x = (value of field_name at from_pos) - (value of field_name at to_pos).
            # We model this as
            # " either y_tpi = 0  or  0 <= x <= tolerance  must hold ",
            # and this in turn as
            #   x <= tolerance + M (1 - y_tpi)
            #   x >= M (y_tpi - 1),
            # where M is a suitably large constant. In LP format, this reads
            #   x + M y_tpi <= tolerance + M
            #   x - M y_tpi >= -M
            x = combine_vars(fpi, tpi, castellers_in_position, rel['field_name'])
            M = 1000000
            label = rel['field_name'] + "_" + str(fpi) + "_" + str(tpi) + ": "
            ineqs.append(label + x + " + " + sum_vars(tpi, castellers_in_position, M) + " <= " + str(M + rel['fparam1']))
            ineqs.append(label + x + " " + sum_vars(tpi, castellers_in_position, -M, "   ") + " >= " + str(-M))

        elif rel['relation_type'] == 2: 
            # Ma can support segon:
            # value of field_name at position is at least fparam1
            label = rel['field_name'] + "_" + str(fpi) + ": "
            ineqs.append(label + sum_vars(fpi, castellers_in_position, rel['field_name']) + \
                             " >= " + str(rel['fparam1']))

        elif rel['relation_type'] == 3: 
            # sum of values is at most fparam1 in absolute value
            if len(pos_list) > 0:
                label = rel['field_name'] + "_" + rel['pos_list'] + ': '
                ineq_str = ''
                for pos in pos_list:
                    ineq_str += sum_vars(pos, castellers_in_position, rel['field_name']) + ' + '
                target_width = len(pos_list) * aux_data['avg_shoulder_width']
                ineqs.append(label + ineq_str[:-3] + " >= " + str(target_width - rel['fparam1']))
                ineqs.append(label + ineq_str[:-3] + " <= " + str(target_width + rel['fparam1']))

        else:
            print "implement me!"

def make_incompatibility_ineqs(db, colla_id, pos_of_casteller, relations, ineqs):
    """
    the database contains pairs of incompatible castellers in the colla.
    here we create the inequalities that express that no two incompatible
    castellers may be employed in any pair of positions related by a relation.
    """
    if DoLogging:
        print "make_incompatibility_ineqs"
    incompatible_castellers = get_incompatible_castellers(db, colla_id)
    for pair in incompatible_castellers:
        p0 = int(pair[0])
        p1 = int(pair[1])
        label = "incomp_" + str(p0) + "_" + str(p1) + ": "
        positions = pos_of_casteller[p0]
        positions.extend(pos_of_casteller[p1])
        positions = set(positions)
        for rel in relations:
            pos_list = rel['pos_list'].split('_')
            if rel['relation_type'] == 1 and len(pos_list)>=2:
                fpi = pos_list[0]
                tpi = pos_list[1]
                if fpi in positions and tpi in positions:
                    ineqs.append(label + var(p0, fpi) + " + " + var(p1, tpi) + " <= 1")
                    ineqs.append(label + var(p0, tpi) + " + " + var(p1, fpi) + " <= 1")
                

def ip_ineqs(prescribed, castell_type_id, colla_id):
    """
    Create the linear inequalities that define the integer program to be solved.
    Fill the dictionaries castellers_in_position, position_data and obj_val.
    as a side effect, calculate the dictionary pos_of_casteller.
    """
    if DoLogging:
        print "ip_ineqs"

    castellers_in_position = dict()
    is_essential_pos = dict()

    db = get_db()
    position_data = get_positions(db, castell_type_id)

    for pos_id, pos in position_data.iteritems():
        is_essential_pos[pos_id] = pos['is_essential']
        castellers_in_position[pos_id] = get_castellers(db, colla_id, castell_type_id, pos_id)

    [obj_val, ineqs, pos_of_casteller] = make_castellers_in_position_ineqs(castellers_in_position, is_essential_pos, prescribed)

    relations = get_relations(db, castell_type_id)

    aux_data = dict([('avg_shoulder_width', get_avg_shoulder_width(db, colla_id))])
    make_relation_ineqs(relations, castellers_in_position, ineqs, aux_data)
    make_incompatibility_ineqs(db, colla_id, pos_of_casteller, relations, ineqs)

    return [castellers_in_position, obj_val, ineqs]
