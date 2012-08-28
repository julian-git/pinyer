def get_solutions(filename):
    model=read(filename)
    model.optimize()
    if model.status == 2:
        sv = model.getVars()
        sol = dict()
        for v in sv:
            sol[v.var_name] = v.x
        return sol
    else:
        return False

if __name__ == "__main__":
    import sys
    sys.path.append('/opt/gurobi500/linux32/lib/python2.7')
    from gurobipy import *
    s = get_solutions("tests/test.lp")
    print s
