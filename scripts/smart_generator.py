#!/usr/bin/env python3
"""
SiliconFlow Image Generator - User-Directed Workflow
用户主导大方向，AI 补充细节，智能选择 API
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

# API 配置
APIS = {
    'siliconflow': {
        'name': 'SiliconFlow (Kolors)',
        'endpoint': 'https://api.siliconflow.cn/v1/images/generations',
        'models': ['Kwai-Kolors/Kolors', 'Qwen/Qwen-Image'],
        'default_model': 'Kwai-Kolors/Kolors',
        'best_for': ['写实人像', '自然场景', '产品摄影'],
        'strengths': ['写实风格强', '皮肤质感好', '光线自然'],
        'env_key': 'SILICONFLOW_API_KEY',
    },
    'zhipu': {
        'name': '智谱 AI (CogView)',
        'endpoint': 'https://open.bigmodel.cn/api/paas/v4/images/generations',
        'models': ['cogview-3'],
        'default_model': 'cogview-3',
        'best_for': ['插画', '概念图', '中文提示词'],
        'strengths': ['中文理解好', '插画风格', '创意表达'],
        'env_key': 'ZHIPU_API_KEY',
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


def ask_choice(question: str, options: List[Dict], allow_skip: bool = True) -> Optional[str]:
    """Ask user to choose from options"""
    print(f"\n❓ {question}")
    for i, opt in enumerate(options, 1):
        desc = opt.get('desc', '')
        print(f"   {i}. {opt['label']}" + (f" - {desc}" if desc else ""))
    if allow_skip:
        print(f"   0. 跳过/不确定")
    
    while True:
        choice = input(f"\n选择 [1-{len(options)}]: ").strip()
        if choice == '0' and allow_skip:
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]['value']
        except:
            pass
        print("   请输入有效选项")


def ask_text(question: str, examples: List[str] = None) -> Optional[str]:
    """Ask free text input"""
    print(f"\n❓ {question}")
    if examples:
        print(f"   例如: {', '.join(examples)}")
    answer = input("> ").strip()
    return answer if answer else None


def collect_user_directions() -> Dict:
    """Step 1: Collect high-level directions from user"""
    print_header("🎨 图像生成向导 - 大方向设定")
    print("\n首先，请告诉我你想要的图像大方向。我会基于你的选择来完善细节。\n")
    
    directions = {}
    
    # 1. 图像类型
    image_types = [
        {'value': 'portrait', 'label': '人像/肖像', 'desc': '人物特写、头像、半身像'},
        {'value': 'character', 'label': '角色设计', 'desc': '游戏角色、概念设计、全身像'},
        {'value': 'scene', 'label': '场景/风景', 'desc': '城市、自然、室内环境'},
        {'value': 'product', 'label': '产品/物品', 'desc': '汽车、电子产品、静物'},
        {'value': 'artistic', 'label': '艺术创作', 'desc': '插画、抽象、艺术风格'},
    ]
    directions['type'] = ask_choice("你想要什么类型的图像？", image_types)
    
    # 2. 风格偏好
    styles = [
        {'value': 'realistic', 'label': '写实/照片级', 'desc': '像照片一样真实'},
        {'value': 'cinematic', 'label': '电影感', 'desc': '戏剧性光影、电影色调'},
        {'value': 'illustration', 'label': '插画/手绘', 'desc': '艺术化、绘画风格'},
        {'value': 'concept', 'label': '概念设计', 'desc': '游戏/电影概念艺术'},
        {'value': 'minimalist', 'label': '极简/干净', 'desc': '简洁、留白、现代'},
    ]
    directions['style'] = ask_choice("什么风格？", styles)
    
    # 3. 用途/场景
    use_cases = [
        {'value': 'avatar', 'label': '头像/个人资料', 'desc': '社交媒体、头像'},
        {'value': 'wallpaper', 'label': '壁纸/背景', 'desc': '桌面、手机壁纸'},
        {'value': 'concept', 'label': '概念参考', 'desc': '设计参考、灵感'},
        {'value': 'commercial', 'label': '商业/展示', 'desc': '产品展示、宣传'},
        {'value': 'creative', 'label': '创意表达', 'desc': '艺术创作、实验'},
    ]
    directions['use_case'] = ask_choice("主要用途是什么？", use_cases)
    
    # 4. 主体描述
    directions['subject'] = ask_text("请描述主体内容:", 
                                     ["一个年轻女性", "科幻城市", "红色跑车", "森林小屋"])
    
    # 5. 整体色调/氛围
    moods = [
        {'value': 'warm', 'label': '温暖/柔和', 'desc': '暖色调、舒适'},
        {'value': 'cool', 'label': '冷峻/清爽', 'desc': '冷色调、冷静'},
        {'value': 'dark', 'label': '暗调/神秘', 'desc': '低光、氛围感'},
        {'value': 'bright', 'label': '明亮/清新', 'desc': '高光、通透'},
        {'value': 'dramatic', 'label': '戏剧性', 'desc': '强烈对比、冲击'},
    ]
    directions['mood'] = ask_choice("整体氛围？", moods)
    
    # 6. 必需要素（用户坚持要的内容）
    print_section("必需要素")
    print("有什么是你**必须坚持**的要素？（直接回车跳过）")
    directions['must_haves'] = []
    
    must_ask = [
        "特定颜色？（如：必须红色）",
        "特定元素？（如：必须有翅膀）",
        "特定角度？（如：必须是侧脸）",
    ]
    for q in must_ask:
        ans = ask_text(q)
        if ans:
            directions['must_haves'].append(ans)
    
    return directions


def ai_enhance_details(directions: Dict) -> Dict:
    """Step 2: AI enhances details based on user directions"""
    print_section("🤖 AI 细节补充")
    print("基于你的选择，我来补充专业细节...\n")
    
    enhanced = directions.copy()
    details = []
    
        # 根据类型补充
    image_type = directions.get('type')
    
    if image_type == 'portrait':
        if not directions.get('facial_details'):
            enhanced['facial_details'] = "natural skin texture, realistic facial features"
            details.append("面部: 自然肤质、写实五官")
        
        if not directions.get('lighting'):
            if directions.get('mood') == 'warm':
                enhanced['lighting'] = "soft golden hour lighting, warm tones"
                details.append("光线: 黄金时刻暖光")
            elif directions.get('mood') == 'dramatic':
                enhanced['lighting'] = "dramatic side lighting, strong shadows"
                details.append("光线: 戏剧性侧光")
            else:
                enhanced['lighting'] = "soft natural lighting, even illumination"
                details.append("光线: 柔和自然光")
    
    elif image_type == 'product':
        enhanced['lighting'] = "professional studio lighting, soft shadows, reflections"
        enhanced['camera'] = "clean product photography, centered composition, sharp focus"
        enhanced['background'] = "clean gradient background, minimal distractions"
        details.append("布光: 专业摄影棚光线")
        details.append("构图: 产品摄影标准构图")
        details.append("背景: 简洁渐变背景")
    
    elif image_type == 'scene':
        if directions.get('mood') == 'cinematic':
            enhanced['camera'] = "wide angle, cinematic composition, depth of field"
            details.append("镜头: 广角电影构图")
        if not directions.get('lighting'):
            enhanced['lighting'] = "natural environmental lighting, atmospheric perspective"
            details.append("光线: 自然环境光")
        if directions.get('mood') == 'cinematic':
            enhanced['camera'] = "wide angle, cinematic composition, depth of field"
            details.append("镜头: 广角电影构图")
    
    # 根据风格补充
    style_quality = {
        'realistic': 'photorealistic, highly detailed, 8k, professional photography',
        'cinematic': 'cinematic lighting, color grading, anamorphic lens look, 8k',
        'illustration': 'digital illustration, artistic style, clean lines, vibrant colors',
        'concept': 'concept art, detailed, professional, game art style',
        'minimalist': 'minimalist, clean, negative space, modern aesthetic',
    }
    
    if directions.get('style') in style_quality:
        enhanced['quality'] = style_quality[directions['style']]
        details.append(f"画质: {directions['style']} 标准")
    
    # 打印补充的细节
    if details:
        print("AI 补充的细节:")
        for d in details:
            print(f"   ✓ {d}")
    else:
        print("用户描述已足够详细，无需补充")
    
    return enhanced


def select_api_and_model(directions: Dict) -> Dict:
    """Step 3: Select best API and model based on requirements"""
    print_section("🔧 API 选择")
    
    # 评分逻辑
    api_scores = {'siliconflow': 0, 'zhipu': 0}
    reasons = {'siliconflow': [], 'zhipu': []}
    
    # 根据风格评分
    if directions.get('style') == 'realistic':
        api_scores['siliconflow'] += 2
        reasons['siliconflow'].append("写实风格 Kolors 更强")
    elif directions.get('style') == 'illustration':
        api_scores['zhipu'] += 2
        reasons['zhipu'].append("插画风格 CogView 更好")
    
    # 根据语言评分
    subject = directions.get('subject', '')
    if any('\u4e00' <= c <= '\u9fff' for c in subject):
        api_scores['zhipu'] += 1
        reasons['zhipu'].append("中文提示词 CogView 理解更好")
    
    # 根据类型评分
    if directions.get('type') == 'portrait':
        api_scores['siliconflow'] += 1
        reasons['siliconflow'].append("人像生成 Kolors 更稳定")
    
    # 选择最高分
    best_api = max(api_scores, key=api_scores.get)
    
    print(f"推荐 API: {APIS[best_api]['name']}")
    print(f"理由:")
    for r in reasons[best_api]:
        print(f"   • {r}")
    
    # 用户确认
    confirm = input(f"\n使用此 API？(y/n/手动选择) [y]: ").strip().lower()
    
    if confirm == 'n':
        # 用户想要另一个
        best_api = 'zhipu' if best_api == 'siliconflow' else 'siliconflow'
        print(f"切换到: {APIS[best_api]['name']}")
    elif confirm == '手动选择':
        print("\n可用 API:")
        for i, (key, api) in enumerate(APIS.items(), 1):
            print(f"   {i}. {api['name']} - 擅长: {', '.join(api['best_for'])}")
        choice = input("选择: ").strip()
        best_api = list(APIS.keys())[int(choice)-1] if choice.isdigit() else best_api
    
    return {
        'api': best_api,
        'api_config': APIS[best_api],
    }


def build_final_prompt(directions: Dict) -> str:
    """Build the final prompt from all components - type aware"""
    parts = []
    image_type = directions.get('type')
    
    # 主体（ always include ）
    if directions.get('subject'):
        parts.append(directions['subject'])
    
    # 风格词
    if directions.get('style') == 'realistic':
        parts.append("photorealistic")
    elif directions.get('style') == 'cinematic':
        parts.append("cinematic")
    elif directions.get('style') == 'illustration':
        parts.append("digital illustration")
    elif directions.get('style') == 'concept':
        parts.append("concept art")
    elif directions.get('style') == 'minimalist':
        parts.append("minimalist, clean composition")
    
    # 类型特定的细节（只添加相关类型的细节）
    if image_type == 'portrait':
        if directions.get('facial_details'):
            parts.append(directions['facial_details'])
    
    # 通用细节
    if directions.get('lighting'):
        parts.append(directions['lighting'])
    if directions.get('camera'):
        parts.append(directions['camera'])
    if directions.get('background'):
        parts.append(directions['background'])
    
    # 氛围
    mood_map = {
        'warm': 'warm tones, cozy atmosphere',
        'cool': 'cool tones, crisp atmosphere', 
        'dark': 'dark moody atmosphere, low key',
        'bright': 'bright and airy, high key',
        'dramatic': 'dramatic atmosphere, high contrast'
    }
    if directions.get('mood') in mood_map:
        parts.append(mood_map[directions['mood']])
    
    # 必需要素
    if directions.get('must_haves'):
        parts.extend(directions['must_haves'])
    
    # 画质
    if directions.get('quality'):
        parts.append(directions['quality'])
    else:
        parts.append("high quality, detailed, 8k")
    
    return ", ".join(parts)


def generate_image(prompt: str, api_config: Dict, seed: int = None):
    """Generate image using selected API"""
    print_section("🚀 图像生成")
    print(f"API: {api_config['api_config']['name']}")
    print(f"模型: {api_config['api_config']['default_model']}")
    print(f"提示词: {prompt[:100]}...")
    print()
    
    # 根据 API 调用不同的生成脚本
    if api_config['api'] == 'siliconflow':
        import subprocess
        cmd = [
            sys.executable,
            str(Path(__file__).parent / 'generate.py'),
            prompt
        ]
        if seed:
            cmd.extend(['--seed', str(seed)])
        subprocess.run(cmd)
    
    elif api_config['api'] == 'zhipu':
        # 调用智谱生成脚本
        import subprocess
        cmd = [
            sys.executable,
            str(Path(__file__).parent / 'generate_zhipu.py'),
            prompt
        ]
        if seed:
            cmd.extend(['--seed', str(seed)])
        subprocess.run(cmd)


def interactive_workflow():
    """Main interactive workflow"""
    # Step 1: User directions
    directions = collect_user_directions()
    
    print_section("📋 用户设定确认")
    print(f"类型: {directions.get('type', '未指定')}")
    print(f"风格: {directions.get('style', '未指定')}")
    print(f"主体: {directions.get('subject', '未指定')}")
    print(f"氛围: {directions.get('mood', '未指定')}")
    
    if input("\n确认继续？(y/n) [y]: ").strip().lower() == 'n':
        print("❌ 已取消")
        return
    
    # Step 2: AI enhances
    enhanced = ai_enhance_details(directions)
    
    # Step 3: Select API
    api_config = select_api_and_model(enhanced)
    
    # Step 4: Build prompt
    final_prompt = build_final_prompt(enhanced)
    
    print_section("📋 最终提示词")
    print(final_prompt)
    print()
    
    # Step 5: Generate
    if input("🚀 立即生成？(y/n) [y]: ").strip().lower() != 'n':
        seed = input("随机种子 (回车随机): ").strip()
        seed = int(seed) if seed.isdigit() else None
        generate_image(final_prompt, api_config, seed)


def main():
    parser = argparse.ArgumentParser(description='智能图像生成向导')
    parser.add_argument('--quick', '-q', metavar='PROMPT', help='快速模式：直接生成')
    
    args = parser.parse_args()
    
    if args.quick:
        # 快速模式：分析 + 自动选择 + 生成
        print_header("🚀 快速生成模式")
        # TODO: 实现快速分析并生成
    else:
        # 完整向导模式
        interactive_workflow()


if __name__ == '__main__':
    main()