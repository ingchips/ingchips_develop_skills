<!-- an_libaudio_cn: 9 语音变速 -->

# 9 语音变速 {#ch-stretch}

音频处理库提供了语音变速功能，可把语音在时域上拉长或则缩短，而语音的采样率、基频以及共振峰保持不变。

## 9.1 使用方法 {#使用方法-6}

1. 确定参数

   确定采样率（如 16kHz）和要关注的基频范围（例如 `STRETCH_DEF_FREQ_RANGE`：55 ~ 333 Hz）。本模块要求：

   - 采样率 / 基频下限 < 2400
   - 采样率 / 基频上限 > 24

   或者说，基频不能超出 [采样率 / 2400, 采样率 / 24]。
2. 初始化变速器对象

   ```c
   struct stretch_ctx_t *stretch_init(
       int sampling_rate,   // 采样率
       int lower_freq,      // 基频下限
       int upper_freq,      // 基频上限
       int flags,           // 标志位
       void *buf);          // 上下文内存
   ```

   标志位 `flags` 是 `STRETCH_..._FLAG` 各种常量的组合，可以为 0。`buf` 是用来存放语音变速器对象上下文的内存，其大小通过 `stretch_get_context_size` 获得。
3. 分配用来接收变速输出的内存

   本模块采用流式处理，假设每次最多输入 `max_num_samples` 个采样，则变速器每次输出的采样数至多为：

   ```c
   int stretch_get_output_capacity(
       struct stretch_ctx_t *ctx,  // 变速器对象
       int max_num_samples,
       float min_speed);
   ```

   其中 `min_speed` 是最小速度。速度近似为原始长度与处理后的语音长度的比值，1.0 为无变化， 大于 1.0 为压缩（加速），小于 1.0 为拉伸（减速）。

   根据 `stretch_get_output_capacity` 返回的最大采样数可为输出分配足够的内存（每个采样为一个 `int16_t`）。
4. 处理语音

   通过 `stretch_samples` 处理一小段语音数据。这个函数返回的是本次处理所输出的采样的个数。

   ```c
   int stretch_samples(
       struct stretch_ctx_t *ctx,  // 变速器对象
       const int16_t *samples,     // 输入的采样
       int num_samples,            // 输入的采样的个数
       int16_t *output,            // 输出
       float speed);               // 本次处理使用的速度
   ```
5. 刷新数据

   使用 `stretch_flush` 输出剩余数据。这个函数返回的是所输出的采样的个数。

   ```c
   int stretch_flush(
       struct stretch_ctx_t *ctx,  // 变速器对象
       int16_t *output);           // 输出
   ```
6. 复位

   使用 `stretch_reset` 复位变速器，为处理下一段语音做好准备。

   ```c
   void stretch_reset(
       struct stretch_ctx_t *ctx); // 变速器对象
   ```

借助变速功能还可实现语音变调（只改变音调，时域长度不变），例如：

1. 将 16kHz 采样的音频直接以 8kHz 播放，音调降低，但时长也被拉长到 2 倍；
2. 使用变速功能将速度变为 2 倍，则时长与原音频保持一致。

## 9.2 资源消耗 {#ch-stretch-resources}

以下数据仅供参考。实际表现受编译器、Cache、RTOS、中断、音频数据等因素影响。

内存占用与参数有关，例如：

```c
stretch_get_context_size(16000, STRETCH_DEF_FREQ_RANGE, 0) == 1788 (字节)
```

使用上述参数，并且 `max_num_samples` 取做 `AMR_WB_PCM_FRAME_16k`，不同 `min_speed` 设置下的 `stretch_get_output_capacity()` 返回的内存大小如表 [9.1](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-stretch.html#tab:ch-stretch-output-capacity)

*表 9.1: 为输出预留的内存空间的大小*
| 最小速度 | 为输出预留的内存（字节） |
| --- | --- |
| 0.6 | 3026 |
| 0.8 | 2706 |
| 1.2 | 2386 |
| 1.4 | 2386 |

提示：用于 TTS 变速时，请留意 `tts_get_scratch_mem2_size()` 的大小， 如果足以容纳变速器的输出，则可考虑复用。

### 9.2.1 ING916XX {#ing916xx-6}

在上述参数下，生成 `AMR_WB_PCM_FRAME_16k` 个采样，需要的平均时间可参考表 [9.2](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-stretch.html#tab:ch-stretch-performance)。

减小基频范围可缩短处理时间。

*表 9.2: 特定参数下语音变速时间消耗参考值*
| 速度 | 时间消耗 (ms) |
| --- | --- |
| 0.6 | 5.9 |
| 0.8 | 5.8 |
| 1.2 | 8.8 |
| 1.4 | 10.1 |
| 1.6 | 11.5 |