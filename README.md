# SiliconFlow Image Generator

**Designer Agent Only** - 专用图像生成 Skill

## 快速使用

```bash
cd /root/.openclaw/workspace/agents/designer
python3 skills/siliconflow-image-gen/generate.py "你的提示词"
```

## 示例

```bash
# 人像生成
python3 skills/siliconflow-image-gen/generate.py "Portrait of a young Asian woman, soft natural lighting, warm skin tones, gentle smile, professional photography"

# 场景生成
python3 skills/siliconflow-image-gen/generate.py "Cinematic sunset over mountains, golden hour lighting, dramatic clouds, 8k quality" --size 1344x768

# 角色设计
python3 skills/siliconflow-image-gen/generate.py "Full body character design of a cyberpunk warrior, neon accents, concept art style" --seed 123
```

## 配置

API Key 存储在 `.env` 文件中，已自动加载。

## 输出

所有图片自动保存到：
```
output/siliconflow_YYYYMMDD/
├── kolors_image_001.png
├── kolors_image_001.json  # 元数据
├── kolors_image_002.png
└── ...
```

## 模型信息

- **默认模型**: Kwai-Kolors/Kolors（快手可图）
- **支持尺寸**: 1024x1024, 768x1344, 1344x768
- **推理速度**: ~4-8秒
- **图片有效期**: 1小时（已自动下载保存）
