---
title: Kỹ thuật ngữ cảnh
description: Làm thế nào để mô hình hiểu bạn mà không tốn quá nhiều chi phí, trong khi vẫn giữ nguyên cửa sổ ngữ cảnh giới hạn?
layout: doc
head:
  meta:
    - property: og:title
      content: Kỹ thuật ngữ cảnh
    - property: og:description
      content: Làm thế nào để mô hình hiểu bạn mà không tốn quá nhiều chi phí, trong khi vẫn giữ nguyên cửa sổ ngữ cảnh giới hạn?
---

# Kỹ thuật ngữ cảnh
> 💡 **Hướng dẫn học tập**: Kỹ thuật Prompt giải quyết vấn đề "làm thế nào để diễn đạt rõ ràng", còn kỹ thuật ngữ cảnh giải quyết vấn đề "làm thế nào để mô hình thấy được thông tin phù hợp vào đúng thời điểm". Chương này sẽ xoay quanh một câu hỏi: **Trong cửa sổ ngữ cảnh giới hạn, làm thế nào để mô hình vừa hiểu bạn, vừa không "đốt" hết tiền?**

Trước khi bắt đầu, bạn nên bổ sung hai "viên gạch nền tảng" sau:

-   **Token là gì**: Bạn có thể đọc phần "Phân tích từ & Token" trong [Giới thiệu về Mô hình ngôn ngữ lớn](./llm-intro.md).
-   **Prompt là gì**: Nếu bạn chưa quen với cấu trúc cơ bản của System / User / Assistant, bạn có thể xem [Kỹ thuật Prompt](./prompt-engineering/).

---

## 0. Lời mở đầu: Tại sao đang trò chuyện, AI lại quên mất mọi thứ và ngày càng đắt đỏ?

<AgentContextFlow />

Nhiều người gặp phải tình huống tương tự khi sử dụng các mô hình ngôn ngữ lớn trong thực tế:

-   Đang trò chuyện dở, mô hình đột nhiên "quên" các điều kiện quan trọng đã nói trước đó;
-   Trong các cuộc hội thoại dài, câu trả lời trước sau mâu thuẫn, khó duy trì cùng một thiết lập;
-   Số lượt trò chuyện càng nhiều, hóa đơn càng tăng như đồng hồ tính tiền taxi.

Theo trực giác, chúng ta sẽ nghĩ rằng: **"Mô hình này có trí nhớ kém"**.
Nhưng hầu hết thời gian, vấn đề không phải do mô hình "không biết nhớ", mà là do chúng ta **chưa thiết kế tốt ngữ cảnh mà nó có thể nhìn thấy**.

<IntroProblemReasonSolution />

Đối mặt với những thách thức này, việc chỉ dựa vào "viết Prompt tốt" đã trở nên không đủ. Chúng ta cần một phương pháp kỹ thuật hệ thống hơn để đảm bảo mô hình luôn nhận được thông tin quan trọng nhất trong cửa sổ và ngân sách giới hạn. Đây chính là vấn đề mà **kỹ thuật ngữ cảnh** cố gắng giải quyết.

---

## 1. "Kỹ thuật ngữ cảnh" là gì? (Định nghĩa + Kịch bản)

Đầu tiên, hãy xem một định nghĩa ngắn gọn về công việc, sau đó là một vài kịch bản điển hình.

> Kỹ thuật ngữ cảnh là một phương pháp kỹ thuật để xây dựng và quản lý "môi trường thông tin" cho LLM, quyết định "mô hình thấy gì, bỏ qua gì, và khi nào thấy", từ đó hoàn thành nhiệm vụ một cách ổn định trong cửa sổ ngữ cảnh giới hạn.

Bạn có thể đơn giản hiểu nó là ba việc: sắp xếp thông tin, kiểm soát cửa sổ, quản lý chi phí.
Các kịch bản phổ biến thường sử dụng nó bao gồm:

-   Agent đàm thoại và chatbot dịch vụ khách hàng
-   Trợ lý code / tài liệu
-   Gọi công cụ đa lượt và sắp xếp quy trình dài

Tiếp theo, chúng ta sẽ bắt đầu từ "những bài học xương máu" của một nhóm thực tế, để xem họ đã từng bước tiến hóa từ "chỉ biết viết Prompt" thành "biết làm kỹ thuật ngữ cảnh" như thế nào.

---

## 2. Bắt đầu từ "những bài học xương máu": Những sai lầm mà nhóm Manus đã mắc phải

Trường hợp này đến từ **Manus** (một AI Agent đa năng).
Khác với các cuộc trò chuyện thông thường, Manus cần tự lập kế hoạch và gọi công cụ để hoàn thành các nhiệm vụ dài (liên quan đến hàng chục hoặc thậm chí hàng trăm lượt tương tác).

