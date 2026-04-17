# Image-Gen-Skill

Universal image generation skill with multi-API support (SiliconFlow + Zhipu AI + ModelScope + Alibaba Cloud DashScope). **Features mandatory design constraints** - enforces user confirmation workflow, detail clarity, and API comparison before generation.

## Design Constraints (强制性设计约束)

本 skill 强制执行以下设计约束，不可绕过：

| 约束ID | 描述 | 规则 | 违反后果 |
|--------|------|------|----------|
| **C001** | 禁止无用户确认直接生成 | 必须使用 `--interactive` 交互模式，逐项确认风格、构图、氛围 | 生成被阻止，提示正确用法 |
| **C002** | 禁止未明确细节直接生成 | 必须完成风格、构图、氛围、必需要素四步确认 | 生成被阻止，返回向导 |
| **C003** | 禁止未比较模型优势直接选择 | 必须向用户展示 API 对比表并获得确认 | 生成被阻止，强制比较步骤 |

这些约束确保：
- 用户主导大方向，AI 只补充细节
- 不会遗漏关键视觉要素
- 选择最适合的 API 而非随机

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

**Option 3: ModelScope (Recommended for FLUX.1, free tier)**
- Register at https://www.modelscope.cn (requires Alibaba Cloud account with real-name verification)
- Get API key from: 个人中心 → 访问令牌 → 创建新令牌
- ⚠️ **Security Note**: API key format is `ms-xxxxx`, but remove the `ms-` prefix when using in Authorization header
- Free tier: 2000 calls/day (500 per model)

**Option 4: Alibaba Cloud DashScope (通义万相, Chinese style specialist)**
- Register at https://dashscope.aliyun.com
- Get API key from: 控制台 → API Key 管理
- Supports Chinese painting style (`<chinese painting>`)
- Free tier for new users (check console for details)

### Configuration

Create `.env` file in skill directory:

```bash
# SiliconFlow API
SILICONFLOW_API_KEY=your_siliconflow_key_here

# Zhipu AI API  
ZHIPU_API_KEY=your_zhipu_key_here

# ModelScope API (FLUX.1, Qwen-Image, etc.)
# Get from: https://www.modelscope.cn/my/myaccesstoken
# IMPORTANT: Remove 'ms-' prefix when using the key
MODELSCOPE_API_KEY=your_modelscope_key_here

# Alibaba Cloud DashScope (通义万相)
# Get from: https://dashscope.aliyun.com
DASHSCOPE_API_KEY=your_dashscope_key_here
```

Or set environment variables:
```bash
export SILICONFLOW_API_KEY=your_key
export ZHIPU_API_KEY=your_key
export MODELSCOPE_API_KEY=your_key
export DASHSCOPE_API_KEY=your_key
```

## Usage

### ⚠️ 唯一合法用法: 交互式模式

```bash
# 启动强制交互向导（唯一方式）
openclaw run image-gen-skill --interactive

# 或简写
openclaw run image-gen-skill -i
```

**禁止的用法**（将被约束系统阻止）:
```bash
❌ openclaw run image-gen-skill --prompt "sunset"     # C001: 禁止直接生成
❌ openclaw run image-gen-skill --quick                # C002: 禁止快速模式
❌ openclaw run image-gen-skill generate "portrait"    # C003: 禁止绕过比较
```

### 交互式向导流程

启动后必须经过以下步骤：

1. **自由描述** - 告诉我想画什么
2. **风格选择** - 写实/插画/电影/油画/概念
3. **构图选择** - 特写/中景/广角
4. **氛围选择** - 忧郁/温暖/戏剧性/宁静
5. **必需要素** - 你有什么坚持要的细节
6. **API 对比** - 系统展示各 API 优势，你确认选择
7. **AI 增强** - 我补充专业细节
8. **最终确认** - 你确认提示词
9. **生成** - 执行

### API 对比（强制步骤）

在生成前，系统会强制展示：

| API | 擅长 | 优势 | 劣势 |
|-----|------|------|------|
| **SiliconFlow (Kolors)** | 写实人像、产品摄影 | 照片级真实感、皮肤质感细腻 | 插画风格一般 |
| **智谱 AI (CogView)** | 插画、概念图、中文提示 | 中文理解好、艺术风格强 | 写实程度一般 |
| **ModelScope (FLUX.1)** | 高质量艺术图、细节丰富 | 免费额度大(2000/天)、FLUX.1质量高 | 需异步轮询、需实名认证 |
| **DashScope (通义万相)** | 中国风、传统美学 | 中国画风格、中文理解强 | 需阿里云账号 |

系统会推荐，但**最终选择权在你**。

### DashScope 通义万相风格选项

当选择 DashScope API 时，支持以下风格：

