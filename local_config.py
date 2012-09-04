# The following variable determines whether or not to use the open source
# IP solver CBC. If set to False, the commercial solver Gurobi is used instead.
UseCBC = True

# If Gurobi is used, you must enter the correct path to gurobipy here
if not UseCBC:
    import sys
    sys.path.append('/opt/gurobi500/linux32/lib/python2.7')
    sys.path.append('/opt/gurobi500/linux64/lib/python2.7')
