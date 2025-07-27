# ./mdtree/component_agent.py
import json
from openai import OpenAI
# 假设您的 OpenAI 配置类 MyConfig 在这里可以访问
# from readconfig.myconfig import MyConfig
from typing import Dict, Any, Optional
import time  # 导入 time 模块

# --- 组件布局代理的 Prompt 模板 (更新版) ---
from APC.config_parser import get_args_parser


COMPONENT_LAYOUT_PROMPT_TEMPLATE_HALF = """请扮演一位经验丰富的演示文稿设计师和信息架构师。
您的任务是为一张幻灯片的内容进行布局设计。您需要决定如何使用提供的文本内容，并选择合适的视觉组件来增强信息传递，同时为特定组件建议文本和Emoji的尺寸。

**核心布局要求**:
**此幻灯片为左文右图布局。** 您生成的所有视觉组件将被放置在幻灯片的左侧区域，右侧区域将用于放置一张照片。因此，您生成的**任何单个组件的 `width` 都不得超过 4.0 英寸**。

已知信息：
1.  **幻灯片可用宽度**: 10 英寸 (Inches)
2.  **幻灯片可用高度**: 7.5 英寸 (Inches)
3.  **内容区边距**: 左右各 0.5 英寸，上方1.5英寸，下方0.5英寸
4.  **内容区可用宽度 (总计)**: 9.0 英寸 (10.0 - 2*0.5)
5.  **内容区可用高度**: 5.5 英寸 (7.5 - 1.5-0.5)
6.  **组件布局区可用宽度**: **4.0 英寸** (位于幻灯片左侧)
7.  **内容区起始坐标**: left=0.5, top=1.5
8.  **内容区结束坐标 (组件部分)**: **right_edge=4.5**, bottom_edge=7.0
9.  **原始 Markdown 内容**:
    ```markdown
    {markdown_content}
    ```
10. **可用的视觉组件类型及其描述**:

    * **`quote_box` (引用框)**: 用于展示引言、名言或重要的陈述。
        * **参数 (`content_params`)**:
            * `quote_text` (str): 引用的主要文本。 (对应函数参数: `quote_text`)
            * `attribution_text` (str, optional): 引用的出处 (例如，作者)。 (对应函数参数: `attribution_text`)
        * **样式 (`style_id`)**:
            * `"default_quote"`: 浅色背景，带有边框，引用文本通常为斜体并居中。署名文本较小，右对齐。
            * `"left_accent_bar_quote"`: 特点是在引用框的左侧有一条彩色的强调竖线，主框体可能无边框。其他文本样式与 "default_quote" 类似。
        * **视觉提示**: 通常用于使某段文字从周围内容中突出，增加其强调性。适合独立的、有影响力的短语或段落。

    * **`data_callout` (数据标注框)**: 用于突出显示关键数据点、统计数字或指标。
        * **参数 (`content_params`)**:
            * `statistic_value` (str): 主要的数据或统计值 (例如, "75%", "3M+"). (对应函数参数: `statistic_value`)
            * `label_text` (str): 对该数据的描述性标签。 (对应函数参数: `label_text`)
        * **样式 (`style_id`)**:
            * `"default_data"`: 通常为圆角矩形，具有特定的背景色。统计数值文字较大，使用主强调色；标签文字较小，使用深色文本。文本内容通常居中。
            * `"circle_emphasis_data"`: 通常为圆形或椭圆形，可能使用更醒目的背景色（如次强调色），统计数值和标签文字都使用浅色。文本内容通常居中。选择此样式时，建议在 `size` 中使 `width` 和 `height` 相等。
        * **视觉提示**: 使数字信息一目了然，吸引注意力。适合从文本中提取的、需要强调的孤立数据点。

    * **`divider` (分隔线)**: 用于在视觉上分隔幻灯片上的不同内容区域或元素。
        * **参数 (`content_params`)**: {{}} (通常为空)
        * **样式 (`style_id`)**:
            * `"default_line"`: 一条简单的、具有一定粗细和颜色的直线。
            * `"dots_accent_line"`: 一条相对较细的直线，中间带有一个或多个装饰性的彩色圆点。
        * **视觉提示**: 帮助组织内容，引导阅读顺序，增加页面的呼吸感。

    * **`main_text` (主文本块)**: 用于放置不适合放入特定组件的、主要的段落文本内容。
        * **参数 (`content_params`)**:
            * `text_content` (str): 分配给此主文本块的 Markdown 格式的文本。(对应函数参数: `text_content`)
        * **视觉提示**: 这是幻灯片信息的主要载体，应保证其可读性。其布局应考虑与其他组件的协调。Markdown中的换行符将被识别，但复杂的Markdown标记（如`##`或`*`用于列表）将作为字面文本显示。如果需要将标题或列表等与普通段落区别对待，请将它们分配到不同的 `main_text` 元素中，并调整其位置和大小以示区别。

    * **`icon_title_bullets` (图标标题项目符号)**: 左侧为带图标和标题的区域，右侧为项目符号列表。
        * **参数 (`content_params`)**:
            * `icon_emoji` (str): 左侧图标框中使用的表情符号字符 (例如 "🚀", "💡", "✅")。 (对应函数参数: `icon_emoji`)
            * `content_data` (dict): 包含 `title` (str) 和 `bullets` (list of str) 的字典。 (对应函数参数: `content_data`)
                * `title` (str): 图标区域下方或旁边的标题文本。
                * `bullets` (list of str): 右侧区域的项目符号点列表。Markdown中的项目符号列表应转换为此结构。
        * **视觉提示**: 适用于展示一个核心概念或主题（由图标和标题代表），并辅以多个相关的关键点或特性。如果Markdown内容中有一个明确的标题（如 H2, H3级别）后紧跟一个项目符号列表（以 `-`, `*` 或数字开头的列表），则此组件是一个很好的选择。

    * **`triple_card` (三卡片组)**: 并排展示三个带有标题和内容的卡片，中间卡片可能有突出显示。
        * **参数 (`content_params`)**:
            * `cards_data` (list of 3 dicts): 包含三个字典的列表，每个字典代表一张卡片，并包含 `title` (str) 和 `content` (str)。列表必须恰好包含三个元素。(对应函数参数: `cards_data`)
                * `title` (str): 卡片的标题。
                * `content` (str): 卡片的主要内容文本。
            * `card_top_emojis` (list of str, optional): 长度最多为3的列表，对应三张卡片顶部的可选表情符号。如果Markdown内容中没有明确指定或不适用，则省略此字段或让LLM根据卡片内容选择合适的emoji。
            * `card_icon_chars` (list of str, optional): 长度最多为3的列表，对应三张卡片右下角的可选图标字符。如果Markdown内容中没有明确指定或不适用，则省略此字段或让LLM根据卡片内容选择合适的图标。
        * **视觉提示**: 适合比较三个相关项目、特性、方案或阶段性成果。寻找可以将内容平均分为三个逻辑部分的结构，每个部分都有一个小标题和相应的描述性文本。**注意：在此布局下，三个卡片必须在 4.0 英寸的总宽度内水平排列，请相应地调整每个卡片的宽度。**

    * **`parallel_boxes` (并行双框)**: 并排展示两个文本框，每个框内顶部可以有可选的表情符号。
        * **参数 (`content_params`)**:
            * `title_text` (str): 左侧框的主要文本内容。 (对应函数参数: `title_text`)
            * `content_text` (str): 右侧框的主要文本内容。 (对应函数参数: `content_text`)
            * `emoji_left` (str, optional): 左侧框顶部的表情符号。如果Markdown内容中没有明确指定或不适用，则省略此字段或让LLM根据文本内容选择合适的emoji。
            * `emoji_right` (str, optional): 右侧框顶部的表情符号。如果Markdown内容中没有明确指定或不适用，则省略此字段或让LLM根据文本内容选择合适的emoji。
        * **视觉提示**: 适用于并列展示两项相关信息，例如对比、原因与结果、问题与解决方案、定义与示例等。**注意：在此布局下，两个框必须在 4.0 英寸的总宽度内水平排列。**

需求：
1.  **分析内容**: 理解 Markdown 内容的结构和语义。特别注意列表、各级标题（H1-H6）以及可以被归纳为多个逻辑组块（例如，2个或3个并行要点）的内容。
2.  **选择组件**: 根据内容和上述组件描述，决定是否以及如何使用这些组件。优先选择能够最好地组织和呈现信息的组件。考虑使用更结构化的组件（如 `icon_title_bullets`, `triple_card`, `parallel_boxes`）来代替多个零散的 `main_text` 块，前提是内容结构与之匹配。
3.  **内容分配**: 将原始 Markdown 内容的相应部分智能地分配给所选的组件。
    * 对于 `icon_title_bullets`：从 Markdown 中提取一个合适的标题文本（通常来自H2-H4级别标题）和紧随其后的项目符号列表（将其转换为字符串列表）。
    * 对于 `triple_card`：尝试将内容分为三个逻辑单元，每个单元包含一个标题（可能来自H3-H5级别标题或段落起始的粗体文本）和一些描述性文本。确保 `cards_data` 列表中恰好有三个元素。
    * 对于 `parallel_boxes`：寻找可以分为两个语义相关且内容量相当的文本块，分别作为 `title_text` 和 `content_text`。
    * 确保分配给 `content_params` 中如 `title`, `content`, `bullets`, `statistic_value`, `label_text` 等字段的文本是纯文本或处理后的文本，不应再包含原始 Markdown 标记 (除非该字段明确说明接受 Markdown，如 `main_text` 的 `text_content`)。对于 Emojis 和 Icon Chars，如果内容中没有明确提示，可以由LLM基于语义进行推荐或留空。
4.  **布局设计与组件尺寸估算**: 为每个选用的组件和 `main_text` 块决定其在幻灯片上的精确位置（`left`, `top`）和尺寸（`width`, `height`）。单位为英寸 (Inches)。
    * 在估计组件（尤其是包含文本的组件）的 `height` 和 `width` 时，请务必考虑其内部文本内容的多少、预估的文本和Emoji大小（参考需求5）、必要的内边距（组件内容距离其边界至少有0.1到0.2英寸）和舒适的行高（例如字体高度的1.2-1.5倍）。文本越多，所需尺寸通常越大。
    * 确保元素之间有适当的间距（建议至少 0.25 英寸），避免视觉拥挤和重叠。
    * 考虑整体的视觉平衡、层级关系和阅读流程。主要内容流向通常为从上到下、从左到右，且全部局限在左侧 4.0 英寸的区域内。
    * **定义清晰的幻灯片边距：所有元素必须严格放置在由“已知信息”部分定义的左侧组件布局区内。具体而言，元素的有效放置区域为：**
        * **单个组件的 `width` 必须 <= 4.0 英寸。**
        * **元素的 `left` 坐标必须 >= 0.5。**
        * **元素的 `(left + width)` 值必须 <= 4.5。**
        * **元素的 `top` 从 1.5 开始，且 `(top + height)` 必须 <= 7.0。**
    * `main_text` 块应灵活利用组件未占用的空间，或者用于呈现不适合其他组件的段落。
5.  **建议文本和Emoji尺寸 (`text_size`)**:
    * 对于以下特定组件类型，如果它们出现在 `selected_elements_json` 中，请在输出中包含一个名为 `text_size` 的字典，用于建议的字体和Emoji大小：
        * **`data_callout`**: `text_size` 包含 `title_size`, 和 `content_size`。
        * **`icon_title_bullets`**: `text_size` 包含 `title_size`, `content_size`, 和 `emoji_size`。
        * **`triple_card`**: `text_size` 包含 `title_size`, `content_size`, 和 `emoji_size`。
        * **`parallel_boxes`**: `text_size` 包含 `content_size`, 和 `emoji_size`。
    * `title_size` 用于控制相应组件中标题文本的大小。
    * `content_size` 用于控制相应组件中正文、列表项或主要描述文本的大小。
    * `emoji_size` 用于控制相应组件中Emoji的视觉大小，应与其关联的文本（如标题或内容）协调。
    * 您需要根据组件内容和整体视觉和谐性，为这些 `*_size` 字段建议合适的、在演示文稿中清晰可读的 `pt` 值。这些建议值应与您在需求4中估算的组件 `width` 和 `height` 相辅相成，确保内容能在计算出的组件框内完美展示。
6.  **输出格式**: 以 JSON 格式返回布局方案。JSON 应包含一个名为 "layout_elements" 的列表。列表中的每个对象代表一个幻灯片元素，并包含以下字段：
    * `element_type`: (str) 组件类型 (e.g., "quote_box", "data_callout", "divider", "main_text", "icon_title_bullets", "triple_card", "parallel_boxes").
    * `content_params`: (dict) 特定于该组件的内容参数。
        * 对于 `quote_box`: {{ "quote_text": "...", "attribution_text": "..." }}
        * 对于 `data_callout`: {{ "statistic_value": "...", "label_text": "..." }}
        * 对于 `divider`: {{}}
        * 对于 `main_text`: {{ "text_content": "..." }}
        * 对于 `icon_title_bullets`: {{ "icon_emoji": "🚀", "content_data": {{ "title": "模块标题", "bullets": ["要点1", "要点2"] }} }}
        * 对于 `triple_card`: {{ "cards_data": [{{ "title": "卡片1标题", "content": "内容1" }}, {{ "title": "卡片2标题", "content": "内容2" }}, {{ "title": "卡片3标题", "content": "内容3" }}], "card_top_emojis": ["💡", "🚀", "🌟"], "card_icon_chars": ["📈", "📢", "👍"] }} (emojis 和 icon_chars 是可选的, 如果提供，列表长度应与卡片数量匹配，通常为3)
        * 对于 `parallel_boxes`: {{ "title_text": "左侧核心观点", "content_text": "右侧补充说明", "emoji_left": "✒️", "emoji_right": "📄" }}
    * `style_id`: (str, optional) 组件的样式 ID (如果适用，例如 `quote_box` 和 `data_callout`)。对于没有预定义样式的组件（如 `icon_title_bullets`, `triple_card`, `parallel_boxes`），此字段可以省略。
    * `position`: (dict) {{ "left": float, "top": float }} (单位：英寸)
    * `size`: (dict) {{ "width": float, "height": float }} (单位：英寸)
    * `text_size`: (dict, optional) 包含建议的文本和Emoji尺寸（单位: pt）。**仅在需求5中指定的组件类型 (`icon_title_bullets`, `triple_card`, `parallel_boxes`) 被选用时出现此字段。** 结构如：`{{ "title_size": 22, "content_size": 12, "emoji_size": 20 }}` (具体键根据组件类型而定)。

**重要提示**:
* 确保所有原始 Markdown 内容都被合理地分配到某个 `layout_elements` 中。可以有多个 `main_text` 元素来容纳不同的文本片段或标题。
* 如果某段内容不适合任何特定组件，应将其放入 `main_text` 元素中。
* 对于 `divider`，其 `size.height` 通常非常小 (可设为名义值如 0.1 英寸)，主要确定 `left`, `top`, `width`。
* 在为 `icon_title_bullets`, `triple_card`, `parallel_boxes` 等组件分配内容时，要特别注意从原始 Markdown 中准确提取并转换数据到其 `content_params` 所需的结构。如果 Markdown 的结构不完全匹配这些复杂组件，优先考虑使用更简单组件（如多个 `main_text`）以保证信息准确性。
* 如果 Markdown 内容片段非常短，或者不足以填充一个复杂组件的所有必需字段，则不应强行使用该组件。
* “main_text 块的 height 应根据其文本内容进行有效适配，避免不必要的空白区域”。
* **布局约束: 所有组件的 `width` 必须 <= 4.0。** 所有元素的 left 必须 >= 0.5，且 (left + width) 必须 <= 4.5。所有元素的 top 必须 >= 1.5，且 (top + height) 必须 <= 7.0。严格遵守这些边界至关重要。

**最终检查与调整**:
* 在完成所有元素的初步布局和尺寸设定后，请进行一次最终检查。
* **首先，再次确认没有任何组件的 `width` 超过 4.0 英寸，且没有任何组件的 `left + width` 超过 4.5 英寸。**
* 接下来，如果发现任何元素的下边缘 (`top + height`) 依然超出 `内容区绝对结束边界.bottom_boundary` (7.0 英寸)，或者所有元素加上它们之间的垂直间距后的总高度超过了 `内容区可用高度` (5.5 英寸)，则**必须采取以下一种或多种措施进行调整，优先级从高到低，直至满足所有边界约束**：
    1.  **优先压缩 `main_text` 的高度**：如果幻灯片中存在`main_text`元素，并且其内容允许，进一步压缩其高度至最小必要值。
    2.  **减少元素间的垂直间距**：可以将建议的0.25英寸间距适当减小（例如，逐步减至0.2英寸，甚至0.15英寸），但必须保持视觉上的基本区隔。
    3.  **统一调整一组导致溢出的元素的高度**：如果一组垂直或水平排列的元素（例如底部的多个卡片）是导致溢出的主要原因，可以考虑略微（统一地）减小这些元素的高度。这可能需要同时略微减小其内部内容的字体大小（例如，`content_size` 最小不低于9pt或10pt，以保证可读性）。
    4.  **略微减小非关键文本组件的字体大小**：对于非标题、非核心数据标注的文本内容，在可读性允许的前提下，可以考虑将 `content_size` 再降低1pt（例如，从12pt降至11pt）。
* **最终目标是：绝不允许任何内容溢出定义的内容区边界。**
    
请严格按照以下 JSON 格式返回，不要包含任何额外的解释性文字或代码块标记：
```json
{{
  "layout_elements": [
    {{
      "element_type": "icon_title_bullets", // 示例：一个需要text_size的组件
      "content_params": {{ "icon_emoji": "💡", "content_data": {{ "title": "核心洞察", "bullets": ["发现点A", "发现点B"] }} }},
      // "style_id" 在此组件中通常省略
      "position": {{ "left": 0.5, "top": 1.5 }},
      "size": {{ "width": 4.0, "height": 2.5 }},
      "text_size": {{
        "title_size": 20, // 单位：pt
        "content_size": 12, // 单位：pt (用于bullets)
        "emoji_size": 22    // 单位：pt (用于icon_emoji)
      }}
    }},
    {{
      "element_type": "main_text", // 示例：一个不需要text_size的组件
      "content_params": {{ "text_content": "这是一段补充说明或者不适合放入其他组件的文本。" }},
      "position": {{ "left": 0.5, "top": 4.25 }},
      "size": {{ "width": 4.0, "height": 1.0 }}
      // 此组件类型不需要 text_size 字段
    }}
    // ... 更多基于Markdown内容选择和设计的元素
  ]
}}"""


