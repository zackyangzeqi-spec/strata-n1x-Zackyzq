# Strata_Zackyzq — N1X Windows ARM64 个人适配版 / Personal Community Adaptation

## 中文

大家好，我是 **Zack_yzq**。

这个项目起初是为了适配我自己的电脑：让手中的**微软 N1X 笔记本（128GB 内存与显存共享、Windows ARM64）**，能够通过 Strata 桌面端更方便地运行本地大模型。现在取得了一些可用成果，希望整理出来，贡献给有同类设备和需求的朋友。

本项目基于 [Niko1221/Strata](https://github.com/Niko1221/Strata) 修改，沿用其桌面应用与推理框架，保留 Strata、Project Maya、ggml 等相关项目的版权、来源和许可证声明。感谢上游作者及贡献者的开放与付出。个人适配维护者为 **Zack_yzq**；各部分权利归相应权利人所有。本项目与微软、NVIDIA、DeepSeek 及 Strata 官方没有隶属或背书关系。

**目前仅在我手中这台128GB微软N1X设备上完成测试；其他N1X笔记本由于暂无实机，尚未验证兼容性。** 欢迎有设备的朋友参与测试和反馈。

已完成Windows ARM64原生CUDA引擎接入、Strata桌面模型加载与卸载、DeepSeek 1017的1.75bpw与2.25bpw运行，以及DSH通过本机接口完成基础聊天和同会话缓存复用。当前2.25bpw在64GB显存＋64GB名义系统内存、内部SSD、12GB专家内存缓存配置下，一轮桌面对照解码约9.3 token/s；DSH两轮约8.8和10.1 token/s。DSH首轮附带约3万token上下文，用时约3分47秒，缓存追问约19秒。以上是特定条件下的样本，不代表所有设备和任务的表现；1M上下文为配置容量，尚未完成1M实际输入验收。

**项目免费提供，个人为爱发电。** 无需付费或打赏即可按许可证使用本项目。若项目对你有帮助，欢迎通过下方微信或支付宝收款码自愿打赏，支持后续适配、测试和维护。量力而行；使用、反馈和参与贡献同样是支持。

如需联系，可以在赞助时备注或留言，简要说明来意及你愿意公开的联系方式（以支付平台实际支持的功能为准），也可以在本项目GitHub仓库提交Issue或在启用的Discussions中留言。**联系和反馈不以赞助为前提；赞助不代表购买技术支持、指定功能、优先响应或修复时限。** 个人维护时间有限，无法保证逐条回复。请勿在公开GitHub留言中上传完整付款凭证、密钥、个人住址或其他敏感信息。

### 使用说明与免责声明

本项目是业余维护的实验性社区适配版本，按现状提供。在适用法律允许的范围内，作者及贡献者不作明示或默示的质量、特定用途适用性或兼容性保证，对因使用、修改或分发软件产生的损失不承担责任，具体以随附许可证及适用法律为准。本说明不排除或限制依法不得排除或限制的责任。

使用前请备份重要数据，自行评估驱动、内存分配、存储空间和负载。模型输出可能有误，请自行核验；模型及其他依赖各自的许可和使用要求仍然适用。

感谢上游开源项目，也感谢愿意试用、反馈和贡献的每一位朋友。

— **Zack_yzq**

## English

Hello, I am **Zack_yzq**.

This project began as a personal adaptation for my **Microsoft N1X laptop with 128GB shared system/GPU memory, running Windows ARM64**. My goal was to make local large language models easier to use through the Strata desktop application. I am sharing the results with others who have similar devices and needs.

This community adaptation is based on [Niko1221/Strata](https://github.com/Niko1221/Strata). It builds on Strata's desktop application and inference framework and retains the copyright, attribution, and license notices of Strata, Project Maya, ggml, and the relevant dependencies. Thank you to the upstream authors and contributors. **Zack_yzq** maintains these adaptation changes; the respective rights remain with their owners. This project is not affiliated with or endorsed by Microsoft, NVIDIA, DeepSeek, or the official Strata project.

**Testing has covered only my own 128GB Microsoft N1X laptop. Other N1X laptops have not been verified because I do not currently have those devices.** Testing and feedback from other owners are welcome.

Completed tests include Windows ARM64 native CUDA integration, desktop model loading/unloading, DeepSeek 1017 at 1.75bpw and 2.25bpw, and basic DSH conversations with same-session prompt-cache reuse through the local endpoint. With 2.25bpw, a 64GB GPU / 64GB nominal system-memory split, internal SSD storage, and a 12GB expert RAM cache, one desktop comparison measured about 9.3 decoding tokens/s. Two DSH turns measured about 8.8 and 10.1 tokens/s. The first DSH turn included roughly 30K input tokens and took about 3 minutes 47 seconds; the cached follow-up took about 19 seconds. These are individual measurements under specific conditions, not performance guarantees. A 1M context is configured, but a full 1M-token input has not been validated.

**The project is provided free of charge and maintained in my spare time.** Payment or a tip is not required to use it under its license. If you find it useful, optional tips via the WeChat Pay or Alipay QR codes below help support further adaptation, testing, and maintenance. Please contribute only if you wish and can comfortably afford to. Feedback and code contributions are equally welcome.

To get in touch, you may leave a note or message with your contribution, briefly stating your purpose and any contact details you are comfortable sharing, where the payment platform supports this. You may also open an Issue in this project's GitHub repository or post in Discussions if enabled. **Contact and feedback do not require a contribution. Tips do not purchase technical support, a particular feature, priority responses, or a repair deadline.** As a spare-time maintainer, I cannot guarantee a response to every message. Please do not post complete payment receipts, credentials, home addresses, or other sensitive information publicly on GitHub.

### Use and disclaimer

This is an experimental, independently maintained community adaptation, provided as is. To the extent permitted by applicable law, the authors and contributors make no express or implied warranties regarding quality, fitness for a particular purpose, or compatibility, and accept no liability for losses arising from use, modification, or distribution, subject to the included licenses and applicable law. Nothing in this statement excludes or limits liability that cannot lawfully be excluded or limited.

Back up important data before use and assess your drivers, memory allocation, storage, and workload. Model outputs may be incorrect and should be checked independently. The licenses and usage requirements of models and other dependencies continue to apply.

Thank you to the upstream open-source projects and everyone who tests, reports issues, or contributes.

— **Zack_yzq**

## 自愿支持 / Optional support

| 支付宝 / Alipay | 微信 / WeChat Pay |
| --- | --- |
| ![支付宝 / Alipay](alipay.jpg) | ![微信 / WeChat Pay](wechat.png) |
