from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np

def create_plot(numbers):
    plt.figure(figsize=(6, 3))
    plt.bar(range(len(numbers)), numbers)
    plt.xticks([])
    plt.savefig("plot.png", bbox_inches="tight")
    plt.close()
    return "plot.png"

def generate_infographic(data, output_file="infographic.png"):
    img = Image.new("RGB", (800, 1200), "white")
    draw = ImageDraw.Draw(img)
    y_offset = 20
    
    # Заголовок
    font = ImageFont.truetype("arial.ttf", 28)
    draw.text((20, y_offset), "Основные выводы", fill="navy", font=font)
    y_offset += 50
    
    # Ключевые пункты
    font = ImageFont.truetype("arial.ttf", 18)
    for point in data["key_points"][:3]:
        draw.text((40, y_offset), f"• {point}", fill="black", font=font)
        y_offset += 40
    
    # Числовые данные
    if data["numbers"]:
        plot_path = create_plot(data["numbers"])
        plot = Image.open(plot_path)
        img.paste(plot, (50, y_offset))
        y_offset += 200
    
    # Факты
    draw.rectangle([20, y_offset, 780, y_offset+2], fill="gray")
    y_offset += 20
    for fact in data["facts"][:3]:
        draw.text((40, y_offset), f"→ {fact}", fill="darkgreen", font=font)
        y_offset += 40
    
    img.save(output_file)
    return output_file
