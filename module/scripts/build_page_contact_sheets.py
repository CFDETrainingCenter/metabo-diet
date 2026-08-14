#!/usr/bin/env python3
"""Create labeled contact sheets for visual review of rendered document pages."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def page_number(path: Path) -> int:
    match = re.search(r"page-(\d+)\.png$", path.name)
    if not match:
        raise ValueError(f"Unexpected page filename: {path.name}")
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--pages-per-sheet", type=int, default=8)
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--thumb-width", type=int, default=440)
    args = parser.parse_args()

    pages = sorted(args.input_dir.glob("page-*.png"), key=page_number)
    if not pages:
        raise SystemExit(f"No rendered pages found in {args.input_dir}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()

    for start in range(0, len(pages), args.pages_per_sheet):
        batch = pages[start : start + args.pages_per_sheet]
        with Image.open(batch[0]) as first:
            ratio = first.height / first.width
        thumb_height = round(args.thumb_width * ratio)
        label_height = 24
        gutter = 16
        rows = math.ceil(len(batch) / args.columns)
        width = args.columns * args.thumb_width + (args.columns + 1) * gutter
        height = rows * (thumb_height + label_height) + (rows + 1) * gutter
        sheet = Image.new("RGB", (width, height), "#d8ddd9")
        draw = ImageDraw.Draw(sheet)

        for index, page_path in enumerate(batch):
            row, column = divmod(index, args.columns)
            x = gutter + column * (args.thumb_width + gutter)
            y = gutter + row * (thumb_height + label_height + gutter)
            with Image.open(page_path) as page:
                thumbnail = page.convert("RGB").resize(
                    (args.thumb_width, thumb_height), Image.Resampling.LANCZOS
                )
            sheet.paste(thumbnail, (x, y + label_height))
            draw.rectangle((x, y, x + args.thumb_width, y + label_height), fill="#102a2c")
            draw.text((x + 8, y + 6), f"Page {page_number(page_path)}", fill="white", font=font)

        end = page_number(batch[-1])
        output = args.output_dir / f"pages-{page_number(batch[0]):03d}-{end:03d}.png"
        sheet.save(output, optimize=True)


if __name__ == "__main__":
    main()
