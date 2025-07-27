import json
from openai import OpenAI

from APC.config_parser import get_args_parser
import time

PROMPT_1_CONTENT_ANALYSIS_AND_COMPONENT_SELECTION = """请扮演一位经验丰富的演示文稿设计师和信息架构师。
您的首要任务是分析提供的Markdown原始内容，并将其智能地分解和分配到最合适的视觉组件中。您需要决定使用哪些组件以及每个组件应包含哪些文本内容。

已知信息：
1.  **原始 Markdown 内容**:
    ```markdown
    {markdown_content}
    ```
2.  **可用的视觉组件类型及其描述 (用于内容匹配)**:

    * **`quote_box` (引用框)**: 用于展示引言、名言或重要的陈述。
        * **参数 (`content_params`)**:
            * `quote_text` (str): 引用的主要文本。
            * `attribution_text` (str, optional): 引用的出处。
        * **样式 (`style_id`)**: `"default_quote"`, `"left_accent_bar_quote"`。
        * **视觉提示**: 适合独立的、有影响力的短语或段落。

    * **`data_callout` (数据标注框)**: 用于突出显示关键数据点、统计数字或指标。
        * **参数 (`content_params`)**:
            * `statistic_value` (str): 主要的数据或统计值。
            * `label_text` (str): 对该数据的描述性标签。
        * **样式 (`style_id`)**: `"default_data"`, `"circle_emphasis_data"`。
        * **视觉提示**: 使数字信息一目了然。适合从文本中提取的、需要强调的孤立数据点。

    * **`divider` (分隔线)**: 用于在视觉上分隔幻灯片上的不同内容区域或元素。
        * **参数 (`content_params`)**: {{}} (通常为空)。
        * **样式 (`style_id`)**: `"default_line"`, `"dots_accent_line"`。
        * **视觉提示**: 帮助组织内容，引导阅读顺序。

    * **`main_text` (主文本块)**: 用于放置不适合放入特定组件的、主要的段落文本内容。
        * **参数 (`content_params`)**:
            * `text_content` (str): 分配给此主文本块的 Markdown 格式的文本。
        * **视觉提示**: Markdown中的换行符将被识别，但复杂的Markdown标记（如`##`或`*`用于列表）将作为字面文本显示。如果需要将标题或列表等与普通段落区别对待，请将它们分配到不同的 `main_text` 元素中。

    * **`icon_title_bullets` (图标标题项目符号)**: 左侧为带图标和标题的区域，右侧为项目符号列表。
        * **参数 (`content_params`)**:
            * `icon_emoji` (str): 左侧图标框中使用的表情符号字符。
            * `content_data` (dict): 包含 `title` (str) 和 `bullets` (list of str) 的字典。
        * **视觉提示**: 适用于展示一个核心概念或主题（由图标和标题代表），并辅以多个相关的关键点。寻找H2/H3级别标题后紧跟项目符号列表的结构。

    * **`triple_card` (三卡片组)**: 并排展示三个带有标题和内容的卡片。
        * **参数 (`content_params`)**:
            * `cards_data` (list of 3 dicts): 每个字典包含 `title` (str) 和 `content` (str)。列表必须恰好包含三个元素。
            * `card_top_emojis` (list of str, optional): 卡片顶部的可选表情符号。
            * `card_icon_chars` (list of str, optional): 卡片右下角的可选图标字符。
        * **视觉提示**: 适合比较三个相关项目。寻找可平均分为三部分的结构，如三个连续的`###`或`####`级别标题引导的小节。

    * **`parallel_boxes` (并行双框)**: 并排展示两个文本框。
        * **参数 (`content_params`)**:
            * `title_text` (str): 左侧框的主要文本内容。
            * `content_text` (str): 右侧框的主要文本内容。
            * `emoji_left` (str, optional): 左侧框顶部的表情符号。
            * `emoji_right` (str, optional): 右侧框顶部的表情符号。
        * **视觉提示**: 适用于并列展示两项相关信息，如对比、原因与结果等。寻找可清晰分为两个语义相关且内容量大致均衡的文本块。

需求：
1.  **内容分析与组件选择**:
    * 深入理解 Markdown 内容的结构（列表、各级标题 H1-H6）和语义。
    * 根据内容特点和上述组件描述，决定最合适的组件类型来组织和呈现信息。
    * 优先选择能够最好地结构化信息的组件（如 `icon_title_bullets`, `triple_card`, `parallel_boxes`），而不是零散地使用多个 `main_text`，前提是内容结构与之匹配。
    * 确保所有原始 Markdown 内容都被合理地分配到某个组件中。如果某段内容不适合任何特定组件，应将其放入 `main_text` 元素中。可以有多个 `main_text` 元素。

2.  **内容分配与参数填充**:
    * 将原始 Markdown 内容的相应部分智能、准确地分配给所选组件的 `content_params`。
    * 对于 `icon_title_bullets`：从 Markdown 中提取标题文本（通常来自H2-H4级标题）和项目符号列表。
    * 对于 `triple_card`：将内容分为三个逻辑单元，每个单元包含标题和描述文本。确保 `cards_data` 列表恰好有三个元素。
    * 对于 `parallel_boxes`：寻找可分为两个语义相关且内容量相当的文本块。
    * 确保分配给 `content_params` (如 `title`, `content`, `bullets`, `statistic_value`, `label_text` 等) 的文本是纯文本或处理后的文本，不应再包含原始 Markdown 标记 (除非如 `main_text` 的 `text_content` 那样明确接受Markdown)。
    * 对于 Emojis 和 Icon Chars，如果内容中没有明确提示，您可以基于语义进行推荐或留空。

3.  **初步内容评估 (辅助后续布局)**:
    * 对于您选择的每一个组件，请根据其承载的内容量，给出一个大致的“内容份量”评估，可选值为：`"low"`, `"medium"`, `"high"`。这将帮助后续的布局阶段判断空间需求。
    * 考虑整体选择的组件数量和它们的“内容份量”，如果初步判断所选内容在典型幻灯片上可能会过于拥挤或信息量过大，请在输出的顶层添加一个 `layout_density_warning` 字段，值为 `true`。

输出格式：
请严格按照以下 JSON 格式返回。JSON 应包含一个名为 `selected_elements` 的列表。列表中的每个对象代表一个被选中的幻灯片元素，并包含以下字段：
* `element_type` (str): 组件类型。
* `content_params` (dict): 特定于该组件的内容参数。
* `style_id` (str, optional): 组件的样式 ID (如果适用)。
* `estimated_content_volume` (str): 内容份量评估 (`"low"`, `"medium"`, `"high"`)。

如果评估后认为内容可能过于密集，请在JSON的顶层包含 `layout_density_warning: true`。

{{
  "layout_density_warning": false, // 或者 true 如果评估内容过多
  "selected_elements": [
    {{
      "element_type": "icon_title_bullets",
      "content_params": {{ "icon_emoji": "💡", "content_data": {{ "title": "核心洞察", "bullets": ["发现点A", "发现点B"] }} }},
      "estimated_content_volume": "medium"
    }},
    {{
      "element_type": "main_text",
      "content_params": {{ "text_content": "这是一段补充说明或者不适合放入其他组件的文本。" }},
      "estimated_content_volume": "low"
    }}
    // ... 更多基于Markdown内容选择和分配的元素
  ]
}}"""

