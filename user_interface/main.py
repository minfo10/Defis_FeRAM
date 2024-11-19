##################
# MAIN PROGRAMME #
##################

from Interface import Interface

test_instance = 'Test Mode'  # or any object/instance that AppWindow can handle

# Directly launch the measurement interface
main = Interface()
main.mainloop()