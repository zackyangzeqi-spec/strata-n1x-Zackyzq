# 源码恢复、构建与复现边界 / Source and Build

**本页面向开发者。** 直接安装桌面程序请阅读 [INSTALL.md](INSTALL.md)。本仓库交付固定上游基线上的适配补丁、授权素材和文档，不是已验证能在任意干净环境一键构建的完整源码树。

以下整理已有构建信息，保留未验证边界；本次文档更新没有执行编译、模型测试或重新打包。

## 1. 固定上游与适配包

| 项目 | 公开基线 |
|---|---|
| 上游仓库 | [Niko1221/Strata](https://github.com/Niko1221/Strata) |
| 上游 commit | `870aedd9e1ebe1c91f94da93b59af17729f6c5c0` |
| 适配补丁 | [`patches/n1x-windows-arm64.patch`](../patches/n1x-windows-arm64.patch) |
| 已记录的 ggml / llama.cpp 基线 | `3cf03257f219afbe7334045ff7c6a06ac68c627d` |
| 公开交付状态 | Experimental public source patch；完整干净构建未验收 |

已公开记录说明当时核对的 ggml 依赖工作树无修改；这不是对未来检出的依赖状态、工具链或干净构建成功的保证。

## 2. 在新的开发目录恢复源码

先取得完整公开适配包或本仓库文件，保留目录结构。以下 PowerShell 命令在**新建开发目录**运行，需要先有 Git；`PATCH_FILE` 替换为公开补丁的绝对路径。不覆盖已有安装目录或版本不明的源码。

```powershell
git clone https://github.com/Niko1221/Strata.git Strata-N1X-source
Set-Location Strata-N1X-source
git checkout 870aedd9e1ebe1c91f94da93b59af17729f6c5c0
git apply --check "PATCH_FILE"
git apply "PATCH_FILE"
```

用途是恢复固定基线并应用适配补丁；完成标志是检出目标 commit，补丁检查与应用均成功。如果基线不匹配或补丁检查失败，停止后续步骤，保留报错并核对来源，不强行应用或自动更换上游版本。

补丁为文本格式，另将本公开包中的以下三个授权素材复制到检出树的同名位置：

- `apps/desktop/src-tauri/icons/icon.ico`
- `apps/desktop/src-tauri/icons/icon.png`
- `apps/host/public/brand/project-avatar.png`

素材用途与许可见 [ASSETS.md](ASSETS.md)。其他个人图片、私有运行配置、密钥及聊天记录不属于源码恢复材料。

## 3. 工具链与依赖

需要 Windows ARM64、兼容 NVIDIA 驱动、Windows ARM64 CUDA 工具链、MSVC ARM64、clang-cl、CMake、Ninja、Rust/Tauri、Python 和 Node。已记录使用 **CUDA 13.4.1、CMake 4.4.4**；当前 host 要求 **Node ≥ 24.12.0**。本公开适配包不分发这些开发工具。

优先使用 ASCII 工程路径，避免 NVCC 诊断编码解析失败。工具链与依赖应按固定基线核对；本页不是自动安装脚本，也不要求停止其他任务或加载模型。

依赖准备、模型 pack 生成和桌面封装尚未整合成完整自动流程。遇到锁文件不匹配等问题，先确认基线和依赖来源，不为让命令通过而擅自升级依赖或绕过检查。

## 4. 原生引擎关键构建参数

在已配置 ARM64 编译环境下，已有记录使用以下 CMake 选项。尖括号项须替换为真实本机工具链/依赖路径；这些是关键选项，不是完整可复制的端到端构建命令。

```text
-G Ninja
-DCMAKE_BUILD_TYPE=Release
-DCMAKE_SYSTEM_PROCESSOR=ARM64
-DCMAKE_C_COMPILER=<clang-cl>
-DCMAKE_CXX_COMPILER=<clang-cl>
-DCMAKE_CUDA_COMPILER=<CUDA>/bin/nvcc.exe
-DCMAKE_CUDA_HOST_COMPILER=<MSVC-ARM64-cl>
-DCUDAToolkit_ROOT=<CUDA>
-DCMAKE_CUDA_ARCHITECTURES=121
-DCMAKE_CUDA_FLAGS=-Xcompiler=/utf-8
-DSTRATA_ENABLE_CUDA=ON
-DSTRATA_BUILD_DSV41=ON
-DSTRATA_BUILD_TESTS=OFF
-DSTRATA_WINDOWS_ARM64_CLANG19_SEH_WORKAROUND=ON
-DSTRATA_GGML_DIR=<pinned-ggml-source>
```

目标为 `strata-dsv41`。已有建议使用编译并行度 1，避免与推理争用内存。是否具备正确 SDK、路径与依赖，需要根据实际开发环境确认，不能仅凭参数文本认定编译成功。

## 5. host 与桌面构建入口

依赖准备好后，已有文档确认的脚本入口如下；完整干净构建仍未验收。

| 目录 | 已记录脚本 | 用途 |
|---|---|---|
| `apps/host` | `npm ci` | 按锁文件准备 host 依赖 |
| `apps/host` | `npm run typecheck` | 类型检查 |
| `apps/host` | `npm run build` | host 构建 |
| `apps/desktop` | `npm ci` | 按锁文件准备桌面依赖 |
| `apps/desktop` | `npm run build` | 按该基线桌面脚本进行构建 |

桌面封装依 `apps/desktop` 的 Tauri 流程。现有发行包使用已授权图标、独立应用 ID 与用户数据目录，并关闭上游自动更新源；独立干净账户的完整安装验收尚未完成。

## 6. 真实二进制清单与模型运行配置

本仓库提供 [`tools/make_native_manifest.py`](../tools/make_native_manifest.py)，仅为**本机已经存在的真实产物**生成哈希清单：

```text
python tools/make_native_manifest.py --exe <strata-dsv41.exe> --library <strata_kq.dll> --out <host/server/n1x-native-build.json>
```

该命令从提供脚本的适配仓库目录调用；尖括号替换为真实路径。输出可能含目标机器路径，只留该机器，不提交 Git。它不生成上游签名，也不替代组件校验。缺少产物时不能伪造清单或跳过检查。

模型 pack 与运行配置通过对应 Strata 准备流程生成。已有配置包含 `--ssd-cache 12`（系统 RAM 专家缓存）、单路、6 专家、DSpark auto、`max-context` 1,048,576，以及 Windows N1X 的 `DS4_COPY_GB=0`、`DS4_UMA_GPU_RESERVE_GB=8`。参数、环境变量与 pack 需要一起核对；12GB 缓存与 8GB 预留来自特定本机配置，不是所有设备或满 1M 负载的保证。详见 [INSTALL.md](INSTALL.md)。

## 7. 复现与发行范围

可以确认的事实与仍未知的结果应分开记录。源码补丁可被检查、命令名称存在、开发机曾生成安装包，分别不等于完整干净构建、独立机器安装或满 1M 运行都已通过。

当前发布边界见 [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md)。本页提供开发入口；实际运行结果应以对应版本的记录为准。

This repository supplies a patch against a pinned upstream revision plus authorized assets and documentation. A full clean-source build and independent clean-account installation remain unverified. Do not fabricate manifests, bypass component checks, or treat Docker page validation as proof of native Windows installation or GPU inference.
