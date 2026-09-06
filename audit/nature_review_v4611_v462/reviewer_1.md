# Reviewer 1

## Review setup

- **Input scope** 冻结评审包中的完整英文稿，包括 `manuscript.tex` 及其四个 TeX 输入、README、所引的现行机制结构证明、收入推导、条件筛选证明、共同支持证明和相关验证代码。本报告按预先指定的完整机制、逐点及连续域证明、条件筛选重点独立完成。
- **Assessment boundary** 本次是内部模拟审稿。没有阅读其他评审报告、共同问题清单或评审包之外的作者审计结论，没有编辑稿件或证书源文件。五项评估标准来自同一冻结包中的 Nature 本地标准文本。没有在线查证优先权、公开仓库状态或外部机制的未舍入收入。
- **Shared manuscript claim summary** 稿件给出一个完整随机机制，证明其逐点 DSIC、ex-post IR 和联合可行性，并得到精确收入 $R_*=0.876464164471798\ldots$。共同容量价格对不限制分配范围的随机机制给出 $U_*=0.882923053258716\ldots$，两端差距小于 $0.006459$，构造收入超过最优收入的 $99.2684\%$。Q、E 和翼部区域的条件筛选结论固定实际剩余容量，其覆盖率不是全局差距关闭比例。稿件明确保留最优机制和匹配证书问题。
- **Visible evidence base** 下文行号均对应冻结包的源文件，缩写根目录为 `review_packet/archive/`。本评审另外在独立 `reviewer_1_work` 镜像中重放六个指定数学入口，并检查镜像与冻结输入的身份；这些新检查记录只属于本评审。
- **Missing materials affecting confidence** 本次没有重新执行两套完整上界树遍历，也没有做外部文献全文优先权审计。上界遍历的全量运行结论仍是评审包提供的证据，不能改称本评审的新全量重放。没有发现应当凭空补设的统计、实验、临床或伦理要求。

## Overall assessment

稿件清楚说明了现行数学主张的范围。它不仅给出一个收入数字，还说明每个真实报告及平局上如何选出兼容的菜单最大化选项，并把条件最优性、共同价格有效性和整个拍卖达到等号区分开。就本次读到的全实数证明及所做的局部精确重放而言，没有找到足以推翻现行机制可行性、Q/E/翼部筛选定理或所列代数收入的反例或证明缺口。

但可携带复现入口存在一个已定位并局部重现的矛盾。它把包含绝对运行路径的生成 JSON 同时当作不可改变的冻结输入，导致最终镜像身份检查无法满足。R1-M1 是必须修复的重大复现问题。该问题没有改变此次重算的数学数值，因此我不将其标记为阻断数学主结论的缺陷。若用于投稿，需要先让复现承诺与实际代码行为一致。

## Who would be interested in the results, and why

多维机制设计、算法博弈论、连续优化及计算机辅助数学证明的研究者会关心这些结果。前两类读者得到一个接近当前证书上界的显式机制，以及能排除某些单边改进方向的条件筛选定理。后两类读者会关心如何将连续域的弱对偶论证、精确代数收入、奇异报告线上的激励限制和有限整数遍历连接起来。对更广泛科学读者，最容易说明的结论是，在这个特定拍卖模型中，一个明确可执行的机制已获得至少约 $99.27\%$ 的最优收入保证；目前材料没有建立更大拍卖、其他分布或实际市场上的相应结论。

## Major strengths

1. **完整机制与逐点证明相互对应。** [现行机制规则](D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/manuscript/functional_exchange_mechanism.tex:20) 第 20 至 76 行把跳跃、广义逆平台、菜单区域、方向规则和联合平局选择逐项写出。其 source-bound research_log/refined_structure_audit.md 第 197 至 330 行分别处理 Q/base、Q/Q、E/base、E/Q、E/E，并说明报告依赖的联合平局选择为何仍满足 DSIC。尤其是平台上只使用广义逆的两个蕴含关系，没有误用 $h(k(t))=t$。

