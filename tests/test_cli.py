import unittest
from detection_lab.cli import features, simulate, sweep


class DetectionTests(unittest.TestCase):
    def test_seed_reproducible(self):
        self.assertEqual(simulate(3), simulate(3))
        self.assertNotEqual(simulate(3), simulate(4))

    def test_threshold_counts(self):
        records = [{"cv": 0.01, "label": "beacon"}, {"cv": 0.7, "label": "benign"}]
        self.assertEqual(sweep(records, [0.1])[0]["tp"], 1)
        self.assertEqual(sweep(records, [0.1])[0]["fp"], 0)

    def test_conflicting_labels_fail(self):
        rows = [{"source": "a", "destination": "b", "timestamp": i, "label": "beacon" if i == 0 else "benign"} for i in range(8)]
        with self.assertRaises(ValueError): features(rows)


if __name__ == "__main__":
    unittest.main()
