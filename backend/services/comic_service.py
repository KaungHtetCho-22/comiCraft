"""Comic script generation service"""
import openai
import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from google import genai
from google.genai import types


class Panel(BaseModel):
    text: str = Field(description="Panel description text")


class Row(BaseModel):
    height: str = Field(description="Row height, e.g., '180px'")
    panels: List[Panel]

class ComicPage(BaseModel):
    title: str = Field(description="Page title")
    rows: List[Row]

class ComicScript(BaseModel):
    pages: List[ComicPage] = Field(description="List of comic pages")

class ComicService:
    """Comic script generator using OpenAI or Google API"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.openai.com/v1", model: str = "gpt-4o-mini", comic_style: str = "doraemon", language: str = "en", google_api_key: str = None):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.comic_style = comic_style
        self.language = language
        self.google_api_key = google_api_key
    
    def _build_system_prompt(self, prompt: str, page_count: int, rows_per_page: int, continuation_context: Dict[str, Any] = None) -> str:
        """Build the system prompt for new-story or continuation generation."""
        """
        Args:
            prompt: User's description of the comic
            page_count: Number of pages to generate
            rows_per_page: Number of rows per page (3-5)
            continuation_context: Optional continuation metadata
        """
        # Define style descriptions
        style_descriptions = {
            "doraemon": "Doraemon anime style: rounded cute character designs, clean simple linework, warm and humorous atmosphere, pastel color palette, expressive chibi-like proportions",
            "american": "Classic American comic style: bold ink outlines, strong dramatic shadows (hatching), heroic proportions, high-contrast color fills, dynamic action compositions, bold speech bubbles",
            "watercolor": "Watercolor illustration style: soft color washes and bleeds, visible brushstrokes, dreamy atmospheric haze, gentle color transitions, painterly loose linework",
            "disney": "Disney animation art style: smooth fluid lines, highly expressive exaggerated faces, graceful movement, warm vibrant colors, magical whimsical atmosphere (art style only — no Disney IP characters)",
            "ghibli": "Studio Ghibli art style: detailed lush nature backgrounds, soft warm color palette, imaginative fantastical elements, nuanced character expressions, poetic and healing atmosphere (art style only — no Ghibli IP characters)",
            "pixar": "Pixar CGI animation style: three-dimensional rounded character forms, rich subsurface lighting, detailed material textures, expressive large eyes, heartfelt emotional storytelling (art style only)",
            "shonen": "Japanese shonen manga style: dynamic speed lines, exaggerated expressions and poses, high-energy action compositions, strong visual impact, fast-paced panel cuts, bold sound-effect lettering",
            "tom_and_jerry": "Tom and Jerry classic cartoon style: 1950s hand-drawn 2D animation, extremely exaggerated physical comedy, elastic rubbery character motion, slapstick chase energy, bright saturated colors",
            "manga": "Classic black-and-white manga style: crisp ink linework, screen tone shading, expressive emotive faces with large eyes, dramatic perspective foreshortening, clean panel compositions, manga-style sound effects",
            "noir": "Film noir comic style: stark black and white with deep shadows, heavy cross-hatching, dramatic chiaroscuro lighting, moody rain-slicked city environments, hard-boiled detective atmosphere, cigarette smoke and silhouettes",
            "superhero": "American superhero comic style: bold dynamic anatomy, dramatic hero poses, explosive action lines, vivid primary colors, dramatic low-angle shots, halftone dot printing texture, bold impact lettering",
            "vintage": "Vintage newspaper comic strip style: 1940s-1960s aesthetic, simple clean linework, limited muted color palette, newspaper print texture, classic panel borders, nostalgic editorial cartoon feel",
            "kawaii": "Japanese kawaii cute style: pastel rainbow colors, tiny simplified character features, oversized heads and eyes, rosy cheek blushes, sparkles and star decorations, bubbly soft rounded shapes",
            "cyberpunk": "Cyberpunk comic style: neon glow effects on dark backgrounds, rain-drenched futuristic cityscapes, glitch digital art overlays, high-tech low-life aesthetic, chrome and neon color palette, dramatic neon-lit character portraits",
            "european": "European ligne claire style (Tintin/Asterix): clean uniform ink outlines, flat solid color fills, no shading gradients, clear readable compositions, expressive but grounded character designs, detailed architectural backgrounds",
            "chibi": "Super-deformed chibi style: extreme 2-3 head-tall proportions, oversized round heads, tiny bodies, dot or star eyes when flustered, exaggerated cute reactions, soft pastel color palette, comedy-focused expressions",
        }

        # Define language instructions
        language_instructions = {
            "en": "Please generate all content in English (including titles and panel descriptions).",
            "my": "ကျေးဇူးပြု၍ အကြောင်းအရာအားလုံးကို မြန်မာဘာသာဖြင့် ဖန်တီးပါ (ခေါင်းစဉ်နှင့် အကွက်ဖော်ပြချက်များ အပါအဝင်)။"
        }

        style_desc = style_descriptions.get(self.comic_style, style_descriptions["doraemon"])
        language_instruction = language_instructions.get(self.language, language_instructions["en"])

        continuation_section = ""
        if continuation_context:
            existing_page_count = continuation_context.get("existing_page_count", 0)
            story_summary = continuation_context.get("story_summary", "")
            recent_pages = continuation_context.get("recent_pages", [])
            formatted_recent_pages = []
            for page in recent_pages:
                title = page.get("title", "Untitled")
                panel_texts = []
                for row in page.get("rows", []):
                    for panel in row.get("panels", []):
                        if panel.get("text"):
                            panel_texts.append(panel["text"])
                formatted_recent_pages.append(f"- {title}: " + " | ".join(panel_texts[:6]))

            continuation_section = f"""

