# Biểu thức chính quy

> 💡 **Hướng dẫn học tập**: Biểu thức chính quy trông như một cuốn sách bí ẩn? Thực ra nó chỉ là một "ngôn ngữ mini" dùng để mô tả các mẫu văn bản. Chương này sẽ giúp bạn từ con số 0 hiểu được tư tưởng cốt lõi của regex, và học cách sử dụng một vài ký hiệu quan trọng để giải quyết 80% vấn đề tìm kiếm và xác thực văn bản.

---

## 0. Tại sao bạn cần biểu thức chính quy?

Hãy tưởng tượng các tình huống sau:
- Tìm tất cả địa chỉ IP từ một đoạn nhật ký dài
- Xác thực định dạng email người dùng nhập có hợp lệ không
- Thay thế tất cả định dạng ngày tháng từ `2024/01/15` thành `2024-01-15` trong văn bản
- Trích xuất tất cả các liên kết từ mã nguồn trang web

**Dùng tìm kiếm chuỗi thông thường?** Bạn sẽ phải viết rất nhiều logic `if-else`.  
**Dùng biểu thức chính quy?** Chỉ một dòng mẫu là xong.

---

## 1. Giới thiệu về Regex: Nắm bắt trong ba phút

👇 Hãy thử: Nhập biểu thức chính quy và xem kết quả khớp theo thời gian thực

<RegexDemo />

::: tip 💡 Tóm tắt trong một câu
Biểu thức chính quy = **sử dụng các ký hiệu đặc biệt để mô tả "loại văn bản bạn muốn tìm"**. `\d` đại diện cho chữ số, `+` đại diện cho một hoặc nhiều lần, vì vậy `\d+` có nghĩa là "một hoặc nhiều chữ số".
:::

---

## 2. Khái niệm cốt lõi: Kết hợp như xếp hình

Bản chất của regex là sử dụng **ba loại khối xếp hình** để tạo ra mẫu bạn muốn:

### 2.1 Khối xếp hình thứ nhất: Lớp ký tự (Khớp ký tự nào)

| Cú pháp | Ý nghĩa | Ví dụ |
|---|---|---|
| `.` | Bất kỳ ký tự nào | `a.c` → abc, a1c, a c |
| `\d` | Chữ số [0-9] | `\d\d` → 42, 99 |
| `\w` | Chữ cái/Chữ số/Dấu gạch dưới | `\w+` → hello, user_1 |
| `\s` | Ký tự khoảng trắng | Khớp khoảng trắng, Tab |
| `[abc]` | Bất kỳ ký tự nào trong tập hợp | `[aeiou]` → Nguyên âm |
| `[^abc]` | Không có trong tập hợp | `[^0-9]` → Ký tự không phải chữ số |

### 2.2 Khối xếp hình thứ hai: Lượng từ (Khớp bao nhiêu lần)

| Cú pháp | Ý nghĩa | Ví dụ |
|---|---|---|
| `*` | 0 lần hoặc nhiều lần | `ab*` → a, ab, abbb |
| `+` | 1 lần hoặc nhiều lần | `ab+` → ab, abbb (Không khớp 'a') |
| `?` | 0 lần hoặc 1 lần | `colou?r` → color, colour |
| `{3}` | Chính xác 3 lần | `\d{3}` → 123 |
| `{2,4}` | Từ 2 đến 4 lần | `\d{2,4}` → 12, 1234 |

### 2.3 Khối xếp hình thứ ba: Vị trí và nhóm

| Cú pháp | Ý nghĩa | Ví dụ |
|---|---|---|
| `^` | Đầu dòng | `^Hello` → Dòng bắt đầu bằng Hello |
| `$` | Cuối dòng | `end$` → Dòng kết thúc bằng end |
| `\b` | Ranh giới từ | `\bcat\b` → cat (Không khớp 'catch') |
| `(...)` | Nhóm bắt giữ | `(\d+)-(\d+)` → Bắt giữ riêng lẻ |
| `a\|b` | Hoặc | `cat\|dog` → cat hoặc dog |

