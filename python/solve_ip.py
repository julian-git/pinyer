from local_config import \
    RootDir, \
    UseCBC, DoLogging, DoSolve, \
    numeric_splitter, text_splitter, field_splitter, \
    pinya_dir
import sys 
sys.path.append(RootDir + 'python/util/')
from db_interaction import get_db, db_castellers
from subprocess import call 
from os import rename
from string import Template
import pickle

def split_var(vname):
    cast_id = int(vname[1:vname.find('p')])
    pos_id = int(vname[vname.find('p')+1:])
    return [cast_id, pos_id]

def sol_from_v(sol, vname, castellers):
    [cast_id, pos_id] = split_var(vname)
    sol[pos_id] = castellers[cast_id]
            
def backup_file(filename):
    try:
        rename(filename, filename + '.1')
    except OSError:
        pass

def run_solver(filename):
    lp_filename = filename + '.complete.lp'
    sol_filename = filename + '.complete.sol'
    log_filename = filename + '.complete.log'
    if UseCBC:
        args = ['cbc', '-import', lp_filename, '-solve', '-solu', sol_filename, '-quit']
    else:
        args = ['gurobi_cl', 'ResultFile=' + sol_filename, lp_filename]
        base_index = 0  # for reading the solution file
    if DoLogging:
        if UseCBC:
            print "solving lp with cbc..."
        else:
            print "solving with gurobi..."
    for f in (log_filename, sol_filename):
        backup_file(f)
    out_file = open(log_filename, 'w')
    call(args, stdout = out_file)

def read_solved_positions(filename, castellers):
    if UseCBC:
        base_index = 1  # for reading the solution file
    else:
        base_index = 0  # for reading the solution file
    f = open(filename + '.complete.sol', 'r')
    sol = dict()
    first_line = True
    for line in f:
        if first_line:
            first_line = False
        else:
            a = line.split()
            if float(a[base_index + 1]) > 0.5:
                sol_from_v(sol, a[base_index], castellers)
    if len(sol.keys()) == 0:
        raise RuntimeError("Solution file empty. No solution found")
    return sol

def read_solved_relations_from_file(filename):
    rels = []
    frel = open(filename + '.rels', 'r')
    for line in frel:
        rels.append(line.split(field_splitter))
    return rels

def read_solved_relations(filename, sol):
    rels = read_solved_relations_from_file(filename)
    rel_vals = []
    for [role_list, pos_list, coeff_list, field_names, bounds] in rels: 
        fs = field_names.split(text_splitter)
        ps = pos_list.split(numeric_splitter)
        cs = coeff_list.split(numeric_splitter)
        val = 0
        for i in range(len(fs)):
            val += float(cs[i]) * sol[int(ps[i])][fs[i]]
        rel_vals.append([pos_list, round(val, 2)])
    return rel_vals

def solve_castell(castell_id_name, colla_id_name):
    if DoLogging:
        print 'solve_castell...'
        
    filename = RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya'

    if DoSolve:
        run_solver(filename)
        
    castellers = db_castellers(get_db(), colla_id_name)
    positions = read_solved_positions(filename, castellers)
    f = open('pinya.solved_positions', 'w')
    pickle.dump(positions, f)

    relations = read_solved_relations(filename, positions)
    return [positions, relations] 


def do_opt():
    [castell_id_name, colla_id_name] = ['cvg.3de9f', 'cvg']
    [positions, relations] = solve_castell(castell_id_name, colla_id_name)
    filename =  RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya' 
    fin = open(filename + '.svg', 'r')
    fout = open(filename + '.solved.svg', 'w')
    froles = open(filename + '.roles', 'r')
    role_of = pickle.load(froles)
    t = Template(fin.read())
    sol = dict()
    for i in positions.keys():
        casteller = positions[i]
        sol['_' + str(i)] = str(i) + '&#10;' + casteller['nickname']
        sol['_c' + str(i)] = str(casteller['shoulder_height']) 
        sol['_rep' + str(i)] = casteller['svg_rep']
        sol['_alt' + str(i) + '_text'] = casteller['alt_text']
        sol['_class_' + str(casteller['id'])] = role_of[i]
    for pos, val in relations:
        sol['_rel' + pos] = str(val)
    solved_svg = t.safe_substitute(sol)
    # now substitute again so that the _class_## fields in the database get substituted, too
    solved_svg = Template(solved_svg).safe_substitute(sol) 
    fout.write(solved_svg)
    print [[pos, c['nickname']] for [pos, c] in positions.iteritems()]
    print relations

if __name__ == "__main__":
#    import cProfile
#    cProfile.run('do_opt()', 'build_ip.stats')
    do_opt()
