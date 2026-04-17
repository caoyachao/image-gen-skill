#!/usr/bin/env python3
"""
ModelScope Image Generator
使用 ModelScope API-Inference 服务生成图像

关键要点:
1. API Key 要去掉 'ms-' 前缀
2. 同步调用，直接返回图像 URL
3. 每日免费额度: 2000次(单模型500次)
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def generate_image(prompt, size="1024x1024", seed=None, model=None):
    """
    Generate image using ModelScope API-Inference
    """
    load_env()
    
    api_key = os.environ.get('MODELSCOPE_API_KEY')
    if not api_key:
        print("❌ Error: ModelScope API key not found. Check .env file.")
        sys.exit(1)
    
    url = "https://api-inference.modelscope.cn/v1/images/generations"
    
    # 处理 API Key - 去掉 ms- 前缀
    if api_key.startswith('ms-'):
        api_key = api_key[3:]
        print(f"🔑 API Key 已自动去掉 'ms-' 前缀")
    
    # 使用默认模型
    model = model or 'black-forest-labs/FLUX.1-Krea-dev'
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 解析尺寸
    width, height = size.split('x')
    
    # 构建请求数据
    data = {
        "model": model,
        "prompt": prompt,
        "width": int(width),
        "height": int(height)
    }
    
    # 添加可选参数
    if steps is not None:
        data["steps"] = steps
    if guidance is not None:
        data["guidance"] = guidance
    if seed is not None:
        data["seed"] = seed
    
    print(f"📝 Request URL: {url}")
    print(f"📝 Request Data: {json.dumps(data, indent=2)}")
    
    # 发送请求
    req = urllib.request.Request(
        url,
        data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ API Error: {e.code}")
        print(f"❌ Error Body: {error_body}")
        return None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def download_image(image_url, output_path):
    """Download image from URL"""
    try:
        req = urllib.request.Request(image_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate images using ModelScope API')
    parser.add_argument('prompt', help='Image generation prompt')
    parser.add_argument('--model', default='Qwen/Qwen-Image', help='Model ID (default: Qwen/Qwen-Image)')
    parser.add_argument('--size', default='1024x1024', help='Image size (default: 1024x1024)')
    parser.add_argument('--seed', type=int, help='Random seed')
    parser.add_argument('--output-dir', help='Output directory')
    
    args = parser.parse_args()
    
    print(f"🎨 ModelScope Image Generation")
    print(f"📝 Prompt: {args.prompt}")
    print(f"📐 Size: {args.size}")
    print(f"🤖 Model: {args.model}")
    print("-" * 50)
    
    # Generate
    result = generate_image(args.prompt, args.size, args.seed, args.model)
    
    if result is None:
        print("\n❌ Generation failed.")
        return
    
    print(f"\n✅ API Response:")
    print(json.dumps(result, indent=2))
    
    # Extract image URL
    if 'images' in result and len(result['images']) > 0:
        image_url = result['images'][0].get('url')
        if image_url:
            print(f"\n🖼️  Image URL: {image_url}")
            
            # Prepare output directory
            if args.output_dir:
                output_dir = Path(args.output_dir)
            else:
                today = datetime.now().strftime('%Y%m%d')
                output_dir = Path('/root/.openclaw/workspace/agents/designer/output') / f'modelscope_{today}'
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Find next available filename
            existing = list(output_dir.glob('modelscope_image_*.png'))
            next_num = len(existing) + 1
            output_path = output_dir / f'modelscope_image_{next_num:03d}.png'
            
            # Download
            print(f"⬇️  Downloading to {output_path}...")
            if download_image(image_url, output_path):
                print(f"✅ Saved: {output_path}")
                
                # Save metadata
                metadata_path = output_dir / f'modelscope_image_{next_num:03d}.json'
                metadata = {
                    'prompt': args.prompt,
                    'model': args.model,
                    'size': args.size,
                    'steps': args.steps,
                    'guidance': args.guidance,
                    'seed': args.seed,
                    'image_url': image_url,
                    'api_response': result,
                    'generated_at': datetime.now().isoformat()
                }
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                return str(output_path)
            else:
                print(f"⚠️  Could not download image. URL: {image_url}")
        else:
            print("❌ No image URL in response")
    else:
        print("❌ No images in response")

if __name__ == '__main__':
    main()
