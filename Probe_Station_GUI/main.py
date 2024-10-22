##################
# MAIN PROGRAMME #
##################

import defaultInterface

test_instance = 'Test Mode'  # or any object/instance that AppWindow can handle

# Directly launch the measurement interface
main = defaultInterface.AppWindow(inst=test_instance)
main.mainloop()