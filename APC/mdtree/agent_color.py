import json

from openai import OpenAI
from APC.config_parser import get_args_parser
from pptx.dml.color import RGBColor
import time
from typing import List, Optional # 用于类型提示

title_color_prompt = '''请扮演一位专业的UI/UX设计师。我正在设计一个PowerPoint演示文稿的封面页，需要一个协调的色彩主题。

已知信息：
- 页面类型：封面页 (Cover Slide)
- 背景颜色：RGB{}
- 演示文稿主题：教育

需求：
请为这个封面页推荐两种文字颜色：
1.  **标题 (Main Title) 颜色**：需要醒目、吸引人，并与背景形成强对比。
2.  **内容/副标题 (Content/Subtitle) 颜色**：需要清晰可读，通常比主标题颜色稍弱一些，但仍需与背景有足够对比度。

请同时考虑颜色的搭配和谐度以及专业性。

**输出格式要求（请严格遵守）：**
请使用json格式返回，切勿输出json格式外的内容。格式如下：
{{
"titleColor": [R, G, B],
"contentColor": [R, G, B]
}}/no_think'''

content_color_prompt = """请扮演一位专业的UI/UX设计师。我正在设计一个PowerPoint演示文稿的内容页。

已知信息：
- 页面类型：内容页 (Content Slide)
- **内容页**背景颜色：RGB{}
- **封面页**已使用的文字颜色（供参考）：
    - 封面主标题颜色：RGB{}
    - 封面内容/副标题颜色：RGB{}
- 演示文稿主题：教育

需求：
请为这个**内容页**推荐两种文字颜色：
1.  **页面标题 (Page Title) 颜色**：需要清晰、易读，与背景对比良好，并与整体风格和封面标题颜色协调。
2.  **正文文本 (Body Text) 颜色**：这是最重要的颜色。必须与背景形成**极佳的对比度**，确保长时间阅读的清晰度和舒适性。

请确保颜色搭配协调、专业，并与封面页颜色形成视觉上的联系（但需优先保证内容页，特别是正文的可读性）。

**输出格式要求（请严格遵守）：**
请使用json格式返回，切勿输出json格式外的内容。格式如下：
{{
  "pageTitleColor": [R, G, B],
  "bodyTextColor": [R, G, B]
}}/no_think"""

