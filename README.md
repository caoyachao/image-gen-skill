# Image-Gen-Skill

Universal image generation skill with multi-API support (SiliconFlow + Zhipu AI + ModelScope + DashScope + Volcengine).
**专为 Designer Agent 打造的图像生成工作流** — 强制设计约束确保产出质量。

## 设计理念

本 skill 不同于普通图像生成工具，它强制执行**设计约束** —— 用户必须先明确大方向（风格、构图、氛围），AI 只在此框架内补充细节。这就像建筑设计：先有结构图，再细化管线，而不是边画边改。

## 核心能力

- **5 大 API 支持**: 
  - SiliconFlow (Kolors) - 写实人像、产品摄影
  - 智谱 AI (CogView) - 插画、概念图、中文提示
  - ModelScope (FLUX.1, Qwen-Image) - 高质量艺术图、免费额度大
  - 阿里云 DashScope (通义万相) - 中国风、传统美学
  - 火山引擎 (豆包 Seedream) - 即梦 AI 底层模型
- **强制交互向导**: 确保关键视觉要素不被遗漏
- **API 对比分析**: 强制比较后由用户选择最适合的模型
- **自动化归档**: 所有产出按日期整理到 `output/` 目录

## 快速开始

### 1. 配置 API 密钥

创建 `.env` 文件：

```bash
# SiliconFlow API (推荐用于写实人像、产品摄影)
SILICONFLOW_API_KEY=your_siliconflow_key_here

# 智谱 AI API (推荐用于插画、概念图、中文提示)
ZHIPU_API_KEY=your_zhipu_key_here

# ModelScope API (FLUX.1, 免费额度大 2000次/天)
MODELSCOPE_API_KEY=your_modelscope_key_here

# 阿里云 DashScope (通义万相, 中国画风格)
DASHSCOPE_API_KEY=your_dashscope_key_here

# 火山引擎 API (豆包 Seedream, 即梦 AI)
VOLCENGINE_API_KEY=your_volcengine_key_here
```

获取方式：
- SiliconFlow: https://siliconflow.cn
- 智谱 AI: https://open.bigmodel.cn
- ModelScope: https://www.modelscope.cn (需实名认证)
- 阿里云 DashScope: https://dashscope.aliyun.com
- 火山引擎: https://console.volcengine.com/ark

### 2. 使用交互式向导（唯一方式）

```bash
# 进入 skill 目录
cd /root/.openclaw/workspace/agents/designer/skills/image-gen-skill

# 启动交互向导
python3 image-gen-skill --interactive
```

⚠️ **禁止直接生成** — 必须使用交互模式确认设计方向

## 交互流程

启动向导后，需要依次确认：

| 步骤 | 内容 | 目的 |
|------|------|------|
| 1. 自由描述 | 告诉我想画什么 | 建立基础概念 |
| 2. 风格选择 | 写实/插画/电影/油画/概念 | 确定视觉语言 |
| 3. 构图选择 | 特写/中景/广角 | 确定画面结构 |
| 4. 氛围选择 | 忧郁/温暖/戏剧性/宁静 | 确定情绪基调 |
| 5. 必需要素 | 你坚持要的细节 | 确保核心需求 |
| 6. API 对比 | 展示各模型优势 | 理性选择工具 |
| 7. AI 增强 | 补充专业细节 | 提升提示词质量 |
| 8. 最终确认 | 确认完整提示词 | 生成前最后检查 |
| 9. 生成 | 执行图像生成 | 产出结果 |

## 示例会话

```
$ python3 image-gen-skill --interactive

🎨 图像生成向导

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
   1. 忧郁/感伤 - 悲剧氛围
   2. 温暖/柔和 - 舒适、亲切
   3. 戏剧性 - 强烈对比、冲击
   4. 宁静/安详 - 平和、淡然
选择氛围 [1-4]: 1

【步骤 5/5】必需要素
   特定颜色或材质? 珍珠耳坠
   特定物品或装饰? (回车跳过)
   特定光线或时间? (回车跳过)

📋 请确认你的选择:
   描述: Jeanne de Lamare的肖像...
   风格: oil_painting
   构图: medium
   氛围: melancholic
   必需要素: 珍珠耳坠
确认以上大方向？(y/n/修改) [y]: y

🔧 API 对比分析
   SiliconFlow (Kolors): ⭐⭐⭐ 写实风格照片级真实感更强
   智谱 AI (CogView): ⭐⭐ 油画风格艺术表达更好
   ModelScope (FLUX.1): ⭐⭐⭐ 高质量艺术图、细节丰富
请选择 API: 2

🤖 AI 正在基于你的选择补充专业细节...

📋 最终提示词:
Jeanne de Lamare的肖像..., oil painting style, classical art, 
medium shot, melancholic atmosphere, 珍珠耳坠, high quality...

🚀 确认生成？(y/n) [y]: y

🎨 使用 智谱 AI (CogView) 生成...
✅ 图像已保存: output/image_gen_YYYYMMDD/image_001.png
```