Điều này dẫn đến mâu thuẫn cốt lõi:
-   **Nếu không nhớ**: Thông tin quan trọng bị mất, nhiệm vụ bị gián đoạn.
-   **Nhớ tất cả**: Chi phí và độ trễ tăng vọt, thậm chí vượt quá giới hạn cửa sổ.

Nhóm Manus đã trải qua nhiều lần tái cấu trúc kiến trúc, mới hiểu ra một điều: **Ngữ cảnh không thể chỉ dựa vào "viết", mà phải dựa vào "thiết kế".**

### 2.1 Bốn lần tái cấu trúc đã dạy chúng ta điều gì?

Ji Yichao, đồng sáng lập Manus, đã chia sẻ "lịch sử vấp ngã" của họ:

| Giai đoạn | Vấn đề gặp phải | Suy nghĩ lúc đó | Kết quả |
| :--- | :--- | :--- | :--- |
| **Lần 1** | AI quên mất mọi thứ khi trò chuyện | "Chỉ cần viết thêm Prompt là được" | Càng viết càng dài, càng đắt |
| **Lần 2** | Thông tin quan trọng luôn bị đẩy ra | "Sao chép những cái quan trọng nhiều lần" | Văn bản dài hơn, chi phí cao hơn |
| **Lần 3** | Hóa đơn cao đến mức đáng sợ | "Có thể tái sử dụng các tính toán trước đó không?" | Tìm cách giảm chi phí tính toán lặp lại |
| **Lần 4** | Không thể xử lý tài liệu dài | "Có thể tra cứu khi cần không?" | Xây dựng giải pháp "thư viện + truy xuất theo yêu cầu" |

**Bài học cốt lõi**: **Không phải nhớ càng nhiều càng tốt, mà là nhớ càng khéo càng tốt**.

### 2.2 Trí nhớ của AI thực sự giống cái gì?

**Bộ nhớ máy tính truyền thống** = **Ổ cứng**:
-   Dung lượng lớn: Có thể lưu trữ lượng lớn dữ liệu trong thời gian dài;
-   Giá thấp: Chi phí lưu trữ một năm tương đối thấp;
-   Tốc độ đọc ghi tương đối chậm, mất một thời gian để tìm kiếm thông tin.

**Ngữ cảnh của AI** = **Bảng đen nhỏ**:
-   Đọc ghi nhanh: Mô hình có thể trực tiếp nhìn thấy toàn bộ ngữ cảnh trong một lần gọi;
-   Dung lượng giới hạn: Khi đầy, buộc phải xóa nội dung cũ;
-   Mỗi Token được ghi vào đều mang lại tính toán và chi phí bổ sung.

**Kinh nghiệm của Manus**: **Bảng đen nhỏ cần được sử dụng tiết kiệm, khéo léo, đừng dùng để lưu trữ bách khoa toàn thư**.

---

## 3. Bước đầu tiên: Nhận biết chi phí - Mỗi đồng tiền của bạn được chi tiêu vào đâu?

### 3.1 Tại sao phải xem xét chi phí trước?

Hãy xem một cuộc trò chuyện AI điển hình, tiền của bạn được chi tiêu như thế nào:

```
💰 Cấu trúc chi phí (một cuộc trò chuyện):
├─ 70% Xem lại nội dung cũ ("Vừa trò chuyện gì?")
├─ 20% Xử lý nội dung mới ("Bây giờ nói gì?")
└─ 10% Tạo phản hồi ("Trả lời thế nào?")
```

**Phát hiện đáng kinh ngạc**: **70% số tiền được chi để AI đọc lại những gì bạn đã nói trước đó!**

### 3.2 KV Cache là gì? (Tái sử dụng tiền tố)

Trước khi thảo luận về giá cả, chúng ta phải hiểu một khái niệm kỹ thuật cốt lõi: **KV Cache (Bộ nhớ đệm khóa-giá trị)**.
Đừng để bị cái tên kỹ thuật này làm bạn sợ hãi, nó thực chất là "bảng tra cứu nhanh bộ nhớ ngắn hạn" của AI.

-   **Khi không có KV Cache**: AI mỗi lần đều phải đọc, hiểu, tính toán lại từ đầu như lần đầu tiên nhìn thấy bài viết này.
-   **Khi có KV Cache**: AI sẽ lưu trữ kết quả tính toán của phần đã đọc (Pre-fill). Lần sau, nếu nội dung ban đầu không thay đổi, nó sẽ trực tiếp lấy từ bộ nhớ, không cần tính toán lại.

