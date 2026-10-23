<!-- an_libaudio_cn: 5 SBC/mSBC 编解码 -->

# 5 SBC/mSBC 编解码 {#ch-sbc}

SBC 支持多种采样率、多种帧长。一个 SBC/mSBC 音频帧由 4 部分组成：

```c
struct
{
    frame_header;
    scale_factors;
    audio_samples;
    padding;
};
```

其中 `frame_header` 里的第一字节为 `sync_word`。对于 SBC，`sync_word` 固定为 `0x9C`, 而 mSBC 则为 `0xAD`。

```c
struct frame_header
{
    uint8_t sync_word;
    ....
};
```

## 5.1 帧描述参数 {#帧描述参数}

帧描述参数见 `sbc_frame` 结构体：

```c
struct sbc_frame
{
    bool msbc;              // 是否为 mSBC
    enum sbc_freq freq;     // 采样频率
    enum sbc_mode mode;     // 声道模式
    enum sbc_bam bam;       // 比特分配方式
    int nblocks, nsubbands; // 分块数，子带数
    int bitpool;            // bit 池大小
};
```

`nblocks` 应为 4、8、12 或 16，`nsubbands` 可为 4 或 8。 进行编码时，每个声道上的每一帧需要 (`nblocks` \times `nsubbands`) 个采样，该值也可通过 `sbc_get_frame_samples()` 获取。

`bitpool` 是一个块（`nsubbands` 个子带）所能占据的最多比特数。

mSBC 使用一组固定的参数：

```c
const struct sbc_frame msbc_frame = {
    .msbc = true,
    .mode = SBC_MODE_MONO,
    .freq = SBC_FREQ_16K,
    .bam = SBC_BAM_LOUDNESS,
    .nsubbands = 8, .nblocks = 15,
    .bitpool = 26
};
```

## 5.2 使用方法 {#使用方法-2}

### 5.2.1 编码 {#编码-1}

1. 确定帧描述参数

   确定了帧描述参数后，务必使用 `sbc_get_frame_size()` 等函数检查参数是否合法。
2. 检查关键参数

   - `sbc_get_frame_size()` 获得编码后每个帧的字节长度；
   - `sbc_get_frame_bitrate()` 获得编码后的比特率；
   - `sbc_get_frame_samples()` 为一个声道编码一个帧所需要的采样数

   如果帧描述参数不合法，这些函数都将返回 0。
3. 初始化对象

   ```c
   void sbc_reset(
       sbc_t *sbc);  // SBC 对象
   ```
4. 进行编码

   音频处理库里包含两个编码函数，其区别在于 `sbc_encode2` 的临时内存由外部分配， 而 `sbc_encode` 的临时内存则在栈上分配。对于栈空间紧张的应用，应该使用 `sbc_encode2`。 调用一次 `sbc_encode2` 或者 `sbc_encode` 完成一帧编码，编码成功返回 0 否则返回错误码。

   `sbc_encode2` 的函数签名如下：

   ```c
   int sbc_encode2(
       sbc_t *sbc,          // SBC 对象
       const int16_t *pcml, // 左声道 PCM 数据
       int pitchl,          // 左声道 PCM 相邻数据在 pcml 里的间隔
       const int16_t *pcmr, // 右声道 PCM 数据
       int pitchr,          // 右声道 PCM 相邻数据在 pcmr 里的间隔
       const struct sbc_frame *frame, // 帧描述参数
       void *data,          // 编码输出
       unsigned size,       // 编码输出的内存长度
       void *scratch);      // 临时内存
   ```

   当只编码一个声道时，忽略 `pcmr` 和 `pitchr` 参数。`pitchl` 和 `pitchr` 分别控制如何从 `pcml` 和 `pcmr` 读取采样：`sample[n] = pcm[n * pitch]`。举例说明如下：

   - 只有一个声道的数据：

     ```c
     scb_encode2(sbc, pcm, 1, ...);
     ```
   - 要编码两个声道，且两个声道的数据独立存放：

     ```c
     scb_encode2(sbc, pcml, 1, pcmr, 1, ...);
     ```
   - 要编码两个声道，且两个声道的数据交织存放，即 `pcm[] = {左, 右, 左, 右, ...}`:

     ```c
     scb_encode2(sbc, pcm, 2, pcm + 1, 2, ...);
     ```

   `size` 参数至少为 `sbc_get_frame_size(frame)`。

   临时内存 `scrach` 应给按 `int` 型对齐，大小至少为 `SBC_ENCODE_SCRATCH_MEM_SIZE`。

   `sbc_encode` 比 `sbc_encode2` 缺少 `scratch` 参数，其它参数完全一致，不再赘述。

   当使用 mSBC 编码时，`frame` 只需要设置 `msbc = true`，不需要完整填写 mSBC 帧参数：

   ```c
   const struct sbc_frame msbc_frame = {
       .msbc = true,
   };
   sbc_encode2(...,
       &msbc_frame,
       ...);
   ```

