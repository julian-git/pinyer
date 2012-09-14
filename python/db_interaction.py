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
    c.execute("""select p.svg_id, role, role.name, is_essential, svg_id, svg_text, svg_elem, x, y, w, h, rx, ry, angle from castell_position p left join role on p.role=role.name where castell_type_id=%s""", (castell_type_id,))
    res = c.fetchall()
    for row in res:
        new_ans = dict(zip(('id', 'role', 'role_name', 'is_essential', 'svg_id', 'svg_text', 'svg_elem', 'x', 'y', 'w', 'h', 'rx', 'ry', 'angle'), row))
        for ind in ['id', 'svg_id']:
            new_ans[ind] = int(new_ans[ind])
        position_data[new_ans['id']] = new_ans
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
    return dict(zip(('name', 'description'), res))


def get_castellers(db, colla_id, castell_type_id, pos_id):
    """
    returns all castellers of the given colla that are present
    and can be employed at the given position pos
    """
    c = db.cursor()
    c.execute("""
select casteller.id, nickname, total_height, shoulder_height, shoulder_width, hip_height, stretched_height, weight, strength 
from casteller
left join casteller_role on casteller_role.casteller_id = casteller.id
left join castell_position on casteller_role.role = castell_position.role 
left join casteller_colla on casteller_colla.casteller_id = casteller.id
where is_present=true and casteller_colla.colla_id = %s and castell_position.castell_type_id = %s and castell_position.svg_id = %s 
""", (colla_id, castell_type_id, pos_id,))
    res = c.fetchall()
    ans = []
    for row in res:
        new_ans = dict(zip(('id', 'nickname', 'total_height', 'shoulder_height', 'shoulder_width', 'hip_height', 'stretched_height', 'weight', 'strength'), row))
        new_ans['id'] = int(new_ans['id'])
        ans.append(new_ans)
    return ans


def get_colla(db, colla_id):
    """
    returns all castellers of the given colla 
    """
    c = db.cursor()
    c.execute("""
select casteller.id, nickname, total_height, shoulder_height, shoulder_width, hip_height, stretched_height, weight, strength, is_present 
from casteller
left join casteller_colla on casteller_colla.casteller_id=casteller.id
where casteller_colla.colla_id = %s
""", (colla_id,))
    res = c.fetchall()
    ans = []
    for row in res:
        new_ans = dict(zip(('id', 'nickname', 'total_height', 'shoulder_height', 'shoulder_width', 'hip_height', 'stretched_height', 'weight', 'strength'), row))
        new_ans['id'] = int(new_ans['id'])
        ans.append(new_ans)
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
        new_ans = dict(zip(('id', 'castell_type_id', 'relation_type', 'field_name', 'pos_list', 'fparam1', 'fparam2', 'iparam2', 'iparam2'), row))
        for ind in ('id', 'castell_type_id', 'relation_type'):
            new_ans[ind] = int(new_ans[ind])
        ans.append(new_ans)
    return ans

def write_relations(db, castell_type_id, relations):
    """ 
    writes the relations of the given castell to the database
    """
    c = db.cursor()
    vals = []
    print relations
    for rel in relations:
        vals.append((3,  rel['pos_list'], \
                         rel['relation_type'], \
                         rel['field_name'], 
                         rel['fparam1']))
    query = """insert into castell_relation (castell_type_id, pos_list, relation_type, field_name, fparam1) 
         values (%s, %s, %s, %s, %s)"""
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


def get_avg_shoulder_width(db, colla_id):
    """ 
    the average shoulder width of the colla
    """
    c = db.cursor()
    c.execute("""
select avg(shoulder_width)
from casteller
left join casteller_colla on casteller_colla.casteller_id=casteller.id
where casteller_colla.colla_id = %s""", colla_id)
    return c.fetchall()[0][0]
