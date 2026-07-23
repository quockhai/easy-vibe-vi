# Cổng và localhost

> 💡 **Hướng dẫn học tập**: Khi bạn chạy `npm run dev` và thấy `http://localhost:5173` xuất hiện trong terminal, bạn có bao giờ tự hỏi: `localhost` là gì? `5173` đại diện cho điều gì? Tại sao đôi khi lại báo lỗi `EADDRINUSE`? Chương này sẽ giải thích cặn kẽ những khái niệm thường gặp hàng ngày trong quá trình phát triển nhưng ít khi được tìm hiểu sâu.

Trước khi bắt đầu, bạn nên bổ sung hai "viên gạch nền tảng" sau:

-   **Kiến thức cơ bản về mạng**: Nếu bạn chưa rõ về khái niệm địa chỉ IP và HTTP, bạn có thể xem phần [Kiến thức cơ bản về máy tính - Giao tiếp mạng](../1-computer-fundamentals/network-fundamentals.md) trước.
-   **Kiến thức cơ bản về Terminal**: Nếu bạn chưa quen với dòng lệnh terminal, bạn có thể xem phần [Dòng lệnh và Shell Script](./command-line-shell.md) trước.

---

## 0. Giới thiệu: `localhost:5173` mà chúng ta thấy hàng ngày rốt cuộc là gì?

<DevServerFlowDemo />

Mỗi nhà phát triển đều không thể thiếu dòng output này:

```
➜  Local:   http://localhost:5173/
```

Nhưng bạn có bao giờ nghĩ rằng, trong dòng chữ ngắn ngủi này, ẩn chứa vài khái niệm quan trọng:

-   **http://** → Giao thức truyền thông (ngôn ngữ để giao tiếp)
-   **localhost** → Địa chỉ đích (tìm ai)
-   **:5173** → Số cổng (sau khi tìm thấy, gõ cửa nào)

Hiểu rõ ba điều này, bạn sẽ nắm được 90% các vấn đề mạng trong môi trường phát triển. Tiếp theo chúng ta sẽ phân tích từng phần.

---

## 1. Cổng là gì? (IP là tòa nhà, cổng là số phòng)

### 1.1 Một phép ẩn dụ trực quan

Hãy tưởng tượng một máy chủ là một tòa nhà:

-   **Địa chỉ IP** (ví dụ `192.168.1.100`) chính là địa chỉ của tòa nhà – cho bạn biết "đi tòa nhà nào".
-   **Số cổng** (ví dụ `:80`) chính là số phòng trong tòa nhà – cho bạn biết "vào phòng nào".

Trong một tòa nhà có thể đồng thời có nhà hàng (phòng số 80), quán cà phê (phòng số 443), văn phòng (phòng số 22). Tương tự, trên một máy tính có thể đồng thời chạy Web server, cơ sở dữ liệu, dịch vụ SSH, mỗi dịch vụ chiếm một cổng khác nhau.

👇 **Thực hành thử**:
Nhấp vào "số phòng" bên dưới để mô phỏng việc tạo kết nối đến các cổng khác nhau. Hãy chú ý quan sát: điều gì sẽ xảy ra khi cổng "mở" (có chương trình đang lắng nghe) và khi cổng "đóng"?

<PortAnalogyDemo />

### 1.2 Phạm vi giá trị của số cổng

Số cổng là một số nguyên nằm trong khoảng **0–65535** (tổng cộng 65536 cổng). Nhiều cổng như vậy được chia thành ba khoảng:

| Khoảng | Phạm vi | Mục đích sử dụng | Ví dụ |
| :--- | :--- | :--- | :--- |
| **Cổng hệ thống** | 0 – 1023 | Dành riêng cho các giao thức chuẩn, người dùng thông thường không thể tùy tiện chiếm dụng | 80 (HTTP), 443 (HTTPS), 22 (SSH) |
| **Cổng đã đăng ký** | 1024 – 49151 | Dành cho các ứng dụng phổ biến đăng ký sử dụng | 3306 (MySQL), 5432 (PostgreSQL), 6379 (Redis) |
| **Cổng động** | 49152 – 65535 | Hệ điều hành cấp phát tạm thời | Khi trình duyệt gửi yêu cầu, hệ thống sẽ ngẫu nhiên cấp phát một cổng nguồn |

