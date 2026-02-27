#!/usr/bin/env python3
"""
Image Optimizer Module for SEO Machine

Optimizes generated images for web use by resizing and compressing.
Called after user approves generated images.

Usage:
    python image_optimizer.py --input "path/to/image.png" --output "path/to/optimized.png"
    python image_optimizer.py --dir "path/to/images/" --web  # Optimize all images in directory

    Or import as module:
    from data_sources.modules.image_optimizer import optimize_image, optimize_for_web
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


# Target dimensions for web
WEB_DIMENSIONS = {
    "banner": (1920, 960),      # Blog banner
    "linkedin": (1080, 1080),   # LinkedIn square
}

# Quality settings
WEBP_QUALITY = 85  # Good balance of quality and size (better than JPEG for vectors)
JPEG_QUALITY = 85  # Fallback for older systems
PNG_COMPRESSION = 6  # 0-9, higher = smaller file but slower


def optimize_image(
    input_path: str,
    output_path: str = None,
    max_width: int = None,
    max_height: int = None,
    quality: int = WEBP_QUALITY,
    format: str = "WEBP"
) -> dict:
    """
    Optimize a single image for web use.

    Args:
        input_path: Path to source image
        output_path: Path for optimized image (default: adds _web suffix)
        max_width: Maximum width (maintains aspect ratio)
        max_height: Maximum height (maintains aspect ratio)
        quality: Quality 1-100 (default: 85)
        format: Output format - "WEBP" (default), "JPEG", or "PNG"

    Returns:
        dict with success, path, original_size, optimized_size, reduction
    """
    result = {
        "success": False,
        "path": None,
        "original_size": 0,
        "optimized_size": 0,
        "reduction_percent": 0,
        "error": None
    }

    try:
        input_file = Path(input_path)
        if not input_file.exists():
            result["error"] = f"File not found: {input_path}"
            return result

        result["original_size"] = input_file.stat().st_size

        # Open image
        img = Image.open(input_path)

        # Convert to RGB if necessary (for JPEG output)
        if format == "JPEG" and img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Resize if dimensions specified
        if max_width or max_height:
            original_width, original_height = img.size

            # Calculate new dimensions maintaining aspect ratio
            if max_width and max_height:
                # Fit within both constraints
                ratio = min(max_width / original_width, max_height / original_height)
            elif max_width:
                ratio = max_width / original_width
            else:
                ratio = max_height / original_height

            # Only resize if image is larger than target
            if ratio < 1:
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Determine output path
        if output_path is None:
            suffix_map = {"WEBP": ".webp", "JPEG": ".jpg", "PNG": ".png"}
            suffix = suffix_map.get(format, ".webp")
            output_path = input_file.parent / f"{input_file.stem}_web{suffix}"
        else:
            output_path = Path(output_path)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save optimized image
        if format == "WEBP":
            img.save(output_path, "WEBP", quality=quality, method=6)  # method 6 = best compression
        elif format == "JPEG":
            img.save(output_path, "JPEG", quality=quality, optimize=True)
        else:
            img.save(output_path, "PNG", optimize=True, compress_level=PNG_COMPRESSION)

        result["success"] = True
        result["path"] = str(output_path)
        result["optimized_size"] = output_path.stat().st_size
        result["reduction_percent"] = round(
            (1 - result["optimized_size"] / result["original_size"]) * 100, 1
        )

    except Exception as e:
        result["error"] = str(e)

    return result


def optimize_for_web(
    image_dir: str,
    output_dir: str = None,
    quality: int = WEBP_QUALITY
) -> dict:
    """
    Optimize all images in a directory for web use.

    Automatically detects banner and linkedin images and applies
    appropriate dimensions and formats:
    - Banner: WebP (best for blog articles)
    - LinkedIn: PNG kept as-is (LinkedIn may not accept WebP)

    Args:
        image_dir: Directory containing images to optimize
        output_dir: Output directory (default: same as input with _web suffix on files)
        quality: Quality 1-100

    Returns:
        dict with results for each image type
    """
    results = {
        "banner": None,
        "linkedin": None,
        "other": []
    }

    image_path = Path(image_dir)
    if output_dir:
        out_path = Path(output_dir)
    else:
        out_path = image_path

    # Look for image files matching naming convention: [imagetype]-[slug]-[date].png
    # Also supports legacy names: banner.png, linkedin.png
    import glob

    for img_type, dimensions in WEB_DIMENSIONS.items():
        # Skip LinkedIn - original PNG is fine for upload (LinkedIn handles compression)
        if img_type == "linkedin":
            print(f"Skipping {img_type} - original PNG is suitable for LinkedIn upload")
            results[img_type] = {"success": True, "path": None, "note": "Use original PNG for LinkedIn"}
            continue

        # Find source file - try new naming convention first, then legacy
        source_file = None
        for pattern in [f"{img_type}-*.png", f"{img_type}-*.jpg", f"{img_type}.png", f"{img_type}.jpg"]:
            matches = list(image_path.glob(pattern))
            if matches:
                source_file = matches[0]  # Use first match
                break

        if source_file and source_file.exists():
            # Generate output filename: replace .png with _web.webp
            output_filename = source_file.stem + "_web.webp"
            output_file = out_path / output_filename

            print(f"Optimizing {img_type} image (WebP)...")
            result = optimize_image(
                input_path=str(source_file),
                output_path=str(output_file),
                max_width=dimensions[0],
                max_height=dimensions[1],
                quality=quality,
                format="WEBP"
            )

            if result["success"]:
                orig_kb = result["original_size"] / 1024
                opt_kb = result["optimized_size"] / 1024
                print(f"  ✓ {orig_kb:.0f}KB → {opt_kb:.0f}KB ({result['reduction_percent']}% reduction)")
            else:
                print(f"  ✗ Failed: {result['error']}")

            results[img_type] = result

    return results


def main():
    """CLI interface for image optimization."""
    parser = argparse.ArgumentParser(
        description="Optimize images for web use"
    )
    parser.add_argument(
        "--input", "-i",
        help="Path to single image to optimize"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output path for optimized image"
    )
    parser.add_argument(
        "--dir", "-d",
        help="Directory containing images to optimize"
    )
    parser.add_argument(
        "--web", "-w",
        action="store_true",
        help="Optimize for standard web dimensions (banner: 1920x960, linkedin: 1080x1080)"
    )
    parser.add_argument(
        "--quality", "-q",
        type=int,
        default=JPEG_QUALITY,
        help=f"JPEG quality 1-100 (default: {JPEG_QUALITY})"
    )
    parser.add_argument(
        "--max-width",
        type=int,
        help="Maximum width (maintains aspect ratio)"
    )
    parser.add_argument(
        "--max-height",
        type=int,
        help="Maximum height (maintains aspect ratio)"
    )

    args = parser.parse_args()

    if args.dir and args.web:
        # Optimize directory for web
        results = optimize_for_web(args.dir, quality=args.quality)
        print("\nOptimization complete!")

    elif args.input:
        # Optimize single image
        result = optimize_image(
            input_path=args.input,
            output_path=args.output,
            max_width=args.max_width,
            max_height=args.max_height,
            quality=args.quality
        )

        if result["success"]:
            orig_kb = result["original_size"] / 1024
            opt_kb = result["optimized_size"] / 1024
            print(f"✓ Optimized: {args.input}")
            print(f"  {orig_kb:.0f}KB → {opt_kb:.0f}KB ({result['reduction_percent']}% reduction)")
            print(f"  Saved to: {result['path']}")
        else:
            print(f"✗ Failed: {result['error']}")
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