PROMPT_2_LAYOUT_AND_SIZING = """请扮演一位经验丰富的演示文稿设计师和空间布局专家。
您的任务是接收一组预选的幻灯片组件及其内容，并为这些组件在幻灯片上进行精确的布局设计。这包括决定它们的位置、尺寸，并为特定组件建议文本和Emoji的视觉大小。必须严格遵守所有边界和布局约束，并在必要时进行调整以防止内容溢出。

已知核心布局参数：
1.  **幻灯片物理宽度**: 10 英寸 (Inches)
2.  **幻灯片物理高度**: 7.5 英寸 (Inches)
3.  **内容区边距**: 左右各 0.5 英寸，上方1.5英寸，下方0.5英寸
4.  **内容区可用宽度**: 9.0 英寸 (计算结果: 10.0 - 2*0.5)
5.  **内容区可用高度**: 5.5 英寸 (计算结果: 7.5 - 1.5 - 0.5)
6.  **内容区绝对起始坐标**: `left_start = 0.5`, `top_start = 1.5`
7.  **内容区绝对结束边界**: `right_boundary = 9.5` (即 `left_start + 内容区可用宽度`), `bottom_boundary = 7.0` (即 `top_start + 内容区可用高度`)
8.  **组件间建议最小间距**: 0.25 英寸 (用于元素上下左右的分隔)

输入数据 (来自第一阶段的输出):
```json
{input_selected_elements_json}
```
该JSON包含一个 `selected_elements` 列表，每个元素有 `element_type`, `content_params`, `style_id` (可选), 和 `estimated_content_volume`。

需求：
1.  **严格遵守边界与布局规则 (最高优先级)**:
    * 所有元素的 `left` 坐标必须 `>= 内容区绝对起始坐标.left_start` (0.5 英寸)。
    * 所有元素的右边缘 (`left + width`) 必须 `<= 内容区绝对结束边界.right_boundary` (9.5 英寸)。
    * 所有元素的 `top` 坐标必须 `>= 内容区绝对起始坐标.top_start` (1.5 英寸)。
    * 所有元素的下边缘 (`top + height`) 必须 `<= 内容区绝对结束边界.bottom_boundary` (7.0 英寸)。**此为硬性限制，不得超出。**
    * 在垂直方向上，所有组件的 `height` 及其之间的间距 (至少0.25英寸) 的总和，不得超过内容区的可用高度 (5.5英寸)。请在布局时进行全局考量。

2.  **组件尺寸与位置确定 (`position` 和 `size`)**:
    * 为 `input_selected_elements_json` 中的每一个组件确定其在幻灯片上的精确 `position` (`left`, `top`) 和 `size` (`width`, `height`)。单位为英寸。
    * 在估计组件（尤其是包含文本的组件）的 `height` 和 `width` 时，需仔细考虑其内部文本内容的多少（可参考输入的 `estimated_content_volume`）、预估的文本和Emoji大小（参考需求3）、必要的内边距（组件内容距离其边界至少有0.1到0.2英寸）和舒适的行高（例如字体高度的1.2-1.5倍）。
    * **`main_text` 组件的高度处理**:
        * 其 `height` **必须**根据 `text_content` 的实际行数、建议的字体大小（内容默认12pt，行高为其1.2-1.5倍）进行**最小化计算**。组件内部上下总内边距不应超过0.2英寸。
        * **如果 `main_text` 的文本内容很少（例如一两行），其高度应该非常小，以避免不必要的空白。**
        * 如果 `main_text` 用于放置少量补充文本，其 `width` 也可适当缩小，无需默认占据整个可用宽度。
    * 对于 `divider`，其 `size.height` 通常非常小 (可设为名义值如 0.1 英寸)，主要确定 `left`, `top`, `width`。
    * 确保元素之间有适当的间距（建议至少 0.25 英寸），避免视觉拥挤和重叠。
    * 考虑整体的视觉平衡、层级关系和阅读流程（通常从上到下、从左到右）。

3.  **建议文本和Emoji尺寸 (`text_size`)**:
    * 对于以下特定组件类型，如果它们出现在最终的 `layout_elements` 中，请在输出中包含一个名为 `text_size` 的字典，用于建议的字体和Emoji大小 (单位: pt)：
        * **`icon_title_bullets`**: `text_size` 包含 `title_size`, `content_size`, 和 `emoji_size`。
        * **`triple_card`**: `text_size` 包含 `title_size`, `content_size`, 和 `emoji_size`。
        * **`parallel_boxes`**: `text_size` 包含 `content_size`, 和 `emoji_size`。
    * 您需要根据组件内容、其 `estimated_content_volume` 以及整体视觉和谐性，为这些 `*_size` 字段建议合适的、在演示文稿中清晰可读的 `pt` 值。这些建议值应与您在需求2中计算的组件 `width` 和 `height` 相辅相成。
    * 如果为了满足布局约束（尤其是下边界限制），可以考虑在合理范围内微调 `content_size`（例如，最小不低于10pt），但应优先通过调整组件 `height` 来解决。

4.  **最终检查与调整 (Final Check and Adjustment)**:
    * 在完成所有元素的初步布局和尺寸设定后，请进行一次最终检查。
    * 如果发现任何元素的下边缘 (`top + height`) 依然超出 `内容区绝对结束边界.bottom_boundary` (7.0 英寸)，或者所有元素加上它们之间的垂直间距后的总高度超过了 `内容区可用高度` (5.5 英寸)，则**必须采取以下一种或多种措施进行调整，优先级从高到低，直至满足所有边界约束**：
        1.  **优先压缩 `main_text` 的高度**：如果幻灯片中存在`main_text`元素，并且其内容允许，进一步压缩其高度至最小必要值。
        2.  **减少元素间的垂直间距**：可以将建议的0.25英寸间距适当减小（例如，逐步减至0.2英寸，甚至0.15英寸），但必须保持视觉上的基本区隔。
        3.  **统一调整一组导致溢出的元素的高度**：如果一组垂直或水平排列的元素（例如底部的多个卡片）是导致溢出的主要原因，可以考虑略微（统一地）减小这些元素的高度。这可能需要同时略微减小其内部内容的字体大小（例如，`content_size` 最小不低于9pt或10pt，以保证可读性）。
        4.  **略微减小非关键文本组件的字体大小**：对于非标题、非核心数据标注的文本内容，在可读性允许的前提下，可以考虑将 `content_size` 再降低1pt（例如，从12pt降至11pt）。
    * **最终目标是：绝不允许任何内容溢出定义的内容区边界。**

输出格式：
请严格按照以下 JSON 格式返回。JSON 应包含一个名为 `layout_elements` 的列表。列表中的每个对象代表一个幻灯片元素，并包含以下字段：
* `element_type` (str): 组件类型。
* `content_params` (dict): 从输入继承的该组件的内容参数。
* `style_id` (str, optional): 从输入继承的组件样式 ID。
* `position` (dict): {{ "left": float, "top": float }} (单位：英寸)。
* `size` (dict): {{ "width": float, "height": float }} (单位：英寸)。
* `text_size` (dict, optional): 包含建议的文本和Emoji尺寸（单位: pt）。

```json
{{
  "layout_elements": [
    {{
      "element_type": "icon_title_bullets",
      "content_params": {{ "icon_emoji": "💡", "content_data": {{ "title": "核心洞察", "bullets": ["发现点A", "发现点B"] }} }},
      "position": {{ "left": 0.5, "top": 1.5 }},
      "size": {{ "width": 8.5, "height": 2.0 }},
      "text_size": {{
        "title_size": 20,
        "content_size": 12,
        "emoji_size": 22
      }}
    }},
    {{
      "element_type": "main_text",
      "content_params": {{ "text_content": "这是一段补充说明。" }},
      "position": {{ "left": 0.5, "top": 3.75 }}, // top = 1.5 (previous_top) + 2.0 (previous_height) + 0.25 (spacing)
      "size": {{ "width": 8.5, "height": 0.5 }} // 高度严格根据内容计算
    }}
    // ... 更多布局好的元素
  ]
}}
"""

