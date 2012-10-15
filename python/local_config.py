# The following variable determines whether or not to invoke the solver.
# If set to False, the solution is read from the file lp_solution_filename
# (see below), which is supposed to exist.
DoSolve = False

# The following variable determines whether or not to use the open source
# IP solver CBC. If set to False, the commercial solver Gurobi is used instead.
UseCBC = False

# If Gurobi is used, you must enter the correct path to gurobipy here
if not UseCBC:
    import sys
    sys.path.append('/opt/gurobi500/linux32/lib/python2.7')
    sys.path.append('/opt/gurobi500/linux64/lib/python2.7')

# The files used for optimization
lp_problem_filename = '/tmp/pinya.lp'
lp_solution_filename = '/tmp/solution.sol'
lp_log_filename = '/tmp/lp_log.txt'

# internal constants
numeric_splitter = '_'
text_splitter = '~'

# roles
pos_types = ('crossa', 'baix', 'contrafort', 'vent', 'ma', 'agulla', 'portacrosses', 'pinya')


# Print log information?
DoLogging = True

# Data defining the relations between positions 

# the tolerance in height between successive mans, vents, and pinya,
# and in width between adjacent pinya in the same ring
tolerances = dict([('height', 5), \
                       ('width', 6), \
                       ('delta_height_c_b', 5), \
                       ('delta_height_c_b_tol', 5) \
                       ])

# the directories used for pinya xml and svg files
pinya_dir = 'pinyas/'
