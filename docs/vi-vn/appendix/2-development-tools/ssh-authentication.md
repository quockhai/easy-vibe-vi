# SSH và Xác thực bằng Khóa

> 💡 **Hướng dẫn học tập**: Mỗi lần `git push` lại phải nhập mật khẩu? Kết nối máy chủ luôn bị báo "Permission denied"? Chương này sẽ giúp bạn hiểu rõ nguyên lý xác thực bằng khóa SSH chỉ trong 5 phút, cùng với cách đăng nhập GitHub và máy chủ không cần mật khẩu chỉ với một cú nhấp chuột.

---

## 0. Bạn chắc chắn đã gặp những tình huống này

- `git push` thì hộp thoại nhập mật khẩu cứ hiện đi hiện lại, thật phiền phức
- Kết nối SSH đến máy chủ thất bại, không biết `id_rsa` và `id_ed25519` là gì
- Nghe nói về "khóa công khai" và "khóa riêng tư", nhưng không rõ cái nào đưa cho người khác, cái nào giữ lại cho mình

**Mâu thuẫn cốt lõi**: Mật khẩu không an toàn, lại phiền phức. Khóa SSH chính là giải pháp để đồng thời giải quyết vấn đề bảo mật và tiện lợi.

---

## 1. Mật khẩu vs Khóa: Tại sao khóa tốt hơn?

👇 Hãy tự mình trải nghiệm: So sánh sự khác biệt giữa đăng nhập bằng mật khẩu và đăng nhập bằng khóa

<SSHAuthDemo />

::: tip 💡 Tóm tắt trong một câu
Đăng nhập bằng mật khẩu = Mỗi lần gửi mật khẩu đi để đối phương kiểm tra (mật khẩu có thể bị chặn);  
Đăng nhập bằng khóa = Chứng minh "tôi có chìa khóa" nhưng không cần cho bạn xem chìa khóa (khóa riêng tư không bao giờ được truyền đi).
:::

---

## 2. Mã hóa bất đối xứng: Khóa công khai và khóa riêng tư

Khóa SSH dựa trên **mã hóa bất đối xứng**, tạo ra hai cặp khóa cùng một lúc:

| | Khóa riêng tư (Private Key) | Khóa công khai (Public Key) |
|---|---|---|
| **Vị trí lưu trữ** | Máy tính của bạn `~/.ssh/id_ed25519` | Máy chủ/GitHub |
| **Có thể đưa cho người khác không** | ❌ Tuyệt đối không | ✅ Thoải mái cho |
| **Chức năng** | Ký (chứng minh danh tính) | Xác minh chữ ký (xác thực danh tính) |
| **So sánh** | Chìa khóa | Ổ khóa |

### Các loại khóa phổ biến

| Loại | Lệnh | Mức độ khuyến nghị | Mô tả |
|---|---|---|---|
| **Ed25519** | `ssh-keygen -t ed25519` | ⭐⭐⭐ | Mới nhất, nhanh nhất, an toàn nhất |
| **RSA** | `ssh-keygen -t rsa -b 4096` | ⭐⭐ | Tương thích tốt, nhưng chậm hơn |
| **ECDSA** | `ssh-keygen -t ecdsa` | ⭐ | Thường không được khuyến nghị |

---

## 3. Thực hành: Tạo và cấu hình khóa SSH

### 3.1 Tạo cặp khóa

```bash
ssh-keygen -t ed25519 -C "your@email.com"
```

Sau khi thực thi, bạn sẽ được nhắc:
- **Đường dẫn tệp**: Nhấn Enter để sử dụng đường dẫn mặc định `~/.ssh/id_ed25519`
- **Cụm mật khẩu**: Có thể thiết lập bảo vệ bổ sung (hoặc để trống)

### 3.2 Thêm khóa công khai vào GitHub

```bash
# 1. Sao chép nội dung khóa công khai
cat ~/.ssh/id_ed25519.pub | pbcopy  # macOS
cat ~/.ssh/id_ed25519.pub | xclip   # Linux

# 2. Mở GitHub → Settings → SSH and GPG keys → New SSH key
# 3. Dán khóa công khai, lưu lại

# 4. Kiểm tra kết nối
ssh -T git@github.com
# Thành công bạn sẽ thấy: Hi username! You've been authenticated...
```

### 3.3 Thêm khóa công khai vào máy chủ

```bash
# Cách 1: ssh-copy-id (khuyến nghị)
ssh-copy-id user@your-server

# Cách 2: Sao chép thủ công
cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

---

## 4. SSH Config: Tạm biệt các lệnh dài dòng

Cấu hình bí danh trong `~/.ssh/config`, một lần cấu hình dùng mãi mãi:

```
Host dev
  HostName 192.168.1.100
  User deploy
  IdentityFile ~/.ssh/id_ed25519

Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
```

Hiệu quả sau khi cấu hình:

| Trước đây | Sau này |
|---|---|
| `ssh -i ~/.ssh/id_ed25519 deploy@192.168.1.100` | `ssh dev` |
| Mỗi lần đều phải nhớ IP và tên người dùng | Chỉ cần nhớ một bí danh là đủ |

---

## 5. Khắc phục sự cố thường gặp

| Vấn đề | Nguyên nhân | Giải pháp |
|---|---|---|
| `Permission denied (publickey)` | Khóa công khai chưa được thêm vào máy chủ | `ssh-copy-id user@server` |
| `WARNING: UNPROTECTED PRIVATE KEY FILE` | Quyền của tệp khóa riêng tư quá rộng | `chmod 600 ~/.ssh/id_ed25519` |
| `Could not resolve hostname` | Cấu hình SSH Config bị lỗi | Kiểm tra định dạng `~/.ssh/config` |
| Vẫn yêu cầu mật khẩu GitHub | Đang sử dụng HTTPS thay vì SSH | Đổi sang dùng `git@github.com:user/repo.git` |

---

## 6. Tóm tắt

::: tip 📚 Các điểm cốt lõi
1.  **Khóa > Mật khẩu**: Khóa riêng tư không bao giờ được truyền đi, an toàn hơn mật khẩu rất nhiều.
2.  **Khuyến nghị Ed25519**: Thuật toán khóa hiện đại nhất, tốc độ nhanh, bảo mật cao.
3.  **Khóa công khai thoải mái cho, khóa riêng tư tuyệt đối không tiết lộ**: Hãy ghi nhớ quy tắc vàng này.
4.  **SSH Config**: Cấu hình bí danh một lần, sau đó `ssh bí_danh` để kết nối chỉ với một cú nhấp chuột.
5.  **GitHub/GitLab**: Sau khi thêm khóa công khai, `git push/pull` sẽ không bao giờ yêu cầu nhập mật khẩu nữa.
:::

**Học tiếp theo**:
- [Cổng và localhost](./ports-localhost) - Hiểu cơ bản về kết nối mạng
- [Biến môi trường và PATH](./environment-path) - Hiểu về cấu hình hệ thống
