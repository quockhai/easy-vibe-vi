---
title: 'Gặp lỗi khi viết code thì làm gì - Hướng dẫn thực tế: chụp màn hình hỏi AI'
description: 'Học cách đặt câu hỏi cho AI một cách hiệu quả để giải quyết các lỗi trong quá trình phát triển, nắm vững quy trình chuẩn: chụp màn hình, mô tả, xác định vấn đề — biến AI thành trợ lý debug của bạn.'
---

<script setup>
const duration = 'khoảng <strong>30 phút</strong>'
</script>

# Gặp lỗi khi viết code thì làm gì

## Giới thiệu chương

<ChapterIntroduction :duration="duration" :tags="['Kỹ thuật debug', 'Cộng tác với AI', 'Xử lý sự cố', 'Công cụ developer']" coreOutput="Một quy trình xử lý lỗi được chuẩn hóa" expectedOutput="Có thể tự giải quyết 90% lỗi thường gặp">

Trong kỷ nguyên AI, cách xử lý lỗi đã thay đổi.

Bạn không cần thuộc lòng tất cả các loại lỗi, không cần trở thành chuyên gia debug, thậm chí không cần hiểu lỗi có nghĩa là gì.

<strong>Bạn chỉ cần học một việc: cách hỏi AI.</strong>

Chương này sẽ dạy bạn một quy trình xử lý <strong>từ đơn giản đến nâng cao</strong>:

1. <strong>Bước 1: Hỏi trực tiếp</strong>: Mô tả hiện tượng + chụp màn hình, hỏi một câu
2. <strong>Bước 2: Bổ sung thông tin</strong>: Nếu chưa giải quyết được, mở F12 bổ sung thêm thông tin quan trọng

Sau khi nắm vững quy trình này, <strong>90% lỗi bạn đều có thể tự giải quyết</strong>.

</ChapterIntroduction>

::: info Lưu ý
Tất cả phương pháp trong chương này đều dựa trên kinh nghiệm thực tế sử dụng Cursor/Trae/Claude và các AI IDE khác, có thể áp dụng trực tiếp vào phát triển hàng ngày.
:::

<div style="margin: 50px 0;">
  <ClientOnly>
    <StepBar :active="0" :items="[
      { title: 'Hỏi trực tiếp', description: 'Mô tả hiện tượng + chụp màn hình' },
      { title: 'Bổ sung thông tin', description: 'Mở F12 xác định vấn đề' },
      { title: 'Lặp lại đến khi giải quyết', description: 'Cho đến khi vấn đề được giải quyết' }
    ]" />
  </ClientOnly>
</div>

## 1. Bí quyết cốt lõi: Chụp màn hình hỏi AI

::: warning Tại sao chương này quan trọng?

Nhiều người mới gặp lỗi thường phản ứng đầu tiên là:
- Hoảng loạn, bắt đầu sửa code bừa bãi
- Dành nửa tiếng tìm kiếm "cách giải quyết lỗi xxx"
- Cố tự hiểu lỗi có nghĩa gì
- Một mình debug đến tận đêm khuya

<strong>Những việc này đều đang lãng phí thời gian.</strong>

Trong kỷ nguyên AI, debug đã trở thành việc rất đơn giản:

```
Thấy lỗi → Chụp màn hình → Hỏi AI → Làm theo AI nói
```

Bạn không cần hiểu lỗi, không cần biết debug, thậm chí không cần biết vấn đề nằm ở đâu.

<strong>Bạn chỉ cần học cách hỏi.</strong>

:::

### 1.1 Cách hỏi đơn giản nhất

Không cần template phức tạp, chọn một trong hai cách:

**Cách 1: Mô tả hiện tượng**

Định dạng: Vừa làm gì, bây giờ xảy ra điều gì

```
Vừa sửa code trang đăng nhập, bây giờ trang trắng trống, phải làm sao?
```

**Cách 2: Chụp màn hình**

Chụp màn hình trực tiếp trang hiện tại hoặc thông tin lỗi

```
[Ảnh chụp màn hình]

Lỗi này giải quyết thế nào?
```

**Cách tốt nhất: Mô tả + Chụp màn hình**

```
Vừa sửa code trang đăng nhập, bây giờ trang trắng trống.

[Ảnh chụp màn hình]

Phải làm sao?
```

**Nhớ: Mô tả rõ ngữ cảnh, kèm ảnh chụp màn hình, AI có thể giúp bạn nhanh hơn.**

### 1.2 Cách trình bày vấn đề rõ ràng

Nhiều người mới biết cần hỏi nhưng không biết nói thế nào. Thực ra chỉ cần nói rõ ba điều:

**1. Vừa làm gì**

```
Vừa nhấp nút Lưu
Vừa sửa code trang đăng nhập
Vừa tải lại trang
```

**2. Bây giờ thấy gì**

```
Bây giờ trang trắng trống
Bây giờ nhấp nút không có phản ứng
Bây giờ hiện thông báo lỗi
```

**3. Muốn đạt kết quả gì**

```
Muốn lưu dữ liệu thành công
Muốn trang hiển thị bình thường
Muốn nhấp nút sau đó hiện thông báo
```

**Ví dụ đầy đủ:**

```
Vừa nhấp nút Lưu, bây giờ trang hiện lỗi "Lưu thất bại".

[Ảnh chụp màn hình]

Muốn lưu dữ liệu biểu mẫu thành công vào cơ sở dữ liệu, phải làm sao?
```

