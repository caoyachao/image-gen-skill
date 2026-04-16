#!/usr/bin/env python3
"""
SiliconFlow Prompt Advisor
Professional prompt analysis and refinement for image generation
"""

import re
from typing import Dict, List, Optional, Tuple


class PromptAnalyzer:
    """Analyze user prompt and identify missing elements for professional image generation"""
    
    # Element detection patterns for different image types
    PORTRAIT_KEYWORDS = {
        'subject': ['portrait', 'person', 'man', 'woman', 'girl', 'boy', 'character', 'people', 'human', 'face'],
        'age': ['year', 'old', 'age', 'young', 'adult', 'child', 'teenager', 'middle-aged', 'elderly', '20s', '30s', '40s', '50s'],
        'facial_features': ['eye', 'eyes', 'hair', 'face', 'expression', 'smile', 'gaze', 'look', 'skin', 'beard', 'mustache'],
        'clothing': ['wear', 'wearing', 'dress', 'shirt', 'jacket', 'sweater', 'coat', 'suit', 'outfit', 'clothes', 'uniform'],
        'lighting': ['light', 'lighting', 'sunlight', 'shadow', 'backlit', 'rim light', 'soft', 'dramatic', 'ambient'],
        'background': ['background', 'setting', 'environment', 'scene', 'indoor', 'outdoor', 'studio', 'backdrop'],
        'style': ['style', 'photorealistic', 'realistic', 'artistic', 'painting', 'drawing', 'sketch', 'anime', 'cartoon'],
        'mood': ['mood', 'atmosphere', 'feeling', 'emotion', 'vibe', 'tone', 'serene', 'dramatic', 'peaceful', 'mysterious'],
        'camera': ['portrait', 'close-up', 'full body', 'half body', 'medium shot', 'headshot', 'bust', 'waist up'],
        'quality': ['quality', 'high quality', '8k', '4k', 'detailed', 'sharp', 'crisp', 'professional', 'masterpiece']
    }
    
    SCENE_KEYWORDS = {
        'subject': ['landscape', 'scene', 'environment', 'city', 'nature', 'forest', 'mountain', 'ocean', 'sky', 'building'],
        'time': ['day', 'night', 'sunset', 'sunrise', 'dawn', 'dusk', 'evening', 'morning', 'afternoon', 'noon'],
        'weather': ['weather', 'sunny', 'rainy', 'cloudy', 'fog', 'snow', 'storm', 'clear', 'overcast'],
        'lighting': ['lighting', 'cinematic', 'dramatic', 'natural light', 'golden hour', 'blue hour', 'neon', 'moonlight'],
        'composition': ['composition', 'perspective', 'angle', 'view', 'wide shot', 'aerial', 'bird eye', 'low angle'],
        'mood': ['mood', 'atmosphere', 'serene', 'dramatic', 'peaceful', 'epic', 'lonely', 'bustling'],
        'style': ['style', 'photorealistic', 'cinematic', 'concept art', 'digital art', 'illustration', 'matte painting'],
        'quality': ['quality', 'high quality', '8k', 'detailed', 'intricate', 'stunning', 'breathtaking']
    }
    
    CHARACTER_KEYWORDS = {
        'subject': ['character', 'design', 'concept', 'hero', 'villain', 'creature', 'monster', 'npc', 'avatar'],
        'appearance': ['appearance', 'features', 'face', 'body', 'physique', 'build', 'height', 'muscular', 'slender'],
        'clothing': ['clothing', 'outfit', 'armor', 'costume', 'attire', 'wear', 'gear', 'equip', 'robe', 'cape'],
        'accessories': ['accessories', 'weapon', 'item', 'prop', 'gear', 'jewelry', 'mask', 'helmet', 'backpack'],
        'style': ['style', 'anime', 'realistic', 'stylized', 'cartoon', 'fantasy', 'sci-fi', 'steampunk', 'cyberpunk'],
        'pose': ['pose', 'stance', 'action', 'standing', 'sitting', 'dynamic', 'fighting', 'running', 'idle'],
        'background': ['background', 'simple', 'white', 'gradient', 'environment', 'scene', 'transparent'],
        'quality': ['quality', 'detailed', 'high quality', 'concept art', 'illustration', 'game art']
    }
    
    def __init__(self, prompt: str):
        self.original_prompt = prompt
        self.prompt = prompt.lower()
        self.image_type = self._detect_image_type()
        self.keywords_map = self._get_keywords_map()
    
    def _detect_image_type(self) -> str:
        """Detect what type of image the user wants based on prompt keywords"""
        prompt_lower = self.prompt.lower()
        
        # Count matches for each type
        portrait_score = sum(1 for kw_list in self.PORTRAIT_KEYWORDS.values() 
                             for kw in kw_list if kw in prompt_lower)
        scene_score = sum(1 for kw_list in self.SCENE_KEYWORDS.values() 
                         for kw in kw_list if kw in prompt_lower)
        character_score = sum(1 for kw_list in self.CHARACTER_KEYWORDS.values() 
                             for kw in kw_list if kw in prompt_lower)
        
        # Check for specific strong indicators
        if any(kw in prompt_lower for kw in ['character design', 'concept art', 'full body', 'outfit', 'costume']):
            return 'character'
        elif any(kw in prompt_lower for kw in ['landscape', 'cityscape', 'environment', 'scene']):
            return 'scene'
        elif any(kw in prompt_lower for kw in ['portrait', 'headshot', 'face']):
            return 'portrait'
        
        # Default based on scores
        scores = {'portrait': portrait_score, 'scene': scene_score, 'character': character_score}
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'portrait'
    
    def _get_keywords_map(self) -> Dict:
        """Get the appropriate keyword map based on image type"""
        maps = {
            'portrait': self.PORTRAIT_KEYWORDS,
            'scene': self.SCENE_KEYWORDS,
            'character': self.CHARACTER_KEYWORDS
        }
        return maps.get(self.image_type, self.PORTRAIT_KEYWORDS)
    
    def analyze(self) -> Dict:
        """Analyze prompt and return detailed report"""
        found_elements = {}
        missing_elements = []
        
        for category, keywords in self.keywords_map.items():
            # Check if any keyword from this category is present
            found = any(kw in self.prompt for kw in keywords)
            found_elements[category] = found
            if not found:
                missing_elements.append(category)
        
        # Calculate completeness score
        total_elements = len(self.keywords_map)
        found_count = sum(1 for v in found_elements.values() if v)
        completeness_score = int((found_count / total_elements) * 100) if total_elements > 0 else 0
        
        # Generate suggestions for missing elements
        suggestions = self._generate_suggestions(missing_elements)
        
        return {
            'image_type': self.image_type,
            'prompt_length': len(self.original_prompt),
            'found_elements': found_elements,
            'missing_elements': missing_elements,
            'completeness_score': completeness_score,
            'suggestions': suggestions
        }
    
    def _generate_suggestions(self, missing_elements: List[str]) -> List[Dict]:
        """Generate professional suggestions for missing elements"""
        suggestion_database = {
            'portrait': {
                'age': {
                    'question': '年龄大概是多少？',
                    'examples': ['25岁左右', '中年', '40岁', '青少年', ' elderly'],
                    'tips': '年龄会影响面部特征和气质表达'
                },
                'facial_features': {
                    'question': '能描述一下五官特征吗？',
                    'examples': ['深邃的眼睛', '高鼻梁', '温和的笑容', '锐利的眼神', '短发'],
                    'tips': '面部细节是肖像的灵魂'
                },
                'clothing': {
                    'question': '穿着什么样的衣服？',
                    'examples': ['白色衬衫', '深色毛衣', '休闲西装', '复古风格', '简约T恤'],
                    'tips': '服装能传达人物的性格和身份'
                },
                'lighting': {
                    'question': '什么样的光线？',
                    'examples': ['自然光', '侧光', '柔和的光线', '戏剧性光影', '窗边光'],
                    'tips': '光线决定氛围和立体感'
                },
                'background': {
                    'question': '背景环境是什么样的？',
                    'examples': ['纯色背景', '咖啡馆', '自然风景', '城市街道', '模糊背景'],
                    'tips': '背景衬托主体，不要太抢眼'
                },
                'mood': {
                    'question': '想要什么样的情绪和氛围？',
                    'examples': ['宁静', '忧郁', '温暖', '专业', '神秘', '放松'],
                    'tips': '情绪是图像的隐性语言'
                },
                'style': {
                    'question': '什么风格？',
                    'examples': ['写实摄影', '艺术人像', '电影感', '柔和色调', '胶片感'],
                    'tips': '风格决定整体视觉语言'
                },
                'camera': {
                    'question': '什么景别？',
                    'examples': ['特写', '半身像', '全身像', '头像'],
                    'tips': '景别决定画面构图'
                },
                'quality': {
                    'question': '需要什么画质？',
                    'examples': ['8K超高清', '专业摄影', '精细细节', '电影级'],
                    'tips': '高质量描述能提升生成效果'
                }
            },
            'scene': {
                'subject': {
                    'question': '场景主体是什么？',
                    'examples': ['城市天际线', '森林', '海滩', '山脉', '建筑'],
                    'tips': '明确场景的核心元素'
                },
                'time': {
                    'question': '什么时间？',
                    'examples': ['黄金时刻', '深夜', '清晨', '阴天', '黄昏'],
                    'tips': '时间决定光线和色调'
                },
                'weather': {
                    'question': '天气如何？',
                    'examples': ['晴朗', '雾蒙蒙', '雨后', '下雪', '多云'],
                    'tips': '天气营造情绪和氛围'
                },
                'lighting': {
                    'question': '光线条件？',
                    'examples': ['自然光', '戏剧性光影', '柔和光线', '霓虹灯光'],
                    'tips': '光是场景的灵魂'
                },
                'composition': {
                    'question': '构图方式？',
                    'examples': ['广角', '鸟瞰', '平视', '仰拍', '前景虚化'],
                    'tips': '构图决定视觉冲击力'
                },
                'mood': {
                    'question': '氛围情绪？',
                    'examples': ['宁静', '史诗感', '孤独', '繁华', '神秘'],
                    'tips': '氛围让观众产生共鸣'
                },
                'style': {
                    'question': '画面风格？',
                    'examples': ['写实摄影', '概念艺术', '电影感', '插画'],
                    'tips': '风格统一视觉语言'
                },
                'quality': {
                    'question': '画质要求？',
                    'examples': ['8K超高清', '精细细节', '壁纸级'],
                    'tips': '高质量适合大屏展示'
                }
            },
            'character': {
                'subject': {
                    'question': '角色类型？',
                    'examples': ['战士', '法师', '刺客', '商人', '动物角色'],
                    'tips': '类型决定设计方向'
                },
                'appearance': {
                    'question': '外貌特征？',
                    'examples': ['高大身材', '独特面部特征', '特殊肤色', '纹身'],
                    'tips': '让角色有辨识度'
                },
                'clothing': {
                    'question': '服装风格？',
                    'examples': ['未来感战甲', '复古风衣', '民族服饰', '皮甲'],
                    'tips': '服装体现角色背景和性格'
                },
                'accessories': {
                    'question': '有什么配饰？',
                    'examples': ['武器', '法杖', '背包', '饰品', '面具'],
                    'tips': '配饰丰富角色设定'
                },
                'style': {
                    'question': '美术风格？',
                    'examples': ['写实', '二次元', '欧美卡通', '像素风'],
                    'tips': '风格决定目标受众'
                },
                'pose': {
                    'question': '什么姿势？',
                    'examples': ['站立', '动态姿势', '坐姿', '战斗姿态', ' idle'],
                    'tips': '姿势展现角色性格'
                },
                'background': {
                    'question': '背景设定？',
                    'examples': ['纯色', '场景背景', '透明', '特效背景'],
                    'tips': '背景衬托角色'
                },
                'quality': {
                    'question': '细节程度？',
                    'examples': ['高精度', '游戏资产级', '概念设计稿'],
                    'tips': '质量决定可用性'
                }
            }
        }
        
        suggestions = []
        type_suggestions = suggestion_database.get(self.image_type, {})
        
        for element in missing_elements:
            if element in type_suggestions:
                suggestions.append({
                    'element': element,
                    **type_suggestions[element]
                })
        
        return suggestions
    
    def get_prompt_template(self) -> str:
        """Get appropriate prompt template based on image type"""
        templates = {
            'portrait': """Portrait of [subject], [age], [facial features], wearing [clothing]. 
[Lighting description], [background/environment]. 
[Style], [mood atmosphere], [quality], [camera shot].""",
            
            'scene': """[Scene description], [time of day], [weather/lighting]. 
[Composition/perspective], [mood atmosphere]. 
[Style], [quality].""",
            
            'character': """Full body character design of [subject], [appearance], wearing [outfit], [accessories]. 
[Pose/action], [style], [background]. 
[Quality], detailed, professional."""
        }
        return templates.get(self.image_type, templates['portrait'])


