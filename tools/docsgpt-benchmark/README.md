# DocsGPT 问答基准 / DocsGPT benchmark

站点右下角的 M4 助手由自托管的 DocsGPT 提供。**这个目录用来回答一个问题：改了 DocsGPT 之后，助手还靠不靠谱？**

用例的期望值全部从 `docs/` 正文抄录（每条都带 `evidence` 出处），不来自模型回答——否则基准只会复述模型现在的脾气，改坏了也看不出来。

## 什么时候该跑

- 升级 DocsGPT、换 embedding 模型、改检索器 / 分块参数之后
- 重新同步文档（`manage_source_files` sync）之后
- 改动 `fourier-grx-M4` 文档结构（挪目录、改文件名）之后 —— 这时先检查 `cite` 里的路径是否还成立

## 怎么跑

```bash
# 全量问答判分（默认，最慢但最贴近用户实际体验）
python3 tools/docsgpt-benchmark/run_benchmark.py

# 只跑检索，秒级出结果，适合先定位“是没召回还是模型没用上”
python3 tools/docsgpt-benchmark/run_benchmark.py --mode retrieve

# 先检索后问答，失败的用例会标注检索阶段是否也没召回
python3 tools/docsgpt-benchmark/run_benchmark.py --mode both

python3 tools/docsgpt-benchmark/run_benchmark.py --list          # 看分类和条数
python3 tools/docsgpt-benchmark/run_benchmark.py --category cli  # 只跑一类
python3 tools/docsgpt-benchmark/run_benchmark.py --id rel-4486 -v
python3 tools/docsgpt-benchmark/run_benchmark.py --mode retrieve --check   # CI 用，有失败即退出码 1
python3 tools/docsgpt-benchmark/run_benchmark.py --fail-under 90           # 通过率低于 90% 即退出码 1
python3 tools/docsgpt-benchmark/run_benchmark.py --json report.json        # 落明细
```

依赖只有 Python 3 和 PyYAML。问答档用站点配置里已发布 Agent 的公开 key（`_config.yaml` 的 `docsgpt.api_key`），可用 `DOCSGPT_API_KEY` 覆盖，地址用 `DOCSGPT_API_HOST` 覆盖。

`retrieve` 模式走 DocsGPT 的检索试跑端点，需要该服务主机上的 JWT 密钥：在那台机器上会自动读 `/opt/docsgpt/.env`，否则显式设 `DOCSGPT_JWT_SECRET`。**密钥不进仓库。**

## 判分口径

| 字段 | 含义 |
|------|------|
| `cite` | 前 20 条引用里必须出现这些文件（全部满足） |
| `cite_any` | 引用里出现其中任意一个即可 |
| `all_of` | 回答必须包含的文档事实锚点 |
| `any_of` | 每个子列表内部是“或”，子列表之间是“与” |
| `none_of` | 出现即判失败（用来抓“拿相邻版本充数”） |
| `absent` | 文档里确实没有这条信息，期望模型明确说查不到，而不是编造 |

文字匹配是大小写不敏感、空白折叠后的子串匹配；所以锚点选的是版本号、TID、参数名、具体数值这类**低噪声、不随措辞变化**的片段，而不是整句。

`retrieve` 模式下文字锚点改在**召回的分块正文**里找（即“证据有没有被捞上来”），而 `absent` 用例只能由生成环节判定，该模式下记为 SKIP。

## 加用例

往 `cases.yaml` 的 `cases` 里追加一条即可。三条规矩：

1. **先翻文档再写期望**，`evidence` 填文件或行号，方便别人复核
2. 锚点用版本号、任务号、参数名、数值，不要用整句中文——模型换种说法就误判
3. **锚点不能是问句里已经出现的词**：只要模型把问题复述一遍就能及格，这条用例等于没写。跨语言/跨页用例尤其注意 `PD`、`DSP`、`会`、`4132` 这类回声锚点，跑 `--audit-anchors` 可以扫出来
4. 加一条 `absent` 用例（文档里没有的东西），这是唯一能抓住“一本正经胡说”的题型

## 自动化

文档合进 `main` 之后，`.github/workflows/docs-sync.yml` 会自动做两件事：

