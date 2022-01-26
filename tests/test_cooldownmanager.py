import threading
import time
import unittest

import toml

from flaskapp.core.cooldownmanager import CoolDownManager


class TestCoolDownManager(unittest.TestCase):
    def setUp(self):
        self.cooldownmanager = CoolDownManager()
        project_config = toml.load("project_config.toml")
        self.ref_cooldown_delay = project_config["time"]["countdown_delay"]
        self.tolerance = project_config["time"]["tolerance"]

    def test_init(self):
        self.assertEqual(self.cooldownmanager._cooldown_delay, self.ref_cooldown_delay)

    def test_cooldown(self):
        time_0 = time.time()
        self.cooldownmanager._cooldown()
        time_1 = time.time()
        self.assertGreaterEqual(time_1 - time_0, self.ref_cooldown_delay)
        self.assertAlmostEqual(
            time_1 - time_0, self.ref_cooldown_delay, delta=self.tolerance
        )

    def test_get_token(self):
        run_thread = threading.Thread(
            target=self.cooldownmanager._run, args=(), daemon=True
        )
        run_thread.start()

        time_0 = time.time()
        token_1 = self.cooldownmanager.get_token()
        time_1 = time.time()

        # no cooldown needed : token should be returned directly
        self.assertEqual(token_1, True)
        self.assertAlmostEqual(
            float(time_1 - time_0), float(0), delta=float(self.tolerance)
        )

        # cooldown needed : token should only be returned after cooldown delay
        time_2 = time.time()
        token_2 = self.cooldownmanager.get_token()
        time_3 = time.time()
        run_thread.join(
            timeout=0
        )  # Do not wait for run_thread to end before destroying it (infinite while loop)
        self.assertLessEqual(
            time_2 - time_1, self.ref_cooldown_delay
        )  # Otherwise this test would be pointless
        self.assertEqual(token_2, True)
        self.assertGreaterEqual(time_3 - time_1, self.ref_cooldown_delay)
        self.assertAlmostEqual(
            time_3 - time_1, self.ref_cooldown_delay, delta=self.tolerance
        )
