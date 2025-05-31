import matplotlib.pyplot as plt
import numpy as np
from math import pi
import os

# Create output directory
os.makedirs('fig/charts', exist_ok=True)

# Data from the table
data = {
    'species': ['Deer', 'Hare', 'Penguin', 'Pūkeko', 'Stoat', 'Wallaby'],
    'CLIP-FT': [63.2, 56.7, 44.0, 56.8, 68.6, 55.5],
    'CLIP-FT+MFA': [66.7, 58.4, 46.0, 58.2, 69.8, 56.8],
    'CLIP-ReID': [65.2, 60.0, 44.8, 57.6, 67.5, 56.9],
    'CLIP-ReID+MFA': [69.4, 63.2, 50.3, 59.8, 71.5, 61.8],
    'ReID-AW': [67.5, 63.3, 48.8, 58.5, 69.5, 58.4],
    'ReID-AW+MFA': [72.4, 66.2, 55.3, 61.8, 74.1, 63.5]
}

def create_radar_chart(baseline_data, mfa_data, baseline_name, title, filename, colors):
    """Create a radar chart comparing baseline vs MFA performance"""
    
    # Number of variables
    categories = data['species']
    N = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Complete the circle
    
    # Add first value to the end to close the radar chart
    baseline_values = baseline_data + baseline_data[:1]
    mfa_values = mfa_data + mfa_data[:1]
    
    # Create figure with high DPI for better quality
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'), dpi=300)
    
    # Plot baseline method
    ax.plot(angles, baseline_values, 'o-', linewidth=3, label=baseline_name, 
            color=colors[0], markersize=8, markerfacecolor=colors[0], markeredgecolor='white', markeredgewidth=2)
    ax.fill(angles, baseline_values, alpha=0.15, color=colors[0])
    
    # Plot MFA method
    ax.plot(angles, mfa_values, 'o-', linewidth=3, label=f'{baseline_name}+MFA', 
            color=colors[1], markersize=8, markerfacecolor=colors[1], markeredgecolor='white', markeredgewidth=2)
    ax.fill(angles, mfa_values, alpha=0.15, color=colors[1])
    
    # Add category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=14, fontweight='bold')
    
    # Set y-axis limits and labels
    ax.set_ylim(35, 80)
    ax.set_yticks([40, 50, 60, 70, 80])
    ax.set_yticklabels(['40%', '50%', '60%', '70%', '80%'], fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add title
    plt.title(title, size=20, fontweight='bold', pad=30)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=14, frameon=True, 
               fancybox=True, shadow=True)
    
    # Add improvement annotation
    avg_improvement = np.mean([mfa_data[i] - baseline_data[i] for i in range(len(baseline_data))])
    plt.figtext(0.5, 0.02, f'Average mAP improvement: +{avg_improvement:.1f}%', 
                ha='center', fontsize=14, fontweight='bold', 
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(f'fig/charts/{filename}', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()

    print(f" Generated: fig/charts/{filename}")

# Define color schemes for each chart
color_schemes = {
    'CLIP-FT': ['#3498db', '#e74c3c'],      # Blue, Red
    'CLIP-ReID': ['#2ecc71', '#9b59b6'],    # Green, Purple  
    'ReID-AW': ['#f39c12', '#34495e']       # Orange, Dark Gray
}

# Generate all three charts
charts_config = [
    {
        'baseline_data': data['CLIP-FT'],
        'mfa_data': data['CLIP-FT+MFA'],
        'baseline_name': 'CLIP-FT',
        'title': 'CLIP-FT Performance Comparison',
        'filename': 'clip_ft_radar.png',
        'colors': color_schemes['CLIP-FT']
    },
    {
        'baseline_data': data['CLIP-ReID'],
        'mfa_data': data['CLIP-ReID+MFA'],
        'baseline_name': 'CLIP-ReID',
        'title': 'CLIP-ReID Performance Comparison',
        'filename': 'clip_reid_radar.png',
        'colors': color_schemes['CLIP-ReID']
    },
    {
        'baseline_data': data['ReID-AW'],
        'mfa_data': data['ReID-AW+MFA'],
        'baseline_name': 'ReID-AW',
        'title': 'ReID-AW Performance Comparison',
        'filename': 'reid_aw_radar.png',
        'colors': color_schemes['ReID-AW']
    }
]

# Generate all charts
print(" Generating radar charts...")
for config in charts_config:
    create_radar_chart(**config)

print("\nAll radar charts generated successfully!")
print(" Charts saved in: fig/charts/")
print(" Files generated:")
print("   - clip_ft_radar.png")
print("   - clip_reid_radar.png") 
print("   - reid_aw_radar.png")

# Generate a combined comparison chart
def create_combined_chart():
    """Create a combined chart showing all methods"""
    categories = data['species']
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'), dpi=300)
    
    methods_config = [
        ('CLIP-FT', data['CLIP-FT'], '#3498db', '-'),
        ('CLIP-FT+MFA', data['CLIP-FT+MFA'], '#e74c3c', '-'),
        ('CLIP-ReID', data['CLIP-ReID'], '#2ecc71', '--'),
        ('CLIP-ReID+MFA', data['CLIP-ReID+MFA'], '#9b59b6', '--'),
        ('ReID-AW', data['ReID-AW'], '#f39c12', '-.'),
        ('ReID-AW+MFA', data['ReID-AW+MFA'], '#34495e', '-.')
    ]
    
    for name, values, color, linestyle in methods_config:
        values_plot = values + values[:1]
        linewidth = 3 if 'MFA' in name else 2
        alpha = 0.8 if 'MFA' in name else 0.6
        ax.plot(angles, values_plot, linestyle, linewidth=linewidth, label=name, 
                color=color, alpha=alpha, markersize=6, marker='o')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=14, fontweight='bold')
    ax.set_ylim(35, 80)
    ax.set_yticks([40, 50, 60, 70, 80])
    ax.set_yticklabels(['40%', '50%', '60%', '70%', '80%'], fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.title('All Methods Performance Comparison', size=20, fontweight='bold', pad=30)
    plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1.1), fontsize=12, frameon=True, 
               fancybox=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig('fig/charts/all_methods_comparison.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(" Generated: fig/charts/all_methods_comparison.png")

# Generate combined chart
create_combined_chart()

print("\n Summary of improvements:")
for baseline in ['CLIP-FT', 'CLIP-ReID', 'ReID-AW']:
    baseline_avg = np.mean(data[baseline])
    mfa_avg = np.mean(data[f'{baseline}+MFA'])
    improvement = mfa_avg - baseline_avg
    print(f"   {baseline}: {baseline_avg:.1f}% to {mfa_avg:.1f}% (+{improvement:.1f}%)")