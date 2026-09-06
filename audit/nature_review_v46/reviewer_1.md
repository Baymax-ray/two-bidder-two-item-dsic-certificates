# Reviewer 1

## Review setup

**Input scope**

本报告是一份内部 AI 辅助投稿前审阅，不是外部同行评审或编辑决定。评阅对象为不可变 packet 中的 20 页稿件、两份 TeX 源文件、参考文献表、容量支持与完整机制的证明源，以及指定证书的清单和实现。R1 的预设重点是解析正确性、量词、全部随机化竞争机制、例外报告，以及条件证书与联合构造的兼容性。未读取其他评阅报告或比较性意见。

**Assessment boundary**

本次逐段阅读两份 TeX，核对相关证明笔记和源程序，并执行下列局部只读检查。没有重跑完整上界遍历，没有从头重新积分全部历史基准层，也没有作新的文献检索。PDF 元数据确认共 20 页；本次没有完成 PDF 的逐页视觉检查，故不对排版作未经核实的评价。此 packet 按 SETUP.md 的约定省略了先前审计材料，不是完整可移植重放发行包。以下评价不将这种有意省略视为发行档案缺陷。

**Shared manuscript claim summary**

稿件研究四个估值坐标独立服从均匀分布的两竞买人、两物品拍卖，要求每一个类型与对手报告上的 DSIC、按内部随机化取期望的 ex-post IR，以及逐报告的物品容量可行性。主要结论为

\[
0.8758198541484224553460<R_J<0.8758198541484224553461,
\qquad
R_J\leq\mathrm{OPT}\leq
\frac{3715139591287203}{4194304000000000}.
\]

其余核心结论是两个具有明确残余条件的完整随机化条件最优性定理，以及一个严格增收的完整联合改动。稿件没有声称求出全局最优机制或取得匹配的共同容量证书。

**Visible evidence base**

以下定位均相对于 packet 的 `archive/`。为便于核查，将 `certificate/joint_residual_screening_lower_bound/source/V4_6/` 简记为 `V46/`。行号指本次读取的源文件行号。

主要依据包括 `manuscript/manuscript.tex`、`manuscript/joint_residual_screening.tex`、`manuscript/references.bib`，`V46/research_log/inner_diagonal_capacity.md`、`inner_lottery_certificate.md`、`outer_lottery_strip.md`、`outer_capacity_junctions.md`、`free_bidder_one.md`、`outer_bundle_reoptimized.md`、`price_joint_reallocation.md`、`price_joint_exact_revenue.md`、`conditional_coverage.md`，以及下表中的源程序。上界核对还涉及 `certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound/manifest.json` 与 `verify_stream_dual.py`。

本次读取的两份稿件源 SHA256 为

- `manuscript.tex` 为 `13246d300bb3d363e33589908bc54ebf6feff8a9d84655f848bb494b830b155b`。
- `joint_residual_screening.tex` 为 `d8d95f0cc3a24269223ee031f67768e06fbd939c5872b5ce89bfac10decccf30`。

**Fresh checks performed**

各入口均使用非优化 Python 和 `-B -X utf8`，未指定写入选项。

| 本次执行的检查 | 实际结果 | 能支持的范围 |
|---|---|---|
| `V46/verifier/inner_lottery_certificate.py` | PASS，20 个精确多边形恒等式例子，63 个实际残余边界检查 | 源实现中的多项式关系、有限菜单例子的精确恒等式与指定边界点 |
| `V46/verifier/inner_diagonal_capacity.py` | PASS，24 个精确多边形恒等式例子，45 个占用线检查 | 对称与受约束 Q 菜单的局部代数及指定占用线实例 |
| `V46/verifier/outer_bundle_reoptimized.py` | PASS，267 个报告与占用线检查 | 耦合响应实现、精确增量计算与指定边界 |
| `V46/verifier/price_joint_reallocation.py` | PASS，315 个边界检查，严格增量下界为 `26902077489/12500000000000000000` | 联合改动的实施例检查及所述有理严格下界 |
| 另写的一次性内存计算，直接读取最终 manifest，用 `Fraction` 重算端点比较和 40 项对数级数余项 | PASS，确认间隙小于 `1/100`、比例大于 `0.988779`，并包围所列 (J) 的 45 位小数区间 | 检查所给精确表达式及有理端点的算术一致性，未重建 (R_{4.5}) 历史积分 |