### 5.2.2 解码 {#解码-1}

1. 初始化

   ```c
   void sbc_reset(
       sbc_t *sbc);  // SBC 对象
   ```
2. 进行解码

   同编码类似，音频处理库里包含两个解码函数，其区别在于 `sbc_decode2` 的临时内存由外部分配， 而 `sbc_decode` 的临时内存则在栈上分配。对于栈空间紧张的应用，应该使用 `sbc_decode2`。 调用一次 `sbc_decode2` 或者 `sbc_decode` 完成一帧解码，解码成功返回 0 否则返回错误码。

   `sbc_decode2` 的函数签名如下：

   ```c
   int sbc_decode2(
       sbc_t *sbc,        // SBC 对象
       const void *data,  // 输入数据（即编码后的一帧）
       unsigned size,     // 输入数据的长度，应不小于该帧的长度
       struct sbc_frame *frame, // 解出的帧描述参数
       int16_t *pcml,     // 左声道 PCM 解码输出
       int pitchl,        // 左声道 PCM 相邻数据在 pcml 里的间隔
       int16_t *pcmr,     // 右声道 PCM 解码输出
       int pitchr,        // 右声道 PCM 相邻数据在 pcmr 里的间隔
       void *scratch);    // 临时内存
   ```

   `pitchl` 和 `pitchr` 的含义与 `sbc_encode2` 里相同，区别在于后者用于读取 PCM 数据， 而在这里用于写入 PCM 数据。

   临时内存 `scrach` 应给按 `int` 型对齐，大小至少为 `SBC_DECODE_SCRATCH_MEM_SIZE`。

   调用解码函数时，必须保证 `pcml` 和 `pcmr` 空间足够，即每个声道都足够容纳 `SBC_MAX_SAMPLES` 个采样。`sbc_decode` 比 `sbc_decode2` 缺少 `scratch` 参数，其它参数完全一致，不再赘述。

## 5.3 资源消耗 {#资源消耗-2}

以下数据仅供参考。实际表现受编译器、Cache、RTOS、中断等因素影响。

使用如下帧描述参数：

```c
const struct sbc_frame frame_param =
{
    .freq = SBC_FREQ_16K,
    .mode = SBC_MODE_MONO,
    .nsubbands = 4,
    .nblocks = 8,
    .bam = SBC_BAM_LOUDNESS,
    .bitpool = 16
};
```

### 5.3.1 ING916XX {#ing916xx-2}

当 CPU 主频为 112 MHz 时，`sbc_encode2` 编码一帧需要约 0.1 ms， 或者说消耗的 CPU 频率约为 5.6 MHz。

当 CPU 主频为 112 MHz 时，`sbc_decode2` 编码一帧需要约 0.09 ms， 或者说消耗的 CPU 频率约为 5 MHz。