## API 对比参考

| API | 擅长场景 | 优势 | 劣势 |
|-----|----------|------|------|
| **SiliconFlow (Kolors)** | 写实人像、产品摄影 | 照片级真实感、皮肤质感细腻 | 插画风格一般 |
| **智谱 AI (CogView)** | 插画、概念图、中文提示 | 中文理解好、艺术风格强 | 写实程度一般 |
| **ModelScope (FLUX.1)** | 高质量艺术图、细节丰富 | 免费额度大(2000/天)、质量高 | 需异步轮询、需实名认证 |
| **DashScope (通义万相)** | 中国风、传统美学 | 中国画风格、支持风格标签 | 需阿里云账号 |
| **Volcengine (Seedream)** | 通用图像生成 | 即梦 AI 底层模型、速度快 | 需开通模型服务 |

### 风格标签支持

**DashScope 通义万相支持:**
- `<chinese painting>` - 中国画风格
- `<anime>` - 动漫风格
- `<oil painting>` - 油画风格
- `<watercolor>` - 水彩风格
- `<sketch>` - 素描风格
- `<photography>` - 摄影风格

## 文件结构

```
image-gen-skill/
├── image-gen-skill        # 主入口脚本（强制执行设计约束）
├── generate.py            # SiliconFlow API 客户端
├── generate_zhipu.py      # 智谱 AI API 客户端
├── generate_modelscope.py # ModelScope API 客户端 (FLUX.1)
├── generate_aliyun.py     # 阿里云 DashScope 客户端 (通义万相)
├── generate_volcengine.py # 火山引擎 API 客户端 (豆包 Seedream)
├── query_free_models.py   # 免费模型查询工具
├── smart_generator.py     # 智能生成器
├── prompt_advisor.py      # 提示词建议器
├── advisor.py             # 设计顾问模块
├── variation.py           # 变体生成器
├── generator.py           # 通用生成器基类
├── SKILL.md               # 完整技能文档（面向 Agent）
├── README.md              # 用户文档（本文档）
├── .env                   # API 密钥（gitignored）
└── .env.example           # 配置模板
```

## 输出目录

所有图像自动归档到：

```
/root/.openclaw/workspace/agents/designer/output/image_gen_YYYYMMDD/
├── image_001.png          # 图像文件
├── image_001.json         # 元数据（提示词、参数、API）
├── image_002.png
└── ...
```

## 模型信息

### SiliconFlow (Kwai-Kolors/Kolors)
- **支持尺寸**: 1024x1024, 768x1344, 1344x768
- **推理速度**: ~4-8秒
- **免费额度**: 注册赠送，用完需充值

### 智谱 AI (CogView-3)
- **支持尺寸**: 1024x1024
- **中文理解**: 优秀
- **免费额度**: 注册赠送

### ModelScope (FLUX.1-Krea-dev)
- **支持尺寸**: 1024x1024
- **推理速度**: ~48秒 (异步)
- **免费额度**: 2000次/天

### 阿里云 DashScope (通义万相 wanx-v1)
- **支持尺寸**: 1024x1024
- **推理速度**: ~30秒 (异步)
- **风格标签**: 支持 `<chinese painting>` 等

### 火山引擎 (豆包 Seedream 4.0)
- **支持尺寸**: 1024x1024
- **推理速度**: ~10秒
- **特点**: 即梦 AI 底层模型

## 设计约束（不可绕过）

| 约束ID | 描述 | 违反后果 |
|--------|------|----------|
| C001 | 禁止无用户确认直接生成 | 生成被阻止 |
| C002 | 禁止未明确细节直接生成 | 返回向导 |
| C003 | 禁止未比较模型直接选择 | 强制比较步骤 |

## 故障排除

### "❌ 必须使用 --interactive 模式"
这是 C001 约束生效。必须启动交互向导确认大方向。

### "❌ 细节未明确，无法生成"
这是 C002 约束生效。需要完成风格/构图/氛围确认步骤。

### "❌ 必须比较 API 优势后由用户确认"
这是 C003 约束生效。必须先展示对比表再选择 API。

### "❌ ModelNotOpen" (火山引擎)
需要在火山方舟控制台开通模型服务：控制台 → 开通管理 → 开通图像生成模型

## 安全提示

- `.env` 文件包含敏感 API 密钥，**永远不要提交到 Git**
- 已配置 `.gitignore` 自动忽略 `.env` 文件
- 定期检查代码中是否有硬编码的 API 密钥

## Credits

- SiliconFlow: https://siliconflow.cn
- 智谱 AI: https://open.bigmodel.cn
- ModelScope: https://www.modelscope.cn
- 阿里云 DashScope: https://dashscope.aliyun.com
- 火山引擎 Ark: https://console.volcengine.com/ark
- 设计约束思想: ACP Harness Pattern

---

**Designer Agent 专属** · 强制设计约束 · 多 API 智能选择
