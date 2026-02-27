#!/usr/bin/env python3
"""
Image Generator Module for SEO Machine

Generates brand-compliant images using Google's Gemini and Imagen APIs.
Called by the /generate-images command.

Usage:
    python image_generator.py --prompt "Your prompt" --output "path/to/output.png" --aspect "16:9" --size "2K"

    Or import as module:
    from data_sources.modules.image_generator import generate_image, generate_banner_variations

Model priority:
    1. Gemini 3 Pro (primary) - Best quality
    2. Imagen 4 (fallback) - Fast and reliable if Gemini fails/hangs
"""

import os
import sys
import argparse
import base64
import signal
import subprocess
from pathlib import Path
from contextlib import contextmanager

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Logo configuration (based on Figma blog cover template)
# At 1920x960: logo at x=69, y=835, size 228x69
LOGO_PATH = Path(__file__).parent.parent.parent / 'context' / 'assets' / 'swimm-logo-white.svg'
LOGO_MARGIN_LEFT = 69   # pixels from left edge
LOGO_MARGIN_BOTTOM = 56  # pixels from bottom edge (960 - 835 - 69 = 56)
LOGO_HEIGHT = 69  # target logo height in pixels

from dotenv import load_dotenv

# Load environment from config
config_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(config_path)

from google import genai
from google.genai import types


# Model configuration
GEMINI_3_PRO = "gemini-3-pro-image-preview"
GEMINI_25_FLASH = "gemini-2.5-flash-image"
IMAGEN_MODEL = "imagen-4.0-generate-001"
IMAGEN_ULTRA = "imagen-4.0-ultra-generate-001"
IMAGEN_FAST = "imagen-4.0-fast-generate-001"

# Default to Gemini 3 Pro (best quality), with Imagen as fallback
DEFAULT_MODEL = GEMINI_3_PRO
FALLBACK_MODEL = IMAGEN_MODEL

# Timeout for Gemini (can hang on complex prompts)
GEMINI_TIMEOUT_SECONDS = 30

# Supported aspect ratios
ASPECT_RATIOS = {
    "banner": "16:9",
    "linkedin": "1:1",
    "portrait": "9:16",
    "standard": "4:3",
    "wide": "3:4",
}

SIZES = ["1K", "2K"]


class TimeoutError(Exception):
    """Raised when an operation times out."""
    pass


@contextmanager
def timeout(seconds):
    """Context manager for timing out operations."""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {seconds} seconds")

    # Set the signal handler
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


def add_logo_to_image(image_path: str, logo_path: str = None) -> bool:
    """
    Overlay the Swimm logo on the bottom-left corner of an image.

    Args:
        image_path: Path to the image to add logo to
        logo_path: Path to logo file (defaults to LOGO_PATH)

    Returns:
        True if successful, False otherwise
    """
    try:
        from PIL import Image
        import cairosvg
        import io

        if logo_path is None:
            logo_path = LOGO_PATH

        logo_path = Path(logo_path)
        if not logo_path.exists():
            print(f"  Warning: Logo file not found at {logo_path}")
            return False

        # Load the base image
        base_image = Image.open(image_path).convert('RGBA')
        base_width, base_height = base_image.size

        # Convert SVG logo to PNG at appropriate size
        # Scale logo height to LOGO_HEIGHT while maintaining aspect ratio
        logo_png_data = cairosvg.svg2png(
            url=str(logo_path),
            output_height=LOGO_HEIGHT
        )
        logo_image = Image.open(io.BytesIO(logo_png_data)).convert('RGBA')
        logo_width, logo_height = logo_image.size

        # Calculate position (bottom-left with margins from Figma specs)
        x_position = LOGO_MARGIN_LEFT
        y_position = base_height - logo_height - LOGO_MARGIN_BOTTOM

        # Composite logo onto base image
        base_image.paste(logo_image, (x_position, y_position), logo_image)

        # Save back (convert to RGB for PNG without alpha issues)
        base_image = base_image.convert('RGB')
        base_image.save(image_path)

        return True

    except ImportError as e:
        print(f"  Warning: Could not add logo - missing dependency: {e}")
        print("  Install with: pip install Pillow cairosvg")
        return False
    except Exception as e:
        print(f"  Warning: Could not add logo: {e}")
        return False


def get_client():
    """Initialize and return the Gemini/Imagen client."""
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment. Check data_sources/config/.env")
    return genai.Client(api_key=api_key)


def _generate_with_model(client, prompt, aspect_ratio, size, model):
    """
    Internal function to generate image with a specific model.
    Returns image_data bytes or raises an exception.
    """
    if 'imagen' in model:
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio,
                image_size=size
            )
        )

        if not response.generated_images:
            raise ValueError("No images generated")

        return response.generated_images[0].image.image_bytes

    else:
        # Gemini models
        if 'gemini-3' in model:
            config = types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=size
                )
            )
        else:
            config = types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config
        )

        if not response.candidates:
            raise ValueError("No candidates in response")

        image_data = None
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if hasattr(part.inline_data, 'data') and part.inline_data.data:
                    image_data = part.inline_data.data
                    if isinstance(image_data, str):
                        image_data = base64.b64decode(image_data)
                    break

        if not image_data:
            raise ValueError("No image data in response")

        return image_data


