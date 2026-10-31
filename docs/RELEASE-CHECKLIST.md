# Release scope / 发布检查范围

- [x] MIT upstream and adaptation notices retained; Project Maya / ggml attribution retained.
- [x] Native runtime manifest and static payload hashes checked; Node, Python, Harness and bundled dependency notices retained.
- [x] App identity and user-data root separated; upstream auto-update disabled; model weights excluded.
- [x] Known private marker scan, authorized image hashes, patch application against pinned upstream checked.
- [x] Development-machine Windows install, unload/load, desktop answers and cache reuse tested. Docker checks cover web pages only.
- [ ] Independent clean-account / SDK-free second-machine test.
- [ ] Full clean source build from this public patch, all prerequisites and packaging recipe.
- [ ] Other N1X hardware, full 1M input, broad task/coding stability.
- [ ] Signed installer and verified community update channel.

发布定位：Experimental Preview；以上未验项是明确限制，不写成已通过。最终安装文件的校验值随 Release 附件提供。版权和许可逐组件适用；用户指定项目图及收款图仅用于本项目展示/支持，不属于代码 MIT 许可。

This is an experimental preview, not a general compatibility certification or a performance guarantee. Final release assets include checksums. A same-machine reinstall does not establish clean-machine reproducibility. The app is free; optional tips do not purchase services. No absolute legal immunity is promised.
