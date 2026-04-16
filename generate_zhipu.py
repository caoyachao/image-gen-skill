#!/usr/bin/env python3
"""
Zhipu AI CogView Image Generator
智谱 AI 图像生成脚本
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
    """Load API key from .env"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def generate_image(prompt: str, size: str = "1024x1024", seed: int = None):
    """Generate image using Zhipu AI CogView"""
    load_env()
    
    api_key = os.environ.get('ZHIPU_API_KEY')
    if not api_key:
        print("❌ Error: ZHIPU_API_KEY not found")
        print("Please set it in .env file or environment variable")
        return None
    
    url = "https://open.bigmodel.cn/api/paas/v4/images/generations"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "cogview-3",
        "prompt": prompt,
    }
    
    if size:
        data["size"] = size
    
    print(f"🎨 使用智谱 AI CogView 生成图像...")
    print(f"📝 提示词: {prompt[:80]}...")
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0]['url']
                request_id = result.get('id', 'unknown')
                
                print(f"✅ 图像生成成功！")
                print(f"📋 Request ID: {request_id}")
                
                # Download image
                workspace = Path(__file__).parent.parent.parent
                today = datetime.now().strftime('%Y%m%d')
                output_dir = workspace / 'output' / f'zhipu_{today}'
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # Find next filename
                existing = list(output_dir.glob('cogview_*.png'))
                next_num = len(existing) + 1
                output_path = output_dir / f'cogview_{next_num:03d}.png'
                
                # Download
                print(f"⬇️  下载中...")
                img_req = urllib.request.Request(image_url, headers={
                    'User-Agent': 'Mozilla/5.0'
                })
                with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                    with open(output_path, 'wb') as f:
                        f.write(img_resp.read())
                
                print(f"✅ 已保存: {output_path}")
                
                # Save metadata
                metadata_path = output_dir / f'cogview_{next_num:03d}.json'
                metadata = {
                    'prompt': prompt,
                    'model': 'cogview-3',
                    'size': size,
                    'request_id': request_id,
                    'image_url': image_url,
                    'generated_at': datetime.now().isoformat()
                }
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                
                return str(output_path)
            else:
                print(f"❌ 生成失败: {result}")
                return None
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ API 错误: {e.code} - {error_body}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Zhipu AI Image Generator')
    parser.add_argument('prompt', help='Image generation prompt')
    parser.add_argument('--size', default='1024x1024', help='Image size')
    parser.add_argument('--seed', type=int, help='Random seed (not used by CogView)')
    
    args = parser.parse_args()
    
    generate_image(args.prompt, args.size, args.seed)

if __name__ == '__main__':
    main()