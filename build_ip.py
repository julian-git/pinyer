from ineqs import * 

def make_lp_file(obj_val, ineqs):
    f = "maximize\n"
    variables = sorted(obj_val.keys())
    for v in variables:
        f = f + str(obj_val[v]) + " " + str(v) + " + "
    f = f[:-3] + "\nsubject to\n"
    for ineq in ineqs:
        f = f + ineq + "\n"
    f = f + "binary\n"
    for v in variables:
        f = f + v + " "
    return f

def write_lp_file(castellers_in_position, position_data, participation, filename='pinya.lp'):
    f = open(filename, 'w')
    obj_val = dict()          # The objective coefficient of each variable
    ineqs = []                # the linear inequalities
    ip_ineqs(castellers_in_position, position_data, obj_val, ineqs, participation)
    f.write(make_lp_file(obj_val, ineqs))
    f.close()

def find_pinya(participation, position_data=dict(), filename='pinya.lp'):
    import sys
    sys.path.append('/opt/gurobi500/linux32/lib/python2.7')
    from gurobipy import read

    castellers_in_position = dict()
    write_lp_file(castellers_in_position, position_data, participation, filename)

    model=read(filename)
    model.optimize()
    if model.status == 2:
        sv = model.getVars()
        sol = dict()
        for v in sv:
            if v.x == 1:
                vname = v.var_name
                cast_id = vname[1:vname.find('p')]
                pos_id = long(vname[vname.find('p')+1:])
                for casteller in castellers_in_position[pos_id]:
                    if casteller['id'] == int(cast_id):
                        sol[int(pos_id)] = casteller['name']
        return sol
    else:
        return False
    
def solution_as_svg(participation):
    from string import Template
    svg_t = Template("""
 <svg>
   <g transform="translate(${_x} ${_y})">
     <rect width="120" height="40" x="-60" y="-20" fill="lightblue"/>
     <text text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
   </g>
 </svg>
""")
    position_data = dict()
    solution = find_pinya(participation, position_data)
    svg = ''
    for pos, name in solution.iteritems():
        svg = svg + svg_t.substitute(_name=name, _x=position_data[pos]['x'], _y=position_data[pos]['y'])
    return svg

if __name__ == "__main__":
    participation = dict([(9, 0), (17, 5)])
    print solution_as_svg(participation)
