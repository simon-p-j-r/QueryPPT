layer_1_half = {
  "layout_elements": [
      {
          "element_type": "main_text",
          "content_params": {
              "text_content": "可选的总体介绍性标题或文本，位于双框组件上方。"
          },
          "position": {"left": 0.5, "top": 2.5},
          "size": {"width": 4.0, "height": 0.7},
      },
      {
          "element_type": "parallel_boxes",
          "content_params": {
              "title_text": "左侧框标题/内容 - 从Markdown提取",
              "content_text": "右侧框内容 - 从Markdown提取",
              "emoji_left": "🧩",
              "emoji_right": "💡"
          },
          "position": {"left": 0.5, "top": 3.4},
          "size": {"width": 4.0, "height": 2.5},
          "text_size": {
              "content_size": 11,
              "emoji_size": 22
          }
      },
      {
          "element_type": "main_text",
          "content_params": {
              "text_content": "可选的总结性文本，位于双框组件下方。"
          },
          "position": {"left": 0.5, "top": 6.1},
          "size": {"width": 4.0, "height": 1.0},
      }
  ]
}

layer_1_half_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。您的目标是分析Markdown，并将其中的相关信息准确地填充到模板指定的各个元素及其内容参数中。

**重要约束：**
* 所有内容将放置在幻灯片的左侧区域，因为幻灯片右侧已预留给图片。

**内容映射与填充规范：**

1.  **对于第一个 `element_type: 'main_text'` 的元素 (通常作为开篇介绍)：**
    * `text_content`: 从“[输入Markdown内容]”的起始部分提取或概括一段适合作为整体介绍或背景引入的文字。

2.  **对于 `element_type: 'parallel_boxes'` 的元素：**
    * **<u>重要映射规则</u>：在此组件的 `content_params` 中，`title_text` 字段将用于填充其<u>左侧区域</u>的显示文本，而 `content_text` 字段将用于填充其<u>右侧区域</u>的显示文本。**
    * `title_text` (将作为**左侧内容**): 根据“[输入Markdown内容]”，针对核心议题的一个方面、观点或论据，撰写一段**<u>高度凝练</u>**的文本，作为此并行框的左侧显示内容。
    * `content_text` (将作为**右侧内容**): 根据“[输入Markdown内容]”，针对核心议题的另一个方面、观点或论据（可与左侧内容形成对比、互补或延续关系），撰写一段**<u>同样高度凝练</u>**的文本，作为此并行框的右侧显示内容。
    * `emoji_left` 和 `emoji_right`: 根据最终为左右两侧确定的文本内容，各自智能选择一个相关的、能够视觉化辅助表达主题的表情符号。

3.  **对于第二个 `element_type: 'main_text'` 的元素 (通常作为补充说明或总结)：**
    * `text_content`: 结合前面的内容，从“[输入Markdown内容]”中提取或撰写一段补充说明、深化理解或总结性的文字。
    
4.  **对于`text_size`的值（针对所有包含此字段的元素）：**
    * 根据内容多少来确定字体大小，避免溢出，其中title_size用于控制标题字体大小，content_size用于控制正文内容的字体大小，emoji_size用于控制emoji的大小

