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
select member.id 
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

db = MySQLdb.connect(user="pinyol", passwd="pinyol01", db="pinyol")

ineqs = []
members_in_position = dict()
for pos in get_positions(db, castell_type_id):
    members_in_position[pos[0]] = get_members(db, colla_id, pos[0])
    ineq = ''
    for mem in members_in_position[pos[0]]:
        ineq = ineq + var(mem, pos[0]) + " + "
    ineqs.append(ineq[:-3] + " <= 1")

for rel in get_relations(db, castell_type_id):
    if rel[3] is not None:
        ineq = ''
        from_mems = members_in_position[rel[2]]
        for from_mem in from_mems:
            ineq = ineq + var(from_mem, rel[2]) + " + "
        ineq = ineq[:-3] + " - "
        to_mems = members_in_position[rel[3]]
        for to_mem in to_mems:
            ineq = ineq + var(to_mem, rel[3]) + " - "
        ineqs.append(ineq[:-3] + " <= 0")
print ineqs
