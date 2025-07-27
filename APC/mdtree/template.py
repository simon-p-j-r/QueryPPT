layer_1 = {'layout_elements':
               [{'element_type': 'main_text',
                 'content_params': {
                     'text_content': '在此填写主题概述文本。建议200字左右的核心内容介绍，包含关键背景信息和核心概念定义。'},
                 'position': {'left': 0.5, 'top': 1.5},
                 'size': {'width': 9.0, 'height': 2.0}},
                {'element_type': 'divider',
                 'content_params': {},
                 'position': {'left': 0.5, 'top': 3.6},
                 'size': {'width': 9.0, 'height': 0.1}},
                {'element_type': 'icon_title_bullets',
                 'content_params':
                     {'icon_emoji': '📜',
                      'content_data':
                          {'title': '分类标题',
                           'bullets': ['要点1：特征/优势/阶段',
                                       '要点2：数据/成就/转折',
                                       '要点3：影响/价值/特色',
                                       '要点4：总结/展望/关联']}},
                 'position': {'left': 0.5, 'top': 3.8},
                 'size': {'width': 9.0, 'height': 2.5},
                 'text_size': {'title_size': 20, 'content_size': 12, 'emoji_size': 22}}]}

layer_1_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。您的目标是分析Markdown，并将其中的相关信息准确地填充到模板指定的各个元素及其内容参数中。

**内容映射与填充规范：**

对于“[当前层级结构模板]”中定义的各个元素，请遵循以下指引进行填充：

1.  **对于 `element_type: 'main_text'` 的元素：**
    * `content_params` 中的 `text_content`: 请从“[输入Markdown内容]”的起始部分或核心段落提取、概括或直接引用一段适合作为主要介绍或开篇的文字。确保内容与Markdown主题紧密相关。

2.  **对于 `element_type: 'divider'` 的元素：**
    * 此元素主要起视觉分隔作用，通常其 `content_params` 为空。请保持模板中对此元素的预设。

3.  **对于 `element_type: 'icon_title_bullets'` 的元素：**
    * `content_params` 中的 `icon_emoji`:
        * 选择一个最能代表该主题的表情符号。
    * `content_params` 中的 `content_data`:
        * `title`: 仔细阅读“[输入Markdown内容]”，提炼或生成一个能够准确概括此部分核心议题的简洁标题。此标题应替换模板中可能存在的旧标题。
        * `bullets` (列表): 根据新的`title`和相关的“[输入Markdown内容]”，提取或总结3至5个关键信息点或论据，作为列表项。这些新的列表项将替换模板中此字段的原始内容。

4.  **对于`text_size`的值：**
    * 根据内容多少来确定字体大小，避免溢出，其中title_size用于控制标题字体大小，content_size用于控制正文内容的字体大小，emoji_size用于控制emoji的大小
    
