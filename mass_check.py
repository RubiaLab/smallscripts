#!/usr/bin/python
__author__ = 'RubiaLab'
__email__ = 'rubialab@rubialab.de'
__version__ = '1.0'

def main():
	from molmass import Formula, ELEMENTS

	# Constants (in u)
	ELECTRON_MASS = 0.000548579909
	PROTON_MASS = ELEMENTS['H'].mass - ELECTRON_MASS
	NAplus_MASS = ELEMENTS['Na'].mass - ELECTRON_MASS
	Kplus_MASS = ELEMENTS['K'].mass - ELECTRON_MASS

	# MS-Modes
	MODES = {
		"1": ("EI",     "M+•"),
		"2": ("ESI+",   "[M+H]+"),
		"3": ("ESI-",   "[M-H]-"),
		"4": ("ESI+Na", "[M+Na]+"),
		"5": ("ESI+K",  "[M+K]+"),
	}

	# Calculate theoretical m/z
	def theoretical_mz(formula: str, mode: str) -> float:
		f = Formula(formula)
		m = f.isotope.mass

		if mode == "EI":
			return m - ELECTRON_MASS
		elif mode == "ESI+":
			return m + PROTON_MASS
		elif mode == "ESI-":
			return m - PROTON_MASS
		elif mode == "ESI+Na":
			return m + NAplus_MASS
		elif mode == "ESI+K":
			return m + Kplus_MASS

	# Calculate ppm deviation
	def ppm_error(measured_mz: float, theoretical_mz: float) -> float:
		return (measured_mz - theoretical_mz) / theoretical_mz * 1e6

	try:
		# Molecular formula
		formula = input("Molecular formula (e.g. C8H10N4O2): ").strip()
		Formula(formula)

		# Mode selection
		print("\nSelect ionization type:")
		for key, (mode, desc) in MODES.items():
			print(f"  [{key}] {mode:6s}  {desc}")

		choice = input("Selection [1..5]: ").strip()
		if choice not in MODES:
			raise ValueError("Invalid selection")

		mode = MODES[choice][0]

		# Measured m/z
		measured_mz = float(input("Measured m/z: ").strip())

		# Calculation
		theo = theoretical_mz(formula, mode)
		ppm = ppm_error(measured_mz, theo)

		# Output
		print("\n--- Result ---")
		print(f"Molecular formula: {formula}")
		print(f"Ionization type:   {mode}")
		print(f"Theoretical m/z:   {theo:.4f}")
		print(f"Measured m/z:      {round(measured_mz, 4)}")
		print(f"ppm deviation:     {round(ppm, 1)} ppm")

	except ValueError as e:
		print(f"Input error: {e}")

	except Exception as e:
		print(f"Unexpected error: {e}")

if __name__ == '__main__':
	main()