> Tại sao các development server của bạn thường dùng 3000, 5173, 8080? Bởi vì những cổng này nằm trong phạm vi "cổng đã đăng ký", không yêu cầu quyền quản trị viên để lắng nghe, và cũng ít khi xung đột với các dịch vụ hệ thống.

### 1.3 Tra cứu nhanh các số cổng phổ biến trong phát triển

👇 **Thực hành thử**:
Nhập số cổng hoặc tên dịch vụ để tìm kiếm, nhấp vào bất kỳ dòng nào để mở rộng và xem ví dụ sử dụng.

<CommonPortsDemo />

---

## 2. localhost là gì? (Tự tìm chính mình)

### 2.1 Khái niệm cốt lõi của "loopback"

`localhost` là một tên miền đặc biệt, nó luôn trỏ đến **chính máy tính của bạn**.

Khi bạn nhập `http://localhost:3000` vào trình duyệt, những điều sau đây sẽ xảy ra:

1.  Trình duyệt hỏi hệ điều hành: "IP của `localhost` là bao nhiêu?"
2.  Hệ điều hành trả lời trực tiếp: "`127.0.0.1`" (không cần kết nối mạng để tra cứu DNS)
3.  Gói dữ liệu được gửi đến `127.0.0.1`, nhưng **sẽ không thực sự rời khỏi máy cục bộ**
4.  Hệ điều hành thông qua "loopback interface" (giao diện loopback) để **gửi ngược** gói dữ liệu trở lại
5.  Chương trình đang lắng nghe trên cổng 3000 nhận được yêu cầu và trả về phản hồi

**Toàn bộ quá trình không đi qua dây mạng, không đi qua router, không cần kết nối mạng.**

👇 **Thực hành thử**:
Nhấp vào "Gửi yêu cầu" để quan sát toàn bộ hành trình của gói dữ liệu. Sau đó nhấp vào "thẻ thông tin" bên dưới để tìm hiểu các cách viết và sự khác biệt của localhost.

<LocalhostLoopbackDemo />

### 2.2 `localhost` so với `127.0.0.1` so với `0.0.0.0`

Ba khái niệm này thường bị nhầm lẫn, nhưng ý nghĩa của chúng hoàn toàn khác nhau:

| Cách viết | Ý nghĩa | Ai có thể truy cập |
| :--- | :--- | :--- |
| `localhost` / `127.0.0.1` | Địa chỉ loopback, chỉ máy cục bộ | Chỉ máy tính của chính bạn |
| `0.0.0.0` | Lắng nghe tất cả các giao diện mạng | Máy cục bộ + các thiết bị khác trong mạng LAN |
| `192.168.x.x` | IP mạng LAN | Các thiết bị trong mạng LAN |

**Tình huống thực tế**:

```bash
# Chỉ mình bạn có thể truy cập (an toàn, phù hợp cho phát triển)
npm run dev -- --host localhost

# Điện thoại cũng có thể truy cập (phù hợp cho debug trên thiết bị di động)
npm run dev -- --host 0.0.0.0
```

> Nhiều framework (như Vite, Next.js) mặc định lắng nghe `localhost`, vì vậy điện thoại của bạn dù có kết nối cùng WiFi cũng không thể truy cập được. Muốn debug bằng điện thoại? Chỉ cần thêm tham số `--host`.

---

## 3. Xung đột cổng: Vấn đề môi trường phát triển phổ biến nhất

### 3.1 Tại sao lại xảy ra xung đột?

**Một cổng tại cùng một thời điểm chỉ có thể được một chương trình lắng nghe.** Điều này giống như một căn phòng chỉ có thể có một hộ gia đình sinh sống.

Nếu bạn cố gắng khởi động dịch vụ thứ hai trên cùng một cổng, bạn sẽ thấy lỗi kinh điển này:

```
Error: listen EADDRINUSE :::3000
```

Dịch ra ngôn ngữ đời thường là: **"Phòng số 3000 đã có người ở rồi, bạn không vào được!"**

