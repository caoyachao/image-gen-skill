#!/usr/bin/env python3
"""
火山引擎（豆包 Seedream）文生图
"""

import os
import sys
import json
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
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value

def generate_image_volcengine(api_key, prompt, model="doubao-seedream-4-0-250828", size="1024x1024"):
    """
    使用火山引擎（豆包 Seedream）生成图像
    
    API 端点: https://ark.cn-beijing.volces.com/api/v3/images/generations
    """
    
    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 构建请求数据
    data = {
        "model": model,
        "prompt": prompt,
        "size": size
    }
    
    print(f"📝 Request URL: {url}")
    print(f"📝 Model: {model}")
    print(f"📝 Prompt: {prompt}")
    print(f"📝 Size: {size}")
    
    # 发送请求
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
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
    """下载图片"""
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
    # Load API key from environment
    load_env()
    api_key = os.environ.get('VOLCENGINE_API_KEY')
    
    if not api_key:
        print("❌ Error: VOLCENGINE_API_KEY not found in .env file")
        print("   Please add VOLCENGINE_API_KEY=your_key to .env")
        sys.exit(1)
    
    # 古装妇女图提示词
    prompt = "古代中国美女，穿着华丽的汉服，长发及腰，手持团扇，优雅端庄，精致的面容，中国传统美学，高清细节，细腻的画质"
    
    print("=" * 60)
    print("🎨 火山引擎（豆包 Seedream）- 古装仕女图")
    print("=" * 60)
    
    # 使用豆包 Seedream 4.0 模型
    result = generate_image_volcengine(api_key, prompt, model="doubao-seedream-4-0-250828")
    
    if result is None:
        print("\n❌ 生成失败")
        return
    
    print(f"\n✅ API Response:")
    print(json.dumps(result, indent=2))
    
    # 提取图片 URL
    if 'data' in result and len(result['data']) > 0:
        image_url = result['data'][0].get('url')
        if image_url:
            print(f"\n🖼️  Image URL: {image_url}")
            
            # 保存图片
            today = datetime.now().strftime('%Y%m%d')
            output_dir = Path('/root/.openclaw/workspace/agents/designer/output') / f'volcengine_{today}'
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / 'ancient_beauty_volc_001.png'
            print(f"⬇️  下载中...")
            
            if download_image(image_url, output_path):
                print(f"✅ 已保存: {output_path}")
                
                # 保存元数据
                metadata_path = output_dir / 'ancient_beauty_volc_001.json'
                metadata = {
                    'prompt': prompt,
                    'model': 'doubao-seedream-4-0-250828',
                    'api_response': result,
                    'generated_at': datetime.now().isoformat()
                }
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                return str(output_path)
            else:
                print(f"⚠️  下载失败，图片 URL: {image_url}")
    else:
        print("❌ 响应中没有图片数据")

if __name__ == '__main__':
    main()
