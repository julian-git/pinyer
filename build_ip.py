from ineqs import * 

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
