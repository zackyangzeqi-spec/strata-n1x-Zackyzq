# 安装与使用 / Installation and Use

## 1. 当前交付与适用范围 / Package status and scope

提供 Windows ARM64 桌面安装程序 `strata_Zackyzq_0.2.8_arm64-setup.exe`，以及独立的源码补丁审阅包。安装程序包含桌面、Node、Python Control、Harness、本机编译的 ARM64 CUDA DeepSeek 引擎及其随应用运行库；不含模型权重或 NVIDIA 驱动。Node/Python 等依赖的架构不都为 ARM64；当前 Control 使用 x64 Python 仿真。安装包未签名，是个人实验性适配版，不是微软、NVIDIA 或上游官方发行版。

The Windows ARM64 desktop installer is `strata_Zackyzq_0.2.8_arm64-setup.exe`; the source-patch review archive is separate. The installer includes the desktop, Node, Python Control, Harness, a locally built ARM64 CUDA DeepSeek engine and app-local runtime libraries. Model weights and NVIDIA drivers are not included. Not every dependency is ARM64; Control currently uses emulated x64 Python. This unsigned experimental community build is not an official Microsoft, NVIDIA, or upstream release.

安装前退出旧程序并备份聊天、设置及运行配置，模型权重原位保留。运行安装程序，选择可写的独立应用目录。不要覆盖未知版本。安装后从桌面快捷方式启动，先确认模型页识别 Windows ARM64 CUDA DeepSeek 引擎，再选择“使用你自己的 GGUF”并指向已有整套文件。首次准备会校验完整性并生成小型 pack 配套；不要把“下载并加载”按钮或界面就绪当成已经通过推理验收。

Before installation, quit the old app and back up chats, preferences and run configurations; retain weights in place. Run the installer and select a writable, separate application directory. Do not overwrite an unknown build. Launch the desktop shortcut, confirm the Windows ARM64 CUDA DeepSeek engine on Models, then use your own GGUF folder. Initial preparation verifies integrity and produces pack metadata; an enabled button or ready-looking page does not prove inference works.

社区版用户数据默认在 `%USERPROFILE%\.strata_Zackyzq`，与旧版数据分开；不会自动导入旧聊天或密钥。默认项目图标为维护者明确指定并授权随发行包公开的图片；用户也可在该目录下 `home\branding\avatar.png` 设置本机替代头像。其他个人图片不自动打包。卸载应用不等于删除模型或这个用户数据目录。源码构建与补丁应用见下一节。

Community user data defaults to `%USERPROFILE%\.strata_Zackyzq`, separate from upstream data. Old chats and keys are not imported automatically. The default project icon is the maintainer-supplied image explicitly authorized for public distribution. An optional local replacement can be placed at `home\branding\avatar.png`; other personal images are not bundled automatically. Uninstalling the app does not delete weights or this user-data folder. Source builds and patch application are described below.

验收边界：Docker Linux Chromium 只验页面与真实 Windows 后端交互，不能运行 Windows 安装器或证明 Windows GPU 推理。Windows 安装、桌面加载、实际回复、退出释放资源分别记录；同一台开发机的重装不等于干净账户、无 SDK 的另一台机器验收。其他 N1X 设备未实测；1024K 是配置上限，尚未验满 1M 输入。

Validation boundaries: Docker Linux Chromium checks pages against the real Windows backend; it does not execute the Windows installer or establish Windows GPU inference. Native installation, desktop loading, actual answers and resource release are separate checks. Reinstallation on the development machine is not a clean-account or SDK-free second-machine test. Other N1X devices are untested; 1024K is a configured maximum, not a validated full-1M input workload.

已测试：128GB微软N1X、Windows ARM64。准备兼容的NVIDIA驱动、足够的内部SSD空间及模型文件；其他设备未验证。128GB为系统与GPU共享总容量，不是各有128GB。

Tested: a 128GB Microsoft N1X laptop running Windows ARM64. Compatible NVIDIA drivers, sufficient internal SSD storage, and model files are required. Other devices are unverified. The 128GB is the shared total, not 128GB for each pool.

## 2. 源码准备 / Source preparation

先解压整个预览包，保留目录结构。以下PowerShell命令在新建的开发目录运行；安装Git后执行，`PATCH_FILE`需替换为解压后的补丁绝对路径。不要覆盖已有官方版或未知版本。

Extract the complete preview while preserving its folder structure. Run these PowerShell commands in a new development directory with Git installed. Replace PATCH_FILE with the extracted patch's absolute path. Do not overwrite an existing installation or an unknown revision.

