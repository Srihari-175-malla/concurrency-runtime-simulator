"""
Deterministic Execution & Concurrency Simulator (DECS)
Simulates deterministic multi-threaded task scheduling, event loops, and network fault injection.

Features:
  - Virtual Logical Clock for 100% deterministic replay.
  - Pseudo-random Fault Injector (Packet Drop, Latency Jitter, Reordering).
  - Thread-pool and Task Queue concurrency simulation.
"""

import heapq
import random

class ScheduledTask:
    def __init__(self, timestamp, task_id, fn, args=()):
        self.timestamp = timestamp
        self.task_id = task_id
        self.fn = fn
        self.args = args

    def __lt__(self, other):
        return (self.timestamp, self.task_id) < (other.timestamp, other.task_id)

class DECSEngine:
    def __init__(self, seed=42, packet_drop_rate=0.05, max_jitter_ms=20):
        self.seed = seed
        self.rng = random.Random(seed)
        self.drop_rate = packet_drop_rate
        self.max_jitter = max_jitter_ms
        self.virtual_clock_ms = 0
        self.task_queue = []
        self._task_seq = 0
        self.execution_log = []

    def schedule_task(self, delay_ms, fn, *args):
        self._task_seq += 1
        exec_time = self.virtual_clock_ms + delay_ms
        task = ScheduledTask(exec_time, self._task_seq, fn, args)
        heapq.heappush(self.task_queue, task)

    def simulate_network_message(self, src, dst, payload, delivery_fn):
        """
        Simulates message delivery with jitter & fault injection.
        """
        if self.rng.random() < self.drop_rate:
            self.execution_log.append((self.virtual_clock_ms, 'DROPPED', src, dst, payload))
            return  # Packet dropped

        jitter = self.rng.randint(1, self.max_jitter)
        self.schedule_task(jitter, delivery_fn, src, dst, payload)

    def run_until_idle(self):
        while self.task_queue:
            task = heapq.heappop(self.task_queue)
            self.virtual_clock_ms = task.timestamp
            res = task.fn(*task.args)
            self.execution_log.append((self.virtual_clock_ms, 'EXECUTED', task.task_id, res))

        return self.execution_log

if __name__ == "__main__":
    def receive_msg(src, dst, data):
        return f"Msg from {src} to {dst}: {data}"

    engine = DECSEngine(seed=100)
    engine.simulate_network_message("NodeA", "NodeB", "PING", receive_msg)
    engine.simulate_network_message("NodeB", "NodeA", "PONG", receive_msg)

    logs = engine.run_until_idle()
    print("=== DECS Deterministic Concurrency Execution Log ===")
    for entry in logs:
        print(entry)
