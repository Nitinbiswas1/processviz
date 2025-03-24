import subprocess
import sys
# Function to install required libraries if not found
def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"{package_name} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
# Install necessary libraries
for package in ['psutil', 'matplotlib']:
    install_package(package)
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# Initialize figure and axes for custom layout
fig = plt.figure(figsize=(14, 14))
fig.suptitle('Real-Time Task Manager Simulation', fontsize=18, weight='bold')
# Define subplot positions
table_ax = fig.add_axes([0.05, 0.7, 0.4, 0.2])  # Table (Top-Left)
pie_ax = fig.add_axes([0.55, 0.7, 0.3, 0.25])   # Pie Chart (Top-Right)
legend_ax = fig.add_axes([0.87, 0.7, 0.1, 0.25])  # Legend Box (Right of Pie Chart)
bar_ax = fig.add_axes([0.1, 0.2, 0.8, 0.4])     # Bar Chart (Bottom)
colors = ['#FF6B6B', '#4D96FF', '#6BCB77', '#FFA36C', '#C47AFF']
def get_top_processes(limit=5):
    """Fetch top processes sorted by CPU usage."""
    return sorted(
        psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']),
        key=lambda p: p.info['cpu_percent'],
        reverse=True
    )[:limit]
def display_process_table(processes):
    """Display process table with smaller column width."""
    table_ax.clear()
    table_ax.axis('off')
    table_ax.set_title('Top 5 Processes', fontsize=14, weight='bold')
    cell_text = [[p.info['pid'], p.info['name'][:10], f"{p.info['cpu_percent']:.2f}", f"{p.info['memory_percent']:.2f}"] for p in processes]
    table = table_ax.table(
        cellText=cell_text,
        colLabels=['PID', 'Name', 'CPU (%)', 'Mem (%)'],
        loc='center',
        cellLoc='center',
        colColours=['#DDDDDD'] * 4
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(0.7, 1.2)
def plot_bar_chart(processes):
    """Render a bar chart and fix label visibility."""
    bar_ax.clear()
    bar_ax.set_title('CPU Usage (Bar Chart)', fontsize=14, weight='bold')
    names = [f"{p.info['name']} (PID {p.info['pid']})" for p in processes]
    cpu_usages = [p.info['cpu_percent'] for p in processes]
    bars = bar_ax.bar(names, cpu_usages, color=colors[:len(processes)], edgecolor='black')
    bar_ax.set_ylabel('CPU Usage (%)', fontsize=12)
    bar_ax.set_ylim(0, max(cpu_usages) + 10)
    bar_ax.set_xticks(range(len(names)))
    bar_ax.set_xticklabels(names, rotation=0, ha='center', fontsize=10)
    for bar, usage in zip(bars, cpu_usages):
        bar_ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, f"{usage:.1f}%", 
                    ha='center', va='bottom', fontsize=9, weight='bold')
def plot_pie_chart(processes):
    """Render the pie chart with a separate legend."""
    pie_ax.clear()
    # Move the title to the left of the pie chart
    pie_ax.text(-1.5, 1, 'CPU Usage Distribution', fontsize=14, weight='bold', ha='center', va='center')
    names = [p.info['name'] for p in processes]
    cpu_usages = [max(p.info['cpu_percent'], 0.1) for p in processes]
    wedges, _ = pie_ax.pie(
        cpu_usages,
        colors=colors[:len(processes)],
        startangle=90,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
    )
    # Add a central white circle for a donut effect
    centre_circle = plt.Circle((0, 0), 0.65, fc='white')
    pie_ax.add_artist(centre_circle)
    # Update the legend separately
    legend_ax.clear()
    legend_ax.axis('off')
    legend_text = [[p.info['name'], f"{p.info['cpu_percent']:.1f}%"] for p in processes]
    legend_table = legend_ax.table(
        cellText=legend_text,
        colLabels=['Process', 'CPU %'],
        loc='center',
        cellLoc='left',
        colColours=['#DDDDDD', '#DDDDDD']
    )
    legend_table.auto_set_font_size(False)
    legend_table.set_fontsize(9)
    legend_table.scale(0.9, 1.2)
def update(frame):
    """Update function called by FuncAnimation."""
    top_processes = get_top_processes()
    display_process_table(top_processes)
    plot_bar_chart(top_processes)
    plot_pie_chart(top_processes)
# Start animation
animation = FuncAnimation(fig, update, interval=1000)
plt.show()