Các tình huống xung đột phổ biến:
-   Development server lần trước chưa tắt sạch, vẫn đang chạy ngầm
-   Hai dự án khác nhau sử dụng cùng một cổng mặc định
-   Một dịch vụ hệ thống nào đó đã chiếm dụng cổng bạn muốn

👇 **Thực hành thử**:
Hãy thử khởi động dịch vụ nhiều lần trong trình mô phỏng bên dưới. Khi xảy ra xung đột cổng, hãy so sánh cách xử lý khác nhau giữa "khởi động trực tiếp" và "khởi động thông minh".

<PortConflictDemo />

### 3.2 Khắc phục và giải quyết

Khi gặp xung đột cổng, quy trình khắc phục sự cố rất cố định:

**macOS / Linux:**
```bash
# Bước một: Kiểm tra xem ai đang chiếm dụng cổng 3000
lsof -i :3000

# Bước hai: Sau khi có PID, buộc dừng
kill -9 <PID>
```

**Windows:**
```bash
# Bước một: Kiểm tra xem ai đang chiếm dụng cổng 3000
netstat -ano | findstr :3000

# Bước hai: Dừng tiến trình
taskkill /PID <PID> /F
```

> Nhiều framework hiện đại (Vite, Create React App, v.v.) khi gặp xung đột cổng sẽ tự động hỏi "có muốn đổi sang cổng khác không?". Nhưng việc hiểu rõ nguyên lý cơ bản sẽ giúp bạn khắc phục nhanh hơn những vấn đề khó mà framework không thể giúp được.

---

## 4. "Chính sách cùng nguồn gốc" và CORS trong phát triển

### 4.1 "Nguồn gốc" là gì?

Trình duyệt có một cơ chế bảo mật gọi là **Same-Origin Policy (Chính sách cùng nguồn gốc)**: chỉ khi **giao thức, tên miền, cổng** cả ba đều hoàn toàn giống nhau thì mới được coi là "cùng nguồn gốc".

| Địa chỉ A | Địa chỉ B | Có cùng nguồn gốc không | Lý do |
| :--- | :--- | :--- | :--- |
| `http://localhost:5173` | `http://localhost:5173/about` | ✅ Cùng nguồn gốc | Giao thức, tên miền, cổng đều giống nhau |
| `http://localhost:5173` | `http://localhost:3000` | ❌ Khác nguồn gốc | **Cổng khác nhau** (5173 so với 3000) |
| `http://localhost:5173` | `https://localhost:5173` | ❌ Khác nguồn gốc | **Giao thức khác nhau** (http so với https) |

### 4.2 Tại sao Frontend-Backend tách biệt chắc chắn gặp CORS?

Khi kiến trúc dự án của bạn là:

```
Frontend (Vite)  →  http://localhost:5173
Backend (Express) →  http://localhost:3000
```

Trang Frontend được tải từ `:5173`, sau đó sử dụng `fetch('/api/users')` để gửi yêu cầu đến API của `:3000` – **cổng không giống nhau, kích hoạt hạn chế CORS!**

**Hai giải pháp phổ biến:**

**Giải pháp một: Backend cấu hình CORS**
```javascript
// Backend Express
app.use(cors({ origin: 'http://localhost:5173' }))
```

**Giải pháp hai: Frontend cấu hình Proxy (khuyên dùng)**
```javascript
// vite.config.js
export default {
  server: {
    proxy: {
      '/api': 'http://localhost:3000'
    }
  }
}
```

Nguyên lý của Proxy: Để Vite development server giúp bạn "chuyển tiếp" yêu cầu. Trình duyệt nghĩ rằng nó đang giao tiếp với `:5173` (cùng nguồn gốc), nhưng thực tế Vite đã âm thầm chuyển tiếp yêu cầu đó cho `:3000` ở phía sau.

---

## 5. Khắc phục sự cố thực tế: Ba vấn đề phổ biến nhất

👇 **Thực hành thử**:
Chọn một vấn đề bạn đã từng gặp, sau đó làm theo các bước để khắc phục. Mỗi bước đều có thể nhấp vào "Thực thi" để xem output.

