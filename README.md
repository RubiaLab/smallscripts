# Small scripts for daily use in science
## weighing_calc.py
This Python program calculates the weight of a solid for the preparation of solutions (molarity or mass percentage) as well as dilution of solution by mixing cross, and conversion from molarity to mass percentage.
Execute the script as follows:

```python
python3 weighing_calc.py
```

> [!NOTE]
>
> This program requires the package molmass which can be installed using pip:
>
> ```bash
> pip install molmass
> ```

## coordinate_scan_plotter.py
This Python program is designed for plotting coordinate scans calculated with the Gaussian quantum chemical calculation program.
Execute the script as follows, where ```gaussian1.out``` and ```gaussian2.out``` are Gaussian calculation outputs:

```python
python3 coordinate_scan_plotter.py gaussian1.out gaussian2.out [further arguments]
```

> [!NOTE]
>
> This program requires the package matplotlib which can be installed using pip:
>
> ```bash
> pip install matplotlib
>``

## Contact

Alexander Krappe – rubialab@rubialab.de

Project link – [https://github.com/RubiaLab/smallscripts](https://github.com/RubiaLab/smallscripts)

## License

Distributed under the MIT License. See ```LICENSE.txt``` for more information.
