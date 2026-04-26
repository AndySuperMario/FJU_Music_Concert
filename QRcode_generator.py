# from PIL import Image, ImageDraw, ImageFont
# import qrcode

# # ===== 基本設定 =====
# W, H = 1600, 2000
# bg = (248, 244, 232)
# ink = (40, 40, 40)
# gold = (191, 155, 89)
# muted = (120, 110, 90)

# url = "https://andysupermario.github.io/FJU_Music_Concert/"

# # ===== 建立畫布 =====
# canvas = Image.new("RGB", (W, H), bg)
# d = ImageDraw.Draw(canvas)

# # ===== 字體（請確認路徑）=====
# font_path = "C:/Windows/Fonts/msjh.ttc"  # 微軟正黑體
# def font(size):
    # return ImageFont.truetype(font_path, size)

# title_font = font(int(W * 0.10))
# sub_font   = font(int(W * 0.045))
# cta_font   = font(int(W * 0.035))

# # ===== 置中函式 =====
# def center_text(y, text, fnt, fill):
    # bbox = d.textbbox((0,0), text, font=fnt)
    # text_w = bbox[2] - bbox[0]
    # d.text(((W - text_w)/2, y), text, font=fnt, fill=fill)

# # ===== 標題 =====
# center_text(180, "音樂會節目冊", title_font, ink)
# center_text(350, "Concert Program", sub_font, muted)

# # ===== 分隔線 =====
# d.line([W//2-150, 450, W//2+150, 450], fill=gold, width=4)

# # ===== 產生 QR code =====
# qr = qrcode.QRCode(
    # error_correction=qrcode.constants.ERROR_CORRECT_H,
    # box_size=10,
    # border=2,
# )
# qr.add_data(url)
# qr.make(fit=True)

# qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
# qr_size = 900
# qr_img = qr_img.resize((qr_size, qr_size))

# # ===== QR 外框（設計感）=====
# qr_x = (W - qr_size) // 2
# qr_y = 550

# # 外框
# d.rounded_rectangle(
    # [qr_x-40, qr_y-40, qr_x+qr_size+40, qr_y+qr_size+40],
    # radius=40,
    # outline=gold,
    # width=4
# )

# canvas.paste(qr_img, (qr_x, qr_y))

# # ===== 底部文字 =====
# center_text(1500, "掃描 QR code 觀看完整節目冊", cta_font, ink)

# # ===== 儲存 =====
# canvas.save("final_qrcode_design.png", dpi=(300,300))



from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
import random
import math

# ===== 基本設定 =====
W, H = 1600, 2000

bg = (248, 244, 232)          # 米白背景
paper = (252, 248, 238)       # QR 內底
ink = (42, 42, 40)            # 深灰字 / QR
gold = (191, 155, 89)         # 金色線條
gold_light = (215, 188, 128)  # 淡金
muted = (120, 110, 90)        # 英文副標
wash_gray = (150, 150, 138)   # 水墨灰
wash_warm = (202, 174, 118)   # 暖金水墨

url = "https://andysupermario.github.io/FJU_Music_Concert/"

# ===== 建立畫布 =====
canvas = Image.new("RGB", (W, H), bg)
d = ImageDraw.Draw(canvas)

# ===== 字體 =====
font_path = "C:/Windows/Fonts/msjh.ttc"  # Windows 微軟正黑體

def font(size):
    return ImageFont.truetype(font_path, size)

title_font = font(150)
sub_font   = font(72)
cta_font   = font(52)

# ===== 置中函式 =====
def center_text(y, text, fnt, fill, spacing=0):
    bbox = d.textbbox((0, 0), text, font=fnt)
    text_w = bbox[2] - bbox[0]
    d.text(((W - text_w) / 2, y), text, font=fnt, fill=fill)

