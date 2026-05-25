import argparse
import sys
from PIL import Image

THEMES = {
    "dark": "@%#*+=-:. ",
    "light": " .:-=+*#%@"
}


def convert_to_ascii(input_path, output_path, width, height, theme):
    try:
        img = Image.open(input_path)
    except Exception as e:
        return f"Ошибка: не удалось открыть файл {input_path}. {e}"
    img = img.resize((width, height))
    img = img.convert("L")
    chars = THEMES.get(theme, THEMES["dark"])
    num_chars = len(chars)
    pixels = img.get_flattened_data()
    ascii_str = ""
    for i, pixel in enumerate(pixels):
        ascii_str += chars[pixel * (num_chars - 1) // 255]
        if (i + 1) % width == 0:
            ascii_str += "\n"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ascii_str)
    except Exception as e:
        return f"Ошибка при записи в файл: {e}"

    return ascii_str


def main():
    parser = argparse.ArgumentParser(description="Преобразование изображения в ASCII-арт.")
    parser.add_argument("input", help="Путь к исходному изображению")
    parser.add_argument("output", help="Путь к выходному текстовому файлу")
    parser.add_argument("cols", type=int, help="Ширина результата (в столбцах/символах)")
    parser.add_argument("rows", type=int, help="Высота результата (в строках)")
    parser.add_argument("--theme", choices=["dark", "light"], default="dark",
                        help="Тема оформления (по умолчанию: dark)")
    args = parser.parse_args()
    result = convert_to_ascii(args.input, args.output, args.cols, args.rows, args.theme)
    if result.startswith("Ошибка"):
        print(result)
        sys.exit(1)
    else:
        print(f"Успешно сохранено в: {args.output}")
        print("\n--- Просмотр ---")
        print(result)


if __name__ == "__main__":
    main()