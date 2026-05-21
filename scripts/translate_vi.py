import os
import glob
import re
import time
import argparse

try:
    import google.generativeai as genai
except ImportError:
    print("Vui lòng cài đặt thư viện google-generativeai bằng lệnh: pip install google-generativeai")
    exit(1)

# Thiết lập cấu hình
DOCS_DIR = "docs/vi-vn"
MODEL_NAME = "gemini-2.5-flash"  # Sử dụng flash để tiết kiệm chi phí và tăng tốc độ

SYSTEM_INSTRUCTION = """
Bạn là một chuyên gia dịch thuật và một kỹ sư phần mềm (Full Stack Developer).
Nhiệm vụ của bạn là dịch toàn bộ nội dung Markdown từ tiếng Trung (hoặc tiếng Anh) sang tiếng Việt.

Yêu cầu BẮT BUỘC:
1. Dịch đầy đủ, chính xác, dễ hiểu. Văn phong mượt mà, tự nhiên, dễ đọc.
2. Giữ nguyên 100% các thuật ngữ kỹ thuật tiếng Anh (ví dụ: PM, Full Stack Dev, Vibe Coding, IDE, API, Frontend, Backend, Model Context Protocol, RAG, v.v...). Tuyệt đối không dịch những từ này sang tiếng Việt (nhà phát triển toàn diện, v.v...).
3. Giữ nguyên ĐỊNH DẠNG Markdown: YAML Frontmatter (--- ... ---), HTML/Vue Component tags (vd: <HomeFeatures />, <script setup>), link, hình ảnh, code block. 
4. KHÔNG dịch các khóa (key) trong YAML (như `title`, `description`, `layout`...), chỉ dịch nội dung (value).
5. Khi dịch, hãy chắc chắn sửa các lỗi gõ chữ cơ bản của tiếng Việt (ví dụ: nếu bạn định viết "NgườI MớI", "ngườI học" thì phải viết đúng thành "Người Mới", "người học").
6. Chỉ trả về nội dung đã dịch, KHÔNG giải thích, KHÔNG bọc kết quả trong markdown code block (ví dụ: ```markdown) trừ khi chính nội dung gốc bắt đầu/kết thúc bằng code block.
"""

def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def translate_content(model, content, max_retries=3):
    prompt = f"Hãy dịch nội dung Markdown sau sang tiếng Việt, tuân thủ nghiêm ngặt các quy tắc đã đề ra:\n\n{content}"
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                )
            )
            result = response.text.strip()
            # Xử lý trường hợp mô hình bọc kết quả trong markdown code block
            if result.startswith("```markdown"):
                result = result[11:]
            if result.startswith("```"):
                result = result[3:]
            if result.endswith("```"):
                result = result[:-3]
            
            return result.strip() + "\n" # Đảm bảo file kết thúc bằng newline
        except Exception as e:
            print(f"  [Lỗi] Lần thử {attempt + 1}: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
            
    return None

def main():
    parser = argparse.ArgumentParser(description="Script tự động dịch docs/vi-vn sang tiếng Việt bằng Google Gemini.")
    parser.add_argument("--api-key", type=str, help="Google Gemini API Key. Nếu không cung cấp, sẽ lấy từ biến môi trường GEMINI_API_KEY")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Lỗi: Không tìm thấy API Key. Vui lòng cung cấp qua --api-key hoặc biến môi trường GEMINI_API_KEY.")
        exit(1)

    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION
    )

    md_files = glob.glob(f"{DOCS_DIR}/**/*.md", recursive=True)
    files_to_translate = []

    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if contains_chinese(content):
                files_to_translate.append((file_path, content))

    print(f"Tìm thấy {len(files_to_translate)} file có chứa tiếng Trung cần dịch.")

    for i, (file_path, content) in enumerate(files_to_translate, 1):
        print(f"[{i}/{len(files_to_translate)}] Đang dịch: {file_path}")
        
        translated_text = translate_content(model, content)
        if translated_text:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(translated_text)
            print(f"  -> Xong.")
        else:
            print(f"  -> Thất bại: Bỏ qua file này.")
            
        # Thêm sleep nhỏ để tránh rate limit nếu dùng free tier
        time.sleep(2)

if __name__ == "__main__":
    main()
