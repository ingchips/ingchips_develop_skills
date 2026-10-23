<!-- an_libaudio_cn: 3 降噪 -->

# 3 降噪 {#ch-denoise}

降噪模块先将音频转换到频域，估计噪声谱，完成降噪，最后再转换到时域。 降噪模块每次处理一个音频帧，一个音频帧包含 `AUDIO_DENOISE_BLOCK_LEN` 个采样。 音频采样率支持 8 kHz、16 kHz，推荐使用 8 kHz。

## 3.1 使用方法 {#使用方法}

1. 初始化对象

   ```c
   audio_denoise_context_t *audio_denoise_init(
       void *buf,
       uint32_t sample_rate);
   ```

   `buf` 是用来存放对象的内存空间，其大小为 `AUDIO_DENOISE_CONTEXT_MEM_SIZE` 字节。
2. 处理音频

   ```c
   void audio_denoise_process(
       audio_denoise_context_t *ctx,   // 对象
       const int16_t *in,              // 音频输入
       int16_t *out,                   // 降噪输出
       void *scratch);                 // 临时内存
   ```

   `in`、`out` 各自包含 `AUDIO_DENOISE_BLOCK_LEN` 个采样。 降噪输出 `out` 可以与 `in` 相同，数据原地处理（in-place）。

   `scratch` 指向用来存放中间结果的内存空间，其大小为 `AUDIO_DENOISE_SCRATCH_MEM_SIZE` 字节。

一个降噪对象只能处理一个声道的数据。如果需要同时处理多个声道，则需要创建多个对象。 如果并发调用多个降噪对象的 `audio_denoise_process` 接口，那么各对象需要使用独立的 `scratch`； 如果顺序调用多个降噪对象的 `audio_denoise_process` 接口，那么可以使用同一块 `scratch` 内存，例如：

```c
audio_denoise_process(ctx_left_ch, ..., ..., scratch);
audio_denoise_process(ctx_right_ch, ..., ..., scratch);
```

## 3.2 资源消耗 {#资源消耗}

以下数据仅供参考。实际表现受编译器、Cache、RTOS、中断等因素影响。

### 3.2.1 ING916XX {#ing916xx}

当 CPU 主频为 112 MHz 时，调用一次 `audio_denoise_process` 大约需要 6 ms，或者说 `audio_denoise_process` 消耗的 CPU 频率约为 42 MHz。

## 3.3 应用建议 {#应用建议}

此降噪模块仅推荐用于 ADC 采集模拟麦克风信号的场景。