**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`, `style_id`中的固定值等），均应直接使用“[当前层级结构模板]”中对应元素的预设值。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。
* 不得增加‘layout_elements’中的元素。

请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**：
{layer}/no_think"""

layer_2 = {'layout_elements': [{'element_type': 'quote_box',
                                'content_params': {'quote_text': '',
                                                   'attribution_text': ''}, 'style_id': 'left_accent_bar_quote',
                                'position': {'left': 0.5, 'top': 1.5}, 'size': {'width': 9.0, 'height': 1.5}},
                               {'element_type': 'triple_card', 'content_params': {
                                   'cards_data': [{'title': '', 'content': ""},
                                                  {'title': '', 'content': ""},
                                                  {'title': '', 'content': ""}],
                                   'card_top_emojis': ['🚀', '☁️', '🕊️']}, 'position': {'left': 0.5, 'top': 3.25},
                                'size': {'width': 9.0, 'height': 3.0},
                                'text_size': {'title_size': 20, 'content_size': 12, 'emoji_size': 24}},
                               {'element_type': 'main_text',
                                'content_params': {'text_content': ''},
                                'position': {'left': 0.5, 'top': 6.5}, 'size': {'width': 9.0, 'height': 0.5}}]}

layer_2_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。您的目标是分析Markdown，并将其中的相关信息准确地填充到模板指定的各个元素及其内容参数中，同时特别注意内容长度的控制以避免溢出。

**内容映射与填充规范：**

对于“[当前层级结构模板]”中定义的各个元素，请遵循以下指引进行填充：

1.  **对于 `element_type: 'quote_box'` 的元素：**
    * `content_params` 中的 `quote_text`: 从“[输入Markdown内容]”中提取或凝练一句能够高度概括核心思想、具有启发性或引人深思的引言或论述。
    * `content_params` 中的 `attribution_text`: 为上述引言注明其准确的出处、人物、相关背景或研究领域（例如：“学者观点”、“经典著作《XXX》”等）。
    * 其他如 `style_id`, `position`, `size` 等参数，请直接采用“[当前层级结构模板]”中的预设值。

2.  **对于 `element_type: 'triple_card'` 的元素：**
    * `content_params` 中的 `cards_data` (列表，包含三张卡片信息):
        * 仔细分析“[输入Markdown内容]”，提炼出三个与主题紧密相关且可以独立阐述的方面、例证或子观点。
        * 对于每一张卡片：
            * `title`: 设定一个**<u>高度概括且非常简洁</u>**的标题（例如2-5个字），准确反映该卡片的核心内容。
            * `content`: 撰写一段**<u>极致精炼、字数严格控制的</u>**描述文字。如果涉及引用原文，请确保引用部分简短且切中要点，并辅以必要的浓缩解读。**<u>内容必须非常简短，以适应卡片的有限展示空间，严防溢出</u>**。
    * `content_params` 中的 `card_top_emojis` (列表，包含三个表情符号):
        * 为上述三张卡片各自选择一个能够生动、形象地代表其`title`或核心`content`思想的表情符号。
    * 其他如 `position`, `size` 以及 `text_size` 内的初始值，请优先采用“[当前层级结构模板]”中的预设值。关于`text_size`的动态调整，请参考下方规则4。

3.  **对于末尾的 `element_type: 'main_text'` 的元素 (通常作为总结或结论)：**
    * `content_params` 中的 `text_content`: 根据“[输入Markdown内容]”的整体主旨，撰写一句**<u>极其精炼、高度浓缩的</u>**总结性陈述或核心要点回顾。**<u>注意：此处的文本框高度 (`size.height`) 可能非常有限，因此内容必须极度简洁。</u>**

4.  **对于`text_size`的值（主要针对 `triple_card` 元素中的文本）：**
    * `triple_card` 元素中的 `text_size` 字段（通常包含 `title_size`, `content_size`, `emoji_size`）应首先参考 `[当前层级结构模板]` 中的预设值作为基准。
    * **<u>核心原则</u>：为确保 `triple_card` 中每张卡片的 `title` 和 `content` 能在有限空间内清晰展示、避免溢出，<u>首要策略</u>是确保生成的文本内容（尤其是 `content`，其次是 `title`）做到<u>极致简洁、字数极少</u>。**
    * 如果文本已达到最精炼状态，但根据预估仍可能超出卡片显示范围（特别是对于 `content`），则可以在填充该 `triple_card` 元素的 `text_size` 字段时，在模板预设的 `content_size` 基础上<u>非常谨慎地略微调小1-2pt</u>。但调整字体大小是次要辅助手段，主要依赖于文本本身的精简。
    * 对于其他不包含或不需要动态调整`text_size`的元素，则遵循其在模板中的预设，或不应用此条规则。

**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`, `style_id`中的固定值等），均应直接使用“[当前层级结构模板]”中对应元素的预设值。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。


