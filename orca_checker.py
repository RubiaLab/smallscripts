#!/usr/bin/python
__author__ = 'RubiaLab'
__email__ = 'rubialab@rubialab.de'
__version__ = '1.0'

def main():
    import sys
    import os

    for filename in sys.argv[1:]:
        if not os.path.isfile(filename):
            print(f'Specified file {filename} does not exist. Moving to next file...')
            continue

        print(f'Checking calculation output "{filename}" for completeness...')
        with open(filename, 'r') as output:
            calc_output = output.readlines()

        normal_termination = any('****ORCA TERMINATED NORMALLY****' in line for line in calc_output)

        if normal_termination:
            print(f'Calculation in file {filename} terminated normally. Nothing to do.')
            continue

        print(f'Calculation in file {filename} did not terminate normally. Removing last unfinished geometry optimization cycle...')

        cycle_start_indices = [i for i, line in enumerate(calc_output) if 'GEOMETRY OPTIMIZATION CYCLE' in line]

        if not cycle_start_indices:
            print(f'No geometry optimization cycles found in {filename}. Skipping.')
            continue

        last_cycle_index = cycle_start_indices[-1]
        trim_index = max(0, last_cycle_index - 2)

        cleaned_output = calc_output[:trim_index]
       
        with open(filename, 'w') as output:
            output.writelines(cleaned_output)

        print(f'Removed lines from last incomplete cycle in file {filename}.')

if __name__ == '__main__':
	main()