---

## 3. Thực hành: Các mẫu xác thực phổ biến

### 3.1 Xác thực email

```
[\w.+-]+@[\w-]+\.[\w.]+
```

Phân tích:
- `[\w.+-]+` — Phần tên người dùng (chữ cái, chữ số, dấu chấm, dấu cộng, dấu gạch ngang)
- `@` — Ký tự @
- `[\w-]+` — Phần tên miền
- `\.` — Dấu chấm được thoát
- `[\w.]+` — Tên miền cấp cao nhất

### 3.2 Xác thực số điện thoại (Trung Quốc)

```
1[3-9]\d{9}
```

Phân tích:
- `1` — Bắt đầu bằng 1
- `[3-9]` — Chữ số thứ hai là 3-9
- `\d{9}` — Tiếp theo là 9 chữ số

### 3.3 Kiểm tra độ mạnh mật khẩu

```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$
```

Phân tích:
- `(?=.*[a-z])` — Ít nhất một chữ cái thường (lookahead assertion)
- `(?=.*[A-Z])` — Ít nhất một chữ cái in hoa
- `(?=.*\d)` — Ít nhất một chữ số
- `.{8,}` — Tổng độ dài ít nhất 8 ký tự

---

## 4. Sử dụng Regex trong code

### JavaScript

```javascript
const text = 'Liên hệ: 13812345678 hoặc 15099887766'
const regex = /1[3-9]\d{9}/g
const phones = text.match(regex)
// ['13812345678', '15099887766']

// Thay thế
text.replace(/\d{4}(?=\d{4}$)/, '****')
// Ẩn bốn chữ số giữa của số điện thoại

// Xác thực
/^[\w.+-]+@[\w-]+\.[\w.]+$/.test('user@example.com')
// true
```

### Python

```python
import re

text = 'Giá là 99 đồng, ưu đãi 20 đồng'
numbers = re.findall(r'\d+', text)
# ['99', '20']

# Thay thế
re.sub(r'\d+', 'X', text)
# 'Giá là X đồng, ưu đãi X đồng'

# Bắt giữ theo nhóm
match = re.search(r'(\d+)-(\d+)', '2024-01-15')
match.group(1)  # '2024'
match.group(2)  # '01'
```

---

## 5. Tham lam vs Lười biếng: Một sự khác biệt quan trọng

```
Văn bản: <b>hello</b> and <b>world</b>
```

| Mẫu | Kết quả khớp | Giải thích |
|---|---|---|
| `<b>.*</b>` | `<b>hello</b> and <b>world</b>` | Tham lam: Cố gắng khớp càng nhiều càng tốt |
| `<b>.*?</b>` | `<b>hello</b>` | Lười biếng: Cố gắng khớp càng ít càng tốt |

::: tip 💡 Lưu ý
Mặc định là chế độ tham lam. Thêm `?` sau lượng từ để chuyển sang chế độ lười biếng. Hầu hết thời gian, bạn sẽ cần chế độ lười biếng.
:::

---

## 6. Tóm tắt

::: tip 📚 Các điểm chính
1.  **Regex = ngôn ngữ mini mô tả mẫu văn bản**, dùng để tìm kiếm, khớp, thay thế
2.  **Ba loại khối xếp hình**: Lớp ký tự (khớp gì) + Lượng từ (khớp bao nhiêu lần) + Vị trí/Nhóm
3.  **\d \w \s** là ba lớp ký tự được sử dụng phổ biến nhất, bao gồm chữ số, từ, khoảng trắng
4.  **Không cần viết từ đầu**: Các mẫu regex đã có sẵn cho các tình huống phổ biến để bạn tái sử dụng
5.  **Tham lam vs Lười biếng**: Mặc định tham lam (khớp nhiều), thêm `?` để thành lười biếng (khớp ít)
:::

**Học tiếp theo**:
- [Biến môi trường và PATH](./environment-path) - Hiểu cấu hình hệ thống
- [SSH và xác thực khóa](./ssh-authentication) - Kết nối an toàn với máy chủ từ xa