def generate_image(
    prompt: str,
    output_path: str,
    aspect_ratio: str = "1:1",
    size: str = "2K",
    model: str = DEFAULT_MODEL,
    use_fallback: bool = True,
    add_logo: bool = False
) -> dict:
    """
    Generate an image using Google's Gemini/Imagen APIs.

    Tries Gemini 3 Pro first (with timeout), falls back to Imagen if it fails.

    Args:
        prompt: The text prompt describing the image to generate
        output_path: Path where the image will be saved
        aspect_ratio: One of "1:1", "16:9", "9:16", "4:3", "3:4"
        size: One of "1K", "2K"
        model: Model ID to use (default: gemini-3-pro-image-preview)
        use_fallback: If True, try Imagen fallback if primary model fails
        add_logo: If True, overlay Swimm logo on bottom-left (for banners)

    Returns:
        dict with keys:
            - success: bool
            - path: str (output path if successful)
            - error: str (error message if failed)
            - model_used: str (which model actually generated the image)
            - logo_added: bool (whether logo was added)
    """
    result = {
        "success": False,
        "path": None,
        "error": None,
        "model_used": None,
        "logo_added": False
    }

    try:
        client = get_client()
        image_data = None
        model_used = model

        # Try primary model (with timeout for Gemini)
        try:
            if 'gemini' in model:
                print(f"  Trying {model} (timeout: {GEMINI_TIMEOUT_SECONDS}s)...")
                with timeout(GEMINI_TIMEOUT_SECONDS):
                    image_data = _generate_with_model(client, prompt, aspect_ratio, size, model)
            else:
                print(f"  Trying {model}...")
                image_data = _generate_with_model(client, prompt, aspect_ratio, size, model)

        except (TimeoutError, Exception) as e:
            primary_error = str(e)
            print(f"  Primary model failed: {primary_error}")

            # Try fallback if enabled and different from primary
            if use_fallback and model != FALLBACK_MODEL:
                print(f"  Falling back to {FALLBACK_MODEL}...")
                model_used = FALLBACK_MODEL
                try:
                    image_data = _generate_with_model(client, prompt, aspect_ratio, size, FALLBACK_MODEL)
                except Exception as fallback_error:
                    result["error"] = f"Primary ({model}): {primary_error}. Fallback ({FALLBACK_MODEL}): {str(fallback_error)}"
                    return result
            else:
                result["error"] = primary_error
                return result

        if not image_data:
            result["error"] = "No image data received"
            return result

        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save the image
        with open(output_file, 'wb') as f:
            f.write(image_data)

        # Add logo if requested (for banner images)
        if add_logo:
            logo_success = add_logo_to_image(str(output_file))
            result["logo_added"] = logo_success
            if logo_success:
                print(f"  ✓ Logo added to image")
            else:
                print(f"  ⚠ Logo could not be added (image saved without logo)")

        result["success"] = True
        result["path"] = str(output_file)
        result["model_used"] = model_used

    except Exception as e:
        result["error"] = str(e)

    return result


def generate_banner_variations(
    prompts: list,
    output_dir: str,
    article_slug: str,
    date_str: str = None,
    size: str = "2K"
) -> list:
    """
    Generate multiple banner variations from a list of prompts.

    Args:
        prompts: List of prompt strings (one per variation)
        output_dir: Directory to save images
        article_slug: Article slug for filename
        date_str: Date string for filename (defaults to today)
        size: Image size ("1K" or "2K")

    Returns:
        List of result dicts, one per prompt
    """
    from datetime import date

    if not date_str:
        date_str = date.today().strftime("%Y-%m-%d")

    output_path = Path(output_dir)
    results = []

    for i, prompt in enumerate(prompts, 1):
        filename = f"banner-{i}-{article_slug}-{date_str}.png"
        print(f"\nGenerating banner variation {i}/{len(prompts)}...")

        result = generate_image(
            prompt=prompt,
            output_path=str(output_path / filename),
            aspect_ratio="16:9",
            size=size,
            model=DEFAULT_MODEL,
            use_fallback=True,
            add_logo=True  # Banners always get the logo
        )

        result["variation_number"] = i
        result["prompt"] = prompt

        if result["success"]:
            logo_status = "with logo" if result.get("logo_added") else "without logo"
            print(f"  ✓ Banner {i} saved: {result['path']} (model: {result['model_used']}, {logo_status})")
        else:
            print(f"  ✗ Banner {i} failed: {result['error']}")

        results.append(result)

    return results