Điều này giống như:
> Bạn đi thi.
> **Tình huống A**: Mỗi lần đều phải đọc lại toàn bộ sách giáo khoa từ đầu, rồi mới bắt đầu làm bài. (Chậm, mệt, tốn kém)
> **Tình huống B**: Nội dung sách giáo khoa bạn đã thuộc lòng (Cache), ngồi xuống làm bài ngay. (Nhanh, dễ dàng, rẻ)

Trong bảng tính phí của các nhà cung cấp dịch vụ đám mây, **"cuốn sách đã thuộc lòng" (Cache Hit)** thường rẻ hơn **"cuốn sách mới đọc" (Cache Miss)** hơn 90%.

### 3.3 Sự khác biệt về giá giữa "Học thuộc lòng" và "Tra cứu tức thì"

Lấy Claude làm ví dụ:
-   **Tra cứu tức thì** (không có cache): $3.00 / triệu từ
-   **Học thuộc lòng** (có cache): $0.30 / triệu từ
-   **Chênh lệch 10 lần**!

**Thực tiễn của Manus**: Bằng cách để AI "học thuộc lòng", họ đã giảm chi phí từ **$0.15 xuống còn $0.02**, **tiết kiệm 87%**!

<ContextWindowVisualizer />

### 3.4 Hướng dẫn tránh bẫy: Đừng để dấu thời gian phá hủy "Cache" của bạn

Nhiều nhà phát triển có thói quen viết "thời gian hiện tại" vào câu đầu tiên của System Prompt, nghĩ rằng điều này rất chặt chẽ.
**Nhưng đây thực chất là một trong những anti-pattern lớn nhất trong kỹ thuật ngữ cảnh.**

Hãy tưởng tượng: Bạn đã thuộc lòng cả một cuốn sách lịch sử (System Prompt), nhưng dòng đầu tiên của cuốn sách lại ghi "số giây hiện tại".
Nếu dòng chữ này thay đổi mỗi giây, thì tất cả nội dung bạn đã thuộc lòng ở giây trước sẽ trở nên vô dụng ở giây tiếp theo – bạn phải thuộc lòng lại từ đầu.

Đây chính là điểm yếu chí mạng của **tái sử dụng tiền tố (KV Cache)**: **Chỉ cần phần đầu thay đổi, tất cả phần sau đều phải tính toán lại.**

#### Ví dụ sai: Đặt thông tin động ở phía trước
```text
System: Bây giờ là 2024-01-01 12:00:01. Bạn là trợ lý...
(Một phút sau)
System: Bây giờ là 2024-01-01 12:01:01. Bạn là trợ lý...
```
**Hậu quả**: Mặc dù chỉ thay đổi vài chữ, nhưng vì ở đầu, dẫn đến 99% nội dung cố định phía sau không thể tái sử dụng cache, mỗi yêu cầu đều chậm và đắt như lần đầu tiên.

#### Cách làm đúng: Tách biệt động và tĩnh
```text
System: Bạn là trợ lý... (Đặt hàng nghìn từ quy tắc cố định, cơ sở tri thức ở đây)
User: (Truyền thời gian hiện tại thông qua gọi công cụ hoặc tin nhắn người dùng ở đây)
```
**Lợi ích**: Hàng nghìn từ quy tắc phía trước không bao giờ thay đổi, AI chỉ cần "thuộc lòng" một lần. Các yêu cầu tiếp theo trực tiếp gọi từ bộ nhớ, tốc độ cực nhanh.

👇 **Hãy thử nhấp vào**:
Nhấp vào công tắc bên dưới, bật **"Tăng tốc học thuộc lòng"**, sau đó nhấp nhiều lần vào "Gửi yêu cầu mới".
Quan sát xem: Khi khối nội dung đầu tiên chuyển thành "Đã thuộc lòng", **Tốc độ phản hồi đầu tiên (TTFT)** sẽ thay đổi như thế nào?

<KVCacheDemo />

---

## 4. Bước thứ hai: Sliding Window - Khi "trí nhớ" trở thành "chi phí"

Khi cuộc trò chuyện càng dài, vấn đề đầu tiên gặp phải là: **Cửa sổ đầy thì làm sao?**

### 4.1 Tại sao "vào trước ra trước" lại gây ra vấn đề?

Quản lý bộ nhớ đơn giản nhất là **Sliding Window (Cửa sổ trượt)**: **Cái mới vào, cái cũ ra**.
Nghe có vẻ công bằng, nhưng trong các nhiệm vụ thực tế lại là một thảm họa.

