import os
import sys

# ===== SET SUMO_HOME - QUAN TRỌNG =====
# Thay đổi đường dẫn này nếu bạn cài SUMO ở chỗ khác
os.environ['SUMO_HOME'] = r'C:\Program Files\sumo-win64-1.25.0\sumo-1.25.0'

# Kiểm tra SUMO_HOME
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("ERROR: Chưa set SUMO_HOME! Sửa dòng 11 trong code này!")

import traci
import numpy as np
import pandas as pd
import json
from datetime import datetime


class TrafficSimulation:
    def __init__(self, network_type='large', seed=42, simulation_time=3600):
        """
        Khởi tạo simulation

        Args:
            network_type: 'small' hoặc 'large'
            seed: Random seed để tái tạo kết quả
            simulation_time: Thời gian mô phỏng (giây)
        """
        self.network_type = network_type
        self.seed = seed
        self.simulation_time = simulation_time
        print(f"### KIỂM TRA: NETWORK_TYPE = {network_type} ###")

        # Đường dẫn files
        self.network_file = f'networks/{network_type}_intersection.net.xml'
        self.route_file = f'routes/{network_type}_intersection.rou.xml'
        self.config_file = f'configs/{network_type}_intersection.sumocfg'

        # Metrics storage
        self.waiting_times = []
        self.queue_lengths = []
        self.step_data = []

        # Set random seed
        np.random.seed(seed)

    def generate_route_file(self, flow_rate=300):
        """
        Tạo file route với fixed flow

        Args:
            flow_rate: Số xe/giờ cho mỗi hướng
        """
        route_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">

    <!-- Vehicle Types -->
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5" maxSpeed="50" guiShape="passenger"/>

    <!-- Routes -->