- `<chinese painting>` - 中国画风格（推荐用于古风）
- `<anime>` - 动漫风格
- `<oil painting>` - 油画风格
- `<watercolor>` - 水彩风格
- `<sketch>` - 素描风格
- `<photography>` - 摄影风格

## Examples

### 文学人物肖像（Jeanne de Lamare）

```
$ openclaw run image-gen-skill --interactive

【步骤 1/5】自由描述
💭 描述: Jeanne de Lamare的肖像，莫泊桑小说《一生》的女主角

【步骤 2/5】风格选择
   1. 写实/照片级 - 像照片一样真实
   2. 插画/手绘 - 艺术化、绘画感
   3. 电影感 - 戏剧性光影、电影色调
   4. 概念设计 - 设计图、概念艺术
   5. 油画风格 - 古典油画质感
选择风格 [1-5]: 5

【步骤 3/5】构图选择
   1. 特写 - 面部细节为主
   2. 中景/半身 - 人物+部分环境
   3. 广角/全身 - 完整人物+环境
选择构图 [1-3]: 2

【步骤 4/5】氛围选择
   1. 忧郁/感伤 - Jeanne式的悲剧氛围
   2. 温暖/柔和 - 舒适、亲切
   3. 戏剧性 - 强烈对比、冲击
   4. 宁静/安详 - 平和、淡然
选择氛围 [1-4]: 1

【步骤 5/5】必需要素
   特定颜色或材质? 必须是珍珠耳坠
   特定物品或装饰? (回车跳过)
   特定光线或时间? (回车跳过)

📋 请确认你的选择:
   描述: Jeanne de Lamare的肖像...
   风格: oil_painting
   构图: medium
   氛围: melancholic
   必需要素: 珍珠耳坠
确认以上大方向？(y/n/修改) [y]: y

🔧 API 对比分析 (强制步骤)
   SiliconFlow (Kolors): ⭐⭐⭐ 写实风格照片级真实感更强
   智谱 AI (CogView): ⭐⭐ 油画风格艺术表达更好
请选择 API: 2

🤖 AI 正在基于你的选择补充专业细节...

📋 最终提示词:
Jeanne de Lamare的肖像..., oil painting style, classical art, 
medium shot, melancholic atmosphere, 珍珠耳坠, high quality...

🚀 确认生成？(y/n) [y]: y

🎨 使用 智谱 AI (CogView) 生成...
✅ 图像已保存
```

### 古风仕女图（使用 DashScope）

```
🔧 API 对比分析 (强制步骤)
   DashScope (通义万相): ⭐⭐⭐ 中国画风格最适合古风题材
请选择 API: 4

🤖 AI 正在基于你的选择补充专业细节...

📋 最终提示词:
古代中国美女，穿着华丽的汉服，长发及腰，手持团扇，
优雅端庄，<chinese painting> style, high quality...

🚀 确认生成？(y/n) [y]: y

🎨 使用 DashScope (通义万相) 生成...
✅ 图像已保存
```

## Why Constraints?

传统图像生成工具的问题是：
- ❌ 输入一句话就生成，结果往往不符合预期
- ❌ 随机选 API，可能选错风格
- ❌ 用户大方向不明确，细节全靠 AI 猜

本 skill 的约束设计强制：
- ✅ 用户必须先想清楚要什么
- ✅ API 选择基于真实对比
- ✅ AI 只在确认框架内补充细节

这就像建筑设计的约束——先有结构图，再细化管线，而不是边画边改。

## Files

```
image-gen-skill/
├── image-gen-skill        # 主入口 (强制执行约束)
├── generate.py            # SiliconFlow API 客户端
├── generate_zhipu.py      # 智谱 AI API 客户端
├── generate_modelscope.py # ModelScope API 客户端 (FLUX.1, Qwen-Image)
├── generate_aliyun.py     # Alibaba Cloud DashScope API 客户端 (通义万相)
├── SKILL.md               # 本文档
└── .env                   # API 密钥 (gitignored)
```

## Troubleshooting

### "❌ 必须使用 --interactive 模式"
这是 C001 约束生效。你不能直接生成，必须启动交互向导确认大方向。

### "❌ 细节未明确，无法生成"
这是 C002 约束生效。你跳过了风格/构图/氛围确认步骤。

### "❌ 必须比较 API 优势后由用户确认"
这是 C003 约束生效。不能直接选 API，必须先展示对比表。

## Credits

- SiliconFlow: https://siliconflow.cn
- Zhipu AI: https://open.bigmodel.cn
- ModelScope: https://www.modelscope.cn
- Alibaba Cloud DashScope: https://dashscope.aliyun.com
- 设计约束思想: ACP Harness Pattern
