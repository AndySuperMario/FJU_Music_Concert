from PIL import Image, ImageDraw, ImageFont
import qrcode

# ===== 基本設定 =====
W, H = 1600, 2000
bg = (248, 244, 232)
ink = (40, 40, 40)
gold = (191, 155, 89)
muted = (120, 110, 90)

url = "https://andysupermario.github.io/FJU_Music_Concert/"

# ===== 建立畫布 =====
canvas = Image.new("RGB", (W, H), bg)
d = ImageDraw.Draw(canvas)

# ===== 字體（請確認路徑）=====
font_path = "C:/Windows/Fonts/msjh.ttc"  # 微軟正黑體
def font(size):
    return ImageFont.truetype(font_path, size)

title_font = font(int(W * 0.10))
sub_font   = font(int(W * 0.045))
cta_font   = font(int(W * 0.035))

# ===== 置中函式 =====
def center_text(y, text, fnt, fill):
    bbox = d.textbbox((0,0), text, font=fnt)
    text_w = bbox[2] - bbox[0]
    d.text(((W - text_w)/2, y), text, font=fnt, fill=fill)

# ===== 標題 =====
center_text(180, "音樂會節目冊", title_font, ink)
center_text(350, "Concert Program", sub_font, muted)

# ===== 分隔線 =====
d.line([W//2-150, 450, W//2+150, 450], fill=gold, width=4)

# ===== 產生 QR code =====
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2,
)
qr.add_data(url)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
qr_size = 900
qr_img = qr_img.resize((qr_size, qr_size))

# ===== QR 外框（設計感）=====
qr_x = (W - qr_size) // 2
qr_y = 550

# 外框
d.rounded_rectangle(
    [qr_x-40, qr_y-40, qr_x+qr_size+40, qr_y+qr_size+40],
    radius=40,
    outline=gold,
    width=4
)

canvas.paste(qr_img, (qr_x, qr_y))

# ===== 底部文字 =====
center_text(1500, "掃描 QR code 觀看完整節目冊", cta_font, ink)

# ===== 儲存 =====
canvas.save("final_qrcode_design.png", dpi=(300,300))