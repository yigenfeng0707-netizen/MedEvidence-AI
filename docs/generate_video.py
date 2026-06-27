"""
MedEvidence AI - 电影级演示视频自动生成器

功能：
1. Edge TTS 生成专业AI配音
2. Pillow 渲染电影级画面帧
3. MoviePy 合成视频+音频+字幕
4. 输出 1920x1080 30fps 超高清 MP4

运行：python generate_video.py
"""

import asyncio
import os
import sys
import time
import math
from pathlib import Path

# ============================================================
# 配置
# ============================================================
WIDTH = 1920
HEIGHT = 1080
FPS = 30
OUTPUT_DIR = Path(__file__).parent / "video_output"
FRAMES_DIR = OUTPUT_DIR / "frames"
AUDIO_DIR = OUTPUT_DIR / "audio"
FINAL_VIDEO = OUTPUT_DIR / "MedEvidence_AI_Demo.mp4"

# 配色
C_BG_DARK = (15, 23, 42)        # #0F172A
C_BG_CARD = (30, 41, 59)        # #1E293B
C_PRIMARY = (37, 99, 235)       # #2563EB
C_PRIMARY_LIGHT = (96, 165, 250) # #60A5FA
C_ACCENT = (6, 182, 212)        # #06B6D4
C_TEXT = (248, 250, 252)        # #F8FAFC
C_TEXT_SEC = (148, 163, 184)    # #94A3B8
C_LEVEL1 = (5, 150, 105)        # #059669
C_LEVEL2 = (16, 185, 129)       # #10B981
C_LEVEL3 = (245, 158, 11)       # #F59E0B
C_LEVEL4 = (249, 115, 22)       # #F97316
C_LEVEL5 = (239, 68, 68)        # #EF4444
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_GOLD = (251, 191, 36)         # #FBBF24

# TTS 语音配置
TTS_VOICE = "zh-CN-YunxiNeural"  # 沉稳男声
TTS_RATE = "-5%"
TTS_VOLUME = "+0%"
TTS_PITCH = "+0Hz"

# ============================================================
# 场景定义
# ============================================================

SCENES = [
    {
        "id": "logo",
        "duration": 4.0,
        "narration": "医学研究，证据为基。MedEvidence AI，你的循证医学智能检索助手。",
        "subtitles": [
            (0.0, 3.5, "医学研究，证据为基。"),
            (3.5, 7.0, "MedEvidence AI，你的循证医学智能检索助手。"),
        ],
    },
    {
        "id": "pain_points",
        "duration": 6.0,
        "narration": "临床决策需要循证依据。但面对海量医学文献，证据等级如何划分？中英文文献如何快速检索？高质量研究在哪里？",
        "subtitles": [
            (0.0, 2.5, "临床决策需要循证依据。"),
            (2.5, 4.5, "证据等级如何划分？"),
            (4.5, 6.5, "中英文文献如何快速检索？"),
            (6.5, 8.5, "高质量研究在哪里？"),
        ],
    },
    {
        "id": "product_intro",
        "duration": 5.0,
        "narration": "MedEvidence AI，基于KnowS医学循证数据库与StepFun大模型，提供中英文双语文献智能检索、五级循证分级标注、AI生成临床摘要的一站式服务。",
        "subtitles": [
            (0.0, 3.0, "MedEvidence AI"),
            (3.0, 5.5, "中英文双语文献智能检索"),
            (5.5, 7.5, "五级循证分级标注"),
            (7.5, 9.5, "AI生成临床摘要"),
        ],
    },
    {
        "id": "chinese_search",
        "duration": 10.0,
        "narration": "我们来试试中文检索。输入Meta分析抗生素，系统自动调用中文文献数据库，返回最相关的研究结果。可以看到，五篇结果全部被准确识别为Level 1，Meta分析或系统评价，这是循证医学中最高等级的证据。",
        "subtitles": [
            (0.0, 2.0, "我们来试试中文检索。"),
            (2.0, 4.0, "输入 'Meta分析 抗生素'"),
            (4.0, 6.0, "系统自动调用中文文献数据库"),
            (6.0, 8.0, "五篇结果全部为 Level 1 - Meta分析"),
            (8.0, 10.0, "循证医学最高等级证据"),
        ],
    },
    {
        "id": "english_search",
        "duration": 8.0,
        "narration": "英文检索同样精准。搜索COVID-19 vaccine randomized trial，系统返回多篇高质量随机对照试验，全部标注为Level 1。每篇文献都包含期刊名称、影响因子、DOI等完整信息。",
        "subtitles": [
            (0.0, 2.0, "英文检索同样精准。"),
            (2.0, 4.0, "搜索 COVID-19 vaccine randomized trial"),
            (4.0, 6.0, "全部标注 Level 1 - 随机对照试验"),
            (6.0, 8.0, "期刊·影响因子·DOI·发表日期"),
        ],
    },
    {
        "id": "evidence_pyramid",
        "duration": 7.0,
        "narration": "什么是五级循证分级？从Level 5的个案报道和专家意见，到Level 4的病例系列与临床指南，Level 3的队列研究，Level 2的低质量RCT，以及最高等级Level 1，Meta分析与高质量RCT。证据等级越高，研究结果越可靠。",
        "subtitles": [
            (0.0, 2.0, "什么是五级循证分级？"),
            (2.0, 3.5, "Level 5: 个案报道/专家意见"),
            (3.5, 4.5, "Level 4: 病例系列/指南"),
            (4.5, 5.5, "Level 3: 队列研究/病例对照"),
            (5.5, 6.5, "Level 2: 低质量RCT"),
            (6.5, 8.0, "Level 1: Meta分析/高质量RCT 金标准"),
            (8.0, 10.0, "证据等级越高，研究结果越可靠"),
        ],
    },
    {
        "id": "architecture",
        "duration": 6.0,
        "narration": "技术层面，MedEvidence AI基于FastAPI构建，深度集成KnowS医学循证数据库与StepFun大语言模型。支持魔搭创空间一键部署、Docker容器化部署，也可本地运行，代码完全开源。",
        "subtitles": [
            (0.0, 2.5, "FastAPI + KnowS + StepFun"),
            (2.5, 4.5, "魔搭创空间一键部署"),
            (4.5, 6.0, "Docker 容器化部署"),
            (6.0, 8.0, "代码完全开源 Apache 2.0"),
        ],
    },
    {
        "id": "compliance",
        "duration": 5.0,
        "narration": "我们高度重视医疗安全与合规。本工具不使用真实患者数据，不提供诊断建议，仅供医学研究与学习参考。临床决策请遵医嘱。",
        "subtitles": [
            (0.0, 2.0, "我们高度重视医疗安全与合规。"),
            (2.0, 4.0, "不使用真实患者数据"),
            (4.0, 5.5, "不提供诊断建议"),
            (5.5, 7.0, "仅供医学研究参考"),
            (7.0, 8.5, "临床决策请遵医嘱"),
        ],
    },
    {
        "id": "ending",
        "duration": 5.0,
        "narration": "MedEvidence AI，用AI照亮医学研究的每一个角落。立即体验，开启你的智能循证之旅。",
        "subtitles": [
            (0.0, 3.0, "用AI照亮医学研究的每一个角落"),
            (3.0, 5.5, "立即体验 MedEvidence AI"),
        ],
    },
]