2. **E 面上的修复针对任意可行竞争机制。** 同一结构证明第 403 至 474 行承认新参数 $a>A$ 时，旧的字面零容量面可能失效。它先用邻接开矩形的占用得到效用沿水平方向恒定，再以 Lipschitz 连续性和双向次梯度比较推出该面上的选定边际为零。这一论证覆盖异常次梯度，且没有把仅对实际剩余容量成立的推论推广为任意容量扰动的支持价格。正文 `functional_exchange_mechanism.tex` 第 189 至 198 行准确概括了这个区别。

3. **翼部筛选给出真实的全类上界。** `functional_exchange_mechanism.tex` 第 200 至 252 行以及 `research_log/residual_wing_screening.md` 第 16 至 114 行保留任意竞争效用的原点租金。占用约束使该效用在无销售区域恒定，并将左边界租金转为整条带上的积分。系数非负且候选分配饱和，因而有限菜单只是等号实例。源证明第 159 至 258 行另行检查实际机制的占用、方向和 $p=1$ 情形，没有用有限报告抽查代替这些连续论证。

4. **收入计算包括容易漏掉的整块区域。** `research_log/refined_revenue_audit.md` 第 174 至 293 行单独计入广义逆的平台、$A<t<a$ 上负的 E 替换项及新增收费带。其第 94 至 133 行重新积分完整基准菜单，并处理单品价格超过一的需求拓扑。本次重放该收入审计及第三套完整积分均返回相同代数收入区间，未把历史基值加上一个新增量冒充完整新积分。

5. **对偶与最优性界限陈述克制。** `common_capacity_upper.tex` 第 74 至 99 行从适用于每个完整单边机制的不等式证明两个收费筛选值为零，明确指出空机制达到该收费目标并不产生拍卖等号。第 155 至 186 行将四种机制松弛与积分证书余量分开，且正松弛只否定当前机制与当前价格的匹配，不证明机制本身次优。这些区别直接支持主定理的有限范围。

## Major Concerns

### R1-M1

- **Concern ID** R1-M1
- **Severity** Major
- **Blocking** No
- **Axis** technical soundness 的 reproducibility 分项
- **claim_pointer** 稿件声称主动证书在密封临时镜像中执行 46 个数学入口，并且重放后复制的证明输入不变，支持离开原研究工作区的复现。定位于 `manuscript/manuscript.tex` 第 939 至 954 行及 `certificate/coordinated_primal_dual/README.md` 第 5 行的复现说明。
- **evidence_pointer** `certificate/coordinated_primal_dual/verify_coordinated.py` 第 42 至 53 行；同目录 `entrypoints.json` 第 142 至 143 行；`source_bindings.json` 第 25 至 27 行；`source/V4_6_1_1_V4_6_2_archive_audit/upper/fresh_support_latest_flatness.py` 第 148 至 150 行。新复现证据位于外层审计目录 `reviewer_1_work/bounded_replay.json` 与 `reviewer_1_work/staged_input_identity.json`。
- **Concern** 最后一个入口无条件重写 `fresh_support_latest_flatness.json`，其 `source_sha256` 字段使用 `str(p)` 作为键，因而保存绝对运行路径。同一个 JSON 又被列入冻结源绑定。临时镜像路径与冻结记录中的原工作区路径必然不同，而 wrapper 第 52 行要求重放后的整个文件 SHA256 与冻结值完全相同。本次按照 wrapper 的绑定和目录映射装载镜像，六个选定数学入口均退出为零；随后只有该 JSON 发生变化，唯一不同的顶层字段就是 `source_sha256`。因此，完整 wrapper 即使通过全部数学入口，也会在所示最终身份检查上失败。这是从已执行的相关入口和同一身份比较规则得到的确定性结论，本次没有假称已执行全部 46 个入口。
- **Why it matters** 密封、可携带的精确复现是论文明确承诺的重要交付物。运行路径变化不应触发“证明输入改变”的失败，也不应让用户误以为数学重算不一致。此次其余数值字段一致，且原冻结包的 156 个源文件与 149 个依赖文件在检查前后身份均通过，因此这里没有证据表明机制、收入或严格松弛数值错误。故标记为重大但非阻断数学主结论。
- **Resolution test** 将证明输入身份与运行环境元数据分离，或使生成记录使用稳定的相对源标识，并按真实需要决定该 JSON 是冻结输入还是生成输出。随后从至少两个不同临时目录完整运行支持入口，确认 46 个数学入口、最终源身份检查和端点协调均成功，原归档文件保持不变。不能只删除最后的身份检查来掩盖输入与输出角色混用。

