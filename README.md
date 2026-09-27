# Detection Threshold Lab 🔬

> 周期外联检测的 CV 阈值到底该设多少？在**带标签的合成流量**里扫一遍阈值，直接看 TP / FP / TN / FN、精确率、召回率和逐实体证据。

```bash
python -m pip install -e .
detection-lab simulate --seed 7 --groups 20 --output demo.csv
detection-lab evaluate demo.csv --thresholds 0.05,0.1,0.2,0.3,0.5 --output report.json
```

输入 CSV 列：`timestamp,source,destination,label`，标签只允许 `beacon` 或 `benign`。按 `(source, destination)` 分组，对正时间间隔计算变异系数 `CV = population_std(intervals) / mean(intervals)`，`CV <= threshold` 判为周期候选。合成样本特意混入有抖动的 beacon 和周期性正常任务，让阈值变化出现真实的误报/漏报取舍。报告保留每组的样本数、平均间隔、CV 和时间范围。

## 为什么做它

“低抖动 = 可疑”很容易写成规则，却很难讨论阈值的代价。这个小实验把漏报与误报摊在同一张表里，便于交流**检测方法的边界**。如果用于真实数据，需先完成合法采集和人工标注，再评估业务周期任务、代理、CDN 等正常行为。

## 限制

- 合成数据是演示，不代表真实网络环境，也不能证明某阈值普适有效。
- 同一实体对标签冲突会报错；事件数不足会排除，报告明确列出排除规则。
- 它不是 C2 判定器，不抓包、不扫描、不访问网络。测试：`python -m unittest discover -s tests`。

后续方向：时间窗口、随机抖动分布、标签不平衡数据集和与 NightWatch 规则对照。欢迎提交**去敏且有标注**的数据生成器或误报案例。

作者：LLR6 · MIT License
