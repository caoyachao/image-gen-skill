#!/usr/bin/env python3
"""
ModelScope Image Generator (Async Mode)
使用 ModelScope API-Inference 服务异步生成图像

关键要点:
1. API Key 要去掉 'ms-' 前缀
2. 必须使用异步模式 (X-ModelScope-Async-Mode: true)
3. 轮询任务状态: GET /v1/tasks/{task_id}
4. 轮询需加 header: X-ModelScope-Task-Type: image_generation
5. 结果从 output_images[0] 获取
6. 每日免费额度: 2000次(单模型500次)
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value

def submit_task(prompt, size="1024x1024", seed=None, model=None, steps=None, guidance=None):
    """
    提交异步图像生成任务
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
        "Content-Type": "application/json",
        "X-ModelScope-Async-Mode": "true"
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
    
    print(f"📝 Submit URL: {url}")
    print(f"📝 Model: {model}")
    print(f"📝 Async Mode: true")
    
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

def poll_task(task_id, api_key, max_retries=60, poll_interval=5):
    """
    轮询任务状态
    
    Args:
        task_id: 任务ID
        api_key: API Key (已去掉 ms- 前缀)
        max_retries: 最大轮询次数 (默认60次 = 5分钟)
        poll_interval: 轮询间隔(秒)
    
    Returns:
        dict: 包含 task_status 和 output_images 的字典
    """
    url = f"https://api-inference.modelscope.cn/v1/tasks/{task_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-ModelScope-Task-Type": "image_generation"
    }
    
    print(f"\n⏳ 开始轮询任务状态...")
    print(f"📝 Poll URL: {url}")
    print(f"📝 Max retries: {max_retries}, Interval: {poll_interval}s")
    
    for i in range(max_retries):
        time.sleep(poll_interval)
        
        req = urllib.request.Request(url, headers=headers, method='GET')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"  ❌ Poll Error {e.code}: {error_body}")
            continue
        except Exception as e:
            print(f"  ❌ Poll failed: {e}")
            continue
        
        status = result.get('task_status', 'UNKNOWN')
        print(f"  [{i+1}/{max_retries}] Status: {status}")
        
        if status == 'SUCCEED':
            print(f"✅ 任务完成!")
            return result
        elif status == 'FAILED':
            print(f"❌ 任务失败: {result.get('message', 'Unknown error')}")
            return result
        elif status in ('PENDING', 'RUNNING', 'PROCESSING'):
            continue
        else:
            print(f"⚠️  未知状态: {status}")
    
    print(f"⏰ 轮询超时 (等待了 {max_retries * poll_interval} 秒)")
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

def generate_image(prompt, size="1024x1024", seed=None, model=None, steps=None, guidance=None, output_dir=None):
    """
    完整的异步图像生成流程：提交 -> 轮询 -> 下载
    
    Returns:
        tuple: (output_path, metadata_path) 或 (None, None)
    """
    load_env()
    api_key = os.environ.get('MODELSCOPE_API_KEY', '')
    if api_key.startswith('ms-'):
        api_key = api_key[3:]
    
    # 1. 提交任务
    print("=" * 60)
    print("🎨 ModelScope Async Image Generation")
    print("=" * 60)
    
    submit_result = submit_task(prompt, size, seed, model, steps, guidance)
    if not submit_result:
        return None, None
    
    task_id = submit_result.get('task_id')
    if not task_id:
        print("❌ 未获取到 task_id")
        print(f"响应: {json.dumps(submit_result, indent=2)}")
        return None, None
    
    print(f"✅ 任务已提交 | Task ID: {task_id}")
    
    # 2. 轮询任务
    poll_result = poll_task(task_id, api_key)
    if not poll_result:
        return None, None
    
    if poll_result.get('task_status') != 'SUCCEED':
        print(f"❌ 任务未成功完成")
        print(f"详情: {json.dumps(poll_result, indent=2)}")
        return None, None
    
    # 3. 获取图片URL
    output_images = poll_result.get('output_images', [])
    if not output_images:
        print("❌ 任务成功但未返回图片 URL")
        return None, None
    
    image_url = output_images[0]
    print(f"🖼️  Image URL: {image_url}")
    
    # 4. 准备输出目录
    if output_dir:
        out_dir = Path(output_dir)
    else:
        today = datetime.now().strftime('%Y%m%d')
        out_dir = Path('/root/.openclaw/workspace/agents/designer/output') / f'modelscope_{today}'
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 5. 下载图片
    existing = list(out_dir.glob('modelscope_image_*.png'))
    next_num = len(existing) + 1
    output_path = out_dir / f'modelscope_image_{next_num:03d}.png'
    
    print(f"⬇️  Downloading to {output_path}...")
    if not download_image(image_url, output_path):
        print(f"⚠️  下载失败，图片 URL: {image_url}")
        return None, None
    
    print(f"✅ Saved: {output_path}")
    
    # 6. 保存元数据
    metadata_path = out_dir / f'modelscope_image_{next_num:03d}.json'
    metadata = {
        'prompt': prompt,
        'model': model or 'black-forest-labs/FLUX.1-Krea-dev',
        'size': size,
        'steps': steps,
        'guidance': guidance,
        'seed': seed,
        'task_id': task_id,
        'image_url': image_url,
        'api_response': poll_result,
        'generated_at': datetime.now().isoformat()
    }
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"📋 Metadata: {metadata_path}")
    
    return str(output_path), str(metadata_path)

def main():
    parser = argparse.ArgumentParser(description='Generate images using ModelScope API (Async Mode)')
    parser.add_argument('prompt', help='Image generation prompt')
    parser.add_argument('--model', default='black-forest-labs/FLUX.1-Krea-dev', help='Model ID')
    parser.add_argument('--size', default='1024x1024', help='Image size')
    parser.add_argument('--seed', type=int, help='Random seed')
    parser.add_argument('--steps', type=int, help='Number of inference steps')
    parser.add_argument('--guidance', type=float, help='Guidance scale')
    parser.add_argument('--output-dir', help='Output directory')
    parser.add_argument('--max-retries', type=int, default=60, help='Max poll retries')
    parser.add_argument('--poll-interval', type=int, default=5, help='Poll interval in seconds')
    
    args = parser.parse_args()
    
    print(f"📝 Prompt: {args.prompt}")
    print(f"📐 Size: {args.size}")
    print(f"🤖 Model: {args.model}")
    print("-" * 50)
    
    output_path, metadata_path = generate_image(
        args.prompt, args.size, args.seed, args.model,
        args.steps, args.guidance, args.output_dir
    )
    
    if output_path:
        print(f"\n🎉 全部完成!")
        print(f"🖼️  Image: {output_path}")
    else:
        print(f"\n❌ 生成失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