请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**：
{layer}/no_think"""

layer_3 = {'layout_elements': [
    {'element_type': 'main_text', 'content_params': {
        'text_content': ''},
     'position': {'left': 0.5, 'top': 1.5}, 'size': {'width': 9.0, 'height': 1.8}},
    {'element_type': 'icon_title_bullets', 'content_params': {'icon_emoji': '🌍',
                                                              'content_data': {
                                                                  'title': '',
                                                                  'bullets': [
                                                                      '',
                                                                      '',
                                                                      '']}},
     'position': {'left': 0.5, 'top': 3.5}, 'size': {'width': 8.5, 'height': 2.0},
     'text_size': {'title_size': 20, 'content_size': 14, 'emoji_size': 24}},
    {'element_type': 'divider', 'content_params': {}, 'position': {'left': 0.5, 'top': 5.7},
     'size': {'width': 8.0, 'height': 0.1}},
    {'element_type': 'main_text',
     'content_params': {
         'text_content': ''},
     'position': {'left': 0.5, 'top': 6.0},
     'size': {'width': 9.0, 'height': 1.0}}]}

layer_3_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。你的目标是分析Markdown，并将其信息适配到模板指定的各个元素中。

**内容映射与填充规范：**

对于“[当前层级结构模板]”中定义的各个元素，请遵循以下指引：

1.  **对于第一个 `element_type: 'main_text'` 的元素 (通常作为开篇介绍)：**
    * `text_content`: 从“[输入Markdown内容]”的起始部分提取或概括一段适合作为整体介绍或背景引入的文字。

2.  **对于 `element_type: 'icon_title_bullets'` 的元素：**
    * `icon_emoji`: 根据下方生成的`title`（标题）的核心含义，智能选择一个最能代表该主题的表情符号。
    * `content_data`:
        * `title`: 仔细分析“[输入Markdown内容]”中与此列表相关的内容，提炼或设定一个简洁且能概括列表核心议题的标题。
        * `bullets` (列表): 根据上述标题和相关Markdown内容，提取或生成3-5个清晰、简洁的关键要点。

3.  **对于 `element_type: 'divider'` 的元素：**
    * 此元素通常无需从Markdown填充特定内容，保持其`content_params`为空或按模板预设即可。

4.  **对于第二个 `element_type: 'main_text'` 的元素 (通常作为补充说明或总结)：**
    * `text_content`: 结合前面的内容（尤其是列表要点），从“[输入Markdown内容]”中提取或撰写一段补充说明、深化理解或总结性的文字。

5.  **对于`text_size`的值（针对所有包含此字段的元素）：**
    * 根据内容多少来确定字体大小，避免溢出，其中title_size用于控制标题字体大小，content_size用于控制正文内容的字体大小，emoji_size用于控制emoji的大小
    
**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`, `style_id`中的固定值等），均应直接使用“[当前层级结构模板]”中对应元素的预设值。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。

请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**：
{layer}/no_think"""

layer_4 = {
    'layout_elements': [
        {
            'element_type': 'main_text',
            'content_params': {
                'text_content': ''
                # 示例内容，AI会根据新Markdown替换
            },
            'position': {'left': 0.5, 'top': 1.5},
            'size': {'width': 9.0, 'height': 0.8}  # 高度调整为 0.8
        },
        {
            'element_type': 'parallel_boxes',
            'content_params': {
                'title_text': '[]',  # 示例占位，原键名不变
                'content_text': '[]',  # 示例占位，原键名不变
                'emoji_left': '🌌',
                'emoji_right': '📜'
            },
            'position': {'left': 0.5, 'top': 2.3},  # top调整为 2.3
            'size': {'width': 9.0, 'height': 3.0},  # height调整为 3.0
            'text_size': {'content_size': 14, 'emoji_size': 20}  # content_size将同时应用于左右两侧文本
        },
        {
            'element_type': 'divider',
            'content_params': {},
            'position': {'left': 0.5, 'top': 5.5},  # top调整为 5.5
            'size': {'width': 9.0, 'height': 0.1}
        },
        {
            'element_type': 'main_text',
            'content_params': {
                'text_content': ''  # 示例内容，AI会根据新Markdown替换
            },
            'position': {'left': 0.5, 'top': 5.7},  # top调整为 5.7
            'size': {'width': 9.0, 'height': 0.8}
        }
    ]
}

layer_4_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。您的目标是分析Markdown，并将其信息准确地填充到模板指定的各个元素及其内容参数中，特别注意 `parallel_boxes` 组件内部左右两侧内容的均衡与简洁。

**内容映射与填充规范：**

对于“[当前层级结构模板]”中定义的各个元素，请遵循以下指引进行填充：

1.  **对于第一个 `element_type: 'main_text'` 的元素 (开篇介绍)：**
    * `content_params` 中的 `text_content`: 从“[输入Markdown内容]”的起始部分或核心段落提取、概括或直接引用一段适合作为主要介绍或开篇的文字。

