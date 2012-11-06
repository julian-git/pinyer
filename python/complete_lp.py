from local_config import RootDir, pinya_dir, text_splitter, numeric_splitter
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
    last_rel = ''
    bounds = []
    while line != 'binary\n':
        if line[0:4] == 'rel_': # output relations into auxiliary file frel
            new_rel = line[4:line.find(':')]
            bounds.append(float(line[line.find('=')+2:-1]))
            if new_rel == last_rel:
                sbounds = sorted(bounds)
                bounds = []
                frel.write(new_rel + text_splitter + str(sbounds[0]) + \
                               numeric_splitter + str(sbounds[1]) + '\n')
            else:
                last_rel = new_rel
        fout.write(line)
        line = fin.readline()
    vars = fin.readline().split()
    for var in vars:
        [cast_id, pos_id] = split_var(var)
        if cast_id in excluded:
            fout.write('excl: ' + var + ' = 0\n')
        elif cast_id in prescribed.keys():
            if pos_id == prescribed[cast_id]:
                fout.write('presc: ' + var + ' = 1\n')
            else:
                fout.write('presc: ' + var + ' = 0\n')
        
    fout.write('binary\n' + ' '.join(vars))

def make_excluded(db):
    c = db.cursor()
    c.execute("""
select id from casteller where nickname in ('Abdul', 'AE', 'Aina', 'Alaitz', 'Aleix', 'Alvarito', 'Arnau', 'Berta', 'Eva', 'Joana', 'Joanet', 'Laia O', 'Lali', 'Marco', 'Martina', 'Montxi', 'Oriolet', 'Rafols', 'Rai', 'Santako', 'Stefano');
""")
    ans = []
    for row in c.fetchall():
        ans.append(int(row[0]))
    return ans

def make_segons(db):
    c = db.cursor()
    c.execute("""
select id from casteller where nickname in ('Abdul', 'Arnau', 'Quim');
""")
    ans = []
    for row in c.fetchall():
        ans.append(int(row[0]))
    print ans
    return ans

def complete_lp():
    db = get_db()
    excluded = make_excluded(db)
    prescribed = dict([(2, 79), (14, 80), (72, 81)]) # Abdul, Arnau, Quim as segons
    [castell_id_name, colla_id_name] = ['cvg.3de9f', 'cvg']
    complete_lp_impl(prescribed, excluded, castell_id_name, colla_id_name)

if __name__=="__main__":
    complete_lp()