这些有限例子不是对全部竞争机制的穷尽。对全部随机化竞争机制的结论依赖下文所评阅的连续解析证明。四个源入口的重新执行也不构成四套彼此独立的证明。

## Overall assessment

我没有在本次审阅范围内发现使主要上下界或两类条件支持定理失效的解析漏洞。最有价值的部分是将条件容量约束对信息租的作用写成了可检查的非负松弛恒等式，并随后给出改变双方完整菜单的严格改进。这比只报告有限菜单搜索中的驻点或数值收益更有说服力。

稿件对若干容易误述的范围作了实质性限制。它保留 (u(0,0)) 或 (u(0,c))，没有假设所有竞争者都归一化为零原点效用；它在带价报告线上使用实际选定的切向分配；它将最终联合改动后保留的 F、Q 和部分 Eplus 范围单独说明。最终正增量 (J) 虽小，却确实针对完整机制而不是一个不可行的单侧彩票降价。

主要不足在意义呈现。现有证据充分支持一个机制设计与计算证书领域的具体技术贡献，但尚不足以使跨学科读者清楚判断它何以具有突出的广泛科学重要性。另有三个可以局部修正的定义或表述问题，见下文。它们不推翻目前可见的核心结论。

## Who would be interested in the results, and why

机制设计研究者会关注完整随机化条件问题的显示解和奇异容量价格，特别是固定残余最优为何仍允许联合增收。连续优化、最优传输和凸分析研究者可能关注容量测度如何与凸效用迹的曲率结合。计算辅助数学与形式验证研究者会关注解析弱对偶、精确见证和有限算术包围的分层结构。对更广泛的经济学、计算机科学或实验科学读者，稿件目前仍需解释这一个小规模标准实例提供了什么可迁移认识。

## Major strengths

1. **上界对完整机制类的量词有明确依据。** `manuscript.tex` 第 168 至 190 行给出联合可测性、可积支付和逐报告的模型。第 585 至 647 行从 DSIC 不等式得到凸 Lipschitz 效用，保留非光滑报告上的已给分配选择，并通过径向积分和散度为零的边界切向修正建立弱对偶。最后的逐物品正最大值松弛只使用概率边际和容量约束，因而确实覆盖随机化分配。它没有假设包络中的逐点赢家本身可由 DSIC 机制实现。

2. **对角孔支持真正保留了信息租和奇异价格。** `joint_residual_screening.tex` 第 48 至 117 行的条件使 \(f\leq0\) 于 (x<A)，从而保证 (F_m\geq0)。面积关系 (3|D_0|=m+1) 使

   \[
   3\int_{D_0}u-mu(0,0)\geq u(0,0)\geq0.
   \]

   这一步可以处理带正原点效用的竞争者。底边和竖直线的容量条件用于达到等号，而不是被作为面积零集合删除。`V46/research_log/inner_diagonal_capacity.md` 第 155 至 222 行进一步核对了受约束 Q 部分的三条实际占用线。

3. **彩票定理的全类结论有超出有限菜单求导的证明内容。** `joint_residual_screening.tex` 第 173 至 205 行的 (T_g) 控制整个右边界凸迹，(M_a) 来自切向分配的单调性，(S_u) 使用 IR 和正面积矩形。结合容量松弛，它们给出对任意 admissible competitor 的不等式，候选菜单再达到等号。`V46/research_log/inner_lottery_certificate.md` 第 104 至 283 行展开了这些步骤，明确没有预先限制竞争者的分配范围。

4. **联合改动的可行性检查覆盖了真正的耦合。** `joint_residual_screening.tex` 第 219 至 305 行及 `V46/research_log/price_joint_reallocation.md` 第 92 至 149 行将新增彩票可能发生的冲突限定到收费矩形 S，并通过完整对手菜单的入场费释放容量。其论证包含空选项优先规则、\(\rho=c\) 保留面及两种物品方向的先前拼接条件，未用几乎处处可行替代逐报告可行。

