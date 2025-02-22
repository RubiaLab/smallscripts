#!/usr/bin/python
__author__ = 'RubiaLab'
__email__ = 'rubialab@rubialab.de'
__version__ = '1.0'

def main():
	import sys
	import os
	import matplotlib.pyplot as plt

	scan_coordinates = []
	energies = []
	all_scan_coordinates = []
	all_energies = []
	min_energy = []

	plt.rcParams["savefig.dpi"] = 300
	font = {'size' : 16,
		'family': 'Arial',
		'weight': 'medium'}
	plt.rc('font', **font)

	# Check for sufficient arguments
	if len(sys.argv) < 2:
		print("Please provide at least one argument.")
		sys.exit()

	# loop over all files
	for i in range(1, len(sys.argv)):
		filename = sys.argv[i]
		if not os.path.isfile(filename):
			print("File {} does not exist. Exiting program...".format(filename))
			sys.exit()

		myfile = open(filename, 'rt')
		calc_output = myfile.readlines()
		myfile.close()

		# check for scanning coordinate
		for scan_start in range(0, len(calc_output)):
			if (calc_output[scan_start].find("Scan") >= 0):
				scan_line = calc_output[scan_start].strip().split()
				scan_keyword = scan_line[1]
				break
		print('scan_line', scan_line)
		print('scan_keyword', scan_keyword)

		# define start and end point for summary file
		for start in range(0, len(calc_output)):
			if (calc_output[start].find("Summary of Optimized Potential Surface Scan") >= 0):
				break

		for end in range(start, len(calc_output)):
			if (calc_output[end].find("Stoichiometry") >= 0):
				break

		# extract scan coordinates (x values) from result
		for current_line in range(start, end):
			if calc_output[current_line].find(str(scan_keyword)) >= 0:
				line_coordinates = calc_output[current_line].strip().split()
				for i in range(1, len(line_coordinates)):
					scan_coordinates.append(float(line_coordinates[i]))
		all_scan_coordinates.append(scan_coordinates)
		print('\nScan Coordinates:', scan_coordinates)

		for energy_countline in range(0, len(calc_output)):
			if (calc_output[energy_countline].find("-- Stationary point found.") >= 0):
				for scf_line in range(energy_countline, 0, -1):
					if (calc_output[scf_line].find("SCF Done:") >= 0):
						energyline = calc_output[scf_line].strip().split()
						energies.append(float(energyline[4]))
						break
		all_energies.append(energies)
		print('\nEnergies:', energies)

		# Write output file
		f_out = open(filename.replace(".out", "") + "_coord_scan.txt", 'w')
		f_out.write("ScanParameter " + scan_line[1] + " " + scan_line[2] + "\n")

		# Find the minimum energy value and use it as zero_level
		min_energy.append(min(map(float, energies)))
		max_energy = max(map(float, energies))
		zero_level = min_energy[i-1]

		print("Minimal Energy: ", min_energy[i-1])
		print("Maximum Energy: ", max_energy)

		for j in range(0, len(scan_coordinates)):
			f_out.write(str(scan_coordinates[j]) + ", " + str(float(energies[j]) - zero_level) + "\n")
		f_out.close()

		# empty file-specific lists
		scan_coordinates = []
		energies = []

# x-offset einbauen für mehrere files
	print("Generate plot? [y/n]")
	plot_start = input()

	if plot_start == "y":
		import matplotlib.pyplot as plt
		
		print("Enter plot title:")
		title = input()

		# x values absolute oder relative to reference geometry
		x_absolute = input("Show x values absolute (unchanged) or relative to optimized geometry? (abs/rel): ").lower()
		if x_absolute == 'rel':
			x_reference = []
			for k in range(len(all_scan_coordinates)):
				print(all_scan_coordinates[k])
				x_reference.append(float(input("Enter reference angle (0°) for {}: ".format(filename))))
				for l in range(len(all_scan_coordinates[k])):
					all_scan_coordinates[k][l] = all_scan_coordinates[k][l] + abs(x_reference[k])
				xlabel = "Rotation around Dihedral Angle (°)"
		else:
			xlabel = "Dihedral Angle (°)"

		# Modify x-range for this dataset (optional)
		plot_x_range = input("Would you like to set the x-range for data {} individually? (yes/no): ".format(filename))
		if plot_x_range.lower() == 'yes':
			start_x = []
			end_x = []
			for m in range(len(all_scan_coordinates)):
				print("Current x-range for data {}: [{}, {}]".format(filename, min(all_scan_coordinates[m]), max(all_scan_coordinates[m])))
				start_x.append(float(input("Enter the start value for the x-range of {}: ".format(filename))))
				end_x.append(float(input("Enter the final value for the x-range of {}: ".format(filename))))
				all_scan_coordinates[m], all_energies[m] = [list(t) for t in zip(*[(x, y) for x, y in zip(all_scan_coordinates[m], all_energies[m]) if start_x[m] <= x <= end_x[m]])]

		print("Energy in:\n"
			"[1] Hartree absolute\n"
			"[2] Hartree relative\n"
			"[3] kcal/mol relative\n"
			"[4] kJ/mol relative\n")
		unit = int(input())
		if unit == 1:
			conversion_factor = 1
			ylabel = "Energy (Hartree)"
		elif unit == 2:
			conversion_factor = 1
			ylabel = "Relative Energy (Hartree)"
		elif unit == 3:
			conversion_factor = 627.5096
			ylabel = "Relative Energy (kcal/mol)"
		elif unit == 4:
			conversion_factor = 2625.5002
			ylabel = "Relative Energy (kJ/mol)"

		for k in range(len(all_energies)):
			for l in range(len(all_energies[k])):
				all_energies[k][l] = all_energies[k][l] - min_energy[k]
				all_energies[k][l] = all_energies[k][l] * conversion_factor

		fig, ax = plt.subplots(figsize=(8,6))
		for l in range(len(all_scan_coordinates)):
			ax.plot(all_scan_coordinates[l], all_energies[l], '-D', markersize=3, linewidth=1, color='C{}'.format(l))
		
		plt.title(title)
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.xaxis.get_ticklocs(minor=True)
		ax.yaxis.get_ticklocs(minor=True)
		ax.minorticks_on()
		#plt.savefig(title + ".pdf", format="pdf", dpi=300)
		plt.show()
	else:
		sys.exit()

if __name__ == '__main__':
	main()