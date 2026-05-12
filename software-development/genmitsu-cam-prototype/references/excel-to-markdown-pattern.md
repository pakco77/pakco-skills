# Excel 宽表转 Markdown 技术参考

## 场景

Genmitsu 产品线有一个 119行×31列 的 Excel（机型为列、参数为行），需要转成可读的 Markdown 存入 Obsidian。直接横着放不可读（31列太宽），需要翻转 + 过滤。

## 技术要点

### 1. 读取 Excel
- 使用 `openpyxl`（系统 Python3 已装：`/usr/bin/python3`）
- 注意：hermes-agent venv 可能没有 openpyxl，fallback 到系统 Python
- 大文件用 `iter_rows(values_only=True)` 避免内存问题

### 2. 翻转策略
- 原始方向：参数为行（119行），机型为列（31列）
- 目标方向：机行为行（23款活跃机型），参数为列
- 分行类别生成多个子表（基本信息/工作范围/X轴传动/主轴/控制/辅助功能等）

### 3. 过滤规则
- 只保留活跃机型（排除含 "Discontinued" 的列）
- 用 Python string matching：`"Discontinued" not in name`

### 4. 输出结构
```markdown
# 标题
> 来源：xxx.xlsx | 生成日期

## 活跃机型一览
| # | 机型 | 系列 |

## 核心参数速查表
| 参数 | 机型1 | 机型2 | ... |

## 详细参数（按类别）
### 基本信息
### 工作范围与尺寸
### X轴传动
...
```

### 5. S级上下文更新
- 在详细表之外，为 S 级系统上下文生成一份精简速查表
- 只取 9 款代表机型（按行程分级：入门/进阶/桌面/中型/大型）
- 加关键约束速记（控制协议/材料/刀具/激光/第四轴）

## 代码模板

```python
import openpyxl

wb = openpyxl.load_workbook(path)
ws = wb[sheet_name]

# 读取表头
headers = [str(c.value) if c.value else "" for c in next(ws.iter_rows(max_row=1))]
machines = headers[2:]  # 跳过参数名列和单位列

# 过滤活跃机型
active = [(i+2, m.strip()) for i, m in enumerate(machines) 
          if "Discontinued" not in m and m.strip()]

# 按行索引取参数值
def get_param(row_idx, col_indices):
    row = list(ws.iter_rows(min_row=row_idx+1, max_row=row_idx+1, values_only=True))[0]
    return {name: (str(row[col]) if row[col] is not None else "—") 
            for col, name in col_indices}

# 生成 Markdown 表
for cat_name, row_indices, param_labels in categories:
    md += f"### {cat_name}\n"
    md += "| 参数 | " + " | ".join(n for _, n in active) + " |\n"
    ...
```

## 已生成文件
- 完整表：`0_S_背景级资料/004_S_硬件产品参数/Genmitsu_CNC_硬件参数表.md`
- S级速查：已嵌入 `0_S_背景级资料/001_S_规则/1_系统级上下文.md` §五
