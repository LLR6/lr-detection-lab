import unittest
from detection_lab.cli import features, pareto_frontier, simulate, sweep


class DetectionTests(unittest.TestCase):
    def test_seed_reproducible(self):
        self.assertEqual(simulate(3), simulate(3))
        self.assertNotEqual(simulate(3), simulate(4))

    def test_threshold_counts(self):
        records = [{"cv": 0.01, "label": "beacon"}, {"cv": 0.7, "label": "benign"}]
        self.assertEqual(sweep(records, [0.1])[0]["tp"], 1)
        self.assertEqual(sweep(records, [0.1])[0]["fp"], 0)

    def test_metrics_include_f1_and_balanced_accuracy(self):
        row = sweep(
            [
                {"cv": 0.01, "label": "beacon"},
                {"cv": 0.02, "label": "beacon"},
                {"cv": 0.03, "label": "benign"},
                {"cv": 0.9, "label": "benign"},
            ],
            [0.1],
        )[0]
        self.assertEqual(row["precision"], 0.6667)
        self.assertEqual(row["recall"], 1.0)
        self.assertEqual(row["specificity"], 0.5)
        self.assertEqual(row["f1"], 0.8)
        self.assertEqual(row["balanced_accuracy"], 0.75)

    def test_pareto_frontier_drops_dominated_threshold(self):
        points = [
            {"threshold": 0.1, "recall": 0.8, "false_positive_rate": 0.0},
            {"threshold": 0.2, "recall": 0.8, "false_positive_rate": 0.2},
            {"threshold": 0.3, "recall": 1.0, "false_positive_rate": 0.2},
        ]
        self.assertEqual(
            [x["threshold"] for x in pareto_frontier(points)],
            [0.1, 0.3],
        )

    def test_conflicting_labels_fail(self):
        rows = [{"source": "a", "destination": "b", "timestamp": i, "label": "beacon" if i == 0 else "benign"} for i in range(8)]
        with self.assertRaises(ValueError): features(rows)


if __name__ == "__main__":
    unittest.main()
