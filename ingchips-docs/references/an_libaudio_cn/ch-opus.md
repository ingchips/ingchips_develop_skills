<!-- an_libaudio_cn: 6 Opus 编码 -->

# 6 Opus 编码 {#ch-opus}

Opus 支持窄带（4 kHz）、中等带宽（6 kHz）、宽带（8 kHz）、超宽带（12 kHz）、全带宽（24 kHz）等多种音频带宽， 支持 2.5 ms、5 ms、10 ms、20 ms、40 ms、60 ms、80 ms、100 ms、120 ms 等 9 种帧长。 Opus 兼具较好的音质和较高的压缩率，计算复杂度也较高。音频处理库裁剪了 Opus 编码器，使其能运行于嵌入式系统。

音频处理库附带了一个 Windows 测试程序 `opus_demo`，这个程序包含了完整版的解码器和裁剪过的编码器。

## 6.1 使用方法 {#使用方法-3}

1. 初始化

   使用 `opus_encoder_init` 初始化编码器对象：

   ```c
   int opus_encoder_init(
       OpusEncoder *st,  // 编码器对象
       opus_int32 Fs,    // 采样率
       int channels,     // 声道数
       int application   // 应用类型
   );
   ```

   通过 `opus_encoder_get_size()` 获得编码器对象的大小。采样率只能是 8000， 12000，16000，24000 或者 48000。声道数只能是 1 或者 2。应用类型及适用场景如下。

   - `OPUS_APPLICATION_VOIP`：适用于大多数 VoIP、视频会议等注重声音质量和可懂性的场景；
   - `OPUS_APPLICATION_AUDIO`：适用于广播或 Hi-Fi 等要求解码输出尽量贴近原始输入的场景；
   - `OPUS_APPLICATION_RESTRICTED_LOWDELAY`：仅用于需要最低延迟的场景。

   下面的代码演示了如何从堆上分配用来存放编码器对象内存，并初始化编码器对象：

   ```c
   int size = opus_encoder_get_size(1);
   OpusEncoder *enc = malloc(size);
   if (NULL == enc)
   {
       ... // error handling
   }

   int error = opus_encoder_init(enc, Fs,
       channels, application);
   if (error)
   {
       ... // error handling
   }
   ```
2. 设置参数

   使用 `opus_encoder_ctl()` 设置编码参数。 `opus_defines.h` 里列出了所有可设置的参数。 例如，将比特率设为 80 kbps：

   ```c
   opus_encoder_ctl(enc, OPUS_SET_BITRATE(80000));
   ```
