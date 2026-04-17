#!/usr/bin/env python3
"""
Universal Image Generator - User-Directed Workflow
通用图像生成向导 - 用户主导大方向，AI 补充细节，智能选 API
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

# 可用 API 配置
APIS = {
    'siliconflow': {
        'name': 'SiliconFlow (Kolors)',
        'models': ['Kwai-Kolors/Kolors', 'Qwen/Qwen-Image'],
        'default_model': 'Kwai-Kolors/Kolors',
        'best_for': ['写实', '人像', '产品', '自然场景'],
        'strengths': ['写实风格强', '皮肤质感好', '光影自然'],
    },
    'zhipu': {
        'name': '智谱 AI (CogView)',
        'models': ['cogview-3'],
        'default_model': 'cogview-3',
        'best_for': ['插画', '概念图', '中文提示词'],
        'strengths': ['中文理解好', '插画风格', '创意表达'],
    }
}


def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_section(title):
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print('─'*60)


def analyze_description(description: str) -> Dict:
    """分析用户描述，提取关键信息"""
    desc_lower = description.lower()
    
    # 检测风格倾向
    style_hints = {
        'realistic': ['写实', '真实', '照片', '摄影', 'photorealistic', 'realistic', 'photo'],
        'illustration': ['插画', '手绘', '绘画', 'illustration', 'painting', 'drawn'],
        'anime': ['动漫', '二次元', 'anime', 'manga', 'cartoon'],
        'cinematic': ['电影', ' cinematic', 'film', 'movie'],
        'concept': ['概念', '设计', 'concept', 'design'],
    }
    
    detected_styles = []
    for style, keywords in style_hints.items():
        if any(kw in desc_lower for kw in keywords):
            detected_styles.append(style)
    
    # 检测主体类型（简单启发式）
    subject_hints = {
        'person': ['人', '肖像', 'portrait', 'woman', 'man', 'girl', 'boy', 'person'],
        'vehicle': ['车', 'car', '汽车', '跑车', 'vehicle', 'bike'],
        'landscape': ['风景', '场景', 'landscape', 'city', 'mountain', 'forest'],
        'object': ['产品', '物品', 'product', 'object', 'item'],
    }
    
    detected_subjects = []
    for subj, keywords in subject_hints.items():
        if any(kw in desc_lower for kw in keywords):
            detected_subjects.append(subj)
    
    return {
        'styles': detected_styles,
        'subjects': detected_subjects,
        'has_chinese': any('\u4e00' <= c <= '\u9fff' for c in description),
    }


def ask_style_preference(detected: List[str]) -> str:
    """询问风格偏好"""
    print_section("风格选择")
    
    # 如果检测到了风格，询问是否确认
    if detected:
        print(f"从你的描述中检测到可能的风格: {', '.join(detected)}")
        confirm = input("确认这种风格吗？(y/n/其他) [y]: ").strip().lower()
        if confirm != 'n':
            return detected[0]
    
    # 让用户选择
    styles = [
        {'value': 'realistic', 'label': '写实/照片级', 'desc': '像照片一样真实'},
        {'value': 'illustration', 'label': '插画/手绘', 'desc': '艺术化、绘画感'},
        {'value': 'cinematic', 'label': '电影感', 'desc': '戏剧性光影、电影色调'},
        {'value': 'concept', 'label': '概念设计', 'desc': '设计图、概念艺术'},
        {'value': 'minimalist', 'label': '极简/干净', 'desc': '简洁、留白'},
    ]
    
    print("\n想要什么风格？")
    for i, s in enumerate(styles, 1):
        print(f"   {i}. {s['label']} - {s['desc']}")
    
    choice = input(f"\n选择 [1-{len(styles)}]: ").strip()
    try:
        return styles[int(choice)-1]['value']
    except:
        return 'realistic'


def ask_composition() -> Dict:
    """询问构图和氛围"""
    print_section("构图与氛围")
    
    # 视角
    angles = [
        {'value': 'close-up', 'label': '特写', 'desc': '聚焦细节'},
        {'value': 'medium', 'label': '中景', 'desc': '平衡主体和环境'},
        {'value': 'wide', 'label': '广角/全景', 'desc': '展现全貌'},
    ]
    
    print("视角？")
    for i, a in enumerate(angles, 1):
        print(f"   {i}. {a['label']} - {a['desc']}")
    angle_choice = input(f"选择 [1-{len(angles)}] (回车默认): ").strip()
    angle = angles[int(angle_choice)-1]['value'] if angle_choice.isdigit() else 'medium'
    
    # 氛围
    moods = [
        {'value': 'bright', 'label': '明亮/清新'},
        {'value': 'warm', 'label': '温暖/柔和'},
        {'value': 'cool', 'label': '冷峻/清爽'},
        {'value': 'dark', 'label': '暗调/神秘'},
        {'value': 'dramatic', 'label': '戏剧性/冲击'},
    ]
    
    print("\n整体氛围？")
    for i, m in enumerate(moods, 1):
        print(f"   {i}. {m['label']}")
    mood_choice = input(f"选择 [1-{len(moods)}] (回车默认): ").strip()
    mood = moods[int(mood_choice)-1]['value'] if mood_choice.isdigit() else 'balanced'
    
    return {'angle': angle, 'mood': mood}


def ask_must_haves() -> List[str]:
    """询问必需要素"""
    print_section("必需要素")
    print("有什么是你必须坚持的细节？（直接回车结束）")
    
    must_haves = []
    prompts = [
        "特定颜色或材质？",
        "必须出现的元素？",
        "特定的光线或时间？",
    ]
    
    for p in prompts:
        ans = input(f"   {p} ").strip()
        if ans:
            must_haves.append(ans)
    
    return must_haves


def collect_user_directions() -> Dict:
    """收集用户大方向"""
    print_header("🎨 图像生成向导")
    print("\n告诉我你想要什么，我会帮你完善细节并选择最适合的 API。\n")
    
    # 1. 自由描述
    print("第一步：自由描述")
    print("用任何方式描述你想要的图像，可以是具体的也可以是模糊的。")
    print("例如：'夕阳下的海边小镇'、'未来感机器人'、'一杯咖啡'\n")
    
    description = input("💭 描述: ").strip()
    if not description:
        print("❌ 需要描述")
        return None
    
    # 分析描述
    analysis = analyze_description(description)
    
    # 2. 风格确认
    style = ask_style_preference(analysis['styles'])
    
    # 3. 构图与氛围
    composition = ask_composition()
    
    # 4. 必需要素
    must_haves = ask_must_haves()
    
    # 5. 用途（影响 API 选择）
    print_section("用途")
    uses = [
        {'value': 'personal', 'label': '个人使用'},
        {'value': 'commercial', 'label': '商业/展示'},
        {'value': 'concept', 'label': '概念参考'},
    ]
    for i, u in enumerate(uses, 1):
        print(f"   {i}. {u['label']}")
    use_choice = input("主要用途？(回车默认个人): ").strip()
    use = uses[int(use_choice)-1]['value'] if use_choice.isdigit() else 'personal'
    
    return {
        'description': description,
        'style': style,
        'angle': composition['angle'],
        'mood': composition['mood'],
        'must_haves': must_haves,
        'use_case': use,
        'has_chinese': analysis['has_chinese'],
        'detected_subjects': analysis['subjects'],
    }


def ai_enhance(directions: Dict) -> Dict:
    """AI 根据用户大方向补充细节"""
    print_section("🤖 AI 细节补充")
    
    enhanced = directions.copy()
    details_added = []
    
    style = directions.get('style')
    mood = directions.get('mood')
    angle = directions.get('angle')
    
    # 根据风格添加质量词
    quality_by_style = {
        'realistic': 'photorealistic, highly detailed, 8k, professional photography',
        'illustration': 'digital illustration, artistic, clean lines, vibrant colors',
        'cinematic': 'cinematic lighting, color grading, film look, 8k',
        'concept': 'concept art, detailed, professional, game art style',
        'minimalist': 'minimalist, clean, negative space, modern aesthetic',
    }
    
    if style in quality_by_style:
        enhanced['quality'] = quality_by_style[style]
        details_added.append(f"画质: {style} 标准")
    
    # 根据氛围添加光线
    mood_lighting = {
        'bright': 'bright and airy, high key lighting, natural daylight',
        'warm': 'warm golden hour lighting, cozy atmosphere, soft shadows',
        'cool': 'cool tones, crisp lighting, blue hour',
        'dark': 'low key lighting, moody atmosphere, dramatic shadows',
        'dramatic': 'dramatic lighting, high contrast, strong shadows',
        'balanced': 'balanced lighting, natural illumination',
    }
    
    if mood in mood_lighting:
        enhanced['lighting'] = mood_lighting[mood]
        details_added.append(f"光线: {mood} 氛围")
    
    # 根据视角添加构图
    angle_shot = {
        'close-up': 'close-up shot, shallow depth of field, detail focus',
        'medium': 'medium shot, balanced composition',
        'wide': 'wide angle, expansive view, environmental context',
    }
    
    if angle in angle_shot:
        enhanced['shot'] = angle_shot[angle]
        details_added.append(f"构图: {angle} 视角")
    
    # 打印补充
    if details_added:
        print("AI 补充的细节:")
        for d in details_added:
            print(f"   ✓ {d}")
    
    return enhanced


def select_api(directions: Dict) -> Dict:
    """智能选择 API"""
    print_section("🔧 API 选择")
    
    scores = {'siliconflow': 0, 'zhipu': 0}
    reasons = {'siliconflow': [], 'zhipu': []}
    
    # 风格评分
    style = directions.get('style')
    if style == 'realistic':
        scores['siliconflow'] += 2
        reasons['siliconflow'].append("写实风格 Kolors 更强")
    elif style in ['illustration', 'concept']:
        scores['zhipu'] += 1
        reasons['zhipu'].append("插画/概念风格 CogView 适合")
    
    # 语言评分
    if directions.get('has_chinese'):
        scores['zhipu'] += 1
        reasons['zhipu'].append("中文提示词 CogView 理解更好")
    
    # 选择最佳
    best = max(scores, key=scores.get)
    
    print(f"推荐: {APIS[best]['name']}")
    print("理由:")
    for r in reasons[best]:
        print(f"   • {r}")
    
    # 用户确认或切换
    confirm = input(f"\n使用此 API？(y/n/手动选择) [y]: ").strip().lower()
    if confirm == 'n':
        best = 'zhipu' if best == 'siliconflow' else 'siliconflow'
        print(f"切换到: {APIS[best]['name']}")
    elif confirm == '手动选择':
        print("\n可用 API:")
        for i, (k, api) in enumerate(APIS.items(), 1):
            print(f"   {i}. {api['name']}")
            print(f"      擅长: {', '.join(api['best_for'])}")
        choice = input("选择: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(APIS):
            best = list(APIS.keys())[int(choice)-1]
    
    return {
        'api': best,
        'config': APIS[best],
    }


def build_prompt(directions: Dict) -> str:
    """构建最终提示词"""
    parts = [directions['description']]
    
    # 风格词
    if directions.get('shot'):
        parts.append(directions['shot'])
    if directions.get('lighting'):
        parts.append(directions['lighting'])
    
    # 必需要素
    if directions.get('must_haves'):
        parts.extend(directions['must_haves'])
    
    # 画质
    if directions.get('quality'):
        parts.append(directions['quality'])
    else:
        parts.append("high quality, detailed, 8k")
    
    return ", ".join(parts)


def generate(prompt: str, api_config: Dict, seed: int = None):
    """执行生成"""
    print_section("🚀 图像生成")
    print(f"API: {api_config['config']['name']}")
    print(f"模型: {api_config['config']['default_model']}")
    print(f"提示词: {prompt[:100]}...")
    print()
    
    import subprocess
    
    if api_config['api'] == 'siliconflow':
        cmd = [
            sys.executable,
            str(Path(__file__).parent / 'generate.py'),
            prompt
        ]
    else:
        cmd = [
            sys.executable,
            str(Path(__file__).parent / 'generate_zhipu.py'),
            prompt
        ]
    
    if seed:
        cmd.extend(['--seed', str(seed)])
    
    subprocess.run(cmd)


def interactive_mode():
    """主交互流程"""
    # 1. 收集用户大方向
    directions = collect_user_directions()
    if not directions:
        return
    
    # 确认
    print_section("📋 确认")
    print(f"描述: {directions['description']}")
    print(f"风格: {directions['style']}")
    print(f"视角: {directions['angle']}")
    print(f"氛围: {directions['mood']}")
    
    if input("\n确认继续？(y/n) [y]: ").strip().lower() == 'n':
        print("❌ 已取消")
        return
    
    # 2. AI 增强
    enhanced = ai_enhance(directions)
    
    # 3. 选择 API
    api_config = select_api(enhanced)
    
    # 4. 构建提示词
    final_prompt = build_prompt(enhanced)
    
    print_section("📋 最终提示词")
    print(final_prompt)
    print()
    
    # 5. 生成
    if input("🚀 立即生成？(y/n) [y]: ").strip().lower() != 'n':
        seed = input("随机种子 (回车随机): ").strip()
        seed = int(seed) if seed.isdigit() else None
        generate(final_prompt, api_config, seed)


def main():
    parser = argparse.ArgumentParser(description='Universal Image Generator')
    parser.add_argument('--quick', '-q', metavar='PROMPT', help='快速模式')
    
    args = parser.parse_args()
    
    if args.quick:
        # 快速模式：分析 + 自动选择 + 生成
        print_header("🚀 快速生成")
        # TODO: 实现快速模式
    else:
        interactive_mode()


if __name__ == '__main__':
    main()