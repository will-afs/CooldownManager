import threading
import time
import unittest

import toml

from flaskapp.core.cooldownmanager import CoolDownManager


class TestCoolDownManager(unittest.TestCase):
    def setUp(self):
        self.cooldownmanager = CoolDownManager()
        project_config = toml.load("project_config.toml")
        self.ref_cooldown_delay = project_config["time"]["cooldown_delay"]
        self.compute_tolerance = project_config["time"]["compute_related_tolerance"]

    def test_init(self):
        self.assertEqual(
            type(self.cooldownmanager._cooldown_lock), type(threading.Lock())
        )
        self.assertEqual(
            type(self.cooldownmanager._get_token_lock), type(threading.Lock())
        )
        self.assertEqual(self.cooldownmanager._cooldown_delay, self.ref_cooldown_delay)
        self.assertEqual(self.cooldownmanager._cooldown_needed, False)
        self.assertEqual(self.cooldownmanager._stopping, False)
        self.assertEqual(self.cooldownmanager._run_thread, None)

    def test_cooldown(self):
        time_0 = time.time()
        self.cooldownmanager._cooldown()
        time_1 = time.time()
        self.assertGreaterEqual(time_1 - time_0, self.ref_cooldown_delay)
        self.assertAlmostEqual(
            time_1 - time_0, self.ref_cooldown_delay, delta=self.compute_tolerance
        )

    def test_start_stop(self):
        self.cooldownmanager.start()
        assert self.cooldownmanager._run_thread
        self.cooldownmanager.stop()
        assert not self.cooldownmanager._run_thread

        self.cooldownmanager.start()
        assert self.cooldownmanager._run_thread
        assert self.cooldownmanager.get_token()
        self.cooldownmanager.stop()
        assert not self.cooldownmanager._run_thread

    def test_get_token(self):
        self.cooldownmanager.start()

        time_0 = time.time()
        token_1 = self.cooldownmanager.get_token()
        time_1 = time.time()

        time_2 = time.time()
        token_2 = self.cooldownmanager.get_token()
        time_3 = time.time()

        self.cooldownmanager.stop()

        # no cooldown needed : token should have been returned directly
        self.assertEqual(token_1, True)
        self.assertAlmostEqual(time_1 - time_0, 0.0, delta=self.compute_tolerance)

        # cooldown needed : token should have only been returned after cooldown delay
        # Assert cooldown delay is not over before running next tests
        self.assertLessEqual(time_2 - time_1, self.ref_cooldown_delay)
        self.assertEqual(token_2, True)
        self.assertGreaterEqual(time_3 - time_1, self.ref_cooldown_delay)
        self.assertAlmostEqual(
            time_3 - time_1, self.ref_cooldown_delay, delta=self.compute_tolerance
        )