2.  **对于 `element_type: 'parallel_boxes'` 的元素：**
    * **<u>重要映射规则</u>：在此组件的 `content_params` 中，`title_text` 字段将用于填充其<u>左侧区域</u>的显示文本，而 `content_text` 字段将用于填充其<u>右侧区域</u>的显示文本。**
    * `title_text` (将作为**左侧内容**): 根据“[输入Markdown内容]”，针对核心议题的一个方面、撰写一段文本，作为此并行框的左侧显示内容。
    * `content_text` (将作为**右侧内容**): 根据“[输入Markdown内容]”，针对核心议题的另一个方面、（可与左侧内容形成对比、互补或延续关系），撰写一段文本，作为此并行框的右侧显示内容。
    * `emoji_left` 和 `emoji_right`: 根据最终为左右两侧确定的文本内容，各自智能选择一个相关的、能够视觉化辅助表达主题的表情符号。

3.  **对于 `element_type: 'divider'` 的元素：**
    * 此元素主要起视觉分隔作用，通常其 `content_params` 为空。请保持模板中对此元素的预设。

4.  **对于末尾的 `element_type: 'main_text'` 的元素 (通常作为总结或结论)：**
    * `content_params` 中的 `text_content`: 根据“[输入Markdown内容]”的整体主旨及前面 `parallel_boxes` 可能讨论的内容，撰写一段总结性陈述或核心要点回顾。**<u>注意此文本框高度有限。</u>**

5.  **对于`text_size`字段的智能处理（针对所有包含此字段的元素）：**
    * 模板中各元素（如 `parallel_boxes`）若包含 `text_size` 字段，其预设值（如 `content_size`, `emoji_size`）应作为首选基准和重要参考。
    * **针对 `parallel_boxes` 元素：其 `title_text` (作为左侧内容) 和 `content_text` (作为右侧内容) 内容量力求均衡。如果这两部分文本根据预估仍可能超出元素的显示范围，则可以在填充该元素的 `text_size` 字段时，在模板预设的 `content_size` 基础上<u>非常谨慎地略微调小1-2pt</u>。**
    * 其他不包含 `text_size` 字段或无需动态调整的元素，则遵循其在模板中的预设。