def enhance_prompt(base_prompt: str, user_inputs: Dict[str, str]) -> str:
    """
    Enhance prompt by intelligently combining base prompt with user inputs.
    Avoids duplication and maintains natural flow.
    """
    enhanced_parts = [base_prompt.strip()]
    base_lower = base_prompt.lower()
    
    # Define enhancement mappings
    enhancements = [
        ('age', lambda v: v if v.lower() not in base_lower else None),
        ('facial_features', lambda v: v if not any(f in base_lower for f in ['eye', 'hair', 'face']) else None),
        ('clothing', lambda v: f"wearing {v}" if 'wear' not in base_lower and 'dress' not in base_lower else v),
        ('lighting', lambda v: v if 'light' not in base_lower else None),
        ('background', lambda v: v if 'background' not in base_lower and 'setting' not in base_lower else None),
        ('mood', lambda v: v if not any(m in base_lower for m in ['mood', 'atmosphere', 'feeling']) else None),
        ('style', lambda v: v if 'style' not in base_lower else None),
        ('camera', lambda v: v if not any(c in base_lower for c in ['portrait', 'close-up', 'full body']) else None),
        ('quality', lambda v: v if 'quality' not in base_lower and '8k' not in base_lower else None),
    ]
    
    # Apply enhancements
    for key, transformer in enhancements:
        if key in user_inputs and user_inputs[key]:
            transformed = transformer(user_inputs[key])
            if transformed and transformed.strip():
                enhanced_parts.append(transformed.strip())
    
    # Always add default quality if not specified
    quality_keywords = ['quality', '8k', '4k', 'high', 'detailed', 'masterpiece']
    if not any(q in base_lower for q in quality_keywords):
        enhanced_parts.append("high quality, detailed, 8k")
    
    # Join with proper punctuation
    result = ", ".join(enhanced_parts)
    
    # Clean up any double punctuation or spacing issues
    result = re.sub(r',\s*,', ',', result)
    result = re.sub(r'\s+', ' ', result)
    
    return result


