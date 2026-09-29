# Metrics and Threshold Selection

Detection Threshold Lab 不输出“唯一最佳阈值”。真实检测系统中的阈值取舍依赖误报成本、漏报成本、调查能力和业务背景。

## Metrics

每个阈值都会输出：

- **TP / FP / TN / FN**：混淆矩阵基础计数。
- **Precision**：被判为 beacon 的组中，真正 beacon 的比例。
- **Recall**：真实 beacon 中，被检测出的比例。
- **False Positive Rate**：正常组被误报的比例。
- **Specificity**：正常组被正确排除的比例。
- **F1**：Precision 与 Recall 的调和平均。
- **Balanced Accuracy**：Recall 与 Specificity 的平均值。
- **Youden's J**：Recall - FPR。

不同指标回答的问题不同，因此不能脱离场景只比较一个数字。

## Pareto frontier

v2 报告增加 `pareto_frontier`。

一个阈值如果同时满足：

- 没有另一个阈值拥有更高或相同 Recall；
- 同时另一个阈值拥有更低或相同 FPR；
- 且至少一个维度严格更好；

那么它不会被该点支配。

Pareto frontier 的意义是缩小候选范围，而不是自动做业务决策。

## Example interpretation

假设：

| Threshold | Recall | FPR |
|---:|---:|---:|
| 0.10 | 0.80 | 0.00 |
| 0.20 | 0.80 | 0.20 |
| 0.30 | 1.00 | 0.20 |

0.20 被 0.10 支配：Recall 没提高，FPR 却更高。

0.10 与 0.30 都可能留在 frontier 上，因为它们代表“零误报但漏检”与“更高召回但接受误报”的不同取舍。

## Limitations

当前示例是小规模合成数据。它适合验证实验管线和理解阈值行为，不应被当成真实网络的效果证明。真实评估还需要：

- 去敏真实流量；
- 可靠标签；
- 时间切分；
- 类别不平衡；
- 多种正常周期任务；
- 不同 jitter 分布；
- 按环境分别校准。
