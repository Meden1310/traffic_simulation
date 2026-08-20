"""
Phân tích và visualize kết quả mô phỏng SUMO
CHẠY TRÊN PYCHARM - WINDOWS
"""

import pandas as pd
import matplotlib.pyplot as plt
import json
import glob
import os
from datetime import datetime


class TrafficAnalysis:
    def __init__(self, output_folder='outputs'):
        self.output_folder = output_folder

    def load_latest_results(self, network_type='large'):
        """Load kết quả mới nhất"""
        # Tìm file summary mới nhất
        pattern = f'{self.output_folder}/{network_type}_*_summary.json'
        files = glob.glob(pattern)

        if not files:
            print(f"❌ Không tìm thấy kết quả cho {network_type} intersection!")
            print(f"   Chạy simulation.py trước đã!")
            return None, None

        # Lấy file mới nhất
        latest_summary = max(files, key=os.path.getctime)

        # Load summary
        with open(latest_summary, 'r', encoding='utf-8') as f:
            summary = json.load(f)

        # Load detailed data
        csv_file = latest_summary.replace('_summary.json', '_detailed.csv')
        df = pd.read_csv(csv_file)

        print(f"✓ Đã load: {latest_summary}")
        return summary, df

    def plot_metrics(self, df, network_type='small', save=True):
        """Vẽ biểu đồ metrics"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Traffic Simulation Results - {network_type.upper()} Intersection',
                     fontsize=16, fontweight='bold')

        # 1. Waiting Time Over Time
        ax1 = axes[0, 0]
        ax1.plot(df['step'], df['avg_waiting_time'], color='#2E86AB', linewidth=1.5)
        ax1.set_xlabel('Simulation Step (seconds)')
        ax1.set_ylabel('Average Waiting Time (s)')
        ax1.set_title('Average Waiting Time Over Time')
        ax1.grid(True, alpha=0.3)

        # 2. Queue Length Over Time
        ax2 = axes[0, 1]
        ax2.plot(df['step'], df['queue_length'], color='#A23B72', linewidth=1.5)
        ax2.set_xlabel('Simulation Step (seconds)')
        ax2.set_ylabel('Queue Length (vehicles)')
        ax2.set_title('Queue Length Over Time')
        ax2.grid(True, alpha=0.3)

        # 3. Number of Vehicles Over Time
        ax3 = axes[1, 0]
        ax3.plot(df['step'], df['num_vehicles'], color='#F18F01', linewidth=1.5)
        ax3.set_xlabel('Simulation Step (seconds)')
        ax3.set_ylabel('Number of Vehicles')
        ax3.set_title('Active Vehicles Over Time')
        ax3.grid(True, alpha=0.3)

        # 4. Histogram of Waiting Times
        ax4 = axes[1, 1]
        ax4.hist(df['avg_waiting_time'], bins=50, color='#6A994E', alpha=0.7, edgecolor='black')
        ax4.set_xlabel('Average Waiting Time (s)')
        ax4.set_ylabel('Frequency')
        ax4.set_title('Distribution of Waiting Times')
        ax4.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        if save:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            plot_file = f'{self.output_folder}/{network_type}_{timestamp}_plots.png'
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            print(f"✓ Đã lưu biểu đồ: {plot_file}")

        plt.show()

    def print_summary(self, summary):
        """In summary đẹp"""
        print("\n" + "=" * 70)
        print(f"TRAFFIC SIMULATION SUMMARY - {summary['network_type'].upper()} INTERSECTION")
        print("=" * 70)
        print(f"Simulation Time:          {summary['simulation_time']} seconds")
        print(f"Random Seed:              {summary['seed']}")
        print(f"Total Steps:              {summary['total_steps']}")
        print("-" * 70)
        print("WAITING TIME METRICS:")
        print(f"  Average:                {summary['average_waiting_time']:.2f} seconds")
        print(f"  Maximum:                {summary['max_waiting_time']:.2f} seconds")
        print(f"  Minimum:                {summary['min_waiting_time']:.2f} seconds")
        print(f"  Std Deviation:          {summary['std_waiting_time']:.2f} seconds")
        print("-" * 70)
        print("QUEUE LENGTH METRICS:")
        print(f"  Average:                {summary['average_queue_length']:.2f} vehicles")
        print(f"  Maximum:                {summary['max_queue_length']:.0f} vehicles")
        print("=" * 70 + "\n")

    def compare_intersections(self):
        """So sánh small và large intersection"""
        # Load cả hai
        print("\n📊 Đang load kết quả small intersection...")
        small_summary, small_df = self.load_latest_results('small')

        print("📊 Đang load kết quả large intersection...")
        large_summary, large_df = self.load_latest_results('large')

        if small_summary is None or large_summary is None:
            print("\n❌ Cần có kết quả của cả small và large intersection để so sánh!")
            print("   Chạy simulation.py với cả 2 loại intersection trước!")
            return

        # Tạo comparison plot
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))

        # Comparison 1: Waiting Time
        ax1 = axes[0]
        metrics = ['average_waiting_time', 'max_waiting_time']
        small_vals = [small_summary[m] for m in metrics]
        large_vals = [large_summary[m] for m in metrics]

        x = range(len(metrics))
        width = 0.35
        ax1.bar([i - width / 2 for i in x], small_vals, width, label='Small', color='#2E86AB')
        ax1.bar([i + width / 2 for i in x], large_vals, width, label='Large', color='#A23B72')
        ax1.set_ylabel('Time (seconds)')
        ax1.set_title('Waiting Time Comparison')
        ax1.set_xticks(x)
        ax1.set_xticklabels(['Average', 'Maximum'])
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')

        # Comparison 2: Queue Length
        ax2 = axes[1]
        metrics = ['average_queue_length', 'max_queue_length']
        small_vals = [small_summary[m] for m in metrics]
        large_vals = [large_summary[m] for m in metrics]

        ax2.bar([i - width / 2 for i in x], small_vals, width, label='Small', color='#2E86AB')
        ax2.bar([i + width / 2 for i in x], large_vals, width, label='Large', color='#A23B72')
        ax2.set_ylabel('Vehicles')
        ax2.set_title('Queue Length Comparison')
        ax2.set_xticks(x)
        ax2.set_xticklabels(['Average', 'Maximum'])
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plot_file = f'{self.output_folder}/comparison_{timestamp}.png'
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"✓ Đã lưu biểu đồ so sánh: {plot_file}")

        plt.show()

        # Print comparison table
        print("\n" + "=" * 90)
        print("INTERSECTION COMPARISON")
        print("=" * 90)
        print(f"{'Metric':<35} {'Small':>20} {'Large':>20} {'Difference':>13}")
        print("-" * 90)

        metrics_compare = [
            ('Average Waiting Time (s)', 'average_waiting_time'),
            ('Max Waiting Time (s)', 'max_waiting_time'),
            ('Average Queue Length', 'average_queue_length'),
            ('Max Queue Length', 'max_queue_length')
        ]

        for label, key in metrics_compare:
            small_val = small_summary[key]
            large_val = large_summary[key]
            diff = ((large_val - small_val) / small_val * 100) if small_val != 0 else 0
            print(f"{label:<35} {small_val:>20.2f} {large_val:>20.2f} {diff:>12.1f}%")

        print("=" * 90 + "\n")


def main():
    """Main function - CHỈNH Ở ĐÂY"""

    # ===== CẤU HÌNH =====
    network_type = 'large'  # 'small' hoặc 'large' - phải khớp với simulation.py
    # ====================

    analysis = TrafficAnalysis()

    print("=" * 70)
    print("TRAFFIC SIMULATION ANALYSIS")
    print("=" * 70)

    # Load và visualize
    summary, df = analysis.load_latest_results(network_type)

    if summary and df is not None:
        analysis.print_summary(summary)
        analysis.plot_metrics(df, network_type)

        # Uncomment dòng dưới để so sánh 2 intersection
        # (Cần chạy simulation.py với cả small và large trước)
        # analysis.compare_intersections()
    else:
        print("\n❌ Không tìm thấy kết quả!")
        print("   Hãy chạy simulation.py trước!\n")


if __name__ == '__main__':
    main()