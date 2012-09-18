from local_config import \
    UseCBC, DoLogging, DoSolve, \
    lp_problem_filename, lp_solution_filename, lp_log_filename
from db_interaction import get_db, get_positions
from ineqs import ip_ineqs
from subprocess import call 

def write_lp_file(obj, ineqs):
    if DoLogging:
        print "write_lp_file..."
    f = open(lp_problem_filename, 'w')

    f.write('maximize\n')
    for v, val in obj.iteritems():
        if val > 0:
            s = ' + '
        elif val == 0:
            continue
        else:
            s = ' '
        f.write(s + str(val) + ' ' + v)
    f.write('\nsubject to\n')
    for ineq in ineqs:
        f.write(ineq)
        f.write('\n')
    f.write('\nbinary\n')
    for v in sorted(obj.keys()):
        f.write(v + " ")
    f.write('\nend')
    f.close()

def sol_from_v(sol, vname, castellers_in_position):
    cast_id = vname[1:vname.find('p')]
    pos_id = long(vname[vname.find('p')+1:])
    for casteller in castellers_in_position[pos_id]:
        if casteller['id'] == int(cast_id):
            sol[int(pos_id)] = [casteller['id'], casteller['nickname']]
            

def do_solve(castellers_in_position):
    if UseCBC:
        args = ['cbc', '-import', lp_problem_filename, '-solve', '-solu', lp_solution_filename, '-quit']
    else:
        args = ['gurobi_cl', 'ResultFile=' + lp_solution_filename, lp_problem_filename]
        base_index = 0  # for reading the solution file
    if DoLogging:
        if UseCBC:
            print "solving lp with cbc..."
        else:
            print "solving with gurobi..."
    out_file = open(lp_log_filename, 'w')
    call(args, stdout = out_file)

def solution(castellers_in_position):
    if UseCBC:
        base_index = 1  # for reading the solution file
    else:
        base_index = 0  # for reading the solution file
    f = open(lp_solution_filename, 'r')
    sol = dict()
    first_line = True
    for line in f:
        if first_line:
            first_line = False
        else:
            a = line.split()
            if a[base_index + 1] == '1':
                sol_from_v(sol, a[base_index], castellers_in_position)
    return sol

def solve_lp(castellers_in_position):
    if DoSolve:
        do_solve(castellers_in_position)
    return solution(castellers_in_position)

def find_pinya(prescribed, castell_type_id, colla_id):
    if DoLogging:
        print "find_pinya..."    
        
    [castellers_in_position, obj, ineqs] = ip_ineqs(prescribed, castell_type_id, colla_id)
    # obj holds the objective coefficient of each variable
    write_lp_file(obj, ineqs)
    return solve_lp(castellers_in_position)
    

def do_opt():
#    prescribed = dict([(9, 0), (17, 5)])
    prescribed = dict()
##########
# FIXME: castell_type_id and colla_id can be chosen independently
#        and this leads to inconsistency and data leak
#    [castell_type_id, colla_id] = [1, 2]  # for debugging
    [castell_type_id, colla_id] = [3, 1] # for "real"
##########
    solution = find_pinya(prescribed, castell_type_id, colla_id)
    print solution

if __name__ == "__main__":
#    import cProfile
#    cProfile.run('do_opt()', 'build_ip.stats')
    do_opt()
