---
title: Git: Cỗ máy thời gian của mã nguồn
description: Git là một trong những công cụ quan trọng nhất trong phát triển phần mềm hiện đại, hầu hết mọi công ty và dự án mã nguồn mở đều sử dụng nó. Chương này được viết dành riêng cho những người chưa từng dùng Git, bắt đầu từ việc Git giúp bạn giải quyết vấn đề gì, sau đó từng bước kết nối các lệnh và khái niệm.
layout: ~/layouts/DocLayout.astro
---

# Git: Cỗ máy thời gian của mã nguồn

> 💡 **Hướng dẫn học tập**: Chương này được viết dành riêng cho những người chưa từng dùng Git. Chúng tôi sẽ không bắt bạn học thuộc lòng các lệnh ngay lập tức, mà thay vào đó, sẽ giúp bạn hiểu rõ "Git thực sự giúp bạn giải quyết vấn đề gì", sau đó từng bước kết nối các lệnh và khái niệm lại với nhau. Sau khi đọc xong, bạn sẽ có thể tự mình thực hiện: `commit` cục bộ, tạo `branch`, và `push` lên GitHub.

---

## 0. Hãy bắt đầu với một câu hỏi: Bạn đã bao giờ trải qua những cơn ác mộng này chưa?

**Tình huống 1: Địa ngục phiên bản**

Bạn viết luận văn hoặc viết code, sửa đến giữa chừng thì phát hiện sửa sai, muốn quay lại phiên bản ba ngày trước – nhưng bạn không tìm thấy nó.

```
项目_v1.zip
项目_v2_修改版.zip
项目_v3_最终版.zip
项目_v3_最终版_真的最终版.zip
项目_v3_最终版_打死不改了.zip
```

Mỗi lần lưu một bản sao mới, ổ cứng của bạn ngày càng lộn xộn, và bạn hoàn toàn không thể nhớ phiên bản nào đã sửa gì.

**Tình huống 2: Ác mộng cộng tác**

Bạn và đồng đội cùng lúc sửa cùng một file:
- Bạn sửa dòng 10, thêm tính năng đăng nhập
- Đồng đội sửa dòng 10, sửa một Bug
- Các bạn gửi code cho nhau qua email, kết quả là khi `merge`, thay đổi của một người bị người kia ghi đè
- Không ai biết đoạn code cuối cùng nào là đúng

**Tình huống 3: Không có "thuốc hối hận"**

Bạn triển khai code mới lên môi trường sản xuất, kết quả là phát sinh Bug, muốn khẩn cấp quay lại phiên bản ổn định trước đó – nhưng bạn không biết cách quay lại, chỉ có thể luống cuống tìm bản sao lưu.

---

**Git ra đời để giải quyết ba vấn đề này.**

Git là một **Hệ thống kiểm soát phiên bản** (Version Control System). Bản chất của nó là: **ghi lại mọi thao tác "lưu trữ" của bạn, tạo thành một dòng thời gian lịch sử hoàn chỉnh, cho phép bạn quay lại bất kỳ điểm lịch sử nào bất cứ lúc nào.**

Không quá lời khi nói rằng, Git là một trong những công cụ quan trọng nhất trong phát triển phần mềm hiện đại. Hầu hết mọi công ty, mọi dự án mã nguồn mở đều đang sử dụng nó.

---

## 1. Git và GitHub có phải là một không?

Nhiều người mới học thường nhầm lẫn hai khái niệm này, hãy làm rõ trước:

| | Git | GitHub |
| :--- | :--- | :--- |
| **Là gì** | Một công cụ kiểm soát phiên bản chạy trên máy tính của bạn | Một trang web lưu trữ các Git `Repository` (trên đám mây) |
| **Ở đâu** | Máy tính cục bộ của bạn | Trên internet |
| **Có thể sử dụng độc lập không** | ✅ Có, chỉ quản lý lịch sử cục bộ | ❌ Cần sử dụng kết hợp với Git |
| **So sánh** | Cuốn nhật ký cục bộ của bạn | Dịch vụ lưu trữ nhật ký trên đám mây |

