from MySQLdb import connect
from string import Template

def get_db():
    return connect(user="pinyer", passwd="", db="pinyer")


def db_castell(db, castell_type_id):
    """
    returns the characteristics of the castell with the given id
    """
    c = db.cursor()
    c.execute("""select name, description from castell_type where id=%s""", (castell_type_id,))
    res = c.fetchall()[0]
    return dict(zip(('name', 'description'), res))


def db_castellers(db, colla_id_name):
    c = db.cursor()
    c.execute("""
select casteller.id, nickname, total_height, shoulder_height, shoulder_width, hip_height, stretched_height, axle_height, weight, strength 
from casteller
left join casteller_colla on casteller_colla.casteller_id = casteller.id
where casteller_colla.colla_id_name = %s 
""", (colla_id_name,))
    res = c.fetchall()
    ans = dict()
    for row in res:
        new_ans = dict(zip(('id', 'nickname', 'total_height', 'shoulder_height', 'shoulder_width', 'hip_height', 'stretched_height', 'axle_height', 'weight', 'strength'), row))
        new_ans['id'] = int(new_ans['id'])
        ans[new_ans['id']] = new_ans
    if len(ans)==0:
        raise RuntimeError('No castellers found for colla_id_name=' + str(colla_id_name))
    return ans

def castellers_of_type(db, colla_id_name, role):
    c = db.cursor()
    c.execute("""
select casteller.id, nickname, total_height, shoulder_height, shoulder_width, hip_height, stretched_height, axle_height, weight, strength 
from casteller
left join casteller_role on casteller_role.casteller_id = casteller.id
left join casteller_colla on casteller_colla.casteller_id = casteller.id
where casteller_colla.colla_id_name = %s and casteller_role.role = %s 
""", (colla_id_name, role,))
    res = c.fetchall()
    ans = []
    for row in res:
        new_ans = dict(zip(('id', 'nickname', 'total_height', 'shoulder_height', 'shoulder_width', 'hip_height', 'stretched_height', 'axle_height', 'weight', 'strength'), row))
        new_ans['id'] = int(new_ans['id'])
        ans.append(new_ans)
    if len(ans)==0:
        raise RuntimeError('No castellers found for colla_id_name=' + str(colla_id_name) + \
                               ', casteller_role=' + str(role))
    return ans


def db_colla(db, colla_id):
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

def db_nicknames_and_char(db, colla_id, char):
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


def db_incompatible_castellers(db, colla_id):
    """
    returns all pairs of incompatible castellers in a colla
    """
    c = db.cursor()
    c.execute("""select cast1_id, cast2_id from incompatible_castellers where colla_id=%s""", (colla_id,))
    return c.fetchall()


def db_avg_shoulder_width(db, colla_id):
    """ 
    the average shoulder width of all members in the colla
    that are present
    """
    c = db.cursor()
    c.execute("""
select avg(shoulder_width)
from casteller
left join casteller_colla on casteller_colla.casteller_id=casteller.id
where casteller_colla.colla_id_name = %s and is_present = true""", colla_id)
    return c.fetchall()[0][0]
