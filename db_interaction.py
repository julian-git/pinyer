def get_positions(db, castell_type_id):
    """
    returns all id numbers of the positions in the given castell type
    """
    c = db.cursor()
    c.execute("""select id, role_id, is_essential, svg_id, svg_text, x, y, w, h, rx, ry from castell_position where castell_type_id=%s""", (castell_type_id,))
    res = c.fetchall()
    ans = []
    for row in res:
        ans.append(dict([('id', int(row[0])), ('role_id', int(row[1])), ('is_essential', row[2]), ('svg_id', row[3]), ('svg_text', row[4]), ('x', row[5]), ('y', row[6]), ('w', row[7]), ('h', row[8]), ('rx', row[9]), ('ry', row[10])]))
    return ans
    return c.fetchall()

def get_castellers(db, colla_id, pos_id):
    """
    returns all castellers of the given colla that can be employed at the given position pos
    """
    c = db.cursor()
    c.execute("""
select casteller.id, name, total_height, shoulder_height, hip_height, stretched_height, weight, strength 
from casteller
left join casteller_role on casteller_role.casteller_id = casteller.id
left join castell_position on casteller_role.role_id = castell_position.role_id 
left join casteller_colla on casteller.id = casteller_colla.casteller_id 
where castell_position.id = %s and casteller_colla.colla_id = %s
""", (pos_id,colla_id,))
    res = c.fetchall()
    ans = []
    for row in res:
        ans.append(dict([('id', int(row[0])), ('name', row[1]), ('total_height', row[2]), ('shoulder_height', row[3]), ('hip_height', row[4]), ('stretched_height', row[5]), ('weight', row[6]), ('strength', row[7])]))
    return ans

def get_relations(db, castell_type_id):
    """
    returns all relations between positions in the given castell_type_id
    """
    c = db.cursor()
    c.execute("""select * from castell_relation where castell_type_id=%s""", (castell_type_id,))
    res = c.fetchall()
    ans = []
    for row in res:
        ans.append(dict([('id', int(row[0])), ('castell_type_id', int(row[1])), ('relation_type', int(row[2])), ('field_name', row[3]), ('from_pos_id', row[4]), ('to_pos_id', row[5]), ('fparam1', row[6]), ('fparam2', row[7]), ('iparam2', row[8]), ('iparam2', row[9])]))
    return ans

def get_incompatible_castellers(db, colla_id):
    """
    returns all pairs of incompatible castellers in a colla
    """
    c = db.cursor()
    c.execute("""select cast1_id, cast2_id from incompatible_castellers where colla_id=%s""", (colla_id,))
    return c.fetchall()
