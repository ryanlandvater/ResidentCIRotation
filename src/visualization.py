
import matplotlib.pyplot as plt
import numpy as np

def generate_QC_graph(df, analyzer_name, mean, sd, warnings = None, failures = None):
    """
    Generate a QC plot with control lines using a pandas DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: timestamp, result (QC values only)
    analyzer_name : str
        Name of the analyzer for the title
    mean : float
        Mean value for control lines
    sd : float
        Standard deviation for control lines
    warnings : pandas.Series
        Boolean Series indicating warnings
    failures : pandas.Series
        Boolean Series indicating failures
    """
    
    # Get QC values from the result column
    qc_values_list = df['result'].values
    
    # Create labels for each QC run
    qc_labels = [f"Day {i+1}\nQC: {qc_val:.1f}" for i, qc_val in enumerate(qc_values_list)]
    
    if warnings is not None and failures is not None:
        # Determine colors based on warnings and failures
        colors = ['#FF0000' if fail else '#FFA500' if warn else "C0" for fail, warn in zip(failures, warnings)]
    else: 
        colors = ['C0'] * len(qc_values_list)  # Default to black if no warnings/failures provided
    # Create plot
    plt.figure(figsize=(16, 8))

    # Add control lines
    plt.axhline(y=mean, color='green', linestyle='-', linewidth=2, label='Mean')
    plt.axhline(y=mean + sd, color='yellow', linestyle='--', linewidth=1)
    plt.axhline(y=mean - sd, color='yellow', linestyle='--', linewidth=1)
    plt.axhline(y=mean + 2*sd, color='orange', linestyle='--', linewidth=1)
    plt.axhline(y=mean - 2*sd, color='orange', linestyle='--', linewidth=1)
    plt.axhline(y=mean + 3*sd, color='red', linestyle='--', linewidth=1)
    plt.axhline(y=mean - 3*sd, color='red', linestyle='--', linewidth=1)

    positions = list(range(1, len(qc_values_list) + 1))
    
    # Plot connecting line first (in gray)
    plt.plot(positions, qc_values_list, linestyle='-', color='C0', linewidth=2, alpha=0.5)
    
    # Plot QC values with individual colors
    plt.scatter(positions, qc_values_list, edgecolors='black', c=colors, s=100, zorder=5)
    
    # Add custom legend entries for QC value status
    plt.plot([], color='yellow', linestyle='--', linewidth=1, label='+/- 1 SD')
    plt.plot([], color='orange', linestyle='--', linewidth=1, label='+/- 2 SD')
    plt.plot([], color='red', linestyle='--', linewidth=1, label='+/- 3 SD')
    
    if (warnings is not None and failures is not None):
        plt.scatter([], [], c='C0', s=100, label='QC Pass')
        plt.scatter([], [], c='#FFA500', s=100, label='QC Warning')
        plt.scatter([], [], c='#FF0000', s=100, label='QC Failure')
    else: 
        plt.scatter([], [], c='C0', s=100, label='QC Values')
    
    plt.xlabel('QC Run (Day and QC Value)')
    plt.ylabel(f'{analyzer_name} Result')
    plt.title(f'Levey-Jennings Control Chart for {analyzer_name}')
    plt.legend(loc='best')
    plt.xticks(positions, qc_labels, rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True, alpha=0.3, axis='y')
    plt.show()

def generate_westguard_graph(df, analyzer_name, mean, sd, ref_lower, ref_upper, warnings = None, failures = None):
    """
    Generate a box plot of patient results per QC timestamp with control lines.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: timestamp, patient_result, qc_timestamp, qc_value
    analyzer_name : str
        Name of the analyzer for the title
    mean : float
        Mean value for control lines
    sd : float
        Standard deviation for control lines
    ref_lower : float
        Lower reference range value
    ref_upper : float
        Upper reference range value
    """
    
    # Group by QC timestamp
    grouped = df.groupby('qc_timestamp')
    
    # Prepare data for plotting
    qc_values_list = [group['qc_value'].iloc[0] for name, group in grouped]
    patient_results_list = [group['patient_result'].values for name, group in grouped]
    
    # Create labels for each QC run
    qc_labels = [f"Day {i+1}\nQC: {qc_val:.1f}" for i, qc_val in enumerate(qc_values_list)]
    
    # Create plot
    plt.figure(figsize=(16, 8))

    # Add control lines
    plt.axhline(y=mean, color='green', linestyle='-', linewidth=2, label='Mean')
    plt.axhline(y=mean + sd, color='yellow', linestyle='--', linewidth=1)
    plt.axhline(y=mean - sd, color='yellow', linestyle='--', linewidth=1)
    plt.axhline(y=mean + 2*sd, color='orange', linestyle='--', linewidth=1)
    plt.axhline(y=mean - 2*sd, color='orange', linestyle='--', linewidth=1)
    plt.axhline(y=mean + 3*sd, color='red', linestyle='--', linewidth=1)
    plt.axhline(y=mean - 3*sd, color='red', linestyle='--', linewidth=1)
    
    positions = list(range(1, len(patient_results_list) + 1))
    
    # Create box plots for patient results
    bp = plt.boxplot(patient_results_list, positions=positions, widths=0.6, 
                     patch_artist=True, showfliers=True)
    
    # Color the boxes
    if warnings is not None and failures is not None:
        colors = ['#FF0000' if fail else '#FFA500' if warn else "C0" for fail, warn in zip(failures, warnings)]
    else:
        colors = ['C0'] * len(patient_results_list)
        
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Plot connecting line first (in gray)
    plt.plot(positions, qc_values_list, linestyle='-', color='C0', linewidth=2, alpha=0.5)
    
    # Plot QC values with individual colors
    plt.scatter(positions, qc_values_list, edgecolors='black', c=colors, s=100, zorder=5)
    
    # Add reference range as shaded regions (after plotting so we know the y-limits)
    y_min, y_max = plt.ylim()
    plt.axhspan(ref_upper, y_max, color='purple', alpha=0.1, label='Outside Reference Range')
    plt.axhspan(y_min, ref_lower, color='purple', alpha=0.1)

    # Add custom legend entries
    plt.plot([], color='yellow', linestyle='--', linewidth=1, label='+/- 1 SD')
    plt.plot([], color='orange', linestyle='--', linewidth=1, label='+/- 2 SD')
    plt.plot([], color='red', linestyle='--', linewidth=1, label='+/- 3 SD')
    
    # Add custom legend entries for QC value status if warnings/failures provided
    plt.xlabel('QC Run (Day and QC Value)')
    plt.ylabel(f'{analyzer_name} Result')
    plt.ylim(y_min, y_max)
    plt.title(f'Patient Results Box Plot with QC Values for {analyzer_name}')
    plt.legend(loc='best')
    plt.xticks(positions, qc_labels, rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True, alpha=0.3, axis='y')
    plt.show()