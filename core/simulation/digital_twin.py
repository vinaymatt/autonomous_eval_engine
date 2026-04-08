import random
import time


class DigitalTwinSimulator:
    def __init__(self, facility_id: str):
        self.facility_id = facility_id

    def fetch_live_kpis(self) -> dict:
        utilization = round(random.gauss(82.5, 4.0), 2)
        utilization = max(60.0, min(98.0, utilization))

        throughput = round(random.gauss(156, 12))
        throughput = max(110, min(200, throughput))

        oee = round(random.gauss(74.5, 3.5), 1)
        oee = max(55.0, min(92.0, oee))

        scrap = round(random.gauss(2.8, 0.6), 2)
        scrap = max(0.5, min(6.0, scrap))

        return {
            "timestamp": time.time(),
            "facility_id": self.facility_id,
            "machine_utilization_pct": utilization,
            "production_throughput_units_per_hr": throughput,
            "overall_equipment_effectiveness_pct": oee,
            "scrap_rate_pct": scrap,
            "active_iot_sensors": 87,
            "machines_online": 12,
            "machines_total": 15,
            "active_work_orders": random.randint(18, 32),
            "on_time_delivery_pct": round(random.gauss(94.2, 2.0), 1),
            "anomaly_detected": random.random() < 0.15,
            "anomaly_detail": "Vibration spike on Haas VF-4SS #02 — bearing wear pattern detected"
            if random.random() < 0.15
            else None,
        }