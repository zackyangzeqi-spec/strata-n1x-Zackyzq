# strata-n1x-Zackyzq — DeepSeek on RTX Spark N1X laptops

**Windows ARM64 原生 CUDA · NVIDIA RTX Spark N1X 128GB 笔记本 · DeepSeek V4.1 Flash 1017 · Strata 社区适配**

[Download / 下载](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq/releases) · [Installation / 安装](docs/INSTALL.md) · [Benchmarks / 实测](docs/BENCHMARKS.md) · [Issues / 反馈](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq/issues) · [Optional support / 自愿支持](sponsorship/README.md)

面向新一代 NVIDIA RTX Spark N1X 笔记本的本地大模型桌面适配。截至 **2026-10-31**，DeepSeek 官方更新页列出的最新 Flash 更新为 **DeepSeek-V4.1-Flash-1017**；本项目测试的是它的第三方量化版本，并非原始全精度权重。应用显示名为 **strata_Zackyzq**，维护者为 **Zack_yzq**。

A community desktop adaptation for the new NVIDIA RTX Spark N1X laptop platform. As checked on **2026-10-31**, DeepSeek's official changelog lists **DeepSeek-V4.1-Flash-1017** as its latest Flash update. This project tests third-party quantizations of that release, not the original full-precision weights. App name: **strata_Zackyzq**; maintainer: **Zack_yzq**.

Sources: [NVIDIA RTX Spark specifications](https://www.nvidia.com/en-us/products/rtx-spark/specifications/) · [DeepSeek official changelog](https://api-docs.deepseek.com/updates/). These sources establish platform/version names, not certification of this community build.

Run DeepSeek 1017 locally through the Strata desktop on the tested NVIDIA N1X 128GB Windows ARM64 laptop. This community adaptation adds a native Windows ARM64 CUDA inference engine, desktop model lifecycle integration, N1X settings and monitoring, and a local OpenAI-compatible endpoint. It does not require LM Studio or a WSL inference bridge.

这是 **Zack_yzq** 为手中的微软 N1X 128GB 笔记本制作的个人适配：在 Windows ARM64 上，通过 Strata 桌面直接加载与运行 DeepSeek 1017，并提供本机 OpenAI 兼容接口。基于 [Niko1221/Strata](https://github.com/Niko1221/Strata)，不是官方发行版，也没有微软、NVIDIA 或 DeepSeek 的背书。

## 下载和开始 / Download and start

- 普通用户：使用 Release 中的 `strata_Zackyzq_0.2.8_arm64-setup.exe`，先阅读 [安装说明](docs/INSTALL.md)。它包含应用及推理运行库，**不包含模型权重或显卡驱动**。
- Developers: this repository contains the reviewed patch against upstream `870aedd9e1ebe1c91f94da93b59af17729f6c5c0`, authorized assets, and build guidance. It is not a second unrelated inference implementation. See [BUILD](docs/BUILD.md).
- 安装包未签名 / unsigned. Release status: **Experimental Preview**. Do not disable OS security to install it; verify the release checksum and your organization's policy.

## 功能与已测范围 / Features and tested scope

|项目 / Area|状态 / Status|
|---|---|
|Windows ARM64 CUDA DeepSeek engine|本机原生运行；not LM Studio or Linux forwarding|
|Desktop load/unload, model folder, avatar|本机已验 / tested on the development machine|
|DeepSeek 1017 1.75 / 2.25bpw|已有实际回复；2.00 未完成同等验收|
|Local OpenAI-compatible API / DSH|两轮基础聊天与缓存复用通过；工具、微信、记忆分别验收|
|1024K configured context|配置上限；**未验满 1M 输入**|
|Other N1X devices / clean-account build|未验证 / not verified|

当前实测配置为 64GiB GPU + 64GiB 名义系统内存、2.25bpw 内置 SSD、12GB 专家 RAM 缓存、完整 6 专家、DSpark auto。一次对照解码约 9.3 token/s；不同输入、缓存、草稿接受率和设备负载会影响结果，不承诺固定速度。See [measured results](docs/BENCHMARKS.md). First-run prompt processing can be much slower than a cached follow-up.

## 来源、反馈与支持 / Attribution, feedback and support

Code adaptation: **Zack_yzq**. Upstream Strata, Project Maya, ggml and dependency copyrights remain intact. Code licenses do not automatically cover proprietary CUDA/CRT runtimes or project/payment images. See [LICENSE](LICENSE), [asset terms](docs/ASSETS.md) and [release scope](docs/RELEASE-CHECKLIST.md).

项目免费，欢迎 GitHub Issues 反馈。自愿打赏不是使用或反馈的前提，也不购买技术支持或修复时限。[中英项目说明、免责声明、微信与支付宝 / Introduction, disclaimer and optional support](sponsorship/README.md).

请只提交脱敏的技术信息，不上传聊天、凭据、完整运行日志或个人资料。No model weights, private chats, credentials, user profiles, or old local Git history are distributed here.