**Tái hiện kịch bản**:
```text
Lịch sử trò chuyện:
[1] Người dùng: Tôi là Trương Tam, phụ trách hệ thống thanh toán
[2] Người dùng: Dự án được phát triển bằng ngôn ngữ Go
[3] Người dùng: Cơ sở dữ liệu là PostgreSQL
...
[20] Người dùng: Giúp tôi viết một API
```
**Kết quả**: Khi trò chuyện đến câu thứ 20, câu thứ 1 "Tôi là Trương Tam" đã bị đẩy ra khỏi cửa sổ. AI hoàn toàn quên bạn là ai, cũng không biết bạn phụ trách hệ thống nào.

**Bản chất vấn đề**: Chiến lược này đối xử bình đẳng với **thông tin quan trọng** (danh tính, công nghệ) và **những lời vô nghĩa** ("được rồi", "đã nhận"), cùng bị loại bỏ.

### 4.2 "Hội chứng mất trí nhớ giữa chừng" - Tại sao AI luôn bỏ qua thông tin quan trọng?

Ngoài việc "quên nhanh", AI còn có một đặc điểm kỳ lạ: **Nó cũng có thể "bỏ sót"**.
Nghiên cứu cho thấy: **AI nhạy cảm nhất với phần đầu và cuối, phần giữa dễ bị bỏ qua nhất**. Đây là hiện tượng nổi tiếng **Lost in the Middle (Mất giữa chừng)**.

**Đường cong trí nhớ hình chữ U**:
```text
Vị trí: Đầu → Giữa → Cuối
Trí nhớ: Cao → Thấp → Cao
```

👇 **Hãy thử nhấp vào**:
1.  Đầu tiên hãy thử **"Sliding Window"**: Trong hộp chat bên dưới, gửi thêm vài tin nhắn, xem các cuộc trò chuyện cũ bị "đẩy ra" một cách không thương tiếc như thế nào.
2.  Sau đó xem **"Mất giữa chừng"**: Quan sát xem, khi thông tin quan trọng bị giấu ở giữa một đoạn văn bản dài, tỷ lệ truy xuất thành công có phải là thấp nhất không?

<SlidingWindowDemo />
<LostInMiddleDemo />

**Giải pháp**: Đặt thông tin quan trọng ở **đầu** (System Prompt) hoặc **cuối** (câu hỏi của người dùng).

---

## 5. Bước thứ ba: Lựa chọn giữ lại - Làm thế nào để "Ghim" thông tin quan trọng?

Nếu "vào trước ra trước" không đáng tin cậy, vậy chúng ta nên làm gì?
Câu trả lời của Manus là: **Xây dựng "hệ thống phân cấp thông tin"**.

### 5.1 Tại sao phải phân cấp thông tin?

Không còn đối xử bình đẳng với mọi thông tin, mà dựa vào mức độ quan trọng để quyết định giữ lại hay loại bỏ:

| Cấp độ | Loại thông tin | Xử lý | Ảnh hưởng chi phí |
| :--- | :--- | :--- | :--- |
| **VIP** | Thiết lập hệ thống, danh tính người dùng | **Luôn giữ lại** | +15% chi phí |
| **Quan trọng** | Mục tiêu nhiệm vụ hiện tại | **Giữ lại trong suốt nhiệm vụ** | +10% chi phí |
| **Thông thường** | Lịch sử trò chuyện thông thường | **Giữ lại 5 lượt gần nhất** | Chi phí cơ bản |
| **Có thể bỏ** | Kiến thức có thể truy xuất | **Tra cứu khi cần** | -60% chi phí |

**Tư tưởng cốt lõi**: **Dùng 25% chi phí tăng thêm, đổi lấy 90% thông tin quan trọng được giữ lại**.

### 5.2 Chiến lược "đóng đinh"

Bạn có thể tưởng tượng cửa sổ ngữ cảnh như một bảng đen:
-   **Thông tin VIP**: Dùng đinh đóng chặt **ghim** lên trên cùng của bảng đen (System Prompt).
-   **Thông tin quan trọng**: Dùng nam châm **hút** vào giữa bảng đen (Context Injection).
-   **Trò chuyện thông thường**: Viết ở nửa dưới bảng đen, khi đầy thì xóa cái cũ (Sliding Window).

👇 **Hãy thử nhấp vào**:
Hãy thử "ghim" một cuộc trò chuyện quan trọng trong bản demo bên dưới.
Quan sát xem: Khi bạn tiếp tục trò chuyện, thông tin đã ghim có luôn ở đó không, còn những thông tin không ghim thì bị đẩy ra?

<SelectiveContextDemo />

---

## 6. Bước thứ tư: RAG - Khi "trí nhớ" cần "thư viện"

