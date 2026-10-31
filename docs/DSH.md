# DeepSeek Harness：连接 N1X 本地 DeepSeek 1017

**Strata 管理模型与推理服务，DeepSeek Harness（DSH）负责会话与客户端功能。** 已有公开记录覆盖两轮基础聊天和提示词缓存复用；完整 Agent 工具任务、记忆与其他集成不包含在这个验证结论中。

[安装](INSTALL.md) · [性能记录](BENCHMARKS.md) · [FAQ](FAQ.md)

## 1. 谁负责哪一层？

| 层次 | 职责 | 本项目的公开范围 |
|---|---|---|
| N1X 与 NVIDIA 驱动 | 提供 GPU/系统共享内存资源及划分设置 | 维护者的一台 128GB Windows ARM64 笔记本 |
| Strata_Zackyzq | 加载/卸载模型，运行原生 CUDA 引擎，提供本机 API 与监控 | 本机桌面与模型回复有记录 |
| DeepSeek Harness | 发送聊天请求，组织历史与客户端功能 | 两轮基础聊天及缓存复用有记录 |
| 工具、搜索、记忆、嵌入等 | 按客户端及插件各自配置执行 | 不由“聊天接通”自动证明 |

DSH 连接 `http://127.0.0.1:47831/v1`，由 Strata 将请求交给桌面管理的 Windows ARM64 CUDA 引擎和本地量化权重。这条已记录的推理链无需另开 LM Studio 服务，也不经过 WSL 推理转发。

## 2. 连接参数与操作顺序

1. 启动 Strata_Zackyzq，选择本地 DeepSeek 1017 量化模型并加载。桌面模型就绪后再配置 DSH。
2. 在 DSH 添加自定义 OpenAI 兼容提供方，填写下表中的 Base URL 与实际 Model ID。
3. 在需要使用本地模型的会话中明确选择该提供方和模型。已有聊天不会因为新增提供方就一定自动迁移。
4. 使用 Strata 监控查看本机请求与提示词复用，避免把其他提供方或另一引擎的回复归到这条链路。

### 2.1 连接必填项

先填写提供方、Base URL 和实际 Model ID。以下参数用来建立连接；版本和历史高级设置单独列在后面。

| 字段 | 填写方法 |
|---|---|
| 提供方类型 | OpenAI-compatible / 自定义 OpenAI 兼容提供方 |
| Base URL | `http://127.0.0.1:47831/v1` |
| Model ID | 以 `/v1/models` 返回的实际 ID 为准；已测 2.25bpw 为 `deepseek-v4.1-flash-ist-das-2.25bpw` |
| API key | 已测回环配置不需要云端密钥；客户端若要求非空，可用本机占位值，它不是访问凭据 |

### 2.2 历史高级配置：用于解释记录

以下是维护者当时的配置，不是所有 DSH 版本都应照抄的默认值。上下文、输出预算和超时应结合当前客户端、服务端与任务需求设置；尤其保留第 3 节的 HTTP 扩展前提。

| 字段 | 历史记录与含义 |
|---|---|
| 并发 | 历史记录为单路 |
| 上下文配置 | 历史记录为 1,048,576 tokens；必须同时符合服务端与客户端设置，且不代表满 1M 已测 |
| 输出预算 | 历史记录设为 131,072 tokens；不是实际生成量，也不是所有客户端版本的推荐值 |
| 请求 / 流空闲等待 | 历史界面设置为 3,600,000 ms；能否实际等待一小时还受底层 HTTP 与版本影响，见下一节 |
| DSH 精确版本 | 当前公开记录未注明；不能用“最新版”代替实测版本 |

端口 `47831` 是桌面 host 默认值，被占用时可能改变，以本机实际地址为准。不要填内部动态引擎端口。已有模型由 Strata 管理时，无需为这条连接再启动第二份相同大模型。

## 3. 历史两轮聊天记录与复现前提

以下内容恢复自 [2026-10-31 的历史 DSH 文档](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq/blob/fef6e1f390074abf399230a445be325ae6eaaa05/docs/DSH.md)，保留原始口径；**不是本次文档改版新增的测试结果。**

| 历史记录 | 输入 token | 复用 token | DSH 侧整轮耗时 | 解码速度 | 当时记录的结果 |
|---|---:|---:|---:|---:|---|
| 首轮 | 约 30K | 未给出 | 227 秒 | 8.8 tokens/s | 数学与 SQL 概念回答被维护者记录为正确 |
| 同会话追问 | 30,102 | 30,077 | 19 秒 | 10.1 tokens/s | 追问回复被维护者记录为正确，并复用了缓存 |

这些是维护者已公开的观察记录，不是标准化题集分数；19 秒不是每次追问的承诺。DSH 整轮耗时含宿主开销，与引擎工作耗时不同。历史 `first_engine_token_s` 与 `duration_s` 的计时起点尚待核对，不用它们宣传首个可见正文速度。

### 当时使用了未随包发布的 HTTP 超时扩展

历史文档明确说明：维护者机器有一个**仅针对回环提供方的 DSH 传输扩展**，用于避免底层 HTTP 默认超时覆盖界面设置。扩展含机器安装位置，未复制到公开包。因此：

- 本页的两轮记录具有该历史环境前提。
- 界面填入 3,600,000 ms，不等于任意 DSH 版本都能实际等待一小时。
- 当前 DSH 版本是否仍需要该扩展、应如何适配，公开材料尚未确定；不能宣称最新版已经不需要，也不能把历史机器路径直接照搬。
- 已有扩展的脱敏实现思路与两轮验收条件见[开发记录补充](DEVELOPMENT-NOTES.md#本地既有记录补充2026-10-31-整理)；历史 DSH 精确版本仍未锁定，不能以当前安装版本反推。

The historical test machine used a loopback-specific HTTP timeout extension that is not included in the public package. The exact DSH version was not recorded publicly. A one-hour UI setting does not establish a one-hour effective timeout for arbitrary client versions. Current extension requirements remain unverified.

## 4. 长上下文、工具能力与联网边界

1024K 是已配置的服务端上下文上限。DSH 的上下文设置不能超过已加载服务端配置；历史、工具上下文与预留输出也必须装得下。客户端压缩、输出限制和服务端资源仍分别生效。**没有满 1M 输入或长时间 Agent 任务稳定性验收。**

基础聊天接通不代表工具、微信、记忆整理或嵌入服务已迁移。它们可能使用不同模型、权限与网络路径，应按各自实际配置理解，不能仅凭模型回复中的“我能做”认定功能已执行。

模型推理发生在本机；DSH 的搜索、插件、远程工具、遥测或其他提供方是否联网，取决于各自配置。因此“本地推理”不等于整个客户端永不联网。保持回环监听；本接入方法不需要开放公网端口。个人 DSH 配置、真实密钥、原始聊天与机器专属扩展路径不应直接提交仓库。

本地连接界面显示的费用估算也不是云端 API 账单凭证。

![N1X 的 NVIDIA 分配、Strata 监控与 DSH 界面](images/n1x-nvidia-strata-dsh.png)

该截图已由维护者授权公开。它展示三者同机使用，不独立证明截图中模型自述的每项工具能力。

Basic two-turn chat and cache reuse were recorded. Tool execution, memory, embeddings and third-party integrations are separate capabilities. Local inference does not imply that every client feature is offline, and the screenshot is not proof of every generated capability claim.
