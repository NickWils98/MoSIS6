#!/bin/sh
echo run task5
python3.8 ./model/task5.py
echo run task6_seed42
python3.8 ./model/task6_seed42.py
echo run task6_seed69
python3.8 ./model/task6_seed69.py
echo run task7_seed42_prob
python3.8 ./model/task7_seed42_prob.py
echo run task7_seed69_prob
python3.8 ./model/task7_seed69_prob.py
echo run task7_seed42_lock
python3.8 ./model/task7_seed42_lock.py
echo run task7_seed69_lock
python3.8 ./model/task7_seed69_lock.py
echo run task8
python3.8 ./model/task8.py