# DEVS
- run.sh: a script that will run all the expiriments for task 5 up until task 8
- Images used in the report and the true travel time excel file can be found in the resources folder
- The model map contains:
  - experiment.py: Setup the system, run and gather information for output
  - model.py: Contains our CoupledDEVS model which connects all the atomic devs
  - task5.py: Set up the system and run for task 5
  - task6_seed42.py: Set up the system and run for task 6 with seed 42
  - task6_seed69.py: Set up the system and run for task 6 with seed 69
  - task7_seed42_lock.py: Set up the system and run for task 7 with lock changed (seed 42)
  - task7_seed42_prob.py: Set up the system and run for task 7 with probability changed (seed 42)
  - task7_seed69_lock.py: Set up the system and run for task 7 with lock changed (seed 69)
  - task7_seed69_prob.py: Set up the system and run for task 7 with probability changed (seed 69)
  - atomic_devs: This folder holds all our atomic devs python implementations
  - messages_events: This folder holds all the message and event python files used in our model
  - plots: This folder contains all the plots which are generated