class ComponentAgentHalf:
    def __init__(self):
        self.config = get_args_parser()
        self.LLM = OpenAI(
            api_key=self.config.OPENAI_API_KEY,
            base_url=self.config.OPENAI_BASE_URL)
        self.model = self.config.model

    def get_layout_plan(self, markdown_content: str) -> Optional[Dict[str, Any]]:
        """
        调用 LLM 获取给定 Markdown 内容的布局计划。

        Args:
            markdown_content: 要布局的原始 Markdown 文本。

        Returns:
            一个包含布局指令的字典 (解析后的 JSON)，如果成功则返回，否则返回 None 或备用布局。
        """

        agent_prompt = COMPONENT_LAYOUT_PROMPT_TEMPLATE_HALF.format(markdown_content=markdown_content)

        # 重试逻辑
        for i in range(3):  # 最多尝试3次
            try:
                create_layout_task = {"role": "user", "content": agent_prompt}
                response = self.LLM.chat.completions.create(
                    model=self.model,  # 请替换为您的目标模型
                    messages=[create_layout_task],
                    temperature=0.2,  # 对于布局，温度不宜过高，以保证结果的稳定性和实用性
                    stream=False
                )
                raw_content = response.choices[0].message.content.strip()

                # 清理可能的代码块标记 (如果 response_format 未完全生效或未使用)
                if "</think>" in raw_content.strip():
                    raw_content = raw_content.strip().split("</think>", 1)[1]
                if "```json" in raw_content.strip():
                    raw_content = raw_content.strip().split("```json", 1)[1]
                    if "```" in raw_content:
                       raw_content = raw_content.rsplit("```", 1)[0]
                raw_content = raw_content.strip()
                parsed_content = json.loads(raw_content)  # 解析 JSON

                # 验证返回的 JSON 是否包含必要的顶层结构
                if "layout_elements" in parsed_content and isinstance(parsed_content["layout_elements"], list):
                    # 可以添加更详细的验证，例如检查每个元素的必需字段
                    return parsed_content
                else:
                    print(f"错误: LLM 返回的 JSON 结构无效 (缺少 'layout_elements' 列表或类型错误)。响应: {raw_content}")
                    # 不立即重试，因为这可能是模型理解或 Prompt 的问题，而不仅仅是瞬时错误
                    # 如果需要，可以在这里决定是否进行下一次尝试
                    if i < 2:  # 如果不是最后一次尝试
                        print(f"将在下一次尝试中继续...")
                        time.sleep(1)  # 等待1秒再试
                        continue
                    else:  # 最后一次尝试也失败
                        parsed_content = None  # 标记为无效，将触发备用方案

            except json.JSONDecodeError as e:
                print(f"JSON 解析错误 (尝试 {i + 1}/{3}): {e}。原始响应片段: '{raw_content[:200]}...'")
            except AttributeError as e:  # 例如 response.choices[0].message 为 None
                print(f"获取 LLM 响应内容时出错 (尝试 {i + 1}/{3}): {e}。可能响应为空或结构不符合预期。")
            except Exception as e:  # 捕获其他 OpenAI API 错误或网络问题
                print(f"调用 LLM 时发生预料之外的错误 (尝试 {i + 1}/{3}): {e}")

            if i < 2:  # 如果不是最后一次尝试
                time.sleep(1)  # 重试前等待1秒

        # 所有尝试失败后
        print("错误: ComponentAgent 在多次尝试后未能成功获取并解析有效的布局计划。将返回默认备用布局。")
        return {  # 返回一个包含原始 Markdown 的简单布局作为最终备用方案
            "layout_elements": [
                {
                    "element_type": "main_text",
                    "content_params": {"markdown_text": markdown_content},
                    "position": {"left": 0.5, "top": 1.5},
                    "size": {"width": 8.0, "height": 4.5}
                }
            ]
        }


