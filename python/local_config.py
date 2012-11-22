RootDir = '/home/julian/Documents/pinyer/'

# The following variable determines whether or not to invoke the solver.
# If set to False, the solution is read from the solution file,
# which is supposed to exist.
DoSolve = True

# Assuming DoSolve == True,
# the following variable determines whether or not to use the open source
# IP solver CBC. If set to False, the commercial solver Gurobi is used instead.
UseCBC = False

# If Gurobi is used, you must enter the correct path to gurobipy here
if not UseCBC:
    import sys
    sys.path.append('/opt/gurobi500/linux32/lib/python2.7')
    sys.path.append('/opt/gurobi500/linux64/lib/python2.7')

# internal constants
numeric_splitter = '_'
text_splitter = '~'
field_splitter = '|'

# roles
pos_types = ('crossa', 'baix', 'contrafort', 'vent', 'ma', 'agulla', 'portacrossa', 'pinya', 'lateral', 'segon')


# Print log information?
DoLogging = False

# Print debug information?
Debug = False

# Data defining the relations between positions 

# the tolerance in height between successive mans, vents, and pinya,
# and in width between adjacent pinya in the same ring
tolerances = dict([('height_target', 3), \
                       ('min_height_tol', 2), \
                       ('max_height_tol', 2), \
                       ('ma_baix_segon_tol', 50), \
                       ('vent_baix_segon_tol', 50), \
                       ('baix_segon_tol', 2), \
                       ('baix_agulla_tol', 5), \
                       ('baix_contrafort_tol', 5), \
                       ('lateral_segon_tol', 50), \
                       ('width_target', 0), \
                       ('min_width_tol', 0), \
                       ('max_width_tol', 10), \
                       ('delta_height_c_b', 5), \
                       ('delta_height_c_b_tol', 5) \
                       ])

# the directories used for pinya xml and svg files
pinya_dir = 'pinyas/'


# how to draw a casteller figure
floor_level = -60

# draw the figure? if False, a rectangle is drawn
drawSketch = True

# how much is the relation curve curved? 0 = nothing, positive = more curved
RelationCurvature = .2

# Underlay the names of the castellers in white? May take extra time to render
PinyaWhiteUnderlay = False

# Underlay the text of the relations in white? May take extra time to render
RelationsWhiteUnderlay = True