<PortTroubleshootDemo />

---

## 6. Bảng thuật ngữ đối chiếu

| Thuật ngữ tiếng Anh | Đối chiếu tiếng Việt | Giải thích |
| :--- | :--- | :--- |
| **Port** | Cổng | Một số từ 0–65535, dùng để phân biệt các dịch vụ mạng khác nhau trên cùng một máy. Mỗi dịch vụ "lắng nghe" một cổng, chờ đợi kết nối từ client. |
| **localhost** | Máy chủ cục bộ | Một tên miền đặc biệt, luôn trỏ đến máy cục bộ (127.0.0.1). Dùng để truy cập các dịch vụ đang chạy trên máy cục bộ mà không cần kết nối mạng. |
| **Loopback Interface** | Giao diện loopback | Giao diện mạng ảo của hệ điều hành. Các gói dữ liệu gửi đến 127.0.0.1 sẽ không rời khỏi máy cục bộ, mà sẽ "quay trở lại" thông qua giao diện này. |
| **EADDRINUSE** | Địa chỉ đã được sử dụng | Lỗi do Node.js / hệ điều hành báo cáo, cho biết cổng bạn muốn lắng nghe đã bị một chương trình khác chiếm dụng. |
| **CORS** | Chia sẻ tài nguyên đa nguồn gốc | Cơ chế bảo mật của trình duyệt. Khi trang Frontend cố gắng yêu cầu API từ một nguồn gốc khác (giao thức/tên miền/cổng khác), cần có sự cho phép rõ ràng từ Backend. |
| **Same-Origin Policy** | Chính sách cùng nguồn gốc | Nền tảng bảo mật của trình duyệt: chỉ cho phép các yêu cầu cùng giao thức, cùng tên miền, cùng cổng tự do giao tiếp, ngăn chặn việc đọc dữ liệu đa nguồn gốc. |
| **Proxy** | Máy chủ ủy quyền | Trong môi trường phát triển, Proxy server thay thế trình duyệt chuyển tiếp yêu cầu đến Backend, bỏ qua hạn chế cùng nguồn gốc của trình duyệt. |
| **0.0.0.0** | Tất cả các giao diện | Khi dịch vụ lắng nghe 0.0.0.0, điều đó có nghĩa là nó chấp nhận kết nối từ bất kỳ giao diện mạng nào (máy cục bộ, mạng LAN, v.v.). |
| **Well-known Ports** | Cổng nổi tiếng | Tên gọi chung cho các cổng từ 0–1023, dành riêng cho các giao thức chuẩn như HTTP (80), HTTPS (443), SSH (22). |
| **PID** | ID tiến trình | Số định danh duy nhất mà hệ điều hành cấp phát cho mỗi chương trình đang chạy, dùng để quản lý và dừng tiến trình. |
| **lsof** | Liệt kê các tệp đang mở | Lệnh của macOS/Linux, dùng để xem tiến trình nào đang chiếm dụng một cổng cụ thể (`lsof -i :số_cổng`). |
| **HMR** | Thay thế module nóng | Chức năng của development server: sau khi bạn sửa đổi code, trình duyệt tự động cập nhật mà không cần làm mới trang thủ công. Cơ chế bên dưới thông báo cho trình duyệt thông qua WebSocket. |

---

## Tóm tắt

Cổng và localhost là những khái niệm cơ bản và thường gặp nhất trong môi trường phát triển:

-   **Cổng** = "Số nhà" để phân biệt các dịch vụ khác nhau trên một máy (0–65535)
-   **localhost** = Địa chỉ đặc biệt "tự tìm chính mình" (127.0.0.1), dữ liệu không rời khỏi máy cục bộ
-   Bản chất của **xung đột cổng** là "một số nhà chỉ có thể treo một biển"
-   Bản chất của **CORS** là "cổng khác nhau = khác nguồn gốc", cần CORS hoặc Proxy để giải quyết

Ghi nhớ bốn câu này, bạn sẽ có thể nhanh chóng xác định nguyên nhân của hầu hết các vấn đề mạng gặp phải trong môi trường phát triển.
