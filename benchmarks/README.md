# Public reproduction protocol / 公开复测步骤

This new prompt suite is provided for future independent tests. It has not been run for this publication update and did not generate the historical numbers in docs/BENCHMARKS.md.

1. Record the app release, native engine build, model quantization, OS/driver version, total memory and GPU/RAM split. Record model SSD location, expert RAM cache, DSpark and context settings. Do not publish serial numbers, usernames, private paths or credentials.
2. Use one already-loaded model, one request at a time. Do not silently stop unrelated tasks. Record load time separately from request time.
3. In a fresh desktop conversation, send each public prompt from prompts.json. Record exact prompt/reused/output token counts, first **engine** token, first **visible answer**, decode tokens/s, whole-request duration and resource peaks. Use null for unavailable measurements rather than estimating from word count.
4. Repeat a follow-up in the same conversation to test caching, clearly labeled warm. Repeat cold/warm trials at least three times where practical; report individual results and medians. A fresh conversation is not proof the OS file cache was cold.
5. Check answer quality: Chinese correctness; SQL half-open month boundary and deterministic tie break; Python tests and O(n) expected complexity. Speed without a usable answer is not a pass.
6. Share a sanitized result and relevant monitor screenshot through Issues. Do not upload private chats or raw runtime profiles. Do not claim 1M capacity from short requests.

逐项记录条件和冷／热状态；不要用字符数猜 token，不把首个思考 token 当作正文首字。测试程序和完整长上下文验收仍可后续补充，本次只交付固定题目与人工可复核流程。