5. **条件最优性的存续范围与全局问题保持分离。** `V46/research_log/conditional_coverage.md` 第 32 至 74 行不仅排除了被直接降价的 W，还排除了可能因对方收费而改变饱和条件的更宽对手高值区间。这是必要的区分。正文第 308 至 313 行已经采纳该范围，`manuscript.tex` 第 969 至 978 行也明确保留共同证书与全局最优性缺口。

6. **计算证据的可信范围披露得较清楚。** 上界见证由有理系数定义，Bernstein 控制系数与定向误差有明确包围规则，源程序 `verify_stream_dual.py` 第 100 至 175 行与正文描述相符。正文第 915 至 943 行将实现级重放独立性与解析定理区分，并承认新增收益重放共享历史基准积分。外部约 (0.876) 的 GemNet 收益也没有被改写为本稿重放的精确证书。

## Major Concerns

### R1-M1 广泛意义尚未由现有结果和叙事建立

**Concern ID** R1-M1  
**Severity** Major  
**Blocking** No  
**Axis** scientific importance / interdisciplinary readership，辅助轴为 novelty-significance  
**Claim pointer** 摘要及 Contributions 将新容量测度、完整联合重分配和小于 (0.01) 的间隙作为主要贡献，`manuscript.tex` 第 35 至 54 行、第 107 至 125 行。  
**Evidence pointer** `manuscript.tex` 第 146 至 164 行说明本稿与既有对偶架构的联系；第 948 至 978 行仍将结果限定为该实例上的显示机制、特定残余的条件定理以及未匹配的全局上下界。`joint_residual_screening.tex` 第 48 至 52 行、第 123 至 141 行给出具体参数和占用线假设。`common_criteria.md` 的 Criteria for publication 与技术论文条款要求突出的科学重要性或对研究群体的显著技术影响。  
**Evidence status** located

**Concern**

现有材料清楚展示了“在这个实例中能做到什么”，但较少说明“由此获得的认识能在何种其他问题中发挥作用”。数值区间缩窄是有价值的技术进展，然而下界仍低于所引用的外部计算基准，全局优化问题仍开放，而新条件定理的实际应用集中在人工构造的若干残余几何上。这些事实不削弱所证定理，却使 Nature 标准下的广泛意义尚未获得充分支持。

更有潜力的科学信息其实是线上的信息租约束以及联合变化的不同量级。`V46/research_log/price_joint_reallocation.md` 第 288 至 305 行解释了如何从所耗用的奇异容量找到完整联合方向，并以 (O(\varepsilon)) 的收益支付 (O(\varepsilon^2)) 的释放成本。当前正文虽然提及这一构造，却没有充分提炼其可复用条件与适用边界。

**Why it matters**

这是贡献定位和读者可达性上的重大问题，不是数学有效性上的阻断项。没有必要为解决它而声称求出全局最优机制，或要求本稿超越 GemNet 的报告收益；但需要让非本领域读者能够判断精确证书之外新增的结构性认识。

**Resolution test**

在引言或 Discussion 中给出一段可以由文内结果直接检验的适用范围说明，明确哪些步骤只依赖一般的凸效用迹和容量饱和，哪些步骤依赖均匀分布及本文特定孔形。将“固定条件最优仍允许双方联合增收”的机制与完整租金成本解释为主要结果之一。若主张技术可迁移性，应给出相应命题、已证明推论或具体适用条件；若没有这些证据，则将定位明确保持为该标准实例上的机制设计技术贡献。修订后，读者应能说出一个超出小数位提升的具体认识，同时不会推断已获得一般最优拍卖定理。

## Minor Comments

### R1-m1 奇异测度配对的残余函数域需要在两个定理中补齐

