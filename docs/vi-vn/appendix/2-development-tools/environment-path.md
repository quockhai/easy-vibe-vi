# Biến môi trường và PATH

> 💡 **Hướng dẫn học tập**: Mỗi khi bạn nhập `git` hoặc `python` vào terminal, hệ thống cần tìm xem chương trình đó nằm ở đâu. Mỗi khi code của bạn gọi API của mô hình lớn, chương trình cần biết sử dụng khóa API nào. Đằng sau hai việc này là cùng một cơ chế – **biến môi trường**.

---

## 0. Mỗi chương trình đều mang theo một bộ cấu hình

Mỗi chương trình đang chạy đều giữ một bộ cấu hình "khóa=giá trị", được gọi là **biến môi trường**. Chương trình có thể đọc các cấu hình này bất cứ lúc nào để hiểu môi trường chạy hiện tại.

Nhấp vào bất kỳ biến nào trong danh sách dưới đây và "xem" giá trị của nó trong terminal:

<EnvVarOverviewDemo />

---

## 1. PATH: Cách Shell tìm thấy lệnh bạn nhập

`PATH` là một biến môi trường đặc biệt, chứa một chuỗi các đường dẫn thư mục (phân tách bằng dấu hai chấm). Khi bạn nhập `git`, Shell sẽ theo thứ tự của chuỗi thư mục này, lần lượt đi vào từng thư mục để tìm file thực thi có tên `git` – tìm thấy cái đầu tiên sẽ dừng ngay lập tức.

```bash
$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Chọn một lệnh, quan sát quá trình Shell tìm kiếm từng thư mục:

<PathSearchDemo />

**Ba quy tắc quan trọng**:
- Thư mục càng nằm ở đầu trong PATH, độ ưu tiên càng cao
- Tìm thấy cái đầu tiên sẽ dừng, không tiếp tục tìm kiếm
- Không tìm thấy ở bất kỳ thư mục nào → `command not found`

---

## 2. Tại sao phải khởi động lại terminal sau khi cài đặt công cụ?

Khi cài đặt các công cụ như nvm, Homebrew, conda, script cài đặt sẽ tự động thêm một dòng vào `~/.zshrc` để đưa thư mục của nó vào PATH:

```bash
# Nội dung được script cài đặt tự động ghi (ví dụ)
export PATH="/usr/local/opt/python@3.12/bin:$PATH"
```

Dòng code này chỉ được thực thi khi **Shell mới khởi động**. Các cửa sổ terminal đã mở sẽ không bị ảnh hưởng, vì vậy:

```bash
# Có thể có hiệu lực ngay lập tức mà không cần khởi động lại
source ~/.zshrc
```

**Các trường hợp phổ biến với công cụ phát triển AI**:

```bash
# Ollama / pipx cài xong báo command not found
which ollama          # Kiểm tra vị trí cài đặt thực tế

# Đường dẫn công cụ CLI được cài đặt bằng pip (thêm vào PATH)
# macOS: ~/Library/Python/3.x/bin
# Linux: ~/.local/bin
export PATH="$PATH:$HOME/.local/bin"

# Nên dùng pipx để cài đặt công cụ dòng lệnh, tự động quản lý PATH
pipx install aider-chat
```

---

## 3. Phạm vi của biến: Ai có thể nhìn thấy biến này?

Biến môi trường không được phát sóng cho tất cả các chương trình – mỗi tiến trình giữ **một bản sao riêng** của mình, được kế thừa từ tiến trình cha, việc sửa đổi bản sao của mình sẽ không ảnh hưởng đến tiến trình cha.

Biểu đồ dưới đây minh họa ba cấp độ. Trong "cấp người dùng", hãy `export` một biến mới và xem liệu nó có xuất hiện ở "cấp tiến trình" không:

<EnvScopeDemo />

---

## 4. export: Quyết định liệu tiến trình con có thể đọc biến này không

Khi thiết lập biến, việc có thêm `export` hay không là hai việc hoàn toàn khác nhau:

<EnvExportDemo />

Để biến tồn tại vĩnh viễn qua các phiên, hãy ghi `export` vào file cấu hình:

```bash
# macOS (zsh)
echo 'export MY_VAR="value"' >> ~/.zshrc
source ~/.zshrc       # Có hiệu lực ngay lập tức, không cần mở lại terminal

