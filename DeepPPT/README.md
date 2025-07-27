# DeepPPT

DeepPPT is the core submodule of QueryPPT, focusing on PPT content collection and chapter design functionality, providing users with intelligent presentation content generation services.

## Features

- 🎯 **Intelligent Content Collection**: Automatically collect relevant information and materials based on user queries
- 📋 **Chapter Design**: Intelligently plan PPT structure and generate reasonable chapter layouts
- 🤖 **AI-Powered**: Integrates advanced LLM and VLM models for high-quality content generation
- 📊 **Structured Output**: Generates standardized Markdown format content

## Quick Start

### Environment Setup

1. **Clone the Repository**
```bash
git clone <repository-url>
cd DeepPPT
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
# install playwright for browser automation
playwright install
```

### Configuration

#### 1. Model Configuration
Configure your AI model parameters in the `core/config/LLMConfig.py` file:

```bash
cd core/config
cp LLMConfig_copy.py LLMConfig.py
```

```python
VLMConfig = {
    "model": "your-vlm-model-name",      # Vision Language Model name
    "api_key": "your-vlm-api-key",       # VLM API key
    "base_url": "your-vlm-base-url",     # VLM service URL
}

LLMConfig = {
    "model": "your-llm-model-name",      # Large Language Model name
    "api_key": "your-llm-api-key",       # LLM API key
    "base_url": "your-llm-base-url",     # LLM service URL
}
```

#### 2. Create Required Directories
```bash
cd core
mkdir output    # Output results directory
mkdir log       # Log files directory
```

### Usage

#### Basic Usage
```bash
cd ..
python main.py --query "your query content"
```

#### Example
```bash
python main.py --query "Applications of Artificial Intelligence in Healthcare"
```

### Output Results

After running, you can view the results in the following locations:

- **Content Output**: Markdown files named after your query will be generated in the `core/output/` directory
- **Execution Logs**: Corresponding log folders will be created in the `core/log/` directory, recording detailed execution processes

## Project Structure

```
DeepPPT/
├── core/                    # Core functionality modules
│   ├── config/             # Configuration files
│   ├── data/               # Data files
│   ├── output/             # Output results
│   ├── log/                # Log files
│   ├── prompts/            # Prompt templates
│   ├── src/                # Source code
│   └── tools/              # Tool modules
├── testset/                # Test datasets
├── requirements.txt        # Dependency package list
└── run.py                  # Main execution script
```

## Important Notes

- Please ensure you have correctly configured API keys and service URLs
- Check network connectivity before first run
- It's recommended to run in a virtual environment to avoid dependency conflicts

## Technical Support

If you encounter issues, please check:
1. Whether the API keys in the configuration file are correct
2. Whether the network connection is normal
3. Whether all dependency packages are completely installed

## Acknowledgments

DeepPPT's design and architecture are inspired by the excellent work of the [DeerFlow](https://github.com/bytedance/deer-flow) project by ByteDance. DeerFlow is a community-driven Deep Research framework that combines language models with tools like web search, crawling, and Python execution. We have learned from their innovative approaches in AI-powered research workflows.

### Design Inspiration from DeerFlow:
- Multi-agent orchestration and workflow design patterns
- Research planning and execution methodologies
- Integration approaches for LLM and VLM models
- Structured output generation techniques

We appreciate the DeerFlow team's contribution to the open-source community and their pioneering work in the field of AI-powered research frameworks.

---

**DeepPPT** - Making PPT creation smarter and more efficient!