Đôi khi, chúng ta cần xử lý quá nhiều thông tin (ví dụ: hàng trăm trang tài liệu kỹ thuật), bảng đen không thể viết hết. Lúc này, chúng ta cần một bộ não gắn ngoài – **RAG (Tạo sinh tăng cường truy xuất)**.

### 6.1 Tại sao "bảng đen nhỏ" không đủ dùng?

Khi Manus đối mặt với tài liệu kỹ thuật hàng triệu từ, họ đã so sánh hai cách làm:

1.  **Ghi toàn bộ**: Đặt tất cả nội dung vào ngữ cảnh cùng một lúc.
    *   **Hậu quả**: Bảng đen bị chiếm đầy ngay lập tức, xử lý cực chậm, và theo lý thuyết "mất giữa chừng", AI hoàn toàn không thể nhớ nội dung ở giữa.
    *   **Chi phí**: Khoảng $50/lần, chờ 15 giây.
2.  **Truy xuất theo yêu cầu (RAG)**: Đầu tiên tìm kiếm trong thư viện (cơ sở dữ liệu), chỉ sao chép vài đoạn liên quan lên bảng đen.
    *   **Hậu quả**: Bảng đen rất gọn gàng, AI tập trung vào thông tin quan trọng.
    *   **Chi phí**: Khoảng $0.5/lần, chờ 2 giây.

**Tiết kiệm 99% tiền, 87% thời gian!**

### 6.2 Thực hành tốt nhất "tra cứu tài liệu"

Tổng kết kinh nghiệm của Manus:
*   **Mỗi cuốn sách nên chia thành bao nhiêu đoạn?** 500-1000 từ là hiệu quả nhất.
*   **Một lần tra cứu bao nhiêu cuốn sách?** 3-5 cuốn, nhiều hơn sẽ gây nhiễu.
*   **Nên tra cứu những cuốn sách có mức độ liên quan như thế nào?** Độ tương đồng > 0.7, tránh "cố gắng ghép nối" nội dung không liên quan.

👇 **Hãy thử nhấp vào**:
Nhập câu hỏi vào ô tìm kiếm (ví dụ: "làm thế nào để đặt lại mật khẩu"), xem hệ thống tìm ra những mục liên quan nhất từ một đống tài liệu như thế nào.

<RAGSimulationDemo />

---

## 7. Bước thứ năm: Nén - Làm thế nào để "bảng đen nhỏ" viết được nhiều hơn?

Nếu tất cả thông tin đều quan trọng, thực sự không thể xóa, mà cũng không muốn tra cứu tài liệu thì sao?
Vậy thì chỉ có thể **viết chữ nhỏ lại** – đây chính là **nén ngữ cảnh**.

### 7.1 Khi nào cần "viết tắt"?
*   Tài liệu truy xuất về quá dày (>2000 từ).
*   Lịch sử trò chuyện quá dài dòng (chiếm >80% không gian bảng đen).
*   Cần trả lời nhanh, không muốn AI đọc những bài dài.

### 7.2 Ba cấp độ của "viết tắt"

| Cách nén | Tỷ lệ nén | Giữ lại gì | Kịch bản áp dụng | Hiệu quả tiết kiệm |
| :--- | :--- | :--- | :--- | :--- |
| **Kiểu tóm tắt** | 70% | Ý chính | Nắm bắt nhanh | Tiết kiệm 30% |
| **Kiểu gạch đầu dòng** | 50% | Các điểm chính | Đầu ra có cấu trúc | Tiết kiệm 50% |
| **Kiểu bảng biểu** | 30% | Dữ liệu cốt lõi | Xử lý chương trình | Tiết kiệm 70% |

👇 **Hãy thử nhấp vào**:
Chọn các chiến lược nén khác nhau, xem những bài dài dòng được rút ngắn và tinh gọn như thế nào.

<ContextCompressionDemo />

---

## 8. Tích hợp hệ thống: Xây dựng "Cung điện ký ức" của AI

Trước đó, chúng ta đã học các chiến lược độc lập như xây dựng khối:
*   **KV Cache**: Giúp chúng ta tiết kiệm tiền (Chương 3)
*   **Sliding Window**: Giúp chúng ta dọn chỗ (Chương 4)
*   **Phân cấp giữ lại**: Giúp chúng ta giữ lại trọng tâm (Chương 5)
*   **RAG**: Giúp chúng ta có thêm "bộ não gắn ngoài" (Chương 6)

Bây giờ, đã đến lúc ghép những khối này thành một lâu đài hoàn chỉnh – chúng ta gọi đó là **"Cung điện ký ức"** của Manus.

### 8.1 Xây dựng ngữ cảnh như xây nhà

