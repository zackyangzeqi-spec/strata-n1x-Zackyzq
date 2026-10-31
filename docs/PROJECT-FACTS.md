# 项目事实表 / Project facts

**文档核对日期：2026-10-31。** 本页用于快速判断项目身份、适用范围和证据来源。运行记录来自维护者已有公开资料，本次文档整理没有新增推理实验。

这里的 `[FACT]` 指来源明确支持的表述；对于项目运行情况，指“公开资料记载了该结果”，不代表本次另行复现。`[INFERENCE]` 表示推断；`[UNKNOWN]` 表示当前公开资料不足。

## 身份与用途

| 字段 | 当前事实 | 来源 |
|---|---|---|
| 项目 | Strata N1X / `strata-n1x-Zackyzq` | [仓库首页](../README.md) |
| 维护者 / 应用名 | Zack_yzq / `strata_Zackyzq` | [AUTHOR](../AUTHOR.md) |
| 上游 | Niko1221/Strata；适配补丁基线 `870aedd9e1ebe1c91f94da93b59af17729f6c5c0` | [BUILD](BUILD.md) |
| 目标 | NVIDIA RTX Spark N1X 128GB 统一内存笔记本，Windows ARM64 | [INSTALL](INSTALL.md) |
| 实测设备范围 | 维护者一台微软 N1X 128GB 笔记本；未扩展为所有 N1X 兼容承诺 | [已有实测](BENCHMARKS.md) |
| 模型正式名称 | **DeepSeek-V4.1-Flash-1017** | [DeepSeek 官方模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) |
| 模型官方更新日期 | **2026-10-17** | [DeepSeek 官方更新日志](https://api-docs.deepseek.com/zh-cn/updates/) |
| 实际权重路线 | 第三方 **ISTA-DASLab GSQ-RCO GGUF** 量化；不是本项目训练或发布的官方原精度权重 | [量化来源](https://huggingface.co/ISTA-DASLab/DeepSeek-V4.1-Flash-1017-GSQ-RCO-GGUF) |
| 已记录量化 | 1.75bpw 与 2.25bpw 有实际回复；2.00bpw 没有等价的本项目验收记录 | [BENCHMARKS](BENCHMARKS.md) |
| 推理与客户端 | 原生 Windows ARM64 CUDA 推理引擎；Strata 桌面；本机 OpenAI 兼容 API；DeepSeek Harness 为客户端 | [DSH](DSH.md) |
| 组件架构 | 推理引擎为 ARM64；控制层包含仿真的 x64 Python，不能写全栈原生 ARM64 | [INSTALL](INSTALL.md) |
| 当前发行 | `v0.2.8-n1x.1`，Experimental Preview，安装包未签名 | [Release](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq/releases/tag/v0.2.8-n1x.1) |

## 已有运行记录

| 状态 | 内容 | 证据及解释 |
|---|---|---|
| [FACT] | 本机桌面加载、卸载、实际回复与同机卸载重装有记录 | [发布检查范围](RELEASE-CHECKLIST.md)；同机测试不等于另一台无 SDK 机器验证 |
| [FACT] | 2.25bpw 截图 UI 汇总 13 次请求、平均输出 13.3 tokens/s | [请求截图](images/n1x-deepseek225-requests.png)；12 行可见，UI 聚合未重算 |
| [FACT] | 2.25bpw 的一条可见请求为 16.1 tokens/s、输出 1,108 tokens | 同图，提示词 51,824、复用 49,504、时长约 90s |
| [FACT] | 可见最大提示词为 56,532，复用 56,317 tokens | 同图；不等于 56,532 个全新 token 的无缓存处理测试 |
| [FACT] | 1.75bpw 的 113-token 缓存短回复为 20.0 tokens/s | [历史记录](BENCHMARKS.md)；与 2.25bpw 分开理解 |
| [FACT] | DSH 两轮基础聊天与缓存复用有历史记录 | [DSH 历史条件](DSH.md)；包含未随包发布的本地 HTTP 超时扩展 |
| [UNKNOWN] | DSH 当时具体版本、其他版本是否仍需要该扩展 | 公开资料尚未完整记录，不能使用官方建议版本填充 |
| [UNKNOWN] | 完整 1M 输入、广泛工具任务、长时间 Agent 稳定性、其他 N1X 机型 | 未见对应公开验收记录 |

## 配置、文件大小与版本边界

已有 2.25bpw 对照配置为：64GiB GPU + 64GiB 名义系统 RAM、内部 SSD、12GB 专家 RAM 缓存、六个专家、DSpark auto、单模型。截图中的 OS 可见系统 RAM 约 62GiB；它与名义分配值的口径不同。GPU/RAM 分配由 NVIDIA 控制面板设置，不由本项目重新创造。

`--ssd-cache 12` 在本引擎中表示**系统 RAM 的专家缓存预算**；不能按名称解释成 12GB SSD 空间。`DS4_COPY_GB=0`、`DS4_UMA_GPU_RESERVE_GB=8` 属于已记录 N1X 配置。1024K / 1,048,576 是配置上限，不构成完整 1M 输入测试。见 [安装与配置](INSTALL.md)。

仓库已有说明记载 **2.25bpw 本机整套配套文件约 273.8GB（十进制）**。2026-10-31 查阅的上游量化模型卡则列 **IQ2_XS 主干 155.23GB + Engram 110.60GB = 265.83GB**，并注明 2026-10-27 更新过文件布局。两者统计范围与版本不能直接等同；上游数值不是本预览包对最新文件布局的验收。既有下载 revision 与七文件哈希已整理到[开发记录](DEVELOPMENT-NOTES.md#已保存的-225bpw-下载锁定信息)；该下载阶段记录与每次推理验收之间的完整绑定仍未知。

## 本地服务示例

| 字段 | 现有示例 | 说明 |
|---|---|---|
| Base URL | `http://127.0.0.1:47831/v1` | 以本机 host 实际端口为准 |
| Model ID | `deepseek-v4.1-flash-ist-das-2.25bpw` | 本地服务 ID，保留原值；不能替换成官方云 API 调用名 |
| 权重位置 / 推理 | 本机文件 / 本机引擎 | DSH 远程工具、搜索、插件是否联网另由其配置决定 |

## 如何引用这个项目

推荐描述：

> 面向 N1X 128GB 笔记本的 DeepSeek-V4.1-Flash-1017 本地部署与 DeepSeek Harness 接入方案：基于 Strata 的社区适配，使用 Windows ARM64 原生 CUDA 推理引擎，提供安装包、说明与维护者已有运行记录。

English summary:

> A community Strata adaptation for quantized DeepSeek-V4.1-Flash-1017 on NVIDIA RTX Spark N1X 128GB Windows ARM64 laptops, with desktop model controls, native CUDA inference and a local OpenAI-compatible backend for DeepSeek Harness. Evidence is limited to the maintainer's documented environment.

本项目不主张“全网第一”、官方背书、原精度无损、所有组件原生 ARM64、稳定 20 tokens/s、满 1M 已验证或全部 Agent 工具已通过。了解原理与贡献见 [适配说明](DEVELOPMENT-NOTES.md)，需要自己的 AI 协助见 [可复用提示词](AI-ASSISTED.md)。
