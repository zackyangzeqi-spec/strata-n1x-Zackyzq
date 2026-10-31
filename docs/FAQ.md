# FAQ / 常见问题

**Can N1X run DeepSeek locally on Windows? / N1X 能在 Windows 本地运行吗？**

This preview has produced replies using the native Windows ARM64 CUDA engine on one 128GB N1X laptop with DeepSeek 1017 1.75/2.25bpw. It is evidence for that device/configuration, not a guarantee for all N1X machines. 本机已跑通，其他设备需要复测。

**Is this WSL or an LM Studio wrapper? / 是 WSL 或 LM Studio 转发吗？**

The released inference path is native Windows ARM64 CUDA. No WSL inference bridge or LM Studio server is required. The desktop/control stack includes an emulated x64 Python component. 原生指推理引擎，不代表所有依赖均为 ARM64。

**Why is a 2.25bpw download about 273.8GB? / 文件这么大，内存够吗？**

That is the whole bundle's decimal disk size, including experts/shared components. Disk storage, resident GPU allocations, expert RAM cache and OS file cache are different. SSD-backed expert access allows a larger bundle than resident memory, but can add latency. It is not a promise that any small-memory device can run it. Keep disk headroom and follow the tested configuration in INSTALL.

**What does 9.3–20.0 tokens/s mean? / 等待时间为什么仍可能很长？**

These are selected decode observations under different quantizations/cache states, not a single setup's guaranteed range. 2.25bpw desktop usage shows a reported 13-request average of 13.3 and a visible 16.1 maximum. The 20.0 sample is a shorter 1.75bpw reply. End-to-end time includes prompt processing, reasoning and tool waits. Read BENCHMARKS for slower cases and first-token definitions.

**Does NVIDIA memory allocation belong to this project? / 显存分配是你们开发的吗？**

No. On the tested device, the NVIDIA app offers the hardware memory split; changing it can require a reboot. Strata uses the resulting resources. 64+64 is a tested configuration, not a universal optimum. Do not infer aggregate 256GB capacity from a 128GB shared-memory device.

**Can it replace LM Studio for DeepSeek Harness? / 能给 DSH 提供模型吗？**

Yes, for the verified local inference workflow via the OpenAI-compatible loopback API. This is not feature parity with every LM Studio function. DSH tools, memory, third-party integrations and network access remain separately configured and tested. See DSH.md.

**Does 1024K mean one million tokens were tested? / 满 1M 测过吗？**

No. 1024K is the configured context ceiling. A supplied screenshot shows a 56,532-token prompt; that does not validate a full 1M input or a DSH end-to-end 1M workload. Client output reservations, history compression and server capacity must all agree.

**Is it official Strata or DGX Spark support? / 官方适配吗？**

It is a free community adaptation by Zack_yzq, derived from Strata. The tested Windows N1X laptop is not interchangeable with DGX Spark Linux or every NVIDIA GPU. No vendor endorsement or cross-engine superiority is claimed.