# ============================================================
# 工具函数
# ============================================================

def lerp_color(c1, c2, t):
    """颜色线性插值"""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t):
    return 4 * t * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def draw_gradient_bg(img, c_top, c_bottom):
    """绘制垂直渐变背景"""
    import numpy as np
    arr = img.load()
    w, h = img.size
    for y in range(h):
        t = y / h
        c = lerp_color(c_top, c_bottom, t)
        for x in range(w):
            arr[x, y] = c


def draw_gradient_bg_fast(img, c_top, c_bottom):
    """快速渐变背景（numpy）"""
    import numpy as np
    w, h = img.size
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        t = y / h
        c = lerp_color(c_top, c_bottom, t)
        arr[y, :] = c
    from PIL import Image as PILImage
    return PILImage.fromarray(arr)


def draw_grid_overlay(img, spacing=40, alpha=8):
    """绘制网格叠加层"""
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=(255, 255, 255, alpha), width=1)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=(255, 255, 255, alpha), width=1)


def draw_glow_circle(img, cx, cy, radius, color, blur=60):
    """绘制发光圆"""
    from PIL import ImageDraw, ImageFilter
    glow = Image.new('RGBA', (radius * 4, radius * 4), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    draw.ellipse(
        [radius * 2 - radius, radius * 2 - radius,
         radius * 2 + radius, radius * 2 + radius],
        fill=(*color, 80)
    )
    glow = glow.filter(ImageFilter.GaussianBlur(blur))
    img.paste(glow, (cx - radius * 2, cy - radius * 2), glow)


def draw_rounded_rect(draw, xy, fill, radius=12, outline=None, width=1):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_text_center(draw, text, y, font, fill, img_width=WIDTH):
    """居中绘制文字"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (img_width - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_text_with_shadow(draw, text, x, y, font, fill, shadow_color=(0, 0, 0), shadow_offset=3):
    """带阴影的文字"""
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)


def draw_text_center_shadow(draw, text, y, font, fill, img_width=WIDTH):
    """居中带阴影文字"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (img_width - tw) // 2
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=fill)


def draw_particles(img, count=30, seed=42):
    """绘制粒子效果"""
    from PIL import ImageDraw
    import random
    random.seed(seed)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for _ in range(count):
        x = random.randint(0, w)
        y = random.randint(0, h)
        size = random.randint(1, 3)
        alpha = random.randint(30, 120)
        draw.ellipse([x, y, x + size, y + size], fill=(96, 165, 250, alpha))


def draw_loading_spinner(draw, cx, cy, radius, progress, color=C_PRIMARY_LIGHT):
    """绘制加载旋转器"""
    import math
    start_angle = progress * 360
    end_angle = start_angle + 270
    draw.arc(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        start=start_angle, end=end_angle,
        fill=color, width=4
    )