Nói một cách đơn giản: **Git là công cụ, GitHub là dịch vụ lưu trữ.** Giống như Word là công cụ, OneDrive là dịch vụ lưu trữ đám mây, cả hai phối hợp với nhau nhưng không phải là cùng một thứ.

Ngoài GitHub, các dịch vụ tương tự còn có GitLab, Gitee (ở Trung Quốc) v.v...

---

## 2. Khái niệm cốt lõi: Ba khu vực

Đây là thiết kế quan trọng nhất của toàn bộ Git, hiểu được ba khu vực này, bạn sẽ hiểu được linh hồn của Git.

Git chia trạng thái file của bạn thành ba lớp:

**Working Directory**
Là **thư mục thông thường** của bạn, tất cả các file bạn đang thấy và đang chỉnh sửa đều ở đây. Bạn có thể thoải mái thay đổi, Git sẽ nhận biết được bạn đã thay đổi gì, nhưng sẽ không ghi lại bất kỳ điều gì.

**Staging Area / Index**
Đây là một **trạm trung chuyển "chuẩn bị `commit`"**. Bạn có thể "đặt" các file muốn lưu từ `Working Directory` vào `Staging Area`, giống như đặt hàng vào hộp `package` – chưa gửi đi, nhưng đã chọn xong những gì cần gửi.

**Repository**
Đây là **kho lưu trữ lịch sử vĩnh viễn**, nằm trong thư mục `.git`. Mỗi khi bạn thực hiện `git commit`, nội dung trong `Staging Area` sẽ được niêm phong vào `Repository`, tạo thành một bản ghi lịch sử không thể thay đổi.

👇 **Hãy thử thao tác**: Lần lượt nhấp vào các nút lệnh, quan sát cách các file di chuyển giữa ba khu vực.

<GitCommitFlow />

### Tại sao lại cần "hai bước" (`add` + `commit`)?

Nhiều người mới học sẽ hỏi: Tại sao không thể lưu trực tiếp bằng một cú nhấp chuột, mà lại phải `add` rồi mới `commit`?

**Bởi vì trong phát triển thực tế, bạn thường không muốn `commit` tất cả các thay đổi cùng một lúc.**

Ví dụ: Hôm nay bạn đã sửa 5 file:
- `login.js`: Đã hoàn thành tính năng đăng nhập (muốn `commit`)
- `style.css`: Đã điều chỉnh kiểu dáng trang đăng nhập (muốn `commit`)
- `debug.log`: Output debug tạm thời (**không muốn** `commit`)
- `experiment.js`: Tính năng mới đang thử nghiệm, chưa hoàn thành (**không muốn** `commit`)
- `todo.txt`: Ghi chú cá nhân của bạn (**không muốn** `commit`)

Nếu không có `Staging Area`, bạn sẽ phải `commit` tất cả 5 file này (lịch sử `commit` sẽ rất lộn xộn), hoặc không `commit` file nào cả.

Với `Staging Area`, bạn có thể kiểm soát chính xác: `git add login.js style.css`, chỉ đặt hai file này vào hộp `package`, sau đó `commit`, lần `commit` này sẽ ghi lại rõ ràng "đã hoàn thành tính năng đăng nhập".

---

## 3. Lần đầu sử dụng Git: Khởi tạo và quy trình làm việc cơ bản

### 3.1 Cài đặt và khởi tạo

Sau khi cài đặt Git (macOS có sẵn, Windows tải từ git-scm.com), mở `terminal`, vào thư mục dự án của bạn:

```bash
# 在当前文件夹初始化一个 Git 仓库
git init

# Git 会创建一个隐藏的 .git 文件夹，所有历史记录存在里面
# 输出：Initialized empty Git repository in .../your-project/.git/
```

Lần đầu sử dụng, bạn cần cho Git biết bạn là ai (thông tin này sẽ được đính kèm vào mỗi bản `commit`):

```bash
git config --global user.name "Tên của bạn"
git config --global user.email "Email của bạn"
```

### 3.2 Quy trình làm việc hàng ngày: Ba bước lưu trữ

Sau khi khởi tạo, 90% các thao tác phát triển hàng ngày là lặp đi lặp lại ba bước này:

**Bước 1: Xem trạng thái**

```bash
git status
```

