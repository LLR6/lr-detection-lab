import argparse
import csv
import json
import random
import statistics
from collections import defaultdict
from pathlib import Path


FIELDS = ("timestamp", "source", "destination", "label")


def simulate(seed: int = 7, groups: int = 20, samples: int = 12) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    for group in range(groups):
        label = "beacon" if group % 2 == 0 else "benign"
        timestamp = float(group * 10000)
        for _ in range(samples):
            if label == "beacon":
                timestamp += 30 + rng.uniform(-12, 12) if group % 5 == 0 else 30 + rng.uniform(-2, 2)
            else:
                timestamp += 30 + rng.uniform(-8, 8) if group % 5 == 1 else rng.expovariate(1 / 30)
            rows.append({"timestamp": round(timestamp, 3), "source": f"host-{group:02d}",
                         "destination": "example.test:443", "label": label})
    return rows


def read_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not set(FIELDS) <= set(reader.fieldnames or []):
            raise ValueError(f"CSV 必须包含列：{', '.join(FIELDS)}")
        rows = []
        for row in reader:
            timestamp = float(row["timestamp"])
            if row["label"] not in ("beacon", "benign"):
                raise ValueError("label 只能为 beacon 或 benign")
            rows.append({**row, "timestamp": timestamp})
        return rows


def features(rows: list[dict], min_events: int = 6) -> list[dict]:
    groups = defaultdict(list)
    labels = defaultdict(set)
    for row in rows:
        key = (row["source"], row["destination"])
        groups[key].append(float(row["timestamp"]))
        labels[key].add(row["label"])
    result = []
    for key in sorted(groups):
        if len(labels[key]) != 1:
            raise ValueError(f"同一实体对存在冲突标签：{key}")
        times = sorted(groups[key])
        if len(times) < min_events:
            continue
        intervals = [b - a for a, b in zip(times, times[1:]) if b > a]
        if len(intervals) < min_events - 1:
            continue
        mean = statistics.mean(intervals)
        result.append({"source": key[0], "destination": key[1], "label": next(iter(labels[key])),
                       "events": len(times), "mean_interval": round(mean, 4),
                       "cv": round(statistics.pstdev(intervals) / mean, 6),
                       "first_timestamp": times[0], "last_timestamp": times[-1]})
    return result


def sweep(records: list[dict], thresholds: list[float]) -> list[dict]:
    results = []
    for threshold in thresholds:
        tp = fp = tn = fn = 0
        for row in records:
            predicted = row["cv"] <= threshold
            positive = row["label"] == "beacon"
            if predicted and positive: tp += 1
            elif predicted: fp += 1
            elif positive: fn += 1
            else: tn += 1
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        false_positive_rate = fp / (fp + tn) if fp + tn else None
        specificity = tn / (tn + fp) if tn + fp else None
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision is not None and recall is not None and precision + recall
            else None
        )
        balanced_accuracy = (
            (recall + specificity) / 2
            if recall is not None and specificity is not None
            else None
        )
        youden_j = (
            recall - false_positive_rate
            if recall is not None and false_positive_rate is not None
            else None
        )
        results.append({
            "threshold": threshold,
            "tp": tp,
            "fp": fp,
            "tn": tn,
            "fn": fn,
            "precision": round(precision, 4) if precision is not None else None,
            "recall": round(recall, 4) if recall is not None else None,
            "false_positive_rate": round(false_positive_rate, 4) if false_positive_rate is not None else None,
            "specificity": round(specificity, 4) if specificity is not None else None,
            "f1": round(f1, 4) if f1 is not None else None,
            "balanced_accuracy": round(balanced_accuracy, 4) if balanced_accuracy is not None else None,
            "youden_j": round(youden_j, 4) if youden_j is not None else None,
        })
    return results


def pareto_frontier(points: list[dict]) -> list[dict]:
    """Return thresholds not dominated on recall (higher) and FPR (lower)."""
    usable = [
        p for p in points
        if p.get("recall") is not None and p.get("false_positive_rate") is not None
    ]
    frontier = []
    for point in usable:
        dominated = any(
            other is not point
            and other["recall"] >= point["recall"]
            and other["false_positive_rate"] <= point["false_positive_rate"]
            and (
                other["recall"] > point["recall"]
                or other["false_positive_rate"] < point["false_positive_rate"]
            )
            for other in usable
        )
        if not dominated:
            frontier.append(point)
    return sorted(frontier, key=lambda x: (x["false_positive_rate"], -x["recall"], x["threshold"]))