Đừng coi ngữ cảnh là một đống văn bản lộn xộn, mà hãy coi nó như một kiến trúc phân tầng. Mỗi tầng đều có chức năng và "quy tắc cư trú" độc đáo của riêng nó.

👇 **Hãy thử nhấp vào**:
Nhấp vào "Bắt đầu xây dựng", xem chúng ta xây dựng cung điện này từng tầng một như thế nào.

<MemoryPalaceDemo />

### 8.2 Tại sao thiết kế này lại mạnh nhất?

Triết lý thiết kế của cung điện này thực chất là để giải quyết ba mâu thuẫn:

1.  **Nền móng (System Prompt) – Giải quyết vấn đề "đắt"**
    *   **Mâu thuẫn**: Thiết lập hệ thống (bạn là ai, quy tắc là gì) dài nhất, phải gửi mỗi lần.
    *   **Giải pháp**: Đặt nó ở tầng thấp nhất, sử dụng công nghệ **KV Cache**, miễn là không thay đổi, AI có thể "thuộc lòng toàn bộ". Trong hàng trăm lượt trò chuyện tiếp theo, chi phí tính toán cho phần này gần như bằng **0**.

2.  **Trụ cột (Task Context) – Giải quyết vấn đề "quên"**
    *   **Mâu thuẫn**: Cuộc trò chuyện dài, AI dễ quên mục tiêu nhiệm vụ ban đầu (ví dụ: "viết một trò chơi rắn săn mồi").
    *   **Giải pháp**: Sử dụng chiến lược **phân cấp giữ lại**, "ghim" mục tiêu nhiệm vụ vào tầng thứ hai. Bất kể trò chuyện bao nhiêu lượt, tầng này sẽ không bao giờ bị xóa, đảm bảo AI không quên mục đích ban đầu.

3.  **Tầng trên cùng (Chat & RAG) – Giải quyết vấn đề "lộn xộn"**
    *   **Mâu thuẫn**: Vừa có cuộc trò chuyện mới, vừa có tài liệu đã tra cứu, trộn lẫn vào nhau dễ gây nhầm lẫn.
    *   **Giải pháp**:
        *   **Phòng khách (trò chuyện)**: Quản lý bằng **Sliding Window**, chỉ giữ lại 5-10 câu gần nhất.
        *   **Thư viện (RAG)**: Tài liệu dùng xong là bỏ, không chiếm chỗ.

### 8.3 Hiệu quả thực chiến

Sau khi nhóm Manus triển khai kiến trúc này, hiệu quả rõ rệt ngay lập tức:

*   **Tiết kiệm tiền**: Vì nền móng đã được "thuộc lòng", chi phí mỗi lượt trò chuyện giảm mạnh **84%**.
*   **Nhanh hơn**: AI không cần đọc lại hàng nghìn từ mỗi lần, thời gian phản hồi trung bình giảm từ 8 giây xuống còn **2 giây**.
*   **Chính xác hơn**: Thông tin quan trọng được "ghim" chặt, không bao giờ còn tình trạng đang trò chuyện lại quên mình đang làm gì.

---

## 9. Mẫu thực chiến: Sao chép ngay

Để bạn hiểu trực quan hơn về cách cơ chế này hoạt động, chúng tôi đã chuẩn bị **mô phỏng toàn bộ chu trình** cho bạn.

Vui lòng chọn một kịch bản, nhấp vào "Tiếp theo", xem trong vài giây từ khi người dùng đặt câu hỏi đến khi AI trả lời, **Cung điện ký ức** đã động điều chỉnh, lắp ráp và dọn dẹp ngữ cảnh như thế nào.

<MemoryPalaceActionDemo />

### 📝 Thiết kế thực chiến sẵn sàng sử dụng

Nếu bạn muốn thiết kế một hệ thống tương tự Manus, đừng chỉ tập trung vào cách viết Prompt, mà hãy chú ý hơn đến **cách kiến trúc hệ thống điều phối ngữ cảnh**.

Dưới đây là **bản thiết kế hệ thống** cho hai kịch bản kinh điển, bao gồm **thiết kế Prompt** và **logic code (mã giả)**.

#### Kịch bản 1: Full Stack Developer Agent (kiểu bộ nhớ dài hạn)
> **Thách thức cốt lõi**: Chu kỳ nhiệm vụ dài, dễ quên yêu cầu ban đầu và bối cảnh dự án.
> **Chiến lược giải quyết**: Lớp System (danh tính) + Lớp Task (ghim mục tiêu) + Lớp Chat (Sliding Window).

