from local_config import std_problem_filename, std_solution_filename, std_log_filename
from db_interaction import get_db, get_positions

def make_lp_file(obj_val, ineqs):
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
    f = f + "\nend"
    return f

def write_lp_file(castellers_in_position, position_data, prescribed, castell_type_id, colla_id, lp_problem_filename):
    from ineqs import ip_ineqs
    f = open(lp_problem_filename, 'w')
    obj_val = dict()          # The objective coefficient of each variable
    ineqs = []                # the linear inequalities
    ip_ineqs(castellers_in_position, position_data, obj_val, ineqs, prescribed, castell_type_id, colla_id)
    f.write(make_lp_file(obj_val, ineqs))
    f.close()

def sol_from_v(sol, vname, castellers_in_position):
     cast_id = vname[1:vname.find('p')]
     pos_id = long(vname[vname.find('p')+1:])
     for casteller in castellers_in_position[pos_id]:
         if casteller['id'] == int(cast_id):
             sol[int(pos_id)] = [casteller['id'], casteller['nickname']]


def solve_lp_with_gurobi(lp_problem_filename, castellers_in_position):
    from gurobipy import read
    model=read(lp_problem_filename)
    model.optimize()
    if model.status == 2:
        sv = model.getVars()
        sol = dict()
        for v in sv:
            if v.x == 1:
                sol_from_v(sol, v.varname, castellers_in_position)
        return sol
    else:
        return False


def solve_lp_with_cbc(lp_problem_filename, castellers_in_position, lp_solution_filename=std_solution_filename, lp_log_filename=std_log_filename):
    from subprocess import call 
    out_file = open(lp_log_filename, 'w')
    call(["cbc", '-import', lp_problem_filename, '-solve', '-solu', lp_solution_filename, '-quit'], stdout=out_file)
    f = open(lp_solution_filename, 'r')
    sol = dict()
    first_line = True
    for line in f:
        if first_line:
            first_line = False
        else:
            a = line.split()
            if a[2] == '1':
                sol_from_v(sol, a[1], castellers_in_position)
    return sol


def find_pinya(prescribed, position_data, castell_type_id, colla_id, lp_problem_filename=std_problem_filename, lp_log_filename=std_log_filename):
    import local_config
    castellers_in_position = dict()
    write_lp_file(castellers_in_position, position_data, prescribed, castell_type_id, colla_id, lp_problem_filename)
    if local_config.UseCBC:
        return solve_lp_with_cbc(lp_problem_filename, castellers_in_position, std_solution_filename, lp_log_filename)
    else:
        return solve_lp_with_gurobi(lp_problem_filename, castellers_in_position)
    

if __name__ == "__main__":
#    prescribed = dict([(9, 0), (17, 5)])
    prescribed = dict()
    castell_type_id = 1
    db = get_db()
    position_data = get_positions(db, castell_type_id)
    colla_id = 2
    solution = find_pinya(prescribed, position_data, castell_type_id, colla_id, '/tmp/test_pinya.lp', '/tmp/test_log.txt')
    print solution
