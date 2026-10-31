# FAQ / 常见问题

[项目首页](../README.md) · [安装](INSTALL.md) · [DSH 接入](DSH.md) · [公开性能记录](BENCHMARKS.md) · [AI 协作提示词](AI-ASSISTED.md) · [源码与构建](BUILD.md)

## 我有一台 128GB 内存的电脑，能用这个项目吗？

目前有记录的是维护者的一台 **微软 N1X 128GB 统一内存、Windows ARM64 笔记本**。128GB 是 CPU/GPU 共享总容量，不是各有 128GB。仅凭容量不能判断兼容性；还需要处理器、GPU、操作系统架构和驱动匹配。普通 Windows x64、Apple Silicon、DGX Spark Linux 不能自动归入已测范围。

## 这里的 DeepSeek 1017 到底是哪一版？

完整名称是 **DeepSeek-V4.1-Flash-1017**，对应 DeepSeek 官方 **2026 年 10 月 17 日**的更新。可查 [官方更新记录](https://api-docs.deepseek.com/updates/)与[官方模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)。使用固定模型名和日期，有助于与其他 DeepSeek 版本区分；“最新”会随后续更新变化。

## 我下载的是官方原始精度权重吗？

本项目已有记录使用的是基于该模型的 **ISTA-DASLab GSQ-RCO GGUF 社区量化权重**，见[量化发布页](https://huggingface.co/ISTA-DASLab/DeepSeek-V4.1-Flash-1017-GSQ-RCO-GGUF)。已记录的精度为 1.75bpw 和 2.25bpw；2.00bpw 没有同等验收。不能把量化模型速度或效果写成官方原始精度的效果，也不能由 `2.25bpw` 反推出统一的质量评分。

## 是 Windows 原生运行，还是通过 WSL / LM Studio 转发？

这条发布路径的**推理引擎是 Windows ARM64 原生 CUDA**，不经过 WSL 推理转发，也不需要 LM Studio 服务器。桌面与控制栈仍含仿真的 x64 Python；“原生”针对推理引擎，不表示所有依赖都是 ARM64。

## 安装之后还需要自己编译吗？

直接使用发布的 Windows ARM64 安装包，按 [INSTALL.md](INSTALL.md) 配置即可。安装程序含应用与推理运行库，但不含模型权重或显卡驱动。只有需要修改源码、审阅补丁或自行构建时，才进入 [BUILD.md](BUILD.md)。公开仓库以固定上游版本加适配补丁交付，尚未证明任意干净环境能一键完整构建。

## 为什么 2.25bpw 的文件约 273.8GB，128GB 内存仍然有运行记录？

273.8GB 是整套模型文件的十进制磁盘占用，包含专家及共享组件。磁盘容量、GPU 常驻分配、专家 RAM 缓存和操作系统文件缓存是不同概念。由 SSD 支撑的专家读取可让整套文件大于常驻内存，但也会增加等待；这并不意味着任意小内存设备都能运行。请保留磁盘余量，并参考[已使用配置](INSTALL.md#4-看懂已经使用过的配置)。

量化发布页已经发生文件布局更新；其当前组件大小与历史本机整套占用不是同一口径。具体差异见 [INSTALL.md](INSTALL.md)；已有下载 revision／哈希现已补入[开发记录](DEVELOPMENT-NOTES.md#已保存的-225bpw-下载锁定信息)，逐请求验收绑定仍不完整。

## `--ssd-cache 12` 是占 12GB 固态硬盘吗？

不是。当前引擎的这个参数表示**系统 RAM 专家缓存预算**。它来自维护者 64GiB GPU + 64GiB 名义 RAM 配置，不能仅因名称含 `ssd` 就当作硬盘配额，也不是对所有内存划分都适用的最优值。启动参数、UMA 环境变量和 pack 配套应一起核对。

## 13.3、16.1、20.0 tokens/s 应该怎样理解？

- **13.3 tokens/s：**2.25bpw 桌面 UI 汇总显示的 13 次请求平均输出速度。保留界面报告口径，未根据可见行自行重算。
- **16.1 tokens/s：**同一组 2.25bpw 截图中的可见单次最高值。
- **20.0 tokens/s：**另一组 1.75bpw 历史记录中的 113-token 缓存短回复。

这些数字跨精度、输入长度与缓存条件，不能合成一个统一配置的保底区间。解码速度不等于整轮等待时间；首轮提示词处理、推理过程、客户端与工具等待都会影响体验。较慢结果、输入与复用数量、计时定义见 [BENCHMARKS.md](BENCHMARKS.md)。

## 1024K 就是已经跑过完整 1M 输入吗？

不是。1024K 是配置值。公开截图中可见的单次提示词达到 **56,532 tokens**，这不等于满 1M 输入，也不等于 DSH 端到端 1M 任务已通过。客户端历史压缩、输出预留、服务端实际容量等仍要同时满足。

## NVIDIA 的 GPU/RAM 划分是这个项目开发的吗？

不是。已测设备由 NVIDIA 应用提供这项硬件/驱动设置，改变划分可能需要重启。Strata 使用划分后的资源。64+64 是已有配置之一，不是普遍最优；也不能由 128GB 共享设备推算出总计 256GB 容量。

## 能给 DeepSeek Harness 提供本地模型吗？

可以，已有两轮基础聊天与缓存复用记录。Strata 提供本机 OpenAI 兼容 API，DSH 连接该接口。本地提供方的 Base URL、Model ID、历史统计以及**未随包发布的超时扩展前提**见 [DSH.md](DSH.md)。这证明一条本地推理路径，不表示具有 LM Studio 所有功能。

## 聊天接通，就证明 DSH 的工具、记忆、微信都能用了吗？

不能这样推断。它们分别涉及模型协议、客户端设置、工具权限或其他服务。本项目两轮聊天记录不覆盖完整工具任务、记忆整理、嵌入或微信集成。截图中的模型自述也不是实际调用证据。

## 本地部署就意味着所有内容永远不联网吗？

本项目的模型权重与推理位于本机，DSH 通过回环 API 连接。DSH 的搜索、插件、远程工具、遥测或另一个提供方仍可能按其配置联网。“本地模型”只说明这条模型推理路径，不能替整个客户端保证永不联网。

## DSH 设置一小时超时，为什么仍可能提前结束？

界面设置之外还有底层 HTTP、桌面 host 及客户端版本行为。维护者历史环境曾使用只针对回环提供方的传输扩展，公开包未包含该机器专用扩展；当前 DSH 精确版本与该扩展是否仍必需尚无公开结论。先看[历史前提](DSH.md#3-历史两轮聊天记录与复现前提)，不要把界面数字直接当作有效等待保证。

## 可以让有 API 或本地模型的 AI 帮我理解、诊断和适配吗？

可以把公开文档、实际设备信息及脱敏报错交给具备相应读写工具的 AI，先让它定位问题、引用依据、列出计划，再根据明确授权操作。有模型/API 不等于自动拥有终端、文件权限或构建工具；聊天 API 可调用也不保证某个 Agent 客户端支持所需协议。提示词是一种协作方法，不是安装成功或自主开发完成的证明。

可直接复用的协作提示词与适用边界见 [AI-ASSISTED.md](AI-ASSISTED.md)。公开开发依据见 [DEVELOPMENT-NOTES.md](DEVELOPMENT-NOTES.md)，开发史不以 AI 无来源的“回忆”补写。

## 这是官方版本、全网首个或所有 N1X 通用方案吗？

这是 **Zack_yzq 基于 Strata 的免费社区适配预览**，没有微软、NVIDIA、DeepSeek 或上游背书。已公开材料支持维护者单机的具体成果，不足以证明“全网第一”“唯一”“全设备兼容”或跨引擎性能领先。上游贡献与许可见 [README](../README.md) 和 [LICENSE](../LICENSE)。

## 文档更新会改变安装包或模型吗？

只修改说明文字、入口和已有记录的整理，不会自动改变既有安装程序、模型文件或 Release 附件。请以 Release 标签与对应校验值确认下载对象；仓库 `main` 上的文档可能比附件内文档更新。任何尚未完成的验证范围以 [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) 为准。

**English scope note:** This is a community preview tested on one Windows ARM64 N1X laptop. Quantized-model results do not establish original-precision quality, full-1M input capacity, comprehensive DSH tool support, universal device compatibility or vendor endorsement. Historical DSH results include a non-distributed timeout-extension prerequisite.
