# 安装与使用 / Installation and Use

**适用对象：希望直接使用 Windows ARM64 安装包，在 N1X 笔记本上运行 DeepSeek 1017 的用户。**

[下载安装包](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq/releases/tag/v0.2.8-n1x.1) · [DeepSeek Harness 接入](DSH.md) · [已公开的运行记录](BENCHMARKS.md) · [常见问题](FAQ.md) · [让 AI 协助理解与适配](AI-ASSISTED.md) · [开发者：源码与构建](BUILD.md)

使用安装包时，按下面的顺序阅读即可。源码恢复、编译工具链和打包命令集中在 [BUILD.md](BUILD.md)。本页整理现有安装与运行方法，不代表本次文档更新进行了新的安装或模型测试。

## 1. 先确认设备与交付内容

| 项目 | 当前公开情况 |
|---|---|
| 已测设备 | 维护者的一台微软 N1X 笔记本，128GB CPU/GPU 统一内存 |
| 操作系统与引擎 | Windows ARM64；原生 Windows ARM64 CUDA DeepSeek 推理引擎 |
| 其他组件 | 桌面、Node、Python Control、Harness 与应用运行库随包提供；Control 仍使用 x64 Python 仿真，并非每个组件都是 ARM64 |
| 安装程序 | `strata_Zackyzq_0.2.8_arm64-setup.exe` |
| 另行准备 | 兼容的 NVIDIA 驱动、模型权重、足够的 SSD 空间 |
| 已有模型回复记录 | DeepSeek-V4.1-Flash-1017 的 1.75bpw 与 2.25bpw 社区量化版本 |
| 发布状态 | 未签名的社区实验性预览；其他设备、独立干净账户与完整干净源码构建尚未验证 |

**128GB 是系统与 GPU 共享的总容量。** NVIDIA 应用中的 GPU/RAM 划分由硬件及驱动提供，本项目使用划分后的资源。仅有“128GB 内存”不能据此判断普通 Windows x64 电脑、DGX Spark Linux 或其他设备兼容。

The installer includes the app and inference runtime, not model weights or GPU drivers. Native ARM64 refers to the inference engine; Control currently uses emulated x64 Python. This unsigned community preview is not an official Microsoft, NVIDIA, DeepSeek or upstream Strata release. Follow your operating system and organization policies.

## 2. 下载并安装桌面程序

1. 从 [v0.2.8-n1x.1 Release](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq/releases/tag/v0.2.8-n1x.1) 下载安装程序及 `SHA256SUMS.txt`，核对安装程序校验值。源码审阅 ZIP 面向开发者，不是普通用户安装的必需项。
2. 退出旧程序，备份聊天、设置与运行配置。已有模型权重可以留在原位置。选择可写的独立应用目录，不覆盖版本不明的安装。
3. 从桌面快捷方式启动 `strata_Zackyzq`，在模型页确认能够识别 Windows ARM64 CUDA DeepSeek 引擎。
4. 打开“设置 → 存储”，选择模型存储目录，再进入下一节准备模型。

社区版的默认用户数据目录是 `%USERPROFILE%\.strata_Zackyzq`，与上游版分开；旧聊天和密钥不会自动导入。卸载应用也不会自动删除模型或这个用户数据目录。

项目默认图标已获维护者授权公开分发。若需本机替代头像，可在用户数据目录内设置 `home\branding\avatar.png`；其他个人图片不会因此自动成为公开素材。

## 3. 选择模型来源并准备整套文件

本项目针对 **DeepSeek 官方于 2026-10-17 更新的 DeepSeek-V4.1-Flash-1017** 的社区量化版本。基础模型与实际下载权重是两层来源：

