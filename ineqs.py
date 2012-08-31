from db_interaction import *

def var(casteller_id, pos_id):
    """
    converts a pair of (casteller_id, position_id) into an integer optimization variable name
    """
    return "c" + str(casteller_id) + "p" + str(pos_id)

def make_ineq1(pos_id, castellers_in_position, prop, operator=" + "):
    """
    make the sum of all variables using the position pos, with the value of the property prop as coefficient
    """
    ineq = ''
    castellers = castellers_in_position[pos_id]
    for casteller in castellers:
        ineq = ineq + str(casteller[prop]) + " " + var(casteller['id'], pos_id) + operator
    ineq = ineq[:-3] 
    return ineq 

def make_ineq2(from_pos_id, to_pos_id, castellers_in_position, prop):
    """
    make the LHS of an inequality using two positions and the property prop
    """
    return make_ineq1(from_pos_id, castellers_in_position, prop) + " - " + make_ineq1(to_pos_id, castellers_in_position, prop, " - ")

def make_castellers_in_position_ineqs(castellers_in_position, is_essential_pos, participation, obj_val, ineqs, pos_of_casteller):
    """ 
    make the inequalities that say that in each position, there may be at most one casteller
    """
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
        if casteller_id in participation: # decide whether to definitely include or exclude her
            if participation[casteller_id] == 0:
                rel = " = 0" # She won't participate
            else: # We fix the position where she must go
                is_position_prescribed = True
                for pos_id in positions:
                    rel2 = " = 0" # usually, she won't go to the current position
                    if pos_id == participation[casteller_id]:
                        rel2 = " = 1" # except when we're told she does
                    ineqs.append(label + var(casteller_id, pos_id) + rel2)
        if not is_position_prescribed:
            ineqs.append(label + casteller_ineq[:-3] + rel)


def make_relation_ineqs(relations, castellers_in_position, ineqs):
    """
    make the inequalities that express relations between different positions in the castell
    """ 
    for rel in relations:
        if rel['relation_type'] == 1: 
            # compare two values
            # 0 <= (value of field_name at from_pos) - (value of field_name at to_pos) <= tolerance
            ineq_terms = make_ineq2(rel['from_pos_id'], rel['to_pos_id'], castellers_in_position, rel['field_name'])
            label = rel['field_name'] + "_" + str(rel['from_pos_id']) + "_" + str(rel['to_pos_id']) + ": "
            ineqs.append(label + ineq_terms + " >= 0")
            ineqs.append(label + ineq_terms + " <= " + str(rel['fparam1']))

        elif rel['relation_type'] == 2: 
            # Ma can support segon:
            # value of field_name at position is at least fparam1
            label = rel['field_name'] + "_" + str(rel['from_pos_id']) + ": "
            ineqs.append(label + make_ineq1(rel['from_pos_id'], castellers_in_position, rel['field_name']) + " >= " + str(rel['fparam1']))

        elif rel_type == 3: # weight at position is at least fparam1
            print "implement me!\n"

def make_incompatibility_ineqs(db, colla_id, pos_of_casteller, relations, ineqs):
    incompatible_castellers = get_incompatible_castellers(db, colla_id)
    for pair in incompatible_castellers:
        p0 = int(pair[0])
        p1 = int(pair[1])
        label = "incomp_" + str(p0) + "_" + str(p1) + ": "
        positions = pos_of_casteller[p0]
        positions.extend(pos_of_casteller[p1])
        positions = set(positions)
        for rel in relations:
            if rel['relation_type'] == 1 and rel['from_pos_id'] in positions and rel['to_pos_id'] in positions:
                ineqs.append(label + var(p0, rel['from_pos_id']) + " + " + var(p1, rel['to_pos_id']) + " <= 1")
                ineqs.append(label + var(p0, rel['to_pos_id']) + " + " + var(p1, rel['from_pos_id']) + " <= 1")
                

def ip_ineqs(castellers_in_position, position_data, obj_val, ineqs, participation = dict(), castell_type_id = 1, colla_id = 1): # CVG and p4 
    import MySQLdb

    db = MySQLdb.connect(user="pinyol", passwd="pinyol01", db="pinyol")

    is_essential_pos = dict()
    get_positions(db, castell_type_id, position_data)
    for pos_id, pos in position_data.iteritems():
        is_essential_pos[pos_id] = pos['is_essential']
        castellers_in_position[pos_id] = get_castellers(db, colla_id, pos_id)

    pos_of_casteller = dict() # The transposed array of castellers_in_position
    make_castellers_in_position_ineqs(castellers_in_position, is_essential_pos, participation, obj_val, ineqs, pos_of_casteller)

    relations = get_relations(db, castell_type_id)
    make_relation_ineqs(relations, castellers_in_position, ineqs)

    make_incompatibility_ineqs(db, colla_id, pos_of_casteller, relations, ineqs)