Đây là lệnh bạn dùng nhiều nhất, không có lệnh nào hơn. Nó cho bạn biết:
- Bạn đang ở `branch` nào
- Những file nào đã được sửa đổi (màu đỏ = chưa `stage`)
- Những file nào đang ở trong `Staging Area` (màu xanh lá = đã `stage`, chờ `commit`)

**Bước 2: Đặt file vào `Staging Area`**

```bash
# Thêm một file
git add login.js

# Thêm nhiều file
git add login.js style.css

# Thêm tất cả các file đã sửa đổi trong thư mục hiện tại (dùng . để biểu thị "tất cả")
git add .
```

> ⚠️ Sai lầm phổ biến của người mới học: `git add .` rất tiện lợi, nhưng nó sẽ thêm tất cả các thay đổi vào, bao gồm cả các file tạm thời mà bạn không muốn `commit`. Hãy tạo thói quen `add` chính xác, hoặc sử dụng `.gitignore` để loại trừ các file không muốn theo dõi (sẽ nói ở phần sau).

**Bước 3: `Commit`, viết mô tả**

```bash
git commit -m "feat: Thêm tính năng đăng nhập người dùng"
```

Nội dung trong dấu ngoặc kép sau `-m` được gọi là **commit message** (mô tả `commit`). Đây là thông điệp viết cho chính bạn trong tương lai và cho đồng đội, cần phải viết có ý nghĩa.

### 3.3 Viết Commit Message như thế nào cho chuyên nghiệp?

```bash
# ❌ Cách viết vô dụng – đọc xong không biết đã làm gì
git commit -m "update"
git commit -m "fix"
git commit -m "Đã sửa một vài thứ"

# ✅ Cách viết tốt: Loại + dấu hai chấm + mô tả ngắn gọn
git commit -m "feat: Thêm tính năng đăng nhập người dùng"
git commit -m "fix: Sửa lỗi màn hình trắng trên iOS Safari ở trang chủ"
git commit -m "docs: Cập nhật hướng dẫn triển khai trong README"
git commit -m "refactor: Tách UserService thành module độc lập"
git commit -m "style: Đồng bộ thụt lề code thành 2 khoảng trắng"
```

**Ý nghĩa các tiền tố thường dùng:**

| Tiền tố | Ý nghĩa |
| :--- | :--- |
| `feat:` | Tính năng mới (`feature`) |
| `fix:` | Sửa Bug |
| `docs:` | Thay đổi tài liệu |
| `style:` | Điều chỉnh định dạng code (không ảnh hưởng chức năng) |
| `refactor:` | Tái cấu trúc code (chức năng không đổi, tối ưu cấu trúc) |
| `chore:` | Liên quan đến build, công cụ, `dependency` |
| `test:` | Liên quan đến test |

Hình thành thói quen này, vài tháng sau khi xem lại lịch sử, bạn sẽ biết ngay mỗi `commit` đã làm gì. Điều này đặc biệt quan trọng trong làm việc nhóm.

### 3.4 Xem lịch sử

```bash
# Định dạng chi tiết (thông tin đầy đủ của mỗi commit)
git log

# Định dạng ngắn gọn (mỗi dòng một commit, khuyến nghị dùng hàng ngày)
git log --oneline

# Ví dụ output:
# a1b2c3d (HEAD -> main) feat: Thêm tính năng đăng nhập người dùng
# 9f3e1b2 init: Khởi tạo dự án
```

---

## 4. Vũ trụ song song: Branch

**Branch** là tính năng mạnh mẽ nhất của Git, và cũng là tính năng gây bối rối nhất cho người mới học. Nhưng sau khi hiểu được nó, bạn sẽ thấy thiết kế này vô cùng tinh tế.

### 4.1 Branch là gì? Hiểu bằng "vũ trụ song song"

Hãy tưởng tượng bạn đang chơi một game nhập vai, trong game có một lựa chọn quan trọng:
- Lựa chọn A: Đi thách đấu Boss lớn (phát triển tính năng mới)
- Lựa chọn B: Tiếp tục giữ vững tình hình hiện tại (đường chính không thay đổi)

Nếu bạn trực tiếp thực hiện lựa chọn A trên bản lưu chính, lỡ thất bại, toàn bộ tiến độ game sẽ bị hủy hoại.