1. `python3 tools/sync_docsgpt.py --check` —— 把 `docs/` 打包推给 DocsGPT 增量同步
2. 抽样跑几条本基准（不阻塞，只作信号）

凭据模型：`simple_jwt` 模式下 DocsGPT 发不出 PAT（`auth_type_supports_pats` 只允许
默认/oidc），所以 CI 持有的是一个**同步令牌**（仓库 secret `DOCSGPT_SYNC_TOKEN`）。
云端 Caddy 只在对 `manage_source_files` / `task_status` 两个端点校验该令牌通过后，
才把它换成 DocsGPT 内部凭据——CI 既拿不到 `JWT_SECRET_KEY`（那等于能伪造任意身份），
也用不到其它接口。顺带 DocsGPT 的公网接口面已收敛到 widget 真正调用的 5 个端点
（`/stream` 与 `/api/{feedback,search,store_attachment,task_status}`），其余管理端点
在边缘返回 403。

注意 `sync` 是**整源替换**语义：zip 里没有的文件会被从源中删除，所以同步脚本要求
`docs/` 至少 120 个 markdown 才肯上传，CI 在 docs 缺失的分支上会直接失败而不是清空语料。

手动补一次同步（例如改完检索参数想立刻验证）：

```bash
DOCSGPT_TOKEN=$(现签的 JWT) python3 tools/sync_docsgpt.py --check   # 在 DocsGPT 主机上
python3 tools/sync_docsgpt.py --dry-run                            # 只体检
```

## 现状

基线（2026-11-24，DocsGPT 1.1.0 + pgvector hybrid + chunks=20，语料对齐 HEAD）：

| 模式 | 结果 |
|------|------|
| `retrieve` | 61/64 = 95.3%（2 条 absent 用例该模式下跳过） |
| `answer` | 62/66 = 93.9% |

- 66 条用例、11 个分类。`release_version`（单版本改动）这一类是历史上最先坏掉的：纯向量检索下，一个开头就是 `4.4.86` 的分块能排到 100 名开外，助手于是回答“资料里没有”。
- 已知偏慢的是跨版本区间类问题，单条可能到几十秒；全量 answer 模式并发 8 约需 6-7 分钟。
- LLM 生成有随机性，个别用例可能偶发失败；连续两次同一用例失败才当作回归看。

## 已知缺口（当前稳定失败的 4 条，不是判分写歪）

留在这里而不是把期望放宽到通过，因为它们各自指向一个真实的薄弱点：

| 用例 | 症状 | 判断 |
|------|------|------|
| `meta-recommend` | 问“新部署推荐装哪个版本”，回答“文档没写明”，而答案明确写在发布页版本列表上方的说明里 | 那段说明与问句**没有共同的拉丁/数字词元**，中文整串又匹配不上，词法通道只能靠 `fourier-grx` 这个高频词，等于退回向量检索 |
| `pre-install-syntax` | 问“怎么安装预发布版本”，回答“文档里没有预发布安装说明”，而 CLI 页有整节「预发布渠道」并给出了命令 | 同上：纯中文问句在词法通道里失声。注意 CLI 页**被引用了**，但引到的是同页其它小节——文件命中不等于段落命中 |
| `safety-knee-boundary` | 命中了位置保护的通用机制，没能同时召回 4.4.48 里“膝限位任务缺少边界更新”这条安全修复 | “症状 → 引入修复的版本”这类问题仍偏弱 |
| `cli-update-version` | CLI 页已被引用，但模型选了“下载 deb + dpkg 手动装”的离线路径，漏掉主路径 `fourier-grx update <version>` | 不是检索问题，是取舍/提示词问题 |

前三条同源：**中文问句在词法通道里贡献为零**。已经试过一种改法并被实测否掉——把中文按 2 字滑窗切成词元，能救回 `meta-recommend` 和 `pre-install-syntax`，但同时把 `cli-version-fields` 和 `rehab-pd-vs-dt` 挤出检索窗口，检索档 61/64 前后持平，因此没有采纳（见 DocsGPT 主机上 `docsgpt_lexsearch.py` 的 `query_terms` 注释）。再试的方向：整串词元给高权重、窗口词元只作次要信号；或只在问句里没有任何拉丁/数字词元时才启用窗口。