'''

        if self.network_type == 'small':
            # Định nghĩa các routes cho small intersection
            routes = [
                ('route_N_S', 'E0', 'E1'),  # Bắc -> Nam
                ('route_N_E', 'E0', 'E2'),  # Bắc -> Đông
                ('route_N_W', 'E0', 'E3'),  # Bắc -> Tây
                ('route_S_N', '-E1', '-E0'),  # Nam -> Bắc
                ('route_S_E', '-E1', 'E2'),  # Nam -> Đông
                ('route_S_W', '-E1', 'E3'),  # Nam -> Tây
                ('route_E_W', '-E2', 'E3'),  # Đông -> Tây
                ('route_E_N', '-E2', '-E0'),  # Đông -> Bắc
                ('route_E_S', '-E2', 'E1'),  # Đông -> Nam
                ('route_W_E', '-E3', 'E2'),  # Tây -> Đông
                ('route_W_N', '-E3', '-E0'),  # Tây -> Bắc
                ('route_W_S', '-E3', 'E1'),  # Tây -> Nam
            ]
        else:  # large intersection
            routes = [
                ('route_N_S', 'E0', 'E1'),
                ('route_N_E', 'E0', 'E2'),
                ('route_N_W', 'E0', 'E3'),
                ('route_S_N', '-E1', '-E0'),
                ('route_S_E', '-E1', 'E2'),
                ('route_S_W', '-E1', 'E3'),
                ('route_E_W', '-E2', 'E3'),
                ('route_E_N', '-E2', '-E0'),
                ('route_E_S', '-E2', 'E1'),
                ('route_W_E', '-E3', 'E2'),
                ('route_W_N', '-E3', '-E0'),
                ('route_W_S', '-E3', 'E1'),
            ]

        # Thêm route definitions
        for route_id, from_edge, to_edge in routes:
            route_content += f'    <route id="{route_id}" edges="{from_edge} {to_edge}"/>\n'

        route_content += '\n    <!-- Traffic Flows -->\n'

        # Thêm flows với fixed seed
        flow_id = 0
        for route_id, _, _ in routes:
            veh_per_hour = flow_rate
            route_content += f'    <flow id="flow_{flow_id}" route="{route_id}" begin="0" end="{self.simulation_time}" ' \
                             f'vehsPerHour="{veh_per_hour}" type="car" departLane="best" departSpeed="max"/>\n'
            flow_id += 1

        route_content += '</routes>'

        # Tạo thư mục nếu chưa có
        os.makedirs('routes', exist_ok=True)

        # Ghi file
        with open(self.route_file, 'w', encoding='utf-8') as f:
            f.write(route_content)

        print(f"✓ Đã tạo route file: {self.route_file}")

    def generate_config_file(self):
        """Tạo SUMO config file"""
        config_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">
    <input>
        <net-file value="../{self.network_file}"/>
        <route-files value="../{self.route_file}"/>
    </input>

    <time>
        <begin value="0"/>
        <end value="{self.simulation_time}"/>
    </time>

    <processing>
        <time-to-teleport value="-1"/>
    </processing>

    <random>
        <seed value="{self.seed}"/>
    </random>

    <report>
        <verbose value="true"/>
        <no-step-log value="true"/>
    </report>
</configuration>
'''

        os.makedirs('configs', exist_ok=True)

        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)

        print(f"✓ Đã tạo config file: {self.config_file}")

    def run_simulation(self):
        """Chạy mô phỏng với TraCI"""
        print(f"\n{'=' * 60}")
        print(f"Bắt đầu mô phỏng: {self.network_type.upper()} Intersection")
        print(f"Seed: {self.seed} | Thời gian: {self.simulation_time}s")
        print(f"{'=' * 60}\n")

        # Khởi động SUMO
        sumo_binary = "sumo"  # Đổi thành "sumo-gui" để xem visualization
        sumo_cmd = [sumo_binary, "-c", self.config_file, "--seed", str(self.seed)]

        traci.start(sumo_cmd)

        step = 0

        try:
            while step < self.simulation_time:
                traci.simulationStep()

                # Thu thập metrics mỗi step
                current_waiting_times = []
                current_queue_length = 0

                # Lấy thông tin tất cả vehicles
                vehicle_ids = traci.vehicle.getIDList()

                for veh_id in vehicle_ids:
                    # Waiting time (giây)
                    waiting_time = traci.vehicle.getWaitingTime(veh_id)
                    current_waiting_times.append(waiting_time)

                    # Queue length (xe đang chờ)
                    if waiting_time > 0:
                        current_queue_length += 1

                # Lưu metrics
                avg_waiting = np.mean(current_waiting_times) if current_waiting_times else 0
                self.waiting_times.append(avg_waiting)
                self.queue_lengths.append(current_queue_length)

                # Lưu chi tiết từng step
                self.step_data.append({
                    'step': step,
                    'num_vehicles': len(vehicle_ids),
                    'avg_waiting_time': avg_waiting,
                    'queue_length': current_queue_length
                })

                # In progress mỗi 300 steps
                if step % 300 == 0:
                    print(f"Step {step}/{self.simulation_time} | "
                          f"Vehicles: {len(vehicle_ids)} | "
                          f"Avg Wait: {avg_waiting:.2f}s | "
                          f"Queue: {current_queue_length}")

                step += 1

        finally:
            traci.close()

        print(f"\n✓ Mô phỏng hoàn thành!")

    def save_results(self):
        """Lưu kết quả ra files"""
        os.makedirs('outputs', exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        prefix = f'outputs/{self.network_type}_{timestamp}'

        # 1. Summary metrics
        summary = {
            'network_type': self.network_type,
            'seed': self.seed,
            'simulation_time': self.simulation_time,
            'average_waiting_time': float(np.mean(self.waiting_times)),
            'max_waiting_time': float(np.max(self.waiting_times)),
            'min_waiting_time': float(np.min(self.waiting_times)),
            'std_waiting_time': float(np.std(self.waiting_times)),
            'average_queue_length': float(np.mean(self.queue_lengths)),
            'max_queue_length': float(np.max(self.queue_lengths)),
            'total_steps': len(self.step_data)
        }

        summary_file = f'{prefix}_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)

        print(f"\n✓ Đã lưu summary: {summary_file}")

        # 2. Chi tiết từng step
        df = pd.DataFrame(self.step_data)
        csv_file = f'{prefix}_detailed.csv'
        df.to_csv(csv_file, index=False)
        print(f"✓ Đã lưu detailed data: {csv_file}")

        # 3. In ra console
        print(f"\n{'=' * 60}")
        print("KẾT QUẢ MÔ PHỎNG")
        print(f"{'=' * 60}")
        print(f"Average Waiting Time: {summary['average_waiting_time']:.2f} seconds")
        print(f"Average Queue Length: {summary['average_queue_length']:.2f} vehicles")
        print(f"Max Queue Length: {summary['max_queue_length']:.0f} vehicles")
        print(f"{'=' * 60}\n")

        return summary, df


def main():
    """Main function - CHỈNH Ở ĐÂY"""

    # ===== CẤU HÌNH - THAY ĐỔI Ở ĐÂY =====
    NETWORK_TYPE = 'large'  # Đổi sang 'large' để test large intersection
    SEED = 42  # Random seed
    SIMULATION_TIME = 3600  # 1 giờ (3600 giây)
    FLOW_RATE = 400  # vehicles/hour mỗi hướng
    # ======================================

    # Tạo simulation
    sim = TrafficSimulation(
        network_type=NETWORK_TYPE,
        seed=SEED,
        simulation_time=SIMULATION_TIME
    )

    # Generate files
    sim.generate_route_file(flow_rate=FLOW_RATE)
    sim.generate_config_file()

    # Run simulation
    sim.run_simulation()

    # Save and display results
    summary, detailed_df = sim.save_results()

    print("\n✓ Hoàn thành! Kiểm tra thư mục 'outputs' để xem kết quả chi tiết.")


if __name__ == '__main__':
    main()