def replicate(seeds: list[int], groups: int, samples: int, thresholds: list[float], min_events: int = 6) -> dict:
    runs = []
    by_threshold = defaultdict(list)
    for seed in seeds:
        records = features(simulate(seed, groups, samples), min_events)
        result = sweep(records, thresholds)
        runs.append({"seed": seed, "evaluated_groups": len(records), "sweep": result})
        for row in result:
            by_threshold[row["threshold"]].append(row)

    aggregate = []
    metric_names = ("precision", "recall", "false_positive_rate", "specificity", "f1", "balanced_accuracy", "youden_j")
    for threshold in thresholds:
        rows = by_threshold[threshold]
        summary = {"threshold": threshold, "runs": len(rows)}
        for metric in metric_names:
            values = [row[metric] for row in rows if row.get(metric) is not None]
            summary[metric] = {
                "mean": round(statistics.mean(values), 4) if values else None,
                "pstdev": round(statistics.pstdev(values), 4) if values else None,
                "min": min(values) if values else None,
                "max": max(values) if values else None,
            }
        aggregate.append(summary)

    return {
        "schema": "lr-detection-lab-replicate/v1",
        "seeds": seeds,
        "groups": groups,
        "samples": samples,
        "min_events": min_events,
        "thresholds": thresholds,
        "aggregate": aggregate,
        "runs": runs,
        "note": "Synthetic repeated-run stability report; not a production-network performance claim.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="周期外联检测阈值实验，不访问网络")
    sub = parser.add_subparsers(dest="action", required=True)
    sim = sub.add_parser("simulate", help="生成可复现的标注合成 CSV")
    sim.add_argument("--seed", type=int, default=7)
    sim.add_argument("--groups", type=int, default=20)
    sim.add_argument("--samples", type=int, default=12, help="events per synthetic entity pair")
    sim.add_argument("--output", default="demo.csv")
    ev = sub.add_parser("evaluate", help="按实体对计算 CV 并扫阈值")
    ev.add_argument("csv")
    ev.add_argument("--thresholds", default="0.05,0.1,0.2,0.3,0.5")
    ev.add_argument("--min-events", type=int, default=6)
    ev.add_argument("--output", help="JSON 报告路径；不填则打印到 stdout")
    rp = sub.add_parser("replicate", help="跨多个随机种子重复合成实验并统计稳定性")
    rp.add_argument("--seeds", default="1,2,3,4,5")
    rp.add_argument("--groups", type=int, default=20)
    rp.add_argument("--samples", type=int, default=12)
    rp.add_argument("--thresholds", default="0.05,0.1,0.2,0.3,0.5")
    rp.add_argument("--min-events", type=int, default=6)
    rp.add_argument("--output")
    args = parser.parse_args(argv)
    if args.action == "simulate":
        if args.groups < 2: parser.error("--groups 至少为 2")
        if args.samples < 3: parser.error("--samples 至少为 3")
        with open(args.output, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(simulate(args.seed, args.groups, args.samples))
        print(f"已写入 {args.output}；随机种子 {args.seed}")
        return 0
    if args.action == "replicate":
        try:
            seeds = [int(x) for x in args.seeds.split(",")]
            thresholds = [float(x) for x in args.thresholds.split(",")]
            if not seeds or len(set(seeds)) != len(seeds):
                raise ValueError("seeds 不能为空且不能重复")
            if args.groups < 2 or args.samples < 3 or args.min_events < 3:
                raise ValueError("groups 至少 2，samples/min-events 至少 3")
            if not thresholds or any(not 0 <= x <= 2 for x in thresholds):
                raise ValueError("阈值须在 0..2 之间")
            report = replicate(seeds, args.groups, args.samples, thresholds, args.min_events)
        except ValueError as exc:
            parser.error(str(exc))
        result = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output: Path(args.output).write_text(result + "\n", encoding="utf-8")
        else: print(result)
        return 0
    try:
        thresholds = [float(x) for x in args.thresholds.split(",")]
        if not thresholds or any(not 0 <= x <= 2 for x in thresholds) or args.min_events < 3:
            raise ValueError("阈值须在 0..2 之间，min-events 至少为 3")
        records = features(read_csv(args.csv), args.min_events)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    sweep_result = sweep(records, thresholds)
    report = {
        "schema": "lr-detection-lab/v2",
        "dataset": Path(args.csv).name,
        "evaluated_groups": len(records),
        "excluded_note": "少于 min-events 或非正间隔的组不参与评估",
        "sweep": sweep_result,
        "pareto_frontier": pareto_frontier(sweep_result),
        "metric_note": "Pareto frontier maximizes recall while minimizing false-positive rate; it is not an automatic best-threshold recommendation.",
        "evidence": records,
    }
    result = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output: Path(args.output).write_text(result + "\n", encoding="utf-8")
    else: print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
