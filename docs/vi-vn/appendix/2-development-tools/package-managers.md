# Trình quản lý gói

> 💡 **Hướng dẫn học tập**: Viết code không cần phải "tự tạo lại bánh xe" từ đầu – 99% chức năng đã có người viết và phát hành trên internet. **Trình quản lý gói** chính là công cụ giúp bạn tìm, tải xuống và quản lý những "linh kiện có sẵn" này. Chương này xoay quanh một câu hỏi cốt lõi: **Làm thế nào để các dependency của code có thể tái tạo, cộng tác và dễ bảo trì?**

---

## 0. Tại sao bạn chắc chắn sẽ dùng trình quản lý gói?

Hãy tưởng tượng bạn muốn viết một chương trình Node.js có thể gửi yêu cầu HTTP. Có hai cách:

-   **Cách A (thủ công)**: Tự mình triển khai kết nối TCP, phân tích giao thức HTTP, xử lý chuyển hướng, cơ chế timeout... Ước tính phải viết hàng nghìn dòng code, gỡ lỗi vài tháng.
-   **Cách B (trình quản lý gói)**: `npm install axios`, mười giây, một dòng code là xong.

Bản chất trình quản lý gói là **"cửa hàng ứng dụng" của code**. Nó giúp bạn:

1.  Tìm thư viện do người khác phát hành trên kho lưu trữ trung tâm (Registry)
2.  Tự động tải xuống và cài đặt vào dự án của bạn
3.  Xử lý các thư viện khác mà thư viện này tự nó phụ thuộc (dependency của dependency)
4.  Ghi lại phiên bản chính xác bạn đang sử dụng, giúp việc cộng tác nhóm không gặp vấn đề

---

## 1. Tổng quan về các trình quản lý gói trong hệ sinh thái ngôn ngữ / hệ thống

Các ngôn ngữ lập trình và hệ điều hành khác nhau có chuỗi công cụ hệ sinh thái riêng, nhưng logic cơ bản hoàn toàn giống nhau.

👇 **Hãy thử nhấp vào**: Chọn hệ sinh thái bạn quen thuộc để khám phá các công cụ quản lý gói phổ biến của nó.

<PackageManagerOverviewDemo />

### 1.1 Tải gói ở đâu? — Registry (Kho lưu trữ)

Mỗi hệ sinh thái đều có một kho lưu trữ trung tâm, nơi chứa tất cả các gói có thể tải xuống:

| Hệ sinh thái | Registry | Số lượng gói |
| :--- | :--- | :--- |
| JavaScript | [npmjs.com](https://npmjs.com) | 2 triệu+ |
| Python | [pypi.org](https://pypi.org) | 500 nghìn+ |
| Rust | [crates.io](https://crates.io) | 150 nghìn+ |
| Go | [pkg.go.dev](https://pkg.go.dev) | 500 nghìn+ |
| Công cụ macOS/Linux | [formulae.brew.sh](https://formulae.brew.sh) | 7000+ |
| Phần mềm Windows | [winget.run](https://winget.run) / [chocolatey.org](https://chocolatey.org) | Hàng chục nghìn |

### 1.2 So sánh ba ông lớn JavaScript: npm vs yarn vs pnpm

Chức năng tương tự nhau, khác biệt chủ yếu nằm ở **tốc độ và dung lượng đĩa**:

```text
Dung lượng đĩa: pnpm (chia sẻ hard link) < yarn PnP (không node_modules) < npm (sao chép đầy đủ)
Tốc độ cài đặt: pnpm ≈ yarn > npm
Thói quen sử dụng: npm (phổ biến nhất) > pnpm (khuyên dùng cho dự án mới) > yarn (một số nhóm)
```

**Khuyên dùng**: Dự án mới dùng `pnpm`, dự án hiện có giữ nguyên công cụ cũ, không nên tùy tiện chuyển đổi.

### 1.3 So sánh ba ông lớn Windows: winget vs Chocolatey vs Scoop

| | winget | Chocolatey | Scoop |
| :--- | :--- | :--- | :--- |
| **Hỗ trợ chính thức** | Microsoft chính thức | Bên thứ ba | Bên thứ ba |
| **Cần quyền admin** | Một số cần | Có | **Không cần** |
| **Phù hợp cho** | Cài đặt phần mềm hàng ngày | Triển khai hàng loạt cho doanh nghiệp | Quản lý công cụ phát triển |
| **Số lượng gói** | Nhiều và tăng nhanh | Nhiều nhất (10000+) | Tập trung vào công cụ phát triển |

**Khuyên dùng**: Hàng ngày dùng `winget`, công cụ phát triển dùng `scoop`, tự động hóa doanh nghiệp dùng `Chocolatey`.

---

## 2. Cài đặt gói — Điều gì đã xảy ra đằng sau?

Sau khi nhập `npm install axios`, dòng lệnh im lặng vài giây rồi hoàn tất. Điều gì đã xảy ra trong vài giây đó?

👇 **Hãy thử nhấp vào**: Chọn một gói, nhấp "Chạy", quan sát toàn bộ quá trình cài đặt.

<PackageInstallDemo />

### 2.1 Giải thích chi tiết bốn giai đoạn

**① Phân giải dependency (Resolve)**

Trình quản lý gói trước tiên "hiểu" bạn muốn cài đặt gì. Ví dụ với `axios`, bản thân nó phụ thuộc vào `follow-redirects`, `form-data` và các gói khác, tất cả những gói này cũng cần được cài đặt. Quá trình này được gọi là **xây dựng cây dependency**.

**② Tải xuống (Fetch)**

Tải xuống tất cả các gói cần thiết từ Registry (dưới dạng file nén `.tgz`). Các trình quản lý gói thông minh sẽ:
-   Tải xuống nhiều gói song song, thay vì chờ từng gói một
-   Kiểm tra cache cục bộ trước, nếu có thì không cần truy cập mạng

**③ Liên kết (Link)**

Giải nén các gói đã tải xuống vào thư mục `node_modules/` và xử lý các mối quan hệ tham chiếu.

**④ Ghi file khóa (Lockfile)**

Ghi **phiên bản chính xác** của lần cài đặt này vào `package-lock.json` (hoặc `yarn.lock` / `pnpm-lock.yaml`).

### 2.2 Tra cứu nhanh các lệnh phổ biến nhất

```bash
# ── JavaScript (npm) ──────────────────────────────────
npm install              # Cài đặt tất cả dependency theo package.json
npm install axios        # Cài đặt gói mới (dependency sản xuất)
npm install -D jest      # Cài đặt devDependency (chỉ dùng khi phát triển)
npm install -g tsx       # Cài đặt toàn cục (có thể dùng ở bất kỳ thư mục nào)
npm uninstall axios      # Gỡ cài đặt gói
npm update               # Nâng cấp tất cả gói lên phiên bản mới nhất tương thích
npm run build            # Chạy script trong package.json scripts
npx create-react-app .   # Chạy tạm thời, không cài đặt vào dự án

# ── Python (pip) ──────────────────────────────────────
pip install requests           # Cài đặt gói
pip install requests==2.28.0   # Cài đặt phiên bản cụ thể
pip freeze > requirements.txt  # Xuất danh sách dependency hiện tại
pip install -r requirements.txt # Cài đặt theo danh sách

# ── Rust (cargo) ──────────────────────────────────────
cargo add serde    # Thêm dependency (sẽ tự động cập nhật Cargo.toml)
cargo build        # Build dự án
cargo test         # Chạy test
cargo run          # Chạy dự án

# ── Go (go mod) ───────────────────────────────────────
go get github.com/gin-gonic/gin  # Thêm dependency
go mod tidy                      # Sắp xếp dependency (xóa thừa, bổ sung thiếu)
go build ./...                   # Build

# ── Windows (winget) ──────────────────────────────────
winget install Git.Git           # Cài đặt phần mềm
winget upgrade --all             # Cập nhật tất cả phần mềm đã cài đặt
```

### 2.3 npm scripts là gì?

Trong `package.json` có một trường `scripts`, đây là **trình chạy tác vụ** tích hợp sẵn của npm:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "jest",
    "lint": "eslint src/"
  }
}
```

Cách chạy: `npm run dev`, `npm run build`. Lợi ích của việc này là:
-   **Điểm vào thống nhất**: Thành viên trong nhóm không cần nhớ các lệnh cụ thể của công cụ cấp thấp
-   **Cấu hình môi trường tự động**: Khi chạy, `node_modules/.bin` sẽ tự động được thêm vào PATH, cho phép sử dụng trực tiếp các công cụ đã cài đặt cục bộ

---

## 3. Cài đặt toàn cục vs Cài đặt cục bộ

Đây là một trong những khái niệm mà người mới dễ bị nhầm lẫn nhất.

### 3.1 Sự khác biệt giữa hai loại

```bash
npm install axios        # Cài đặt cục bộ: cài vào ./node_modules/, chỉ dự án hiện tại có thể dùng
npm install -g typescript  # Cài đặt toàn cục: cài vào thư mục hệ thống, bất kỳ dự án/thư mục nào cũng có thể dùng
```

| | Cài đặt cục bộ | Cài đặt toàn cục |
| :--- | :--- | :--- |
| **Vị trí lưu trữ** | `./node_modules/` | Thư mục cấp hệ thống (ví dụ: `/usr/local/lib/`) |
| **Phù hợp cho** | Thư viện dependency của dự án (axios, vue, react) | Công cụ dòng lệnh (tsc, eslint, create-react-app) |
| **Cô lập phiên bản** | Mỗi dự án phiên bản độc lập ✅ | Toàn máy dùng chung một phiên bản ⚠️ |
| **Tính nhất quán nhóm** | Lockfile đảm bảo nhất quán ✅ | Phiên bản của mỗi người có thể khác nhau ⚠️ |

### 3.2 Quy tắc vàng

> **Dependency dạng thư viện (axios, lodash, vue) luôn cài đặt cục bộ;  
> Công cụ dòng lệnh (tsc, eslint) ưu tiên cài đặt cục bộ, dùng `npx` để gọi.**

**Tại sao công cụ dòng lệnh cũng nên cài đặt cục bộ?**

Giả sử bạn đã cài đặt `eslint@8` toàn cục, nhưng dự án A cần các quy tắc mới của `eslint@9`, bạn sẽ phải liên tục chuyển đổi giữa phiên bản toàn cục và dự án. Cài đặt `eslint` cục bộ, dùng `npx eslint .` để gọi, mỗi dự án có thể cấu hình phiên bản riêng của mình.

### 3.3 npx — Chạy tạm thời, không làm ô nhiễm môi trường

`npx` là trình chạy công cụ tích hợp sẵn của npm, cho phép bạn **chạy một gói mà không cần cài đặt** nó:

```bash
# Không cài đặt create-vue, chạy trực tiếp để khởi tạo dự án
npx create-vue my-project

# Không cài đặt prettier, định dạng file trực tiếp
npx prettier --write src/

# Buộc sử dụng phiên bản cụ thể (bỏ qua phiên bản đã cài đặt)
npx typescript@5.4 tsc --version
```

`uvx` của Python, `cargo run` của Rust cũng cung cấp khả năng "chạy tạm thời" tương tự:

```bash
uvx ruff check .       # Python: Chạy tạm thời công cụ kiểm tra ruff
cargo install ripgrep  # Rust: Cài đặt toàn cục, trở thành lệnh hệ thống rg
```

---

## 4. Bí mật của số phiên bản — Semantic Versioning (Phiên bản ngữ nghĩa)

Bạn sẽ thấy nội dung như thế này trong `package.json`:

```json
{
  "dependencies": {
    "axios": "^1.6.8",
    "typescript": "~5.4.0"
  }
}
```

`^` và `~` ở đây có nghĩa là gì?

👇 **Hãy thử nhấp vào**: Di chuột qua các phần của số phiên bản để hiểu ý nghĩa; nhấp vào ký hiệu phạm vi để xem những phiên bản nào sẽ được chấp nhận.

<DependencyTreeDemo />

### 4.1 Tại sao không khóa cứng phiên bản?

| Cách làm | Ưu điểm | Nhược điểm |
| :--- | :--- | :--- |
| `"axios": "1.6.8"` (khóa chính xác) | Hoàn toàn có thể dự đoán | Các bản vá bảo mật không thể tự động cập nhật |
| `"axios": "^1.6.8"` (phạm vi tương thích, khuyên dùng) | Tự động nhận các bản sửa lỗi và tính năng mới | Rất hiếm khi gây ra sự không tương thích nhỏ |
| `"axios": "*"` (bất kỳ phiên bản nào) | Luôn là mới nhất | Nâng cấp phiên bản MAJOR có thể phá vỡ code hoàn toàn |

**Thực hành tốt nhất**: Dùng `^` để khai báo phạm vi + lockfile để cố định phiên bản thực tế, kết hợp cả hai.

### 4.2 Dependency Hell là gì?

Khi bạn phụ thuộc vào 50 gói, mỗi gói lại phụ thuộc vào một số gói khác, "cây dependency" có thể có hàng trăm node. Nếu hai gói bạn phụ thuộc cần **cùng một thư viện nhưng ở các phiên bản không tương thích**, thì sẽ xảy ra "xung đột dependency".

Giải pháp của các hệ sinh thái:
-   **npm v3+**: Các phiên bản MAJOR giống nhau được nâng lên cấp cao nhất để chia sẻ, các phiên bản MAJOR khác nhau được cài đặt riêng.
-   **pnpm**: Hard link + cô lập nghiêm ngặt, về cơ bản ngăn chặn "Phantom Dependency" (gói không khai báo nhưng vẫn có thể sử dụng).
-   **cargo (Rust)**: Ngôn ngữ buộc mỗi gói chỉ có thể phụ thuộc vào cùng một phiên bản, loại bỏ hoàn toàn xung đột.
-   **go mod (Go)**: Chiến lược Minimal Version Selection (MVS), chọn phiên bản thấp nhất có thể đáp ứng tất cả các ràng buộc.

---

## 5. Lockfile — Nền tảng của sự cộng tác nhóm

### 5.1 Tại sao cần lockfile?

Giả sử `package.json` ghi `"axios": "^1.6.0"`:

-   Bạn cài đặt hôm nay → cài đặt `1.6.8`
-   Đồng đội cài đặt ngày mai → có thể cài đặt `1.7.0` (vừa phát hành tối qua)
-   Máy chủ CI tuần tới → có thể cài đặt `1.7.1`

Cùng một đoạn code, ba người chạy ra ba kết quả khác nhau. **Lockfile** ghi lại phiên bản chính xác của mỗi gói, mọi người cài đặt theo nó, kết quả hoàn toàn nhất quán.

| Kịch bản | Lệnh | Hành vi |
| :--- | :--- | :--- |
| Đồng bộ môi trường phát triển | `npm install` | Cài đặt theo lockfile, không nâng cấp phiên bản |
| Triển khai CI / sản xuất | `npm ci` | Cài đặt **nghiêm ngặt** theo lockfile, nếu có khác biệt sẽ báo lỗi ngay |
| Chủ động nâng cấp phiên bản | `npm update` | Nâng cấp trong phạm vi cho phép, và cập nhật lockfile |

### 5.2 Lockfile có nên được commit vào Git không?

**Ứng dụng phải commit, thư viện phát hành lên npm có thể không commit.**

-   ✅ **Ứng dụng Web, dịch vụ Backend**: Bắt buộc phải commit, đảm bảo môi trường triển khai và môi trường phát triển hoàn toàn nhất quán.
-   ❌ **Thư viện phát hành npm**: Thường không commit, người dùng thư viện có lockfile riêng của họ.
-   ✅ **Dự án Python**: `requirements.txt` bản thân nó đóng vai trò lockfile, nên commit.
-   ✅ **Dự án Go**: `go.sum` bắt buộc phải commit, dùng để kiểm tra tính toàn vẹn.

---

## 6. Môi trường ảo Python

Python có một khái niệm đặc biệt cần chú ý: **môi trường ảo (venv)**.

**Tại sao cần?**

Python mặc định cài đặt gói **toàn cục**. Dự án A của bạn cần `requests==2.28`, dự án B cần `requests==2.31`, cả hai sẽ xung đột với nhau.

**Giải pháp**: Tạo môi trường ảo độc lập cho mỗi dự án, không can thiệp lẫn nhau.

```bash
# 1. Tạo môi trường ảo (chạy tại thư mục gốc của dự án)
python -m venv .venv

# 2. Kích hoạt môi trường ảo
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows (Command Prompt CMD)
.venv\Scripts\Activate.ps1       # Windows (PowerShell)

# 3. Sau khi kích hoạt, pip install chỉ ảnh hưởng đến môi trường ảo hiện tại, không làm ô nhiễm toàn cục
pip install requests

# 4. Thoát môi trường ảo
deactivate
```

> ⚠️ **Vấn đề thường gặp trên Windows**: PowerShell mặc định cấm chạy script, cần thực hiện lệnh sau trước:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**Các giải pháp thay thế hiện đại**:
-   `conda create -n myproject python=3.11` — Quản lý cả phiên bản Python.
-   `uv venv && source .venv/bin/activate` — Viết bằng Rust, tốc độ tạo cực nhanh.

**`.venv` có nên commit vào Git không?**

Không! `.venv` được tạo cục bộ trên máy, nên thêm vào `.gitignore`. Dùng `requirements.txt` hoặc `pyproject.toml` để mô tả dependency.

---

## 7. Tra cứu nhanh các vấn đề thường gặp

**Q: `node_modules` có nên commit vào Git không?**

Không! Thường có vài trăm MB, nên thêm vào `.gitignore`. Với `package-lock.json`, bất kỳ ai cũng có thể `npm install` để xây dựng lại nhanh chóng.

**Q: Cài đặt thất bại / xuất hiện lỗi lạ thì làm sao?**

```bash
# Xóa cache, xóa cài đặt cũ, làm lại từ đầu
npm cache clean --force
rm -rf node_modules package-lock.json   # macOS/Linux
rmdir /s /q node_modules && del package-lock.json  # Windows CMD
npm install
```

**Q: Tốc độ cài đặt quá chậm?**

```bash
# Chuyển sang mirror trong nước (khuyên dùng ghi vào file .npmrc, không làm ô nhiễm toàn cục)
echo "registry=https://registry.npmmirror.com" > .npmrc

# pip cũng có thể cấu hình mirror
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q: Gói có lỗ hổng bảo mật thì xử lý thế nào?**

```bash
npm audit          # Quét các lỗ hổng đã biết
npm audit fix      # Tự động sửa các lỗ hổng tương thích
npm audit fix --force  # Buộc nâng cấp (có thể gây phá vỡ, dùng cẩn thận)
```

**Q: Làm sao để biết một gói có đáng tin cậy không?**

Kiểm tra trên [npmjs.com](https://npmjs.com) hoặc [bundlephobia.com](https://bundlephobia.com):
-   Số lượt tải xuống hàng tuần (càng cao càng đáng tin cậy)
-   Thời gian cập nhật cuối cùng (cẩn thận nếu hơn 2 năm không cập nhật)
-   Số lượng dependency (càng nhiều dependency, khả năng gây vấn đề càng lớn)
-   Số GitHub Stars và mức độ hoạt động của Issues

**Q: Phần mềm cài đặt bằng winget trên Windows nằm ở đâu?**

winget mặc định cài đặt vào thư mục hệ thống (cần quyền admin) hoặc `%LOCALAPPDATA%\Microsoft\WindowsApps`. Phần mềm cài đặt bằng Scoop thống nhất nằm ở `%USERPROFILE%\scoop\apps\`, thuận tiện cho việc quản lý và di chuyển.

---

## 8. Bảng đối chiếu thuật ngữ

| Thuật ngữ tiếng Anh | Đối chiếu tiếng Việt | Giải thích |
| :--- | :--- | :--- |
| **Package** | Gói / Thư viện | Module code đã được người khác viết và phát hành |
| **Registry** | Registry / Kho lưu trữ | Máy chủ lưu trữ trung tâm của tất cả các gói (ví dụ: npmjs.com) |
| **Dependency** | Dependency | Các gói khác mà dự án của bạn cần để chạy |
| **devDependency** | DevDependency | Các gói chỉ cần trong giai đoạn phát triển (framework test, công cụ build, v.v.) |
| **Lockfile** | Lockfile | Ghi lại số phiên bản chính xác, đảm bảo tính nhất quán của môi trường |
| **SemVer** | Semantic Versioning | Quy tắc đặt tên phiên bản MAJOR.MINOR.PATCH |
| **node_modules** | Thư mục module | Thư mục thực tế nơi npm cài đặt các gói |
| **venv** | Môi trường ảo | Sandbox cô lập gói độc lập cho dự án Python |
| **tarball** | Tarball | Định dạng phân phối gói, thường là file `.tgz` |
| **Hoisting** | Hoisting | npm nâng các sub-dependency lên cấp cao nhất để tránh cài đặt trùng lặp |
| **Phantom Dependency** | Phantom Dependency | Gói không được khai báo trong file cấu hình nhưng vẫn có thể sử dụng (pnpm có thể ngăn chặn) |
| **npx** | — | Trình chạy gói tích hợp của npm, chạy gói tạm thời mà không cần cài đặt |
| **go.sum** | — | File kiểm tra hash của module Go, ngăn chặn dependency bị giả mạo |
| **Crate** | — | Tên đơn vị "gói" trong hệ sinh thái Rust |
| **winget** | — | Trình quản lý gói chính thức của Windows (tích hợp sẵn trong Windows 10/11) |

---

## Tóm tắt: Bản chất của trình quản lý gói

Bốn câu để ghi nhớ cốt lõi:

1.  **Trình quản lý gói = Cửa hàng ứng dụng**: Giúp bạn tìm, cài đặt, quản lý các linh kiện code, không cần lặp lại công việc.
2.  **Lockfile = Hợp đồng nhóm**: Cố định phiên bản chính xác, biến câu "chạy tốt trên máy tôi" thành quá khứ.
3.  **Semantic Versioning = Ngôn ngữ giao tiếp**: `^` an toàn để nhận cập nhật, phiên bản MAJOR thay đổi thì cần cẩn thận.
4.  **Cục bộ > Toàn cục**: Dependency của dự án nên cài đặt cục bộ, `npx` / `uvx` chạy công cụ tạm thời, giữ môi trường sạch sẽ.