def generate_linkedin_image(
    prompt: str,
    output_dir: str,
    article_slug: str,
    date_str: str = None,
    size: str = "2K"
) -> dict:
    """
    Generate a single LinkedIn image.

    Args:
        prompt: The prompt for the LinkedIn image
        output_dir: Directory to save image
        article_slug: Article slug for filename
        date_str: Date string for filename (defaults to today)
        size: Image size ("1K" or "2K")

    Returns:
        Result dict
    """
    from datetime import date

    if not date_str:
        date_str = date.today().strftime("%Y-%m-%d")

    output_path = Path(output_dir)
    filename = f"linkedin-{article_slug}-{date_str}.png"

    print(f"\nGenerating LinkedIn image...")

    result = generate_image(
        prompt=prompt,
        output_path=str(output_path / filename),
        aspect_ratio="1:1",
        size=size,
        model=DEFAULT_MODEL,
        use_fallback=True
    )

    result["prompt"] = prompt

    if result["success"]:
        print(f"  ✓ LinkedIn saved: {result['path']} (model: {result['model_used']})")
    else:
        print(f"  ✗ LinkedIn failed: {result['error']}")

    return result


def generate_blog_images(
    topic: str,
    output_dir: str,
    article_slug: str = None,
    date_str: str = None,
    banner_prompt: str = None,
    linkedin_prompt: str = None,
    size: str = "2K"
) -> dict:
    """
    Generate both banner and LinkedIn images for a blog article.

    Note: This is a legacy function. For the new 5-variation workflow,
    use generate_banner_variations() followed by generate_linkedin_image().

    Args:
        topic: The article topic (used if prompts not provided)
        output_dir: Directory to save images
        article_slug: Article slug for filename
        date_str: Date string for filename
        banner_prompt: Custom prompt for banner (optional)
        linkedin_prompt: Custom prompt for LinkedIn (optional)
        size: Image size ("1K" or "2K")

    Returns:
        dict with banner and linkedin results
    """
    from datetime import date

    if not date_str:
        date_str = date.today().strftime("%Y-%m-%d")

    if not article_slug:
        article_slug = topic.lower().replace(" ", "-").replace("_", "-")
        article_slug = "".join(c for c in article_slug if c.isalnum() or c == "-")
        while "--" in article_slug:
            article_slug = article_slug.replace("--", "-")

    results = {
        "banner": None,
        "linkedin": None
    }

    # Minimal default prompts - real prompts should come from the command
    if not banner_prompt:
        banner_prompt = f"""{topic} as flat vector illustration, \
dark charcoal background, \
abstract conceptual representation, \
deep blue as primary color, \
soft yellow or violet accents, \
solid colors with clean lines, \
NOT photorealistic, \
horizontal composition"""

    if not linkedin_prompt:
        linkedin_prompt = f"""{topic} as flat vector illustration, \
dark charcoal background, \
centered abstract composition, \
deep blue primary, violet or yellow accent, \
solid colors, clean vector style, \
bold and recognizable at small sizes, \
NOT photorealistic, \
square composition"""

    output_path = Path(output_dir)
    banner_filename = f"banner-{article_slug}-{date_str}.png"
    linkedin_filename = f"linkedin-{article_slug}-{date_str}.png"

    # Generate banner
    print("Generating banner image...")
    results["banner"] = generate_image(
        prompt=banner_prompt,
        output_path=str(output_path / banner_filename),
        aspect_ratio="16:9",
        size=size,
        model=DEFAULT_MODEL,
        use_fallback=True
    )
    if results["banner"]["success"]:
        print(f"  ✓ Banner saved: {results['banner']['path']} (model: {results['banner']['model_used']})")
    else:
        print(f"  ✗ Banner failed: {results['banner']['error']}")

    # Generate LinkedIn
    print("Generating LinkedIn image...")
    results["linkedin"] = generate_image(
        prompt=linkedin_prompt,
        output_path=str(output_path / linkedin_filename),
        aspect_ratio="1:1",
        size=size,
        model=DEFAULT_MODEL,
        use_fallback=True
    )
    if results["linkedin"]["success"]:
        print(f"  ✓ LinkedIn saved: {results['linkedin']['path']} (model: {results['linkedin']['model_used']})")
    else:
        print(f"  ✗ LinkedIn failed: {results['linkedin']['error']}")

    return results


def main():
    """CLI interface for image generation."""
    parser = argparse.ArgumentParser(
        description="Generate brand-compliant images using Google Gemini/Imagen APIs"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Text prompt describing the image to generate"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output path for the generated image"
    )
    parser.add_argument(
        "--aspect", "-a",
        default="1:1",
        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
        help="Aspect ratio (default: 1:1)"
    )
    parser.add_argument(
        "--size", "-s",
        default="2K",
        choices=["1K", "2K"],
        help="Image size (default: 2K)"
    )
    parser.add_argument(
        "--model", "-m",
        default=DEFAULT_MODEL,
        help=f"Model to use (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Disable fallback to Imagen if primary model fails"
    )

    args = parser.parse_args()

    print(f"Generating image...")
    print(f"  Primary model: {args.model}")
    print(f"  Fallback: {FALLBACK_MODEL if not args.no_fallback else 'disabled'}")
    print(f"  Aspect ratio: {args.aspect}")
    print(f"  Size: {args.size}")
    print(f"  Output: {args.output}")

    result = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        aspect_ratio=args.aspect,
        size=args.size,
        model=args.model,
        use_fallback=not args.no_fallback
    )

    if result["success"]:
        print(f"\n✓ Image saved: {result['path']}")
        print(f"  Model used: {result['model_used']}")
    else:
        print(f"\n✗ Generation failed: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