## Minor Comments

### R1-m1

- **Concern ID** R1-m1
- **Severity** Minor
- **Axis** readability for nonspecialists 与 writing-clarity
- **Affected element** 历史 V4.6 下界段落对现行主定理的回指。
- **claim_pointer** `joint_residual_screening.tex` 第 492 行称其证明了 Theorem `thm:bracket` 的下界主张。
- **evidence_pointer** 同文件第 484 至 495 行只得到 $R_J$ 位于 $0.8758198541484224553460$ 与 $0.8758198541484224553461$ 之间；`manuscript.tex` 第 187 至 208 行的现行主定理则以更大的 $R_*$ 为下界，来自后续 `functional_exchange_mechanism.tex` 第 78 至 142 行。
- **Issue** 历史结果本身可用，但该句不能按字面证明现行定理中更强的下界。上下文已有历史标识，且后文提供了正确现行证明，所以这是局部交叉引用错误，不是现行下界缺证。
- **Required correction** 将回指改为“证明所保留的 V4.6 下界及其与历史 stream 上界构成的区间”，或者明确指向后续现行机制命题才完成的主定理下界。

### R1-m2

- **Concern ID** R1-m2
- **Severity** Minor
- **Axis** readability for nonspecialists 与 writing-clarity
- **Affected element** $R_0$ 的两种收入含义。
- **claim_pointer** `manuscript.tex` 第 479 至 486 行把 $R_0$ 定义为双买方 affine 基准的收入；`common_capacity_upper.tex` 第 35 至 36 行又用 $R_0$ 表示单买方全容量菜单的收入。
- **evidence_pointer** 两处数值分别是 $26232089810531183/30000000000000000$ 和 $4/9+2\sqrt2/27$。`manuscript.tex` 第 520 至 543 行还把前一个 $R_0$ 用于收入分解。
- **Issue** 两个对象在同一篇稿件中都作为后续算式的基准值出现，没有显式说明符号重新局部定义。专门读者能从数值还原含义，但对照下界收入与共同支持质量时容易混淆。
- **Required correction** 为单买方菜单值使用单独符号，例如 $R_{\rm SB}$，并在共同支持质量和减项推导中保持一致。

## Technical failings that need to be addressed before the case is established

目前没有定位到需要标为 Blocking Yes 的数学缺陷。完整机制、连续收入和条件筛选的证据链在本次重点检查范围内成立。R1-M1 必须在“可携带且全部输入不变的完整复现”这一交付主张成立前修复；R1-m1 和 R1-m2 应在提交前清理。未亲自重跑全上界遍历是本评审的验证边界，不应转化为作者未提供上界遍历证据的指控。

本次新执行的有限范围检查如下。镜像材料严格来自同一冻结包。