**Concern ID** R1-m1  
**Severity** Minor  
**Axis** technical soundness / writing-clarity  
**Claim pointer** 两个松弛恒等式声称适用于 (a\leq r) 的每个竞争者，并出现 \(\langle\pi,r\rangle\)。  
**Affected element** `joint_residual_screening.tex` 第 85 至 89 行、第 166 至 169 行。  
**Evidence pointer** 同文件第 6 至 11 行将容量函数先定义为 jointly measurable，第 25 至 27 行的总命题另有限定 “for which the pairing is defined”；对角定理第 55 行明确要求 (r^*) 为 Borel，但泛化不等式中的 (r) 没有重复此限制。对应源笔记 `V46/research_log/inner_diagonal_capacity.md` 第 90 至 95 行与 `inner_lottery_certificate.md` 第 253 至 258 行明确写的是 Borel residual。  
**Evidence status** located

**Issue**

若 jointly measurable 沿用正文允许的联合 Lebesgue 可测解释，仅有面积可测性不足以保证任意残余函数在带价报告线上的可测性。可在一条面积零直线上用一个关于线测度不可测的集合改变容量，得到面积意义上仍可测的函数，但其奇异价格配对未必有定义。DSIC 所确保的切向分配可测性只适用于 (a)，不能自动传给任意上界 (r)。当前候选残余被要求为 Borel，因而这不影响候选最优性或构造的上下界。

**Required correction**

在两个定理的泛化不等式处明确要求 (r) 为 Borel，或要求各坐标对相应容量价格测度可测，并保留总命题中的配对可定义条件。这是一个函数域说明，无需缩小被比较的 DSIC 随机化机制类，也无需改变实际候选。

### R1-m2 历史基准到活跃机制的常数变化应有简短桥接

**Concern ID** R1-m2  
**Severity** Minor  
**Axis** readability for nonspecialists / reproducibility  
**Claim pointer** 活跃机制从 source-bound V4.5 reference 开始，并继承其完整菜单规则。  
**Affected element** `joint_residual_screening.tex` 第 215 至 219 行、第 317 至 320 行，以及此前确定性机制与之后参考机制之间的衔接。  
**Evidence pointer** `manuscript.tex` 第 232 至 235 行的 base split cost 为 (s=1137/1000)，第 541 至 551 行结束于 (L_{\rm det})；随后正文使用 (q=113/500) 的新筛选参数。`V46/research_log/outer_lottery_strip.md` 第 10 至 14 行明确列出继承自 V4.02 的 (s=142/125)、(d=1/2)、(q=113/500)。  
**Evidence status** located

**Issue**

源包给出了明确的不同阶段，故没有证据表明实际常数被错误混用。但读者从确定性构造直接进入“V4.5 reference”，容易误以为此前的 (s=1.137) 一直沿用。确切收益中的 (R_{4.5}) 也因此比此前详细解释的 (L_{\rm det}) 更难定位。版本编号提供来源，却没有提供简短的数学桥接。

**Required correction**

增加一个短段落或简表，列出从 (L_{\rm det}) 到当前参考机制改变了哪些主要规则与常数，并给出 V4.5 完整评价器和 V4.02 精确参考积分的直接路径。明确 (s=142/125) 属于后续参考机制，(s=1137/1000) 属于此前展示的确定性层。无需把全部历史表格再搬进正文。

### R1-m3 彩票排除语句应指向“不存在更高收益”，避免暗示唯一性

**Concern ID** R1-m3  
**Severity** Minor  
**Axis** technical soundness / claim-moderation  
**Claim pointer** “The hinge term excludes nonlinear convex trace changes and additional lotteries, including scarce allocations below one.”  
**Affected element** `joint_residual_screening.tex` 第 208 至 211 行。  
**Evidence pointer** 同文件第 166 至 205 行的证明依赖容量松弛、(T_g)、(\lambda M_a)、(S_u) 的总和；其中 hinge 项只直接控制右边界迹的曲率。`manuscript.tex` 第 969 至 971 行明确不主张一般有限分配范围或最优拍卖分类。  
**Evidence status** located

**Issue**

显示的恒等式证明全部随机化竞争者无法超过该候选收益。它没有单独给出所有取等机制的唯一性或分配范围分类。因而将“额外彩票”概括为被 hinge 项排除，可能被读成任何含额外彩票的机制都不可能取等。额外菜单选项是否被使用、其他区域的取等自由度，以及报告零测集合上的选择，并没有由这句话建立分类。