def draw_level_badge(draw, x, y, level, text, font_small):
    """绘制证据等级标签"""
    colors = {
        1: C_LEVEL1, 2: C_LEVEL2, 3: C_LEVEL3, 4: C_LEVEL4, 5: C_LEVEL5
    }
    c = colors.get(level, C_TEXT_SEC)
    bbox = draw.textbbox((0, 0), text, font=font_small)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    padding = 8
    draw_rounded_rect(draw, (x, y, x + tw + padding * 2, y + th + padding * 2),
                      fill=(*c, 40), radius=6)
    draw.text((x + padding, y + padding), text, font=font_small, fill=c)


# ============================================================
# 字体加载
# ============================================================

def load_fonts():
    """加载字体"""
    from PIL import ImageFont
    
    font_paths = {
        "title_large": "C:/Windows/Fonts/msyhbd.ttc",   # 微软雅黑粗体
        "title": "C:/Windows/Fonts/msyhbd.ttc",
        "body": "C:/Windows/Fonts/msyh.ttc",
        "body_bold": "C:/Windows/Fonts/msyhbd.ttc",
        "mono": "C:/Windows/Fonts/consola.ttf",
        "emoji_fallback": "C:/Windows/Fonts/seguisym.ttf",
    }
    
    fonts = {}
    sizes = {
        "title_large": 72,
        "title": 48,
        "subtitle": 32,
        "body": 24,
        "body_bold": 24,
        "body_large": 28,
        "small": 18,
        "tiny": 14,
        "mono": 16,
        "mono_large": 20,
    }
    
    for name, size in sizes.items():
        if "title" in name:
            path_key = "title_large"
        elif "body_bold" in name:
            path_key = "body_bold"
        elif "body" in name:
            path_key = "body"
        elif "mono" in name:
            path_key = "mono"
        else:
            path_key = "body"
        path = font_paths.get(path_key, "C:/Windows/Fonts/msyh.ttc")
        try:
            fonts[name] = ImageFont.truetype(path, size)
        except:
            fonts[name] = ImageFont.load_default()
    
    # 特殊大小
    try:
        fonts["logo"] = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 84)
    except:
        fonts["logo"] = fonts["title_large"]
    
    try:
        fonts["logo_sub"] = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
    except:
        fonts["logo_sub"] = fonts["subtitle"]
    
    return fonts


# ============================================================
# 场景渲染器
# ============================================================

