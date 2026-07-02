from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# 폴더 안 이미지에 워터마크 삽입 하기

# 폴더 경로 설정
INPUT_FOLDER = Path("images") # 현재 경로의 images 폴더
OUTPUT_FOLDER = Path("watermarked")

# 출력 폴더 생성
OUTPUT_FOLDER.mkdir(exist_ok=True)


# 워터마크 설정
WATERMARK_TEXT = "Ray's photo"

FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf" # Arial Bold 폰트
FONT_SIZE = 60 # 폰트 크기
ROTATE_ANGLE = 20 # 폰트 회전 각도

# 지원 이미지 확장자 (.jpg, .jpeg, .png 파일)
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

# 워터마크 삽입 함수
def add_watermark(image_path):

    # 이미지 열기
    image = Image.open(image_path).convert("RGBA")

    # 투명 레이어 생성
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(overlay)

    # 폰트 설정
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # 텍스트 크기 계산
    bbox = draw.textbbox((0, 0), WATERMARK_TEXT, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # 중앙 좌표 계산
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    # 워터마크를 넣을 위치(x, y), 내용, 글꼴, 색상을 정합니다.
    draw.text(
        (x, y), # 워터마크를 삽입할 좌표
        WATERMARK_TEXT, # 내용
        font=font, # 글꼴
        fill=(255, 255, 255, 70) # 색상 (r, g, b, alpha(투명도))
    )

  # 텍스트 회전
    overlay = overlay.rotate(ROTATE_ANGLE)

    # 원본 + 워터마크 합성
    watermarked = Image.alpha_composite(image, overlay)
    watermarked.show()

    # 저장 경로
    output_path = OUTPUT_FOLDER / image_path.name

    # RGB 변환 후 저장
    watermarked.convert("RGB").save(output_path)
   

    print(f"[DONE] {image_path.name}")



# 폴더 안 전체 이미지 처리
def process_images():

    print("\n=== Watermark Process Start ===\n")

    for image_path in INPUT_FOLDER.iterdir():

        # 파일인지 확인
        if image_path.is_file():

            # 이미지 확장자 검사
            if image_path.suffix.lower() in IMAGE_EXTENSIONS:

                add_watermark(image_path) # 워터마크 삽입 함수 호출

    print("\n=== All Images Processed ===")



# =========================
# 실행
# =========================
if __name__ == "__main__":
    process_images() 

