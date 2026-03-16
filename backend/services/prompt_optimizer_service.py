"""Prompt optimization service"""
import logging
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class PromptOptimizerService:
    """Prompt optimizer using OpenAI or Google API"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o-mini",
        comic_style: str = "doraemon",
        language: str = "en",
        google_api_key: Optional[str] = None
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.comic_style = comic_style
        self.language = language
        self.google_api_key = google_api_key
    
    def optimize_prompt(self, prompt: str) -> str:
        """
        Optimize user's simple prompt into detailed comic storyboard description

        Args:
            prompt: User's simple prompt

        Returns:
            Optimized detailed prompt suitable for comic generation
        """
        # Define style descriptions (English)
        style_descriptions = {
            "doraemon": "Doraemon anime style: rounded cute characters, clean simple linework, warm humorous atmosphere",
            "american": "American comic style: bold ink outlines, strong dramatic shadows, heroic proportions, high-contrast colors",
            "watercolor": "Watercolor illustration style: soft color washes, dreamy atmosphere, loose painterly linework",
            "disney": "Disney animation style: smooth fluid lines, expressive faces, warm vibrant colors, magical whimsical atmosphere",
            "ghibli": "Studio Ghibli style: detailed lush nature, soft warm palette, imaginative fantastical elements, poetic atmosphere",
            "pixar": "Pixar CGI style: rounded 3D character forms, rich lighting, detailed textures, heartfelt emotional storytelling",
            "shonen": "Shonen manga style: dynamic speed lines, exaggerated expressions, high-energy action, bold sound-effect lettering",
            "tom_and_jerry": "Tom and Jerry cartoon style: 1950s 2D animation, exaggerated physical comedy, elastic rubbery motion, bright saturated colors",
            "manga": "Classic manga style: crisp ink linework, screen tone shading, expressive large eyes, clean panel compositions",
            "noir": "Film noir style: stark black and white, heavy shadows, moody city environments, hard-boiled atmosphere",
            "superhero": "Superhero comic style: dynamic anatomy, dramatic hero poses, explosive action lines, vivid primary colors",
            "vintage": "Vintage newspaper strip style: 1940s-1960s aesthetic, clean linework, muted color palette, editorial cartoon feel",
            "kawaii": "Kawaii cute style: pastel colors, oversized heads and eyes, rosy cheeks, sparkles, bubbly rounded shapes",
            "cyberpunk": "Cyberpunk style: neon glow on dark backgrounds, futuristic cityscapes, glitch overlays, high-tech low-life aesthetic",
            "european": "European ligne claire style: clean uniform outlines, flat solid colors, clear readable compositions, detailed backgrounds",
            "chibi": "Chibi super-deformed style: 2-3 head-tall proportions, oversized round heads, tiny bodies, exaggerated cute reactions",
        }

        # Define language instructions
        language_instructions = {
            "en": "Please optimize the prompt in English.",
            "my": "မြန်မာဘာသာဖြင့် prompt ကိုပိုမိုကောင်းမွန်အောင်လုပ်ပါ။"
        }

        style_desc = style_descriptions.get(self.comic_style, style_descriptions["doraemon"])
        language_instruction = language_instructions.get(self.language, language_instructions["en"])
        
        system_prompt = f"""You are a professional comic storyboard prompt optimizer. Your task is to take a user's simple idea and expand it into a detailed, vivid description suitable for comic storyboard generation.

**Comic Style Context**: {style_desc}

**Language Requirement**: {language_instruction}

**Your Task**:
1. Understand the user's core idea and intent
2. Expand it with rich visual details suitable for comic panels:
   - Character descriptions (appearance, expressions, clothing)
   - Scene settings (location, atmosphere, time of day)
   - Key actions and interactions
   - Emotional tones and story beats
3. Structure the description to support multi-panel storytelling
4. Make it vivid and specific enough for visual generation
5. Keep it concise but comprehensive (2-4 sentences)

**Output Format**:
- Single paragraph with clear, visual descriptions
- Include specific details about characters, settings, and actions
- Maintain story flow and coherence
- Emphasize visual elements over abstract concepts

**Important**:
- Focus on what CAN BE SEEN in comic panels
- Use concrete visual language
- Consider the specified comic style in your descriptions
- Output ONLY the optimized prompt, no explanations or meta-commentary"""

        try:
            if self.google_api_key:
                # Use Google Gemini API (preferred)
                logger.info("Using Google Gemini API for prompt optimization")
                client = genai.Client(api_key=self.google_api_key)
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=[system_prompt, prompt],
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        thinking_config=types.ThinkingConfig(thinking_level="low")
                    )
                )
                
                optimized = response.text.strip()
                logger.info(f"Prompt optimized successfully with Gemini: {len(optimized)} chars")
                return optimized
                
            elif self.api_key:
                # Use OpenAI API
                logger.info("Using OpenAI API for prompt optimization")
                llm = ChatOpenAI(
                    model=self.model,
                    openai_api_key=self.api_key,
                    base_url=self.base_url,
                    temperature=0.7,
                    max_tokens=500
                )
                
                response = llm.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=prompt)
                ])
                
                optimized = response.content.strip()
                logger.info(f"Prompt optimized successfully with OpenAI: {len(optimized)} chars")
                return optimized
            else:
                raise ValueError("No API key provided")
                
        except Exception as e:
            logger.error(f"Prompt optimization failed: {str(e)}")
            raise Exception(f"Prompt optimization failed: {str(e)}")
