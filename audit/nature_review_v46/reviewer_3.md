# Reviewer 3

## Review setup

**Input scope** 本报告是内部 AI 辅助投稿前审阅，不是外部同行评审或编辑决定。审阅对象是 SETUP.md 指定的冻结稿件及其源材料。本审阅未接触其他审阅报告、共享问题清单或原始工作区材料。

**Assessment boundary** 完整阅读两份 TeX 源文件、书目、归档说明和相关数学实现，重点追踪最终机制、参考收入、代数及对数增量、上界系数和计算证据边界。材料是经过筛选的 source-reading packet，明确不构成完整独立发布重放包。因此，预期省略的审计文件及其导致的发布入口不可执行性，不被视为归档缺陷。本次没有运行全上界遍历，也没有重新积分全部历史基础层。当前可用环境没有 pypdf 或 pdftotext，未完成 PDF 提取或页面视觉检查，排版判断限于 TeX 结构。

**Shared manuscript claim summary** 在四个独立均匀估值的两竞标者两物品模型下，给出完整随机化、逐点 DSIC、事后 IR 和联合可行的机制，其收入为

\[
0.8758198541484224553460<R_J<0.8758198541484224553461,
\qquad
R_J\leq\mathrm{OPT}\leq
\frac{3715139591287203}{4194304000000000}.
\]

论文同时提出指定剩余容量下的全随机化条件筛选证书，并用联合修改展示条件最优不能自动拼接成全局最优。它没有声称已确定全局最优机制、最优值或最优值的取得性。

**Visible evidence base** 下列路径都相对于冻结 packet。为使位置可重查，使用以下缩写。

