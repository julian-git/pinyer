from local_config import \
    RootDir, \
    UseCBC, DoLogging, DoSolve, \
    numeric_splitter, text_splitter, \
    pinya_dir
import sys 
sys.path.append(RootDir + 'python/util/')
from db_interaction import get_db, db_castellers
from subprocess import call 
from os import rename
from string import Template

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
    if UseCBC:
        args = ['cbc', '-import', filename + '.lp', '-solve', '-solu', filename + '.sol', '-quit']
    else:
        args = ['gurobi_cl', 'ResultFile=' + filename + '.sol', filename + '.lp']
        base_index = 0  # for reading the solution file
    if DoLogging:
        if UseCBC:
            print "solving lp with cbc..."
        else:
            print "solving with gurobi..."
    for f in (filename + '.log', filename + '.sol'):
        backup_file(f)
    out_file = open(filename + '.log', 'w')
    call(args, stdout = out_file)

def read_solved_positions(filename, castellers):
    if UseCBC:
        base_index = 1  # for reading the solution file
    else:
        base_index = 0  # for reading the solution file
    f = open(filename + '.sol', 'r')
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
        rel = line.split(text_splitter)
        if len(rel) > 3: 
            # there is more than one field 
            # (the last entries are positions and bounds)
            positions = rel[-2].split(numeric_splitter)
            bounds = rel[-1].split(numeric_splitter)
            bounds[-1] = bounds[-1][:-1] # get rid of trailing newline
            rels.append([rel[:-2], positions, bounds])
    return rels

def read_solved_relations(filename, sol):
    rels = read_solved_relations_from_file(filename)
    rel_vals = []
    for [fields, positions, bounds] in rels:
        for i in range(len(fields)):
            fp = int(positions[i])
            for j in range(i+1, len(fields)):
                tp = int(positions[j])
                rel_vals.append([str(fp) + '_' + str(tp), \
                                     round(abs(sol[fp][fields[i]] - sol[tp][fields[i]]), 2)])
    return rel_vals

def solve_castell(castell_id_name, colla_id_name):
    if DoLogging:
        print 'solve_castell...'
        
    filename = RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya.complete'

    if DoSolve:
        run_solver(filename)
        
    castellers = db_castellers(get_db(), colla_id_name)
    positions = read_solved_positions(filename, castellers)
    relations = read_solved_relations(filename, positions)
    return [positions, relations] 


def do_opt():
    [castell_id_name, colla_id_name] = ['cvg.3de9f', 'cvg']
    [positions, relations] = solve_castell(castell_id_name, colla_id_name)
    filename =  RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya' 
    fin = open(filename + '.svg', 'r')
    fout = open(filename + '.solved.svg', 'w')
    t = Template(fin.read())
    sol = dict()
    for i in positions.keys():
        casteller = positions[i]
        sol['_' + str(i)] = casteller['nickname']
        sol['_c' + str(i)] = str(casteller['shoulder_height']) 
    for pos, val in relations:
        sol['_rel' + pos] = str(val)
    fout.write(t.safe_substitute(sol))
    print [[pos, c['nickname']] for [pos, c] in positions.iteritems()]
    print relations

if __name__ == "__main__":
#    import cProfile
#    cProfile.run('do_opt()', 'build_ip.stats')
    do_opt()
