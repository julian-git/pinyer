import MySQLdb

colla_id = 1  # CVG
castell_type_id = 1  # p4

def get_positions(db, castell_type_id):
    """
    returns all id numbers of the positions in the given castell type
    """
    c = db.cursor()
    c.execute("""select id from castell_position where castell_type_id=%s""", (castell_type_id,))
    return c.fetchall()

def get_castellers(db, colla, pos):
    """
    returns all castellers of the given colla that can be employed at the given position pos
    """
    c = db.cursor()
    c.execute("""
select casteller.id, total_height, shoulder_height, hip_height, stretched_height, weight 
from casteller
left join casteller_role on casteller_role.casteller_id = casteller.id
left join castell_position on casteller_role.role_id = castell_position.role_id 
left join casteller_colla on casteller.id = casteller_colla.casteller_id 
where castell_position.id = %s and casteller_colla.colla_id = %s
""", (pos,colla,))
    return c.fetchall()

def get_relations(db, castell_type_id):
    """
    returns all relations between positions in the given castell_type_id
    """
    c = db.cursor()
    c.execute("""select * from castell_relation where castell_type_id=%s""", (castell_type_id,))
    return c.fetchall()

def var(casteller, pos):
    """
    converts a pair of (casteller_id, position_id) into an integer optimization variable name
    """
    return "c" + str(casteller[0]) + "p" + str(pos)

def make_ineq1(pos, castellers_in_position, prop_index, operator=" + "):
    """
    make part of an inequality using the position pos and the property indexed by prop_index
    """
    ineq = ''
    from_mems = castellers_in_position[pos]
    for from_mem in from_mems:
        prop = from_mem[prop_index]
        ineq = ineq + str(prop) + " " + var(from_mem, pos) + operator
    ineq = ineq[:-3] 
    return ineq 

def make_ineq2(from_pos, to_pos, castellers_in_position, prop_index):
    """
    make the LHS of an inequality using two positions and the property indexed by prop_index
    """
    return make_ineq1(from_pos, castellers_in_position, prop_index) + " - " + make_ineq1(to_pos, castellers_in_position, prop_index, " - ")

def make_castellers_in_position_ineqs(db, castellers_in_position, ineqs):
    """ 
    make the inequalities that say that in each position, there may be at most one casteller
    """
    for pos in get_positions(db, castell_type_id):
        pos_id = pos[0]
        castellers_in_position[pos_id] = get_castellers(db, colla_id, pos_id)
        ineq = ''
        for mem in castellers_in_position[pos_id]:
            ineq = ineq + var(mem, pos_id) + " + "
        ineqs.append(ineq[:-3] + " <= 1")

def make_relation_ineqs(db, castellers_in_position, ineqs):
    """
    make the inequalities that express relations between different positions in the castell
    """ 
    for rel in get_relations(db, castell_type_id):
        rel_type, from_pos, to_pos, tolerance = rel[2:6]

        if rel_type == 1: # (total height at from_pos) - (total_height at to_pos) <= tolerance
            if from_pos is None or to_pos is None:
                print "Error in relation ", rel, ": from_pos or to_pos is None"
                break
            ineqs.append(make_ineq2(from_pos, to_pos, castellers_in_position, 1) + " <= " + str(tolerance))

        elif rel_type == 2: # stretched_height at position is at least fparam1
            if from_pos is None:
                print "Error in relation ", rel, ": from_pos is None"
                break
            ineqs.append(make_ineq1(from_pos, castellers_in_position, 5) + " >= " + str(tolerance))

        elif rel_type == 3: # weight at position is at least fparam1
            print


db = MySQLdb.connect(user="pinyol", passwd="pinyol01", db="pinyol")

ineqs = []
castellers_in_position = dict()
make_castellers_in_position_ineqs(db, castellers_in_position, ineqs)
make_relation_ineqs(db, castellers_in_position, ineqs)

        
print ineqs
