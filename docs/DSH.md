# DeepSeek Harness local setup / DSH 本地接入

```text
DeepSeek Harness (chat, tools, memory)
    -> http://127.0.0.1:47831/v1 (OpenAI-compatible API)
    -> Strata_Zackyzq desktop-managed native Windows ARM64 CUDA engine
    -> local DeepSeek 1017 weights
```

## Connect / 设置

1. Start Strata_Zackyzq, select the local DeepSeek 1017 model and load it. Wait until ready. 首先确认桌面本身能收到回复。
2. In DSH's custom OpenAI-compatible provider, use base URL `http://127.0.0.1:47831/v1`. Choose the actual ID returned by `/v1/models`; the tested 2.25 ID is `deepseek-v4.1-flash-ist-das-2.25bpw`.
3. The tested loopback setup has no cloud API key. If the client requires a nonempty placeholder, it is not an access credential. Do not enter or publish real cloud keys for this local endpoint.
4. Send a short message, then a follow-up in the same conversation. Verify the request and token reuse in Strata monitoring. Do not run a second copy of the same large model in LM Studio alongside it.

For this workflow, Strata serves the role of a local model server; LM Studio is not required. This does not assert that it replaces every LM Studio feature.

## Long context and privacy / 长上下文和本地边界

The tested engine is configured for 1,048,576 tokens (1024K). DSH's provider context setting must not exceed the loaded server setting, and history plus reserved output must fit. Client compression/output limits still apply. **Full 1M input and long-agent-task stability have not been accepted.** Do not simply disable every limit.

模型推理在本机进行；DSH 的搜索、插件、远程工具或其他供应商是否联网，由各自配置决定。因此“本地模型”不等于整个客户端永不联网。保持服务仅监听回环地址；本说明不要求公网开放端口。

Basic two-turn DSH chat and prompt reuse were verified. Tools, WeChat and memory are separate integrations, not implicitly covered by that check. The screenshot is a visual demonstration, not proof of all abilities described by the model itself.

![Native N1X allocation and DSH connection](images/n1x-nvidia-strata-dsh.png)

See [INSTALL](INSTALL.md), [BENCHMARKS](BENCHMARKS.md) and [FAQ](FAQ.md).