7. **Story Continuation (CRITICAL)**:
   - This is NOT a new story. You are continuing an existing comic that already has {existing_page_count} page(s).
   - Generate EXACTLY {page_count} NEW page(s) that continue naturally from the existing ending.
   - Do NOT restart the setup, reintroduce the cast from scratch, or repeat earlier scenes unless the story explicitly calls for it.
   - Preserve all existing characters, world rules, setting, tone, relationships, and unresolved plot threads.
   - Advance the narrative from the last known scene into new events with clear continuity.
   - If the current comic has a specific environment or art-direction constraint, keep using it consistently.

## Existing Story Summary
{story_summary}

## Most Recent Pages
{chr(10).join(formatted_recent_pages)}"""

        system_prompt = f"""You are a professional comic storyboard script assistant. Please generate a {page_count}-page comic storyboard script based on the user's description.

**IMPORTANT: Please use {style_desc} to design the storyboard content.**

**Language Requirement: {language_instruction}**

Please strictly follow the provided Schema structure to generate the storyboard script:

1. **Story Structure & Layout**:
   - Generate a complete and coherent {page_count}-page story.
   - **Page Layout**: Each comic page is laid out VERTICALLY with multiple ROWS stacked from top to bottom.
   - **Row Count**: Each page MUST contain EXACTLY {rows_per_page} rows (vertical sections). Do not add more or fewer rows.
   - **Panel Layout**: Each row contains 1-2 panels arranged HORIZONTALLY within that row.
   - **Pacing Control**: Mix single-panel rows (for emphasis/key moments) with two-panel rows (for dialogue/action sequences) to create dynamic pacing.

2. **Visual Design (Critical)**:
   - **Row Height**: Dynamically adjust `height` based on the importance of the panels.
     - Standard shots/dialogue: Use '250px'.
     - Key actions/emphasis shots: Use '350px' or '400px'.
     - Avoid using the same height for all rows.
   - **Panel Description**: The `text` field MUST contain specific visual descriptions (e.g., camera angle, facial expressions, body language, background details).
   - Descriptions should fully reflect the visual style of {self.comic_style}.

3. **Dialogue Content (Very Important)**:
   - **Rich Dialogue**: Comics should primarily tell stories through dialogue and spoken text.
   - **Speech Bubbles**: In the `text` field, use quotes to indicate character dialogue (e.g., "Character A: 'Hello, how are you?'"). This text will appear as speech bubbles in the comic.
   - **Balance**: Prioritize dialogue over internal thoughts. Show emotions through what characters SAY and DO, not just what they think. Internal monologue should be minimal.
   - **Readable Comics**: Ensure readers can follow the story through dialogue alone. Each panel should have verbal content when characters are present.

