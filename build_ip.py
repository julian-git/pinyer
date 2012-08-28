def get_positions(db, castell_type_id):
    """
    returns all id numbers of the positions in the given castell type
    """
    c = db.cursor()
    c.execute("""select id, is_essential from castell_position where castell_type_id=%s""", (castell_type_id,))
    return c.fetchall()

def get_castellers(db, colla_id, pos_id):
    """
    returns all castellers of the given colla that can be employed at the given position pos
    """
    c = db.cursor()
    c.execute("""
select casteller.id, total_height, shoulder_height, hip_height, stretched_height, weight, strength 
from casteller
left join casteller_role on casteller_role.casteller_id = casteller.id
left join castell_position on casteller_role.role_id = castell_position.role_id 
left join casteller_colla on casteller.id = casteller_colla.casteller_id 
where castell_position.id = %s and casteller_colla.colla_id = %s
""", (pos_id,colla_id,))
    return c.fetchall()

def get_relations(db, castell_type_id):
    """
    returns all relations between positions in the given castell_type_id
    """
    c = db.cursor()
    c.execute("""select * from castell_relation where castell_type_id=%s""", (castell_type_id,))
    return c.fetchall()

def var(casteller_id, pos_id):
    """
    converts a pair of (casteller_id, position_id) into an integer optimization variable name
    """
    return "c" + str(casteller_id) + "p" + str(pos_id)

def make_ineq1(pos_id, castellers_in_position, prop_index, operator=" + "):
    """
    make part of an inequality using the position pos and the property indexed by prop_index
    """
    ineq = ''
    from_castellers = castellers_in_position[pos_id]
    for from_casteller in from_castellers:
        prop = from_casteller[prop_index]
        ineq = ineq + str(prop) + " " + var(from_casteller[0], pos_id) + operator
    ineq = ineq[:-3] 
    return ineq 

def make_ineq2(from_pos_id, to_pos_id, castellers_in_position, prop_index):
    """
    make the LHS of an inequality using two positions and the property indexed by prop_index
    """
    return make_ineq1(from_pos_id, castellers_in_position, prop_index) + " - " + make_ineq1(to_pos_id, castellers_in_position, prop_index, " - ")

def make_castellers_in_position_ineqs(castellers_in_position, is_essential_pos, participation, obj_val, ineqs):
    """ 
    make the inequalities that say that in each position, there may be at most one casteller
    """
    pos_of_casteller = dict() # The transposed array of castellers_in_position

    for pos_id, castellers in castellers_in_position.iteritems():
        position_ineq = '' # in position pos_id, there may be at most one casteller
        for casteller in castellers:
            casteller_id = casteller[0]; casteller_strength = casteller[6]
            v = var(casteller_id, pos_id)
            obj_val[v] = casteller_strength
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
        if casteller_id in participation: # decide whether to definitely include or exclude her
            if participation[casteller_id]:
                rel = " = 1"
            else:
                rel = " = 0"
        ineqs.append("cas" + str(casteller_id) + ": " + casteller_ineq[:-3] + rel)


def make_relation_ineqs(relations, castellers_in_position, ineqs):
    """
    make the inequalities that express relations between different positions in the castell
    """ 
    for rel in relations:
        rel_type, from_pos, to_pos, tolerance = rel[2:6]

        if rel_type == 1: 
            # rengla descends weakly: 
            # 0 <= (total height at from_pos) - (total_height at to_pos) <= tolerance
            if from_pos is None or to_pos is None:
                print "Error in relation ", rel, ": from_pos or to_pos is None"
                break
            ineq_terms = make_ineq2(from_pos, to_pos, castellers_in_position, 1)
            label = "rel" + str(from_pos) + "_" + str(to_pos) + ": "
            ineqs.append(label + ineq_terms + " >= 0")
            ineqs.append(label + ineq_terms + " <= " + str(tolerance))

        elif rel_type == 2: 
            # Ma can support segon:
            # stretched_height at position is at least fparam1
            if from_pos is None:
                print "Error in relation ", rel, ": from_pos is None"
                break
            ineqs.append("h" + str(from_pos) + ": " + make_ineq1(from_pos, castellers_in_position, 5) + " >= " + str(tolerance))

        elif rel_type == 3: # weight at position is at least fparam1
            print "implement me!\n"


def ip_ineqs(participation = dict(), castell_type_id = 1, colla_id = 1): # CVG and p4 
    import MySQLdb

    db = MySQLdb.connect(user="pinyol", passwd="pinyol01", db="pinyol")

    castellers_in_position = dict()
    is_essential_pos = dict()
    for pos in get_positions(db, castell_type_id):
        pos_id = pos[0]
        is_essential_pos[pos_id] = pos[1]
        castellers_in_position[pos_id] = get_castellers(db, colla_id, pos_id)

    obj_val = dict()
    ineqs = []
    make_castellers_in_position_ineqs(castellers_in_position, is_essential_pos, participation, obj_val, ineqs)

    relations = get_relations(db, castell_type_id)
    make_relation_ineqs(relations, castellers_in_position, ineqs)

    return [obj_val, ineqs]

def lp_format(t):
    obj_val, ineqs = t
    f = "maximize\n"
    variables = sorted(obj_val.keys())
    for v in variables:
        f = f + str(obj_val[v]) + " " + str(v) + " + "
    f = f[:-3] + "\nsubject to\n"
    for ineq in ineqs:
        f = f + ineq + "\n"
    f = f + "binary\n"
    for v in variables:
        f = f + v + " "
    return f

if __name__ == "__main__":
    participation = dict([(9, False), (17, True)])
    print lp_format(ip_ineqs(participation))
