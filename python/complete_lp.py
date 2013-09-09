from local_config import RootDir, pinya_dir, text_splitter, numeric_splitter
import sys 
sys.path.append(RootDir + 'python/util/')
from db_interaction import get_db
from solve_ip import split_var

def complete_lp_impl(prescribed, excluded, castell_id_name, colla_id_name):
    filename = RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya'
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
        elif cast_id in prescribed.keys():
            if pos_id == prescribed[cast_id]:
                fout.write('presc: ' + var + ' = 1\n')
            else:
                fout.write('presc: ' + var + ' = 0\n')
        
    fout.write('binary\n' + ' '.join(vars))

def make_excluded(db):
    c = db.cursor()
    c.execute("""
select id from casteller where nickname in ('AE', 'Aina', 'Alaitz', 'Aleix', 'Alvarito', 'Berta', 'Eva', 'Joana', 'Joanet', 'Laia O', 'Lali', 'Marco', 'Martina', 'Montxi', 'Oriolet', 'Rafols', 'Rai', 'Santako', 'Stefano');
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
    print prescribed
    print excluded 
    [castell_id_name, colla_id_name] = ['cvg.3de9f', 'cvg']
    complete_lp_impl(prescribed, excluded, castell_id_name, colla_id_name)

if __name__=="__main__":
    complete_lp()
