##################
# MAIN PROGRAMME #
##################

import Probe_Station_GUI.Interface as Interface

test_instance = 'Test Mode'  # or any object/instance that AppWindow can handle

# Directly launch the measurement interface
main = Interface.AppWindow(inst=test_instance)
main.mainloop()