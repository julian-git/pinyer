from local_config import std_problem_filename, std_solution_filename, std_log_filename, DoLogging, UseCBC
from db_interaction import get_db, get_positions
from subprocess import call 

def make_lp_file(f, obj_val, ineqs):
    if DoLogging:
        print "make_lp_file..."

    f.write("maximize\n")
    variables = sorted(obj_val.keys())
    is_first = True
    for v in variables:
        if is_first:
            is_first = False
        else: 
            f.write(' + ')
        f.write(str(obj_val[v]) + " " + str(v))
    f.write("\nsubject to\n")
    for ineq in ineqs:
        f.write(ineq + "\n")
    f.write("binary\n")
    for v in variables:
        f.write(v + " ")
    f.write("\nend")
    if DoLogging:
        print "done."

def write_lp_file(castellers_in_position, position_data, prescribed, castell_type_id, colla_id, lp_problem_filename):
    if DoLogging:
        print "write_lp_file..."
    from ineqs import ip_ineqs
    f = open(lp_problem_filename, 'w')
    obj_val = dict()          # The objective coefficient of each variable
    ineqs = []                # the linear inequalities
    ip_ineqs(castellers_in_position, position_data, obj_val, ineqs, prescribed, castell_type_id, colla_id)
    make_lp_file(f, obj_val, ineqs)
    f.close()

def sol_from_v(sol, vname, castellers_in_position):
    cast_id = vname[1:vname.find('p')]
    pos_id = long(vname[vname.find('p')+1:])
    for casteller in castellers_in_position[pos_id]:
        if casteller['id'] == int(cast_id):
            sol[int(pos_id)] = [casteller['id'], casteller['nickname']]
            

def solve_lp(lp_problem_filename, castellers_in_position, \
                 lp_solution_filename=std_solution_filename, \
                 lp_log_filename=std_log_filename):
    if UseCBC:
        args = ["cbc", '-import', lp_problem_filename, '-solve', '-solu', lp_solution_filename, '-quit']
    else:
        args = ['gurobi_cl', 'ResultFile=' + lp_solution_filename, lp_problem_filename]
    if DoLogging:
        if UseCBC:
            print "solving lp with cbc..."
        else:
            print "solving with gurobi..."
    out_file = open(lp_log_filename, 'w')
    call(args, stdout = out_file)
    f = open(lp_solution_filename, 'r')
    sol = dict()
    first_line = True
    if UseCBC:
        base_index = 1
    else:
        base_index = 0
    for line in f:
        if first_line:
            first_line = False
        else:
            a = line.split()
            if a[base_index + 1] == '1':
                sol_from_v(sol, a[base_index], castellers_in_position)
    return sol


def find_pinya(prescribed, position_data, castell_type_id, colla_id, lp_problem_filename=std_problem_filename, lp_log_filename=std_log_filename):
    if DoLogging:
        print "find_pinya..."    
    import local_config
    castellers_in_position = dict()
    write_lp_file(castellers_in_position, position_data, prescribed, castell_type_id, colla_id, lp_problem_filename)
    return solve_lp(lp_problem_filename, castellers_in_position, \
                        std_solution_filename, lp_log_filename)
    

if __name__ == "__main__":
#    prescribed = dict([(9, 0), (17, 5)])
    prescribed = dict()
##########
# FIXME: castell_type_id and colla_id can be chosen independently
#        and this leads to inconsistency and data leak
#    [castell_type_id, colla_id] = [1, 2]  # for debugging
    [castell_type_id, colla_id] = [3, 1] # for "real"
##########
    db = get_db()
    position_data = get_positions(db, castell_type_id)
    solution = find_pinya(prescribed, position_data, castell_type_id, colla_id, '/tmp/test_pinya.lp', '/tmp/test_log.txt')
    print solution
