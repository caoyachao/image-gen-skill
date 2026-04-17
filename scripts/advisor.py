#!/usr/bin/env python3
"""
SiliconFlow Interactive Image Generator with Prompt Advisor
Professional prompt refinement workflow before image generation
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from prompt_advisor import PromptAnalyzer, enhance_prompt, translate_to_english


def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_section(title):
    """Print section divider"""
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print('─'*60)


def get_multiline_input(prompt_text):
    """Get multi-line input from user"""
    print(prompt_text)
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines).strip()


def analyze_and_enhance(user_prompt: str, skip_questions: bool = False) -> str:
    """
    Analyze user prompt and optionally ask for missing details.
    Returns the final enhanced prompt.
    """
    analyzer = PromptAnalyzer(user_prompt)
    analysis = analyzer.analyze()
    
    print_section("分析结果")
    print(f"📊 图像类型: {analysis['image_type'].upper()}")
    print(f"📏 完整度评分: {analysis['completeness_score']}/100")
    
    # Show found elements
    found = [k for k, v in analysis['found_elements'].items() if v]
    if found:
        print(f"✅ 已包含: {', '.join(found)}")
    
    # Show missing elements
    missing = analysis['missing_elements']
    if missing:
        print(f"❌ 缺失: {', '.join(missing[:5])}{'...' if len(missing) > 5 else ''}")
    
    # If complete enough, ask if user wants to proceed
    if analysis['completeness_score'] >= 80:
        print("\n✨ 提示词已经很完整了！")
        if skip_questions:
            return user_prompt
        choice = input("\n🤔 直接生成图像？(y/n/edit) [y]: ").strip().lower()
        if choice == '' or choice == 'y':
            return enhance_prompt(user_prompt, {})
        elif choice == 'edit':
            print("\n当前提示词:")
            print(user_prompt)
            print("\n请输入修改后的提示词 (输入 END 结束):")
            edited = get_multiline_input("")
            return edited if edited else user_prompt
        # else continue to question mode
    
    # Interactive question mode
    if not skip_questions and analysis['suggestions']:
        print_section("完善细节")
        print("💡 回答以下问题可以让图像效果更好 (直接回车跳过):")
        print()
        
        user_inputs = {}
        for i, suggestion in enumerate(analysis['suggestions'][:6], 1):
            print(f"{i}. {suggestion['question']}")
            print(f"   💡 {suggestion['tips']}")
            print(f"   示例: {', '.join(suggestion['examples'][:3])}")
            answer = input("   你的回答: ").strip()
            if answer:
                user_inputs[suggestion['element']] = answer
            print()
        
        # Build enhanced prompt
        enhanced = enhance_prompt(user_prompt, user_inputs)
        
        print_section("生成结果")
        print("📋 原始提示词:")
        print(f"   {user_prompt}")
        print()
        print("📋 增强后提示词:")
        print(f"   {enhanced}")
        
        # Allow final edit
        final_choice = input("\n🤔 (g)直接生成 / (e)编辑 / (r)重新回答 [g]: ").strip().lower()
        if final_choice == 'e':
            print("\n请输入修改后的提示词 (输入 END 结束):")
            edited = get_multiline_input("")
            return edited if edited else enhanced
        elif final_choice == 'r':
            return analyze_and_enhance(user_prompt, skip_questions=False)
        else:
            return enhanced
    
    # No suggestions or skip questions - just add quality defaults
    return enhance_prompt(user_prompt, {})


def interactive_mode():
    """Run full interactive prompt refinement session"""
    print_header("🎨 SiliconFlow 图像生成顾问")
    print()
    print("我将帮你把简单的描述转化为专业的图像生成提示词。")
    print("可以简单描述，比如：'一个中国女孩在咖啡馆'，我会询问细节并完善。")
    print()
    
    # Get user prompt
    user_prompt = input("💭 请描述你想要生成的图像:\n> ").strip()
    
    if not user_prompt:
        print("❌ 请输入描述")
        return None
    
    print(f"\n🔍 正在分析: '{user_prompt}'")
    
    # Analyze and enhance
    final_prompt = analyze_and_enhance(user_prompt)
    
    if not final_prompt:
        print("❌ 未生成有效提示词")
        return None
    
    # Show final result
    print_section("最终提示词")
    print(final_prompt)
    print()
    
    # Generate confirmation
    gen_choice = input("🚀 立即生成图像？(y/n) [y]: ").strip().lower()
    if gen_choice == '' or gen_choice == 'y':
        return final_prompt
    else:
        print("❌ 已取消生成")
        return None


def quick_analyze(prompt: str):
    """Quick analysis without interactive mode"""
    print_header("🎨 SiliconFlow 提示词分析")
    print()
    print(f"📝 原始提示词: {prompt}")
    print()
    
    analyzer = PromptAnalyzer(prompt)
    analysis = analyzer.analyze()
    
    print(f"📊 图像类型: {analysis['image_type'].upper()}")
    print(f"📏 完整度: {analysis['completeness_score']}/100")
    print()
    
    # Progress bar
    score = analysis['completeness_score']
    filled = int(score / 5)
    bar = "█" * filled + "░" * (20 - filled)
    print(f"   [{bar}] {score}%")
    print()
    
    # Found elements
    print("✅ 已包含的元素:")
    for element, found in analysis['found_elements'].items():
        if found:
            print(f"   ✓ {element}")
    
    # Missing elements
    if analysis['missing_elements']:
        print("\n❌ 缺失的元素:")
        for element in analysis['missing_elements']:
            print(f"   ✗ {element}")
        
        print("\n💡 建议补充:")
        for i, suggestion in enumerate(analysis['suggestions'][:3], 1):
            print(f"   {i}. {suggestion['question']}")
            print(f"      例如: {', '.join(suggestion['examples'][:2])}")
    else:
        print("\n✨ 提示词已经很完整了！")
    
    # Template
    print("\n📋 推荐模板:")
    print("─" * 40)
    print(analyzer.get_prompt_template())
    
    # Enhanced version
    enhanced = enhance_prompt(prompt, {})
    print("\n📝 自动增强后:")
    print(enhanced)


def batch_process(prompts_file: str):
    """Process multiple prompts from a file"""
    try:
        with open(prompts_file, 'r') as f:
            prompts = [line.strip() for line in f if line.strip()]
        
        print_header(f"🎨 批量处理: {len(prompts)} 个提示词")
        
        results = []
        for i, prompt in enumerate(prompts, 1):
            print(f"\n[{i}/{len(prompts)}] {prompt[:50]}...")
            analyzer = PromptAnalyzer(prompt)
            analysis = analyzer.analyze()
            enhanced = enhance_prompt(prompt, {})
            
            results.append({
                'original': prompt,
                'enhanced': enhanced,
                'score': analysis['completeness_score'],
                'type': analysis['image_type']
            })
        
        # Save results
        output_file = prompts_file.replace('.txt', '_enhanced.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 结果已保存至: {output_file}")
        
    except FileNotFoundError:
        print(f"❌ 文件未找到: {prompts_file}")
    except Exception as e:
        print(f"❌ 错误: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='SiliconFlow Interactive Image Generator with Prompt Advisor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 交互式模式（推荐）
  python3 advisor.py
  python3 advisor.py --interactive
  
  # 仅分析提示词
  python3 advisor.py --analyze "portrait of a girl"
  
  # 直接生成（先分析后生成）
  python3 advisor.py --generate "your prompt here"
  
  # 批量处理文件
  python3 advisor.py --batch prompts.txt
  
  # 带参数生成
  python3 advisor.py --generate "portrait" --seed 42 --size 1024x1024
        """
    )
    
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='启动交互式提示词完善模式')
    parser.add_argument('--analyze', '-a', metavar='PROMPT',
                        help='仅分析提示词完整度')
    parser.add_argument('--generate', '-g', metavar='PROMPT',
                        help='分析后生成图像')
    parser.add_argument('--batch', '-b', metavar='FILE',
                        help='批量处理提示词文件')
    parser.add_argument('--seed', type=int, help='随机种子')
    parser.add_argument('--size', default='1024x1024', help='图像尺寸')
    parser.add_argument('--model', help='模型名称')
    parser.add_argument('--skip-questions', '-s', action='store_true',
                        help='跳过提问，仅自动增强')
    
    args = parser.parse_args()
    
    # Default to interactive if no args
    if not any([args.interactive, args.analyze, args.generate, args.batch]):
        args.interactive = True
    
    # Handle batch mode
    if args.batch:
        batch_process(args.batch)
        return
    
    # Handle analyze mode
    if args.analyze:
        quick_analyze(args.analyze)
        return
    
    # Handle generate mode
    if args.generate:
        print_header("🎨 SiliconFlow 图像生成")
        print()
        print(f"📝 原始提示词: {args.generate}")
        print()
        
        final_prompt = analyze_and_enhance(args.generate, skip_questions=args.skip_questions)
        
        if final_prompt:
            print("\n" + "="*60)
            print("🚀 启动图像生成...")
            print("="*60)
            
            import subprocess
            cmd = [
                sys.executable,
                str(Path(__file__).parent / 'generate.py'),
                final_prompt
            ]
            if args.seed:
                cmd.extend(['--seed', str(args.seed)])
            if args.size:
                cmd.extend(['--size', args.size])
            if args.model:
                cmd.extend(['--model', args.model])
            
            subprocess.run(cmd)
        return
    
    # Handle interactive mode
    if args.interactive:
        final_prompt = interactive_mode()
        
        if final_prompt:
            print("\n" + "="*60)
            print("🚀 启动图像生成...")
            print("="*60)
            
            import subprocess
            cmd = [
                sys.executable,
                str(Path(__file__).parent / 'generate.py'),
                final_prompt
            ]
            if args.seed:
                cmd.extend(['--seed', str(args.seed)])
            if args.size:
                cmd.extend(['--size', args.size])
            if args.model:
                cmd.extend(['--model', args.model])
            
            subprocess.run(cmd)


if __name__ == '__main__':
    main()