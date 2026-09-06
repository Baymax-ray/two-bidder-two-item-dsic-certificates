# Reviewer 3

## Review setup

- **Input scope** 冻结包中的完整英文主稿及四个 TeX 输入、参考文献、README 和相关数学源证明。预先指定的关注点是贡献与新颖性定位、论证组织及非专业读者可读性。
- **Assessment boundary** 这是内部模拟投稿前评估。本报告只使用指定冻结包及共同评审标准，没有读取其他评审意见、历史评审或汇总。没有检索包外文献，没有修改源材料。
- **Shared manuscript claim summary** 对两位可加竞买人、两件物品及四个独立均匀估值，稿件给出逐点 DSIC、ex-post IR 且联合可行的随机机制，以及覆盖不受有限菜单限制的随机机制类的连续上界。当前区间约为 \([0.8764641644718,0.8829230532587]\)，并证明若干实际剩余容量上的完整条件筛选最优性。全局最优机制及匹配证书仍未获得。
- **Visible evidence base** 主稿完整解析论证、当前机制的全实数分类证明与占用翼证明、显式收入表达式及当前上界清单。具体位置采用下列源索引，行号以冻结文件为准。
- **Missing materials affecting confidence** 包内没有所引外部文章的完整正文或外部机制与对偶数组。因此，本文献定位的完整性、外部结果的逐项数学复核以及最新优先权不能在此独立确认。这一限制不等于发现引文错误。

### 源索引

以下链接均指向只读冻结包。后文的行号沿用对应源文件。

- **S1** [manuscript.tex](D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/manuscript/manuscript.tex)
- **S2** [joint_residual_screening.tex](D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/manuscript/joint_residual_screening.tex)
- **S3** [reference_specification.tex](D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/manuscript/reference_specification.tex)
- **S4** [functional_exchange_mechanism.tex](D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/manuscript/functional_exchange_mechanism.tex)
- **S5** [common_capacity_upper.tex](D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/manuscript/common_capacity_upper.tex)
- **S6** [refined_structure_audit.md](D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/certificate/coordinated_primal_dual/source/V4_6_1_1_lower_bound/research_log/refined_structure_audit.md)
- **S7** [residual_wing_screening.md](D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/certificate/coordinated_primal_dual/source/V4_6_1_1_lower_bound/research_log/residual_wing_screening.md)
- **S8** [当前 manifest.json](D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/archive/certificate/coordinated_primal_dual/manifest.json)，按字段名定位。
- **S9** [共同 Nature 标准](<D:/文档/ChatGPT/AI4MATH/output/output/two_bidder_two_item_full_dsic_exact_auction/V4_6_1_1_V4_6_2_archive_audit/review_packet/criteria/editorial criteria and processes.md>)，按 Criteria for publication 与 After submission 段落定位。

### 本次实际核查

只读重算通过冻结包 SHA-256 清单的全部 404 个条目。另用独立写出的内存计算，通过整数平方根及 Fraction 有理运算重新包围 \(\sqrt2\) 和 \(\sqrt{493894}\)，验证主稿给定的 \(R_*\) 严格区间。由 S8 的精确有理数重新核对上界减法、\(U_*-R_*\) 区间和 \(R_*/U_*>0.992684\)。三个条件区域的面积相加也精确得到 \(2887322279191/4500000000000\)。上述核查均通过，没有产生证明源文件写入。

这些检查没有重新积分整份收入，也没有重新遍历两套完整 Bernstein 树。本次阅读核对了相应解析论证，检查了明确写出的分类与条件，但没有把有限源记录或哈希通过当作全实数定理的独立形式化验证。S1 第 939 至 945 行所述完整运行及 S5 第 115 至 117 行所述遍历一致性，在本报告中仍属于包内报告的执行证据。

## Overall assessment

