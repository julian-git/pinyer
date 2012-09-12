from MySQLdb import connect
from string import Template

def get_db():
    return connect(user="pinyer", passwd="", db="pinyer")


def get_positions(db, castell_type_id):
    """
    returns all id numbers of the positions in the given castell type
    """
    position_data = dict()
    c = db.cursor()
    c.execute("""select p.id, role_id, role.name, is_essential, svg_id, svg_text, svg_elem, x, y, w, h, rx, ry from castell_position p left join role on p.role_id=role.id where castell_type_id=%s""", (castell_type_id,))
    res = c.fetchall()
    for row in res:
        position_data[int(row[0])] = dict([('role_id', int(row[1])), ('role_name', row[2]), ('is_essential', row[3]), ('svg_id', row[4]), ('svg_text', row[5]), ('svg_elem', row[6]), ('x', row[7]), ('y', row[8]), ('w', row[9]), ('h', row[10]), ('rx', row[11]), ('ry', row[12])])
    return position_data

def write_positions(db, castell_type_id, position_at):
    """ 
    writes the positions of the given castell to the database
    """
    c = db.cursor()
    vals = []
    for pos_id, pos in position_at.iteritems():
        vals.append((3, \
                         pos['role'], \
                         pos['svg_id'], \
                         pos['svg_text'], \
                         pos['x'], \
                         pos['y'], \
                         pos['angle']))
    query = """insert into castell_position (castell_type_id, role, svg_id, svg_text, x, y, angle)
         values (%s, %s, %s, %s, %s, %s, %s)"""
    c.executemany(query, vals)

def get_castell(db, castell_type_id):
    """
    returns the characteristics of the castell with the given id
    """
    c = db.cursor()
    c.execute("""select name, description from castell_type where id=%s""", (castell_type_id,))
    res = c.fetchall()[0]
    return dict([('name', res[0]), ('description', res[1])])


def get_castellers(db, colla_id, pos_id):
    """
    returns all castellers of the given colla that are present
    and can be employed at the given position pos
    """
    c = db.cursor()
    c.execute("""
select casteller.id, nickname, total_height, shoulder_height, hip_height, stretched_height, weight, strength 
from casteller
left join casteller_role on casteller_role.casteller_id = casteller.id
left join castell_position on casteller_role.role_id = castell_position.role_id 
left join casteller_colla on casteller.id = casteller_colla.casteller_id 
where is_present=true and castell_position.id = %s and casteller_colla.colla_id = %s
""", (pos_id,colla_id,))
    res = c.fetchall()
    ans = []
    for row in res:
        ans.append(dict([('id', int(row[0])), ('nickname', row[1]), ('total_height', row[2]), ('shoulder_height', row[3]), ('hip_height', row[4]), ('stretched_height', row[5]), ('weight', row[6]), ('strength', row[7])]))
    return ans


def get_colla(db, colla_id):
    """
    returns all castellers of the given colla 
    """
    c = db.cursor()
    c.execute("""
select casteller.id, nickname, total_height, shoulder_height, hip_height, stretched_height, weight, strength, is_present 
from casteller
left join casteller_colla on casteller_colla.casteller_id=casteller.id
where casteller_colla.colla_id = %s
""", (colla_id,))
    res = c.fetchall()
    ans = []
    for row in res:
        ans.append(dict([('id', int(row[0])), ('nickname', row[1]), ('total_height', row[2]), ('shoulder_height', row[3]), ('hip_height', row[4]), ('stretched_height', row[5]), ('weight', row[6]), ('strength', row[7]), ('is_present', row[8])]))
    return ans

def get_nicknames_and_char(db, colla_id, char):
    """
    returns the nicknames of all castellers of the given colla 
    """
    c = db.cursor()
    tpl = Template("""
select casteller.id, nickname, ${_char} as c
from casteller
left join casteller_colla on casteller_colla.casteller_id=casteller.id
where casteller_colla.colla_id = %s order by c
""")
    c.execute(tpl.substitute(_char=char), (colla_id,))
    res = c.fetchall()
    ans = []
    for row in res:
        ans.append(dict([('id', int(row[0])), ('nickname', row[1]), ('c', row[2])]))
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

def write_relations(db, castell_type_id, relations):
    """ 
    writes the relations of the given castell to the database
    """
    c = db.cursor()
    vals = []
    for rel in relations:
        vals.append((3, \
                         rel['from_pos_id'], \
                         rel['to_pos_id'], \
                         rel['pos_list'],
                         rel['relation_type'], \
                         rel['field_name'], 
                         rel['fparam1']))
    query = """insert into castell_relation (castell_type_id, from_pos_id, to_pos_id, pos_list, relation_type, field_name, fparam1) 
         values (%s, %s, %s, %s, %s, %s, %s)"""
    print query
    print vals
    c.executemany(query, vals)
    

def get_incompatible_castellers(db, colla_id):
    """
    returns all pairs of incompatible castellers in a colla
    """
    c = db.cursor()
    c.execute("""select cast1_id, cast2_id from incompatible_castellers where colla_id=%s""", (colla_id,))
    return c.fetchall()
