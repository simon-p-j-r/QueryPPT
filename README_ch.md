

# QueryPPT：从查询到演示文稿的智能生成框架

**QueryPPT** 是一个创新的自动化演示文稿生成框架，旨在将用户的简明自然语言查询（query）直接转化为内容丰富、视觉协调的演示文稿。该框架突破了传统方法对结构化文档的依赖，通过“智能内容生成”和“自适应演示文稿创建”两大阶段，实现了从零开始的“Query to All”自动化流程。

本项目由两个核心子模块构成：

* **DeepPPT**：负责第一阶段的智能内容生成。
* **Adaptive Presentation Creation (APC)**：负责第二阶段的自适应演示文稿创建。

---

## 📖 项目介绍

QueryPPT, From Query to All: Web-Enhanced Content and Intelligent Layout for Stunning Presentations

自动化演示文稿（PPT）生成是提高生产力的重要方向，QueryPPT 提出了一种新颖的端到端框架，能够直接从用户的简明自然语言查询（query）自动化生成内容丰富且视觉协调的演示文稿。


<p align="center" width="100%">
<img src="https://github.com/simon-p-j-r/QueryPPT/blob/main/QueryPPT.png" alt="QueryPPT 架构图" style="width: 90%; height: auto; display: inline-block; margin: auto; border-radius: 40%;">
</p>

QueryPPT 的核心思想在于将复杂的生成过程解耦为两个协同工作的阶段：

1. **智能内容生成**：此阶段由一个中央“planner agent”主导，它首先解析用户意图并进行任务规划。随后，该 planner 协调多个“researcher agent”执行并行的网页搜索与内容提炼任务。“Imagent agent”对检索到的图片进行分析与摘要，以辅助生成图文并茂的章节。所有内容最终由“recorder”模块整合成一份结构完整的内容大纲。

2. **自适应演示文稿创建**：此阶段专注于视觉呈现。首先，“painter agent”根据用户查询的风格和主题，动态生成标题页与内容页的背景图像。紧接着，“colorist agent”依据生成的背景智能地推断出最佳的字体颜色方案。在布局方面，我们提供了两种灵活策略：“architect agent”采用组件化布局，根据内容动态适配预设的视觉组件；而“mapper agent”则采用预定义幻灯片组合，将内容高效地填充至设计好的模板中。

---

## 📚 如何使用

本项目分为两个独立的模块，每个模块都有详细的使用说明。请根据您的需求，参考对应的 `README` 文件。

### 1. DeepPPT（智能内容生成）

此模块负责根据您的查询，通过网络搜索和多智能体协作，生成结构化的 Markdown 内容。

📘 **详细指南请参阅：**
👉 [`DeepPPT/README_zh.md`](DeepPPT/README_zh.md)

### 2. Adaptive Presentation Creation (APC)（自适应演示文稿创建）

此模块负责将 DeepPPT 生成的 Markdown 内容，渲染成视觉上吸引人且布局合理的 PPT 文件。

📘 **详细指南请参阅：**
👉 [`APC/README_ch.md`](APC/README_ch.md)

---

## 🙏 致谢

我们衷心感谢以下项目和社区对本项目的贡献和支持：

* 本项目的设计和架构受到了字节跳动优秀项目 **[DeerFlow](https://github.com/bytedance/deer-flow)** 的启发，尤其是在多智能体编排、研究规划和 LLM/VLM 集成方面。
* 我们也特别感谢 **[Auto-PPT](https://github.com/limaoyi1/Auto-PPT)** 项目，其创新的设计理念和实现方式为本项目的视觉呈现部分提供了重要参考。

---

## 💬 问题反馈与联系方式

非常欢迎大家提出 [Issues](https://github.com/YourRepo/QueryPPT/issues) 或建议，新手请见谅，我们会不断改进优化！

📮 联系人：

* 彭佳仁：[1354527247@qq.com](mailto:1354527247@qq.com)
* 胡静阳：[191415857@qq.com](mailto:191415857@qq.com)

---

## 🌟 支持我们

如果您喜欢 QueryPPT 项目，欢迎给我们一个 ⭐ Star！您的支持是项目持续发展的最大动力。

> QueryPPT - 让 PPT 制作更智能、更高效！

---
