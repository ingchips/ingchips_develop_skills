# 低功耗与 RTOS 协作

低功耗先查 `pg_power_saving_en`，再查目标芯片外设手册；RTOS 概念查 `freertos_manual`，SDK 集成和回调上下文查 `user_guide` / `pg_ble_stack_cn`。通用 FreeRTOS 文档不证明项目内核版本、配置或移植层行为。

- 睡眠/唤醒：确认模式、唤醒源、外设是否保留、时钟恢复、RAM 保留与待处理中断；区分芯片能力、板级功耗与软件策略。
- BLE 与外设共存：核实协议栈调度要求、唤醒时序、外设恢复和数据丢失风险，不照搬其他芯片的睡眠入口。
- ISR 与任务：确认调用上下文、可用的中断 API、优先级限制、阻塞条件和调度点；不能仅凭函数名猜测是否可在 ISR 使用。
- 缓冲区与消息：说明生产者/消费者、所有权交接、队列满处理、超时和重入；仅 `volatile` 不能作为完整同步方案。
- 功耗目标：给测量条件和建议检查点，不声称已测出功耗；本 skill 不控制仪器、不复位板卡、不运行固件。

建议检索：`sleep`、`wakeup`、`retention`、`ISR`、`FromISR`、`queue`、`task notification`。用 `--topic power` 或 `--topic rtos` 分别检索，混合问题按需补充两侧证据。
