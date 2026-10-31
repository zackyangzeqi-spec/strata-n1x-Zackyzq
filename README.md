# Strata N1X — DeepSeek on Windows ARM64

**NVIDIA RTX Spark N1X 128GB 笔记本 · 原生 CUDA · DeepSeek 1017 · DeepSeek Harness 本地接入**

[Download / 下载](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq/releases/tag/v0.2.8-n1x.1) · [Install / 安装](docs/INSTALL.md) · [Benchmarks / 实测](docs/BENCHMARKS.md) · [DSH setup / 接入](docs/DSH.md) · [FAQ](docs/FAQ.md) · [Issues / 反馈](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq/issues)

在 **Windows ARM64 的 NVIDIA N1X 笔记本**上，通过 Strata 桌面加载 DeepSeek V4.1 Flash 1017 本地量化模型，并把本机 OpenAI 兼容接口提供给 **DeepSeek Harness (DSH)**。这条推理链不需要 LM Studio，也不经过 WSL 推理转发。

Run **DeepSeek V4.1 Flash 1017 locally on Windows ARM64 / NVIDIA RTX Spark N1X**, with a native CUDA inference engine, Strata desktop controls, monitoring and a local OpenAI-compatible API for **DeepSeek Harness**. LM Studio is not required for this workflow.

**实测亮点 / Observed performance:** selected decode examples span **9.3–20.0 tokens/s across different quantizations and cache conditions**. The supplied **2.25bpw desktop session reports 13.3 tokens/s across 13 requests**, with **16.1 tokens/s** in a visible request; the **20.0** result is a separate **1.75bpw, 113-token cached reply**. These are observations, not a guaranteed range or cross-engine ranking. [Full conditions and slower results / 完整条件与较慢对照](docs/BENCHMARKS.md).

![DeepSeek 2.25bpw desktop monitoring on N1X](docs/images/n1x-deepseek225-monitor.png)

## 为什么使用 / Why use it?

- **Windows 原生推理 / Native inference:** ARM64 CUDA engine integrated into the desktop load/unload workflow. The bundled control layer still includes x64 Python under emulation; not every component is ARM64.
- **适配共享内存设备 / Shared-memory hardware:** works with the GPU/system-memory split configured in the NVIDIA app on the tested N1X device. This is a NVIDIA driver feature, not a memory-partitioning feature invented by this project. Splits tested include 92+36, 80+48 and 64+64 GiB nominal allocations.
- **本地模型服务 / Local model server:** Strata_Zackyzq can serve as the local inference backend for DSH instead of requiring a separate LM Studio server. Existing chats and tools remain the client's responsibility.
- **长上下文与缓存 / Context and caching:** 1024K configured context, prompt reuse and expert RAM caching. The supplied desktop screenshot shows a 56,532-token prompt with 56,317 tokens reused. **Full 1M input is not validated.** The server, DSH client and task each impose their own effective limits.
- **可观察 / Observable:** desktop monitoring separates decode speed, prefill, resources, prompt reuse and request duration. Faster token generation does not eliminate prompt processing or reasoning time.

## 下载和适用范围 / Download and scope

1. Read [installation instructions](docs/INSTALL.md), then download `strata_Zackyzq_0.2.8_arm64-setup.exe` from the linked **preview release**. Verify its SHA256. The installer includes the app and inference runtime, **not model weights or GPU drivers**.
2. Select your model directory and load a supported model in the desktop. The tested configuration is 128GB total shared memory, **64GiB GPU + 64GiB nominal RAM**, internal SSD, 2.25bpw, 12GB expert RAM cache, six experts and DSpark auto.
3. For DeepSeek Harness, follow [DSH setup](docs/DSH.md). Use the loopback endpoint; no public server is needed.

这是 **Zack_yzq** 为本人微软 N1X 128GB 笔记本制作的免费社区适配，应用显示名为 **strata_Zackyzq**。其他 N1X 笔记本尚无实体测试；不把 DGX Spark、其他 NVIDIA GPU 或 Windows x64 视作自动兼容。安装包未签名，当前为 **Experimental Preview**。

This free community adaptation was tested on the maintainer's Microsoft N1X 128GB laptop. Other N1X laptops, independent clean-account installation and full clean-source builds remain unverified. It is not an official Microsoft, NVIDIA, DeepSeek or Strata release. See [release scope](docs/RELEASE-CHECKLIST.md).

|Capability / 能力|Evidence / 验证边界|
|---|---|
|Windows ARM64 native CUDA, desktop load/unload|Tested on the development machine / 本机已测|
|DeepSeek 1017 1.75 and 2.25bpw|Actual replies; 2.00 has not had equivalent acceptance|
|DSH local API|Two basic turns and cache reuse verified; tool execution, WeChat and memory need separate acceptance|
|1024K context setting|Configured, not a full 1M-input test|
|Other devices and long-running workloads|Not certified / 未全面验证|

## NVIDIA allocation + DSH / 分配与接入展示

![N1X NVIDIA allocation, Strata monitoring and DSH client](docs/images/n1x-nvidia-strata-dsh.png)

The maintainer authorized this screenshot for publication. It illustrates the three interfaces together; it does not prove every capability claimed in the displayed model-generated reply. NVIDIA controls the hardware allocation; Strata serves inference; DSH orchestrates conversations and tools. See [DSH setup and limits](docs/DSH.md).

## 来源与贡献 / Attribution and contribution

Based on [Niko1221/Strata](https://github.com/Niko1221/Strata), with upstream Strata, Project Maya, ggml and dependency notices retained. This repository ships the reviewed adaptation patch against `870aedd9e1ebe1c91f94da93b59af17729f6c5c0`; see [BUILD](docs/BUILD.md). Adaptation maintainer: **Zack_yzq**.

[LICENSE](LICENSE) applies to the covered code; proprietary runtimes and project/payment images have separate terms in [ASSETS](docs/ASSETS.md) and third-party notices. This project does not claim ownership of upstream technology. Platform/version references: [NVIDIA](https://www.nvidia.com/en-us/products/rtx-spark/specifications/) · [DeepSeek](https://api-docs.deepseek.com/updates/).

项目免费。欢迎在 [GitHub Issues](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq/issues) 提交脱敏反馈，或通过 [微信／支付宝自愿支持](sponsorship/README.md)。打赏不是使用或反馈的前提，也不购买支持承诺。Optional support is welcome; it does not purchase services or response deadlines.

No model weights, credentials, private runtime profiles or old local Git history are distributed. The maintainer explicitly approved the project/payment images and three demonstration screenshots; the combined screenshot includes their chosen visible chat/profile content. Other private logs and conversations are excluded.
