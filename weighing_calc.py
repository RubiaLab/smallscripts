# Program for calculating the weighing of solids or dilution of solutions
from molmass import Formula

def calc_molar_solution():
	print('\n[1] x-molar solution from solid')
	print('Chemical formula of substance:')
	sumformula = Formula(input())
	print('Molarity of the solution in mol/L:')
	molarity = float(input())
	print('Volume of the solution in mL:')
	vol = float(input())

	weighing = round((sumformula.mass * molarity) * (vol / 1000), 4)

	print(f"{'Molar mass of':<25} {sumformula}: {round(sumformula.mass, 4)} g/mol")
	print(f"{'Molarity:':<25} {molarity} mol/L")
	print(f"{'Solution volume:':<25} {vol} mL")
	print(f"{'Required weighing:':<25} {weighing} g")

def calc_percent_solution():
	print('\n[2] x%-solution from solid')
	print('Chemical formula of substance:')
	sumformula = Formula(input())
	print('Mass fraction in %:')
	target_conc = float(input())
	print('Density of the target solution:')
	density = float(input())
	print('Solution volume in mL:')
	target_vol = float(input())

	conc = ((density * 1000) * (target_conc / 100)) / sumformula.mass
	weighing = round((conc * (target_vol / 1000) * sumformula.mass), 4)

	print(f"{'Substance concentration:':<25} {round(conc, 2)} mol/L")
	print(f"{'Required weighing:':<25} {weighing} g of {sumformula}")

def calc_dilution():
	print('\n[3] Solution by dilution (mixing cross)')
	print('Select unit:\n'
		'[1] %\n'
		'[2] mol/L\n')
	unit = int(input())
	print_unit = '%' if unit == 1 else 'mol/L'

	print(f'Concentration of solution 1 in {print_unit}:')
	conc_1 = float(input())
	print(f'Concentration of solution 2 in {print_unit}:')
	conc_2 = float(input())
	print(f'Target concentration in {print_unit}:')
	target_conc = float(input())
	print('Solution volume in mL:')
	target_vol = float(input())

	part_1 = abs(conc_2 - target_conc)
	part_2 = abs(conc_1 - target_conc)
	vol_1 = round((part_1 / (part_1 + part_2)) * target_vol, 2)
	vol_2 = round((part_2 / (part_1 + part_2)) * target_vol, 2)

	print(f"{'Concentration solution 1:':<30} {conc_1} {print_unit}")
	print(f"{'Concentration solution 2:':<30} {conc_2} {print_unit}")
	print(f"{'Target concentration:':<30} {target_conc} {print_unit}")
	print(f"{'Total solution volume:':<30} {target_vol} mL")
	print(f"{'Volume solution 1:':<30} {vol_1} mL")
	print(f"{'Volume solution 2:':<30} {vol_2} mL")

def calc_molar_from_percent():
	print('\n[4] x-molar solution from x%-solution')
	print('Empirical formula of substance:')
	sumformula = Formula(input())
	print('Mass fraction in %:')
	mass_fraction = float(input())
	print('Density of the stock solution:')
	density = float(input())
	print('Target molarity:')
	target_molarity = float(input())
	print('Solution volume in mL:')
	vol = float(input())

	mass = (density * 1000) * (mass_fraction / 100)
	molarity = mass / sumformula.mass
	print(f'{sumformula} with a mass fraction of {mass_fraction}% has a concentration of {round(molarity, 2)} mol/L.')
	target_vol = round((target_molarity * vol) / molarity, 2)
	add_vol = round(vol - target_vol, 2)

	print(f'Measure {target_vol} mL of the {mass_fraction}% solution and dilute with {add_vol} mL water.')

calculation_methods = {
	1: calc_molar_solution,
	2: calc_percent_solution,
	3: calc_dilution,
	4: calc_molar_from_percent
}

print('Select calculation:\n'
	'[1] x-molar solution from solid (e.g., 1M NaOH)\n'
	'[2] x%-solution from solid (e.g., 10% NaOH)\n'
	'[3] Solution by dilution (mixing cross)\n'
	'[4] x-molar solution from x%-solution\n')

while True:
	try:
		calctype = int(input())
		if calctype in calculation_methods:
			calculation_methods[calctype]()
			break
		else:
			print('Please enter a valid option (1-4).')
	except ValueError:
		print('Invalid input. Please enter a number between 1 and 4.')