Nhưng nếu bạn **sao chép một bản lưu**, và trong bản sao đó đi thách đấu Boss:
- Thắng rồi? `Merge` kết quả của bản sao về bản lưu chính
- Thua rồi? Bản lưu chính hoàn toàn không bị ảnh hưởng, xóa bản sao đi và chơi lại

**Git Branch chính là cơ chế "sao chép bản lưu" này.**

Trong Git, `main` (hoặc `master`) `branch` là "bản lưu chính" của bạn, luôn giữ ổn định và sẵn sàng sử dụng. Khi bạn muốn phát triển một tính năng mới, bạn tạo một `branch` mới từ `main`, phát triển và test ở đó, sau khi hoàn thành thì `merge` trở lại `main`.

### 4.2 Minh họa trực quan về Branch

👇 **Hãy thử thao tác**: Lần lượt nhấp vào các nút lệnh, quan sát biểu đồ `branch` bên dưới phân nhánh, mở rộng và cuối cùng `merge` như thế nào. Đặc biệt chú ý đến sự thay đổi vị trí của tag `HEAD` – nó luôn chỉ vào "bạn đang ở đâu".

<GitBranchVisual />

### 4.3 Chi tiết thao tác Branch

**Tạo và chuyển sang `branch` mới:**

```bash
# Cách 1: Tạo trước, sau đó chuyển (hai bước)
git branch feature-login      # Tạo branch
git checkout feature-login    # Chuyển sang

# Cách 2: Một bước (khuyến nghị)
git checkout -b feature-login

# Output: Switched to a new branch 'feature-login'
```

Sau khi tạo `branch`, dấu nhắc `command line` của bạn sẽ hiển thị tên `branch` hiện tại, ví dụ:
```
user@mac ~/project (feature-login) $
```

**Xem tất cả các `branch`:**

```bash
git branch

# Output (* biểu thị branch hiện tại):
# * feature-login
#   main
```

**Phát triển bình thường trên `branch`:**

```bash
# Trên feature-login branch, sửa code, add, commit, hoàn toàn giống như bình thường
git add login.js
git commit -m "feat: Thêm cấu trúc HTML form đăng nhập"

git add login.js api.js
git commit -m "feat: Hoàn thành tích hợp API đăng nhập"
```

Những `commit` này chỉ nằm trên `branch feature-login`, `branch main` hoàn toàn không biết bạn đã làm gì.

**Chuyển về `branch` chính, `merge`:**

```bash
# Chuyển về main
git checkout main

# Merge tất cả các thay đổi từ feature-login vào
git merge feature-login

# Sau khi merge xong, có thể xóa branch này (tùy chọn)
git branch -d feature-login
```

### 4.4 Khi nào nên tạo Branch?

| Tình huống | Đề xuất | Lý do |
| :--- | :--- | :--- |
| Phát triển một tính năng mới | ✅ Tạo `branch` | Không ảnh hưởng đến đường chính trước khi tính năng hoàn thành, có thể hủy bỏ bất cứ lúc nào |
| Sửa Bug khẩn cấp trên môi trường production | ✅ Tạo `hotfix-xxx` `branch` từ `main` | Sau khi sửa xong, `merge` trực tiếp lên `production`, không mang theo các tính năng chưa hoàn thành |
| Phát triển song song với đồng đội | ✅ Mỗi người tạo một `branch` riêng | Không gây nhiễu lẫn nhau, sau khi hoàn thành thống nhất `merge` thông qua `Pull Request` |
| Chỉ sửa một lỗi chính tả | ❌ Sửa trực tiếp trên `main` | Rủi ro cực thấp, không cần thiết phải tạo thêm `branch` |

### 4.5 Các chiến lược Branch thường dùng trong nhóm

Trong các dự án thực tế, nhóm thường sẽ thống nhất về cách đặt tên và mục đích sử dụng của các `branch`:

| Tên `branch` | Mục đích | Đặc điểm |
| :--- | :--- | :--- |
| `main` / `master` | Code ổn định của môi trường production | Chỉ code đã test thành công mới được vào, không thể `push` trực tiếp |
| `dev` / `develop` | `Branch` tích hợp hàng ngày | Tất cả các `feature branch` sẽ `merge` vào đây trước, sau khi test thành công mới lên `main` |
| `feature/xxx` | Phát triển tính năng cụ thể | Ví dụ `feature/user-login`, sau khi hoàn thành sẽ `merge` vào `dev` |
| `hotfix/xxx` | Sửa lỗi khẩn cấp | Tạo từ `main`, sau khi sửa xong sẽ `merge` trực tiếp về `main` và `dev` |

---

## 5. Cộng tác với đồng đội: Remote Repository

Cho đến nay, bạn đã học các thao tác Git **cục bộ** – tất cả lịch sử đều được lưu trữ trên máy tính của riêng bạn. Để chia sẻ code với đồng đội, bạn cần một **Remote Repository**, tức là một dịch vụ lưu trữ đám mây như GitHub, GitLab.

### 5.1 Nguyên lý hoạt động của Remote Repository

Có thể hiểu `Remote Repository` là **"bản lưu công cộng" dùng chung của nhóm**:

- Mỗi người viết code, `commit` cục bộ
- Sau khi viết xong thì `push` (tải lên) lên `Remote Repository`
- Đồng đội `pull` (tải xuống) nội dung mới nhất từ `Remote Repository` về máy cục bộ của mình
- Như vậy code của mọi người sẽ được đồng bộ

👇 **Hãy thử thao tác**: Lần lượt nhấp vào các lệnh, trải nghiệm quy trình hoàn chỉnh từ liên kết `Remote Repository`, `push`, đến `pull` cập nhật của đồng đội.

<GitSyncDemo />

### 5.2 Lần đầu tiên `push` dự án lên GitHub

**Bước 1**: Tạo một `Repository` mới trên GitHub (nhấp vào dấu + ở góc trên bên phải → New repository), không chọn tùy chọn khởi tạo.

**Bước 2**: Quay lại `terminal` cục bộ, liên kết `Remote Repository`:

```bash
# Liên kết Repository cục bộ với Repository trên GitHub
# "origin" là alias của Remote Repository, là tên đã được quy ước (có thể đổi, nhưng không cần thiết)
git remote add origin https://github.com/tên_người_dùng_của_bạn/tên_repository.git

# Xác nhận liên kết thành công
git remote -v
# Output:
# origin  https://github.com/tên_người_dùng_của_bạn/tên_repository.git (fetch)
# origin  https://github.com/tên_người_dùng_của_bạn/tên_repository.git (push)
```

**Bước 3**: `Push` nội dung cục bộ lên `remote`:

```bash
# Lần push đầu tiên, -u có nghĩa là "sau này khi git push, mặc định sẽ push lên branch main của origin"
git push -u origin main

# Sau đó, mỗi lần push chỉ cần:
git push
```

### 5.3 Các lệnh cộng tác hàng ngày

**`Push` (bạn đã sửa đổi, muốn đồng đội thấy):**
```bash
git push
```

**`Pull` (đồng đội đã sửa đổi, bạn muốn đồng bộ):**
```bash
git pull
```

`git pull` thực chất là sự kết hợp của hai lệnh:
1. `git fetch`: Đầu tiên tải các bản `commit` mới nhất từ `Remote Repository`
2. `git merge`: `Merge` nội dung đã tải về vào `branch` hiện tại của bạn

**Lần đầu tiên lấy dự án của người khác từ GitHub:**
```bash
# Sao chép toàn bộ Remote Repository về cục bộ (chỉ cần làm một lần)
git clone https://github.com/ai_đó/dự_án_nào_đó.git

# Lệnh clone sẽ tự động thiết lập liên kết với remote, sau đó chỉ cần push/pull là được
```

### 5.4 Hướng của `push` và `pull`

```
Máy tính của bạn (Local Repository)  ←→  GitHub (Remote Repository)

git push:  Cục bộ → Remote   (Bạn đã sửa đổi, tải lên cho đồng đội)
git pull:  Remote → Cục bộ   (Đồng đội đã sửa đổi, tải xuống máy của bạn)
git clone: Remote → Cục bộ   (Lần đầu tiên sao chép toàn bộ Repository)
```