def translate_to_english(text: str) -> str:
    """
    Simple Chinese to English translation helper for common image generation terms.
    In production, this could be replaced with a proper translation API.
    """
    translations = {
        # Lighting
        '自然光': 'natural lighting',
        '柔和': 'soft',
        '侧光': 'side lighting',
        '背光': 'backlit',
        '逆光': 'backlit',
        '暖色': 'warm tones',
        '冷色': 'cool tones',
        '阴影': 'shadow',
        '高光': 'highlights',
        
        # Style
        '写实': 'photorealistic',
        '艺术': 'artistic',
        '电影感': 'cinematic',
        '高清': 'high quality',
        '精致': 'detailed',
        '模糊': 'blurred',
        '清晰': 'sharp',
        
        # Colors
        '深色': 'dark',
        '浅色': 'light',
        '白色': 'white',
        '黑色': 'black',
        '灰色': 'gray',
        '红色': 'red',
        '蓝色': 'blue',
        '绿色': 'green',
        '黄色': 'yellow',
        
        # Features
        '短发': 'short hair',
        '长发': 'long hair',
        '直发': 'straight hair',
        '卷发': 'curly hair',
        '眼睛': 'eyes',
        '笑容': 'smile',
        
        # Clothing
        '衬衫': 'shirt',
        '毛衣': 'sweater',
        '外套': 'coat',
        '西装': 'suit',
        '牛仔裤': 'jeans',
        '裙子': 'dress',
        
        # Environment
        '背景': 'background',
        '室内': 'indoor',
        '室外': 'outdoor',
        '风景': 'landscape',
        '城市': 'city',
        '自然': 'nature',
    }
    
    result = text
    for cn, en in translations.items():
        if cn in result:
            result = result.replace(cn, en)
    
    return result


# Test function
if __name__ == '__main__':
    test_prompts = [
        "一个中国女孩",
        "Portrait of a man",
        "futuristic city",
        "character design of a warrior"
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"Prompt: {prompt}")
        print('='*60)
        
        analyzer = PromptAnalyzer(prompt)
        analysis = analyzer.analyze()
        
        print(f"\n📊 图像类型: {analysis['image_type'].upper()}")
        print(f"📏 完整度评分: {analysis['completeness_score']}/100")
        print(f"✅ 已包含: {', '.join([k for k, v in analysis['found_elements'].items() if v]) or '无'}")
        print(f"❌ 缺失: {', '.join(analysis['missing_elements']) or '无'}")
        
        if analysis['suggestions']:
            print(f"\n💡 建议补充:")
            for i, sug in enumerate(analysis['suggestions'][:3], 1):
                print(f"  {i}. {sug['question']}")
                print(f"     示例: {', '.join(sug['examples'][:2])}")
        
        print(f"\n📋 推荐模板:")
        print(analyzer.get_prompt_template())