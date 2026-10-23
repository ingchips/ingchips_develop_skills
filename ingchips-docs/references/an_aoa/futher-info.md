<!-- an_aoa: 6 Further Information -->

# 6 Further Information {#futher-info}

## 6.1 Algorithm Integeration {#algorithm-integeration}

A command line tool called `alg` which performs the same algorithm as *Real-time Locating Demo* is provided in the *RTL* sub-directory of SDK. It uses ASCII strings over standard input/output as external interface, and can be integrated into locating systems easily.

`alg` reads a whole line as input, and output a line containing the result in JSON format, as shown in Table [6.1](https://ingchips.github.io/application-notes/an_aoa/futher-info.html#tab:ch4-json-result). The input is a prefix “EXT0:” followed by the Base64 encoding of below packed data structure `le_meta_pro_connless_iq_report`:

```c
typedef struct le_iq_sample
{
    int8_t i;
    int8_t q;
} le_iq_sample_t;

typedef struct le_meta_pro_connless_iq_report
{
    uint8_t addr_type;
    uint8_t addr[6];
    phy_type_t rx_phy;
    uint8_t  channel_index;
    int16_t  rssi;
    uint8_t  rssi_ant_id;
    uint8_t  cte_type;
    uint8_t  slot_durations;
    uint8_t  packet_status;
    uint8_t  sample_count;
    le_iq_sample_t samples[0];
} le_meta_pro_connless_iq_report_t;
```

*Table 6.1: Fields in the JSON Output*
| Field | Note |
| --- | --- |
| status | A string describing if error occurs in the processing of the input. |
| id | A string representing the tag’s address. Only available when status is “ok”. |
| azimuth | Estimated azimuth of the tag in degree. Only available when status is “ok”. |
| elevation | Estimated elevation of the tag in degree. Only available when status is “ok”. |

An example session of `alg`:

```shell
EXT0:ABTzMRQuhAERPv4AAAEAUt7PziEgMjTh4s3LHRw1N+gdE5o/Ka0+1ykTnyI
E3jv6NjPB+NjYId40J8MH8LQ59g0fhwBKyUr3HCSc6xXlNxgVRszb8cks8xo8xuo
WtzcQ/SKWx1v3RRsHLbG/HvImLfNJ5MgLyC4I/UHY0TfKJyrtHLydVCUtOvIr2qE
iAgk70DgCwCXVJB7cNfXDS+0NOeEO+Ig7Rg1J3x4MmhwT7Ti7GyHK
{"status": "ok", "id": "P:84:2E:14:31:F3:14", "azimuth": 174.0, 
"elevation": 48.0 }
```

Note that, the input must be in a single line.

## 6.2 Evaluation of Different Antenna Array Types {#evaluation-of-different-antenna-array-types}

To assist the evaluation of different antenna array types, both `alg` and *Real-time Locating Demo* might accept an additional command option to specify a sub portion of the whole antenna array board by “`alg -array {TYPE}`” or “`RTLing_xx -array {TYPE}`”. When using this option, the switching pattern used in the firmware (*Central CTE* example) should be updated accordingly.

*Table 6.2: Supported Array Types for 4x4 Antenna Array Board (Rectangle)*
| {TYPE} | Switching Pattern | Note |
| --- | --- | --- |
| 4x4 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Whole array is used (default) |
| 3x3 | 0, 1, 2, 4, 5, 6, 8, 9, 10 | 3 \times 3 URA sub-array |
| 2x2 | 0, 1, 4, 5 | 2 \times 2 URA sub-array |
| 1x4 | 0, 1, 2, 3 | 1 \times 4 ULA sub-array |
| 1x3 | 0, 1, 2 | 1 \times 3 ULA sub-array |
| 1100 | 0, 1 | 1 \times 2 ULA sub-array |
| 1010 | 0, 2 | 1 \times 2 ULA sub-array |
| 1001 | 0, 3 | 1 \times 2 ULA sub-array |

*Table 6.3: Supported Array Types for 3x3 Antenna Array Board (Round)*
| {TYPE} | Switching Pattern | Note |
| --- | --- | --- |
| o3x3 | 0, 1, 2, 3, 4, 5, 6, 7, 8 | Whole array is used |

For example, if we want to evaluate the performance of 1x4 ULA sub-array on 4x4 Antenna Array Board (Rectangle), then

1. Change the switching pattern used in *Central CTE* to 0, 1, 2, 3,
2. Build *Central CTE* and download it to the Antenna Array Board,
3. Start `alg` by `alg -array 1x4`, or,
4. Start *Real-time Locating Demo* by “`RTLing_dx -array 1x4`” or “`RTLing_gl -array 1x4`”.