# Author revision ledger after the frozen self-review

本记录是作者侧修订与验收台账，不是给期刊编辑的回复信，也不改写三份原始报告。所有修订保持同一机制、同一精确收入表达式和同一全局上界。报告中的源行号可在 submitted/ 的冻结稿件中核对，当前正文采用下表的节号与标签定位。

| 来源意见 | 已实施的修订 | 当前依据与验收 | 状态及剩余范围 |
|---|---|---|---|
| R1-M1、R2-M1、R3-M2 | 引言和 Discussion 区分一般凸性基础、具体容量支持、完整联合方向及本例限制；Section 6.6 展示 lambda 与真实单侧降价导数之差、双方积分收入和严格正总增益。 | `joint_residual_screening.tex` 的 trace-slack 与 J1/J2 段落；`joint_explanation_check.py` 独立积分通过。 | 已完成现有证据支持的意义阐释。超出本例的广泛科学影响和 Nature 定位仍需外部评价，没有用修辞宣称解决。 |
| R3-M1、R1-m2 | 新增 Section 6.4，集中列出 s0 与 s、冻结价格增量移植、共享选择次序、Q 菜单、彩票菜单、最后联合释放及支付积分；列出收入依赖表。 | `reference_specification.tex`；`reference_index.md` 的源码函数、边界与见证检查。 | 已补齐稳定数学入口和源定位，不需阅读历史研究日志。有限费用表仍由明确命名且哈希绑定的 JSON 指定，历史基准未伪装为新从头积分。 |
| R1-m1 | 明确两类条件定理的所有 residual 为 Borel；一般剩余值的分组恒等式仍允许原模型的联合可测机制。 | Section 6.1 的范围说明及 Theorems 7、8 的一般 r 陈述。 | 已修正奇异测度配对函数域；没有缩小被比较的 DSIC 随机化机制类。 |
| R1-m3 | 将彩票排除语句改为“完整松弛恒等式排除更高条件收入”，并明确不主张唯一性或全部取等机制分类。 | Section 6.3 末段。 | 已完成。 |
| R2-m1 | 给出同一完整报告空间上的共同非负容量测度接口，列明双方收入不等式、定义域、取等和容量饱和条件。 | Section 6.1 的 sufficient common-certificate interface。 | 已完成充分接口。没有声称存在、完备性、强对偶或最终机制已获共同证书。 |
| R2-m2、R3-m1 | 统一二维报告角色，区分彩票对齐方向和固定物理方向，并加入最终 F、Q、G、Eplus、W、S 范围表。 | Sections 6.4、6.5，Table 2；实际原始评估器的参数顺序和边界见 reference_index.md。 | 已完成。排除纤维没有被写成已证次优。 |
| R2-m3 | 解释零概率报告线为何通过全局激励相容约束正概率区域，线价格不表示线上正概率交易。 | Section 6.1。 | 已完成。 |
| R3-m2 | 说明上界封存文件中的旧 lower/gap 字段只描述历史比较；当前区间使用新 lower enclosure 与保留 upper。 | Section 7.5；`../v46_upper_source_identity.json`；主 README。 | 已完成。封存上界 8 个文件保持原字节身份，两套全遍历均在本轮通过。 |
| R3-m3 | 独立推导 D(h)=D+Ch+h²/2 和 R'(h)=1-3D(h)，说明 top/right traces 条件；给出实际 C>1 行。 | Section 6.6；`joint_explanation_check.md/.py`，t=7/10 的 exact fee change 检查。 | 已完成。所选 epsilon 与未证明的一般可行参数族严格区分。 |

## Additional archive consistency repairs

- 将 CFF schema version 保持为 1.2.0，发布版本更新为 1.3.0。YAML 解析及标题/版本一致性检查通过。
- 新下界入口逐项比较公开 manifest 的代数系数、对数项和收入区间与独立收入审计，修改后完整便携重放通过。
- 发布构建复制全部 TeX 输入文件，并在必要时增加交叉引用稳定性编译。最终 PDF 保留八个主要章节。
- 新增作者侧 joint explanation checker 的归档副本使用显式非优化运行保护，默认只读。其数值与证明公式未改动。

## Verification boundary

新增说明所用的精确作者核查独立重建完整菜单多边形、收费单项式积分和彩票积分的局部留数，不导入源验证器。它另算的 J1、J2 和 J 与现有证书一致。此检查不是第四份评阅报告，也没有向原评阅者反馈汇总后再征求一致意见。

完整历史基准的第二套从零连续积分、任意分布的推广、最优机制分类和匹配全局证书仍未完成。当前主张始终是显式可行机制、严格小于 0.01 的证书区间和指定残余上的完整随机化条件定理。