```powershell
git clone https://github.com/Niko1221/Strata.git Strata-N1X-source
Set-Location Strata-N1X-source
git checkout 870aedd9e1ebe1c91f94da93b59af17729f6c5c0
git apply --check "PATCH_FILE"
git apply "PATCH_FILE"
```

先读BUILD.md，再准备Windows ARM64 CUDA、MSVC ARM64、clang-cl、CMake、Ninja、Rust/Tauri、Python和Node（当前host要求Node>=24.12.0）。引擎构建参数及本机哈希清单生成命令见BUILD.md。本包未将引擎依赖安装、模型pack准备和应用封装整合成全自动流程，这些仍是发布前验收项；不要伪造引擎清单或忽略组件校验。

Read BUILD.md before preparing Windows ARM64 CUDA, MSVC ARM64, clang-cl, CMake, Ninja, Rust/Tauri, Python, and Node (the current host requires Node >=24.12.0). BUILD.md documents engine flags and the machine-local hash manifest tool. Dependency setup, model-pack preparation, and desktop packaging are not yet integrated into a fully automated process and remain release gates. Do not fabricate manifests or bypass component checks.

源码依赖准备后，可在apps/host中执行`npm ci`、`npm run typecheck`、`npm run build`；apps/desktop中执行`npm ci`、`npm run build`。这些脚本名称已与当前package.json核对，完整干净构建尚未验收。若当前依赖锁文件与npm ci不匹配，先确认基线，不擅自改依赖版本。

After prerequisites are ready, use `npm ci`, `npm run typecheck`, and `npm run build` in apps/host; use `npm ci` and `npm run build` in apps/desktop. Script names have been checked against the current package.json files; a complete clean build remains unverified. If npm ci reports a lock mismatch, confirm the baseline rather than changing dependency versions blindly.

## 3. 桌面准备模型 / Prepare a model in the desktop app

打开适配后的桌面程序，进入设置→存储，选择模型目录；保留已有可复用文件。进入模型页选择DeepSeek 1017及量化版本。已准备版本点击“加载模型”；未准备版本走下载/复用→完整校验→准备→加载。下载完成不等于已准备或已加载。其他版本的首次下载/准备全链路仍待单独验收。

Open the adapted desktop app, choose a model directory under Settings → Storage, and retain reusable files. Select DeepSeek 1017 and its quantization in Models. Load prepared versions directly; unprepared versions must complete download/reuse, integrity checks, preparation, and loading. Download completion alone does not mean prepared or loaded. First-time preparation of other versions still requires independent validation.

当前可复用配置：2.25bpw、内部SSD、64GB显存＋64GB名义系统内存、专家RAM缓存12GB、完整6专家、单模型、DSpark自动。请先核本机负载，不同时加载多个大模型。不要仅为照抄本例就改系统内存划分。2.25整套文件约273.8GB（标称十进制），另留下载临时空间、构建空间与系统余量。分区不等于不同物理磁盘。

The measured configuration is 2.25bpw on an internal SSD, a 64GB GPU / 64GB nominal system-memory split, a 12GB expert RAM cache, all six experts, one model, and automatic DSpark. Check existing workload before loading. Do not change your system partition solely to copy this example. The complete 2.25 file set is approximately 273.8GB in decimal units; allow additional temporary download/build space and system headroom. Partitions are not separate physical drives.

N1X DeepSeek页的上下文固定为1024K配置，生成加速为自动DSpark。它不代表已测满1M输入或所有任务可稳定运行。专家缓存参数`--ssd-cache 12`在当前引擎中指系统RAM专家缓存预算；名字含ssd不代表12GB固态空间。仅在模型卸载后更改配置，再重新加载并核参数；不要边推理边改。

N1X 的已测配置还包含 `DS4_COPY_GB=0` 和 `DS4_UMA_GPU_RESERVE_GB=8`。启动参数、环境变量和 pack 必须一起核对；只复制可见参数会遗漏 UMA 专家预算，使 1024K 配置把 GPU 专家缓存估为零。新版准备流程只在 Windows N1X 分支写入这两项，不改变其他设备默认值。8GB 是本机短输入实测配置，不保证满 1M 输入仍有足够余量。

The measured N1X configuration also includes `DS4_COPY_GB=0` and `DS4_UMA_GPU_RESERVE_GB=8`. Check arguments, environment and pack together: copying arguments alone can leave the generic UMA estimate reserving all GPU expert capacity at 1024K. Preparation writes these values only on Windows N1X. The 8GB value is tested on this machine with short inputs, not a guarantee for full-1M workloads.