# ===== 背景水墨效果 =====
def add_watercolor_blob(base, center, color, size, alpha=45, count=28):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)

    cx, cy = center
    for _ in range(count):
        rx = random.randint(-size, size)
        ry = random.randint(-size // 2, size // 2)
        r = random.randint(size // 3, size)
        a = random.randint(alpha // 3, alpha)

        ld.ellipse(
            [cx + rx - r, cy + ry - r, cx + rx + r, cy + ry + r],
            fill=color + (a,)
        )

    layer = layer.filter(ImageFilter.GaussianBlur(radius=35))
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")

random.seed(7)

canvas = add_watercolor_blob(canvas, (230, 1450), wash_gray, 280, alpha=38)
canvas = add_watercolor_blob(canvas, (1280, 1430), wash_gray, 320, alpha=34)
canvas = add_watercolor_blob(canvas, (350, 1650), wash_warm, 240, alpha=32)
canvas = add_watercolor_blob(canvas, (1120, 1630), wash_warm, 230, alpha=26)

d = ImageDraw.Draw(canvas)

# ===== 金色細線 / 山水感線條 =====
def draw_gold_curve(points, width=3):
    for i in range(len(points) - 1):
        d.line([points[i], points[i + 1]], fill=gold_light, width=width)

draw_gold_curve([
    (100, 1550), (230, 1490), (420, 1470), (620, 1410),
    (780, 1370), (950, 1340), (1180, 1280), (1460, 1200)
], width=3)

draw_gold_curve([
    (980, 1560), (1120, 1510), (1270, 1460), (1440, 1390)
], width=2)

# ===== 標題 =====
center_text(170, "音樂會節目冊", title_font, ink)
center_text(345, "Concert Program", sub_font, muted)

# ===== 分隔線 =====
d.line([W // 2 - 150, 455, W // 2 + 150, 455], fill=gold, width=4)

# ===== QR code 設定 =====
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,   # 建議保留 4，掃描比較安全
)
qr.add_data(url)
qr.make(fit=True)

matrix = qr.get_matrix()
modules = len(matrix)

# ===== QR 尺寸與位置 =====
qr_size = 860
cell = qr_size / modules

qr_x = (W - qr_size) // 2
qr_y = 610

panel_pad = 70
panel_x1 = qr_x - panel_pad
panel_y1 = qr_y - panel_pad
panel_x2 = qr_x + qr_size + panel_pad
panel_y2 = qr_y + qr_size + panel_pad

# ===== QR 外框陰影 =====
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle(
    [panel_x1 + 12, panel_y1 + 18, panel_x2 + 12, panel_y2 + 18],
    radius=48,
    fill=(80, 60, 30, 34)
)
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=18))
canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB")
d = ImageDraw.Draw(canvas)

# ===== QR 外框底色 =====
d.rounded_rectangle(
    [panel_x1, panel_y1, panel_x2, panel_y2],
    radius=48,
    fill=paper,
    outline=gold,
    width=4
)

# 內層細框
inner_gap = 18
d.rounded_rectangle(
    [panel_x1 + inner_gap, panel_y1 + inner_gap, panel_x2 - inner_gap, panel_y2 - inner_gap],
    radius=36,
    outline=(211, 184, 126),
    width=2
)

# 四角裝飾線，讓它更像節目冊細框
corner_len = 95
corner_r = 32
for sx, sy in [
    (panel_x1 + 28, panel_y1 + 28),
    (panel_x2 - 28, panel_y1 + 28),
    (panel_x1 + 28, panel_y2 - 28),
    (panel_x2 - 28, panel_y2 - 28),
]:
    pass

# ===== QR code 內底 =====
qr_bg_pad = 18
d.rounded_rectangle(
    [qr_x - qr_bg_pad, qr_y - qr_bg_pad, qr_x + qr_size + qr_bg_pad, qr_y + qr_size + qr_bg_pad],
    radius=24,
    fill=(255, 252, 244)
)

# ===== 畫圓角 QR 格子 =====
# 注意：不要改成太淡、太細，否則掃不到
module_color = (38, 38, 36)
radius_ratio = 0.22   # 0.15~0.25 比較安全；不要太圓

for row in range(modules):
    for col in range(modules):
        if matrix[row][col]:
            x1 = qr_x + col * cell
            y1 = qr_y + row * cell
            x2 = qr_x + (col + 1) * cell
            y2 = qr_y + (row + 1) * cell

            r = cell * radius_ratio
            d.rounded_rectangle(
                [x1, y1, x2, y2],
                radius=r,
                fill=module_color
            )

# ===== 補強三個定位角，讓掃描更穩 =====
# 這段會讓三個大角比較乾淨、像設計款，但仍維持 QR 結構
def draw_finder(row, col):
    x = qr_x + col * cell
    y = qr_y + row * cell
    s = 7 * cell

    # 清掉該區
    d.rounded_rectangle(
        [x, y, x + s, y + s],
        radius=cell * 1.2,
        fill=(255, 252, 244)
    )

    # 外框
    d.rounded_rectangle(
        [x, y, x + s, y + s],
        radius=cell * 1.4,
        fill=module_color
    )

    # 中間白框
    inset1 = cell * 1.15
    d.rounded_rectangle(
        [x + inset1, y + inset1, x + s - inset1, y + s - inset1],
        radius=cell * 0.9,
        fill=(255, 252, 244)
    )

    # 中心黑塊
    inset2 = cell * 2.25
    d.rounded_rectangle(
        [x + inset2, y + inset2, x + s - inset2, y + s - inset2],
        radius=cell * 0.45,
        fill=module_color
    )

# qrcode.get_matrix() 已包含 border，所以定位角位置是 border 開始
b = qr.border
draw_finder(b, b)
draw_finder(b, modules - b - 7)
draw_finder(modules - b - 7, b)

# ===== 底部文字 =====
center_text(1550, "掃描 QR code 觀看完整節目冊", cta_font, ink)

# ===== 輕微紙張質感 =====
noise = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd = ImageDraw.Draw(noise)
for _ in range(2600):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    a = random.randint(5, 13)
    nd.point((x, y), fill=(120, 105, 80, a))

canvas = Image.alpha_composite(canvas.convert("RGBA"), noise).convert("RGB")

# ===== 儲存 =====
canvas.save("final_qrcode_design_v3.png", dpi=(300, 300))
print("完成：final_qrcode_design_v3.png")