theme_palette_prompt_template_cn = """请扮演一位专业的UI/UX和品牌形象设计师。我正在创建一个PowerPoint演示文稿，需要一个协调的色彩主题。

已知信息：
- 主要演示文稿背景颜色：{}
- 演示文稿标题字体颜色：{}
- 演示文稿内容字体颜色：{}
- 演示文稿主题：{}

需求：
请生成一个包含以下颜色角色的调色板。每种颜色都应独特且能良好搭配。请确保在涉及文本时有良好的对比度。

1.  **primary_accent (主强调色)**：一种强烈、引人注目的颜色，用于主要高光、行动号召和重要的视觉元素。应与主要演示文稿背景形成良好对比。
2.  **secondary_accent (次要强调色)**：一种与主强调色不同的互补强调色。可用于次要高光、图表或区分元素。
3.  **light_background (浅色背景元素)**：一种浅色 (例如，非常浅的灰色、米白色或强调色的浅色变体)，用作特定元素（如引用框或某些标注框）的背景，特别是当主幻灯片背景也是浅色时。它应确保 `dark_text` 在其上清晰可读。
4.  **dark_text (深色文本)**：一种非常深的颜色 (例如，非常深的灰色、近黑色或强调色的深色变体)，用于浅色背景（如上述 `light_background` 或浅色幻灯片背景）上的主要正文文本。
5.  **light_text (浅色文本)**：一种非常浅的颜色 (例如，白色、非常浅的灰色或强调色的浅色调)，用于深色背景（例如，如果 `primary_accent` 是深色并用作背景，或在深色幻灯片背景上）上的文本。
6.  **quote_border (引用边框色)**：一种中性或略微去饱和的颜色 (例如，灰色、去饱和的蓝色/绿色)，适用于引用框的边框或细分隔线。
7.  **data_callout_bg (数据标注背景色)**：数据标注框的背景颜色。此颜色应使数据（可能使用 `primary_accent` 或适当的文本颜色显示统计数字）突出。它应与用于数据统计的文本颜色形成良好对比。

输出格式要求 (请严格遵守此JSON格式。不要在JSON结构之外包含任何解释性文本)：
{{
  "primary_accent": [R, G, B],
  "secondary_accent": [R, G, B],
  "light_background": [R, G, B],
  "dark_text": [R, G, B],
  "light_text": [R, G, B],
  "quote_border": [R, G, B],
  "data_callout_bg": [R, G, B]
}}
/no_think"""
class ColorAgent:
    def __init__(self):
        self.config = get_args_parser()
        self.LLM = OpenAI(
            api_key=self.config.OPENAI_API_KEY,
            base_url=self.config.OPENAI_BASE_URL)
        self.model = self.config.model

        self.cover_title_color: Optional[List[int]] = None
        self.cover_content_color: Optional[List[int]] = None
        self.content_title_color: Optional[List[int]] = None
        self.content_content_color: Optional[List[int]] = None

    def _format_rgb_for_prompt(self, rgb: List[int]) -> str:
        """将 RGB 列表格式化为 '(R, G, B)' 字符串，用于插入提示。"""
        if isinstance(rgb, (list, tuple)) and len(rgb) == 3 and all(isinstance(c, int) for c in rgb):
            return f"[{rgb[0]}, {rgb[1]}, {rgb[2]}]"
        else:
            raise ValueError(f"无效的 RGB 格式提供给 _format_rgb_for_prompt: {rgb}")

    def __call__(self, rgb, title=False, other_color=False, abs=None):
        bg_color_str = self._format_rgb_for_prompt(rgb)

        if other_color is False:
            if title is True:
                prompt_template = title_color_prompt
                agent_prompt = prompt_template.format(bg_color_str)
            elif title is False:
                prompt_template = content_color_prompt
                agent_prompt = prompt_template.format(bg_color_str, self.cover_title_color, self.cover_content_color)
        if other_color is True and abs is not None:
            prompt_template = theme_palette_prompt_template_cn
            agent_prompt = prompt_template.format(bg_color_str, self.content_title_color, self.content_content_color, abs)

        for i in range(3):
            try:
                create_outline = {"role": "user",
                                  "content": agent_prompt}
                response = self.LLM.chat.completions.create(
                    model=self.model,
                    messages=[create_outline],
                    temperature=0,
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

                # 使用 json.loads() 安全地解析 JSON
                parsed_content = json.loads(raw_content)
                if other_color is False:
                    if title:
                        self.cover_title_color = parsed_content["titleColor"]
                        self.cover_content_color = parsed_content["contentColor"]

                        title_result = RGBColor(self.cover_title_color[0], self.cover_title_color[1], self.cover_title_color[2])
                        content_result = RGBColor(self.cover_content_color[0], self.cover_content_color[1], self.cover_content_color[2])
                        return [title_result, content_result]
                    else:
                        self.content_title_color = parsed_content["pageTitleColor"]
                        self.content_content_color = parsed_content["bodyTextColor"]
                        page_title_result = RGBColor(self.content_title_color[0], self.content_title_color[1], self.content_title_color[2])
                        body_text_result = RGBColor(self.content_content_color[0], self.content_content_color[1], self.content_content_color[2])
                        return [page_title_result, body_text_result]

                if other_color is True and abs is not None:
                    return self.convert_to_rgbcolor(parsed_content)

            except (KeyError, Exception) as e:  # 捕获特定错误 + 通用后备
                print(f"尝试 {i+1} 失败: {e}")
                if i < 2:  # 最后一次尝试后不睡眠
                    time.sleep(1)  # 重试前等待1秒
                continue  # 进入循环的下一次迭代


    def convert_to_rgbcolor(self,color_dict):
      """
      将包含 RGB 列表的字典转换为包含 RGBColor 对象的字典。

      参数:
        color_dict (dict): 一个字典，键是颜色名称 (字符串)，
                           值是包含三个整数 [R, G, B] 的列表。

      返回:
        dict: 一个新的字典，键与输入字典相同，
              值是相应的 RGBColor 对象。
      """
      rgb_color_objects = {}
      for color_name, rgb_values in color_dict.items():
        if isinstance(rgb_values, list) and len(rgb_values) == 3:
          r, g, b = rgb_values
          rgb_color_objects[color_name] = RGBColor(r, g, b)
        else:
          # 如果值不是预期的格式，可以选择抛出错误或跳过
          print(f"警告：跳过 '{color_name}'，因为其值 '{rgb_values}' 不是有效的 RGB 列表。")
      return rgb_color_objects