**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`中的预设值, `theme_colors`等），均应直接使用“[当前层级结构模板]”中对应元素的预设值，除非另有说明。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。

请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**：
{layer}"""

layer_2_half = {
  "layout_elements": [
            {
                "element_type": "data_callout",
                "content_params": {
                    "statistic_value": "数据1",
                    "label_text": "标签1 - 从Markdown提取",
                    "style_id": "default_data"
                },
                "position": {"left": 0.5, "top": 2.0},
                "size": {"width": 1.8, "height": 1.2},
                "text_size": {
                    "title_size": 18,
                    "content_size": 10
                }
            },
            {
                "element_type": "data_callout",
                "content_params": {
                    "statistic_value": "数据2",
                    "label_text": "标签2 - 从Markdown提取",
                    "style_id": "circle_emphasis_data"
                },
                "position": {"left": 2.7, "top": 2.0},
                "size": {"width": 1.8, "height": 1.2},
                "text_size": {
                    "title_size": 18,
                    "content_size": 10
                }
            },
            {
                "element_type": "icon_title_bullets",
                "content_params": {
                    "icon_emoji": "📊",
                    "content_data": {
                        "title": "核心要点分析",
                        "bullets": [
                            "要点A: 根据Markdown内容生成",
                            "要点B: 适应左侧布局",
                            "要点C: 突出关键信息"
                        ]
                    },
                },
                "position": {"left": 0.5, "top": 3.5},
                "size": {"width": 4.0, "height": 3.5},
                "text_size": {
                    "title_size": 18,
                    "content_size": 12,
                    "emoji_size": 48
                }
            }
        ]
}


layer_2_half_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。您的目标是分析Markdown，并将其中的相关信息准确地填充到模板指定的各个元素及其内容参数中。

**重要约束：**
* 所有内容将放置在幻灯片的左侧区域，因为幻灯片右侧已预留给图片。

**内容映射与填充规范：**
    
1.  **对于两个 `element_type: 'data_callout'` 的元素：**
    * `content_params` 中的 `statistic_value`: 从“[输入Markdown内容]”中提取一个关键数据、百分比或简短指标。
    * `content_params` 中的 `label_text`: 为上述数据提供一个简洁的描述性标签。
    * `content_params` 中的 `style_id`: 选择数据标注框样式，例如 `"default_data"`（圆角矩形） 或 `"circle_emphasis_data"`（椭圆）。

2.  **对于 `element_type: 'icon_title_bullets'` 的元素：**
    * `content_params` 中的 `icon_emoji`: 根据下方 `content_data.title` 的核心含义，智能选择一个最能代表该主题的表情符号。
    * `content_params` 中的 `content_data`:
        * `title`: 仔细阅读“[输入Markdown内容]”，提炼或生成一个能够准确概括此部分核心议题的简洁标题。
        * `bullets` (列表): 根据新的`title`和相关的“[输入Markdown内容]”，提取或总结3至5个关键信息点或论据，作为列表项。

5.  **对于`text_size`的值（针对所有包含此字段的元素）：**
    * 根据内容多少来确定字体大小，避免溢出，其中title_size用于控制标题字体大小，content_size用于控制正文内容的字体大小，emoji_size用于控制emoji的大小，请注意'data_callout'需要较小的字体
    
**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`, `style_id`中的固定值等），均应直接使用“[当前层级结构模板]”中对应元素的预设值。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。

请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**：
{layer}
"""

layer_3_half = {
  "layout_elements": [
            {
                "element_type": "main_text",
                "content_params": {
                    "text_content": "在此处填写主要的介绍性文本或段落。这段文字将放置在幻灯片的左侧，为右侧的图片提供上下文信息。"
                },
                "position": {"left": 0.5, "top": 2.0},
                "size": {"width": 4.0, "height": 2.0},
            },
            {
                "element_type": "divider",
                "content_params": {},
                "position": {"left": 0.5, "top": 4.2},
                "size": {"width": 4.0},
                "style_id": "default_line"
            },
            {
                "element_type": "quote_box",
                "content_params": {
                    "quote_text": "将从Markdown中提取或生成的引用文本放在这里。",
                    "attribution_text": "引用来源或作者"
                },
                "position": {"left": 0.5, "top": 4.5},
                "size": {"width": 4.0},
                "style_id": "left_accent_bar_quote"
            }
        ]
}

layer_3_half_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。您的目标是分析Markdown，并将其中的相关信息准确地填充到模板指定的各个元素及其内容参数中。

**重要约束：**
* 所有内容将放置在幻灯片的左侧区域，因为幻灯片右侧已预留给图片。

**内容映射与填充规范：**

1.  **对于 `element_type: 'main_text'` 的元素：**
    * `content_params` 中的 `text_content`: 从“[输入Markdown内容]”中提取或概括一段适合作为主要介绍或说明的文字。

2.  **对于 `element_type: 'divider'` 的元素：**
    * `style_id` (顶层键): 选择一个分隔线样式，例如 `"default_line"`（默认线条样式）或 `"dots_accent_line"`（带点的强调线条样式）。
    * `content_params` (通常为空): 此元素主要起视觉分隔作用。

3.  **对于 `element_type: 'quote_box'` 的元素：**
    * `content_params` 中的 `quote_text`: 从“[输入Markdown内容]”中提取或生成一句有代表性的引言。
    * `content_params` 中的 `attribution_text` (可选): 提供引言的作者或来源。
    * `style_id` (顶层键): 选择引用框样式，例如 `"default_quote"` （默认引用框样式）或 `"left_accent_bar_quote"`（左侧强调条引用框样式）。

**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`, `style_id`中的固定值等），均应直接使用“[当前层级结构模板]”中对应元素的预设值。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。

请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**：
{layer}
"""
template_half = [layer_1_half, layer_2_half, layer_3_half]
template_half_prompt = [layer_1_half_prompt, layer_2_half_prompt, layer_3_half_prompt]