**1. System Prompt (Lớp 1 & 2)**
```markdown
# Lớp 1: Thiết lập danh tính (System Prompt) - Không bao giờ thay đổi, sử dụng KV Cache
Bạn là một Full Stack Developer cấp cao, thành thạo Python và Vue3.
Phong cách code:
- Tên biến tuân thủ nghiêm ngặt PEP8
- Logic quan trọng phải có chú thích
- Ưu tiên sử dụng các hàm tiện ích đã có trong dự án

# Lớp 2: Khóa nhiệm vụ (Task Context) - Không được xóa trong suốt nhiệm vụ
Nhiệm vụ hiện tại: Tái cấu trúc module thanh toán (payment_module)
Ràng buộc cốt lõi:
1. Phải tương thích với API phiên bản cũ v1.0
2. Script di chuyển cơ sở dữ liệu phải là idempotent
3. Thời hạn: Thứ Sáu tuần này
```

**2. Logic lắp ráp ngữ cảnh (Pseudo-Code)**
```python
def build_engineer_context(user_input, chat_history, task_info):
    context = []

    # 1. Lớp nền móng: Thiết lập danh tính (Sử dụng KV Cache)
    # Phần nội dung này không thay đổi trong hàng trăm lượt trò chuyện, chi phí tính toán gần như bằng 0
    context.append(SYSTEM_PROMPT)

    # 2. Lớp trụ cột: Khóa nhiệm vụ (Pinned)
    # Bất kể cuộc trò chuyện dài bao nhiêu, phần này luôn được chèn sau System
    context.append(f"Nhiệm vụ hiện tại: {task_info}")

    # 3. Lớp truy xuất: Đoạn code (RAG)
    # Dựa trên câu hỏi của người dùng, tìm kiếm code liên quan trong kho code
    relevant_code = search_codebase(user_input)
    if relevant_code:
        context.append(f"Tham khảo code:\n{relevant_code}")

    # 4. Lớp tương tác: Lịch sử trò chuyện (Sliding Window)
    # Chỉ lấy 10 lượt gần nhất, tránh làm đầy ngữ cảnh
    recent_chat = chat_history[-10:]
    context.extend(recent_chat)

    # 5. Đầu vào mới nhất
    context.append(user_input)

    return context
```

#### Kịch bản 2: Smart Customer Service Agent (kiểu hỏi đáp chính xác)
> **Thách thức cốt lõi**: Nhạy cảm về chi phí, và tuyệt đối không được bịa đặt.
> **Chiến lược giải quyết**: Lớp System (ràng buộc chặt chẽ) + Lớp RAG (tiêm động).

**1. System Prompt (Lớp 1)**
```markdown
# Lớp 1: Thiết lập danh tính (System Prompt)
Bạn là một chuyên viên chăm sóc khách hàng thương mại điện tử chuyên nghiệp.
Nguyên tắc trả lời:
1. Giọng điệu nhẹ nhàng, chuyên nghiệp, súc tích
2. **Tuyệt đối cấm** bịa đặt sự thật, chỉ trả lời dựa trên [tài liệu tham khảo]
3. Nếu tài liệu không có câu trả lời, vui lòng trả lời trực tiếp "Rất xin lỗi, vấn đề này tôi cần chuyển tiếp đến tổng đài viên"
```

**2. Logic lắp ráp ngữ cảnh (Pseudo-Code)**
```python
def build_support_context(user_input):
    context = []

    # 1. Lớp nền móng: Thiết lập danh tính
    context.append(SYSTEM_PROMPT)

    # 2. Lớp thư viện: Truy xuất động (RAG)
    # Chỉ trong kịch bản dịch vụ khách hàng, RAG mới là nhân vật chính, đặt ở vị trí giữa
    docs = vector_db.search(user_input, top_k=3)

    context.append("【Bắt đầu tài liệu tham khảo】")
    for doc in docs:
        context.append(doc.content)
    context.append("【Kết thúc tài liệu tham khảo】")

    # 3. Lớp tương tác: Lịch sử cực ngắn
    # Dịch vụ khách hàng thường không cần bộ nhớ quá xa, giữ lại 3 lượt gần nhất là đủ
    context.extend(get_recent_chat(limit=3))

    context.append(user_input)

    return context
```

---

## 10. Bảng đối chiếu thuật ngữ

