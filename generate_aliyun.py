#!/usr/bin/env python3
"""
阿里云 DashScope 文生图
使用通义万相模型
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
import time

def generate_aliyun_image(api_key, prompt, size="1024x1024"):
    """
    使用阿里云 DashScope 生成图像
    默认使用通义万相模型
    """
    
    # 阿里云 DashScope API 端点
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"  # 异步模式
    }
    
    # 解析尺寸
    width, height = size.split('x')
    
    # 构建请求数据 - 通义万相模型
    # 风格可选: <3d cartoon>, <anime>, <oil painting>, <watercolor>, <sketch>, <chinese painting>, <flat illustration>, <photography>, <portrait>, <auto>
    data = {
        "model": "wanx-v1",  # 通义万相
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "size": f"{width}*{height}",
            "style": "<chinese painting>",  # 中国画风格
            "n": 1
        }
    }
    
    print(f"📝 Request URL: {url}")
    print(f"📝 Prompt: {prompt}")
    print(f"📝 Size: {size}")
    print(f"📝 Style: <chinese painting>")
    
    # 发送请求
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
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

def check_task_status(api_key, task_id):
    """查询异步任务状态"""
    
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    
    req = urllib.request.Request(url, headers=headers, method='GET')
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        print(f"❌ Failed to check task status: {e}")
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

def main():
    # Load API key from environment
    load_env()
    api_key = os.environ.get('DASHSCOPE_API_KEY')
    
    if not api_key:
        print("❌ Error: DASHSCOPE_API_KEY not found in .env file")
        print("   Please add DASHSCOPE_API_KEY=your_key to .env")
        sys.exit(1)
    
    prompt = "古代中国美女，穿着华丽的汉服，长发及腰，手持团扇，优雅端庄，工笔画风格，细腻的线条，淡雅的配色，中国传统美学，高清细节"
    
    print("=" * 60)
    print("🎨 阿里云 DashScope 通义万相 - 古代仕女图")
    print("=" * 60)
    
    # 提交任务
    result = generate_aliyun_image(api_key, prompt)
    
    if result is None:
        print("\n❌ 任务提交失败")
        return
    
    print(f"\n✅ 任务提交成功:")
    print(json.dumps(result, indent=2))
    
    task_id = result.get('output', {}).get('task_id')
    if not task_id:
        print("❌ 未获取到任务 ID")
        return
    
    print(f"\n⏳ Task ID: {task_id}")
    print("⏳ 等待生成完成...")
    
    # 轮询等待结果
    max_wait = 120  # 最多等待120秒
    interval = 5
    
    for i in range(0, max_wait, interval):
        time.sleep(interval)
        status = check_task_status(api_key, task_id)
        
        if status is None:
            print(f"   [{i+interval}s] 查询失败，继续等待...")
            continue
        
        task_status = status.get('output', {}).get('task_status', 'UNKNOWN')
        print(f"   [{i+interval}s] Status: {task_status}")
        
        if task_status == 'SUCCEEDED':
            results = status.get('output', {}).get('results', [])
            if results and len(results) > 0:
                image_url = results[0].get('url')
                if image_url:
                    print(f"\n🎉 图片生成成功!")
                    print(f"🖼️  URL: {image_url}")
                    
                    # 保存图片
                    today = datetime.now().strftime('%Y%m%d')
                    output_dir = Path('/root/.openclaw/workspace/agents/designer/output') / f'aliyun_{today}'
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    output_path = output_dir / 'ancient_beauty_001.png'
                    print(f"⬇️  下载中...")
                    
                    if download_image(image_url, output_path):
                        print(f"✅ 已保存: {output_path}")
                        return str(output_path)
                    else:
                        print(f"⚠️  下载失败，图片 URL: {image_url}")
                        return None
            
        elif task_status == 'FAILED':
            print(f"❌ 任务失败: {status.get('output', {}).get('message', 'Unknown error')}")
            return None
    
    print(f"\n⏰ 超时，任务仍在处理中")
    print(f"   Task ID: {task_id}")
    return None

if __name__ == '__main__':
    main()
