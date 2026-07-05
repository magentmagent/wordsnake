from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "social-card.png"
OUT_VERSIONED = ROOT / "public" / "social-card-v2.png"

W, H = 1200, 630
BG = "#f4efe6"
INK = "#20242a"
MUTED = "#d8d0c2"
TILE = "#fffdf8"
EMPTY = "#eadfce"
ACCENT = "#0f777d"


def font(name, size):
    path = Path("C:/Windows/Fonts") / name
    return ImageFont.truetype(str(path), size)


title_font = font("arialbd.ttf", 98)
panel_title_font = font("arialbd.ttf", 30)
tile_font = font("arialbd.ttf", 43)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow_triangle(draw, a, b, size=15):
    ax, ay = a
    bx, by = b
    mx = (ax + bx) / 2
    my = (ay + by) / 2
    if abs(bx - ax) > abs(by - ay):
        sign = 1 if bx > ax else -1
        pts = [(mx + sign * size, my), (mx - sign * size * 0.65, my - size * 0.75), (mx - sign * size * 0.65, my + size * 0.75)]
    else:
        sign = 1 if by > ay else -1
        pts = [(mx, my + sign * size), (mx - size * 0.75, my - sign * size * 0.65), (mx + size * 0.75, my - sign * size * 0.65)]
    draw.polygon(pts, fill=ACCENT)


def draw_centered_text(draw, box, text, fnt, fill):
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 2), text, font=fnt, fill=fill)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    x = 82
    y = 88
    for line in ["Word", "Chain", "Snake"]:
        draw.text((x, y), line, font=title_font, fill=INK)
        y += 104

    panel = (708, 56, 1122, 574)
    rounded(draw, panel, 28, "#fffaf1", MUTED, 3)
    draw.text((754, 102), "Valid chain path", font=panel_title_font, fill=ACCENT)

    size = 62
    gap = 12
    left = 750
    top = 158

    letters = {
        (0, 0): "S",
        (1, 0): "T",
        (2, 0): "O",
        (3, 0): "N",
        (4, 0): "E",
        (4, 1): "A",
        (4, 2): "G",
        (4, 3): "L",
        (4, 4): "E",
        (3, 4): "E",
        (2, 4): "L",
    }
    path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4)]

    centers = {}
    for row in range(5):
        for col in range(5):
            cx = left + col * (size + gap)
            cy = top + row * (size + gap)
            centers[(col, row)] = (cx + size / 2, cy + size / 2)
            fill = TILE if (col, row) in letters else EMPTY
            rounded(draw, (cx, cy, cx + size, cy + size), 8, fill, "#d8d0c2", 2)

    for a, b in zip(path, path[1:]):
        arrow_triangle(draw, centers[a], centers[b])

    for key, letter in letters.items():
        cx, cy = centers[key]
        draw_centered_text(draw, (cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2), letter, tile_font, INK)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)
    img.save(OUT_VERSIONED, optimize=True)
    print(f"wrote {OUT}")
    print(f"wrote {OUT_VERSIONED}")


if __name__ == "__main__":
    main()