| 需要确认什么 | 公开入口与范围 |
|---|---|
| 基础模型身份 | [DeepSeek 官方更新记录](https://api-docs.deepseek.com/updates/)；[官方模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) |
| 社区量化权重 | [ISTA-DASLab / DeepSeek-V4.1-Flash-1017-GSQ-RCO-GGUF](https://huggingface.co/ISTA-DASLab/DeepSeek-V4.1-Flash-1017-GSQ-RCO-GGUF) |
| 项目已有回复记录的精度 | 1.75bpw、2.25bpw；2.00bpw 没有同等验收记录 |
| 已记录的 2.25bpw 整套磁盘占用 | 约 273.8GB，十进制；另留下载临时空间与系统余量 |
| 精确权重 revision、逐文件清单 | 既有下载锁定 revision／七文件哈希见[开发记录](DEVELOPMENT-NOTES.md#已保存的-225bpw-下载锁定信息)；逐次验收与该清单的绑定仍不完整，不能把站点最新文件当作已测文件 |

**文件布局有版本差异。** 截至 2026-10-31 查阅，量化发布页记载了 2026-10-27 的布局更新，并为 2.25bpw 的 IQ2_XS 列出 backbone 155.23GB、Engram 110.60GB，合计 265.83GB；vision 另列 0.97GB。这是上游当前页面的组件口径。维护者历史记录的 **273.8GB** 则是本机整套配套文件口径，两者不能直接互相替换，也不能据此声称当前上游文件已被本预览安装包验收。下载阶段锁定清单现已整理到开发记录；它不等于完整的逐请求权重绑定证明，本文不提供未经确认的跨版本拼接或链接命令。

### 已经有权重

在模型页选择 DeepSeek 1017 与对应量化，使用“使用你自己的 GGUF”指向已有的**整套文件目录**。已准备版本可以加载；未准备版本按程序的复用、完整性校验与准备流程完成，期间会生成 pack 配套信息。保留可复用文件，不必先删除再下载。

### 还没有权重

先查看上表中的量化仓库及其文件说明，再使用桌面的下载/准备入口。量化主文件、专家文件及所需 Engram/DSpark 等配套，应按所选版本的实际文件布局和当前准备流程核对；当前没有经过本预览包验收、适用于所有版本的通用文件清单。下载结束后仍需完成完整性校验、准备和加载。

**这里提供现有准备路径，未声称所有量化版本都完成了首次下载到首次回复的全流程验收。** 若缺少某个 revision 或配套文件的信息，先保留现状，依据错误提示和来源文件核对；不要用其他版本的同名文件拼凑。

Model weights are third-party quantizations of the named DeepSeek release. A completed download or ready-looking button is not evidence of successful inference. A historical download manifest is now summarized in DEVELOPMENT-NOTES; its binding to every inference acceptance remains incomplete; first-time preparation for every available variant is not certified.

## 4. 看懂已经使用过的配置

下面是维护者公开记录中的配置，便于理解现有结果。**它不是要求每台机器立即照改的默认最优方案。**

| 配置项 | 已记录配置 | 含义与注意事项 |
|---|---|---|
| 模型 | DeepSeek 1017，2.25bpw | 社区量化权重 |
| GPU / 系统内存划分 | 64GiB GPU + 64GiB 名义 RAM | 实际可见系统内存低于名义值；由 NVIDIA 设置控制 |
| 磁盘 | 内置 SSD | 273.8GB 为整套文件大小；逻辑分区不等于不同物理磁盘 |
| 专家 RAM 缓存 | `--ssd-cache 12` | 当前引擎中指系统 RAM 专家缓存预算，不是 12GB SSD 空间 |
| 专家与并发 | 完整 6 专家，单模型、单路 | 不应据此自行并行加载多个大模型 |
| 生成加速 | DSpark auto | N1X DeepSeek 分支的现行配置 |
| 上下文配置 | 1024K，即 1,048,576 tokens | 配置上限；没有满 1M 输入验收 |
| UMA 环境变量 | `DS4_COPY_GB=0`、`DS4_UMA_GPU_RESERVE_GB=8` | 已测配置的一部分，应与参数及 pack 一起理解 |

只复制可见启动参数而漏掉 UMA 环境变量，可能使 1024K 配置下的通用估算将 GPU 专家缓存算成零。当前准备流程仅在 Windows N1X 分支写入上述两个值；8GB 预留来自维护者短输入配置，并不保证满 1M 输入仍有足够余量。

若以后确需修改配置，先停止请求、卸载模型，再修改并重新加载。不要在推理进行中修改缓存、内存划分或模型配套；也不要仅为照抄本文而更改 NVIDIA 的系统内存划分。

## 5. 桌面聊天与 DeepSeek Harness

模型加载就绪后，可在 Strata 桌面新建聊天。已有运行记录说明，首轮处理系统提示词与工具上下文可能较慢；同会话缓存复用可能缩短后续等待。生成 tokens/s 与整轮等待时间请分开看，详细口径见 [BENCHMARKS.md](BENCHMARKS.md)。

使用 DeepSeek Harness（DSH）时，由 Strata 管理模型，DSH 连接本机 OpenAI 兼容 API：

| 字段 | 已记录值 |
|---|---|
| Base URL | `http://127.0.0.1:47831/v1` |
| 2.25bpw Model ID | `deepseek-v4.1-flash-ist-das-2.25bpw` |
| 端口 | 上述为桌面 host 默认端口；以本机实际地址为准 |
| API key | 已测回环连接无需云端密钥；客户端若强制非空，仅使用本机占位值 |

完整字段、历史两轮聊天记录和 **DSH 超时扩展前提**见 [DSH.md](DSH.md)。不要使用内部动态引擎端口。已有 DSH 会话不一定自动切换到新提供方；聊天、记忆整理、嵌入和其他功能有各自设置。

这条链路使用本机推理服务，无需 LM Studio 或 WSL 推理转发。DSH 的搜索、插件与远程工具是否联网，仍取决于客户端配置。服务保持回环监听即可；本流程不要求公网开放端口。

## 6. 停止、更新与常见问题

正常停止顺序为：停止生成 → 等待请求结束 → 卸载模型 → 退出应用。窗口关闭不一定代表进程与资源已经释放。若系统失去响应，可通过操作系统处理对应推理进程，同时注意未保存工作，不要无差别结束系统或其他应用。

| 现象 | 先核对什么 |
|---|---|
| 看不到引擎 | 核对安装版本、Windows 架构、文件哈希、依赖运行库与本机清单，并查看对应错误日志 |
| 找不到模型或外置盘掉线 | 盘符、完整文件及校验结果；恢复连接再准备，避免直接重复下载整套 |
| 首轮等待长 | 实际提示词长度、提示词复用、磁盘及其他负载；不能只看手打问题的字数 |
| 内存不足或系统卡慢 | 停止请求并查看资源，保留必要诊断；不要自动放大缓存或并行加载 |
| DSH 提前超时 | DSH 设置、桌面 host、底层 HTTP 各层；详情见 [DSH 历史条件](DSH.md#3-历史两轮聊天记录与复现前提) |

社区版未启用上游自动升级，更新前请备份本机设置并核对版本。不要混用来源不明的引擎。Windows 卸载器会保留安装目录之外的用户数据与模型；开发机卸载重装已有记录，独立干净账户与其他设备仍未验证。

Docker Linux Chromium 只覆盖页面与真实后端交互，不能证明 Windows 安装、GPU 推理或干净构建成功。完整范围见 [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md)。本安装包不分发上游可选的 Qwen experimental-speed-projection 控制向量，该功能不在本版发布和验证范围内。

The existing development-machine reinstall is not a clean-account or second-machine certification. Docker page checks do not establish Windows installer or GPU execution. No full-1M input, broad agent workflow, or universal hardware compatibility is claimed.