class SceneRenderer:
    def __init__(self, fonts):
        self.fonts = fonts
    
    def render_frame(self, scene_id, progress, frame_in_scene, total_frames_in_scene):
        """渲染单个帧"""
        from PIL import Image
        img = Image.new('RGB', (WIDTH, HEIGHT), C_BG_DARK)
        
        renderer = getattr(self, f"_render_{scene_id}", None)
        if renderer:
            renderer(img, progress, frame_in_scene, total_frames_in_scene)
        else:
            self._render_default(img, scene_id, progress)
        
        return img
    
    def _render_logo(self, img, progress, frame, total):
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # 渐变背景
        bg = draw_gradient_bg_fast(img, (10, 15, 35), (15, 23, 50))
        img.paste(bg)
        
        # 粒子
        draw_particles(img, count=40, seed=1)
        
        # Logo文字 - 缩放动画
        scale = ease_out_cubic(min(progress * 2, 1.0))
        logo_text = "MedEvidence AI"
        bbox = draw.textbbox((0, 0), logo_text, font=self.fonts["logo"])
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        cx = WIDTH // 2
        cy = HEIGHT // 2 - 30
        
        # 渐变文字效果（模拟）
        for offset in range(3):
            alpha = 255 - offset * 60
            color = lerp_color(C_PRIMARY_LIGHT, C_ACCENT, offset / 3)
            draw.text((cx - tw // 2 + offset, cy - th // 2 + offset),
                     logo_text, font=self.fonts["logo"], fill=color)
        
        # 副标题
        sub_alpha = ease_out_cubic(max(0, min((progress - 0.3) * 3, 1.0)))
        if sub_alpha > 0:
            sub_text = "医学循证智能检索助手"
            bbox2 = draw.textbbox((0, 0), sub_text, font=self.fonts["logo_sub"])
            tw2 = bbox2[2] - bbox2[0]
            draw.text(((WIDTH - tw2) // 2, cy + 60),
                     sub_text, font=self.fonts["logo_sub"],
                     fill=lerp_color(C_TEXT_SEC, C_TEXT, sub_alpha))
        
        # 标语
        tag_alpha = ease_out_cubic(max(0, min((progress - 0.5) * 3, 1.0)))
        if tag_alpha > 0:
            tag_text = "用 AI 照亮医学研究的每一个角落"
            bbox3 = draw.textbbox((0, 0), tag_text, font=self.fonts["body"])
            tw3 = bbox3[2] - bbox3[0]
            draw.text(((WIDTH - tw3) // 2, cy + 110),
                     tag_text, font=self.fonts["body"],
                     fill=lerp_color(C_TEXT_SEC, (180, 190, 210), tag_alpha))
    
    def _render_pain_points(self, img, progress, frame, total):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        bg = draw_gradient_bg_fast(img, (12, 18, 38), (18, 26, 48))
        img.paste(bg)
        
        # 标题
        title = "医学文献检索，是否也有这些困扰？"
        draw_text_center_shadow(draw, title, 80, self.fonts["title"], C_TEXT)
        
        # 痛点卡片
        pains = [
            ("📚", "一篇指南几百篇参考文献，从何读起？"),
            ("🔬", "Meta分析、RCT、队列研究，证据等级怎么分？"),
            ("🌐", "中英文数据库来回切换，检索效率太低！"),
        ]
        
        for i, (icon, text) in enumerate(pains):
            delay = i * 0.2
            card_progress = ease_out_cubic(max(0, min((progress - delay - 0.1) * 3, 1.0)))
            if card_progress <= 0:
                continue
            
            y = 220 + i * 140
            card_x = 200
            card_w = WIDTH - 400
            card_h = 110
            
            # 卡片背景
            alpha = int(200 * card_progress)
            draw_rounded_rect(draw, (card_x, y, card_x + card_w, y + card_h),
                            fill=(30, 41, 59), radius=16)
            
            # 图标区域
            draw_rounded_rect(draw, (card_x + 20, y + 20, card_x + 80, y + 90),
                            fill=(239, 68, 68, 30), radius=12)
            draw.text((card_x + 32, y + 32), icon, font=self.fonts["title"], fill=C_TEXT)
            
            # 文字
            draw.text((card_x + 100, y + 38), text, font=self.fonts["body_large"], fill=C_TEXT)
    
    def _render_product_intro(self, img, progress, frame, total):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        bg = draw_gradient_bg_fast(img, (10, 15, 35), (15, 23, 48))
        img.paste(bg)
        
        # 产品名
        draw_text_center_shadow(draw, "MedEvidence AI", 60, self.fonts["logo"], C_PRIMARY_LIGHT)
        
        # 副标题
        draw_text_center_shadow(draw, "一站式医学循证智能检索平台", 160, self.fonts["subtitle"], C_TEXT_SEC)
        
        # 三个功能卡片
        features = [
            ("🔍", "智能检索", "中英文双语检索\n自然语言输入\n精准匹配相关文献"),
            ("🏆", "循证分级", "五级证据等级体系\n自动识别研究类型\n快速定位金标准"),
            ("✨", "AI 摘要", "StepFun 大模型生成\n中文临床要点摘要\n高效获取核心结论"),
        ]
        
        card_w = 380
        card_h = 320
        gap = 40
        start_x = (WIDTH - card_w * 3 - gap * 2) // 2
        card_y = 250
        
        for i, (icon, name, desc) in enumerate(features):
            delay = i * 0.15
            cp = ease_out_cubic(max(0, min((progress - delay - 0.1) * 3, 1.0)))
            if cp <= 0:
                continue
            
            x = start_x + i * (card_w + gap)
            
            # 卡片
            draw_rounded_rect(draw, (x, card_y, x + card_w, card_y + card_h),
                            fill=(30, 41, 59), radius=20)
            
            # 图标
            draw.text((x + card_w // 2 - 28, card_y + 30), icon,
                     font=self.fonts["title"], fill=C_TEXT)
            
            # 名称
            bbox = draw.textbbox((0, 0), name, font=self.fonts["body_bold"])
            tw = bbox[2] - bbox[0]
            draw.text((x + (card_w - tw) // 2, card_y + 110),
                     name, font=self.fonts["body_bold"], fill=C_TEXT)
            
            # 描述
            lines = desc.split('\n')
            for j, line in enumerate(lines):
                bbox2 = draw.textbbox((0, 0), line, font=self.fonts["body"])
                tw2 = bbox2[2] - bbox2[0]
                draw.text((x + (card_w - tw2) // 2, card_y + 160 + j * 35),
                         line, font=self.fonts["body"], fill=C_TEXT_SEC)
    
    def _render_chinese_search(self, img, progress, frame, total):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        bg = draw_gradient_bg_fast(img, (10, 15, 35), (15, 23, 48))
        img.paste(bg)
        
        # 标签
        tag_text = "🎯 中文检索演示"
        draw_text_center_shadow(draw, tag_text, 30, self.fonts["body"], C_PRIMARY_LIGHT)
        
        # 标题
        draw_text_center_shadow(draw, "Meta分析 · 抗生素", 75, self.fonts["title"], C_TEXT)
        
        # 搜索框
        search_y = 140
        search_x = 300
        search_w = WIDTH - 600
        search_h = 60
        draw_rounded_rect(draw, (search_x, search_y, search_x + search_w, search_y + search_h),
                        fill=(30, 41, 59), radius=30)
        draw.text((search_x + 20, search_y + 15), "Meta分析 抗生素",
                 font=self.fonts["body_large"], fill=C_TEXT)
        
        # 搜索按钮
        btn_x = search_x + search_w - 130
        draw_rounded_rect(draw, (btn_x, search_y + 5, btn_x + 120, search_y + 55),
                        fill=C_PRIMARY, radius=25)
        draw.text((btn_x + 35, search_y + 15), "检索",
                 font=self.fonts["body_bold"], fill=C_WHITE)
        
        # 结果卡片
        results = [
            ("Level 1 · Meta分析/系统评价", "抗生素对免疫检查点抑制剂治疗非小细胞肺癌疗效影响的Meta分析", "中国肺癌杂志 · 2023"),
            ("Level 1 · Meta分析/系统评价", "抗生素在种植治疗中的应用:早期种植失败的系统回顾和Meta分析", "J Dent Res · 2022"),
            ("Level 1 · Meta分析/系统评价", "单一及联合应用抗生素治疗呼吸机相关性肺炎效果Meta分析", "中华医院感染学杂志 · 2023"),
            ("Level 1 · Meta分析/系统评价", "抗生素人工骨治疗慢性骨髓炎疗效和安全性的Meta分析", "中国矫形外科杂志 · 2022"),
            ("Level 1 · Meta分析/系统评价", "围手术期抗生素预防假体关节感染效果的Meta分析", "中华骨科杂志 · 2023"),
        ]
        
        card_y = 220
        for i, (level, title, meta) in enumerate(results):
            delay = 0.3 + i * 0.12
            cp = ease_out_cubic(max(0, min((progress - delay) * 4, 1.0)))
            if cp <= 0:
                continue
            
            y = card_y + i * 130
            x = 200
            w = WIDTH - 400
            h = 110
            
            draw_rounded_rect(draw, (x, y, x + w, y + h),
                            fill=(30, 41, 59), radius=14)
            
            # 等级标签
            draw.text((x + 15, y + 12), level,
                     font=self.fonts["tiny"], fill=C_LEVEL1)
            
            # 标题
            draw.text((x + 15, y + 38), title[:50],
                     font=self.fonts["body"], fill=C_TEXT)
            
            # 元信息
            draw.text((x + 15, y + 72), meta,
                     font=self.fonts["tiny"], fill=C_TEXT_SEC)
        
        # 统计条
        if progress > 0.8:
            stat_y = card_y + len(results) * 130 + 20
            draw_rounded_rect(draw, (300, stat_y, WIDTH - 300, stat_y + 60),
                            fill=(30, 41, 59), radius=14)
            
            stats = [("5", "检索结果"), ("100%", "Level 1"), ("1.7s", "响应时间"), ("中", "文献语言")]
            stat_w = (WIDTH - 600) // 4
            for i, (val, label) in enumerate(stats):
                sx = 300 + i * stat_w + stat_w // 2
                draw_text_center(draw, val, stat_y + 8, self.fonts["title"], C_PRIMARY_LIGHT, WIDTH)
                draw_text_center(draw, label, stat_y + 38, self.fonts["tiny"], C_TEXT_SEC, WIDTH)
    
    def _render_english_search(self, img, progress, frame, total):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        bg = draw_gradient_bg_fast(img, (10, 15, 35), (15, 23, 48))
        img.paste(bg)
        
        draw_text_center_shadow(draw, "🌍 英文检索演示", 30, self.fonts["body"], C_PRIMARY_LIGHT)
        draw_text_center_shadow(draw, "COVID-19 Vaccine · Randomized Trial", 75, self.fonts["title"], C_TEXT)
        
        # 搜索框
        search_y = 140
        search_x = 200
        search_w = WIDTH - 400
        search_h = 60
        draw_rounded_rect(draw, (search_x, search_y, search_x + search_w, search_y + search_h),
                        fill=(30, 41, 59), radius=30)
        draw.text((search_x + 20, search_y + 15), "COVID-19 vaccine randomized trial",
                 font=self.fonts["body"], fill=C_TEXT)
        
        btn_x = search_x + search_w - 130
        draw_rounded_rect(draw, (btn_x, search_y + 5, btn_x + 120, search_y + 55),
                        fill=C_PRIMARY, radius=25)
        draw.text((btn_x + 25, search_y + 15), "Search",
                 font=self.fonts["body_bold"], fill=C_WHITE)
        
        # 结果
        results = [
            ("Level 1 · RCT", "Randomized Trial of BCG Vaccine to Protect against Covid-19", "NEJM · 2021 · IF:91.2"),
            ("Level 1 · RCT", "Effect of 2 Inactivated SARS-CoV-2 Vaccines on Symptomatic COVID-19", "JAMA · 2021 · IF:120.7"),
            ("Level 1 · RCT", "Efficacy of the adjuvanted subunit protein COVID-19 vaccine, SCB-2019", "The Lancet · 2021 · IF:168.9"),
            ("Level 1 · RCT", "Safety and Efficacy of the BNT162b2 mRNA Covid-19 Vaccine", "NEJM · 2020 · IF:91.2"),
            ("Level 1 · RCT", "Efficacy and Safety of the mRNA-1273 SARS-CoV-2 Vaccine", "NEJM · 2020 · IF:91.2"),
        ]
        
        card_y = 220
        for i, (level, title, meta) in enumerate(results):
            delay = 0.3 + i * 0.12
            cp = ease_out_cubic(max(0, min((progress - delay) * 4, 1.0)))
            if cp <= 0:
                continue
            
            y = card_y + i * 130
            x = 200
            w = WIDTH - 400
            h = 110
            
            draw_rounded_rect(draw, (x, y, x + w, y + h),
                            fill=(30, 41, 59), radius=14)
            draw.text((x + 15, y + 12), level, font=self.fonts["tiny"], fill=C_LEVEL1)
            draw.text((x + 15, y + 38), title[:55], font=self.fonts["body"], fill=C_TEXT)
            draw.text((x + 15, y + 72), meta, font=self.fonts["tiny"], fill=C_TEXT_SEC)
    
    def _render_evidence_pyramid(self, img, progress, frame, total):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        bg = draw_gradient_bg_fast(img, (10, 15, 35), (15, 23, 48))
        img.paste(bg)
        
        draw_text_center_shadow(draw, "五级循证证据金字塔", 40, self.fonts["title"], C_TEXT)
        draw_text_center_shadow(draw, "Evidence-Based Medicine Hierarchy", 100, self.fonts["body"], C_TEXT_SEC)
        
        levels = [
            (1, "Meta分析 · 系统评价 · 高质量RCT", "金标准", C_LEVEL1, 0.35),
            (2, "低质量随机对照试验", "", C_LEVEL2, 0.50),
            (3, "队列研究 · 病例对照研究", "", C_LEVEL3, 0.65),
            (4, "病例系列 · 临床指南 · 专家共识", "", C_LEVEL4, 0.80),
            (5, "个案报道 · 专家意见 · 基础研究", "", C_LEVEL5, 0.95),
        ]
        
        max_w = 900
        level_h = 55
        gap = 6
        start_y = 180
        center_x = WIDTH // 2
        
        for i, (lvl, name, tag, color, width_ratio) in enumerate(levels):
            delay = i * 0.12
            cp = ease_out_cubic(max(0, min((progress - delay - 0.1) * 4, 1.0)))
            if cp <= 0:
                continue
            
            w = int(max_w * width_ratio * cp)
            h = level_h
            y = start_y + i * (level_h + gap)
            x = center_x - w // 2
            
            # 层级背景
            fill_color = (*color, 30)
            draw_rounded_rect(draw, (x, y, x + w, y + h),
                            fill=(int(color[0] * 0.15), int(color[1] * 0.15), int(color[2] * 0.15)),
                            radius=10)
            
            # 等级编号
            draw.text((x + 15, y + 15), f"L{lvl}",
                     font=self.fonts["body_bold"], fill=color)
            
            # 名称
            draw.text((x + 60, y + 15), name,
                     font=self.fonts["body"], fill=color)
            
            # 标签
            if tag:
                draw.text((x + w - 80, y + 15), tag,
                         font=self.fonts["body_bold"], fill=C_GOLD)
        
        # 金标准说明
        if progress > 0.8:
            draw_text_center_shadow(draw, "⭐ 证据等级越高，研究结果越可靠",
                                   start_y + 5 * (level_h + gap) + 20,
                                   self.fonts["body"], C_GOLD)
    
    def _render_architecture(self, img, progress, frame, total):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        bg = draw_gradient_bg_fast(img, (10, 15, 35), (15, 23, 48))
        img.paste(bg)
        
        draw_text_center_shadow(draw, "技术架构", 40, self.fonts["title"], C_TEXT)
        draw_text_center_shadow(draw, "Modern, Scalable, Open Source", 100, self.fonts["body"], C_TEXT_SEC)
        
        blocks = [
            ("👨‍⚕️", "用户", "医生 / 医学生 / 研究者"),
            ("⚡", "MedEvidence AI", "FastAPI + Python"),
            ("📚", "KnowS API", "医学循证数据库"),
            ("🧠", "StepFun LLM", "大语言模型"),
        ]
        
        block_w = 280
        block_h = 160
        gap = 30
        start_x = (WIDTH - block_w * 4 - gap * 3) // 2
        block_y = 200
        
        for i, (icon, name, desc) in enumerate(blocks):
            delay = i * 0.15
            cp = ease_out_cubic(max(0, min((progress - delay - 0.1) * 3, 1.0)))
            if cp <= 0:
                continue
            
            x = start_x + i * (block_w + gap)
            
            draw_rounded_rect(draw, (x, block_y, x + block_w, block_y + block_h),
                            fill=(30, 41, 59), radius=16)
            
            draw.text((x + block_w // 2 - 25, block_y + 20), icon,
                     font=self.fonts["title"], fill=C_TEXT)
            bbox = draw.textbbox((0, 0), name, font=self.fonts["body_bold"])
            tw = bbox[2] - bbox[0]
            draw.text((x + (block_w - tw) // 2, block_y + 80),
                     name, font=self.fonts["body_bold"], fill=C_TEXT)
            bbox2 = draw.textbbox((0, 0), desc, font=self.fonts["body"])
            tw2 = bbox2[2] - bbox2[0]
            draw.text((x + (block_w - tw2) // 2, block_y + 115),
                     desc, font=self.fonts["body"], fill=C_TEXT_SEC)
            
            # 箭头
            if i < 3:
                arrow_x = x + block_w + gap // 2 - 15
                draw.text((arrow_x, block_y + 65), "→",
                         font=self.fonts["title"], fill=C_PRIMARY_LIGHT)
        
        # 部署方式
        if progress > 0.6:
            dep_y = block_y + block_h + 50
            tags = ["🚀 魔搭创空间一键部署", "🐳 Docker 容器化", "💻 本地运行"]
            tag_w = 300
            tag_start = (WIDTH - tag_w * 3 - 40 * 2) // 2
            for i, tag in enumerate(tags):
                tx = tag_start + i * (tag_w + 40)
                draw_rounded_rect(draw, (tx, dep_y, tx + tag_w, dep_y + 45),
                                fill=(37, 99, 235, 20), radius=10)
                bbox = draw.textbbox((0, 0), tag, font=self.fonts["body"])
                tw = bbox[2] - bbox[0]
                draw.text((tx + (tag_w - tw) // 2, dep_y + 10),
                         tag, font=self.fonts["body"], fill=C_PRIMARY_LIGHT)
        
        # 开源
        if progress > 0.8:
            draw_text_center_shadow(draw, "📜 Apache 2.0 开源许可 · 代码完全公开",
                                   dep_y + 70, self.fonts["body"], C_TEXT_SEC)
    
    def _render_compliance(self, img, progress, frame, total):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        bg = draw_gradient_bg_fast(img, (10, 15, 35), (15, 23, 48))
        img.paste(bg)
        
        # 盾牌
        draw_text_center_shadow(draw, "️", 60, self.fonts["logo"], C_TEXT)
        
        draw_text_center_shadow(draw, "医疗安全与合规", 160, self.fonts["title"], C_TEXT)
        draw_text_center_shadow(draw, "Medical Safety & Compliance", 220, self.fonts["body"], C_TEXT_SEC)
        
        items = [
            "不使用真实患者数据",
            "不提供诊断建议",
            "仅供医学研究与学习参考",
            "临床决策请遵医嘱",
        ]
        
        item_y = 310
        for i, text in enumerate(items):
            delay = i * 0.12
            cp = ease_out_cubic(max(0, min((progress - delay - 0.1) * 4, 1.0)))
            if cp <= 0:
                continue
            
            x = 400
            w = WIDTH - 800
            h = 65
            
            draw_rounded_rect(draw, (x, item_y + i * 85, x + w, item_y + i * 85 + h),
                            fill=(30, 41, 59), radius=14)
            
            # 勾选
            draw_rounded_rect(draw, (x + 15, item_y + i * 85 + 15, x + 50, item_y + i * 85 + 50),
                            fill=C_LEVEL1, radius=25)
            draw.text((x + 24, item_y + i * 85 + 20), "✓",
                     font=self.fonts["body_bold"], fill=C_WHITE)
            
            draw.text((x + 65, item_y + i * 85 + 20), text,
                     font=self.fonts["body_large"], fill=C_TEXT)
    
    def _render_ending(self, img, progress, frame, total):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        bg = draw_gradient_bg_fast(img, (10, 15, 35), (15, 23, 48))
        img.paste(bg)
        
        draw_particles(img, count=50, seed=99)
        
        # Logo
        draw_text_center_shadow(draw, "MedEvidence AI", 120, self.fonts["logo"], C_PRIMARY_LIGHT)
        
        # 标语
        draw_text_center_shadow(draw, "用 AI 照亮医学研究的每一个角落", 230, self.fonts["subtitle"], C_TEXT_SEC)
        
        # 链接
        links = [
            "modelscope.cn/studios/gsym236998/MedEvidence-AI",
            "github.com/yigenfeng0707-netizen/MedEvidence-AI",
        ]
        link_y = 380
        for i, link in enumerate(links):
            draw_text_center(draw, link, link_y + i * 45, self.fonts["mono"], C_PRIMARY_LIGHT)
        
        # CTA
        if progress > 0.5:
            draw_text_center_shadow(draw, "立即体验，开启你的智能循证之旅",
                                   link_y + 120, self.fonts["body_large"], C_ACCENT)
    
    def _render_default(self, img, scene_id, progress):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((100, 100), f"Scene: {scene_id}", font=self.fonts["body"], fill=C_TEXT)


# ============================================================
# TTS 音频生成
# ============================================================

async def generate_tts_audio(text, output_path, voice=TTS_VOICE, rate=TTS_RATE):
    """使用 Edge TTS 生成语音"""
    import edge_tts
    
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))
    print(f"  ✅ 音频生成: {output_path}")


async def generate_all_audio():
    """生成所有场景的配音"""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n🎙️  生成AI配音...")
    for i, scene in enumerate(SCENES):
        audio_path = AUDIO_DIR / f"scene_{i:02d}_{scene['id']}.mp3"
        if audio_path.exists():
            print(f"  ️  跳过 (已存在): {scene['id']}")
            continue
        
        print(f"  🎤 生成: {scene['id']}")
        await generate_tts_audio(scene["narration"], audio_path)
    
    print("✅ 所有音频生成完成\n")


# ============================================================
# 视频帧生成
# ============================================================

def generate_all_frames():
    """生成所有场景的视频帧"""
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    
    print("🎨 渲染视频帧...")
    fonts = load_fonts()
    renderer = SceneRenderer(fonts)
    
    total_frames = 0
    for i, scene in enumerate(SCENES):
        scene_frames = int(scene["duration"] * FPS)
        print(f"  🎬 场景 {i+1}/{len(SCENES)}: {scene['id']} ({scene_frames} 帧)")
        
        for f in range(scene_frames):
            progress = f / scene_frames
            frame = renderer.render_frame(scene["id"], progress, f, scene_frames)
            
            frame_path = FRAMES_DIR / f"frame_{total_frames:06d}.png"
            frame.save(str(frame_path), "PNG")
            total_frames += 1
    
    print(f"✅ 共生成 {total_frames} 帧\n")
    return total_frames


# ============================================================
# 字幕生成 (SRT)
# ============================================================

def generate_srt():
    """生成SRT字幕文件"""
    srt_path = OUTPUT_DIR / "subtitles.srt"
    
    print("📝 生成字幕文件...")
    
    lines = []
    subtitle_idx = 1
    current_time = 0.0
    
    for i, scene in enumerate(SCENES):
        scene_start = current_time
        for sub_start, sub_end, text in scene["subtitles"]:
            abs_start = scene_start + sub_start
            abs_end = scene_start + sub_end
            
            def fmt_time(t):
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = int(t % 60)
                ms = int((t % 1) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            
            lines.append(f"{subtitle_idx}")
            lines.append(f"{fmt_time(abs_start)} --> {fmt_time(abs_end)}")
            lines.append(text)
            lines.append("")
            subtitle_idx += 1
        
        current_time += scene["duration"]
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ 字幕文件: {srt_path} ({subtitle_idx - 1} 条)\n")
    return srt_path


# ============================================================
# 视频合成
# ============================================================

def compose_video(total_frames):
    """合成最终视频"""
    print("🎬 合成视频...")
    
    from moviepy import ImageSequenceClip, AudioFileClip
    import numpy as np
    
    # 1. 创建视频片段
    print("  📹 加载帧序列...")
    frame_files = sorted([str(f) for f in FRAMES_DIR.glob("frame_*.png")])
    
    video_duration = len(frame_files) / FPS
    clip = ImageSequenceClip(frame_files, fps=FPS)
    print(f"  ✅ 视频片段: {len(frame_files)} 帧, {video_duration:.1f}秒")
    
    # 2. 添加音频 - 使用 concatenate_audioclips 并截断到视频时长
    print("  🎵 合成音频...")
    audio_clips = []
    
    for i, scene in enumerate(SCENES):
        audio_path = AUDIO_DIR / f"scene_{i:02d}_{scene['id']}.mp3"
        if audio_path.exists():
            try:
                audio = AudioFileClip(str(audio_path))
                audio_clips.append(audio)
            except Exception as e:
                print(f"  ⚠️ 音频加载失败 {scene['id']}: {e}")
    
    if audio_clips:
        from moviepy import concatenate_audioclips
        final_audio = concatenate_audioclips(audio_clips)
        # 截断音频到视频时长
        if final_audio.duration > video_duration:
            final_audio = final_audio.subclipped(0, video_duration)
        clip = clip.with_audio(final_audio)
        print(f"  ✅ 音频已合成 ({len(audio_clips)} 个片段, {final_audio.duration:.1f}秒)")
    else:
        print("  ⚠️ 无音频片段")
    
    # 3. 导出 - 使用高码率确保画质
    print(f"  💾 导出视频: {FINAL_VIDEO}")
    clip.write_videofile(
        str(FINAL_VIDEO),
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        audio_bitrate='192k',
        bitrate='12000k',
        preset='medium',
        ffmpeg_params=['-crf', '18', '-maxrate', '15000k', '-bufsize', '20000k'],
        threads=4,
        logger='bar'
    )
    
    # 4. 清理临时文件
    for ac in audio_clips:
        ac.close()
    if audio_clips:
        final_audio.close()
    clip.close()
    
    # 5. 验证输出
    file_size = os.path.getsize(str(FINAL_VIDEO))
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"\n✅ 视频生成完成: {FINAL_VIDEO}")
    print(f"   分辨率: {WIDTH}x{HEIGHT}")
    print(f"   帧率: {FPS} fps")
    print(f"   时长: {video_duration:.1f} 秒")
    print(f"   文件大小: {file_size_mb:.1f} MB")


# ============================================================
# 主流程
# ============================================================

def main():
    print("=" * 60)
    print("🎬 MedEvidence AI - 电影级演示视频自动生成器")
    print("=" * 60)
    print(f"分辨率: {WIDTH}x{HEIGHT} | 帧率: {FPS}fps")
    print(f"场景数: {len(SCENES)} | 总时长: {sum(s['duration'] for s in SCENES):.1f}s")
    print()
    
    start_time = time.time()
    
    # 步骤1: 生成音频
    asyncio.run(generate_all_audio())
    
    # 步骤2: 生成帧
    total_frames = generate_all_frames()
    
    # 步骤3: 生成字幕
    generate_srt()
    
    # 步骤4: 合成视频
    compose_video(total_frames)
    
    elapsed = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"🎉 全部完成！耗时: {elapsed:.0f} 秒 ({elapsed/60:.1f} 分钟)")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f" 最终视频: {FINAL_VIDEO}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
