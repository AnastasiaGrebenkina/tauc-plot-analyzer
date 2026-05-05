# tauc-plot-analyzer
This tool automates the calculation of the optical band gap (Eg) from UV-Vis absorption spectra using the Tauc plot method.

The script expects an Excel file named data.xlsx in the root directory.
Column A: Wavelength in nm
Column B: Absorbance (А) in arbitrary units.

The script automatically converts Absorbance to Reflectance and then applies the Kubelka-Munk function before plotting.

Run:
1. Clone the repository
2. Install packages: 'pip install pandas numpy matplotlib openpyxl'
3. Replace the data in data.xlsx with your data.
4. Execute 'python tauc.py'
