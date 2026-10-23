<!-- pg_power_saving_en: 7 FAQ -->

# 7 FAQ {#ch-faq}

- **Q**: Why do the reconfiguration in event handler of waking up? The framework can remember all peripheral configurations and reconfigure them.
- **A**: Configure a peripheral is not an easy job like writing a bulk of registers. It’s impractical to handle all peripherals one by one. On the other hand, it’s easy for Apps to reconfigure them, as the code is ready there.

---

- **Q**: What happened to CPU in sleep modes of Category B?
- **A**: It’s powered off.

---

- **Q**: How to debug programs when power saving is enabled?
- **A**: It depends on which part of programs need to be debugged.

  For the part between PLATFORM_CB_EVT_BEFORE_DEEP_SLEEP and PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP, it’s generally not debug-able.

  For other parts, firstly, disable power saving and debug it as usual. After everything is OK, re-enable power saving. Or, in the handler of PLATFORM_CB_EVT_QUERY_DEEP_SLEEP_ALLOWED, check if debugger is attached, and if so, disallow sleep modes of Category B:

  ```c
  uint32_t query_deep_sleep_allowed(void *dummy,
    void *user_data)
  {
    if (IS_DEBUGGER_ATTACHED())
      return 0;

    // ....
  }
  ```

---