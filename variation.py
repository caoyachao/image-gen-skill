#!/usr/bin/env python3
"""
SiliconFlow Image-to-Image Generator
基于参考图生成变体（表情/动作变化）
"""

import os
import sys
import json
import base64
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

def image_to_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def generate_image_variation(prompt, reference_image, size="1024x1024", strength=0.7):
    """
    Generate image variation based on reference image
    strength: 0.0-1.0, how much to transform (0.7 = keep structure, change details)
    """
    load_env()
    
    api_key = os.environ.get('SILICONFLOW_API_KEY')
    base_url = os.environ.get('SILICONFLOW_BASE_URL', 'https://api.siliconflow.cn/v1')
    default_model = os.environ.get('DEFAULT_MODEL', 'Kwai-Kolors/Kolors')
    
    if not api_key:
        print("❌ Error: API key not found. Check .env file.")
        sys.exit(1)
    
    # Convert reference image to base64
    print(f"📸 Loading reference image: {reference_image}")
    try:
        base64_image = image_to_base64(reference_image)
        print(f"✅ Image loaded ({len(base64_image)} chars)")
    except Exception as e:
        print(f"❌ Failed to load image: {e}")
        sys.exit(1)
    
    # Prepare request
    url = f"{base_url}/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": default_model,
        "prompt": prompt,
        "image_size": size,
        "batch_size": 1,
        "image": base64_image,  # Reference image
        "strength": strength  # How much to change (0.7 = moderate change)
    }
    
    # Make request
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
        print(f"❌ API Error: {e.code} - {error_body}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)

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
    parser = argparse.ArgumentParser(description='Generate image variations using reference image')
    parser.add_argument('prompt', help='Image generation prompt describing new expression/pose')
    parser.add_argument('--reference', '-r', required=True, help='Path to reference image')
    parser.add_argument('--size', default='1024x1024', help='Image size')
    parser.add_argument('--strength', type=float, default=0.7, 
                       help='Transformation strength 0.0-1.0 (default: 0.7, higher = more change)')
    parser.add_argument('--output-dir', help='Output directory')
    
    args = parser.parse_args()
    
    print(f"🎨 Generating image variation...")
    print(f"📝 New prompt: {args.prompt}")
    print(f"🔗 Reference: {args.reference}")
    print(f"⚡ Strength: {args.strength} ({'subtle' if args.strength < 0.5 else 'moderate' if args.strength < 0.8 else 'strong'} change)")
    
    # Generate
    result = generate_image_variation(args.prompt, args.reference, args.size, args.strength)
    
    # Extract image URL
    if 'images' in result and len(result['images']) > 0:
        image_url = result['images'][0]['url']
        inference_time = result.get('timings', {}).get('inference', 0)
        
        print(f"✅ Image generated in {inference_time:.2f}s")
        
        # Prepare output directory
        workspace = Path(__file__).parent.parent.parent
        if args.output_dir:
            output_dir = Path(args.output_dir)
        else:
            today = datetime.now().strftime('%Y%m%d')
            output_dir = workspace / 'output' / f'siliconflow_{today}'
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find next available filename
        existing = list(output_dir.glob('kolors_variation_*.png'))
        next_num = len(existing) + 1
        output_path = output_dir / f'kolors_variation_{next_num:03d}.png'
        
        # Download
        print(f"⬇️  Downloading to {output_path}...")
        if download_image(image_url, output_path):
            print(f"✅ Saved: {output_path}")
            
            # Save metadata
            metadata_path = output_dir / f'kolors_variation_{next_num:03d}.json'
            metadata = {
                'prompt': args.prompt,
                'reference_image': str(args.reference),
                'model': 'Kwai-Kolors/Kolors',
                'size': args.size,
                'strength': args.strength,
                'inference_time': inference_time,
                'image_url': image_url,
                'generated_at': datetime.now().isoformat()
            }
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return str(output_path)
        else:
            print(f"⚠️  Image URL (valid for 1 hour): {image_url}")
            return None
    else:
        print(f"❌ Unexpected response: {result}")
        sys.exit(1)

if __name__ == '__main__':
    main()
