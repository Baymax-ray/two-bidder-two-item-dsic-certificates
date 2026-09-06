# 审后修订与验收台账

本轮保留原稿八个主要章节、旧证书及所有冻结审稿报告。仅调整现行证明导航、贡献表述、复现范围与发布验证辅助代码；数学端点和原研究分支源文件不变。

| 意见 | 作者修订 | 位置与验收 |
|---|---|---|
| R1-M1、R2-M1 | 新审计 helper 默认在内存比较 JSON，依赖名称改为镜像内稳定相对路径；仅显式 --write 生成文件。保留最终暂存输入不变断言。 | [修复说明](../v4611_v462/portability_correction.md)。修复后两次不同临时根的完整运行均退出 0、46/46 通过并完成最终身份与端点核对，分别耗时 763.647 和 604.843 秒；见 [第二次报告](../v4611_v462/second_corrected_replay/validation_report.md)。 |
| R3-M1 | 给出旧 Pi0 的 charged inequality 与空机制等号，明确 H1=H2=0 已由旧 stream argument 得到。新增内容定位为严格减少总价格及替换/IC 环兼容性。同步摘要、引言、贡献、讨论、README 和 CITATION.cff。 | manuscript/common_capacity_upper.tex 中 “What is improved relative to the stream measure”；manifest 数值未变。 |
| R2-m1 | 逐项写明 B20 两份完整遍历、Delta1024 一份完整累计与有限独立交叉检查、后者的共享函数、IC 环整盒符号与精确减量。收窄摘要和发布文档的概括。 | manuscript/common_capacity_upper.tex 与 manuscript.tex 的复现段；verification/README.md；根 README 与 CITATION.cff。 |
| R1-m1、R2-m2、R3-m1 | 旧收入证明指向保留的 V4.6 下界，现行下界另指 functional-exchange 命题；仍未得到的是匹配候选的共同证书。 | manuscript/joint_residual_screening.tex。作者已在盲审运行期间发现并修正，原审稿意见保持原样。 |
| R1-m2、R3-m2 | 新单买方收入改为 R_SB，保留旧双买方基准 R0 的记号。 | manuscript/common_capacity_upper.tex reusable conditional inequality。 |
| R2-m3 | 增加三来源表：约 0.00138972521893 的包围改进、约 0.00144551594101 的条件替换、精确 8.1e-9 的 IC 环减量。明确 IC 环当前数值贡献小。 | manuscript/common_capacity_upper.tex 的上界减量表及根 README。作者用 manifest 的 Fraction 值独立核对所报舍入与分解。 |
| R3-m3 | 主定理后增加四行现行证明路线表；注明历史收益层不是现行 R* 的定义，并用一句话解释固定另一买方时的条件最优不排除联合变化。 | manuscript/manuscript.tex 的 active-roadmap 表与随后说明。 |

## 验收边界

旧审稿包的 230 项身份与本轮 404 项冻结身份均以重构方式保存。三份报告在解封前分别冻结，REPORTS_SHA256SUMS 绑定其原始字节。审稿记录中的失败是对当时冻结版本的真实结果，不能被修复后的通过记录覆盖。

修订后 32 页 PDF 已干净编译并逐页检查；无 overfull box、未定义引用或可见裁切。两处临时根的完整修复后复现均通过，第二次对 162 项包内文件的前后身份、156 项源绑定和 149 项依赖绑定全部核对。最初因 Windows 工作目录过长而在 0/46 处退出的尝试另外保留，它不算作完整通过运行。发布验证通过公开 runner 的现行精确断言组合本轮已执行且源身份未变的 13 组数学结果，再核对文本、冻结包、编译和全文件散列；这个组合验收不冒充一次额外完整数学重跑。

## 最终验收结果

本台账所列 11 个意见 ID 均已完成对应修订与范围限定。R1-M1/R2-M1 的两个不同临时位置全量验收通过；其余意见通过直接证明说明、精确表格算术、交叉引用检查与 PDF 检查落实，没有把额外未执行实验列为已完成。

公开验证断言已接受本轮 13 组新执行且源身份未变的组件结果，旧 230 项/本轮 404 项证据包与三份报告身份、端点与文稿一致性、干净编译及发布散列覆盖均通过。见 [发布验收记录](../v4611_v462/publication_validation.txt) 和 [最终验收摘要](../v4611_v462/final_acceptance.json)。

开放问题不因这些修订关闭：无限制最优机制、确切最优值、匹配证书、跨实例推广性和文献优先权仍未得到确认。
