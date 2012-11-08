RootDir = '/home/julian/Documents/pinyer/'

# The following variable determines whether or not to invoke the solver.
# If set to False, the solution is read from the file lp_solution_filename
# (see below), which is supposed to exist.
DoSolve = True

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
pos_types = ('crossa', 'baix', 'contrafort', 'vent', 'ma', 'agulla', 'portacrossa', 'pinya', 'lateral', 'segon')


# Print log information?
DoLogging = False

# Data defining the relations between positions 

# the tolerance in height between successive mans, vents, and pinya,
# and in width between adjacent pinya in the same ring
tolerances = dict([('height_target', 3), \
                       ('min_height_tol', 2), \
                       ('max_height_tol', 2), \
                       ('ma_baix_segon_tol', 50), \
                       ('baix_segon_tol', 2), \
                       ('baix_agulla_tol', 5), \
                       ('baix_contrafort_tol', 5), \
                       ('lateral_segon_tol', 10), \
                       ('width_target', 0), \
                       ('min_width_tol', 0), \
                       ('max_width_tol', 10), \
                       ('delta_height_c_b', 5), \
                       ('delta_height_c_b_tol', 5) \
                       ])

# the directories used for pinya xml and svg files
pinya_dir = 'pinyas/'
