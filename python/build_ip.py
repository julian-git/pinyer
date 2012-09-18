from local_config import \
    UseCBC, DoLogging, DoSolve, \
    lp_problem_filename, lp_solution_filename, lp_log_filename
from db_interaction import get_db, get_positions
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

def sol_from_v(sol, vname, castellers_in_position, _props):
    cast_id = int(vname[1:vname.find('p')])
    pos_id = long(vname[vname.find('p')+1:])
    props = ['nickname']
    props.extend(_props)
    for casteller in castellers_in_position[pos_id]:
        if casteller['id'] == cast_id:
            sol[int(pos_id)] = dict([(p, casteller[p]) for p in props])
            

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
    rename(lp_log_filename, lp_log_filename + '.1')
    rename(lp_solution_filename, lp_solution_filename + '.1')
    out_file = open(lp_log_filename, 'w')
    call(args, stdout = out_file)

def solved_positions(castellers_in_position, props):
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
                sol_from_v(sol, a[base_index], castellers_in_position, props)
    return sol

def solved_relations(relations, sol):
    sol_rel = dict()
    for rel in relations:
        positions = rel['pos_list'].split('_')
        prop = rel['field_name']
        print positions
        for i in range(0, len(positions)-1):
            for j in range(1, len(positions)):
                fp = int(positions[i])
                tp = int(positions[j])
                print fp, sol[fp], ";" , tp, sol[tp]
                sol_rel[fp, tp] = round(sol[fp][prop] - sol[tp][prop], 2)
    return sol_rel

def solution(castellers_in_position, relations, props):
    sol = solved_positions(castellers_in_position, props)
    return dict([('positions', sol), \
                     ('relations', solved_relations(relations, sol))])


def find_pinya(prescribed, castell_type_id, colla_id):
    if DoLogging:
        print "find_pinya..."    
        
    [castellers_in_position, obj, ineqs, relations] = \
        ip_ineqs(prescribed, castell_type_id, colla_id)
    # obj holds the objective coefficient of each variable
    # relations holds the relations between positions
    write_lp_file(obj, ineqs)
    if DoSolve:
        do_solve(castellers_in_position)
        
    props = ['shoulder_height', 'shoulder_width']
    return solution(castellers_in_position, relations, props)
    

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
