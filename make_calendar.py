from calendar import month
from turtle import left
from PIL import Image, ImageDraw, ImageFont
import datetime as dt
import yaml


def make_calendar(input_yaml="calendar.yaml",output_path="sample.png"):
    image = Image.new("RGB", (500,600), "white")
    draw = ImageDraw.Draw(image)
    with open(input_yaml) as f:
        calendar = yaml.safe_load(f) 
    for calendar_index, year_month in enumerate(calendar.keys()):
        ## サイズの初期化
        margin = 30
        left_top = (margin, margin + int(image.height/2)*calendar_index)
        right_bottom = (image.width - margin, int(image.height/2 - margin) + int(image.height/2)*calendar_index)
        cell_size = ((right_bottom[0] - left_top[0])/7, ( right_bottom[1] - left_top[1])/6)
        ## 日付の初期化
        year, month = map(int, year_month.split("_"))
        date = dt.date(year, month, 1)
        day = date.strftime('%a')
        DAY_LIST = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        first_day = DAY_LIST.index(day)
        font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 10, encoding="unic")
        ## 縦線の表示
        for x_times in range(8):
            x1 = left_top[0] + cell_size[0]*x_times
            y1 = left_top[1]
            x2 = x1 
            y2 = right_bottom[1]
            draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=1)
        ## 横線の表示
        for y_times in range(7):
            x1 = left_top[0]
            y1 = left_top[1] + cell_size[1]*y_times
            x2 = right_bottom[0]
            y2 = y1
            draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=1)
        ## 年月の表示
        draw.text((left_top[0], left_top[1] - margin), f"{year}/{month}", "black", font=font)
        ## 曜日名の表示
        for x_times in range(7):
            y = left_top[1] - int(margin/2)
            x = left_top[0] + cell_size[0]*x_times
            color = ["black","black","black","black","black","blue","red"][x_times]
            draw.text((x+int(cell_size[0]/10),y), DAY_LIST[x_times], color, font=font)
        ## 各日付の表示
        index = 0
        for y_times in range(6):
            for x_times in range(7):
                x = left_top[0] + cell_size[0]*x_times
                y = left_top[1] + cell_size[1]*y_times
                date_str = str(index - first_day + 1)
                ## 
                if date_str in  calendar[year_month]:
                    bg_color = "white" if calendar[year_month][date_str] == "empty" else (192,192,192)
                    draw.rectangle((x, y, x+cell_size[0], y+cell_size[1]), fill=bg_color, outline="black")
                else:
                    date_str = "-"
                    draw.rectangle((x, y, x+cell_size[0], y+cell_size[1]), fill=(192,192,192), outline="black")
                color = ["black","black","black","black","black","blue","red"][x_times]
                draw.text((x+int(cell_size[0]/10),y+int(cell_size[1]/10)), date_str, color, font=font)
                index += 1
    image.save(output_path)

if __name__ == "__main__":
    make_calendar()