if __name__ == '__main__':
    print("正在运行 ComponentAgent 测试...")
    agent = ComponentAgent()
    slide_body_markdown = """
    这是一段引人入胜的开场白，为接下来的内容奠定了基础。我们希望在这里抓住观众的注意力。

    > “机会总是留给有准备的人。” —— 路易斯·巴斯德
    > 这是一句非常鼓舞人心的名言，我们希望用一个漂亮的引用框来展示它。

    接下来，我们有一些关键的年度数据需要突出显示：

    * **新用户增长率**: 45%
    * **客户满意度**: 92/100
    * **市场份额**: 增加了 5 个百分点

    这些数据点非常重要，应该用数据标注框清晰地展示出来，也许可以并排排列或者上下排列，取决于空间的可用性。

    --- (这里可能需要一个分隔线)

    然后，我们想深入探讨一下增长策略的细节。这部分内容比较多，可能需要一个较大的主文本区域。
    策略一：xxxxxx
    策略二：yyyyyy

    最后，用一段总结性的文字来结束本张幻灯片的内容。
        """

    print(f"\n正在为以下 Markdown 内容获取布局计划:\n---\n{slide_body_markdown}\n---")
    layout_plan = agent.get_layout_plan(slide_body_markdown)

    if layout_plan and layout_plan.get("layout_elements"):
        print("\n成功获取布局计划:")
        # 使用 ensure_ascii=False 来正确显示中文字符
        print(json.dumps(layout_plan, indent=2, ensure_ascii=False))
    else:
        print("\n未能获取有效的布局计划。")