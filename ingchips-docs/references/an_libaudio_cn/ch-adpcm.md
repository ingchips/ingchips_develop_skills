<!-- an_libaudio_cn: 4 ADPCM 编解码 -->

# 4 ADPCM 编解码 {#ch-adpcm}

ADPCM 编码将 PCM 转换为每采样占用 4-bit 的压缩格式；ADPCM 解码把这种压缩格式转换为 16-bit PCM。

## 4.1 使用方法 {#使用方法-1}

### 4.1.1 编码 {#编码}

1. 定义回调函数

   这个回调函数用来接收编码结果，其签名为：

   ```c
   typedef void (*adpcm_encode_output_cb_f)(
       uint8_t output, // 编码输出，包含两个 4-bit 数据
       void *param);   // 用户数据
   ```
2. 初始化编码器对象

   ```c
   void adpcm_enc_init(
       adpcm_enc_t *adpcm,                // 编码器对象
       adpcm_encode_output_cb_f callback, // 回调函数
       void *param);                      // 传给回调函数的用户数据
   ```
3. 编码

   ```c
   void adpcm_encode(
       adpcm_enc_t *adpcm,         // 编码器对象
       const pcm_sample_t *input,  // 音频数据
       int input_size);            // 音频采样数
   ```

   采样数 `input_size` 可以是奇数。每产生两个 4-bit 编码输出（拼接为 1 个字节[6](#fn6)）， 就会调用一次 `callback`。

### 4.1.2 解码 {#解码}

1. 定义回调函数

   这个回调函数用来接收解码结果，其签名为：

   ```c
   typedef void (*adpcm_decode_output_cb_f)(
       pcm_sample_t output, // 解码输出
       void* param);        // 用户数据
   ```
2. 初始化解码器

   ```c
   void adpcm_dec_init(
       adpcm_dec_t* adpcm,                // 解码器对象
       adpcm_decode_output_cb_f callback, // 回调函数
       void* param);                      // 传给回调函数的用户数据
   ```
3. 解码

   ```c
   void adpcm_decode(
       adpcm_dec_t *adpcm, // 解码器对象
       uint8_t data);      // ADPCM 编码
   ```

## 4.2 资源消耗 {#资源消耗-1}

以下数据仅供参考。实际表现受编译器、Cache、RTOS、中断等因素影响。

### 4.2.1 ING916XX {#ing916xx-1}

当 CPU 主频为 112 MHz 时，`adpcm_encode` 处理 1 个采样仅需 0.7 \mu s ，或者说 处理 1 个采样消耗的 CPU 频率约为 80 Hz，处理 16 kHz 采样消耗的 CPU 频率约为 1.25 MHz。

当 CPU 主频为 112 MHz 时，`adpcm_decode` 解码 1 个字节输出 2 个采样约需 1.9 \mu s ，或者说 解码 1 个字节消耗的 CPU 频率约为 213 Hz，解码 16 kHz ADPCM 消耗的 CPU 频率约为 3.4 MHz。

---

1. <a id="fn6"></a>设高 4-bit 对应第 n 个采样，则低 4-bit 对应第 n + 1 个采样。[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-adpcm.html#fnref6)