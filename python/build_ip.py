from local_config import \
    UseCBC, DoLogging, DoSolve, \
    lp_problem_filename, lp_solution_filename, lp_log_filename, \
    pos_splitter, field_name_splitter
from db_interaction import get_db
from ineqs import ip_ineqs
from subprocess import call 
from os import rename

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
    cast_id = int(vname[1:vname.find('p')])
    pos_id = long(vname[vname.find('p')+1:])
    for casteller in castellers_in_position[pos_id]:
        if casteller['id'] == cast_id:
            sol[int(pos_id)] = casteller
            
def backup_file(filename):
    try:
        rename(filename, filename + '.1')
    except OSError:
        pass

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
    for f in (lp_log_filename, lp_solution_filename):
        backup_file(f)
    out_file = open(lp_log_filename, 'w')
    call(args, stdout = out_file)

def read_solved_positions(castellers_in_position):
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
    if len(sol.keys()) == 0:
        raise RuntimeError("Solution file empty. No solution found")
    return sol

def relation_values_from_solution(relations, sol):
    rel_val = dict()
    for rel in relations:
        positions = rel['pos_list'].split(pos_splitter)
        prop = rel['field_names'].split(field_name_splitter)
        if len(positions) != len(prop):
            print "positions = ", positions
            print "prop = ", prop 
            raise RuntimeError("positions and prop have different length")
        for i in range(0, len(positions)-1):
            for j in range(1, len(positions)):
                fp = int(positions[i])
                tp = int(positions[j])
                rel_val[fp, tp] = round(sol[fp][prop[j]] - sol[tp][prop[j]], 2)
    return rel_val

def solve_castell(prescribed, castell_type_id, colla_id):
    if DoLogging:
        print "find_pinya..."    
        
    [castellers_in_position, obj, ineqs, relations] = \
        ip_ineqs(prescribed, castell_type_id, colla_id)
    # obj holds the objective coefficient of each variable
    # relations holds the relations between positions

    write_lp_file(obj, ineqs)
    if DoSolve:
        do_solve(castellers_in_position)
        
    sol = read_solved_positions(castellers_in_position)
    return dict([('positions', sol), \
                     ('relations', relation_values_from_solution(relations, sol))])
    

def do_opt():
#    prescribed = dict([(9, 0), (17, 5)])
    prescribed = dict()
##########
# FIXME: castell_type_id and colla_id can be chosen independently
#        and this leads to inconsistency and data leakage
    [castell_type_id, colla_id] = [1000, 2]  # for debugging
#    [castell_type_id, colla_id] = [3, 1] # for "real"
##########
    solution = solve_castell(prescribed, castell_type_id, colla_id)
    print [[pos,c['nickname']] for [pos, c] in solution['positions'].iteritems()]
    print solution['relations']

if __name__ == "__main__":
#    import cProfile
#    cProfile.run('do_opt()', 'build_ip.stats')
    do_opt()