稿件已经形成一个边界明确、具有可审查数学内容的精确证书研究。最有价值的部分是同时处理两个竞买人的菜单变化，把实际占用区域通过激励约束转化为条件筛选限制，并将这些局部结构与一个更小的全局上界连接起来。解析命题与有理数证书的职责区分清楚。当前结果提供严格收入保证，没有声称解出了全局最优拍卖。

我认为还需要一次实质性的贡献表述校准。尤其是“两位竞买人的 charged screening 值都等于零”这一性质，在本文保留的旧 stream 上界中已经可以直接推出。新增价值应集中在更小的公共价格总质量、允许这种减少的相容性条件，以及对应的精确分解，而不能让读者把零值性质本身理解为此前缺失的关键突破。这个问题削弱新颖性与重要性的论证，不使当前数值区间失效。

## Who would be interested in the results, and why

机制设计与算法博弈论研究者会关注一个经典连续实例中更窄的严格区间，以及超出单边菜单替换的可行改进。凸分析与最优控制背景的读者可能关注占用条带如何强迫边界信息租在正面积区域持续，从而消去一部分自由度。计算辅助数学研究者会关注显式连续对象、解析弱对偶、定向舍入及独立实现之间的证据链。

这些是可以从现有内容说明的专业及相邻领域读者群。稿件尚未展示对更大拍卖、其他分布或领域外问题的实际影响，S1 第 986 至 993 行也明确承认此范围。因此，现有材料支持专业研究意义，但不足以据此确定已经达到 S9 所要求的广泛跨学科重大影响。

## Major strengths

- **机制是完整对象。** S4 第 38 至 76 行给出全部对手报告上的菜单与联合可行的最大化选择，S6 第 197 至 330 行逐类处理兼容性、平局及随机实现。DSIC 是对内部随机性的期望效用陈述，这一点没有被混同为每个随机种子上的真实性。
- **条件证书确实超出有限菜单比较。** S4 第 200 至 235 行及 S7 第 40 至 108 行从任意竞争机制的凸效用出发，利用实际容量与激励限制导出非负系数恒等式。S4 第 184 至 187 行正确解释了覆盖率的分母，也没有把未覆盖部分说成已知存在正遗憾。
- **外部与内部比较较克制。** S1 第 65 至 78、218 至 224 行区分外部打印收入、外部严格上界及内部精确证书，避免从 GemNet 的约数推出严格排名。S1 第 141 至 159 行承认既有弱对偶与凸势框架，当前全文也没有一般收敛或首次使用基础原则的优先权主张。
- **松弛量的解释有实质内容。** S5 第 155 至 186 行把机制本身的激励、容量及虚拟值松弛与数值包围余项区分开来。正松弛只能排除这份价格与该机制匹配，不能推出存在更好的可行机制，稿件保留了这个重要逻辑边界。

## Major Concerns

### R3-M1 公共价格的零 charged 值应与新增的价格质量改进区分

- **Concern ID** R3-M1
- **Severity** Major
- **Blocking** No
- **Axis** originality / scientific importance，技术分类为 novelty-significance
- **claim_pointer** 摘要及贡献列表把构造一个公共容量测度、使双方不受菜单范围限制的 charged screening 值均为零，列为主要新增组成部分。
- **evidence_pointer** S1 第 45 至 49、107 至 109 行。S5 第 74 至 99 行给出零值命题并用 empty 达到零。对照 S1 第 621 至 645 行的单竞买人 stream 收入恒等式及容量放松。
- **Concern** 从稿内既有推导即可定义 \(\Pi^0_j=\max\{0,F_{1j},F_{2j}\}\)。对任意一位竞买人的完整 DSIC/IR 机制，已有

  \[
  R_i=\int F_i\cdot a_i-\int u_i(0;v_{-i})
  \leq\sum_j\int\Pi^0_j a_{ij}.
  \]

  空机制达到零，所以同样有 \(H_1(\Pi^0)=H_2(\Pi^0)=0\)。这里用到的只是已有单人恒等式、非负分配和 \(\Pi^0\ge F_i\)，不要求两个独立竞争机制事先联合可行。因此，零值性质及公共测度的存在本身，不足以区分本节新增内容与前面的旧证书。S5 已说明空机制留下容量未用，这个解释是正确的，但贡献层面的表述仍容易让读者高估“双方 charged 问题已解”的新增含义。
