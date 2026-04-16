# Image-Gen-Skill

Universal image generation skill with multi-API support (SiliconFlow + Zhipu AI). Features user-directed workflow, smart API selection, and prompt enhancement.

## Prerequisites

### Required API Keys

You need at least one of the following API keys:

**Option 1: SiliconFlow (Recommended for realistic images)**
- Register at https://siliconflow.cn
- Get API key from dashboard
- Free tier available

**Option 2: Zhipu AI (Recommended for illustration/Chinese prompts)**
- Register at https://open.bigmodel.cn
- Get API key from console
- Free tier available

### Configuration

Create `.env` file in skill directory:

```bash
# SiliconFlow API
SILICONFLOW_API_KEY=your_siliconflow_key_here

# Zhipu AI API  
ZHIPU_API_KEY=your_zhipu_key_here
```

Or set environment variables:
```bash
export SILICONFLOW_API_KEY=your_key
export ZHIPU_API_KEY=your_key
```

## Installation

```bash
# Clone to OpenClaw skills directory
cd ~/.openclaw/skills
git clone https://github.com/caoyachao/image-gen-skill.git

# Or copy to agent workspace
cp -r image-gen-skill ~/.openclaw/workspace/agents/{your-agent}/skills/
```

## Usage

### Quick Generate (Auto API Selection)

```bash
# Simple generation - API auto-selected based on prompt
openclaw run image-gen-skill --prompt "a beautiful sunset"

# With style preset
openclaw run image-gen-skill --prompt "portrait" --style realistic

# Chinese prompts work too
openclaw run image-gen-skill --prompt "夕阳下的海边小镇"
```

### Interactive Mode (Recommended)

```bash
# Full interactive wizard - user directs, AI assists
openclaw run image-gen-skill --interactive
```

Workflow:
1. Describe your image freely
2. Confirm/adjust detected style
3. Choose composition and mood
4. Add must-have elements
5. AI enhances with professional details
6. Smart API selection
7. Generate

### Command Mode

```bash
# Direct generation with specific API
openclaw run image-gen-skill generate "portrait of a girl"
openclaw run image-gen-skill generate "未来城市" --api zhipu

# Analyze prompt completeness
openclaw run image-gen-skill analyze "a car"

# Interactive wizard
openclaw run image-gen-skill interactive
```

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `--prompt`, `-p` | Generation prompt | `--prompt "sunset"` |
| `--style`, `-s` | Style preset | `--style realistic` |
| `--api` | Force specific API | `--api siliconflow` |
| `--seed` | Random seed for reproducibility | `--seed 42` |
| `--size` | Image dimensions | `--size 1024x1024` |
| `--interactive`, `-i` | Interactive wizard mode | `--interactive` |

## API Selection Guide

| API | Best For | Strengths |
|-----|----------|-----------|
| **SiliconFlow (Kolors)** | Realistic photos, portraits, products | Photorealistic quality, natural lighting |
| **SiliconFlow (Qwen)** | Text rendering, Chinese text in images | Good at generating readable text |
| **Zhipu AI (CogView)** | Illustrations, concept art, Chinese prompts | Better Chinese understanding, creative styles |

Auto-selection rules:
- Realistic style + English → SiliconFlow
- Illustration style → Zhipu AI
- Chinese prompt → Zhipu AI (slight preference)

## Output

Images saved to: `output/{api}_{date}/{filename}.png`

Each image includes:
- PNG file
- JSON metadata (prompt, seed, model, timestamp)

## Examples

### Portrait Photography
```bash
openclaw run image-gen-skill --prompt "portrait of young woman, soft lighting" --style realistic
```

### Product Shot
```bash
openclaw run image-gen-skill --prompt "minimalist watch on white background" --style realistic
```

### Illustration
```bash
openclaw run image-gen-skill --prompt "fantasy castle on floating island" --style illustration --api zhipu
```

### Chinese Scene
```bash
openclaw run image-gen-skill --prompt "江南水乡，小桥流水，水墨风格"
```

## Troubleshooting

### "No API key found"
- Check `.env` file exists in skill directory
- Verify API key format
- Try setting environment variable directly

### "Model does not exist"
- Check API key has access to image generation models
- Verify model name spelling
- Try default model (auto-selected)

### Poor image quality
- Use `--interactive` mode for better prompt refinement
- Add quality keywords: "8k", "detailed", "professional"
- Try different style preset

## Files

```
image-gen-skill/
├── image-gen-skill        # Main entry point (this skill)
├── generate.py            # SiliconFlow API client
├── generate_zhipu.py      # Zhipu AI API client
├── generator.py           # Interactive wizard logic
├── prompt_advisor.py      # Prompt analysis engine
├── smart_generator.py     # User-directed workflow
├── advisor.py             # CLI advisor interface
├── .env                   # API keys (gitignored)
├── .env.example           # Example configuration
├── SKILL.md               # This file
└── README.md              # Quick reference
```

## Version History

- **v2.2** - Universal generator, user-directed workflow, smart API selection
- **v2.1** - Multi-API support (SiliconFlow + Zhipu AI)
- **v2.0** - AI-powered prompt advisor with completeness analysis
- **v1.0** - Basic SiliconFlow Kolors integration

## Credits

- SiliconFlow: https://siliconflow.cn
- Zhipu AI: https://open.bigmodel.cn
- Kolors model by Kwai
- CogView model by Zhipu AI