> **Thực hành tốt nhất**: Mỗi ngày trước khi bắt đầu làm việc, hãy `git pull` để lấy code mới nhất; sau khi tan làm hoặc hoàn thành một tính năng, hãy `git push` để sao lưu kịp thời và cho đồng đội thấy tiến độ của bạn.

---

## 6. Nâng cao: Xử lý Conflict

Conflict là điều không thể tránh khỏi trong cộng tác, nhưng cũng không quá đáng sợ.

### 6.1 Conflict xảy ra như thế nào?

Khi bạn và đồng đội **cùng lúc sửa đổi cùng một dòng trong cùng một file**, khi `merge`, Git không biết nên dùng phiên bản của ai, lúc đó sẽ phát sinh `conflict`.

Ví dụ:
- Bạn viết ở dòng 5 của `login.js`: `const timeout = 3000`
- Đồng đội cùng lúc viết ở cùng dòng đó: `const timeout = 5000`
- Khi bạn `git pull` hoặc `git merge`, Git phát hiện mâu thuẫn này, nó sẽ "tạm dừng" và nói với bạn: Tôi không biết nên dùng cái nào, bạn hãy quyết định.

### 6.2 File bị Conflict trông như thế nào?

Git sẽ chèn các ký hiệu đặc biệt vào những chỗ bị `conflict`:

```javascript
function login() {
  const url = '/api/login'

<<<<<<< HEAD
  const timeout = 3000   // 你的版本
=======
  const timeout = 5000   // 队友的版本
>>>>>>> feature/update-timeout

  return fetch(url, { timeout })
}
```

- Giữa `<<<<<<< HEAD` và `=======`: là nội dung của `branch` hiện tại của bạn
- Giữa `=======` và `>>>>>>> xxx`: là nội dung được `merge` vào

### 6.3 Làm thế nào để giải quyết Conflict?

**Bước 1**: Mở file bị `conflict`, tìm tất cả các ký hiệu `<<<<<<<` (thường các editor như VS Code sẽ tự động highlight)

**Bước 2**: Quyết định giữ lại đoạn code nào, sau đó chỉnh sửa file thủ công, xóa tất cả các ký hiệu đánh dấu (`<<<<<<<`, `=======`, `>>>>>>>`).

Ví dụ quyết định dùng 5000 (phiên bản của đồng đội):
```javascript
function login() {
  const url = '/api/login'
  const timeout = 5000   // Sử dụng thay đổi của đồng đội
  return fetch(url, { timeout })
}
```

**Bước 3**: `Commit` lại

```bash
# Đánh dấu conflict đã được giải quyết
git add login.js

# Hoàn thành commit merge (Git sẽ tự động tạo commit message merge)
git commit
```

### 6.4 Những thói quen tốt để giảm Conflict

- **`Pull` thường xuyên**: Đồng bộ code mới nhất trước khi bắt đầu làm việc, giảm tình trạng "bạn bị tụt hậu quá nhiều"
- **`Commit` từng bước nhỏ**: Đừng viết code cả tuần rồi mới `commit` một lần, `commit` nhỏ và thường xuyên sẽ dễ phát hiện và giải quyết `conflict` hơn
- **Phân tách `branch`**: Các tính năng khác nhau dùng các `branch` khác nhau, giảm cạnh tranh trên cùng một dòng code
- **Giao tiếp**: Trước khi sửa các file chung (ví dụ `config.js`), hãy thông báo cho đồng đội

---

## 7. Tra cứu nhanh các lệnh thường dùng

<GitCommandCheatsheet />

---

## 8. Thực chiến: Quy trình hoàn chỉnh khi tham gia một dự án nhóm

Đây là quy trình thao tác chuẩn khi bạn tham gia một nhóm hoặc dự án mới, có thể sao chép trực tiếp:

