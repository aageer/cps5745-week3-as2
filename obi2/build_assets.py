"""Build the Linux-lab banner and the standalone dynamic visualization."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

import plotly.express as px

ROOT = Path(__file__).resolve().parent


def _chunk(tag: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


GLYPHS = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "G": ["01111", "10000", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "4": ["10010", "10010", "10010", "11111", "00010", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
}


def blit(pixels, width, text, origin_x, origin_y, scale, color):
    cursor = origin_x
    for character in text:
        glyph = GLYPHS[character]
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit != "1":
                    continue
                for dy in range(scale):
                    for dx in range(scale):
                        x = cursor + col * scale + dx
                        y = origin_y + row * scale + dy
                        if 0 <= x < width and 0 <= y < len(pixels) // width:
                            pixels[y * width + x] = color
        cursor += 6 * scale


def write_banner(path: Path) -> None:
    width, height = 960, 280
    navy = (15, 61, 115)
    gold = (184, 146, 46)
    cream = (247, 243, 234)
    white = (255, 255, 255)
    pixels = []
    for y in range(height):
        for x in range(width):
            if y < 18 or y > height - 19:
                pixels.append(gold)
            elif 70 < y < 210 and 48 < x < width - 48:
                pixels.append(navy)
            else:
                pixels.append(cream)
    blit(pixels, width, "AKHIL AGEER", 88, 102, 6, white)
    blit(pixels, width, "CPS 5745", 88, 156, 4, gold)
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        raw.extend(channel for pixel in pixels[y * width : (y + 1) * width] for channel in pixel)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    path.write_bytes(png)


def write_dynamic_viz(path: Path) -> None:
    frame = px.data.gapminder()
    figure = px.scatter(
        frame,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=58,
        animation_frame="year",
        animation_group="country",
        range_x=[100, 100000],
        range_y=[25, 90],
        title="Life expectancy and income, 1952–2007",
        labels={
            "gdpPercap": "GDP per capita (log scale)",
            "lifeExp": "Life expectancy (years)",
            "continent": "Continent",
            "pop": "Population",
        },
        category_orders={
            "continent": ["Africa", "Americas", "Asia", "Europe", "Oceania"]
        },
    )
    figure.update_layout(
        paper_bgcolor="#f7f3ea",
        plot_bgcolor="#fffdf8",
        font={"family": "Avenir Next, Segoe UI, sans-serif", "color": "#1d2430"},
        title={"x": 0.02, "xanchor": "left"},
        legend_title_text="Continent (click to hide)",
        margin={"l": 70, "r": 30, "t": 70, "b": 70},
    )
    chart = figure.to_html(
        include_plotlyjs=True,
        full_html=False,
        config={"displaylogo": False, "responsive": True},
    )
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dynamic visualization · Akhil Ageer</title>
  <style>
    body {{
      margin: 0;
      background: #f7f3ea;
      color: #1d2430;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
    }}
    header {{ max-width: 1100px; margin: 0 auto; padding: 28px 20px 0; }}
    h1 {{
      font-family: "Iowan Old Style", Palatino, Georgia, serif;
      font-size: 2rem;
      margin: 0 0 8px;
    }}
    p {{ max-width: 78ch; line-height: 1.5; }}
    .chart {{ max-width: 1100px; margin: 0 auto; padding: 8px 12px 40px; }}
    a {{ color: #0f3d73; }}
  </style>
</head>
<body>
  <header>
    <h1>Dynamic visualization</h1>
    <p>Akhil Ageer · CPS 5745 Interactive Information Visualization · Week 3 AS2 extra credit.</p>
    <p>Press play or drag the year slider. Hover a bubble for the country, and click a continent in the legend to filter it. Bubble area is population. Data: Plotly’s built-in Gapminder table (country, year, life expectancy, GDP per capita, population).</p>
    <p><a href="MyPage.html">Back to MyPage</a></p>
  </header>
  <div class="chart">
    {chart}
  </div>
</body>
</html>
"""
    path.write_text(page, encoding="utf-8")


def main() -> None:
    write_banner(ROOT / "kean_banner.png")
    write_dynamic_viz(ROOT / "dynamic_viz.html")
    print("wrote", ROOT / "kean_banner.png")
    print("wrote", ROOT / "dynamic_viz.html", (ROOT / "dynamic_viz.html").stat().st_size)


if __name__ == "__main__":
    main()