4. **Language**:
   - All content (titles, descriptions, dialogue) must follow the language requirement: {language_instruction}

5. **Character Naming (CRITICAL)**:
   - **ONLY use the character names/descriptions provided by the user.** If the user says "rabbit", use "rabbit" — do NOT replace with copyrighted character names.
   - **DO NOT use any copyrighted or trademarked character names** (e.g., Mickey Mouse, Elsa, Totoro, etc.).
   - The style setting only affects the visual appearance and art style, NOT the characters themselves.
   - Create original character names if needed, but never use existing IP character names.

6. **Character Consistency (CRITICAL for visual coherence)**:
   - In the FIRST panel of the FIRST page, include a brief character sheet description: enumerate each named character's FIXED visual traits (hair color & style, eye color, clothing color & style, body type, distinguishing features).
   - **Repeat these exact visual traits verbatim** in every subsequent panel that character appears in.
   - Format: "Character: [Name] — [trait 1], [trait 2], [trait 3]..." at the start of each panel description.
   - NEVER change a character's appearance mid-story (no hair color changes, no clothing changes unless plot-relevant and explicitly noted).
   - Secondary characters introduced later must also receive consistent trait descriptions from their first appearance onward.{continuation_section}"""
        return system_prompt

    def generate_comic_script(self, prompt: str, page_count: int = 3, rows_per_page: int = 4, continuation_context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Generate comic script based on user prompt

        Args:
            prompt: User's description of the comic
            page_count: Number of pages to generate
            rows_per_page: Number of rows per page (3-5)
            continuation_context: Optional continuation metadata

        Returns:
            List of comic page data
        """
        system_prompt = self._build_system_prompt(prompt, page_count, rows_per_page, continuation_context)

        try:
            if self.api_key:
                llm = ChatOpenAI(model=self.model, openai_api_key=self.api_key, base_url=self.base_url, temperature=0.7, max_tokens=3000)
                structured_llm = llm.with_structured_output(ComicScript)
                response: ComicScript = structured_llm.invoke(
                    input=[
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=prompt)
                    ],
                )
                
                # Parse and validate JSON
                comic_data = [elem.model_dump() for elem in response.pages]
                return comic_data
            else:
                # Fallback to Google Gemini
                client = genai.Client(api_key=self.google_api_key)
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=[system_prompt, prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=ComicScript,
                        thinking_config=types.ThinkingConfig(thinking_level="low")
                    )
                )
                
                # Parse Google response
                comic_script_data = response.parsed
                if not comic_script_data:
                    # Retry with raw JSON parsing if needed
                    text_response = response.text
                    # Extract JSON from potential markdown
                    if "```json" in text_response:
                        text_response = text_response.split("```json")[1].split("```")[0].strip()
                    elif "```" in text_response:
                        text_response = text_response.split("```")[1].split("```")[0].strip()
                    
                    data = json.loads(text_response)
                    comic_script_data = ComicScript(**data)
                
                return [elem.model_dump() for elem in comic_script_data.pages]
            
        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")


def validate_script(script) -> tuple[bool, str]:
    """
    Validate comic script format
    
    Args:
        script: Comic script object or array
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not script:
        return False, "No script provided"
    
    def _validate_page(page: Dict) -> bool:
        """Validate a single page structure"""
        if not isinstance(page, dict):
            return False
        
        if 'rows' not in page or not isinstance(page['rows'], list):
            return False
        
        for row in page['rows']:
            if not isinstance(row, dict):
                return False
            if 'panels' not in row or not isinstance(row['panels'], list):
                return False
            for panel in row['panels']:
                if not isinstance(panel, dict):
                    return False
        
        return True
    
    # Validate structure
    if isinstance(script, list):
        for page in script:
            if not _validate_page(page):
                return False, "Invalid page structure"
    else:
        if not _validate_page(script):
            return False, "Invalid page structure"
    
    return True, ""