**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`, `style_id`中的固定值等），均应直接使用“[当前层级结构模板]”中对应元素的预设值。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。

**输入Markdown内容:**

请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**：
{layer}/no_think"""

layer_5 = {'layout_elements': [
    {
        'element_type': 'main_text',
        'content_params': {
            'text_content': ''
        },
        'position': {'left': 0.5, 'top': 1.5},
        'size': {'width': 9.0, 'height': 1.2}  # 高度从 1.5 修改为 1.2
    },
    {
        'element_type': 'quote_box',
        'content_params': {
            'quote_text': '',
            'attribution_text': ''
        },
        'style_id': 'left_accent_bar_quote',
        'position': {'left': 0.5, 'top': 2.95},  # 从 3.25 修改为 2.95
        'size': {'width': 9.0, 'height': 1.2},
        'text_size': {'title_size': 18, 'content_size': 14, 'emoji_size': 20}
    },
    {
        'element_type': 'parallel_boxes',
        'content_params': {
            'title_text': '',
            'content_text': '',
            'emoji_left': '⚔️',
            'emoji_right': '🌙'
        },
        'position': {'left': 0.5, 'top': 4.25},  # 从 4.65 修改为 4.25
        'size': {'width': 4.25, 'height': 1.7},
        'text_size': {'content_size': 12, 'emoji_size': 20}
    },
    {
        'element_type': 'parallel_boxes',
        'content_params': {
            'title_text': '',
            'content_text': '',
            'emoji_left': '🌌',
            'emoji_right': '📜'
        },
        'position': {'left': 5.25, 'top': 4.25},  # 从 4.65 修改为 4.25
        'size': {'width': 4.25, 'height': 1.7},
        'text_size': {'content_size': 12, 'emoji_size': 20}
    },
    {
        'element_type': 'main_text',
        'content_params': {
            'text_content': ''
        },
        'position': {'left': 0.5, 'top': 6.10},  # 从 6.5 修改为 6.10
        'size': {'width': 9.0, 'height': 0.8}
    }
]}

layer_5_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。你的目标是分析Markdown，并将其信息适配到模板指定的各个元素中。

**内容映射与填充规范：**

对于“[当前层级结构模板]”中定义的各个元素，请遵循以下指引：

1.  **对于第一个 `element_type: 'main_text'` 的元素 (开篇概述)：**
    * `text_content`: 从“[输入Markdown内容]”提取或撰写一段对主题进行总体介绍或背景铺垫的文字。

2.  **对于 `element_type: 'quote_box'` 的元素：**
    * `quote_text`: 从“[输入Markdown内容]”中选取或总结一至两句最能体现核心观点或引人注目的引言/数据。
    * `attribution_text`: 明确引言的出处或相关背景。

3.  **对于第一个 `element_type: 'parallel_boxes'` 的元素 (左侧并行框)：**
    * `title_text`: 针对“[输入Markdown内容]”中的一个特定方面或子主题，设定一个**<u>极其简洁</u>**的标题。
    * `content_text`: 围绕该标题，从Markdown中提取或撰写一段**<u>高度凝练、字数严格控制的</u>**方面、观点或论据，**以确保文本能在有限的框体内完全显示，避免溢出**。
    * `emoji_left` 和 `emoji_right`: 智能选择与此框内容相关的表情符号。

4.  **对于第二个 `element_type: 'parallel_boxes'` 的元素 (右侧并行框)：**
    * `title_text`: 针对“[输入Markdown内容]”中的另一个特定方面或子主题（应与左侧框内容有所区分），设定一个**<u>极其简洁</u>**的标题。
    * `content_text`: 围绕该标题，从Markdown中提取或撰写一段**<u>高度凝练、字数严格控制的</u>**方面、观点或论据，**以确保文本能在有限的框体内完全显示，避免溢出**。
    * `emoji_left` 和 `emoji_right`: 智能选择与此框内容相关的表情符号。

5.  **对于末尾的 `element_type: 'main_text'` 的元素 (总结或扩展)：**
    * `text_content`: 综合前文，从“[输入Markdown内容]”中提取或撰写一段总结性评论、影响分析或对未来的展望。

6.  **对于`text_size`的值（针对所有包含此字段的元素）：**
    * `title_size`用于控制标题字体大小，`content_size`用于控制正文内容的字体大小，`emoji_size`用于控制emoji的大小。
    * **<u>特别强调</u>：对于 `parallel_boxes` 类型的元素，鉴于其显示空间通常较为狭小，解决内容可能溢出的<u>首要策略</u>是确保其 `title_text` 和 `content_text` 做到<u>极致简洁、字数极少</u>。如果文本内容已压缩至最精炼状态，但根据预估仍可能超出显示范围，则应在填充该元素的 `text_size` 字段时，<u>适当调小 `content_size` 的值</u>（可以在模板预设值基础上进一步减小，例如减小1-2pt）。**
    
**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`, `style_id`中的固定值，以及多数情况下`text_size`中的初始参考值等），均应直接使用“[当前层级结构模板]”中对应元素的预设值。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。

