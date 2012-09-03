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
    f = f + "\nend"
    return f

def write_lp_file(castellers_in_position, position_data, participation, filename='pinya.lp'):
    f = open(filename, 'w')
    obj_val = dict()          # The objective coefficient of each variable
    ineqs = []                # the linear inequalities
    ip_ineqs(castellers_in_position, position_data, obj_val, ineqs, participation)
    f.write(make_lp_file(obj_val, ineqs))
    f.close()

def sol_from_v(sol, vname, castellers_in_position):
     cast_id = vname[1:vname.find('p')]
     pos_id = long(vname[vname.find('p')+1:])
     for casteller in castellers_in_position[pos_id]:
         if casteller['id'] == int(cast_id):
             sol[int(pos_id)] = casteller['name']


def solve_lp_with_gurobi(filename, castellers_in_position):
    import sys
    sys.path.append('/opt/gurobi500/linux32/lib/python2.7')
    sys.path.append('/opt/gurobi500/linux64/lib/python2.7')
    from gurobipy import read

    model=read(filename)
    model.optimize()
    if model.status == 2:
        sv = model.getVars()
        sol = dict()
        for v in sv:
            if v.x == 1:
                sol_from_v(sol, v.varname, castellers_in_position)
        return sol
    else:
        return False


def solve_lp_with_cbc(filename, castellers_in_position):
    import subprocess
    subprocess.call(["cbc", '-import', filename, '-solve', '-solu', 'solution.txt', '-quit'])
    f = open("solution.txt", 'r')
    sol = dict()
    first_line = True
    for line in f:
        if first_line:
            first_line = False
        else:
            a = line.split()
            if a[2] == '1':
                sol_from_v(sol, a[1], castellers_in_position)
    return sol


def find_pinya(participation, position_data=dict(), filename='pinya.lp'):
    castellers_in_position = dict()
    write_lp_file(castellers_in_position, position_data, participation, filename)
    return solve_lp_with_cbc(filename, castellers_in_position)
    
def solution_as_svg(participation):
    from string import Template
    svg_rect = Template("""
<g id="${_svg_id}" transform="translate(${_x} ${_y})">
  <rect width="${_w}" height="${_h}" x="-60" y="-20" fill="lightblue"/>
  <text text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
</g>
""")
    svg_circle = Template("""
<g id="${_svg_id}" transform="translate(${_x} ${_y})">
  <circle x="-60" y="-20" r="${_rx}" fill="lightblue"/>
  <text text-anchor="middle" dominant-baseline="mathematical">${_name}</text>
</g>
""")
    position_data = dict()
    solution = find_pinya(participation, position_data)
    svg = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Pinyol</title>
</head>
<body>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
viewBox="0 0 200 200"> 
"""
    for pos, name in solution.iteritems():
        pd = position_data[pos]
        if pd['svg_elem'] == 'rect':
            svg = svg + svg_rect.substitute(_svg_id=pd['svg_id'], _name=name, _x=pd['x'], _y=pd['y'], _w=pd['w'], _h=pd['h'])
        elif pd['svg_elem'] == 'circle':
            svg = svg + svg_circle.substitute(_svg_id=pd['svg_id'], _name=name, _x=pd['x'], _y=pd['y'], _rx=pd['rx'])
    return svg + "</svg>" + "</html>"

if __name__ == "__main__":
    participation = dict([(9, 0), (17, 5)])
    f = open("index.html", 'w')
    f.write(solution_as_svg(participation))
