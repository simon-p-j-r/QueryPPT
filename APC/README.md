# Adaptive Presentation Creation (APC)

**APC** is the second stage of the QueryPPT framework, responsible for intelligently rendering structured Markdown content into visually appealing and well-laid-out presentations (PPTs). It drives visual design with content, achieving automated, high-quality slide generation through intelligent color schemes, component layout, and multimodal integration.

-----

## ✨ Features

  * 🎨 **Intelligent Visual Design**
    Dynamically generates background images for title and content slides based on the content's theme, enhancing overall aesthetics and stylistic consistency.

  * 🌈 **Automatic Color Scheme**
    Intelligently deduces the optimal font color and theme palette from the background image to ensure readability and beauty.

  * 🧱 **Flexible Layout Engine**

      * **Component-based Layout (Architect Agent)**: Dynamically selects and assembles visual components to adapt to different types of content.
      * **Predefined Template Adaptation (Mapper Agent)**: Efficiently populates content into professionally designed slide templates.

  * 😊 **Multimodal Fusion**
    Seamlessly integrates text, images, and emojis to enhance the expressiveness and visual impact of the slides.

  * 🧩 **Design Asset Library Support**

      * **Component Library**: Provides a collection of basic, stylized, and composite components.
      * **Layout Library**: Covers common layout needs such as full-page, half-page, and table of contents.

-----

## 🚀 Quick Start

### 1️⃣ Environment Setup

It is recommended to install the dependencies in a new Python virtual environment:

```bash
pip install -r requirements.txt
```

### 2️⃣ Prepare Input

Please ensure you have completed the first stage of QueryPPT (DeepPPT) and have the structured Markdown content.

### 3️⃣ Modify Configuration

Adjust paths, styles, or mode parameters in `../config_parser.py` as needed.

-----

## ⚙️ Custom Configuration Guide

  * 📁 **Custom Backgrounds**
    Place your custom background images in the `pptx_static/static/bg_new/` directory, and the system will automatically select them.

  * 🖼️ **Recommended Background Generation**
    You can use image generation tools like [OpenAI's](https://chat.openai.com/) to obtain high-quality images and enhance the visual effect of your slides.

-----

## 📘 Example Usage

We provide a complete example script to help you quickly experience the entire process from Markdown to PPT:

```bash
python sample_test.py
```

Running this script will automatically read the sample Markdown, complete background generation, content layout, and output the final presentation.

-----

## 🙏 Acknowledgments

We would like to extend our special thanks to the following open-source projects and communities for their inspiration and support:

  * [**Auto-PPT**](https://github.com/limaoyi1/Auto-PPT): Its innovative visual presentation methods and engineering structure provided significant reference for this module.

-----

For further assistance, feel free to submit an issue or contact the project maintainers. If you like this project, please give us a ⭐ Star—your support is our greatest motivation for continuous improvement\!