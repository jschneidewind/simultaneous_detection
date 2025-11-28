import pprint as pp
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 12
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

from pyKES.database.database_experiments import ExperimentalDataset


def main():
    dataset = ExperimentalDataset.load_from_hdf5('data/251130_processed_O2_H2_data_with_fits.h5')

    fig, ax = plt.subplots(2, 1, figsize=(7, 7))
    fig.tight_layout(pad=2.0)
    fig.subplots_adjust(left = 0.12, right = 0.55, hspace = 0.4)

    O2_gas_experimental = dataset.experiments['NB-312'].processed_data['[O2-g]_experimental']
    O2_gas_fit = dataset.experiments['NB-312'].processed_data['[O2-g]_fit']

    H2_gas_experimental = dataset.experiments['NB-312'].processed_data['[H2-g]_experimental']
    H2_gas_fit = dataset.experiments['NB-312'].processed_data['[H2-g]_fit']

    O2_aq_experimental = dataset.experiments['NB-353'].processed_data['[O2-aq]_experimental']
    O2_aq_fit = dataset.experiments['NB-353'].processed_data['[O2-aq]_fit']

    H2_aq_experimental = dataset.experiments['NB-353'].processed_data['[H2-aq]_experimental']
    H2_aq_fit = dataset.experiments['NB-353'].processed_data['[H2-aq]_fit']

    ax[0].plot(H2_aq_experimental['x'], H2_aq_experimental['y'],
        '.', color = 'gray', label = 'Data H$_2$')

    ax[0].plot(H2_aq_fit['x'], H2_aq_fit['y'],
        '-', color = 'orange', label = 'Model H$_2$')

    ax[0].plot(O2_aq_experimental['x'], O2_aq_experimental['y'],
        '.', color = 'black', label = 'Data O$_2$')

    ax[0].plot(O2_aq_fit['x'], O2_aq_fit['y'],
        '-', color = 'red', label = 'Model O$_2$')

    # Create second y-axis for H2/O2 ratio (liquid phase)
    ax0_twin = ax[0].twinx()

    start_idx = 20
    ratio_aq_experimental = H2_aq_experimental['y'][start_idx:] / O2_aq_experimental['y'][start_idx:]
    ratio_aq_fit = H2_aq_fit['y'][start_idx:] / O2_aq_fit['y'][start_idx:]
      # Skip initial points to avoid large ratios in initial phase
    
    ax0_twin.plot(H2_aq_experimental['x'][start_idx:], ratio_aq_experimental,
        '.', color = 'green', markersize=2, alpha=0.4, label = 'Ratio H$_2$/O$_2$ (Data)')
    
    ax0_twin.plot(H2_aq_fit['x'][start_idx:], ratio_aq_fit,
        '-', color = 'darkgreen', linewidth = 2, label = 'Ratio H$_2$/O$_2$ (Model)')
    
    ax0_twin.set_ylabel('H$_2$/O$_2$ Ratio', color='darkgreen')
    ax0_twin.tick_params(axis='y', labelcolor='darkgreen')

    # Combine legends from both axes
    lines_0, labels_0 = ax[0].get_legend_handles_labels()
    lines_0_twin, labels_0_twin = ax0_twin.get_legend_handles_labels()
    ax[0].legend(lines_0 + lines_0_twin, labels_0 + labels_0_twin, 
                 loc='center left', bbox_to_anchor=(1.25, 0.66))
    
    ax[0].set_title('Liquid phase', fontweight='bold')
    ax[0].set_xlabel('Time / s')
    ax[0].set_ylabel('Concentration / μmol·L$^{-1}$')

    ax[1].plot(H2_gas_experimental['x'], H2_gas_experimental['y'],
        '.', color = 'gray', label = 'Data H$_2$')
    ax[1].plot(H2_gas_fit['x'], H2_gas_fit['y'],
        '-', color = 'orange', label = 'Model H$_2$')

    ax[1].plot(O2_gas_experimental['x'], O2_gas_experimental['y'],
        '.', color = 'black', label = 'Data O$_2$')
    ax[1].plot(O2_gas_fit['x'], O2_gas_fit['y'],
        '-', color = 'red', label = 'Model O$_2$')   

    # Create second y-axis for H2/O2 ratio (gas phase)
    ax1_twin = ax[1].twinx()
    start_idx_gas = 500
    ratio_gas_experimental = H2_gas_experimental['y'][start_idx_gas:] / O2_gas_experimental['y'][start_idx_gas:]
    ratio_gas_fit = H2_gas_fit['y'][start_idx_gas:] / O2_gas_fit['y'][start_idx_gas:]
    
    
    ax1_twin.plot(H2_gas_experimental['x'][start_idx_gas:], ratio_gas_experimental,
        '.', color = 'green', markersize=2, alpha=0.4, label = 'Ratio H$_2$/O$_2$ (Data)')
    
    ax1_twin.plot(H2_gas_fit['x'][start_idx_gas:], ratio_gas_fit,
        '-', color = 'darkgreen', linewidth = 2, label = 'Ratio H$_2$/O$_2$ (Model)')
    
    ax1_twin.set_ylabel('H$_2$/O$_2$ Ratio', color='darkgreen')
    ax1_twin.tick_params(axis='y', labelcolor='darkgreen')
    
    # Combine legends from both axes
    lines_1, labels_1 = ax[1].get_legend_handles_labels()
    lines_1_twin, labels_1_twin = ax1_twin.get_legend_handles_labels()
    ax[1].legend(lines_1 + lines_1_twin, labels_1 + labels_1_twin, 
                 loc='center left', bbox_to_anchor=(1.25, 0.34))
    
    ax[1].set_title('Gas phase', fontweight='bold')
    ax[1].set_xlabel('Time / s')
    ax[1].set_ylabel('Concentration / μmol·L$^{-1}$')


    img = mpimg.imread('figures/Reaction_Scheme_Liquid_Gas.png')
    imagebox = OffsetImage(img, zoom=0.1) 
    ab = AnnotationBbox(imagebox, (1.71, 1.2), frameon=True, 
                        bboxprops=dict(boxstyle='round,pad=0.5', edgecolor = 'lightgrey'),
                        xycoords=ax[1].transAxes)
    ax[1].add_artist(ab)



    ax[0].text(-0.23, 1.0, 'A',transform=ax[0].transAxes,fontsize=22, fontweight='bold')
    ax[1].text(-0.23, 1.0, 'B',transform=ax[1].transAxes,fontsize=22, fontweight='bold')
    ax[1].text(1.3, 1.57, 'C',transform=ax[1].transAxes,fontsize=22, fontweight='bold')

    #fig.savefig('Figures/Liquid_Gasphase_Model.pdf', dpi = 500)

    plt.show()
    

if __name__ == "__main__":
    main()