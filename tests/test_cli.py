import json
import tempfile
import unittest
from pathlib import Path

from detection_lab.cli import features, main, pareto_frontier, replicate, simulate, sweep


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

    def test_replicate_aggregates_multiple_seeds(self):
        report = replicate([1, 2, 3], 20, 12, [0.1, 0.2])
        self.assertEqual(report["schema"], "lr-detection-lab-replicate/v1")
        self.assertEqual(len(report["runs"]), 3)
        self.assertEqual(len(report["aggregate"]), 2)
        self.assertEqual(report["aggregate"][0]["runs"], 3)
        self.assertIn("mean", report["aggregate"][0]["recall"])
        self.assertIn("pstdev", report["aggregate"][0]["recall"])

    def test_cli_simulate_evaluate_and_replicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_path = root / "demo.csv"
            eval_path = root / "evaluation.json"
            rep_path = root / "replicate.json"

            self.assertEqual(
                main(["simulate", "--seed", "3", "--groups", "6", "--samples", "8", "--output", str(csv_path)]),
                0,
            )
            self.assertTrue(csv_path.exists())

            self.assertEqual(
                main(["evaluate", str(csv_path), "--thresholds", "0.1,0.2", "--output", str(eval_path)]),
                0,
            )
            evaluation = json.loads(eval_path.read_text(encoding="utf-8"))
            self.assertEqual(evaluation["schema"], "lr-detection-lab/v2")
            self.assertEqual(len(evaluation["sweep"]), 2)

            self.assertEqual(
                main([
                    "replicate",
                    "--seeds", "1,2",
                    "--groups", "6",
                    "--samples", "8",
                    "--thresholds", "0.1,0.2",
                    "--output", str(rep_path),
                ]),
                0,
            )
            replicate_report = json.loads(rep_path.read_text(encoding="utf-8"))
            self.assertEqual(replicate_report["seeds"], [1, 2])

    def test_cli_rejects_invalid_simulation_size(self):
        with self.assertRaises(SystemExit) as ctx:
            main(["simulate", "--groups", "1"])
        self.assertEqual(ctx.exception.code, 2)

    def test_cli_rejects_bad_replicate_threshold(self):
        with self.assertRaises(SystemExit) as ctx:
            main(["replicate", "--thresholds", "3.0"])
        self.assertEqual(ctx.exception.code, 2)

    def test_conflicting_labels_fail(self):
        rows = [{"source": "a", "destination": "b", "timestamp": i, "label": "beacon" if i == 0 else "benign"} for i in range(8)]
        with self.assertRaises(ValueError):
            features(rows)


if __name__ == "__main__":
    unittest.main()
