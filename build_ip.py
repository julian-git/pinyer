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

def get_members(db, colla, pos):
    """
    returns all members of the given colla that can be employed at the given position pos
    """
    c = db.cursor()
    c.execute("""
select member.id, total_height, shoulder_height, hip_height, stretched_height, weight 
from member
left join member_role on member_role.member_id = member.id
left join castell_position on member_role.role_id = castell_position.role_id 
left join member_colla on member.id = member_colla.member_id 
where castell_position.id = %s and member_colla.colla_id = %s
""", (pos,colla,))
    return c.fetchall()

def get_relations(db, castell_type_id):
    """
    returns all relations between positions in the given castell_type_id
    """
    c = db.cursor()
    c.execute("""select * from castell_relation where castell_type_id=%s""", (castell_type_id,))
    return c.fetchall()

def var(member, pos):
    """
    converts a pair of (member_id, position_id) into an integer optimization variable name
    """
    return "x_" + str(member[0]) + "_" + str(pos)

def make_ineq1(pos, members_in_position, prop_index):
    """
    make the LHS of an inequality using the position pos and the property indexed by prop_index
    """
    ineq = ''
    from_mems = members_in_position[pos]
    for from_mem in from_mems:
        prop = from_mem[prop_index]
        ineq = ineq + str(prop) + " " + var(from_mem, pos) + " + "
    ineq = ineq[:-3] 
    return ineq 

def make_ineq2(from_pos, to_pos, members_in_position, prop_index):
    """
    make the LHS of an inequality using two positions and the property indexed by prop_index
    """
    ineq = make_ineq1(from_pos, members_in_position, prop_index) + " - "
    to_mems = members_in_position[to_pos]
    for to_mem in to_mems:
        prop = to_mem[prop_index]
        ineq = ineq + str(prop) + " " + var(to_mem, to_pos) + " - "
    return ineq


db = MySQLdb.connect(user="pinyol", passwd="pinyol01", db="pinyol")

ineqs = []
members_in_position = dict()
for pos in get_positions(db, castell_type_id):
    pos_id = pos[0]
    members_in_position[pos_id] = get_members(db, colla_id, pos_id)
    ineq = ''
    for mem in members_in_position[pos_id]:
        ineq = ineq + var(mem, pos_id) + " + "
    ineqs.append(ineq[:-3] + " <= 1")

for rel in get_relations(db, castell_type_id):
    rel_type, from_pos, to_pos, tolerance = rel[2:6]
    if rel_type == 1: # (total height at from_pos) - (total_height at to_pos) <= tolerance
        if from_pos is None or to_pos is None:
            print "Error in relation ", rel, ": from_pos or to_pos is None"
            break
        ineq = make_ineq2(from_pos, to_pos, members_in_position, 1)
        ineqs.append(ineq[:-3] + " <= " + str(tolerance))

    elif rel_type == 2: # stretched_height at position is at least fparam1
        if from_pos is None:
            print "Error in relation ", rel, ": from_pos is None"
            break
        ineq = make_ineq1(from_pos, members_in_position, 5)
        ineqs.append(ineq + " >= " + str(tolerance))

    elif rel_type == 3: # weight at position is at least fparam1
        print

        
print ineqs
