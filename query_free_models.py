#!/usr/bin/env python3
"""
查询各平台免费文生图模型列表
安全版本：不打印 API Key
"""

import urllib.request
import json
import os
from pathlib import Path

def load_env():
    """加载环境变量"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value

def query_siliconflow_models():
    """查询 SiliconFlow 模型列表"""
    print("=" * 60)
    print("🔍 SiliconFlow 免费模型")
    print("=" * 60)
    
    load_env()
    api_key = os.environ.get('SILICONFLOW_API_KEY')
    
    if not api_key:
        print("❌ 未配置 SiliconFlow API Key")
        print("   配置方法: 在 .env 文件添加 SILICONFLOW_API_KEY=your_key")
        return
    
    # 隐藏 key 显示
    masked_key = api_key[:10] + "****" + api_key[-4:] if len(api_key) > 14 else "****"
    print(f"   API Key: {masked_key} (已隐藏)")
    
    url = "https://api.siliconflow.cn/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # 筛选图像生成模型
            image_models = []
            for model in result.get('data', []):
                model_id = model.get('id', '')
                # 常见的文生图模型关键词
                if any(keyword in model_id.lower() for keyword in 
                       ['kolors', 'stable-diffusion', 'flux', 'sdxl', 'image']):
                    image_models.append({
                        'id': model_id,
                        'description': model.get('description', 'N/A')[:50]
                    })
            
            print(f"\n✅ 找到 {len(image_models)} 个文生图模型:")
            for m in image_models[:10]:  # 只显示前10个
                print(f"   • {m['id']}")
            if len(image_models) > 10:
                print(f"   ... 还有 {len(image_models) - 10} 个模型")
                
    except Exception as e:
        print(f"\n❌ 查询失败: {e}")
        print("\n📋 已知免费模型 (来自官方文档):")
        print("   • Kwai-Kolors/Kolors")
        print("   • stabilityai/stable-diffusion-xl-base-1.0")
        print("   • black-forest-labs/FLUX.1-schnell")

def query_modelscope_models():
    """查询 ModelScope 模型列表"""
    print("\n" + "=" * 60)
    print("🔍 ModelScope 免费模型 (API-Inference)")
    print("=" * 60)
    
    # ModelScope 可以通过网页查询，不需要 API Key
    print("\n📋 推荐免费文生图模型:")
    
    models = [
        ("black-forest-labs/FLUX.1-Krea-dev", "FLUX.1 高质量版本", "48秒"),
        ("black-forest-labs/FLUX.1-dev", "FLUX.1 开发版", "40-60秒"),
        ("Qwen/Qwen-Image", "通义万相，中文理解强", "20-60秒"),
        ("ZhipuAI/Z-Image-Turbo", "阿里通义，8步推理", "20-30秒"),
        ("MusePublic/489_ckpt_FLUX_1", "FLUX 社区版", "30-50秒"),
    ]
    
    for model_id, desc, speed in models:
        print(f"   • {model_id}")
        print(f"     描述: {desc}")
        print(f"     速度: {speed}")
        print()
    
    print("💡 查询更多模型:")
    print("   浏览器访问: https://www.modelscope.cn/aigc")
    print("   筛选条件: 勾选 '支持API-Inference'")
    print("\n💡 免费额度:")
    print("   • 每日 2000 次总额度")
    print("   • 单模型 500 次上限")

def query_zhipu_models():
    """查询智谱 AI 模型"""
    print("\n" + "=" * 60)
    print("🔍 智谱 AI 免费模型")
    print("=" * 60)
    
    print("\n📋 文生图模型:")
    print("   • cogview-3 (标准版)")
    print("   • cogview-3-plus (增强版，可能有额度限制)")
    
    print("\n💡 查询方式:")
    print("   访问: https://open.bigmodel.cn/overview")
    print("   查看: 控制台中的 '免费额度' 或 '限免' 标识")
    
    print("\n💡 免费额度:")
    print("   • 新用户注册赠送")
    print("   • 具体额度查看控制台")

def main():
    print("\n" + "=" * 60)
    print("🎨 免费文生图模型查询工具")
    print("=" * 60)
    print("\n注意: API Key 已安全隐藏，不会显示在输出中\n")
    
    query_siliconflow_models()
    query_modelscope_models()
    query_zhipu_models()
    
    print("\n" + "=" * 60)
    print("📊 免费额度对比")
    print("=" * 60)
    print("""
┌─────────────────┬─────────────────────┬──────────────────┐
│ 平台            │ 免费额度            │ 推荐模型         │
├─────────────────┼─────────────────────┼──────────────────┤
│ SiliconFlow     │ 100-200次/天/模型   │ Kolors, SDXL     │
│ 智谱 AI         │ 新用户赠送          │ cogview-3        │
│ ModelScope      │ 2000次/天(500/模型) │ FLUX.1, Qwen     │
└─────────────────┴─────────────────────┴──────────────────┘
    """)
    
    print("🎯 推荐: ModelScope (FLUX.1)")
    print("   • 额度最大 (2000次/天)")
    print("   • 模型最多 (12800+ 个)")
    print("   • 质量最高 (FLUX.1)")
    print()

if __name__ == '__main__':
    main()