**Nguyên tắc quan trọng:**
- Dùng ngôn ngữ bình thường, không cần thuật ngữ chuyên ngành
- Nói theo thứ tự thời gian: làm gì trước, rồi xảy ra gì
- Nói ra kỳ vọng của bạn, để AI biết bạn muốn gì

## 2. Bước 1: Mô tả hiện tượng hỏi trực tiếp

Khi gặp vấn đề, <strong>đừng vội mở F12</strong>. Hãy mô tả hiện tượng trực tiếp, chụp màn hình trang hiện tại, đưa cho AI xem trước.

Nhiều khi, AI thấy ảnh chụp là có thể đưa ra giải pháp ngay.

### 2.1 Cách mô tả các hiện tượng thường gặp

::: tip Mô tả trực tiếp là được

**Trang trắng trống**
```
Mở trang ra trống trắng, phải làm sao?

[Ảnh chụp màn hình]
```

**Nhấp nút không có phản ứng**
```
Nhấp nút này không có phản ứng, xem giúp tôi với.

[Ảnh chụp màn hình]
```

**Không lưu được dữ liệu**
```
Nhấp lưu, dữ liệu không lưu được, phải làm sao?

[Ảnh chụp màn hình]
```

**Hiển thị style sai**
```
Nút này bị lệch vị trí, điều chỉnh thế nào?

[Ảnh chụp màn hình]
```

**API báo lỗi**
```
Gọi API bị lỗi, xem giúp tôi với.

[Ảnh chụp màn hình]
```

:::

### 2.2 Nếu AI giải quyết ngay được

Chúc mừng, vấn đề đã giải quyết! Sửa theo AI hướng dẫn là xong.

### 2.3 Nếu AI nói "cần thêm thông tin"

Lúc này mới cần mở F12, bổ sung thông tin quan trọng. Xem tiếp phần dưới.

## 3. Bước 2: Bổ sung thông tin quan trọng

Khi AI nói cần thêm thông tin, tuỳ loại vấn đề, mở F12 chụp nội dung tương ứng.

### 3.1 Khi nào cần bổ sung thông tin

AI có thể trả lời như sau:
- "Mở Console xem có báo lỗi không"
- "Chụp màn hình panel Network cho tôi xem"
- "Cần xem thông báo lỗi cụ thể"

Lúc này, bổ sung ảnh chụp theo hướng dẫn dưới đây.

### 3.2 Bổ sung thông tin Console (Trang trắng/Báo lỗi)

::: tip Các bước thực hiện

**Bước 1: Nhấn F12 mở Developer Tools**

Trên Mac là `Cmd+Option+I`, hoặc nhấp chuột phải vào trang chọn "Inspect".

**Bước 2: Chuyển sang tab Console**

**Bước 3: Chụp ảnh thông báo lỗi màu đỏ**

**Bước 4: Gửi cho AI**

```
Lỗi Console như sau:

[Ảnh chụp màn hình]
```

:::

### 3.3 Bổ sung thông tin Network (Vấn đề dữ liệu/API báo lỗi)

::: tip Các bước thực hiện

**Bước 1: Nhấn F12 mở Developer Tools**

**Bước 2: Chuyển sang tab Network**

**Bước 3: Thực hiện lại thao tác** (nhấp lưu/tải lại trang)

**Bước 4: Tìm request tương ứng, chụp ảnh**

- Xem URL và mã trạng thái
- Xem Payload (tham số được truyền)
- Xem Response (kết quả trả về)

**Bước 5: Gửi cho AI**

```
Thông tin Network như sau:

Request: [Ảnh chụp 1]
Tham số: [Ảnh chụp 2]
Kết quả trả về: [Ảnh chụp 3]
```

:::

### 3.4 Bổ sung thông tin Elements (Vấn đề style)

::: tip Các bước thực hiện

**Bước 1: Nhấp chuột phải vào phần tử → "Inspect"**

Developer Tools sẽ tự định vị đến phần tử đó.

**Bước 2: Chụp ảnh panel Styles**

**Bước 3: Gửi cho AI**

```
Style phần tử như sau:

[Ảnh chụp màn hình]
```

:::

## 4. Bước 3: Lặp lại cho đến khi giải quyết

### 4.1 Cách làm kém hiệu quả

Những việc này sẽ lãng phí thời gian của bạn:

- Thấy lỗi là hoảng, bắt đầu sửa code bừa bãi
- Dành nửa tiếng tìm kiếm giải pháp cho lỗi
- Cố tự hiểu từng lỗi có nghĩa gì
- Một mình debug đến tận đêm khuya

### 4.2 Cách làm hiệu quả

Làm theo quy trình này:

1. Mô tả hiện tượng + chụp màn hình hỏi trước
2. Khi AI nói cần thêm thông tin, mới mở F12 bổ sung
3. Sửa code theo gợi ý
4. Sửa xong kiểm tra, nếu vẫn còn vấn đề thì tiếp tục chụp ảnh hỏi

## 5. Tổng kết: Quy trình hoàn chỉnh

```
Gặp vấn đề
    ↓
Mô tả hiện tượng + Chụp màn hình
    ↓
Đưa cho AI: "Phải làm sao?"
    ↓
AI giải quyết ngay?
    ↓ Có
Làm theo AI nói
    ↓
Kiểm tra đã giải quyết chưa
    ↓
    ↓ Không / AI cần thêm thông tin
Mở F12, bổ sung thông tin quan trọng
    ↓
Gửi lại cho AI
    ↓
Lặp lại cho đến khi giải quyết
```
