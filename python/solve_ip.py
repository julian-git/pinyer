from local_config import \
    UseCBC, DoLogging, DoSolve, \
    numeric_splitter, text_splitter, \
    pinya_dir
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

def solve_castell(filename):
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

def relation_values_from_solution(relations, sol):
    rel_val = dict()
    for rel in relations:
        positions = rel['pos_list'].split(numeric_splitter)
        prop = rel['field_names'].split(text_splitter)
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

def solve_castell(prescribed, castell_id_name, colla_id_name):
    if DoLogging:
        print 'solve_castell...'
        
    filename = '../www/' + pinya_dir + '/' + castell_id_name + '/pinya.complete'

    if DoSolve:
        solve_castell(filename)
        
    castellers = db_castellers(get_db(), colla_id_name)
    sol = read_solved_positions(filename, castellers)
    return dict([('positions', sol), \
                     ('relations', '')]) #relation_values_from_solution(relations, sol))])
    

def make_excluded():
    c = get_db().cursor()
    c.execute("""
select id from casteller where nickname in ('Abdul', 'AE', 'Aina', 'Alaitz', 'Aleix', 'Alvarito', 'Arnau', 'Berta', 'Eva', 'Joana', 'Joanet', 'Laia O', 'Lali', 'Marco', 'Martina', 'Montxi', 'Oriolet', 'Rafols', 'Rai', 'Santako', 'Stefano');
""")
    ans = []
    for row in c.fetchall():
        ans.append(int(row[0]))
    return ans

def complete_lp(prescribed, excluded, castell_id_name, colla_id_name):
    filename = '../www/' + pinya_dir + '/' + castell_id_name + '/pinya'
    fin = open(filename + '.lp', 'r')
    fout = open(filename + '.complete.lp', 'w')
    line = fin.readline()
    while line != 'binary\n':
        fout.write(line)
        line = fin.readline()
    vars = fin.readline().split()
    for var in vars:
        [cast_id, pos_id] = split_var(var)
        if cast_id in excluded:
            fout.write('excl: ' + var + ' = 0\n')
    fout.write('binary\n' + ' '.join(vars))

def do_opt():
#    prescribed = dict([(9, 0), (17, 5)])

    excluded = make_excluded()
    prescribed = dict()
    [castell_id_name, colla_id_name] = ['cvg.3de9f', 'cvg']
    complete_lp(prescribed, excluded, castell_id_name, colla_id_name)
    solution = solve_castell(prescribed, castell_id_name, colla_id_name)
    filename =  '../www/' + pinya_dir + '/' + castell_id_name + '/pinya' 
    fin = open(filename + '.svg', 'r')
    fout = open(filename + '.solved.svg', 'w')
    t = Template(fin.read())
    positions = solution['positions']
    sol = dict()
    for i in positions.keys():
        sol['_' + str(i)] = positions[i]['nickname']
        sol['_c' + str(i)] = str(positions[i]['shoulder_height']) + \
            '_' + str(positions[i]['id'])
    fout.write(t.safe_substitute(sol))
    print [[pos, c['nickname']] for [pos, c] in solution['positions'].iteritems()]
    print solution['relations']

if __name__ == "__main__":
#    import cProfile
#    cProfile.run('do_opt()', 'build_ip.stats')
    do_opt()
