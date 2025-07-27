import re
from openai import OpenAI
from APC.config_parser import get_args_parser
import time

content_expand_prompt = """您是一位资深的演示内容策划与文本优化AI专家。您的核心能力在于将结构化的初步构想或简洁大纲，精心打磨并扩充为既能充分填充幻灯片版面、使其信息饱满，又能在演示时清晰传达核心信息、引人入胜的优质文本内容。您善于平衡信息的深度与呈现的简洁性，确保扩充后的内容适合在幻灯片上高效展示。

**核心任务：**
基于提供的输入文本（该文本概述了某一主题的关键要点或章节），您的任务是显著地丰富和扩展每个部分。目标是将初始框架转化为更详细、更具解释性且论据更充分的文字作品，使其内容足以良好地填充演示幻灯片，并帮助演示者向观众进行清晰、有力的阐述。

**输入文本框架：**
{}

**详细内容扩展指令（适用于输入的每个部分）：**

1.  **解构并深化核心概念：**
    * 识别该部分提出的中心思想、概念或陈述。
    * 通过将其分解为其构成部分，解释其细微差别，定义关键术语并探讨其基本原则来详细阐述。确保阐述的深度和广度足以支撑一页或数个要点清晰的幻灯片内容。
    * 如果输入呈现了某个发现、事件或论点，请详细说明其背景、来龙去脉和主要特征，使其易于观众理解。

2.  **用相关证据和示例进行证实：**
    * 用可信且与上下文相符的证据、示例、数据或案例研究来支持阐述的概念，这些内容应易于在幻灯片上呈现（例如，关键数据点、有代表性的引言、简明扼要的案例）。
    * 此类证实的性质应与输入文本的领域直接相关：
        * **对于科学/技术主题：** 引用关键的既定理论、核心实验结果、重要的经验数据、有代表性的统计发现、关键算法步骤或简明的案例研究。
        * **对于人文学科/艺术/社会科学主题：** 参考核心的原始文本节选、标志性的历史事件、精辟的批判性分析、有影响力的理论概要、简短且有力的权威来源引文、具有代表性的艺术实例或概括性的社会趋势。
        * **对于商业/项目管理/实践领域主题：** 使用关键的行业报告结论、核心市场数据、重要的项目成果、核心绩效指标、凝练的最佳实践或易于理解的说明性场景。
    * 确保所有示例和证据都能直接阐明并加强所提出的观点，并且适合在幻灯片中作为支撑材料。

3.  **分析机制、过程或结构：**
    * 在适用情况下，解释与该部分主题相关的潜在机制、过程、方法论或结构组成部分，力求使复杂概念条理清晰，易于通过幻灯片要点或简图辅助说明。
    * 讨论不同元素如何相互作用，或其中存在的因果关系，重点突出关键环节。
    * 例如，这可能涉及解释一个科学过程的关键步骤、一个历史发展的核心驱动因素、一个系统架构的主要模块、一种艺术技巧的突出特点或一个逻辑论证的中心环节。

4.  **探讨重要性、影响和背景：**
    * 讨论所呈现信息的更广泛重要性或影响，凝练出适合在幻灯片上强调的“亮点”或“关键启示”。
    * 考虑其应用、在其领域内的重要性、任何未解决的关键问题、主要争论点，或其与其他核心概念或发展的关系。
    * 将信息置于更大的理论、历史或实践背景中，并提炼出对观众最有价值的背景信息。

5.  **保持清晰性、连贯性和呈现的吸引力：**
    * 确保所用语言清晰、准确且适合主题内容，同时兼顾口语化和书面语的平衡，使其既专业又易懂。在简单术语足够时避免使用行话，或解释必要的技术术语。
    * 语气应翔实、客观、权威，同时具有吸引力和说服力，能够抓住观众的注意力。
    * 在每个扩展部分内保持逻辑流程和连贯性，确保内容组织有序，适合分点或分层在幻灯片上展示。如果整体输出是单一连续的文本，则确保平稳过渡，便于切分为不同的幻灯片主题。

**输出格式和语言：**

* **结构：** 严格保留并遵循输入文本的结构格式（例如，如果输入使用Markdown标题如 `#`, `##`, `###`, 以及 `<p>` 标签内的段落，输出必须为相应扩展内容复制此结构）。内容应组织得当，便于后续拆分成单张或系列幻灯片。
* **语言：** 输出语言应与输入文本的语言一致。/no_think"""


