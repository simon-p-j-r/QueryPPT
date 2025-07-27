# DeepPPT

DeepPPT是QueryPPT的核心子模块，专注于PPT内容收集与章节设计功能，为用户提供智能化的演示文稿内容生成服务。

## 功能特性

- 🎯 **智能内容收集**：基于用户查询自动收集相关信息和素材
- 📋 **章节设计**：智能规划PPT结构，生成合理的章节布局
- 🤖 **AI驱动**：集成先进的LLM和VLM模型，提供高质量内容生成
- 📊 **结构化输出**：生成标准化的Markdown格式内容

## 快速开始

### 环境准备

1. **克隆项目**
```bash
git clone <repository-url>
cd DeepPPT
```

2. **安装依赖**
```bash
pip install -r requirements.txt
# 安装playwright浏览器驱动
playwright install
```

### 配置设置

#### 1. 模型配置
在 `core/config/LLMConfig.py` 文件中配置您的AI模型参数：


```bash
cd core/config
cp LLMConfig_copy.py LLMConfig.py
```

```python
VLMConfig = {
    "model": "your-vlm-model-name",      # 视觉语言模型名称
    "api_key": "your-vlm-api-key",       # VLM API密钥
    "base_url": "your-vlm-base-url",     # VLM服务地址
}

LLMConfig = {
    "model": "your-llm-model-name",      # 大语言模型名称
    "api_key": "your-llm-api-key",       # LLM API密钥
    "base_url": "your-llm-base-url",     # LLM服务地址
}
```

#### 2. 创建必要目录
```bash
cd core
mkdir output    # 输出结果目录
mkdir log       # 日志文件目录
```

### 运行使用

#### 基本用法
```bash
cd ..
python main.py --query "您的查询内容"
```

#### 示例
```bash
python main.py --query "人工智能在医疗领域的应用"
```

### 输出结果

运行完成后，您可以在以下位置查看结果：

- **内容输出**：`core/output/` 目录下会生成以查询内容命名的Markdown文件
- **运行日志**：`core/log/` 目录下会创建对应的日志文件夹，记录详细的执行过程

## 项目结构

```
DeepPPT/
├── core/                    # 核心功能模块
│   ├── config/             # 配置文件
│   ├── data/               # 数据文件
│   ├── output/             # 输出结果
│   ├── log/                # 日志文件
│   ├── prompts/            # 提示词模板
│   ├── src/                # 源代码
│   └── tools/              # 工具模块
├── testset/                # 测试数据集
├── requirements.txt        # 依赖包列表
└── run.py                  # 主运行脚本
```

## 注意事项

- 请确保您已正确配置API密钥和服务地址
- 首次运行前请检查网络连接状态
- 建议在虚拟环境中运行以避免依赖冲突

## 技术支持

如遇到问题，请检查：
1. 配置文件中的API密钥是否正确
2. 网络连接是否正常
3. 依赖包是否完整安装

## 致谢

DeepPPT的设计和架构受到了字节跳动优秀项目 [DeerFlow](https://github.com/bytedance/deer-flow) 的启发。DeerFlow是一个社区驱动的深度研究框架，结合了语言模型与网络搜索、爬虫和Python执行等工具。我们从他们在AI驱动研究工作流方面的创新方法中获得了灵感。

### 设计灵感来源：
- 多智能体编排和工作流设计模式
- 研究规划和执行方法论
- LLM和VLM模型的集成方法
- 结构化输出生成技术

我们感谢DeerFlow团队对开源社区的贡献以及在AI驱动研究框架领域的开创性工作。

---

**DeepPPT** - 让PPT制作更智能、更高效！