- MS 指 \`archive/manuscript/manuscript.tex\`。
- JS 指 \`archive/manuscript/joint_residual_screening.tex\`。
- JL 指 \`archive/certificate/joint_residual_screening_lower_bound/\`。
- S 指 JL 下的 \`source/\`。
- UB 指 \`archive/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound/\`。

行号依据所提供文件实际逐行读取。评议使用 common_criteria.md 的五项标准。材料之外的文献优先权、公开仓库的当前状态，以及完整发布包的本次重放结果，均未另行评估。

## Overall assessment

稿件提供了值得重视的精确证书工作。其最可信的特征是清楚分开了三类对象，完整可行机制给出的下界、对全部可接受机制成立的上界，以及只对特定剩余容量成立的条件最优性。严格收益改善没有被提升为全局最优性，有限菜单也没有被误当作条件竞争者的先验限制。

就我的重点而言，最终增量的计算链比正文呈现得更清楚。实际代码会计算整张受影响菜单的收入变化，含仍获得相同物品但支付改变的类型；最终收入的高精度则明确依赖被冻结的历史参考区间。本次两项只读精确重算及直接有理数检查均与稿件一致。我未发现可据此认定为 Blocking Yes 的具体错误，但这一判断受源阅读和局部执行范围限制，并非完整新认证。

最需要实质修改的是从可运行研究历史转化为可独立理解的论文表述。正文详细列出了较早确定性机制的分解，却把最终参考机制和参考收入压缩为版本号引用。对于以“explicit mechanism”和“exact revenue specification”为核心贡献的论文，这使主要定理的对象辨认和后续复用成本偏高。另一个问题是广泛科学重要性的论证仍弱于领域内技术价值。

## Who would be interested in the results, and why

机制设计和算法博弈论研究者会关心严格连续上界、无有限菜单限制的条件证书，以及兼顾另一竞标者反应的可行变形。凸分析、最优传输和计算证明研究者也可能对奇异线测度如何约束信息租，以及精确包围如何衔接连续弱对偶感兴趣。

对更广泛的优化或机器学习读者，潜在启发是如何把数值发现转化为可验证的连续结论，以及为什么分别最优的菜单仍会留下有利的联合变化。现稿没有证明该流程在其他实例上有效，因而不宜把这种潜在兴趣直接等同于已经展示的跨领域影响。

## Major strengths

1. **论断范围控制准确。** MS 第 192 至 228 行把严格区间、98.8779% 保证和外部小数基准分开，MS 第 969 至 978 行明确保留全局最优问题。对 GemNet 约 0.876 的比较没有被写成本文超过该下界。

2. **精确收入涵盖完整激励反应。** JS 第 346 至 360 行保留彩票降价和完整菜单入场费的共同影响。S 下 \`V4_6/verifier/price_joint_revenue.py\` 第 151 至 233 行分别积分低于 \(c\) 的菜单和具体费用分区，再加上彩票收入项。程序重建部分分式恒等式，并对有符号对数项使用正确方向的区间端点。本次运行得到 \`PRICE_JOINT_REVENUE_EXACT_PASS\)，其中竞标者 1 的总增量为
   \[
   -\frac{24631898853429}{125000000000000000000000}.
   \]
   这说明计算没有只保留有利的竞标者 2 收入。

3. **条件证书保留了关键的逐点信息。** JS 第 74 至 117 行和第 156 至 211 行给出体积项与报告线上的测度项，明确保留原点信息租和实际选取的子梯度。JS 第 308 至 313 行还限制了最终机制保留的 Eplus 条件证书范围。该处理比仅以面积零为由忽略线约束更符合本文逐点模型。

4. **上界证据的组成和独立性边界透明。** MS 第 571 至 647 行给出解析弱对偶，第 752 至 819 行指定有理见证，第 821 至 918 行说明有限包围及实现层面的重放。对 32 个系数和基序的直接逐项检查与 UB manifest 一致。正文也明确说明两份实现共享有理输入和 Bernstein 原理，避免把实现分离误称为完全无共同依赖的证明。

## Major Concerns

### R3-M1

**Severity** Major

**Blocking** No

**Axis** technical soundness / reproducibility / readability for nonspecialists

**issue_key** final-mechanism-and-reference-revenue-specification

**Claim pointer** MS 第 119 至 120 行和第 192 至 210 行将显式机制及精确收入作为主要成果。JS 第 215 至 223 行以 V4.5 为完整参考机制，第 317 至 324 行以“included V4.02 continuous integrals”定义 \(R_{4.5}\)。

**Evidence pointer** MS 第 234 至 235 行、第 524 至 550 行；JS 第 215 至 249 行、第 317 至 324 行；JL \`manifest.json\` 的 \`mechanism\`、\`predecessor\` 和 \`exact_revenue\` 字段；S 下 \`V4_02/verifier/split_cost_candidate.py\` 第 19 至 24 行、第 33 至 81 行；\`V4_02/verifier/split_cost_revenue.py\` 第 99 至 135 行；\`V4_5/verifier/independent_lottery.py\` 第 130 至 141 行；\`V4_6/verifier/independent_revenue.py\` 第 147 至 174 行。

**evidence_status** located

**Concern** 最终定理的对象在源材料中可以追踪，但论文对其必要定义过度依赖历史版本布局。一个具体例子是正文显式基础参数仍为 \(s=1137/1000\)，而最终机制的参考链已经使用 \(s=142/125\)，并把冻结 V3 菜单相对旧基础菜单的增量移植到新基础菜单上，再进行 Q 区域替换和彩票修改。这不是仅把正文确定性机制加上所显示的四个新步骤就能无歧义重建的规则。

收入也有相同问题。\(\,R_{4.5}\,\)不是一个给出的常数表项或单个展示积分，它继续依赖 V4.02 的整套变形公式，后者又读取 V3.1 的参考收入。JS 没有精确指出这些被积函数、边界和前置常数在论文中的最终定义位置。相较之下，正文唯一的收入分解表只列出较早的确定性前驱，读者很容易把那个完整表误认为主要下界的完整定义。

**Why it matters** 这是主要结果的可辨认性和可复用性问题，不是已经发现的收入计算错误。提供源代码允许读者逐层追踪，因此不判为 Blocking Yes。但“精确给定的最终机制”应当有一个稳定、可引用、摆脱探索版本命名的数学入口；否则不同读者可能从不同前驱开始重建，最终机制的教学、比较和扩展也会依赖研究历史考古。

**Resolution test** 在正文或一个明确命名的附录中，集中给出最终参考机制的常数、菜单区域、继承顺序和端点规则，并指向 JL manifest 所指定的最终 \`mechanism(profile)\`。同时给出一个最终收入依赖表，列明 \(R_{4.5}\) 的有限积分定义、各历史基础依赖、最终四阶段增量、每项的精确表达形式，以及是重算还是继承区间。验收标准是另一位读者不必阅读带历史版本叙述的研究日志，就能确定任一报告所属菜单，并从明确列出的数学对象重建所宣称的收入区间。无需把已正确的历史文件重写成一个新实现。

### R3-M2

**Severity** Major

**Blocking** No

**Axis** originality / scientific importance / interdisciplinary readership interest

**issue_key** reusable-insight-and-broad-significance

**Claim pointer** MS 第 107 至 125 行将有限容量测度、完整联合变形和新下界作为连贯贡献；第 157 至 164 行把新理论内容定位在具体剩余容量支持及其带来的原始变形；第 948 至 978 行讨论其结构意义和未解决问题。

**Evidence pointer** MS 第 66 至 78 行、第 146 至 164 行、第 948 至 978 行；JS 第 262 至 313 行、第 343 至 373 行；S 下 \`V4_6/research_log/price_joint_reallocation.md\` 第 207 至 209 行、第 288 至 305 行；common_criteria.md 的 Criteria for publication 和 After submission 部分。

**evidence_status** located

**Concern** 论文已谨慎避免全局最优和新的最佳下界宣称，但尚未充分说明，除这一规范实例的精确推进之外，读者能直接复用什么新的科学认识。尤其值得突出的结论是，消耗中的报告线支持并不能直接当作完整联合收入导数，实际彩票变化的一阶项为 \(\alpha\ell_*/4\)，而不是 \(\lambda=\alpha(c+\ell_*/4)\)。源笔记清楚解释了差额来自凸迹松弛，但正文把这个解释压缩在多个条件证书和机制修补之间。

精确 \(J\) 只有约 \(3.9161\times10^{-9}\)。这并不削弱“严格存在有利联合方向”的数学意义，却意味着不能只靠最终小数改善来传达这部分理论的价值。另一方面，整体新下界仍低于外部报告值，较强的可证明全球上界又是保留的见证。因此，Nature 式跨领域重要性需要建立在清楚展示的方法或概念变化上，而不只是本次区间越过 0.01。

**Why it matters** 目前材料支持领域内有用且可审计的技术贡献，尚不足以让我判断已经展示了广泛而深远的科学影响。这不否定主定理，故 Blocking No。问题也不是必须再赢得一个数值排行榜，而是主要理论增量的可迁移内容和限制还不够鲜明。

**Resolution test** 用现有证据提炼一个简洁、可独立阅读的说明或流程，明确哪些步骤是一般的凸混合与弱对偶基础，哪些依赖本例的线测度与几何，为什么单边影子价格会误报联合导数，以及严格有利方向如何承担全部信息租成本。用已有实例完成这一说明即可，不应为满足审稿而捏造一般性定理。若不能提供可支持的广泛意义，应把贡献明确定位为该规范实例的精确证书和条件筛选研究，并据此调整投稿定位。

## Minor Comments

### R3-m1

**Severity** Minor

**Axis** readability for nonspecialists / writing-clarity

**Claim pointer** JS 第 232 至 311 行使用 \(v,w\) 分别描述自身类型、对手报告、Q 区域和最终两个矩形。

**Affected element** 完整联合机制段的报告角色与物品方向。

**Evidence pointer** MS 第 168 至 170 行；JS 第 232 至 252 行、第 264 至 295 行；S 下 \`V4_6/research_log/price_joint_reallocation.md\` 第 40 至 47 行；\`V4_5/verifier/residual_lottery.py\` 第 44 至 55 行。

**evidence_status** located

**Issue** MS 最初把 \(w\) 定义成第四个标量坐标，JS 后续改用向量 \(w\) 而未在联合机制段开头明确声明“竞标者 1 报告为 \(w\)，竞标者 2 报告为 \(v\)”。局部证明又把 \(v=(x,y)\) 作为已对齐坐标，而最终价格修改只使用一个物理方向。这要求读者自行对照源码，容易误读矩形究竟是自身报告集还是索引菜单的对手报告集。

**Required correction** 在联合机制段开头明确两方报告和物理物品次序，说明何时对齐高低坐标、何时旋转回物理物品，并用相同记号标注 \(F,G,Q,E^+,W,S\) 的菜单索引角色。以文中的 \(((.45,.45),(.44,.44))\) 所有权转移例和最终彩票转移例各检查一次映射即可。

### R3-m2

**Severity** Minor

**Axis** reproducibility / claim-to-artifact correspondence

**Claim pointer** MS 第 893 至 944 行说明发布检查和定理端点对应关系，UB 被列为现行上界证书。

**Affected element** 保留上界 manifest 及 transcript 中的历史下界字段。

**Evidence pointer** UB \`manifest.json\` 的 \`expected.certified_primal_lower_bound\` 和 \`expected.promoted.remaining_exact_gap\`；UB \`verification_output.txt\`、\`independent_replay_output.txt\` 的同名字段；JL \`manifest.json\` 的 \`lower_floor\` 和 \`strict_gap\`。

**evidence_status** located

**Issue** 现行上界证书保留
\[
26237753173862063/30000000000000000
\]
作为 \`certified_primal_lower_bound\`，其 \`remaining_exact_gap\` 因而也对应历史下界。保持封存文件原样是合理的，但这些字段的名称本身没有提示历史范围，与 JL 的当前下界并非同一端点。独立读取某个 transcript 的用户可能会误把旧 gap 当作当前论文 gap。

**Required correction** 在上界目录说明或最终定理与证书对应表中明确标注这些字段仅为封存时的历史比较，当前区间由 JL 的端点和保留上界共同组成。可以增加外部解释而不改动既有封存 transcript。检查读者能从两个目录准确区分“上界证书的目标值”和“当前下界配对后的 gap”。

### R3-m3

**Severity** Minor

**Axis** technical soundness / readability for nonspecialists

**Claim pointer** JS 第 352 至 359 行使用完整入场费公式
\[
\Delta R_1=(1-3D)\varepsilon-\frac32 C\varepsilon^2-\frac12\varepsilon^3.
\]

**Affected element** 最终入场费收入恒等式的适用条件。

**Evidence pointer** MS 第 409 至 440 行；JS 第 123 至 131 行、第 352 至 359 行；S 下 \`V4_6/research_log/price_joint_reallocation.md\` 第 213 至 238 行；\`V4_6/verifier/price_joint_revenue.py\` 第 151 至 189 行。

**evidence_status** located

**Issue** 先前展示的四选项菜单收入引理要求 \(C\leq1\)，但最终受影响的彩票菜单确实会有 \(C>1\)。例如 \(t=7/10\) 时，直接精确代入得到 \(\delta=1727/62500\)，从而 \(C=31301/31250>1\)。因此读者不能只引用前面的菜单引理来推出最终入场费公式。

这不是指出公式错误。源证明另有足够明确的几何条件，入场费使无售出面积增加 \(C h+h^2/2\)，且所用 \(0\leq h\leq\varepsilon\) 内顶部和右侧效用迹保持正。正文没有把这一独立理由说清楚，容易使读者误以为所有后续计算自动落在先前 \(C\leq1\) 的价格区域。

**Required correction** 在该公式后补充其针对实际费用行的适用条件和简短推导，说明依赖无售出区域扩张及边界迹，而不依赖 \(C\leq1\)。保留对具体费用分区的独立核查指针，并明确零面积的 \(y=c\) 面由点态机制规则处理。以一个 \(C>1\) 的实际行验证条件，避免只使用早期确定性菜单的参数范围。

## Technical failings that need to be addressed before the case is established

在本次可见材料与有限执行范围内，没有定位到足以标记 Blocking Yes 的技术失效。R3-M1 要求补齐主要定理的清晰数学入口和收入依赖呈现，R3-M2 要求使科学贡献和适用范围足以由读者判断。R3-m1 至 R3-m3 是可以局部完成的记号、历史字段和公式条件说明。

这种评估不能替代对全部连续可行性分支的重新证明或全发布重放。特别是有理报告回归点和菜单多边形检查各自有明确范围，不能独立推出所有实报告的逐点结论。本文相应结论仍需要其连续证明。

## Assessment against Nature-style criteria

| Axis | Assessment |
|---|---|
| originality | 所给比较中，具体径向流见证、剩余容量线测度和完整联合变化有可识别的技术内容。稿件没有把一般凸势或互补松弛冒称为新方法。更全面的优先权未由本次材料独立验证。 |
| scientific importance | 精确连续界及指定条件问题的完整证书对本领域有价值。仅凭当前单例和数值进展，还不能认定已达到广泛科学重要性，见 R3-M2。 |
| interdisciplinary readership | 计算证明、优化和机器学习验证读者有潜在兴趣，但目前论证的主要可见受众仍是机制设计专家。 |
| technical soundness | 解析与算术层次分离合理，局部精确重算吻合。未发现明确 blocking 缺陷，但没有执行全部证书或进行全历史基础收入重积分。 |
| readability for nonspecialists | 摘要和开放问题说明有帮助；最终机制与参考收入过度依赖版本链，报告角色转换也提高理解成本，见 R3-M1 和 R3-m1。 |

## Recommendation posture

建议完成实质性表述修订后继续评估。对于领域内的机制设计或算法理论读者，这是一份有具体证据和清晰开放边界的研究稿。对于 Nature 式广泛读者，当前最需要加强的是可复用的概念结论及其讲解，而不是再增加小数位数。我不据此代替编辑作出录用或送审决定。

## 本次实际核查

所有执行均在冻结 packet 内使用非优化 Python，未带 \`--write\`，未生成字节码。

1. \`python -B -X utf8 S/V4_6/verifier/price_joint_revenue.py\` 通过，返回 \`PRICE_JOINT_REVENUE_EXACT_PASS\)，重新计算最终有理数加对数增量，并与保存证书比较。
2. \`python -B -X utf8 S/V4_6/verifier/consolidated_bounds.py\` 通过，返回 \`V4_6_EXACT_BOUNDS_LEDGER_PASS_NOT_CLOSED\)。输出收入区间与 JS 一致，剩余 gap 被包围在 0.0099384483702321295385 与 0.0099384483702321295386 之间。该入口重算新代数及对数项，仍继承 V4.5 区间，不是完整基础重积分。
3. 使用 \`fractions.Fraction\` 独立检查 JL manifest 的 \(U-L<1/100\)、\(L/U>988779/10^6\)，以及 \(8919/10000-U=25760146312797/4194304000000000\)，全部通过。
4. 解析 MS 的见证表并逐项比较 UB manifest 的基序及有理系数，32 项全部一致。
5. 精确代入 \(t=7/10\) 核查 R3-m3 的 \(\delta\) 和 \(C>1\) 例子。该检查仅说明公式适用条件需要单独交代，不构成对最终收入的反例。

这些命令中的 S 是前述源目录缩写，实际运行使用冻结 packet 中的绝对路径。PDF 提取尝试因当前工具未安装而未完成，未因此修改环境或材料。

## Risk / unsupported claims

- 本报告不声称进行过完整上界重放、全部历史基础收入重积分或完整发布入口验证。
- 保存 transcript 的数值一致性和系数一致性支持可审计性，不独立证明解析弱对偶或全部连续可行性分支。
- packet 对既往审计材料的有意省略不被推断为完整归档的缺陷。
- 外部约 0.876 和 0.8919 的性质采用稿件明确给定的比较范围，本次未重建外部机制或对偶数组。
- 支持指定剩余容量的测度，并不自动成为两竞标者共同证书。任何全局最优、一般有限菜单充分性或新最佳下界的扩张性表述，都不受本次评估支持；现稿已经避免这些宣称。

本报告独立定稿后冻结，不作跨审阅比较驱动的修改。