| Thuật ngữ tiếng Anh | Đối chiếu tiếng Việt | Giải thích |
| :--- | :--- | :--- |
| **Context Window** | Cửa sổ ngữ cảnh | Chiều dài tối đa của văn bản mà mô hình có thể xử lý cùng một lúc (bao gồm cả đầu vào và đầu ra). Nội dung vượt quá giới hạn sẽ bị cắt bớt hoặc bị quên. |
| **Token** | Token | Đơn vị nhỏ nhất mà LLM xử lý văn bản. Thường 1 Token xấp xỉ 0.75 từ tiếng Anh hoặc 0.5 ký tự tiếng Hán. Việc tính phí và giới hạn cửa sổ đều dựa trên đơn vị này. |
| **KV Cache** | KV Cache | Một kỹ thuật tăng tốc suy luận, bằng cách lưu trữ các cặp khóa-giá trị chú ý đã được tính toán, tránh tính toán lặp lại cho các tiền tố trùng lặp, giảm đáng kể độ trễ và chi phí. |
| **RAG** | RAG | Tạo sinh tăng cường truy xuất. Trước khi trả lời câu hỏi, hệ thống sẽ truy xuất thông tin liên quan từ cơ sở tri thức bên ngoài, cung cấp làm ngữ cảnh cho mô hình, nhằm giảm Hallucination và mở rộng phạm vi kiến thức. |
| **Sliding Window** | Sliding Window | Chiến lược quản lý ngữ cảnh cơ bản nhất. Giữ số lượng Token trong cửa sổ không đổi, khi nội dung mới vào, tự động loại bỏ nội dung cũ nhất. |
| **Lost in Middle** | Lost in Middle | Một hạn chế của các mô hình ngôn ngữ lớn. Nghiên cứu cho thấy mô hình ghi nhớ sâu nhất thông tin ở đầu và cuối ngữ cảnh dài, trong khi dễ bỏ qua thông tin ở phần giữa. |
| **System Prompt** | System Prompt | Lệnh nằm ở đầu cuộc trò chuyện, dùng để thiết lập danh tính, quy tắc hành vi, phong cách trả lời và nhiệm vụ cốt lõi của mô hình. |
| **Few-shot** | Few-shot | Học ít mẫu. Cung cấp một vài ví dụ "câu hỏi-trả lời" trong Prompt, giúp mô hình nhanh chóng hiểu mẫu nhiệm vụ và định dạng đầu ra. |
| **Chain of Thought** | Chain of Thought | Hướng dẫn mô hình xuất ra các bước suy luận trước khi đưa ra câu trả lời cuối cùng. Phương pháp này có thể nâng cao đáng kể khả năng giải quyết các vấn đề logic và toán học phức tạp của mô hình. |
| **Hallucination** | Hallucination | Hiện tượng mô hình tự tin tạo ra thông tin có vẻ hợp lý nhưng thực tế là sai hoặc không tồn tại. |
| **Embedding** | Embedding | Kỹ thuật chuyển đổi văn bản thành các vector số học đa chiều. Văn bản có ý nghĩa tương tự sẽ có khoảng cách gần hơn trong không gian vector, là nền tảng của tìm kiếm ngữ nghĩa. |
| **Vector DB** | Vector DB | Cơ sở dữ liệu chuyên dùng để lưu trữ và truy xuất dữ liệu vector. Hỗ trợ tìm kiếm theo độ tương đồng để nhanh chóng tìm thấy các đoạn tài liệu phù hợp nhất với truy vấn. |
| **Temperature** | Temperature | Siêu tham số kiểm soát tính ngẫu nhiên của đầu ra mô hình. Giá trị càng cao (ví dụ 0.8) đầu ra càng đa dạng, sáng tạo; giá trị càng thấp (ví dụ 0.2) đầu ra càng chắc chắn, chặt chẽ. |
| **TTFT** | TTFT | Time to First Token, tức là thời gian từ khi người dùng gửi yêu cầu đến khi mô hình xuất ra Token đầu tiên, là chỉ số quan trọng để đánh giá trải nghiệm tương tác. |

---

## Tóm tắt: Bản chất của kỹ thuật ngữ cảnh

Bốn lần tái cấu trúc của Manus cho chúng ta biết:

**Từ góc độ thực tiễn**: Không phải nhớ càng nhiều càng tốt, mà là nhớ càng có cấu trúc, càng có chọn lọc càng tốt.

**Từ góc độ chi phí**:
-   Phần lớn lãng phí đến từ việc tính toán lặp lại các tiền tố cố định, cần được giải quyết bằng cơ chế ổn định tiền tố và caching;
-   Thông tin quan trọng bị xóa nhầm thường do Sliding Window "đối xử bình đẳng", cần được giải quyết bằng chiến lược phân cấp thông tin và ghim;
-   Khi đối mặt với tài liệu và cơ sở tri thức siêu dài, việc chỉ dựa vào việc tăng Context Window là không thực tế, phải kết hợp cơ chế truy xuất và nén.

Mục tiêu là: Trong giới hạn mô hình và ngữ cảnh cho phép, đảm bảo mỗi Token được đầu tư đều có mục đích rõ ràng.