**Required correction**

改成“完整松弛恒等式排除了通过额外彩票或更一般随机化分配提高条件收益；hinge 项控制整个彩票区间上的非线性凸迹变化”。如欲作更强的唯一性或菜单分类陈述，则另外给出完整取等条件。这里无需增加这样的强结论。

## Technical failings that need to be addressed before the case is established

本次未发现 Blocking Yes 的技术问题。R1-m1 应在正式定理陈述中修正，以避免奇异测度配对被套用到没有定义的容量函数上。R1-m2 和 R1-m3 分别改善机制源的可追踪性与定理解释的精度。R1-M1 关系到 Nature 风格的意义论证，不应被误解为上下界或条件最优性目前无效。

这一判断具有明确执行边界。本次重新执行的是四个局部入口及独立的有理端点、对数余项算术，未执行全部 29 个新增入口，未重跑 3,738,334 个节点的完整上界遍历，也未重新构造历史基准的所有多面体积分。因此我支持的是“可见解析链条没有发现阻断漏洞，所执行检查通过”，不是一份新的全档案重认证声明。

## Assessment against Nature-style criteria

| 评价轴 | 本次判断 |
|---|---|
| Originality | 稿件清楚区分已有凸势、传输和 DSIC 对偶框架与本文显示的径向流见证、特定残余容量测度及完整原始变化。包内证据支持其贡献被具体陈述；在没有新文献检索和原论文全面比较的情况下，不能确认全面的首创性或当前最优文献地位。 |
| Scientific importance | 对连续 DSIC 的一个经典小规模实例具有可辨认的技术价值。严格容量证书和条件最优与联合改进的分离比小数位本身更有意义。超出该实例的突出科学重要性仍需补足，见 R1-M1。 |
| Interdisciplinary readership | 机制设计、凸优化、连续对偶与计算辅助证明之间存在真实联系。面向更广泛读者的结论和迁移条件尚需更直接的说明。 |
| Technical soundness | 上界的随机化全类量词、两类条件支持的非负松弛和联合释放的容量论证在本次源审阅中相互协调。所执行的精确检查均通过。需澄清 R1-m1 的泛化残余函数域；完整算术重放和历史基准重积分不在本次验证范围内。 |
| Readability for nonspecialists | 摘要明确给出问题、数值区间和开放范围，是优点。正文先展示多层确定性前身，再转入用版本号定义的参考机制，增加理解活跃结果的成本。R1-m2 的桥接，以及 R1-M1 中对租金和联合变化的直接解释，会使核心贡献更容易把握。 |

## Recommendation posture

我倾向于在保留现有结论范围的前提下修订后继续推进投稿。修订重点是奇异配对定义、参考机制衔接和广泛意义论证。当前材料已形成可信的领域内技术论文基础；仅凭这些包内结果，我不能认定已经达到 Nature 对突出科学重要性与跨学科影响的要求，也不作编辑送审或接收决定。

## Risk / unsupported claims

- 未发现支持将本文写成精确求解 \(\mathrm{OPT}\)、证明最优值必被取得、分类全部最优机制，或构造匹配共同容量证书的证据。稿件目前也明确没有这样声称。
- F 与 Q 的存续和受限 Eplus 的存续，不能概括为最终机制在全部对手报告上条件最优，更不能据此推出全局最优。
- 有理哈希、旧的通过记录和本次有限例子均不等同于一份新的完整连续定理重放。本次对 (J) 的对数表达式进行了独立级数包围，但所输入表达式的积分来源仍依赖已阅读的完整菜单推导。
- 约 (0.876) 的 GemNet 收益和 (0.8919) 的外部严格上界在本报告中均作为稿件所提供的文献比较使用。本次没有重新构造外部机制、重放外部上界数组或开展新的优先权调查。
- 本报告没有以本次无法运行完整发行流程或无法完成 PDF 视觉检查为由，推断原发行包存在缺件、代码不工作或版面有缺陷。

本报告完成后冻结，不依据后续比较修改。
