<!-- an_libaudio_cn: 7 AMR-WB 编解码 -->

# 7 AMR-WB 编解码 {#ch-amr-wb}

AMR-WB 由 3GPP（第三代合作伙伴计划）制定[10](#fn10)，是一种用于语音编码的音频压缩标准，广泛应用于移动通信领域，特别是在 3G 和 4G 网络中。 AMR-WB 支持的音频带宽范围为 50-7000 Hz，比 AMR-NB 更宽，语音更清晰、自然。 具备从 6.6 kbps 到 23.85 kbps 等多种码率，支持动态调整、优化语音质量和带宽占用。

AMR-WB 音频采样率为 16kHz，以 20ms 为一帧，即 320 个采样（`AMR_WB_PCM_FRAME_16k`）。

## 7.1 使用方法 {#使用方法-4}

### 7.1.1 编码 {#编码-2}

1. 初始化

   使用 `amr_wb_encoder_init` 初始化编码器对象：

   ```c
   struct amr_wb_encoder *amr_wb_encoder_init(
       int bit_stream_format,  // 比特流格式
       int allow_dtx,          // 是否启用 DTX (1 或 0)
       int mode,               // 默认模式（即码率）
       void *buf);             // 用于存放上下文的内存
   ```

   支持三种比特流格式，如表 [7.1](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-amr-wb.html#tab:ch5-amr-bit-stream-format) 所示。当用于语音数据压缩时， 应该使用 MIME 格式（`AMR_WB_BIT_STREAM_FORMAT_MIME_IETF`）。

   *表 7.1: AMR-WB 比特流格式*
   | 格式 | 帧头长度（字节） | 载荷格式 |
   | --- | --- | --- |
   | ETS | 6 | 每 2 个字节表示一个比特 |
   | ITU | 4 | 每 2 个字节表示一个比特 |
   | MIME | 1 | 详见 RFC 3267 (5.1，5.3) |

   帧头长度也可以通过 `amr_wb_get_frame_header_size(mode)` 获得。

   `allow_dtx` 参数详见 AMR-WB 规范，可以填 `0`。

   模式参数 `mode` 与实际码率对应关系见表 [7.2](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-amr-wb.html#tab:ch5-amr-modes)。

   *表 7.2: AMR-WB 码率模式与帧长（MIME 格式）*
   | 模式 | 码率（kb/s） | 每帧比特数 | 每帧载荷长度（字节） |
   | --- | --- | --- | --- |
   | 0 | 6.6 | 132 | 17 |
   | 1 | 8.85 | 177 | 23 |
   | 2 | 12.65 | 253 | 32 |
   | 3 | 14.25 | 285 | 36 |
   | 4 | 15.85 | 317 | 40 |
   | 5 | 18.25 | 365 | 40 |
   | 6 | 19.85 | 397 | 50 |
   | 7 | 23.05 | 461 | 58 |
   | 8 | 23.85 | 477 | 60 |

   调用 `amr_wb_encoder_get_context_size()` 可获取 `buf` 所需大小。
2. 编码

   调用 `amr_wb_encoder_encode_frame` 编码一个音频帧，其返回值为音频帧的帧头和载荷的总长度。

   ```c
   int amr_wb_encoder_encode_frame(
       struct amr_wb_encoder *ctx, // 编码器对象
       const int16_t *pcm_samples, // PCM 输入
       uint8_t *output,            // 编码输出
       void *scratch);             // 临时内存
   ```

   编码输出 `output` 的大小根据选择的码率确定（见表 [7.2](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-amr-wb.html#tab:ch5-amr-modes)）， 例如，若码率为 6.6 kb/s，则 `output` 的长度应该至少是 1 + 17 = 18 字节。

   调用 `amr_wb_encoder_get_context_size()` 可获取临时内存 `scratch` 所需大小。

   需要切换模式时，调用 `amr_wb_encoder_encode_frame2`，先切换模式，再编码。

下面的代码演示了如何编码一整段数据。

```c
void *context = malloc(amr_wb_encoder_get_context_size());
void *scratch = malloc(amr_wb_encoder_get_scratch_mem_size());

static uint8_t output[模式所对应的载荷长度 + 1];
const uint16_t *in = ...        // 音频采样
const int NUM_OF_SAMPLES = .... // 总采样数

struct amr_wb_encoder *enc =
    amr_wb_encoder_init(AMR_WB_BIT_STREAM_FORMAT_MIME_IETF,
        0, 模式, context);

for (i = 0;
     i < NUM_OF_SAMPLES - AMR_WB_PCM_FRAME_16k;
     i += AMR_WB_PCM_FRAME_16k)
{
    int r = amr_wb_encoder_encode_frame(
        enc, in + i, output, scratch);

    // 处理 pcm_output
    ....
}
```

### 7.1.2 解码 {#解码-2}

1. 初始化

   使用 `amr_wb_decoder_init` 初始化解码器对象：

   ```c
   struct amr_wb_decoder *amr_wb_decoder_init(
       int bit_stream_format,      // 比特流格式
       void *buf);                 // 用于存放上下文的内存
   ```

   调用 `amr_wb_decoder_get_context_size()` 可获取 `buf` 所需大小。

   比特流格式仅支持 `AMR_WB_BIT_STREAM_FORMAT_MIME_IETF`。
2. 解码帧头

   使用 `amr_wb_decoder_probe` 解码帧头，获得音频帧基本参数：

   ```c
   int amr_wb_decoder_probe(
       struct amr_wb_decoder *ctx, // 解码器对象
       const uint8_t *stream);     // 音频流
   ```

   音频流 `stream` 应该指向一个音频帧的帧头。这个函数将返回这个音频帧的载荷的长度。 如果出现错误，将返回负值错误码。
3. 解码载荷

   使用 `amr_wb_decoder_decode_frame` 解码载荷：

   ```c
   int amr_wb_decoder_decode_frame(
       struct amr_wb_decoder *ctx, // 解码器对象
       const uint8_t *payload,     // 音频帧载荷
       int16_t *synth_pcm,         // PCM 输出
       void *scratch);             // 临时内存
   ```

   这个函数返回输出的 PCM 采样的个数，即 `AMR_WB_PCM_FRAME_16k`， `synth_pcm` 的长度也应为 `AMR_WB_PCM_FRAME_16k`。

   调用 `amr_wb_decoder_get_scratch_mem_size()` 可获取临时内存 `scratch` 所需大小。

下面的代码演示了如何解码一段数据。

```c
static uint8_t pcm_output[AMR_WB_PCM_FRAME_16k];

const uint8_t *in = ...; // 音频数据
int data_size = ...;     // 音频数据总长度
void *context = malloc(amr_wb_decoder_get_context_size());
void *scratch = malloc(amr_wb_decoder_get_scratch_mem_size());

struct amr_wb_decoder *dec = amr_wb_decoder_init(
    AMR_WB_BIT_STREAM_FORMAT_MIME_IETF, context);
const int header_size = amr_wb_get_frame_header_size(
    AMR_WB_BIT_STREAM_FORMAT_MIME_IETF);

while (data_size > header_size)
{
    int payload_len = amr_wb_decoder_probe(dec, in);
    in += header_size;
    data_size -= header_size;

    if (payload_len > data_size) break;
    if (payload_len < 0) break;

    int r = amr_wb_decoder_decode_frame(
        dec, in, pcm_output, scratch);

    in        += payload_len;
    data_size -= payload_len;

    // 处理 pcm_output
    ....
}
```

## 7.2 资源消耗 {#ch-amr-wb-resources}

以下数据仅供参考。实际表现受编译器、Cache、RTOS、中断、音频数据等因素影响。

### 7.2.1 ING916XX {#ing916xx-4}

*表 7.3: AMR-WB 编解码器的内存需求*
| 功能 | `context`（字节） | `scratch`（字节） |
| --- | --- | --- |
| 编码 | 2788 | 11898 |
| 解码 | 1552 | 3826 |

当 CPU 主频为 112 MHz 时，AMR-WB 编解码器的处理一个音频帧所消耗的时间见表 [7.4](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-amr-wb.html#tab:ch5-amr-time-usage)。 从表中可以看出，需要进行实时编码时，只能使用 6.6 kbps，不可使用更高速率。

*表 7.4: AMR-WB 编解码器处理一个音频帧所消耗的平均时间*
| 模式 | 编码 （ms） | 解码 （ms） |
| --- | --- | --- |
| 0 | 16.7 | 7.9 |
| 1 | 20.0 | 6.6 |
| 2 | 22.2 | 5.9 |
| 3 | 23.9 | 5.9 |
| 4 | 23.9 | 6.0 |
| 5 | 24.6 | 6.1 |
| 6 | 25.6 | 6.2 |
| 7 | 25.3 | 6.2 |
| 8 | 24.8 | 6.6 |

---

1. <a id="fn10"></a>参见 TS 26.171 等[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-amr-wb.html#fnref10)