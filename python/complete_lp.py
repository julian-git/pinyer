from local_config import RootDir, pinya_dir
import sys 
sys.path.append(RootDir + 'python/util/')
from db_interaction import get_db
from solve_ip import split_var

def complete_lp_impl(prescribed, excluded, castell_id_name, colla_id_name):
    filename = RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya'
    fin = open(filename + '.lp', 'r')
    fout = open(filename + '.complete.lp', 'w')
    frel = open(filename + '.complete.rels', 'w')
    line = fin.readline()
    while line != 'binary\n':
        if line[0:4] == 'rel_':
            frel.write(line[4:line.find(':')] + '\n')
        fout.write(line)
        line = fin.readline()
    vars = fin.readline().split()
    for var in vars:
        [cast_id, pos_id] = split_var(var)
        if cast_id in excluded:
            fout.write('excl: ' + var + ' = 0\n')
    fout.write('binary\n' + ' '.join(vars))

def make_excluded():
    c = get_db().cursor()
    c.execute("""
select id from casteller where nickname in ('Abdul', 'AE', 'Aina', 'Alaitz', 'Aleix', 'Alvarito', 'Arnau', 'Berta', 'Eva', 'Joana', 'Joanet', 'Laia O', 'Lali', 'Marco', 'Martina', 'Montxi', 'Oriolet', 'Rafols', 'Rai', 'Santako', 'Stefano');
""")
    ans = []
    for row in c.fetchall():
        ans.append(int(row[0]))
    return ans

def complete_lp():
    excluded = make_excluded()
    prescribed = dict()
    [castell_id_name, colla_id_name] = ['cvg.3de9f', 'cvg']
    complete_lp_impl(prescribed, excluded, castell_id_name, colla_id_name)

if __name__=="__main__":
    complete_lp()
