import sys


def srgb_channel(channel):
    """Convert one 0–255 sRGB channel to linear light."""
    value = channel / 255.0
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def relative_luminance(red, green, blue):
    """WCAG relative luminance for an sRGB color."""
    return (
        0.2126 * srgb_channel(red)
        + 0.7152 * srgb_channel(green)
        + 0.0722 * srgb_channel(blue)
    )


def contrast_ratio(luminance_a, luminance_b):
    lighter = max(luminance_a, luminance_b)
    darker = min(luminance_a, luminance_b)
    return (lighter + 0.05) / (darker + 0.05)


def parse_hex(text):
    cleaned = text.strip().lstrip("#")
    if len(cleaned) != 6:
        raise ValueError("use a 6-digit hex color such as 1B4F72")
    try:
        return tuple(int(cleaned[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError as error:
        raise ValueError("use a 6-digit hex color such as 1B4F72") from error


def grade_normal_text(ratio):
    if ratio >= 7:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3:
        return "AA Large only"
    return "Fail"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: Two hex colors are required.")
        sys.exit(1)

    try:
        red_a, green_a, blue_a = parse_hex(sys.argv[1])
        red_b, green_b, blue_b = parse_hex(sys.argv[2])
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)

    luminance_a = relative_luminance(red_a, green_a, blue_a)
    luminance_b = relative_luminance(red_b, green_b, blue_b)
    ratio = contrast_ratio(luminance_a, luminance_b)
    grade = grade_normal_text(ratio)
    print(
        f"Contrast ratio of #{sys.argv[1].strip().lstrip('#').upper()} "
        f"on #{sys.argv[2].strip().lstrip('#').upper()} is {ratio:.2f}:1 "
        f"({grade} for normal text)."
    )