```bash
# ① Ngày đầu tiên: Clone dự án về cục bộ (chỉ làm một lần)
git clone https://github.com/team/project.git
cd project

# ② Mỗi ngày bắt đầu làm việc: Đầu tiên pull code mới nhất, đảm bảo code của bạn là mới nhất
git pull origin main

# ③ Tạo branch tính năng của riêng bạn (đừng sửa trực tiếp trên main)
git checkout -b feature/user-profile

# ④ Phát triển bình thường... viết code...

# ⑤ Sau khi hoàn thành một tính năng nhỏ, commit ngay lập tức (đừng để dồn lại)
git add src/UserProfile.vue
git commit -m "feat: Hoàn thành tính năng tải ảnh đại diện người dùng"

git add src/UserProfile.vue src/api/user.js
git commit -m "feat: Hoàn thành API chỉnh sửa thông tin người dùng"

# ⑥ Push branch của bạn lên remote, để đồng đội có thể thấy
git push origin feature/user-profile

# ⑦ Tạo Pull Request (PR) trên GitHub, yêu cầu merge vào main
# (Bước này thực hiện trên trang web GitHub)

# ⑧ Chờ đồng đội Code Review, sửa đổi theo feedback, tiếp tục commit + push

# ⑨ Sau khi PR được merge, quay về main, cập nhật cục bộ, xóa branch tính năng
git checkout main
git pull
git branch -d feature/user-profile
```

---

## 9. .gitignore: Những file nào không nên được theo dõi?

Một số file bạn **không muốn** `commit` vào Git `Repository`, ví dụ:
- `node_modules/`: Các gói `dependency`, dung lượng lớn, có thể tạo lại bằng `npm install`
- `.env`: File biến môi trường, có thể chứa mật khẩu cơ sở dữ liệu, `API Key`, **tuyệt đối không được tải lên `Repository` công khai**
- `*.log`: File `log`
- `.DS_Store`: File ẩn được macOS tự động tạo
- `dist/`, `build/`: Sản phẩm biên dịch, có thể xây dựng lại

Tạo một file `.gitignore` trong thư mục gốc của dự án, viết các quy tắc cho những file không muốn theo dõi:

```gitignore
# Gói dependency
node_modules/

# Biến môi trường (Quan trọng! Mật khẩu không được commit)
.env
.env.local

# Sản phẩm build
dist/
build/

# File hệ thống
.DS_Store
Thumbs.db

# Log
*.log
```

Trên GitHub có các template `.gitignore` cho nhiều ngôn ngữ và framework khác nhau: [github.com/github/gitignore](https://github.com/github/gitignore)

---

## Bảng tra cứu nhanh thuật ngữ

| Thuật ngữ | Tiếng Anh | Giải thích |
| :--- | :--- | :--- |
| **Kho lưu trữ** | Repository (Repo) | Cơ sở dữ liệu lưu trữ tất cả lịch sử phiên bản của dự án, nằm trong thư mục `.git` |
| **Cam kết** | Commit | Một bản ghi phiên bản hoàn chỉnh, giống như điểm lưu game, kèm theo mô tả và dấu thời gian |
| **Nhánh** | Branch | Dòng phát triển độc lập, giống như dòng thời gian song song, không ảnh hưởng lẫn nhau |
| **Hợp nhất** | Merge | Tích hợp các thay đổi từ một `branch` vào một `branch` khác |
| **Xung đột** | Conflict | Cùng một dòng code bị nhiều người sửa đổi, Git không biết nên dùng cái nào, cần giải quyết thủ công |
| **Tạm lưu** | Stage / Index | Thao tác đưa các thay đổi vào danh sách "chuẩn bị `commit`" |
| **Từ xa** | Remote | Bản sao `Repository` trên đám mây (GitHub / GitLab / Gitee) |
| **Sao chép** | Clone | Sao chép toàn bộ `Remote Repository` về cục bộ |
| **Đẩy** | Push | Tải các `commit` cục bộ lên `Remote Repository` |
| **Kéo** | Pull | Tải nội dung mới nhất từ `remote` về và `merge` vào cục bộ |
| **HEAD** | HEAD | Con trỏ chỉ `branch`/`commit` hiện tại, biểu thị "bạn đang ở đâu" |
| **origin** | origin | `Alias` mặc định của `Remote Repository` (tên đã được quy ước) |
| **stash** | Stash | Tạm thời lưu các thay đổi chưa `commit`, dùng khi chuyển đổi tác vụ |
| **PR / MR** | Pull Request / Merge Request | Yêu cầu `merge branch` của bạn vào `branch` chính, thường cần đồng đội `review` |