请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**
{layer}"""

layer_6 = {'layout_elements': [
    {  # 第一个组件 (main_text) 保持不变
        'element_type': 'main_text',
        'content_params': {
            'text_content': ''
        },
        'position': {'left': 0.5, 'top': 1.5},  # 保持不变
        'size': {'width': 9.0, 'height': 1.5}  # 保持不变
    },
    {  # 第二个组件 (parallel_boxes)
        'element_type': 'parallel_boxes',
        'content_params': {
            'title_text': '',
            'content_text': "",
            'emoji_left': '📚',
            'emoji_right': '🍷'
        },
        'position': {'left': 0.5, 'top': 3.25 - 0.7},
        'size': {'width': 4.5, 'height': 2.0},
        'text_size': {'content_size': 14, 'emoji_size': 20}
    },
    {  # 第三个组件 (parallel_boxes)
        'element_type': 'parallel_boxes',
        'content_params': {
            'title_text': '',
            'content_text': "",
            'emoji_left': '🎭',
            'emoji_right': '🏇'
        },
        'position': {'left': 5.0, 'top': 3.25 - 0.7},
        'size': {'width': 4.5, 'height': 2.0},
        'text_size': {'content_size': 14, 'emoji_size': 20}
    },
    {  # 第四个组件 (divider)
        'element_type': 'divider',
        'content_params': {},
        'position': {'left': 0.5, 'top': 5.5 - 0.7},
        'size': {'width': 9.0, 'height': 0.1},
        'style_id': 'dots_accent_line'
    },
    {  # 第五个组件 (icon_title_bullets)
        'element_type': 'icon_title_bullets',
        'content_params': {
            'icon_emoji': '🌌',
            'content_data': {
                'title': '',
                'bullets': ['',
                            '',
                            '']
            }
        },
        'position': {'left': 0.5, 'top': 5.8 - 0.7},
        'size': {'width': 9.0, 'height': 2.0},
        'text_size': {'title_size': 18, 'content_size': 14, 'emoji_size': 24}
    }
]}

layer_6_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。你的目标是分析Markdown，并将其信息适配到模板指定的各个元素中。

**内容映射与填充规范：**

对于“[当前层级结构模板]”中定义的各个元素，请遵循以下指引：

1.  **对于第一个 `element_type: 'main_text'` 的元素 (主题引入)：**
    * `text_content`: 从“[输入Markdown内容]”提取或撰写一段引出核心讨论主题的介绍性文字。

2.  **对于第一个 `element_type: 'parallel_boxes'` 的元素 (左侧并行框)：**
    * `title_text`: 依据“[输入Markdown内容]”，为此框内容（通常是主题的第一个方面或案例）设定一个明确的标题。
    * `content_text`: 围绕该标题，从Markdown中提取或撰写具体阐述。
    * `emoji_left` 和 `emoji_right`: 智能选择与此框内容贴合的表情符号。

3.  **对于第二个 `element_type: 'parallel_boxes'` 的元素 (右侧并行框)：**
    * `title_text`: 依据“[输入Markdown内容]”，为此框内容（主题的第二个方面或案例，与左侧有所区别）设定一个明确的标题。
    * `content_text`: 围绕该标题，从Markdown中提取或撰写具体阐述。
    * `emoji_left` 和 `emoji_right`: 智能选择与此框内容贴合的表情符号。

4.  **对于 `element_type: 'divider'` 的元素：**
    * 此元素通常无需从Markdown填充特定内容，`style_id`（如有）应按模板预设。

5.  **对于 `element_type: 'icon_title_bullets'` 的元素 (总结与升华)：**
    * `icon_emoji`: 根据下方生成的`title`的核心思想，智能匹配一个表情符号。
    * `content_data`:
        * `title`: 从“[输入Markdown内容]”中提炼或构思一个具有总结性或哲学思辨意味的标题。
        * `bullets` (列表): 根据该标题和Markdown内容，列出3个核心观点、启示或相关的延伸性思考。

6.  **对于`text_size`的值（针对所有包含此字段的元素）：**
    * 根据内容多少来确定字体大小，避免溢出，其中title_size用于控制标题字体大小，content_size用于控制正文内容的字体大小，emoji_size用于控制emoji的大小
    
**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`, `style_id`中的固定值等），均应直接使用“[当前层级结构模板]”中对应元素的预设值。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。

请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**：
{layer}"""

layer_7 = {'layout_elements': [{'element_type': 'quote_box',
                                'content_params': {'quote_text': '',
                                                   'attribution_text': ''},
                                'style_id': 'left_accent_bar_quote', 'position': {'left': 0.5, 'top': 1.5},
                                'size': {'width': 8.0, 'height': 1.8},
                                'text_size': {'quote_size': 20, 'attribution_size': 14}},
                               {'element_type': 'icon_title_bullets', 'content_params': {'icon_emoji': '🍶',
                                                                                         'content_data': {
                                                                                             'title': '',
                                                                                             'bullets': [
                                                                                                 '',
                                                                                                 '',
                                                                                                 '']}},
                                'position': {'left': 0.5, 'top': 3.5}, 'size': {'width': 8.0, 'height': 3.0},
                                'text_size': {'title_size': 22, 'content_size': 14, 'emoji_size': 24}},
                               {'element_type': 'main_text', 'content_params': {
                                   'text_content': ''},
                                'position': {'left': 0.5, 'top': 6.7}, 'size': {'width': 8.0, 'height': 0.8}}]}

