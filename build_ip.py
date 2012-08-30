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


def var(casteller_id, pos_id):
    """
    converts a pair of (casteller_id, position_id) into an integer optimization variable name
    """
    return "c" + str(casteller_id) + "p" + str(pos_id)

def make_ineq1(pos_id, castellers_in_position, prop, operator=" + "):
    """
    make part of an inequality using the position pos and the property indexed by prop_index
    """
    ineq = ''
    from_castellers = castellers_in_position[pos_id]
    for from_casteller in from_castellers:
        ineq = ineq + str(from_casteller[prop]) + " " + var(from_casteller['id'], pos_id) + operator
    ineq = ineq[:-3] 
    return ineq 

def make_ineq2(from_pos_id, to_pos_id, castellers_in_position, prop):
    """
    make the LHS of an inequality using two positions and the property indexed by prop_index
    """
    return make_ineq1(from_pos_id, castellers_in_position, prop) + " - " + make_ineq1(to_pos_id, castellers_in_position, prop, " - ")

def make_castellers_in_position_ineqs(castellers_in_position, is_essential_pos, participation, obj_val, ineqs):
    """ 
    make the inequalities that say that in each position, there may be at most one casteller
    """
    pos_of_casteller = dict() # The transposed array of castellers_in_position

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
            label = "rel" + str(rel['from_pos_id']) + "_" + str(rel['to_pos_id']) + ": "
            ineqs.append(label + ineq_terms + " >= 0")
            ineqs.append(label + ineq_terms + " <= " + str(rel['fparam1']))

        elif rel['relation_type'] == 2: 
            # Ma can support segon:
            # value of field_name at position is at least fparam1
            ineqs.append("h" + str(rel['from_pos_id']) + ": " + make_ineq1(rel['from_pos_id'], castellers_in_position, rel['field_name']) + " >= " + str(rel['fparam1']))

        elif rel_type == 3: # weight at position is at least fparam1
            print "implement me!\n"


def ip_ineqs(castellers_in_position, participation = dict(), castell_type_id = 1, colla_id = 1): # CVG and p4 
    import MySQLdb

    db = MySQLdb.connect(user="pinyol", passwd="pinyol01", db="pinyol")

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

def make_lp_file(t):
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

def write_lp_file(castellers_in_position, participation, filename='pinya.lp'):
    f = open(filename, 'w')
    f.write(make_lp_file(ip_ineqs(castellers_in_position, participation)))
    f.close()

def find_pinya(participation, filename='pinya.lp'):
    import sys
    sys.path.append('/opt/gurobi500/linux32/lib/python2.7')
    from gurobipy import read

    castellers_in_position = dict()
    write_lp_file(castellers_in_position, participation, filename)

    model=read(filename)
    model.optimize()
    if model.status == 2:
        sv = model.getVars()
        sol = dict()
        for v in sv:
            if v.x == 1:
                vname = v.var_name
                cast_id = vname[1:vname.find('p')]
                pos_id = long(vname[vname.find('p')+1:])
                for casteller in castellers_in_position[pos_id]:
                    if casteller['id'] == int(cast_id):
                        sol[int(pos_id)] = casteller['name']
        return sol
    else:
        return False
    

if __name__ == "__main__":
    castellers_in_position = dict()
    participation = dict([(9, 0), (17, 5)])
#    print lp_file(ip_ineqs(castellers_in_position, participation))
    print find_pinya(participation)