The N1X DeepSeek branch fixes the configured context at 1024K and generation acceleration to automatic DSpark. This does not validate full-1M input or all workloads. In the current engine, `--ssd-cache 12` is an expert system-RAM cache budget, not a 12GB SSD allocation. Unload before changing configuration, then reload and verify the effective parameters.

## 4. 聊天与DSH / Chat and DSH

等待模型就绪后新建聊天，先用简单问题验证，再处理文件或长任务。首次请求会读取系统提示词和工具上下文；相同会话的缓存复用可能缩短后续等待，但不保证固定速度。

Wait until the model is ready, start a new chat, and verify a simple question before file or long-running work. The first request processes system/tool context; same-session cache reuse may reduce later waiting, without a fixed-speed guarantee.

DSH连接参数和范围见DSH.md。默认Base URL为`http://127.0.0.1:47831/v1`，模型ID为`deepseek-v4.1-flash-ist-das-2.25bpw`。核对本机实际端口，先在Strata加载，再在DSH选对应提供商与模型。不要填写内部动态引擎端口；本机配置和凭据不提交Git。DSH记忆、嵌入、微信和工具任务需要各自验收。

See DSH.md for configuration and limits. The default base URL is `http://127.0.0.1:47831/v1`; the model ID is `deepseek-v4.1-flash-ist-das-2.25bpw`. Confirm the actual host port, load in Strata first, then select that provider/model in DSH. Do not use the private dynamic engine port or commit local settings/credentials. Memory, embeddings, WeChat, and tool tasks need separate validation.

## 5. 停止、更新与问题处理 / Stop, update, and troubleshooting

停止生成后等待请求结束，再卸载模型，最后退出应用。进程仍在或资源未释放时，不能只凭窗口关闭就认定已退出。系统失去响应时使用操作系统结束相关推理进程，注意未保存工作；不要无差别终止系统或其他应用。

Stop generation, wait for requests to finish, unload the model, then quit. A closed window does not prove that the process exited or resources were released. If unresponsive, use the operating system to end the relevant inference process, taking care of unsaved work; do not indiscriminately terminate system or unrelated processes.

- 无引擎：核Windows ARM64、实际构建产物、本机清单哈希和依赖；禁止用假清单消除提示。
- 缺模型/外置盘掉线：核盘符、完整文件和校验结果，恢复连接后再准备；不要直接重新下载全部文件。
- 首轮慢：核实际输入长度、缓存、磁盘及其他负载；不要只看用户输入的字数。
- 内存不足或卡慢：先停止生成并核资源，保留诊断；不自动放大缓存、改内存划分或并行加载。
- 超时：核DSH、桌面host和底层HTTP各层；大上下文配置不自动解决超时。

- No engine: verify Windows ARM64, actual build artifacts, local manifest hashes, and dependencies. Never fabricate a manifest to hide the warning.
- Missing model/disconnected external drive: check drive identity, complete files, and hashes; reconnect and prepare again instead of redownloading everything.
- Slow first turn: check actual prompt size, cache, disk, and competing workload, not just the typed question's length.
- Low memory/sluggish system: stop generation and inspect resources; do not automatically increase caches, repartition memory, or load in parallel.
- Timeout: inspect DSH, desktop-host, and underlying HTTP layers. A larger context setting does not resolve timeouts by itself.

当前安装包提供 Windows 卸载器；应用数据与模型在安装目录之外，卸载时保留。开发机已完成卸载与重装测试，独立干净账户和另一台机器尚未验证。社区版未启用自动升级，避免被上游安装包覆盖。更新前备份本机设置，核基线与补丁匹配；不要混用未知引擎。Docker 的页面检查不能代替 Windows ARM64 安装与 N1X GPU 推理验收。

The installer includes a Windows uninstaller. User data and model weights outside the installation directory are retained. Uninstall/reinstall was tested on the development machine; an independent clean account and another machine remain untested. Community automatic updates are disabled to avoid replacement by an upstream package. Back up settings and check revision compatibility before updates. Docker page checks do not replace native Windows installation and N1X GPU inference tests.

本 N1X/DeepSeek 安装包不分发上游可选的 Qwen experimental-speed-projection 控制向量；该功能不属于本次验证或发布范围。
This N1X/DeepSeek installer excludes the optional Qwen experimental-speed-projection control vector; that functionality is outside this release and its validation scope.
