# Detection Threshold Lab：可复现使用案例

作者：LLR6

## 要解决的场景

用带标签的合成时间序列比较周期检测阈值，直接查看误报、漏报和每个实体对的间隔证据。适合检测工程入门、阈值敏感性实验和指标教学。

## 复现

先克隆仓库并进入根目录，Python 3.10+。

```bash
python -m pip install -e .
detection-lab simulate --seed 7 --groups 20 --output demo.csv
detection-lab evaluate demo.csv --thresholds 0.05,0.1,0.2,0.3,0.5 --output demo.json
```

这份[公开输出](../examples/showcase/output.json)由仓库源码实际运行产生，未手工修改。对应源码提交：`c3491548c7aafbab23421310d32f2502e8aacf08`。输入为仓库自带示例生成器的 seed 7、20 组、默认 12 个样本/组，没有使用用户真实日志。

## 结果怎么看

本次 seed 7 的 **20 组合成样本**：阈值 0.05 时 TP=8 / FP=0 / FN=2；阈值 0.30 时 TP=10 / FP=2 / FN=0。多检出两组的同时多误报两组。完整报告包含指标、Pareto 候选与逐组证据；这些结果不是实际网络准确率。

| 你的场景 | 可以先试什么 |
| --- | --- |
| 想理解 Precision 与 Recall 的取舍 | 同一批样本扫描多个 CV 阈值 |
| 某个随机种子的结果特别好 | 用 replicate 比较多个种子的均值与波动 |
| 只看指标，解释不了具体判定 | 回查逐组事件数、时间范围和 CV |

## 换成自己的输入

准备 timestamp,source,destination,label 列的有标签 CSV，再执行 evaluate。若没有可靠标签，不能计算可信的误报/漏报指标。

## 有用的反馈

提交最小可复现输入、实际输出与预期行为。日志请先去敏；明确误报或遗漏发生在哪一行。详细能力边界和输入要求见 [README](../README.md)。