| 检查 | 结果与范围 |
|---|---|
| `refined_structure_audit.py` | 退出码 0，2,209 个报告组合、188 个源实现对照报告；连续量词另由结构证明承担 |
| `residual_wing_screening.py` | 退出码 0，168 个恒等式检查、12,220 个实际报告检查，翼部面积 $438867/2500000$ |
| `refined_revenue_audit.py` | 退出码 0，完整收入及 45 个菜单面积检查通过 |
| `third_revenue_and_pairing.py` | 退出码 0，完整收入三项系数与端点区间相符，比例下界为 $0.9926846526851006\ldots$；此入口不重新遍历上界树 |
| `independent_structure_identities.py` | 退出码 0，22 个结构恒等式检查通过 |
| `fresh_support_latest_flatness.py` | 退出码 0，共同支持质量及最新机制整盒严格松弛检查通过；同时重现 R1-M1 的路径元数据变更 |
| 冻结输入及镜像身份 | 原包 156 个源文件和 149 个依赖身份检查前后通过；镜像只有上述生成 JSON 的 `source_sha256` 改变 |

初次镜像创建遇到 Windows 长路径限制，使用扩展长度路径后完成上述检查。该本评审工作目录较长造成的环境问题不列为稿件缺陷。

## Assessment against Nature-style criteria

| 标准 | 评估 |
|---|---|
| Originality | 以所供材料判断，完整跳跃交换、针对实际占用的条件筛选恒等式、相容共同价格及精确端点构成具体研究贡献。稿件第 122 至 159 行认真区分既有凸效用和对偶基础。没有外部全文检索，不能认定优先权或首次出现。 |
| Scientific importance | 对这个经典且困难的特定实例，显式机制与小于 $0.006459$ 的可证明区间有明确领域内价值。最优机制未被刻画，方法对其他分布或规模的效力尚未建立，因此现有材料主要支持专门领域内的推进，尚不足以据此断言杰出的广泛科学影响。 |
| Interdisciplinary readership | 连续优化、经济理论和形式化验证附近的读者可能受益，但稿件目前没有证明这些技术已改变其他学科的研究结论。可迁移兴趣是合理预期，不是已验证应用。 |
| Technical soundness | 重点证明区分逐点菜单选择与几乎处处积分，注意异常面、原点租金和固定容量条件。此次新重放支持现行收入及结构恒等式。R1-M1 暴露的是归档复现接口与身份约束矛盾，不能据此将已通过的数学数值称为错误。 |
| Readability for nonspecialists | 摘要给出收入保证并明确开放问题，正文解释零概率报告线为何有激励作用，这些做得较好。主文在现行机制前铺陈很长的历史构造，参数和收入符号多次变化，会增加读者追踪成本。R1-m1、R1-m2 是可明确修正的局部问题；若面向广泛读者，现行主定理与其四条证明依赖应比版本沿革更早出现。 |

## Recommendation posture

建议先完成一轮实质性复现修订，再将论文作为连续机制设计和精确证书研究送交专业评议。现有材料支持认真讨论其领域内技术价值；它没有给出足以让我确认 Nature 广泛科学重要性的证据。本报告不替代编辑决定，也不要求作者为了期刊定位将有界结论改写为一般最优性定理。

## Risk / unsupported claims

- 本次六个入口的成功不等于新运行完整 46 个入口，也不等于对整个归档作了第二次全量证明。
- $64.1627\%$ 是固定实际剩余容量时已解决的对手报告区域面积，不是已关闭的收入差距比例。
- 两个收费筛选值为零及当前机制对当前价格有正松弛，分别不能推出最优拍卖已找到或当前机制次优。
- 所供外部 GemNet 收入是舍入值。当前精确收入超过所印数字不能判定超过其未舍入收入。
- 没有证据将内部 AI 辅助检查称为外部同行评议、证明助手形式化或独立的文献优先权核验。

## Evidence location convention

以上 `manuscript/` 和 `certificate/` 路径均相对于以下只读评审根目录，行号已在本次直接核实。

`D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/`

机制重点证明的 `research_log/` 路径均相对于 `certificate/coordinated_primal_dual/source/V4_6_1_1_lower_bound/`。新运行记录的根目录为 `D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/reviewer_1_work/`。