class SplitComponentAgent:
    def __init__(self):
        self.config = get_args_parser()
        self.LLM = OpenAI(
            api_key=self.config.OPENAI_API_KEY,
            base_url=self.config.OPENAI_BASE_URL)
        self.model = self.config.model

    def get_openai_response(self, prompt_text: str, client: OpenAI, model: str) -> dict:
        """
        向 OpenAI API 发送请求并获取 JSON 格式的响应。

        Args:
            prompt_text: 要发送给模型的完整提示。
            client: 初始化后的 OpenAI 客户端。
            model: 要使用的 OpenAI 模型。

        Returns:
            一个包含模型响应的字典 (已解析的 JSON)。
        """
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert presentation designer and information architect. Your goal is to generate valid JSON based on the user's instructions."},
                    {"role": "user", "content": prompt_text}
                ],
                response_format={"type": "json_object"}, # 请求 JSON 输出
                temperature=0.2 # 低温以获得更一致和结构化的输出
            )
            raw_content = completion.choices[0].message.content
            if "</think>" in raw_content.strip():
                raw_content = raw_content.strip().split("</think>", 1)[1]
            if "```json" in raw_content.strip():
                raw_content = raw_content.strip().split("```json", 1)[1]
                if "```" in raw_content:
                    raw_content = raw_content.rsplit("```", 1)[0]
            response_content = raw_content.strip()
            if response_content:
                return json.loads(response_content)
            else:
                print("Error: Received empty response content from OpenAI.")
                return {}
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return {}

    def generate_slide_layout_from_markdown(self,markdown_content: str) -> dict:
        """
        通过两步提示策略从 Markdown 内容生成幻灯片布局。

        Args:
            markdown_content: 原始的 Markdown 字符串。

        Returns:
            包含最终幻灯片布局元素的字典，如果出错则为空字典。
        """
        for i in range(3):  # 最多尝试3次
            try:
                # self.LL
                # --- 步骤 1: 内容分析与组件选择 ---
                prompt1_filled = PROMPT_1_CONTENT_ANALYSIS_AND_COMPONENT_SELECTION.format(markdown_content=markdown_content)
                selected_elements_response = self.get_openai_response(prompt1_filled, self.client, self.model)
                if not selected_elements_response or "selected_elements" not in selected_elements_response:
                    assert 0==1

                # --- 步骤 2: 组件布局与尺寸设定 ---
                selected_elements_json_str = json.dumps(selected_elements_response, ensure_ascii=False)
                prompt2_filled = PROMPT_2_LAYOUT_AND_SIZING.format(input_selected_elements_json=selected_elements_json_str)
                final_layout_response = self.get_openai_response(prompt2_filled, self.client, self.model)
                if not final_layout_response or 'layout_elements' not in final_layout_response:
                    assert 0 == 1
                if 'element_type' not in final_layout_response['layout_elements'][0] \
                        or 'content_params' not in final_layout_response['layout_elements'][0] \
                        or 'position' not in final_layout_response['layout_elements'][0] \
                        or 'size' not in final_layout_response['layout_elements'][0]:
                    assert 0 == 1
                return final_layout_response

            except:
                print(f"调用 LLM 时发生预料之外的错误 (尝试 {i + 1}/{3})")

            if i < 2:  # 如果不是最后一次尝试
                time.sleep(1)  # 重试前等待1秒