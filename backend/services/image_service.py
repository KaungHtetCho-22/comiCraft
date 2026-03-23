"""Image generation service"""
import os
import glob
import logging
import requests
from typing import List, Dict, Any, Optional, Union, Tuple
from comic_generator import generate_comic_image_core

logger = logging.getLogger(__name__)


class ImageService:
    """Image generation and proxy service"""

    # Reference image directory path (relative to project root).
    # Defaults to `refer_image/` so the app does not depend on a removed `assets/` folder.
    # Set COMICCRAFT_REFER_IMAGE_BASE_PATH to override (e.g. "refer_image" or "/abs/path").
    REFER_IMAGE_BASE_PATH = os.getenv("COMICCRAFT_REFER_IMAGE_BASE_PATH", "refer_image")
    
    STYLE_DESCRIPTIONS = {
        "doraemon": "Doraemon anime style: rounded cute character designs, clean simple linework, warm and humorous atmosphere, pastel color palette, expressive chibi-like proportions",
        "american": "Classic American comic style: bold ink outlines, strong dramatic shadows (hatching), heroic proportions, high-contrast color fills, dynamic action compositions, bold speech bubbles",
        "watercolor": "Watercolor illustration style: soft color washes and bleeds, visible brushstrokes, dreamy atmospheric haze, gentle color transitions, painterly loose linework",
        "disney": "Disney animation art style: smooth fluid lines, highly expressive exaggerated faces, graceful movement, warm vibrant colors, magical whimsical atmosphere (art style only)",
        "ghibli": "Studio Ghibli art style: detailed lush nature backgrounds, soft warm color palette, imaginative fantastical elements, nuanced character expressions, poetic and healing atmosphere (art style only)",
        "pixar": "Pixar CGI animation style: three-dimensional rounded character forms, rich subsurface lighting, detailed material textures, expressive large eyes, heartfelt emotional storytelling (art style only)",
        "shonen": "Japanese shonen manga style: dynamic speed lines, exaggerated expressions and poses, high-energy action compositions, strong visual impact, fast-paced panel cuts, bold sound-effect lettering",
        "tom_and_jerry": "Tom and Jerry classic cartoon style: 1950s hand-drawn 2D animation, extremely exaggerated physical comedy, elastic rubbery character motion, slapstick chase energy, bright saturated colors",
        "manga": "Classic black-and-white manga style: crisp ink linework, screen tone shading, expressive emotive faces with large eyes, dramatic perspective foreshortening, clean panel compositions, manga-style sound effects",
        "noir": "Film noir comic style: stark black and white with deep shadows, heavy cross-hatching, dramatic chiaroscuro lighting, moody rain-slicked city environments, hard-boiled detective atmosphere, cigarette smoke and silhouettes",
        "superhero": "American superhero comic style: bold dynamic anatomy, dramatic hero poses, explosive action lines, vivid primary colors, dramatic low-angle shots, halftone dot printing texture, bold impact lettering",
        "vintage": "Vintage newspaper comic style: 1940s-1960s aesthetic, simple clean linework, limited muted color palette, newspaper print texture, classic panel borders, nostalgic editorial cartoon feel",
        "kawaii": "Japanese kawaii cute style: pastel rainbow colors, tiny simplified character features, oversized heads and eyes, rosy cheek blushes, sparkles and star decorations, bubbly soft rounded shapes",
        "cyberpunk": "Cyberpunk comic style: neon glow effects on dark backgrounds, rain-drenched futuristic cityscapes, glitch digital art overlays, high-tech low-life aesthetic, chrome and neon color palette, dramatic neon-lit character portraits",
        "european": "European ligne claire style (Tintin/Asterix): clean uniform ink outlines, flat solid color fills, no shading gradients, clear readable compositions, expressive but grounded character designs, detailed architectural backgrounds",
        "chibi": "Super-deformed chibi style: extreme 2-3 head-tall proportions, oversized round heads, tiny bodies, dot or star eyes when flustered, exaggerated cute reactions, soft pastel color palette, comedy-focused expressions",
    }

    @staticmethod
    def get_style_reference_images(comic_style: str) -> List[Tuple[str, str]]:
        """
        Get reference images for a specific comic style.

        Args:
            comic_style: The comic style (e.g., 'doraemon', 'disney', etc.)

        Returns:
            List of tuples (character_name, image_path) where character_name
            is derived from the filename (without extension)
        """
        # Get project root directory (one level up from backend)
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_root = os.path.dirname(backend_dir)

        base_path = ImageService.REFER_IMAGE_BASE_PATH
        if not base_path:
            return []

        refer_dir = (
            os.path.join(project_root, base_path, comic_style)
            if not os.path.isabs(base_path)
            else os.path.join(base_path, comic_style)
        )

        if not os.path.exists(refer_dir):
            logger.debug(f"Reference image directory not found: {refer_dir}")
            return []

        # Supported image formats
        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.webp', '*.gif']
        reference_images = []

        for ext in image_extensions:
            pattern = os.path.join(refer_dir, ext)
            for image_path in glob.glob(pattern):
                # Extract character name from filename (remove extension)
                filename = os.path.basename(image_path)
                character_name = os.path.splitext(filename)[0]
                reference_images.append((character_name, image_path))
                logger.info(f"Found reference image for '{character_name}': {image_path}")

        return reference_images

    @staticmethod
    def generate_comic_image(
        page_data: Dict[str, Any],
        comic_style: str = 'doraemon',
        reference_img: Optional[Union[str, List[Union[str, Dict[str, Any]]]]] = None,
        extra_body: Optional[List] = None,
        google_api_key: str = None,
        rows_per_page: Optional[int] = None,
        language: str = 'en'
    ) -> tuple[Optional[str], str]:
        """
        Generate comic image from page data

        Args:
            page_data: Comic page data with rows and panels
            comic_style: Style of the comic
            reference_img: Optional reference image(s)
            extra_body: Optional extra body parameters (previous pages)
            google_api_key: Google API key for image generation
            rows_per_page: Optional number of rows to strictly limit (3-5)
            language: Language of the comic content

        Returns:
            Tuple of (image_url, prompt)
        """
        # Truncate page data to rows_per_page if specified
        if rows_per_page is not None and 'rows' in page_data:
            page_data = page_data.copy()  # Don't modify original
            page_data['rows'] = page_data['rows'][:rows_per_page]

        # Get built-in style-specific character reference images
        style_references = ImageService.get_style_reference_images(comic_style)
        character_info = []
        style_environment_info = []
        character_sheet_info = []
        reference_images = []

        for char_name, img_path in style_references:
            character_info.append((char_name, "", img_path))
            reference_images.append({
                "type": "built_in_style_character",
                "name": char_name,
                "imageUrl": img_path
            })

        # Add user-provided reference images (from studio references or manual upload)
        if reference_img:
            if isinstance(reference_img, list):
                for ref in reference_img:
                    if isinstance(ref, dict):
                        reference_images.append(ref)
                    elif isinstance(ref, str):
                        reference_images.append({"type": "user_reference", "imageUrl": ref})
            elif isinstance(reference_img, str):
                reference_images.append({"type": "user_reference", "imageUrl": reference_img})

        # Add previous generated pages as additional references
        if extra_body and isinstance(extra_body, list):
            for prev_page in extra_body:
                if isinstance(prev_page, dict) and 'imageUrl' in prev_page:
                    reference_images.append({
                        "type": "previous_page",
                        "name": prev_page.get("pageTitle"),
                        "imageUrl": prev_page["imageUrl"]
                    })
                elif isinstance(prev_page, str):
                    reference_images.append({"type": "previous_page", "imageUrl": prev_page})

        # Separate reference categories for stronger prompting.
        previous_page_info = []
        character_info = [] # Reset to prevent duplicates, we rebuild it from reference_images
        style_environment_info = []
        character_sheet_info = []
        
        for idx_0based, ref in enumerate(reference_images):
            idx = idx_0based + 1
            ref_type = ref.get("type", "")
            if ref_type in {"studio_character", "built_in_style_character"}:
                character_info.append((ref.get("name", "Character"), ref.get("description", ""), idx))
            elif ref_type == "locked_character_sheet":
                character_sheet_info.append((
                    ref.get("name", "Locked Character Sheet"),
                    ref.get("description", ""),
                    idx
                ))
            elif ref_type == "studio_style":
                style_environment_info.append((
                    ref.get("name", "Art Style"),
                    ref.get("description", ""),
                    idx
                ))
            elif ref_type == "locked_style_sheet":
                style_environment_info.append((
                    ref.get("name", "Locked Environment Sheet"),
                    ref.get("description", ""),
                    idx
                ))
            elif ref_type == "previous_page":
                page_label = ref.get("name") or ref.get("pageTitle") or f"Page {len(previous_page_info) + 1}"
                previous_page_info.append((page_label, idx))

        # Convert page data to prompt with style, character references, and style environment references
        prompt = ImageService._convert_page_to_prompt(
            page_data, comic_style, language, character_info, style_environment_info, character_sheet_info,
            previous_page_info
        )

        # Use reference_images if we have any, otherwise None
        final_reference = reference_images if reference_images else None
        
        # Generate image
        image_url = generate_comic_image_core(
            prompt=prompt,
            reference_img=final_reference,
            google_api_key=google_api_key
        )
        
        return image_url, prompt
    
    @staticmethod
    def generate_comic_cover(
        comic_style: str = 'doraemon',
        google_api_key: str = None,
        reference_imgs: List[Union[str, Dict]] = None,
        language: str = 'en',
        custom_requirements: str = ''
    ) -> tuple[Optional[str], str]:
        """
        Generate comic cover image

        Args:
            comic_style: Style of the comic
            google_api_key: Google API key
            reference_imgs: List of reference image URLs
            language: Language of the comic
            custom_requirements: User's custom cover requirements (optional)

        Returns:
            Tuple of (image_url, prompt)
        """
        # Get style-specific character reference images
        style_references = ImageService.get_style_reference_images(comic_style)
        character_info = []
        style_ref_paths = []

        for i, (char_name, img_path) in enumerate(style_references):
            character_info.append((char_name, "", i + 1))
            style_ref_paths.append(img_path)

        # Create cover prompt with character references
        prompt = ImageService._create_cover_prompt(
            comic_style, language, custom_requirements, character_info
        )

        # Prepare reference images list
        processed_refs = []

        # Add style-specific character reference images first
        processed_refs.extend(style_ref_paths)

        # Add story page reference images (extract URLs from objects if needed)
        if reference_imgs:
            for img in reference_imgs:
                if isinstance(img, dict) and 'imageUrl' in img:
                    processed_refs.append(img['imageUrl'])
                elif isinstance(img, str):
                    processed_refs.append(img)

        image_url = generate_comic_image_core(
            prompt=prompt,
            reference_img=processed_refs,
            google_api_key=google_api_key
        )

        return image_url, prompt
    
    @staticmethod
    def proxy_image_download(image_url: str) -> tuple[bytes, str]:
        """
        Proxy image download to bypass CORS restrictions
        
        Args:
            image_url: URL of the image to download
            
        Returns:
            Tuple of (image_content, content_type)
        """
        response = requests.get(image_url, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch image: {response.status_code}")
        
        content_type = response.headers.get('Content-Type', 'image/png')
        return response.content, content_type
    
    @staticmethod
    def _convert_page_to_prompt(
        page_data: Dict[str, Any],
        comic_style: str = 'doraemon',
        language: str = 'en',
        character_info: Optional[List[Tuple[str, str, int]]] = None,
        style_environment_info: Optional[List[Tuple[str, str, int]]] = None,
        character_sheet_info: Optional[List[Tuple[str, str, int]]] = None,
        previous_page_info: Optional[List[Tuple[str, int]]] = None
    ) -> str:
        """Convert page data to image generation prompt"""
        import json

        # Build layout description and panel content
        layout_rows = []
        panels = []
        if 'rows' in page_data:
            for i, row in enumerate(page_data['rows'], 1):
                if 'panels' in row:
                    panel_count = len(row['panels'])
                    layout_rows.append(f"Row {i}: {panel_count} panel(s)")
                    for j, panel in enumerate(row['panels'], 1):
                        if 'text' in panel:
                            panels.append(f"Row {i}, Panel {j}: {panel['text']}")

        # Create layout description
        total_rows = len(layout_rows)
        layout_description = f"This page has {total_rows} rows:\n" + "\n".join(layout_rows)

        language_map = {
            'en': 'English',
            'my': 'Burmese (မြန်မာ)'
        }
        target_lang = language_map.get(language, 'English')

        # Get style description
        style_desc = ImageService.STYLE_DESCRIPTIONS.get(comic_style, f"a {comic_style} animation style")

        # Build sections
        character_ref_section = ""
        if character_info and len(character_info) > 0:
            char_entries = []
            for char_name, char_desc, img_idx in character_info:
                entry = f"  - Reference image #{img_idx}: Character named '{char_name}'"
                if char_desc:
                    entry += f" — visual description: {char_desc}"
                char_entries.append(entry)
            
            character_ref_section = f"""
## Character Reference Images (SOURCE OF TRUTH)
The following reference images are provided to show what specific characters look like.
You MUST draw these characters EXACTLY as shown in their reference images:
{chr(10).join(char_entries)}

IMPORTANT: These references are the absolute source of truth for character design. Even when applying the {comic_style} style, you MUST preserve the core features, hair, clothing, and proportions shown in these references. Do NOT let the style override their unique identity."""

        character_sheet_section = ""
        if character_sheet_info and len(character_sheet_info) > 0:
            sheet_entries = []
            for sheet_name, sheet_desc, img_idx in character_sheet_info:
                summary = f"  - Reference image #{img_idx}: Locked character sheet '{sheet_name}'"
                if sheet_desc:
                    summary += f" described as '{sheet_desc}'"
                sheet_entries.append(summary)
            
            character_sheet_section = f"""
## Locked Character Sheets
The following reference images are locked character sheets that define the final approved look for the active cast.
You MUST treat these sheets as the highest-priority visual source:
{chr(10).join(sheet_entries)}

IMPORTANT: Preserve the exact face shape, body proportions, clothing, and accessories shown in these sheets throughout every panel."""

        style_ref_section = ""
        if style_environment_info and len(style_environment_info) > 0:
            style_entries = []
            for style_name, style_desc_val, img_idx in style_environment_info:
                summary = f"  - Reference image #{img_idx}: Art Style named '{style_name}'"
                if style_desc_val:
                    summary += f" described as '{style_desc_val}'"
                style_entries.append(summary)
            
            style_ref_section = f"""
## Art Style And Aesthetic References
The following reference images define the RENDERING STYLE and aesthetic.
You MUST apply this exact aesthetic to every panel:
{chr(10).join(style_entries)}

IMPORTANT: Use the SAME artistic rendering technique, line weight, and color grading shown in these style references universially."""

        previous_page_section = ""
        if previous_page_info and len(previous_page_info) > 0:
            page_labels = [f"  - Reference image #{img_idx}: Previous page reference '{label}'" for label, img_idx in previous_page_info]
            
            previous_page_section = f"""
## Previous Page Consistency References
The following reference images represent earlier pages from this story. 
You MUST use these as your primary reference for the visual "engine" of the comic: line weight, shading style, color saturation, and background detail level.
{chr(10).join(page_labels)}

CRITICAL: Match the exact artistic rendering seen in these previous pages to ensure all pages look like they were drawn by the same artist in a single session.
HOWEVER: For the characters' anatomical details, priority remains with the high-quality character references above (Image #1, #2, etc.)."""

        # Main prompt construction
        prompt_content = f"""Using the specific art style described as: {style_desc}, create a high-quality comic page. You MUST maintain perfect visual consistency with any previous pages provided. All text in the comic, including titles and speech bubbles, MUST be in {target_lang}.

# Page Layout (MUST FOLLOW EXACTLY):
{layout_description}

# Content:

## Title
{page_data.get('title', '')}

## Panel Details
{"\n".join(panels)}
{character_ref_section}
{character_sheet_section}
{style_ref_section}
{previous_page_section}"""

        # Build requirements list
        char_ref_req = ""
        if character_info:
            char_refs = [str(i) for _, _, i in character_info]
            char_ref_req = f"\n- MANDATORY CHARACTER DESIGN: Follow reference images {', '.join(char_refs)} exactly for character appearances."

        sheet_ref_req = ""
        if character_sheet_info:
            sheet_refs = [str(i) for _, _, i in character_sheet_info]
            sheet_ref_req = f"\n- CHARACTER SHEET PRIORITY: Follow locked sheets {', '.join(sheet_refs)} as the primary source for character traits."

        style_ref_req = ""
        if style_environment_info:
            style_refs = [str(i) for _, _, i in style_environment_info]
            style_ref_req = f"\n- STYLE ADHERENCE: Use style reference images {', '.join(style_refs)} for the rendering aesthetic."

        prev_page_req = ""
        if previous_page_info:
            prev_refs = [str(i) for _, i in previous_page_info]
            prev_page_req = f"\n- STYLE CONTINUITY: Match the line-weight, shading, and color palette of previous pages {', '.join(prev_refs)} exactly."

        requirements_content = f"""- LAYOUT: Strictly follow the {total_rows}-row layout specified.
- Dialogue and Title MUST be in {target_lang}.
- Use a font that matches the {style_desc} aesthetic.
- Maintain consistent character appearances across all panels.{char_ref_req}{sheet_ref_req}{style_ref_req}{prev_page_req}
- Render the title clearly at the top.
- Ensure all text is legible and bubbles are correctly placed."""

        negative_prompt = "overly complex panels, distorted proportions, inconsistent characters, panel indices, cluttered dialogue, blurry text, style drift, multiple title locations"

        return json.dumps({
            "image_generation_data": {
                "prompt": prompt_content.strip(),
                "requirements": requirements_content.strip(),
                "negative_prompt": negative_prompt
            }
        }, ensure_ascii=False)

    @staticmethod
    def _create_cover_prompt(
        comic_style: str,
        language: str = 'en',
        custom_requirements: str = '',
        character_info: Optional[List[Tuple[str, str, int]]] = None
    ) -> str:
        """Create prompt for comic cover

        Args:
            comic_style: Style of the comic
            language: Language code
            custom_requirements: User's custom cover requirements
            character_info: List of (character_name, description, image_index) tuples for reference
        """
        language_map = {
            'en': 'English',
            'my': 'Burmese (မြန်မာ)'
        }
        target_lang = language_map.get(language, 'English')

        # Build character reference section if available
        character_ref_section = ""
        if character_info and len(character_info) > 0:
            char_descriptions = []
            for char_name, char_desc, img_idx in character_info:
                entry = f"  - Reference image #{img_idx}: Character named '{char_name}'"
                if char_desc:
                    entry += f" — visual description: {char_desc}"
                char_descriptions.append(entry)
            character_ref_section = """
# Character Reference Images:
The following reference images are provided to show what specific characters look like.
You MUST draw these characters exactly as shown in their reference images:
{char_list}

IMPORTANT: When any of these characters appear in the cover, you MUST use their exact appearance from the reference images - same face, hair, clothing, and style.
""".format(char_list="\n".join(char_descriptions))

        final_style_desc = ImageService.STYLE_DESCRIPTIONS.get(comic_style, f"a {comic_style} animation style")
        prompt_template = """Create a high-quality comic book cover using the specific art direction: {final_style_desc}.
{character_ref_section}
# Important Context:
- The reference images provided show the story pages of this comic (after any character reference images).
- You MUST base the cover on the characters, scenes, and storyline shown in these reference images.
- The cover should capture the essence and key moments from the story pages.
- Use the same characters, props, and items with consistent appearances as shown in the reference images.

# Requirements:
- The image must be a vertical comic book cover composition.
- The art style must strictly follow the described direction: {final_style_desc}.
- Make it eye-catching and dramatic while staying true to the story.
- Feature the main characters and key scenes from the reference story pages.
- High resolution, detailed, and professional quality.
- No other text except the title.
- The title text must be in {target_lang}.
- Clear and sharp text for the title, do not repeat all the titles in reference images.
- Vibrant colors and "Cover Art" aesthetic.
- Only present one row one panel in the cover.
- Ensure all characters in the title are correctly rendered and legible.
- The cover should feel like a natural introduction to the story shown in the reference pages.
{custom_section}"""

        # Add custom requirements if provided
        custom_section = ""
        if custom_requirements and custom_requirements.strip():
            custom_section = f"""

# IMPORTANT - User's Custom Requirements (MUST FOLLOW STRICTLY):
The user has provided specific requirements below. These are CRITICAL and take HIGHEST PRIORITY.
You MUST strictly follow these custom requirements while maintaining the basic comic cover style.

User Requirements:
{custom_requirements.strip()}

** You MUST implement ALL of the above user requirements. They are mandatory. **"""

        final_prompt = prompt_template.format(
            final_style_desc=final_style_desc,
            target_lang=target_lang,
            custom_section=custom_section,
            character_ref_section=character_ref_section
        )
        return final_prompt.strip()