- **Why it matters** 这是对主要创新点的识别问题。真正需要凸效用结构、对手符号证明与稀疏 IC 环的部分，是在保持双方有效的同时减少价格总质量，并给出连续积分的严格界。若把一个旧证书已具备的零值性质单独作为关键进展，读者难以判断新增数学与一般弱对偶基础各贡献了什么。
- **Resolution test** 在公共测度命题附近明确指出旧 \(\Pi^0\) 也具有零 charged 值，并将摘要、贡献项和讨论中的新增内容具体落到 \(\Pi'\) 的构造、可替换区域的相容性、质量减少以及松弛分解。无需证明两种表示不等价，也无需补出最优拍卖。修改后，应能仅依靠主稿准确回答“新证书比旧证书多获得了哪个不自动成立的性质，以及该性质怎样改善上界”。
- **Severity rationale** 需要对核心新颖性叙述作实质校准，因此属于 Major。有效上界、完整机制及严格收入保证仍可成立，因此 Blocking No。

## Minor Comments

### R3-m1 清除历史章节对当前结论的过时指向

- **Concern ID** R3-m1
- **Severity** Minor
- **Axis** readability / claim-moderation
- **Affected element** 历史条件支持与历史收入小节中的现在时及定理交叉引用。
- **evidence_pointer** S2 第 40 至 44 行说同时支持双方的单一测度仍是 unresolved requirement，而当前 S5 第 65 至 95 行已经构造这种测度。S2 第 484 至 494 行以历史 \(R_J\) 和旧 \(U_{\rm stream}\) 的区间，称其建立 标记为 `thm:bracket` 的定理 的 lower claim；当前该定理实际陈述 S1 第 187 至 208 行的 \(R_*\)。S2 第 69 至 71 行虽限定随后历史构造，却没有消除这两处指向的歧义。
- **Issue** 当前上下界在别处有各自证明，因此这不是找到证明缺口。问题是读者可能把历史阶段未完成的任务当作今天仍未完成，或把 \(R_J\) 的证明误接到更大的 \(R_*\)。
- **Required correction** 将第一处限定为该历史阶段或那些局部证书本身尚未建立公共测度，并明确链接当前公共证书。将第二处改为历史 bracket 的下界说明，当前 \(R_*\) 的证明应直接指向 S4 的完整机制命题与其收入式。

### R3-m2 避免用同一个 \(R_0\) 表示两种不同收入

- **Concern ID** R3-m2
- **Severity** Minor
- **Axis** readability / writing-clarity
- **Affected element** 收入符号。
- **evidence_pointer** S1 第 479 至 486 行把 \(R_0\) 定义为两位竞买人的旧 affine base 收入。S5 第 35 至 36 行又以 \(R_0=4/9+2\sqrt2/27\) 表示一个单竞买人全容量菜单的收入。
- **Issue** 两个数的含义不同，但新定义没有显式局部作用域。稿件已经有较长的历史收入依赖链，这一复用会使公式核对更容易出错。
- **Required correction** 为单竞买人收入使用不同符号，例如 \(R_{\rm SB}\)，并保持其与旧两人 \(R_0\) 的区别。

### R3-m3 在主定理后提供当前证明的短路线图

- **Concern ID** R3-m3
- **Severity** Minor
- **Axis** readability for nonspecialists
- **Affected element** 主定理至当前机制和当前公共上界之间的阅读路径。
- **evidence_pointer** S1 第 114 至 120 行仅提供两个章节引用。主定理之后先经过 S1 第 226 至 549 行的历史确定性机制，再经过 S2 的历史条件与重分配结构及 S3 的 206 行保留机制说明，才到 S4 的当前构造。上界侧 S1 第 666 至 750 行的径向特殊函数计算及第 821 至 892 行的旧遍历记录，也先于 S5 的当前证书。
- **Issue** 这些材料具有可复现价值，但非本领域读者很难看出哪些是当前定理的必需解析输入、哪些是保留的历史收入结果。S4 第 2 至 4、131 至 141 行说明当前收入重新完整积分，这个关系在主定理附近没有得到同样直接的呈现。
- **Required correction** 在主定理后增加一幅简短依赖图或一个紧凑表格，分别列出当前完整机制、当前收入积分、条件最优性及当前公共上界的入口，并标明历史收入不是当前收入的逐项加法定义。为非专业读者补一句解释，固定对手的分配后才得到“剩余容量”，一个条件问题最优并不意味着两人同时变化也无法改进。无需删除保留材料或重写已有证明。

## Technical failings that need to be addressed before the case is established

本次限定核查未发现可以据此认定当前区间定理失效的技术错误，没有提出 Blocking Yes 的事项。R3-M1 影响的是新增贡献的数学定位，R3-m1 与 R3-m2 需要修正以免读者接错结论或收入符号。

这个判断不等于完成全套独立复现。尤其是完整 revenue integration、所有有限算术树节点和全部辅助代码的正确性，并未在本次重新执行。全实数证明与执行可信边界应继续按稿件既有方式单独陈述。

## Assessment against Nature-style criteria

| 共同评价轴 | 评估 |
|---|---|
| Originality | 包内支持具体的新机制、实际剩余容量恒等式和更小的精确公共证书。对基础凸势及弱对偶的归属较克制。R3-M1 要求进一步分清通用零 charged 值与新增的严格质量改进。文献全局优先权在本包内不可独立判断。 |
| Scientific importance | 对经典连续实例的严格界、可审查构造和条件最优性有专业意义。\(99.2684\%\) 是由上下界得到的保守保证，不能作为已刻画最优机制的替代。当前材料尚不能支撑对广泛科学领域影响的确定判断。 |
| Interdisciplinary readership | 激励约束、凸效用、资源约束与计算辅助证明之间存在清楚的交叉点。对其他分布、更多物品或非拍卖问题的适用性仍未建立，作者已明确限定。 |
| Technical soundness | 主稿保留逐点激励与容量要求，条件竞争类不局限于有限菜单，公共测度使用绝对连续配对，数值余项与机制松弛分开。本次确切完成的核查是全包文件身份、当前代数收入区间及上界和保证算术，未声称完整计算重放。 |
| Readability for nonspecialists | 引言和讨论解释了研究动机，但大量历史构造与重新使用的符号使当前贡献难以定位。R3-m1 至 R3-m3 是具体可完成的改进；修正后应使读者更容易识别主定理证据链。 |

## Recommendation posture

建议围绕 R3-M1 校准核心贡献，并完成上述局部表达修订后，再作专业领域的外部同行评审。这份材料已经足以支持一个有实质内容的精确机制设计研究讨论，不需要为了显得完整而把剩余开放问题写成已解决。若按 Nature 的广泛重要性标准衡量，当前证据主要显示领域内及相邻数学方法上的价值，尚不足以据此给出强肯定的刊物定位。这是模拟评审意见，不是编辑决定。

## Risk / unsupported claims

- 没有独立确认完整外部文献优先权、GemNet 未四舍五入收入或外部双数组。稿件目前的保守比较方式应保留。
- 不从条件覆盖率推断全局缺口关闭比例，不从公共价格对当前机制的严格松弛推断当前机制次优，也不从双方 charged 值为零推断存在匹配拍卖。
- 不把本报告中的 404 项哈希通过或有限精确算术核查，表述为完整解析证明或两套完整上界遍历的独立重现。

## Freeze declaration

本报告在独立上下文中完成，仅依赖上述共同冻结包及本评审预先指定的关注点。完成后计算 SHA-256 并向协调者提交；冻结后不根据其他报告调整关注点、严重性或措辞。