3. 设置临时内存

   ```c
   void opus_set_scratch_mem(
       const void *buf, // 起始位置
       int size);       // 临时内存的大小（单位：字节）
   ```

   在程序运行过程中，如果发现临时内存空间不足，会调用 `opus_on_run_of_out_scratch_mem`。 音频库里包含了该函数的弱定义，开发者可以重新定义这个函数以自定义处理方法。这个函数的弱定义大致为：

   ```c
   void __attribute((weak)) opus_on_run_of_out_scratch_mem(
       const char *fn, int line_no)
   {
       platform_raise_assertion(fn, line_no);
   }
   ```

   请参考“[参数选择与评估](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-opus.html#参数选择与评估)”了解如何确定临时内存的大小。
4. 编码

   调用 `opus_encode` 编码一个音频帧。

   ```c
   opus_int32 opus_encode(
       OpusEncoder *st,           // 编码器对象
       const opus_int16 *pcm,     // PCM 输入
       int frame_size,            // 这一帧的每个声道所包含的采样数
       unsigned char *data,       // 编码输出（载荷）
       opus_int32 max_data_bytes  // 编码输出的最大长度
   );
   ```

   当编码两个声道时，左右声道在 `pcm` 里交织排列。 `frame_size` 参数结合采样率可推算出音频帧的时长，这个音频帧的时长必须是合法，否则函数将返回一个错误码。 各种采样率所允许的 `frame_size` 如表 [6.1](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-opus.html#tab:ch4-opus-frame-size) 所示。

   *表 6.1: Opus 采样率与帧长*
   | 采样率 (Hz) | 2.5 ms | 5 ms | 10 ms | 20 ms | 40 ms | 60 ms | 80 ms | 100 ms | 120 ms |
   | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
   | 8 k | 20 | 40 | 80 | 160 | 320 | 480 | 640 | 800 | 960 |
   | 12 k | 30 | 60 | 120 | 240 | 480 | 720 | 960 | 1200 | 1440 |
   | 16 k | 40 | 80 | 160 | 320 | 640 | 960 | 1280 | 1600 | 1920 |
   | 24 k | 60 | 120 | 240 | 480 | 960 | 1440 | 1920 | 2400 | 2880 |
   | 48 k | 120 | 240 | 480 | 960 | 1920 | 2880 | 3840 | 4800 | 5760 |

   `max_data_bytes` 是这一帧所允许的最大编码长度，建议预留足够大的空间，不建议用此参数进行比特率调整或控制。

   如果编码成功，这个函数将返回编码输出（载荷）的实际长度，否则返回错误码（负值）。
5. 音频帧打包

   `opus_encode` 所输出的 `data` 仅为载荷部分，还需要附加帧长信息才能组成可解码的音频流。`opus_demo` 所使用的帧头结构为：

   - 帧长：4 字节，大端模式
   - FINAL_RANGE：4 字节，大端模式

   `test_opus_data` 函数演示了如何将编码结果保存为 `opus_demo` 所支持的帧格式。将 `save_bytes()` 收到的字节流保存到文件，就可以用 `opus_demo` 解码，回听效果。

   ```c
   void test_opus_data(OpusEncoder *enc,
       const int16_t *in, const int total_samples,
       const int sample_rate, const int samples_per_frame,
       uint8_t *output, const int max_output_bytes)
   {
       unsigned char int_field[4];
       uint32_t enc_final_range;
       int i;
       for (i = 0; i < total_samples - samples_per_frame;
            i += samples_per_frame)
       {
           int r = opus_encode(enc, in + i, samples_per_frame,
               output, max_output_bytes);
           if (r < 0) platform_raise_assertion("opus_encode", r);

           big_endian_store_32(int_field, 0, (uint32_t)r);
           save_bytes(int_field, sizeof(int_field));

           opus_encoder_ctl(enc, OPUS_GET_FINAL_RANGE(&enc_final_range));
           big_endian_store_32(int_field, 0, enc_final_range);
           save_bytes(int_field, sizeof(int_field));

           save_bytes(output, r);
       }
   }
   ```

## 6.2 参数选择与评估 {#参数选择与评估}

### 6.2.1 临时内存评估 {#临时内存评估}

不同的参数将显著影响所需要的临时内存的大小。运行 `opus_demo`，可以得出需要的临时内存的大小。

这里使用 Audacity[7](#fn7) 辅助转换和播放 PCM 数据。

1. 准备测试数据

   准备一个音频文件（比如一首歌曲或一段录音），使用 Audacity 按 Opus 支持的某一采样率（例如 16 kHz）导出[8](#fn8)为单声道无格式的 16-bit PCM 文件（例如保存为 `data_16k.raw`）。
2. 编码测试

   运行 `opus_demo`，编码测试数据。

   ```sh
   opus_demo -e audio 16000 1 100000 data_16k.raw result.enc
   ```

   这里以 100 kpbs 的比特率转换为 `result.enc`。程序会打印出所需要的临时空间的大小（单位：字节）：

   ```
   stack_max_usage = 12345
   ```
3. 解码测试

   如有必要，可再运行 `opus_demo` 解码 `result.enc`：

   ```sh
   opus_demo -d 16000 1 result.enc result.dec
   ```

   在 Audacity 里导入[9](#fn9)无格式的 PCM 文件 `result.dec`，采样率 16 kHz，回听编解码效果。

重复上述步骤，确定应用中所要使用的采样率、比特率等关键参数，根据工具报告的 `stack_max_usage` 确定临时空间大小。

### 6.2.2 性能评估 {#性能评估}

`test_opus_performance` 函数演示了如何评估编码所消耗的时间。

```c
void test_opus_performance(OpusEncoder *enc,
    const int16_t *in, const int total_samples,
    const int sample_rate, const int samples_per_frame,
    uint8_t *output, const int max_output_bytes)
{
    int i = 0;
    int frame_cnt = 0;
    uint32_t total_time = 0;

    for (i = 0; i < total_samples - samples_per_frame;
         i += samples_per_frame, frame_cnt++)
    {
        int64_t t = platform_get_us_time();
        int r = opus_encode(enc, in + i, samples_per_frame,
            output, max_output_bytes);
        uint32_t tt = (uint32_t)(platform_get_us_time() - t);
        platform_printf("%d: len = %d, %u\n", frame_cnt, r, tt);
        total_time += tt;
    }

    platform_printf("average time per frame = %d us\n",
        total_time / frame_cnt);
    platform_printf("scratch max used       = %d bytes\n",
        opus_scratch_get_max_used_size());
}
```

## 6.3 资源消耗 {#资源消耗-3}

以下数据仅供参考。实际表现受编译器、Cache、RTOS、中断、音频数据等因素影响。

使用如下参数：

- 采样率：16 kHz
- 单声道
- 使用 OPUS_APPLICATION_AUDIO
- 比特率：80 kpbs
- 帧长：10 ms

### 6.3.1 ING916XX {#ing916xx-3}

当 CPU 主频为 112 MHz 时，`sbc_encode2` 编码一帧平均约需要 5 ms，或者说消耗的 CPU 频率约为 56 MHz。

需要的临时内存为 8944 字节。`opus_encoder_get_size(1)` `= 7196`，所以总计需要约 16 kB 内存。

## 6.4 线程安全性 {#线程安全性}

编译时定义了 `NONTHREADSAFE_PSEUDOSTACK`，所以只允许单线程使用。

---

1. <a id="fn7"></a>[https://www.audacityteam.org/](https://www.audacityteam.org/)[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-opus.html#fnref7)
2. <a id="fn8"></a>[https://manual.audacityteam.org/man/other_uncompressed_files_export_options.html](https://manual.audacityteam.org/man/other_uncompressed_files_export_options.html)[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-opus.html#fnref8)
3. <a id="fn9"></a>[https://manual.audacityteam.org/man/file_menu_import.html#raw_data](https://manual.audacityteam.org/man/file_menu_import.html#raw_data)[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-opus.html#fnref9)