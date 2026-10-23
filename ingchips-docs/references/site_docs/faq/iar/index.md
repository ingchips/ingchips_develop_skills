# IAR 相关问题

## 1. 如何将 Keil μVision 项目转换为 IAR 项目？ {#1-如何将-keil-μvision-项目转换为-iar-项目}

- **建议**：通过 Wizard 向导创建一个新的 IAR 项目，逐一添加 Keil 项目里的源代码；
- **不推荐** 使用 IAR Project Converter。

---

## 2. 开始调试时弹出对话框提示无法在 main 上打断点，如何解决？ {#2-开始调试时弹出对话框提示无法在-main-上打断点如何解决}

![](https://ingchips.github.io/docs/faq/img/iar_err_main.png)

**临时解决方案**：关闭 IAR IDE，在 *项目目录/settings* 文件夹内找到 *.dnx 文件，可看到文件里有如下内容：

```highlight
<Stack>
    ...
    <UseTrigger>1</UseTrigger>
    <TriggerName>main</TriggerName>
    ...
</Stack>
```

根据需要将 *UseTrigger* 改为 0，或者将 *TriggerName* 改为 *app_main*。

---

---

- [IAR 相关问题](https://ingchips.github.io/docs/faq/iar/)
