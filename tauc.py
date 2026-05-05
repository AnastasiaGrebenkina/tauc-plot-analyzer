import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_NAME = 'data.xlsx'
energy_min = 2.0
energy_max = 4.5
delta = 0.1

def tauc_plots(filename):

    df = pd.read_excel(filename)
    df = df.apply(pd.to_numeric, errors='coerce').dropna() #drop str, NaN
    
    wavelength = df.iloc[:, 0].values
    abs_data = df.iloc[:, 1].values   
    
    energy = 1240 / wavelength
    reflectance = 10**(-abs_data)
    # Kubelka-Munk function
    fr = ((1 - reflectance)**2) / (2 * reflectance + 1e-9) #avoid division by zero
    
    idx = np.argsort(energy)
    energy, fr = energy[idx], fr[idx]

    transitions = {
        0.5: "Direct Allowed (1/2)",
        2.0: "Indirect Allowed (2)",
        1.5: "Direct Forbidden (3/2)",
        3.0: "Indirect Forbidden (3)"
    }

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for i, (r, label) in enumerate(transitions.items()):
        # tauc
        y_axis = (fr * energy)**(1/r)

        mask_search = (energy > energy_min) & (energy < energy_max)
        if not np.any(mask_search): continue

        #find the steepest part in the ROI
        
        dy = np.diff(y_axis) / np.diff(energy)
        dy_smooth = np.convolve(dy, np.ones(5)/5, mode='same')
        
        idx_max_slope = np.argmax(dy_smooth[mask_search[:-1]]) 
        actual_idx = np.where(mask_search)[0][idx_max_slope]
        
        # fit the line in a small window (+- delta)
        fit_window = (energy > energy[actual_idx] - delta) & (energy < energy[actual_idx] + delta)
        
        m, b = np.polyfit(energy[fit_window], y_axis[fit_window], 1)
        eg = -b / m
        
        # draw
        ax = axes[i]
        ax.plot(energy, y_axis, color='black', lw=1.5, label='Data')
        x_extrap = np.linspace(eg, energy[actual_idx] + 0.5, 100)
        y_tangent = m * x_extrap + b
        ax.plot(x_extrap, y_tangent, 'r--', lw=3, label=f'Eg = {eg:.3f} eV')
        
        ax.axhline(0, color='black', lw=1)
        ax.set_title(label, fontsize=12, fontweight='bold')
        ax.set_xlabel('Energy (eV)')
        ax.set_ylabel('Tauc Value')
 
        ax.set_xlim(energy.min(), energy.max())
        limit_idx = int(len(energy) * 0.95)
        y_max_auto = np.max(y_axis[:limit_idx])
        ax.set_ylim(-y_max_auto * 0.05, y_max_auto * 1.1)
        
        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


if __name__ == "__main__":
    tauc_plots(FILE_NAME)