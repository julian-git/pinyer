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