# Linux (bash)
echo 'export MY_VAR="value"' >> ~/.bashrc
source ~/.bashrc
```

---

## 5. Khóa API: Tuyệt đối không được viết vào code

Khi gọi các API như OpenAI, Anthropic, DeepSeek, khóa API chính là "chứng minh thư + thẻ tín dụng" của bạn. Nếu bị lộ, người khác có thể sử dụng hạn mức của bạn để tiêu dùng, và bạn sẽ phải chịu chi phí.

Lỗi phổ biến nhất là viết trực tiếp khóa API vào code:

<ApiKeyDangerDemo />

---

## 6. Phát triển cục bộ: Dùng file .env để quản lý khóa API

Khi phát triển cục bộ, hãy đặt khóa API vào file `.env` trong thư mục gốc của dự án, code sẽ đọc thông qua thư viện dotenv. File `.env` phải được thêm vào `.gitignore`, không được commit lên Git.

Bên trái viết cấu hình, bên phải đọc – chuyển đổi ngôn ngữ để xem hai cách viết:

<DotEnvDemo />

---

## 7. Môi trường sản xuất: Để nền tảng vận hành tự động inject khóa API

`.env` là một công cụ tiện lợi trong giai đoạn phát triển. Trên máy chủ và nền tảng đám mây, **môi trường vận hành** phải chịu trách nhiệm inject khóa API, bản thân code hoàn toàn không cần biết khóa API được đặt ở đâu:

<ServerSecretDemo />

---

## 8. Xử lý sự cố thực tế

### `command not found`

```bash
# Bước 1: Xác nhận xem có trong PATH không
which python3         # Nếu có output nghĩa là đã tìm thấy

# Bước 2: Tìm vị trí thực tế của chương trình (macOS)
brew list python | grep bin

# Bước 3: Thêm thư mục vào PATH
export PATH="/đường_dẫn_tìm_thấy:$PATH"
source ~/.zshrc       # Sau khi ghi vào file cấu hình nhớ source
```

### Cài đặt hai phiên bản, nhưng lại dùng phiên bản không mong muốn

```bash
which python
# /usr/bin/python ← Phiên bản cũ của hệ thống, nằm ở đầu PATH

# Đặt thư mục của phiên bản mới lên đầu PATH
export PATH="/usr/local/bin:$PATH"

which python
# /usr/local/bin/python ← Phiên bản mới, bây giờ được ưu tiên
```

### Biến đã được thiết lập, nhưng chương trình không đọc được

| Nguyên nhân | Giải pháp |
|:---|:---|
| Quên `export` | Thêm `export` rồi thử lại |
| Đã sửa `~/.zshrc` nhưng chưa có hiệu lực | `source ~/.zshrc` |
| Đã dùng `.env` nhưng chưa cài dotenv | `pip install python-dotenv` / `npm install dotenv` |
| Trên máy chủ chỉ có hiệu lực trong phiên SSH | Thay bằng systemd `EnvironmentFile` |

---

## Tra cứu thuật ngữ nhanh

| Thuật ngữ | Ý nghĩa |
|:---|:---|
| **PATH** | Lưu trữ danh sách các thư mục Shell tìm kiếm file thực thi, phân tách bằng dấu hai chấm, thứ tự quyết định độ ưu tiên |
| **export** | Đánh dấu biến là có thể kế thừa, tiến trình con tự động nhận bản sao khi khởi động |
| **source** | Thực thi lại file cấu hình trong Shell hiện tại, làm cho thay đổi có hiệu lực ngay lập tức |
| **which** | Hiển thị đường dẫn file thực thi tương ứng với một lệnh (kết quả tìm kiếm của PATH) |
| **.env** | File cấu hình cục bộ của dự án, lưu trữ khóa API dùng cho phát triển, phải được thêm vào `.gitignore` |
| **.env.example** | Mẫu với tên biến đầy đủ, giá trị để trống, có thể commit an toàn lên Git |
| **chmod 600** | Quyền file: Chỉ chủ sở hữu có thể đọc và ghi, phù hợp để bảo vệ file khóa API |
| **Secret Scanner** | Các nền tảng như GitHub tự động quét rò rỉ khóa API, sau khi phát hiện sẽ thông báo cho nhà cung cấp để thu hồi |
