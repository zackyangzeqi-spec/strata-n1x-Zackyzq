# 构建与复现边界

需要Windows ARM64、匹配的NVIDIA驱动、CUDA Windows ARM64工具链、MSVC ARM64、clang-cl、CMake、Ninja、Rust/Tauri和Node。已用CUDA13.4.1、CMake4.4.4；本包不分发这些软件。

优先在ASCII工程路径构建，避免NVCC诊断编码解析失败。上游仓库及其依赖按固定版本检出。已核当前ggml源的llama.cpp基线提交为`3cf03257f219afbe7334045ff7c6a06ac68c627d`；本次核对该依赖工作树无修改；全部工具链、干净构建与安装仍须复验，不能仅凭提交号视作已完全可复现。

在已配置ARM64编译环境下，CMake关键选项：
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
构建目标strata-dsv41，编译并行建议1，避免与推理争用内存。不要因本说明自动安装、关闭其他任务或加载模型。

引擎清单：`python tools/make_native_manifest.py --exe <strata-dsv41.exe> --library <strata_kq.dll> --out <host/server/n1x-native-build.json>`。它只为本机已有二进制生成哈希清单，不伪造上游签名、不修改官方组件安全检查。输出包含目标机器路径，仅留该机器，不提交Git。

桌面host依上游apps/host/package.json执行typecheck、build；桌面封装依apps/desktop的Tauri构建流程。当前安装包已使用明确授权的项目图标、独立应用ID/用户数据目录及关闭的官方更新源；独立干净账户的完整验收仍待进行。补丁以文本导出，另将本包 apps/ 中的三个 PNG/ICO 复制到检出树对应位置。

模型pack/运行配置需通过当前Strata准备流程生成。缓存参数为`--ssd-cache 12`（系统RAM专家缓存预算，非SSD容量），并发1，DSpark auto，max-context1048576；12GB只为本次64+64测试结果，其他配置需测算，不强行套用。
