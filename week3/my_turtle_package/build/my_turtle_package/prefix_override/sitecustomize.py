import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/esha/Mr-lab _eshamajad/week3/my_turtle_package/install/my_turtle_package'
