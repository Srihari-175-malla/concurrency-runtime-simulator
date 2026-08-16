import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from decs_engine import DECSEngine

class TestDECS(unittest.TestCase):
    def test_deterministic_replay(self):
        def dummy_handler(a, b, msg):
            return f"{a}->{b}:{msg}"

        # Run 1
        e1 = DECSEngine(seed=42)
        e1.simulate_network_message("A", "B", "req1", dummy_handler)
        e1.simulate_network_message("B", "C", "req2", dummy_handler)
        log1 = e1.run_until_idle()

        # Run 2 with same seed
        e2 = DECSEngine(seed=42)
        e2.simulate_network_message("A", "B", "req1", dummy_handler)
        e2.simulate_network_message("B", "C", "req2", dummy_handler)
        log2 = e2.run_until_idle()

        self.assertEqual(log1, log2)

if __name__ == '__main__':
    unittest.main()
