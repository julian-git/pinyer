def get_solutions(filename):
    import sys
    sys.path.append('/opt/gurobi500/linux32/lib/python2.7')
    sys.path.append('/opt/gurobi500/linux64/lib/python2.7')
    from gurobipy import read

    model=read(filename)
    model.optimize()
    if model.status == 2:
        sv = model.getVars()
        sol = []
        for v in sv:
            if v.x == 1:
                sol.append(v.var_name)
        return sol
    else:
        return False

if __name__ == "__main__":
    import sys
    sys.path.append('/opt/gurobi500/linux32/lib/python2.7')
    sys.path.append('/opt/gurobi500/linux64/lib/python2.7')
    from gurobipy import *
    s = get_solutions("tests/test.lp")
    print s
