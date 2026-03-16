"""Session title generation service"""
import logging
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class SessionTitleService:
    """Generate concise, descriptive titles for comic sessions using OpenAI or Google API"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o-mini",
        language: str = "en",
        google_api_key: Optional[str] = None
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.language = language
        self.google_api_key = google_api_key

    def generate_title(self, prompt: str, comic_data: Optional[dict] = None) -> str:
        """
        Generate a concise, descriptive title for a comic session

        Args:
            prompt: User's original prompt for the comic
            comic_data: Optional comic data (first page, overall structure)

        Returns:
            A short, descriptive title (3-8 words)
        """
        # Define language instructions
        language_instructions = {
            "en": "Generate the title in English. Keep it concise (3-8 words), catchy, and capture the core theme or highlight of the story.",
            "my": "ခေါင်းစဉ်ကို မြန်မာဘာသာဖြင့် ဖန်တီးပါ။ အတိုချုံး (၃-၈ စကားလုံး) နှင့် ဇာတ်လမ်း၏ အဓိကအချက်ကို ဖော်ပြပါ။",
        }

        language_instruction = language_instructions.get(self.language, language_instructions["en"])

        # Build context from comic data if available
        context_info = ""
        if comic_data and isinstance(comic_data, dict):
            if "pages" in comic_data and len(comic_data["pages"]) > 0:
                first_page = comic_data["pages"][0]
                if "title" in first_page:
                    context_info += f"\n\nFirst page title: {first_page['title']}"
                if "rows" in first_page and len(first_page["rows"]) > 0:
                    first_row = first_page["rows"][0]
                    if "panels" in first_row and len(first_row["panels"]) > 0:
                        first_panel_text = first_row["panels"][0].get("text", "")
                        if first_panel_text:
                            preview = first_panel_text[:100] + "..." if len(first_panel_text) > 100 else first_panel_text
                            context_info += f"\nFirst panel: {preview}"

        system_prompt = f"""You are a professional comic session title generator. Create a short, accurate, catchy title for a comic creation session.

**Language requirement**: {language_instruction}

**Core principles** (in priority order):
1. **Accuracy first**: The title must accurately reflect the core theme — do not stray from the subject
2. **Concise**: Stay within the recommended length, remove unnecessary words
3. **Focus**: Center on the protagonist, key event, or core conflict
4. **Recognizable**: Let the user immediately identify this story

**Good examples**:
- User: "A robot learns to dance at a city festival" → Title: "Dancing Robot"
- User: "Detective cat solves the mystery of the missing fish" → Title: "The Fish Mystery"
- User: "Two chefs compete in a magical cooking battle" → Title: "Magic Chef Duel"

**Avoid**:
❌ Too long: "The exciting adventure of a robot who discovers dancing at a city festival"
❌ Too vague: "A new adventure", "Dreams begin" (too generic)
❌ Off-topic titles that miss the main character or event

**Output**: Only the title itself — no quotes, no explanation, no punctuation marks around it."""

        user_message = f"Story description: {prompt}{context_info}"

        try:
            if self.google_api_key:
                logger.info("Using Google Gemini API for title generation")
                client = genai.Client(api_key=self.google_api_key)
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=[system_prompt, user_message],
                    config=types.GenerateContentConfig(
                        temperature=0.6,
                        max_output_tokens=64,
                        thinking_config=types.ThinkingConfig(thinking_level="low")
                    )
                )

                if not response or not response.text:
                    raise ValueError("Gemini API returned empty response")

                title = response.text.strip().strip('"').strip("'").strip()
                if not title:
                    raise ValueError("Generated title is empty")

                logger.info(f"Title generated successfully with Gemini: {title}")
                return title

            elif self.api_key:
                logger.info("Using OpenAI API for title generation")
                llm = ChatOpenAI(
                    model=self.model,
                    openai_api_key=self.api_key,
                    base_url=self.base_url,
                    temperature=0.6,
                    max_tokens=30
                )

                response = llm.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_message)
                ])

                if not response or not response.content:
                    raise ValueError("OpenAI API returned empty response")

                title = response.content.strip().strip('"').strip("'").strip()
                if not title:
                    raise ValueError("Generated title is empty")

                logger.info(f"Title generated successfully with OpenAI: {title}")
                return title
            else:
                raise ValueError("No API key provided")

        except Exception as e:
            logger.error(f"Title generation failed: {str(e)}")
            raise Exception(f"Title generation failed: {str(e)}")