class CotentAgent:
    def __init__(self):
        self.config = get_args_parser()
        self.LLM = OpenAI(
            api_key=self.config.OPENAI_API_KEY,
            base_url=self.config.OPENAI_BASE_URL)
        self.model = self.config.model

    def llm_response(self, content=False):
        agent_prompt = content_expand_prompt.format(content)

        for i in range(3):
            try:
                create_outline = {"role": "user",
                                  "content": agent_prompt}
                response = self.LLM.chat.completions.create(
                    model=self.model,
                    messages=[create_outline],
                    temperature=1.0,
                    stream=False
                )
                raw_content = response.choices[0].message.content
                # 尝试清理可能的代码块标记
                if "</think>" in raw_content.strip():
                    raw_content = raw_content.strip().split("</think>", 1)[1]
                if "```json" in raw_content.strip():
                    raw_content = raw_content.strip().split("```json", 1)[1]
                    if "```" in raw_content:
                       raw_content = raw_content.split("```", 1)[0]
                raw_content = raw_content.strip()

                return raw_content

            except (KeyError, Exception) as e:  # 捕获特定错误 + 通用后备
                print(f"尝试 {i+1} 失败: {e}")
                if i < 2:  # 最后一次尝试后不睡眠
                    time.sleep(1)  # 重试前等待1秒
                continue  # 进入循环的下一次迭代

    def __call__(self, input_text_content):
        """
        将输入文本分割成多个结构化片段：
        1. 第一个H2标题之前的前导文本（如果有）。
        2. 每个H2标题及其全部内容（直到下一个H2标题或文本末尾）。

        然后对每个片段应用内部的 'process_segment' 方法，并将结果拼接。

        Args:
            input_text_content (str): 需要处理的完整文本内容。

        Returns:
            str: 处理并重新拼接后的文本内容。
        """

        def process_segment(segment_text_block):

            segment_text_block = self.llm_response(segment_text_block)
            return segment_text_block + '\n\n'

        if self.split is False:
            return process_segment(input_text_content)

        elif self.split is True:
            h2_marker_pattern = r"^## (?!#)"
            h2_section_start_indices = [match.start() for match in
                                        re.finditer(h2_marker_pattern, input_text_content, flags=re.MULTILINE)]

            raw_text_segments = []  # 用于存放分割后的原始文本片段

            if not h2_section_start_indices:
                # 如果没有找到任何H2标题，则整个文本视为一个单独的片段
                if input_text_content:  # 避免处理完全空的输入字符串，除非有意
                    raw_text_segments.append(input_text_content)
            else:
                # 1. 处理前导文本 (第一个H2标题之前的内容)
                first_h2_start_index = h2_section_start_indices[0]
                if first_h2_start_index > 0:
                    # 如果第一个H2标题不是从文本开头开始，则存在前导文本
                    preamble = input_text_content[0:first_h2_start_index]
                    raw_text_segments.append(preamble)

                # 2. 处理每个H2标题及其内容
                for i in range(len(h2_section_start_indices)):
                    current_h2_start = h2_section_start_indices[i]

                    # 确定当前H2部分的结束位置
                    if i + 1 < len(h2_section_start_indices):
                        # 如果有下一个H2标题，则当前部分在此之前结束
                        next_h2_start_for_slicing = h2_section_start_indices[i + 1]
                    else:
                        # 这是最后一个H2标题，其内容延伸到文本末尾
                        next_h2_start_for_slicing = len(input_text_content)

                    h2_section_block = input_text_content[current_h2_start:next_h2_start_for_slicing]
                    raw_text_segments.append(h2_section_block)

            # 对每个分割出来的原始文本片段应用 process_segment 方法
            processed_segments_list = []
            processed_segments_list.append(raw_text_segments[0])
            for segment_item in raw_text_segments[1:]:
                processed_segments_list.append(process_segment(segment_item))

            # 将所有处理过的片段拼接起来
            return "".join(processed_segments_list)