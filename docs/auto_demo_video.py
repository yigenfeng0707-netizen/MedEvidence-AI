"""
MedEvidence AI - 演示视频自动生成脚本

使用方法：
1. 确保已安装：pip install selenium pillow
2. 安装Chrome浏览器和对应版本的ChromeDriver
3. 确保演示页面在本地服务器运行：python -m http.server 8765
4. 运行本脚本：python auto_demo_video.py

输出：
- frames/ 目录：每一帧的PNG截图
- demo_video_frames/ 目录：帧序列（可用ffmpeg合成视频）

注意：
- 本脚本只生成帧序列，最终视频建议用剪映等软件剪辑配音
- 如需直接生成视频，可安装ffmpeg后使用下方命令
"""

import os
import time
import shutil
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  selenium 未安装，跳过自动录屏功能")
    print("   安装命令：pip install selenium")

DEMO_URL = "http://localhost:8765/demo-video-page.html"
OUTPUT_DIR = Path(__file__).parent / "demo_video_frames"
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

# 每个场景的停留时间（秒）
SCENE_DURATIONS = [
    4.0,   # Scene 1: Logo片头
    5.0,   # Scene 2: 痛点引入（3个痛点）
    4.0,   # Scene 3: 产品亮相
    10.0,  # Scene 4: 中文检索演示（含加载动画）
    8.0,   # Scene 5: 英文检索演示
    6.0,   # Scene 6: 证据金字塔
    5.0,   # Scene 7: 技术架构
    4.0,   # Scene 8: 合规声明
    5.0,   # Scene 9: 结尾页
]

FPS = 30


def setup_driver():
    """配置Chrome浏览器"""
    chrome_options = Options()
    chrome_options.add_argument(f"--window-size={FRAME_WIDTH},{FRAME_HEIGHT + 120}")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=chrome_options)


def capture_scene_frames(driver, scene_idx, duration, fps=FPS):
    """捕获一个场景的所有帧"""
    num_frames = int(duration * fps)
    frames = []
    
    # 切换到指定场景
    driver.execute_script(f"showScene({scene_idx});")
    time.sleep(0.5)  # 等待动画开始
    
    for i in range(num_frames):
        frame_path = OUTPUT_DIR / f"scene{scene_idx+1:02d}_frame{i:04d}.png"
        driver.save_screenshot(str(frame_path))
        frames.append(frame_path)
        time.sleep(1.0 / fps)
    
    return frames


def generate_video_with_ffmpeg():
    """用ffmpeg合成视频（如果有ffmpeg的话）"""
    import subprocess
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-framerate", str(FPS),
        "-i", str(OUTPUT_DIR / "scene%02d_frame%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "slow",
        "medevidence_demo_no_audio.mp4"
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("✅ 视频生成成功：medevidence_demo_no_audio.mp4")
    except FileNotFoundError:
        print("ℹ️  未安装ffmpeg，已生成帧序列，可用剪映等软件导入合成")
    except Exception as e:
        print(f"⚠️  ffmpeg合成失败：{e}")
        print("   帧序列已保存在 demo_video_frames/ 目录")


def main():
    if not SELENIUM_AVAILABLE:
        print("\n📋 请按以下步骤手动录制：")
        print("1. 打开 demo-video-page.html")
        print("2. 按 F11 全屏")
        print("3. 用 OBS 或 剪映 录屏")
        print("4. 按方向键 → 切换场景")
        print("5. 参考 docs/VIDEO_PRODUCTION_GUIDE.md 进行后期制作")
        return
    
    print("🎬 MedEvidence AI 演示视频自动生成")
    print("=" * 50)
    
    # 准备输出目录
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    
    print(f"📁 帧输出目录：{OUTPUT_DIR}")
    print(f"🎞️  帧率：{FPS} fps")
    print(f"📐 分辨率：{FRAME_WIDTH}x{FRAME_HEIGHT}")
    
    total_duration = sum(SCENE_DURATIONS)
    total_frames = int(total_duration * FPS)
    print(f"⏱️  总时长：约 {total_duration:.1f} 秒 ({total_frames} 帧)")
    
    print("\n🚀 启动浏览器...")
    driver = setup_driver()
    
    try:
        print(f"🌐 打开演示页面：{DEMO_URL}")
        driver.get(DEMO_URL)
        time.sleep(2)  # 等待页面加载
        
        all_frames = []
        for idx, duration in enumerate(SCENE_DURATIONS):
            print(f"📹  录制场景 {idx+1}/{len(SCENE_DURATIONS)} ({duration:.1f}s)...")
            frames = capture_scene_frames(driver, idx, duration)
            all_frames.extend(frames)
        
        print(f"\n✅ 录制完成！共 {len(all_frames)} 帧")
        print(f"📂 帧文件在：{OUTPUT_DIR}")
        
        # 尝试用ffmpeg合成
        print("\n🎞️  尝试合成视频...")
        generate_video_with_ffmpeg()
        
    finally:
        driver.quit()
    
    print("\n" + "=" * 50)
    print("🎉 完成！")
    print("\n📝 下一步：")
    print("1. 用剪映打开帧序列/视频")
    print("2. 添加配音（参考 docs/VIDEO_SCRIPT.md）")
    print("3. 导入字幕 docs/subtitles_zh.srt")
    print("4. 添加背景音乐和音效")
    print("5. 导出最终视频")
    print("\n详细教程见 docs/VIDEO_PRODUCTION_GUIDE.md")


if __name__ == "__main__":
    main()
