# Genmitsu CAM 项目核心上下文

> 交付PM 在派发子代理时的必读背景。子代理不直接读此文件——交付PM 摘取相关片段注入 context。

## 产品定位

**Genmitsu CAM** 是一 Web 端 CAM 软件，为 Genmitsu CNC 雕刻机用户提供**从设计到加工的一站式体验**。核心差异化：**硬件深度预配置 + 全链路打通**。

定位公式：**Genmitsu 机器的官方数字伴侣（Official Digital Companion）**。

## MVP 功能范围

### Day 1（必须有）
- 项目管理（创建/打开/保存）
- 设计画布（导入 SVG/DXF、基础形状、文字、对象变换、图层）
- 刀路生成（轮廓切割、口袋加工、钻孔、V-Carving、刀路预览）
- ★ Genmitsu 机器预设库（3018-PROVer, 4030, PROVer XL 等）
- ★ 官方刀具库（随机附带刀具参数预设）
- ★ 材料-刀具推荐组合
- G-code 导出（GRBL）
- 新手引导 + 上下文帮助

★ = 核心差异化功能

### V1.1（1-2个月后）
- 项目模板库、Tab 自动生成、高级刀路参数、项目分享、自定义机器配置

### V2（3-6个月后）
- WebSerial 直连、激光模块、社区市场、AI 辅助、手机端、多语言

## 竞品矩阵

| 竞品 | 形态 | 定位 | 核心启示 |
|------|------|------|----------|
| **Easel** | Web App | 一体化 CNC 工作台 | CAD/CAM/Sender 全链路、机器 Profile 体系 |
| **easyCrave** | Web App | 引导式浮雕 CAM | 线性 4 步法、渐进式信息暴露、上下文帮助 |
| **Candle/UGS** | 桌面端 | G-code 发送器 | 体验粗糙但免费 |
| **LightBurn** | 桌面端 | 激光专精 | 不做 CNC |

## 目标用户

- CNC 入门到中级用户
- 使用 Genmitsu 机器（3018、4030、PROVer XL 等）
- 场景：2D 切割、2.5D 浮雕加工
- 常见加工：亚克力字、PCB、铝件面板、木工榫卯

## 现有资产

- v0.1 画布工作台（已存在，非本次设计）
- 位于 `/Users/pakco/Desktop/SainStore/01_Genmitsu/CAM/CNC/`
- 已有问题收集文档（bug list）
- 设计讨论记录在 Obsidian：`/Users/pakco/Documents/Obsidian Vault/Genmitsu/Agents team 思考工程/`

## 变现模型

- Genmitsu 机器用户：注册绑定序列号，全功能免费
- 非 Genmitsu 用户：Freemium，Pro 版 $7.99/月

## 技术约束

- Web 端（浏览器运行）
- 原生 JS/CSS/HTML 原型（不用 React/Vue 框架以避免上下文膨胀）
- 刀路计算为简化仿真（非真实 CAM 算法）
- 3D 模拟用 Three.js 或原生 WebGL
