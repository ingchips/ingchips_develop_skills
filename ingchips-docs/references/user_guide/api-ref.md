<!-- user_guide: 6 Platform API Reference -->

# Chapter 6 Platform API Reference {#api-ref}

This chapter describes the platform API.

## 6.1 Configuration & Information {#configuration-information}

### 6.1.1 platform_config {#platform_config}

Configure some platform functionalities.

#### 6.1.1.1 Prototype {#prototype}

```c
void platform_config(const platform_cfg_item_t item,
                     const uint32_t flag);
```

#### 6.1.1.2 Parameters {#parameters}

- `const platform_cfg_item_t item`

  Specify the item to be configured. It can be one of following values:

  - `PLATFORM_CFG_LOG_HCI`: Print host controller interface messages. Default: Disabled.

    Only available on ING918. HCI logging is only intended for a quick check on BLE behavior. Please consider using tracing (see [Debugging & Tracing](https://ingchips.github.io/user_guide/dive-into-sdk.html#debugging-tracing)).
  - `PLATFORM_CFG_POWER_SAVING`: Power saving. Default: Disabled.
  - `PLATFORM_CFG_TRACE_MASK`: Bit map of selected trace items. Default: `0`.

    ```c
    typedef enum
    {
        PLATFORM_TRACE_ID_EVENT                 = 0,
        PLATFORM_TRACE_ID_HCI_CMD               = 1,
        PLATFORM_TRACE_ID_HCI_EVENT             = 2,
        PLATFORM_TRACE_ID_HCI_ACL               = 3,
        PLATFORM_TRACE_ID_LLCP                  = 4,
        //..
    } platform_trace_item_t;
    ```
  - `PLATFORM_CFG_RT_RC_EN`: Enable/Disable real-time RC clock. Default: Enabled.
  - `PLATFORM_CFG_RT_OSC_EN`: Enable/Disable real-time crystal oscillator. Default: Enabled.
  - `PLATFORM_CFG_RT_CLK`: Real-time clock selection. Flag is `platform_rt_clk_src_t`. Default: `PLATFORM_RT_RC`

    ```c
    typedef enum
    {
        PLATFORM_RT_OSC,           // External real-time crystal oscillator
        PLATFORM_RT_RC             // Internal real-time RC clock
    } platform_rt_clk_src_t;
    ```

    For ING918, When modifying this configuration, both RT_RC and RT_OSC should be **enabled** and **run**:

    ```
      * For RT_OSC, wait until status of RT_OSC is OK;
      * For RT_RC, wait 100μs after enabled.
    ```

    And wait another 100μs before disabling the unused clock.
  - `PLATFORM_CFG_RT_CLK_ACC`: Configure real-time clock accuracy in ppm.
  - `PLATFORM_CFG_RT_CALI_PERIOD`: Real-time clock auto-calibration period in seconds. Default: 3600 * 2 (2 hours).
  - `PLATFORM_CFG_DEEP_SLEEP_TIME_REDUCTION`: Sleep time reduction (deep sleep mode) in micro seconds. ING918 Default: ~550μs.
  - `PLATFORM_CFG_SLEEP_TIME_REDUCTION`: Sleep time reduction (other sleep mode) in micro seconds. ING918 Default: ~450μs.
  - `PLATFORM_CFG_LL_DBG_FLAGS`: Link layer flags. Combination of bits in `ll_cfg_flag_t`. Check out *Programmers’ Guide on Bluetooth Low Energy*[24](#fn24) for details.
  - `PLATFORM_CFG_LL_LEGACY_ADV_INTERVAL`: Link layer legacy advertising intervals for high duty cycle (higher 16bits) and normal duty cycle (lower 16bits) in micro seconds. Default for high duty cycle: 1250; default for normal duty cycle: 1500.
  - `PLATFORM_CFG_RTOS_ENH_TICK`: Enable enhanced ticks for RTOS. Default: Disabled. When enabled, ticks becomes more accurate when peripherals are generating interrupt requests frequently.
  - `PLATFORM_CFG_LL_DELAY_COMPENSATION`: Delay compensation for Link Layer.

    When system runs at a lower frequency, more time (in μs) is needed by Link Layer to schedule RF tasks. For example, if ING916 runs at 24MHz, a compensation of ~2500 μs is needed.
  - `PLATFORM_CFG_24M_OSC_TUNE`: 24M OSC tunning. Not available for ING918.

    For ING916, tunning value may vary in 0x16~0x2d.
  - `PLATFORM_CFG_ALWAYS_CALL_WAKEUP`: Always trigger `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP` event no matter if deep sleep procedure is completed or aborted (failed). Default for ING918: Disabled for backward compatibility. Default for ING916: Enabled.
  - `PLATFORM_CFG_FAST_DEEP_SLEEP_TIME_REDUCTION`: Sleep time reduction for fast deep sleep mode in micro seconds. Not available for ING918.

    This configuration must be less or equal to `PLATFORM_CFG_DEEP_SLEEP_TIME_REDUCTION`. When equal to `PLATFORM_CFG_DEEP_SLEEP_TIME_REDUCTION`, fast deep sleep mode is not used.

    Default for ING916: ~2000μs.
  - `PLATFORM_CFG_AUTO_REDUCE_CLOCK_FREQ`: Automatically reduce CPU clock frequency in these circumstances:

    - The default IDLE procedure,
    - When entering sleep modes.

    Not available for ING918. Default for ING916: Enabled.
- `const uint32_t flag`

  To disable or enable an item. It can be one of following values:

  - `PLATFORM_CFG_ENABLE`
  - `PLATFORM_CFG_DISABLE`

#### 6.1.1.3 Return Value {#return-value}

Void.

#### 6.1.1.4 Remarks {#remarks}

Void.

#### 6.1.1.5 Example {#example}

```c
// On ING918, Enable HCI logging
platform_config(PLATFORM_CFG_LOG_HCI, PLATFORM_CFG_ENABLE);
```

### 6.1.2 platform_get_version {#platform_get_version}

Get version number of platform.

#### 6.1.2.1 Prototype {#prototype-1}

```c
const platform_ver_t *platform_get_version(void);
```

#### 6.1.2.2 Parameters {#parameters-1}

Void.

#### 6.1.2.3 Return Value {#return-value-1}

Pointer to `platform_ver_t`.

#### 6.1.2.4 Remarks {#remarks-1}

Platform version number has three parts, major, minor and patch:

```c
typedef struct platform_ver
{
    unsigned short major;
    char  minor;
    char  patch;
} platform_ver_t;
```

#### 6.1.2.5 Example {#example-1}

```c
const platform_ver_t *ver = platform_get_version();
printf("Platform version: %d.%d.%d\n", ver->major, ver->minor, ver->patch);
```

### 6.1.3 platform_read_info {#platform_read_info}

Read platform information.

#### 6.1.3.1 Prototype {#prototype-2}

```c
uint32_t platform_read_info(const platform_info_item_t item);
```

#### 6.1.3.2 Parameters {#parameters-2}

- `const platform_info_item_t item`

  Information item.

  - `PLATFORM_INFO_RT_OSC_STATUS`: Read status of real-time crystal oscillator. Value 0: not OK; Non-0: OK.

  For ING916: this clock become running **after** selected as real time clock source.

  - `PLATFORM_INFO_RT_CLK_CALI_VALUE`: Read current real time clock calibration result.
  - `PLATFOFM_INFO_IRQ_NUMBER`: Get the underline IRQ number of a platform IRQ.

    For example, get the underline IRQ number of UART0:

    ```c
    platform_read_info(
        PLATFOFM_INFO_IRQ_NUMBER + PLATFORM_CB_IRQ_UART0)
    ```

#### 6.1.3.3 Return Value {#return-value-2}

Value of the information item.

#### 6.1.3.4 Remarks {#remarks-2}

Void.

#### 6.1.3.5 Example {#example-2}

```c
platform_read_info(PLATFORM_INFO_RT_OSC_STATUS);
```

### 6.1.4 platform_switch_app {#api-switch-app}

Switch to a secondary app.

#### 6.1.4.1 Prototype {#prototype-3}

```c
void platform_switch_app(const uint32_t app_addr);
```

#### 6.1.4.2 Parameters {#parameters-3}

- `const uint32_t app_addr`

  Entry address of the secondary app.

#### 6.1.4.3 Return Value {#return-value-3}

Void.

#### 6.1.4.4 Remarks {#remarks-3}

When calling this function, the code after it will not be executed.

#### 6.1.4.5 Example {#example-3}

```c
platform_switch_app(0x80000);
```

## 6.2 Events & Interrupts {#events-interrupts}

### 6.2.1 platform_set_evt_callback_table {#platform_set_evt_callback_table}

Register a callback function table for all platform events.

#### 6.2.1.1 Prototype {#prototype-4}

```c
void platform_set_evt_callback_table(
    const platform_evt_cb_table_t *table);
```

#### 6.2.1.2 Parameters {#parameters-4}

- `const platform_evt_cb_table_t *table`

  Address of the callback function table.

#### 6.2.1.3 Return Value {#return-value-4}

Void.

#### 6.2.1.4 Remarks {#remarks-4}

This function shall only be called in `app_main`. If `platform_set_evt_callback` is used, this function shall not be used.

Comparing to `platform_set_evt_callback`, use this function can save a block of RAM of `sizeof(platform_evt_cb_table_t)` bytes.

#### 6.2.1.5 Example {#example-4}

```c
static const platform_evt_cb_table_t evt_cb_table =
{
    .callbacks = {
        [PLATFORM_CB_EVT_HARD_FAULT] = {
            .f = (f_platform_evt_cb)cb_hard_fault,
        },
        [PLATFORM_CB_EVT_PROFILE_INIT] = {
            .f = setup_profile,
        },
        // ...
    }
};

int app_main()
{
    // ...
    platform_set_evt_callback_table(&evt_cb_table);
    // ...
}
```

### 6.2.2 platform_set_irq_callback_table {#platform_set_irq_callback_table}

Register a callback function table for all platform interrupt requests.

#### 6.2.2.1 Prototype {#prototype-5}

```c
void platform_set_irq_callback_table(
    const platform_irq_cb_table_t *table);
```

#### 6.2.2.2 Parameters {#parameters-5}

- `const platform_irq_cb_table_t *table`

  Address of the callback function table.

#### 6.2.2.3 Return Value {#return-value-5}

Void.

#### 6.2.2.4 Remarks {#remarks-5}

This function shall only be called in `app_main`. If `platform_set_irq_callback` is used, this function shall not be used.

Comparing to `platform_set_irq_callback`, use this function can save a block of RAM of `sizeof(platform_irq_cb_table_t)` bytes.

#### 6.2.2.5 Example {#example-5}

```c
static const platform_irq_cb_table_t irq_cb_table =
{
    .callbacks = {
        [PLATFORM_CB_IRQ_UART0] = {
            .f = (f_platform_irq_cb)cb_irq_uart,
            .user_data = APB_UART0
        },
        // ...
    }
};

int app_main()
{
    // ...
    platform_set_irq_callback_table(&irq_cb_table);
    // ...
}
```

### 6.2.3 platform_set_evt_callback {#platform_set_evt_callback}

Registers callback functions to platform events.

#### 6.2.3.1 Prototype {#prototype-6}

```c
void platform_set_evt_callback(platform_evt_callback_type_t type,
                               f_platform_evt_cb f,
                               void *user_data);
```

#### 6.2.3.2 Parameters {#parameters-6}

- `platform_evt_callback_type_t type`

  Specify the event type to which the callback function is registered. It can be one of following values:

  - `PLATFORM_CB_EVT_PUTC`: Ouput ASCII character event

    When platform want to output ASCII characters for logging, this event is fired. Parameter `void *data` passed into the callback function is casted from `char *`.

    `Wizard` can automatically generate code that redirects platform log to UART if `Print to UART` is checked on `Common Function` when creating a new project.
  - `PLATFORM_CB_EVT_PROFILE_INIT`: Profile initialization event

    When host initializes, this event is fired to request app to initialize GATT profile.

    `Wizard` can automatically generate code for this event when creating a new project.
  - `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP`: Wakeup from deep sleep event

    When waking up from deep sleep, this event is fired. During deep sleep, peripheral interfaces (such as UART, I2C, etc) are all powered off. So, when waking up, these interfaces might need to be re-initialized.

    `Wizard` can automatically generate code for event if `Deep Sleep` is checked on `Common Function` when creating a new project.

    Parameter `void *data` passed into the callback function is casted from `platform_wakeup_call_info_t *`.

    RTOS is not resumed yet, some ROTS APIs are not usable; Some platform APIs (such as `platform_get_us_time`) might be unusable either.
  - `PLATFORM_CB_EVT_ON_IDLE_TASK_RESUMED`: OS is fully resumed from power saving modes.

    The callback is invoked after `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP` if its reason is `PLATFORM_WAKEUP_REASON_NORMAL`. For NoOS variants, the callback is invoked by `platform_os_idle_resumed_hook()`. This event is different with `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP`:

    - all OS functionalities are resumed (For NoOS variants, this depends on the proper use of `platform_os_idle_resumed_hook()`)
    - all platform APIs are functional
    - callback is invoked in the idle task.

    Parameter `void *data` is always `NULL`.
  - `PLATFORM_CB_EVT_QUERY_DEEP_SLEEP_ALLOWED`: Query if deep sleep is allowed event

    When platform prepares to enter deep sleep mode, this event is fired to query app if deep sleep is allow at this moment. Callback function can reject deep sleep by returning `0`, and allow it by returning a non-`0` value.

    `Wizard` can automatically generate code for event if `Deep Sleep` is checked on `Common Function` when creating a new project.
  - `PLATFORM_CB_EVT_HARD_FAULT`: Hard fault occurs

    When hard fault occurs, this event is fired. Parameter `void *data` passed into the callback function is casted from `hard_fault_info_t *`. If this callback is not defined, CPU enters a dead loop when hard fault occurs.
  - `PLATFORM_CB_EVT_ASSERTION`: Software assertion fails

    When software assertion fails, this event is fired. Parameter `void *data` passed into the callback function is casted from `assertion_info_t *`. If this callback is not defined, CPU enters a dead loop when assertion occurs.
  - `PLATFORM_CB_EVT_LLE_INIT`: Link layer engine initialized.

    When link layer engine initialized, this event is fired.
  - `PLATFORM_CB_EVT_HEAP_OOM`: Out of memory.

    When allocation on heap fails (heap out of memory), this event is fired. If this event is fired and no callback is defined, CPU enters a dead loop. Parameter `void *data` is casted from an integer identifying which heap is run out:

    - `0`: FreeRTOS’s heap;
    - `1`: Link Layer’s heap;
    - `2`: Link Layer’s task pool.
  - `PLATFORM_CB_EVT_TRACE`: Trace output.

    When a trace item is emitted, this event is fired. Apps can define a callback function for this event to save or log trace output. `param` to the callback is casted from `platform_trace_evt_t *` (See [Debugging & Tracing](https://ingchips.github.io/user_guide/dive-into-sdk.html#debugging-tracing)).

    ```c
    typedef struct
    {
        const void *data1;
        const void *data2;
        uint16_t len1;
        uint16_t len2;
    } platform_evt_trace_t;
    ```

    A trace item is a combination of `data1` and `data2`. Note:

    1. `len1` or `len2` might be 0, but not both;
    2. If callback function finds that it can’t output data of size `len1` + `len2`, then, both `data1` & `data2` should be discarded to avoid trace item corruption.
  - `PLATFORM_CB_EVT_EXCEPTION`: Hardware exceptions.

    Parameter `void *data` is casted from `platform_exception_id_t *`.
  - `PLATFORM_CB_EVT_IDLE_PROC`: Customized IDLE procedure.

    See “Programmer’s Guide - Power Saving”[25](#fn25).
  - `PLATFORM_CB_EVT_HCI_RECV`: Take over HCI and isolate the built-in Host completely.

    When defined:

    - HCI events and ACL data are passed to this callback;
    - `PLATFORM_CB_EVT_PROFILE_INIT` is ignored.

    Parameter `void *data` is casted from `const platform_hci_recv_t *`. See also [`platform_get_link_layer_interf`](https://ingchips.github.io/user_guide/api-ref.html#platform_get_link_layer_interf).
  - `PLATFORM_CB_EVT_BEFORE_DEEP_SLEEP`: Platform is entering deep sleep mode

    When platform decides to enter deep sleep mode, this event is emitted. Apps can take this opportunity to configure peripherals. The callback function shall be simple and return as soon as possible.

    Parameter `void *data` is casted from `platform_sleep_category_b_t`, representing the selected sleep mode.
- `f_platform_evt_cb f`

  The callback function registered to event `type`. `f_platform_evt_cb` is:

  ```c
  typedef uint32_t (*f_platform_evt_cb)(void *data, void *user_data);
  ```

  Returned value is ignored except explicitly stated.
- `void *user_data`

  This is passed to callback function’s `user_data` unchanged.

#### 6.2.3.3 Return Value {#return-value-6}

Void.

#### 6.2.3.4 Remarks {#remarks-6}

It is not required to register callback functions to each event.

If no callback function is registered to `PLATFORM_CB_EVT_PUTC` event, all platform log including `platform_printf` is discarded.

If no callback function is registered to `PLATFORM_CB_EVT_PROFILE_INIT` event, BLE device’s profile is empty.

If no callback function is registered to `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP` event, app will not be notified when waking up from deep sleep.

If no callback function is registered to `PLATFORM_CB_EVT_QUERY_DEEP_SLEEP_ALLOWED` event, deep sleep is *disabled*.

#### 6.2.3.5 Example {#example-6}

```c
uint32_t cb_putc(char *c, void *dummy)
{
    // TODO: output char c to UART
    return 0;
}

......

platform_set_evt_callback(PLATFORM_CB_EVT_PUTC, (f_platform_evt_cb)cb_putc,
                          NULL);
```

### 6.2.4 platform_set_irq_callback {#platform_set_irq_callback}

Registers callback functions to interrupt requests.

Developers do not need to define IRQ handlers in apps, but use callback functions instead.

#### 6.2.4.1 Prototype {#prototype-7}

```c
void platform_set_irq_callback(platform_irq_callback_type_t type,
                               f_platform_irq_cb f,
                               void *user_data);
```

#### 6.2.4.2 Parameters {#parameters-7}

- `platform_irq_callback_type_t type`

  Specify the IRQ type to which the callback function is registered. Values vary for different chip families. Take ING918 as an example:

  ```c
  PLATFORM_CB_IRQ_RTC,
  PLATFORM_CB_IRQ_TIMER0,
  PLATFORM_CB_IRQ_TIMER1,
  PLATFORM_CB_IRQ_TIMER2,
  PLATFORM_CB_IRQ_GPIO,
  PLATFORM_CB_IRQ_SPI0,
  PLATFORM_CB_IRQ_SPI1,
  PLATFORM_CB_IRQ_UART0,
  PLATFORM_CB_IRQ_UART1,
  PLATFORM_CB_IRQ_I2C0,
  PLATFORM_CB_IRQ_I2C1
  ```
- `f_platform_irq_cb f`

  The callback function registered to IRQ `type`. `f_platform_irq_cb` is:

  ```c
  typedef uint32_t (*f_platform_irq_cb)(void *user_data);
  ```
- `void *user_data`

  This is passed to callback function’s `user_data` unchanged.

#### 6.2.4.3 Return Value {#return-value-7}

Void.

#### 6.2.4.4 Remarks {#remarks-7}

When a callback function is registered to an IRQ, the IRQ is enabled automatically. See also [`platform_enable_irq`](https://ingchips.github.io/user_guide/api-ref.html#platform_enable_irq).

#### 6.2.4.5 Example {#example-7}

```c
uint32_t cb_irq_uart0(void *dummy)
{
    // TODO: add UART0 IRQ handling code
    return 0;
}

......

platform_set_irq_callback(
    PLATFORM_CB_IRQ_UART0,
    cb_irq_uart0,
    NULL);
```

### 6.2.5 platform_enable_irq {#platform_enable_irq}

Enable or disable a specified IRQ.

#### 6.2.5.1 Prototype {#prototype-8}

```c
void platform_enable_irq(
    platform_irq_callback_type_t type,
    uint8_t flag);
```

#### 6.2.5.2 Parameters {#parameters-8}

- `platform_irq_callback_type_t type`:

  The IRQ to be configured.
- `uint8_t flag`:

  Enable (1) or disable (0).

#### 6.2.5.3 Return Value {#return-value-8}

Void.

#### 6.2.5.4 Remarks {#remarks-8}

“Enabling” or “disabling” an interrupt here is from the perspective of CPU. Take UART as an example, UART itself has to be configured to generate interrupts for Rx, Tx, or timeout, which is out of the scope of this function.

#### 6.2.5.5 Example {#example-8}

To enable the interrupt request from UART0:

```c
platform_enable_irq(
    PLATFORM_CB_IRQ_UART0,
    1);
```

## 6.3 Clocks {#clocks}

See also “The Real-time Clock”[26](#fn26) in “Programmer’s Guide - Power Saving”[27](#fn27).

### 6.3.1 platform_calibrate_rt_clk {#platform_calibrate_rt_clk}

Calibrate real-time clock and get the calibration value.

#### 6.3.1.1 Prototype {#prototype-9}

```c
uint32_t platform_calibrate_rt_clk(void);
```

### 6.3.2 platform_rt_rc_auto_tune {#platform_rt_rc_auto_tune}

Automatically tune the internal real-time RC clock, and get the tuning value.

For ING918, this function tunes the internal real-time RC clock to 50kHz[28](#fn28). For others, it tunes the internal real-time RC clock to 32768Hz.

#### 6.3.2.1 Prototype {#prototype-10}

```c
uint16_t platform_rt_rc_auto_tune(void);
```

#### 6.3.2.2 Parameters {#parameters-9}

Void.

#### 6.3.2.3 Return Value {#return-value-9}

The 16-bits tuning value.

#### 6.3.2.4 Remarks {#remarks-9}

This function must be called if the app enables power saving mode, and the real-time RC clock is used as the clock source.

This operation costs ~250ms. It is recommended to call this once and store the returned value for later usage.

#### 6.3.2.5 Example {#example-9}

```c
// the simplest example: call this function in the
// callback function of `PLATFORM_CB_EVT_PROFILE_INIT`
// without saving the returned value.
uint32_t setup_profile(void *user_data)
{
    platform_rt_rc_auto_tune();
    ...
}
```

### 6.3.3 platform_rt_rc_auto_tune2 {#platform_rt_rc_auto_tune2}

Automatically tune the internal real-time RC clock to a specific frequency, and get the tuning value.

#### 6.3.3.1 Prototype {#prototype-11}

```c
uint16_t platform_rt_rc_auto_tune2(
    uint32_t target_frequency);
```

#### 6.3.3.2 Parameters {#parameters-10}

- `uint32_t target_frequency`

  Target frequency in Hertz.

#### 6.3.3.3 Return Value {#return-value-10}

The 16-bits tuning value.

### 6.3.4 platform_rt_rc_tune {#platform_rt_rc_tune}

Tune internal the real-time RC clock with the tune value.

#### 6.3.4.1 Prototype {#prototype-12}

```c
void platform_rt_rc_tune(uint16_t value);
```

#### 6.3.4.2 Parameters {#parameters-11}

- `uint16_t value`

  Value used to tune the clock (returned by [`platform_rt_rc_auto_tune`](https://ingchips.github.io/user_guide/api-ref.html#platform_rt_rc_auto_tune), or [`platform_rt_rc_auto_tune2`](https://ingchips.github.io/user_guide/api-ref.html#platform_rt_rc_auto_tune2))

#### 6.3.4.3 Return Value {#return-value-11}

Void.

#### 6.3.4.4 Remarks {#remarks-10}

void.

#### 6.3.4.5 Example {#example-10}

```c
platform_rt_rc_tune(value);
```

## 6.4 RF {#rf}

### 6.4.1 platform_set_rf_clk_source {#platform_set_rf_clk_source}

Select RF clock source. This function is for internal use.

### 6.4.2 platform_set_rf_init_data {#platform_set_rf_init_data}

Customize RF initialization data. This function is for internal use.

### 6.4.3 platform_set_rf_power_mapping {#platform_set_rf_power_mapping}

Power level is represented by an index internally. There is a power mapping table which lists the actual Tx power level of an index. Take ING918 as an example, power index is in a range of [0..63], and power mapping table is an array of 64 entries, each entry giving the Tx power level in 0.01 dBm.

For applications that need better power level control, actual power level can be measured for each index. Update the mapping with this function, then the stack can determine the proper index for a request power level.

#### 6.4.3.1 Prototype {#prototype-13}

```c
void platform_set_rf_power_mapping(
    const int16_t *rf_power_mapping);
```

#### 6.4.3.2 Parameters {#parameters-12}

- `const int16_t *rf_power_mapping`

  The new power mapping table.

#### 6.4.3.3 Return Value {#return-value-12}

Void.

#### 6.4.3.4 Remarks {#remarks-11}

Void.

#### 6.4.3.5 Example {#example-11}

```c

static const int16_t power_mapping[] =
{
    -6337,  // index 0: -63.37dBm
    // ...
    603     // index 63: 6.03dBm
};


platform_set_rf_power_mapping(
    power_mapping);
```

### 6.4.4 platform_patch_rf_init_data {#platform_patch_rf_init_data}

Patch part of the internal RF initialization data. This function is for internal use.

## 6.5 Memory & RTOS {#memory-rtos}

### 6.5.1 platform_call_on_stack {#platform_call_on_stack}

Call a function on a separate dedicated stack. This is useful when a function that uses a lot of stack needs to be called, occasionally.

#### 6.5.1.1 Prototype {#prototype-14}

```c
void platform_call_on_stack(
    f_platform_function f,
    void *user_data,
    void *stack_start,
    uint32_t stack_size);
```

#### 6.5.1.2 Parameters {#parameters-13}

- `f_platform_function f`

  The function to be called.
- `void *user_data`

  User data to be passed to `f`.
- `void *stack_start`

  Start (lowest) address of the dedicated stack.
- `uint32_t stack_size`

  Size of the dedicated stack in bytes.

#### 6.5.1.3 Return Value {#return-value-13}

Void.

#### 6.5.1.4 Remarks {#remarks-12}

Although `stack_size` is provided, this function does not protect the stack from overwritten by `f`.

### 6.5.2 platform_get_current_task {#platform_get_current_task}

Get the current task from which this API is called.

#### 6.5.2.1 Prototype {#prototype-15}

```c
platform_task_id_t platform_get_current_task(void);
```

#### 6.5.2.2 Parameters {#parameters-14}

Void.

#### 6.5.2.3 Return Value {#return-value-14}

```c
typedef enum
{
    PLATFORM_TASK_CONTROLLER,
    PLATFORM_TASK_HOST,
    PLATFORM_TASK_RTOS_TIMER,
} platform_task_id_t;
```

#### 6.5.2.4 Remarks {#remarks-13}

This API is only available in bundles with built-in RTOS.

### 6.5.3 platform_get_gen_os_driver {#platform_get_gen_os_driver}

Get the generic OS driver. For “NoOS” variants, driver provided by app is returned; for bundles with built-in RTOS, an emulated driver is returned.

#### 6.5.3.1 Prototype {#prototype-16}

```c
const void *platform_get_gen_os_driver(void);
```

#### 6.5.3.2 Parameters {#parameters-15}

Void.

#### 6.5.3.3 Return Value {#return-value-15}

Return value is casted from `const gen_os_driver_t *`. Developers can cast the return value back to `const gen_os_driver_t *` and use API in it.

#### 6.5.3.4 Remarks {#remarks-14}

`gen_os_driver_t` is an abstract layer over RTOS. Using API in it instead of RTOS API can make apps cross RTOS (independent of underlying RTOS).

In and after SDK v8.5, since the built-in RTOS can be replaced, things become *tricky* in `app_main`. For backward compatibility, `platform_get_gen_os_driver` will return the emulated driver as elder versions. If developers want to replace the built-in RTOS, this API shall not be used in `app_main`.

### 6.5.4 platform_get_heap_status {#platform_get_heap_status}

Get current status of built-in RTOS’s heap, such as available size, etc.

#### 6.5.4.1 Prototype {#prototype-17}

```c
void platform_get_heap_status(platform_heap_status_t *status);
```

#### 6.5.4.2 Parameters {#parameters-16}

- `platform_heap_status_t *status`

  Heap status.

#### 6.5.4.3 Return Value {#return-value-16}

Void.

#### 6.5.4.4 Remarks {#remarks-15}

Heap status is defined as:

```c
typedef struct
{
    uint32_t bytes_free;                // total free bytes
    uint32_t bytes_minimum_ever_free;   // minimum of bytes_free from startup
} platform_heap_status_t;
```

#### 6.5.4.5 Example {#example-12}

```c
platform_heap_status_t status;
platform_get_heap_status(&status);
```

### 6.5.5 platform_get_rtos_heap_mem {#platform_get_rtos_heap_mem}

Get memory block used as heap by built-in RTOS.

#### 6.5.5.1 Prototype {#prototype-18}

```c
void *platform_get_rtos_heap_mem(int *size);
```

#### 6.5.5.2 Parameters {#parameters-17}

- `int *size`

  Memory block size in byte.

#### 6.5.5.3 Return Value {#return-value-17}

Address of memory block.

#### 6.5.5.4 Remarks {#remarks-16}

When replacing built-in RTOS with a customized one, this memory block is not used at all. Developers can use this API to get its address and size, and utilize it.

#### 6.5.5.5 Example {#example-13}

```c
// initialize this memory block as heap for RT-Thread
int size = 0;
char *heap = platform_get_rtos_heap_mem(&size);
rt_system_heap_init(heap, heap + size);
```

### 6.5.6 platform_get_task_handle {#platform_get_task_handle}

Get RTOS handle of a specific platform task.

#### 6.5.6.1 Prototype {#prototype-19}

```c
uintptr_t platform_get_task_handle(
    platform_task_id_t id);
```

#### 6.5.6.2 Parameters {#parameters-18}

- `platform_task_id_t id`

  Platform task ID.

#### 6.5.6.3 Return Value {#return-value-18}

Task handle if such task is known to platform else 0. For example, in the case of “NoOS” variants, platform does not know the handle of `PLATFORM_TASK_RTOS_TIMER`, so 0 is returned.

### 6.5.7 platform_install_task_stack {#platform_install_task_stack}

Install a new RTOS stack for a specific platform task.

Use this to enlarge stack when the default stack size is not enough for internal tasks. For example, user developed RTOS timer callbacks might require a larger stack space.

Developers can check RTOS documentation for how to check stack usages. For example, `uxTaskGetStackHighWaterMark` in FreeRTOS is used to query how close a task has come to overflowing the stack space allocated to it.

#### 6.5.7.1 Prototype {#prototype-20}

```c
void platform_install_task_stack(
    platform_task_id_t id,
    void *start,
    uint32_t size);
```

#### 6.5.7.2 Parameters {#parameters-19}

- `platform_task_id_t id`

  Task identifier.
- `void *start`

  Start (lowest) address of the stack. Address shall be properly aligned for underlying CPU.
- `uint32_t size`

  Size of the new stack in bytes.

#### 6.5.7.3 Return Value {#return-value-19}

Void.

#### 6.5.7.4 Remarks {#remarks-17}

This function shall only be called in `app_main`.

For NoOS variants, RTOS stacks can be replaced (modify its size, etc) when implementing the generic OS interface.

### 6.5.8 platform_install_isr_stack {#platform_install_isr_stack}

Install a new stack for ISR.

#### 6.5.8.1 Prototype {#prototype-21}

```c
void platform_install_isr_stack(void *top);
```

#### 6.5.8.2 Parameters {#parameters-20}

- `void *top`

  Top of the new stack, which must be properly aligned for the underlying CPU.

#### 6.5.8.3 Return Value {#return-value-20}

Void.

#### 6.5.8.4 Remarks {#remarks-18}

In case apps need a much larger stack than the default one in ISR, a new stack can be installed to replace the default one.

This function is only allowed to be called in `app_main`. The new stack is put into use after `app_main` returns.

#### 6.5.8.5 Example {#example-14}

```c
uint32_t new_stack[2048];
...
platform_install_isr_stack(new_stack + sizeof(new_stack) / sizeof(new_stack[0]));
```

## 6.6 Time & Timers {#time-timers}

API for reading current time (timer counter):

- `platform_get_timer_counter`
- `platform_get_us_time`

API for using timers with 625μs resolution:

- `platform_set_abs_timer`
- `platform_set_timer`
- `platform_delete_timer`

API for using timers with 1μs resolution:

- `platform_create_us_timer`
- `platform_cancel_us_timer`
- `platform_create_us_timer2`

Both types of timers can be used with power saving, i.e. it just works as expected when power saving is enabled. A comparison of of these two types of timers is shown in Table [6.1](https://ingchips.github.io/user_guide/api-ref.html#tab:ch-api-compare-timers).

*Table 6.1: Two Types of Platform Timers*
| Type | 625μs resolution | 1μs resolution |
| --- | --- | --- |
| Callback | Invoked from a task-like context | Invoked from an ISR or caller |
| Identifier | Callback function pointer | Timer handle |
| Capacity | Limited by heap | Only a few |

Timers with 1μs resolution are redesigned in SDK v8.5.

- In elder versions,

  API are actually wrapper around some Controller functions, where `platform_create_us_timer` is scheduling an operation with a duration of 1μs at time *T*. Therefore, if Controller *will be doing* something like Scanning or Advertising around time *T*, `platform_create_us_timer` will fail. Calling `platform_create_us_timer` in `callback` is also **forbidden**.
- In and after v8.5,

  This type of timer is not a wrapper any more, and `platform_create_us_timer` will succeed in such cases and Controller uses this interface for managing all RF operations. `platform_create_us_timer` can be called in `callback`.

`platform_create_us_timer` allocates data from a dedicated memory pool size of which is fixed and limited. In and after v8.5, up to 4 timers can be created. Note that Controller uses exactly one such timer. If Controller fails to create a timer, event `PLATFORM_CB_EVT_HEAP_OOM` is raised.

### 6.6.1 platform_cancel_us_timer {#platform_cancel_us_timer}

Cancel a platform timer previously created by `platform_create_us_timer`.

#### 6.6.1.1 Prototype {#prototype-22}

```c
int platform_cancel_us_timer(
    platform_us_timer_handle_t timer_handle);
```

#### 6.6.1.2 Parameters {#parameters-21}

- `platform_us_timer_handle_t timer_handle`

  Handle of the timer.

#### 6.6.1.3 Return Value {#return-value-21}

This function returns 0 if the specified time is canceled successfully. Otherwise, a non-0 value is returned, which also means the callback function of the timer is executing.

### 6.6.2 platform_create_us_timer {#platform_create_us_timer}

Setup a single-shot platform timer with 1 microsecond (μs) resolution.

#### 6.6.2.1 Prototype {#prototype-23}

```c
platform_us_timer_handle_t platform_create_us_timer(
    uint64_t abs_time,
    f_platform_us_timer_callback callback,
    void *param);
```

#### 6.6.2.2 Parameters {#parameters-22}

- `uint64_t abs_time`

  When `platform_get_us_timer() == abs_time`, the callback is invoked.
- `f_platform_us_timer_callback callback`

  The callback function. The signature is:

  ```c
  typedef void (* f_platform_us_timer_callback)(
      platform_us_timer_handle_t timer_handle,
      uint64_t time_us,
      void *param);
  ```

  Where, `timer_handle` is the returned value of `platform_create_us_timer`, i.e., `time_us` is current value of `platform_get_us_timer` when invoking the callback, and `param` is the user parameter when creating this timer.
- `void *param`

  User parameter.

#### 6.6.2.3 Return Value {#return-value-22}

This function returns a handle of the created timer. A non-NULL value is returned when the timer is successfully created. Otherwise, NULL is returned.

#### 6.6.2.4 Remarks {#remarks-19}

Although `abs_time` is in microsecond (μs), callback is **not guaranteed** to be invoked with such resolution.

Pseudo code:

```c
create_us_timer(..)
{
    if (out of memory) return NULL;
    r = allocate a handle;
    if (timer is too near) {
        // callback is invoked immediately in the context of the caller
        callback(param);
        free memory;
        return r;        // a non-NULL value is returned
    }
    save r into a queue; // callback will be invoked in an ISR later
    return r;
}
```

### 6.6.3 platform_create_us_timer2 {#platform_create_us_timer2}

Setup a single-shot platform timer with 1 microsecond (μs) resolution.

#### 6.6.3.1 Prototype {#prototype-24}

```c
int platform_create_us_timer2(
    uint64_t abs_time,
    f_platform_us_timer_callback callback,
    void *param,
    platform_us_timer_handle_t *timer_handle);
```

#### 6.6.3.2 Parameters {#parameters-23}

- `uint64_t abs_time`

  When `platform_get_us_timer() == abs_time`, the callback is invoked.
- `f_platform_us_timer_callback callback`

  The callback function.
- `void *param`

  User parameter.
- `platform_us_timer_handle_t *timer_handle`

  Handle of the created timer if successfully created. Otherwise, `timer_handle` is set to NULL.

#### 6.6.3.3 Return Value {#return-value-23}

`0` is returned when the timer is successfully created. Otherwise, `-1` is returned.

#### 6.6.3.4 Remarks {#remarks-20}

It is common practice to clear the handle in the `callback`. This could be problematic using `platform_create_us_timer`. For example:

```c
platform_us_timer_handle_t handle;
void callback(...)
{
    handle = NULL;
}

// callback might be called before this functions returns
// so, handle would not be cleared.
handle = platform_create_us_timer(T,
    callback);
```

`platform_create_us_timer2` is provided to solve such issues.

```c
// handle is set properly by `platform_create_us_timer2`
// before calling `callback`.
platform_create_us_timer2(T,
    callback,
    &handle);
```

### 6.6.4 platform_delete_timer {#platform_delete_timer}

Delete a previously platform timer created by `platform_set_timer` or `platform_set_abs_timer`.

#### 6.6.4.1 Prototype {#prototype-25}

```c
void platform_delete_timer(f_platform_timer_callback callback)
```

#### 6.6.4.2 Parameters {#parameters-24}

- `f_platform_timer_callback callback`

  The callback function, which is also an identifier for the timer.

#### 6.6.4.3 Return Value {#return-value-24}

Void.

#### 6.6.4.4 Remarks {#remarks-21}

When calling this function, the callback might already be queued for invoking in the task. Therefore, the callback might still be invoked after this function is called.

### 6.6.5 platform_get_timer_counter {#platform_get_timer_counter}

Read the counter of platform timer at 625μs resolution.

#### 6.6.5.1 Prototype {#prototype-26}

```c
uint32_t platform_get_timer_counter(void);
```

#### 6.6.5.2 Parameters {#parameters-25}

Void.

#### 6.6.5.3 Return Value {#return-value-25}

A full 32 bits value represents current counter, which is roughly `platform_get_us_time() / 625`.

### 6.6.6 platform_get_us_time {#platform_get_us_time}

Read the internal time counting from BLE initialization.

#### 6.6.6.1 Prototype {#prototype-27}

```c
int64_t platform_get_us_time(void);
```

#### 6.6.6.2 Parameters {#parameters-26}

Void.

#### 6.6.6.3 Return Value {#return-value-26}

Value of the internal time counter counting at 1μs. This counter wraps around every ~21.8 years.

#### 6.6.6.4 Remarks {#remarks-22}

This counter restarts after shutdown.

#### 6.6.6.5 Example {#example-15}

```c
uint64_t now = platform_get_us_time();
```

### 6.6.7 platform_set_abs_timer {#platform_set_abs_timer}

Setup a single-shot platform timer triggered at an absolute time with 625μs resolution.

#### 6.6.7.1 Prototype {#prototype-28}

```c
void platform_set_abs_timer(
    f_platform_timer_callback callback,
    uint32_t abs_time);
```

#### 6.6.7.2 Parameters {#parameters-27}

- `f_platform_timer_callback callback`

  The callback function when the timer expired, and is called in a RTOS task-like[29](#fn29) context, but not an ISR.
- `uint32_t abs_time`

  when `platform_get_timer_counter() == abs_time`, `callback` is invoked. If `abs_time` just passes `platform_get_timer_counter()`, `callback` is invoked immediately, for example, `abs_time` is `platform_get_timer_counter() - 1`.

#### 6.6.7.3 Return Value {#return-value-27}

Void.

#### 6.6.7.4 Remarks {#remarks-23}

This function always succeeds, except when running out of memory.

#### 6.6.7.5 Example {#example-16}

Use this function to emulate a periodic timer.

```c

#define PERIOD  100
static uint32_t last_timer = 0;

void platform_timer_callback(void)
{
    last_timer += PERIOD;
    platform_set_abs_timer(platform_timer_callback, last_timer);

    // do periodic job
    // ...
}

last_timer = platform_get_timer_counter() + PERIOD;
platform_set_abs_timer(platform_timer_callback, last_timer);
```

### 6.6.8 platform_set_timer {#platform_set_timer}

Setup a single-shot platform timer after a delay from “now” with 625μs resolution.

#### 6.6.8.1 Prototype {#prototype-29}

```c
void platform_set_timer(
    f_platform_timer_callback callback,
    uint32_t delay);
```

#### 6.6.8.2 Parameters {#parameters-28}

- `f_platform_timer_callback callback`

  The callback function when the timer expired, and is called in a RTOS task-like context, but not an ISR.
- `uint32_t delay`

  Time delay before the timer expires (unit: 625μs).

  Valid Range: 0~0x7fffffff. When `delay` is 0, the timer is cleared.

#### 6.6.8.3 Return Value {#return-value-28}

Void.

#### 6.6.8.4 Remarks {#remarks-24}

This function always succeeds, except when running out of memory.

`platform_set_timer(f, 100)` is equivalent to:

```c
platform_set_abs_timer(f,
    platform_get_timer_counter() + 100);
```

`platform_set_timer(f, 0)` is equivalent to:

```c
platform_delete_timer(f);
```

but not

```c
platform_set_abs_timer(f,
    platform_get_timer_counter() + 0);
```

Since `callback` is also the identifier of the timer, below two lines defines only a timer expiring after 200 units but not two separate timers:

```c
platform_set_timer(f, 100);
platform_set_timer(f, 200); // update the timer, but not creating a new one
```

If `f` is used once again in `platform_set_abs_timer`, then the timer is updated again:

```c
platform_set_abs_timer(f, ...);
```

## 6.7 Power Saving {#power-saving}

This section provides APIs for implementing power saving in RTOS. See “Programmer’s Guide - Power Saving”[30](#fn30) for more information.

### 6.7.1 platform_pre_suppress_cycles_and_sleep_processing {#platform_pre_suppress_cycles_and_sleep_processing}

Prepare to suppress some cycles for tick-less power saving.

#### 6.7.1.1 Prototype {#prototype-30}

```c
uint32_t platform_pre_suppress_cycles_and_sleep_processing(
    uint32_t expected_cycles);
```

#### 6.7.1.2 Parameters {#parameters-29}

- `uint32_t expected_cycles`

  Excepted cycles that can be suppressed (skipped safely in power saving modes).

  Full range of `uint32_t` is supported.

#### 6.7.1.3 Return Value {#return-value-29}

Adjusted cycles that can be suppressed.

### 6.7.2 platform_pre_sleep_processing {#platform_pre_sleep_processing}

Preprocessing for tick-less sleep.

#### 6.7.2.1 Prototype {#prototype-31}

```c
void platform_pre_sleep_processing(void);
```

#### 6.7.2.2 Parameters {#parameters-30}

Void.

#### 6.7.2.3 Return Value {#return-value-30}

Void.

### 6.7.3 platform_post_sleep_processing {#platform_post_sleep_processing}

Postprocessing for tick-less sleep.

#### 6.7.3.1 Prototype {#prototype-32}

```c
void platform_post_sleep_processing(void);
```

#### 6.7.3.2 Parameters {#parameters-31}

Void.

#### 6.7.3.3 Return Value {#return-value-31}

Void.

#### 6.7.3.4 Remarks {#remarks-25}

If `platform_pre_sleep_processing` is called, it must be followed by `platform_post_sleep_processing`.

### 6.7.4 platform_os_idle_resumed_hook {#platform_os_idle_resumed_hook}

Hook for Idle task got resumed. Call this when Idle task is resumed.

#### 6.7.4.1 Prototype {#prototype-33}

```c
void platform_os_idle_resumed_hook(void);
```

#### 6.7.4.2 Parameters {#parameters-32}

Void.

#### 6.7.4.3 Return Value {#return-value-32}

Void.

### 6.7.5 platform_pre_suppress_ticks_and_sleep_processing {#platform_pre_suppress_ticks_and_sleep_processing}

Pre-suppress ticks and sleep processing. This API is obsoleted. Use `platform_pre_suppress_cycles_and_sleep_processing` instead.

## 6.8 Utilities {#utilities}

### 6.8.1 platform_hrng {#platform_hrng}

Generate random bytes by using hardware random-number generator.

#### 6.8.1.1 Prototype {#prototype-34}

```c
void  platform_hrng(uint8_t *bytes, const uint32_t len);
```

#### 6.8.1.2 Parameters {#parameters-33}

- `uint8_t *bytes`

  Random data output.
- `const uint32_t len`

  Number of random bytes to be generated.

#### 6.8.1.3 Return Value {#return-value-33}

Void.

#### 6.8.1.4 Remarks {#remarks-26}

Time consumption to generate a fix length of data is undetermined.

#### 6.8.1.5 Example {#example-17}

```c
uint32_t strong_random;
platform_hrng(&strong_random, sizeof(strong_random));
```

### 6.8.2 platform_rand {#platform_rand}

Generate a pseudo random integer by internal PRNG.

#### 6.8.2.1 Prototype {#prototype-35}

```c
int platform_rand(void);
```

#### 6.8.2.2 Parameters {#parameters-34}

Void.

#### 6.8.2.3 Return Value {#return-value-34}

A pseudo random integer in range of 0 to RAND_MAX.

#### 6.8.2.4 Remarks {#remarks-27}

Seed of the internal PRNG is initialized by HRNG at startup. This function can be used as a replacement of `rand()` in standard library.

#### 6.8.2.5 Example {#example-18}

```c
printf("rand: %d\n", platform_rand());
```

### 6.8.3 platform_read_persistent_reg {#platform_read_persistent_reg}

Read value from the persistent register. See also [`platform_write_persistent_reg`](https://ingchips.github.io/user_guide/api-ref.html#platform_write_persistent_reg).

#### 6.8.3.1 Prototype {#prototype-36}

```c
uint32_t platform_read_persistent_reg(void);
```

#### 6.8.3.2 Parameters {#parameters-35}

Void.

#### 6.8.3.3 Return Value {#return-value-35}

The value written by [`platform_write_persistent_reg`](https://ingchips.github.io/user_guide/api-ref.html#platform_write_persistent_reg).

#### 6.8.3.4 Remarks {#remarks-28}

Void.

#### 6.8.3.5 Example {#example-19}

```c
platform_read_persistent_reg();
```

### 6.8.4 platform_reset {#platform_reset}

Reset platform (SoC).

#### 6.8.4.1 Prototype {#prototype-37}

```c
void platform_reset(void);
```

#### 6.8.4.2 Parameters {#parameters-36}

Void.

#### 6.8.4.3 Return Value {#return-value-36}

Void.

#### 6.8.4.4 Remarks {#remarks-29}

When calling this function, the code after it will not be executed.

#### 6.8.4.5 Example {#example-20}

```c
  if (out-of-memory)
    platform_reset();
```

### 6.8.5 platform_shutdown {#platform_shutdown}

Bring the whole system into shutdown state, and reboot after a specified duration. Optionally, a portion of memory can be retained during shutdown, and apps can continue to use it after reboot.

Note that this function will NOT return except that shutdown procedure fails to initiate. Possible causes for failures include:

1. External wake-up signal is issued;
2. Input parameters are not proper;
3. Internal components are busy.

#### 6.8.5.1 Prototype {#prototype-38}

```c
void platform_shutdown(const uint32_t duration_cycles,
                       const void *p_retention_data,
                       const uint32_t data_size);
```

#### 6.8.5.2 Parameters {#parameters-37}

- `const uint32_t duration_cycles`

  Duration (measured in cycles of real-time clock) before power on again (reboot). The minimum duration is 825 cycles (about 25.18ms). If `0` is used, the system will stay in shutdown state until external wake-up signal is issued.
- `const void *p_retention_data`

  Pointer to the start of data to be retained. Only data within SYSTEM memory can be retained. This parameter can be set to `NULL` when `data_size` is `0`.
- `data_size`

  Size of the data to be retained. Set to `0` when memory retention is not needed.

#### 6.8.5.3 Return Value {#return-value-37}

Void.

#### 6.8.5.4 Remarks {#remarks-30}

Void.

#### 6.8.5.5 Example {#example-21}

```c
// Shutdown the system and reboot after 1s.
platform_shutdown(32768, NULL, 0);
```

### 6.8.6 platform_write_persistent_reg {#platform_write_persistent_reg}

Write a value to the persistent register. This value is kept even in power saving, shutdown mode, or when switching to another app.

Only a few bits are saved as shown in Table [6.2](https://ingchips.github.io/user_guide/api-ref.html#tab:ch-api-reg-bits).

*Table 6.2: Persistent Register Bit Size*
| Chip Family | Register Size (bit) |
| --- | --- |
| ING918 | 4 |
| ING916 | 5 |

#### 6.8.6.1 Prototype {#prototype-39}

```c
void platform_write_persistent_reg(const uint8_t value);
```

#### 6.8.6.2 Parameters {#parameters-38}

- `const uint8_t value`

  The value.

#### 6.8.6.3 Return Value {#return-value-38}

Void.

#### 6.8.6.4 Remarks {#remarks-31}

Void.

#### 6.8.6.5 Example {#example-22}

```c
platform_write_persistent_reg(1);
```

## 6.9 Debugging & Tracing {#debugging-tracing-1}

### 6.9.1 platform_printf {#platform_printf}

The `printf` function stored in platform binary.

#### 6.9.1.1 Prototype {#prototype-40}

```c
 void  platform_printf(const char *format, ...);
```

#### 6.9.1.2 Parameters {#parameters-39}

- `const char *format`

  Format string.
- `...`

  Variable arguments for format string.

#### 6.9.1.3 Return Value {#return-value-39}

Void.

#### 6.9.1.4 Remarks {#remarks-32}

There are pros & cons to use this function.

Pros:

- This function is located in platform binary, app binary size can be saved.

Cons:

- Output is directed `PLATFORM_CB_EVT_PUTC` event, so its callback function must be defined.

#### 6.9.1.5 Example {#example-23}

```c
platform_printf("Hello world");
```

### 6.9.2 platform_raise_assertion {#platform_raise_assertion}

Raise a software assertion.

#### 6.9.2.1 Prototype {#prototype-41}

```c
void  platform_raise_assertion(const char *file_name, int line_no);
```

#### 6.9.2.2 Parameters {#parameters-40}

- `const char *file_name`

  File name where the assertion occurred.
- `int line_no`

  Line number where the assertion occurred.

#### 6.9.2.3 Return Value {#return-value-40}

Void.

#### 6.9.2.4 Remarks {#remarks-33}

Void.

#### 6.9.2.5 Example {#example-24}

```c
  if (NULL == ptr)
    platform_raise_assertion(__FILE__, __LINE__);
```

### 6.9.3 platform_trace_raw {#platform_trace_raw}

Output a block of raw data to TRACE. ID is `PLATFORM_TRACE_ID_RAW`.

#### 6.9.3.1 Prototype {#prototype-42}

```c
void platform_trace_raw(
    const void *buffer,
    const int byte_len);
```

#### 6.9.3.2 Parameters {#parameters-41}

- `const void *buffer`

  Pointer of the buffer.
- `const int byte_len`

  Length of data buffer in bytes.

## 6.10 Others {#others}

### 6.10.1 platform_get_link_layer_interf {#platform_get_link_layer_interf}

Get link layer driver API.

#### 6.10.1.1 Prototype {#prototype-43}

```c
const platform_hci_link_layer_interf_t *
    platform_get_link_layer_interf(void);
```

#### 6.10.1.2 Parameters {#parameters-42}

Void.

#### 6.10.1.3 Return Value {#return-value-41}

The driver interface `platform_hci_link_layer_interf_t *`.

#### 6.10.1.4 Remarks {#remarks-34}

This API exposes the Controller HCI interface. This driver interface is only available when `PLATFORM_CB_EVT_HCI_RECV` is defined, in which case, the built in Host is disabled.

### 6.10.2 sysSetPublicDeviceAddr {#syssetpublicdeviceaddr}

Set the public address of device.

The public address of a BLE device is a 48-bit extended unique identifier (EUI-48) created in accordance with the IEEE 802-2014 standard[31](#fn31).

*INGCHIPS* 91x *DO NOT* have public addresses. This function should *ONLY* be used for debugging or testing, and *NEVER* be used in final products.

#### 6.10.2.1 Prototype {#prototype-44}

```c
void sysSetPublicDeviceAddr(const unsigned char *addr);
```

#### 6.10.2.2 Parameters {#parameters-43}

- `const unsigned char *addr`

  New public address.

#### 6.10.2.3 Return Value {#return-value-42}

Void.

#### 6.10.2.4 Remarks {#remarks-35}

In order to avoid potential issues, this function should be called before calling any GAP functions. It is recommended to call this function in `app_main` or `PLATFORM_CB_EVT_PROFILE_INIT` event callback function.

#### 6.10.2.5 Example {#example-25}

```c
const unsigned char pub_addr[] = {1,2,3,4,5,6};
sysSetPublicDeviceAddr(pub_addr);
```

---

1. <a id="fn24"></a>[https://ingchips.github.io/application-notes/pg_ble_stack_cn/index.html](https://ingchips.github.io/application-notes/pg_ble_stack_cn/index.html)[↩︎](https://ingchips.github.io/user_guide/api-ref.html#fnref24)
2. <a id="fn25"></a>[https://ingchips.github.io/application-notes/pg_power_saving_en/](https://ingchips.github.io/application-notes/pg_power_saving_en/)[↩︎](https://ingchips.github.io/user_guide/api-ref.html#fnref25)
3. <a id="fn26"></a>[https://ingchips.github.io/application-notes/pg_power_saving_en/ch-api.html#the-real-time-clock](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-api.html#the-real-time-clock)[↩︎](https://ingchips.github.io/user_guide/api-ref.html#fnref26)
4. <a id="fn27"></a>[https://ingchips.github.io/application-notes/pg_power_saving_en/](https://ingchips.github.io/application-notes/pg_power_saving_en/)[↩︎](https://ingchips.github.io/user_guide/api-ref.html#fnref27)
5. <a id="fn28"></a>Starting from v8.4.6. For elder version, 32768Hz is used.[↩︎](https://ingchips.github.io/user_guide/api-ref.html#fnref28)
6. <a id="fn29"></a>It’s called from the Controller task if existing.[↩︎](https://ingchips.github.io/user_guide/api-ref.html#fnref29)
7. <a id="fn30"></a>[https://ingchips.github.io/application-notes/pg_power_saving_en/](https://ingchips.github.io/application-notes/pg_power_saving_en/)[↩︎](https://ingchips.github.io/user_guide/api-ref.html#fnref30)
8. <a id="fn31"></a>[http://standards.ieee.org/findstds/standard/802-2014.html](http://standards.ieee.org/findstds/standard/802-2014.html)[↩︎](https://ingchips.github.io/user_guide/api-ref.html#fnref31)