layer_7_prompt = """请根据下方提供的“[输入Markdown内容]”和“[当前层级结构模板]”，智能地完成内容填充任务。您的目标是分析Markdown，并将其中的相关信息准确地填充到模板指定的各个元素及其内容参数中，同时特别注意内容长度的控制以避免溢出。

**内容映射与填充规范：**

对于“[当前层级结构模板]”中定义的各个元素，请遵循以下指引进行填充：

1.  **对于 `element_type: 'quote_box'` 的元素：**
    * `content_params` 中的 `quote_text`: 从“[输入Markdown内容]”中提取一段最具代表性、能够引人深思或概括核心观点的引文（例如诗句、名言等）。
    * `content_params` 中的 `attribution_text`: 明确注明上述引文的出处（例如作者、作品名称等）。

2.  **对于 `element_type: 'icon_title_bullets'` 的元素：**
    * `content_params` 中的 `icon_emoji`:
        * 如果“[当前层级结构模板]”中已为此字段预设了表情符号，并且该符号与从Markdown中提炼出的新`title`内容相符，则可沿用。
        * 否则，或如果模板中未预设，请根据新`title`的核心含义，智能选择一个最能代表该主题的表情符号。
    * `content_params` 中的 `content_data`:
        * `title`: 仔细阅读“[输入Markdown内容]”，提炼或生成一个能够准确概括此列表核心议题的简洁标题。
        * `bullets` (列表): 根据新的`title`和相关的“[输入Markdown内容]”，提取或总结3-4个关键信息点、分析维度或例证。**<u>每个列表项的文本都应力求简洁明了，如果包含引文或案例，也应高度概括，避免单个列表项内容过长导致显示问题。</u>**

3.  **对于末尾的 `element_type: 'main_text'` 的元素 (通常作为总结或结论)：**
    * `content_params` 中的 `text_content`: 根据“[输入Markdown内容]”的整体主旨以及前面元素（如图标列表）所讨论的内容，撰写一句**<u>高度凝练、字数严格控制的</u>**总结性陈述或核心观点回顾。**<u>注意：此处的文本框高度 (`size.height`) 可能非常有限（如模板所示为0.8），因此内容必须极度简洁。</u>**

4.  **对于`text_size`字段的智能处理（针对所有包含此字段的元素）：**
    * 模板中各元素（如 `quote_box`, `icon_title_bullets` 等）若包含 `text_size` 字段，其预设值（如 `quote_size`, `attribution_size`, `title_size`, `content_size`, `emoji_size`）应作为首选基准和重要参考。
    * 特别是对于 `icon_title_bullets` 中的 `bullets`（列表项），以及空间有限的 `main_text`，每个单位文本的长度都需要严格控制，使其在预设的相应字号下能够清晰、完整地展示。
    * 如果在文本预估可能超出元素的显示范围，则可以在填充对应元素的 `text_size` 字段时，在模板预设的相应字号（如 `content_size` 或 `quote_size`）基础上<u>非常谨慎地略微调小1-2pt</u>。字体大小调整是次要的辅助手段，文本自身的简洁性是主要依赖和首先要保证的。
    * 其他不包含 `text_size` 字段或无需动态调整的元素，则遵循其在模板中的预设，或不应用此条规则。

**通用指令：**
* 所有未明确要求从Markdown提取或生成的参数（如`position`, `size`, `style_id`中的固定值等），均应直接使用“[当前层级结构模板]”中对应元素的预设值。
* 在提取或生成文本内容时，力求忠实于“[输入Markdown内容]”的原意，同时确保表达流畅、简洁。

请按此框架处理下方Markdown内容，直接输出完整JSON，无需解释：
**[输入Markdown内容]:**
'''
{markdown}
'''

**[当前层级结构模板]:**：
{layer}/no_think"""

template_1 = [layer_1, layer_2, layer_3, layer_4, layer_5, layer_6, layer_7]
template_1_prompt = [layer_1_prompt, layer_2_prompt, layer_3_prompt, layer_4_prompt, layer_5_prompt, layer_6_prompt,
                     layer_7_prompt]
