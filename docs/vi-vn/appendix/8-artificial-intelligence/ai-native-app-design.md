# Thiết kế ứng dụng AI Native

::: tip Lời nói đầu
**Tại sao một số sản phẩm AI lại gây ấn tượng mạnh, trong khi một số khác chỉ là "vỏ bọc ChatGPT"?** Sự khác biệt không nằm ở việc sử dụng mô hình mạnh đến đâu, mà ở chỗ sản phẩm có được thiết kế từ nền tảng xoay quanh các đặc tính của AI hay không. Ứng dụng AI Native không phải là "thêm một hộp chat" vào ứng dụng truyền thống, mà là một mô hình hoàn toàn mới để suy nghĩ lại về tương tác người dùng, kiến trúc hệ thống và logic sản phẩm.
:::

**Bài viết này sẽ giúp bạn học được gì?**

Sau khi hoàn thành chương này, bạn sẽ đạt được:

-   **Nhận thức về mô hình**: Hiểu được sự khác biệt bản chất giữa ứng dụng AI Native và ứng dụng truyền thống
-   **Nguyên tắc thiết kế**: Nắm vững các nguyên tắc cốt lõi trong thiết kế sản phẩm AI Native
-   **Prompt Engineering**: Tìm hiểu cách thiết kế Prompt chất lượng cao để thúc đẩy khả năng của AI
-   **Mô hình tương tác**: Nhận biết các mô hình tương tác người dùng mới trong kỷ nguyên AI
-   **Tư duy kiến trúc**: Hiểu quy trình xử lý yêu cầu và kiến trúc hệ thống của ứng dụng AI

| Chương | Nội dung | Khái niệm cốt lõi |
|-----|------|---------|
| **Chương 1** | So sánh kiến trúc | Ứng dụng truyền thống vs ứng dụng AI Native |
| **Chương 2** | Nguyên tắc thiết kế | Tư duy AI-First, thiết kế bất định |
| **Chương 3** | Prompt Engineering | System Prompt, thiết kế template |
| **Chương 4** | Mô hình tương tác | Streaming, Multimodal, Agent |
| **Chương 5** | Quy trình yêu cầu | Vòng đời hoàn chỉnh của ứng dụng AI |

---

## 0. Toàn cảnh: Từ "thêm AI" đến "AI Native"

Trong vài năm qua, con đường AI hóa của nhiều sản phẩm thường là: có một ứng dụng hiện có, sau đó thêm một nút "trợ lý AI" ở một góc nào đó. Cách làm này giống như lắp một động cơ vào xe ngựa – nó có thể chạy, nhưng kém xa so với việc thiết kế một chiếc ô tô từ đầu.

**Ứng dụng AI Native** là một tư duy sản phẩm hoàn toàn mới: từ dòng code đầu tiên, AI đã được thiết kế như một khả năng cốt lõi, chứ không phải là một tính năng bổ sung sau này.

::: tip Ứng dụng truyền thống vs ứng dụng AI Native
-   **Ứng dụng truyền thống**: Thao tác người dùng → logic xác định → kết quả xác định. Mỗi lần nhấp "gửi đơn hàng", quy trình hoàn toàn giống nhau.
-   **Ứng dụng AI Native**: Ý định người dùng → AI hiểu → kết quả mang tính xác suất. Cùng một câu hỏi, mỗi lần trả lời có thể hơi khác nhau.
-   **Chuyển đổi cốt lõi**: Từ "viết quy tắc" sang "mô tả ý định", từ "xác định" sang "xác suất", từ "giao diện thao tác" sang "giao diện hội thoại".
:::

---

## 1. So sánh kiến trúc: Hai thế giới hoàn toàn khác biệt

Kiến trúc của ứng dụng truyền thống là mô hình "request-response": người dùng nhấp vào nút, backend thực thi logic xác định, trả về kết quả xác định. Toàn bộ quá trình có thể dự đoán, kiểm thử và tái hiện.

Ứng dụng AI Native lại giới thiệu một vai trò hoàn toàn mới – **Large Language Model (LLM)**. Nó giống như một "lớp trung gian thông minh", nhận đầu vào ngôn ngữ tự nhiên và xuất ra kết quả ngôn ngữ tự nhiên. Điều này mang lại những thay đổi cơ bản về kiến trúc.

<AINativeArchDemo />

| Chiều | Ứng dụng truyền thống | Ứng dụng AI Native |
|------|---------|------------|
| Cách thức nhập | Form, nút, dropdown | Ngôn ngữ tự nhiên, hình ảnh, giọng nói |
| Logic xử lý | if-else, rule engine | Suy luận LLM, Prompt driven |
| Đặc tính đầu ra | Xác định, có thể tái hiện | Xác suất, mỗi lần có thể khác |
| Đặc điểm độ trễ | Mili giây | Giây (cần Streaming) |
| Xử lý lỗi | Mã lỗi rõ ràng | Ảo giác, từ chối trả lời, trả lời sai trọng tâm |
| Mô hình chi phí | Tài nguyên tính toán cố định | Tính phí theo token, chi phí biến động lớn |

::: tip Ba giai đoạn tiến hóa của kiến trúc
1.  **AI Enhanced**: Nhúng tính năng AI vào ứng dụng hiện có (ví dụ: tự động hoàn thành, đề xuất thông minh)
2.  **AI Collaborative**: AI là phương thức tương tác cốt lõi, nhưng vẫn có UI truyền thống hỗ trợ (ví dụ: Notion AI, GitHub Copilot)
3.  **AI Native**: Toàn bộ sản phẩm được xây dựng xoay quanh AI, nếu bỏ AI thì sản phẩm không còn tồn tại (ví dụ: ChatGPT, Cursor, Midjourney)
:::

---

## 2. Nguyên tắc thiết kế: "Hiến pháp" của sản phẩm AI Native

Thiết kế ứng dụng AI Native không thể sao chép tư duy thiết kế phần mềm truyền thống. Tính xác suất, độ trễ và sự khó đoán của AI đòi hỏi chúng ta phải xây dựng một bộ nguyên tắc thiết kế hoàn toàn mới.

<AIDesignPrincipleDemo />

::: tip Năm nguyên tắc thiết kế cốt lõi
1.  **Chấp nhận sự bất định**: Đầu ra của AI không đáng tin cậy 100%, thiết kế sản phẩm phải tính đến trường hợp "AI có thể mắc lỗi". Cung cấp cơ chế chỉnh sửa, thử lại, phản hồi, để người dùng luôn có quyền kiểm soát.
2.  **Niềm tin tăng dần**: Đừng để AI đưa ra các quyết định rủi ro cao ngay từ đầu. Hãy bắt đầu từ các kịch bản rủi ro thấp để xây dựng lòng tin của người dùng, sau đó dần dần mở rộng quyền tự chủ của AI.
3.  **Minh bạch và giải thích được**: Cho người dùng biết AI đang làm gì, tại sao lại làm như vậy. Hiển thị quá trình suy luận, trích dẫn nguồn, chú thích độ tin cậy.
4.  **Hợp tác giữa người và máy**: AI không thay thế con người, mà là tăng cường khả năng của con người. Thiết kế tốt nhất là để AI làm bản nháp, con người làm bản cuối cùng.
5.  **Giảm cấp một cách linh hoạt (Graceful Degradation)**: Khi dịch vụ AI không khả dụng hoặc kết quả không như mong muốn, sản phẩm vẫn có thể sử dụng được. Luôn có Plan B.
:::

---

## 3. Prompt Engineering: "Ngôn ngữ lập trình" của ứng dụng AI

Trong ứng dụng truyền thống, bạn dùng code để nói cho máy tính biết phải làm gì. Trong ứng dụng AI Native, bạn dùng Prompt để nói cho mô hình biết phải làm gì. **Prompt chính là ngôn ngữ lập trình của kỷ nguyên AI** – viết tốt, AI thể hiện xuất sắc; viết kém, AI nói lung tung.

<PromptDesignDemo />

::: tip Cấu trúc bốn lớp của thiết kế Prompt
1.  **System Prompt**: Định nghĩa vai trò, giới hạn khả năng và quy tắc hành vi của AI. Đây là chỉ thị cấp "hiến pháp", người dùng không thấy nhưng luôn có hiệu lực.
2.  **Context Injection**: Thông qua các tài liệu liên quan được truy xuất bằng RAG, lịch sử người dùng, v.v., cung cấp thông tin nền tảng cần thiết cho AI để trả lời.
3.  **User Message**: Câu hỏi hoặc chỉ thị thực tế của người dùng.
4.  **Output Format Constraint**: Chỉ định định dạng đầu ra của AI (JSON, Markdown, template cụ thể), đảm bảo kết quả có thể được chương trình phân tích.
:::

| Kỹ thuật Prompt | Giải thích | Hiệu quả |
|------------|------|------|
| Đặt vai trò | "Bạn là một Frontend Engineer cấp cao" | Nâng cao chất lượng trả lời trong lĩnh vực chuyên môn |
| Few-shot Example | Đưa ra 2-3 ví dụ input-output | Giúp mô hình hiểu định dạng và phong cách mong muốn |
| Chain-of-Thought (CoT) | "Hãy suy nghĩ từng bước một" | Nâng cao độ chính xác của suy luận phức tạp |
| Ràng buộc đầu ra | "Trả lời bằng định dạng JSON" | Đảm bảo đầu ra có thể được chương trình phân tích |
| Chỉ thị phủ định | "Đừng bịa đặt thông tin không chắc chắn" | Giảm ảo giác và thông tin sai lệch |

---

## 4. Mô hình tương tác: Trải nghiệm người dùng trong kỷ nguyên AI

Ứng dụng AI Native đã tạo ra một loạt các mô hình tương tác hoàn toàn mới. Tương tác của ứng dụng truyền thống là "nhấp - chờ - xem", trong khi tương tác của ứng dụng AI giống như "đối thoại - quan sát - điều chỉnh".

<AIUXPatternDemo />

::: tip Bốn mô hình tương tác cốt lõi
1.  **Streaming**: AI hiển thị nội dung từng chữ một khi đang tạo, thay vì đợi tạo xong toàn bộ rồi mới hiển thị. Điều này giúp giảm đáng kể thời gian chờ đợi nhận thức của người dùng, và cũng cho phép người dùng đánh giá xem hướng đi có đúng không trong quá trình tạo.
2.  **Multi-turn Conversation**: Thực hiện hội thoại liên tục thông qua bộ nhớ ngữ cảnh, người dùng có thể dần dần tinh chỉnh yêu cầu. Thử thách chính là quản lý cửa sổ ngữ cảnh và nén lịch sử hội thoại.
3.  **Multimodal Interaction**: Hỗ trợ nhiều phương thức nhập liệu như văn bản, hình ảnh, giọng nói, tệp, và AI cũng có thể xuất ra nhiều định dạng như hình ảnh, code, bảng.
4.  **Agent Mode**: AI không chỉ trả lời câu hỏi mà còn tự chủ lập kế hoạch, thực hiện các tác vụ đa bước. Người dùng đưa ra mục tiêu, AI tự phân tách các bước và hoàn thành từng bước một.
:::

---

## 5. Quy trình yêu cầu: Vòng đời hoàn chỉnh của một lời gọi AI

Khi người dùng gửi một tin nhắn trong ứng dụng AI, điều gì đã xảy ra đằng sau? Hiểu quy trình hoàn chỉnh này là nền tảng để xây dựng ứng dụng AI đáng tin cậy.

<AIAppFlowDemo />

::: tip Sáu giai đoạn xử lý yêu cầu
1.  **Tiền xử lý đầu vào**: Xác thực đầu vào người dùng, kiểm duyệt an toàn nội dung, ẩn danh thông tin nhạy cảm
2.  **Ghép nối ngữ cảnh**: Nối System Prompt, truy xuất tài liệu liên quan (RAG), tải lịch sử hội thoại
3.  **Gọi mô hình**: Gửi Prompt đã ghép nối đến LLM API, bắt đầu phản hồi Streaming
4.  **Hậu xử lý đầu ra**: Định dạng đầu ra, lọc an toàn nội dung, trích xuất dữ liệu có cấu trúc
5.  **Lưu cache kết quả**: Lưu cache kết quả cho các câu hỏi phổ biến, giảm chi phí và độ trễ
6.  **Giám sát ghi lại**: Ghi lại mức sử dụng token, thời gian phản hồi, phản hồi người dùng, để tối ưu hóa liên tục
:::

| Giai đoạn | Cân nhắc chính | Vấn đề thường gặp |
|------|---------|---------|
| Tiền xử lý đầu vào | Bảo vệ chống Prompt Injection, giới hạn độ dài | Prompt Injection, tấn công Jailbreak |
| Ghép nối ngữ cảnh | Phân bổ ngân sách token, ưu tiên thông tin | Ngữ cảnh tràn, thông tin quan trọng bị cắt |
| Gọi mô hình | Xử lý timeout, chiến lược thử lại, truyền Streaming | API rate limit, network timeout |
| Hậu xử lý đầu ra | Xác thực định dạng, phát hiện ảo giác | Định dạng đầu ra không như mong đợi |
| Chiến lược cache | Semantic cache vs Exact cache | Tỷ lệ cache hit thấp |
| Giám sát cảnh báo | Giám sát chi phí, đánh giá chất lượng | Chi phí token vượt tầm kiểm soát |

---

## Tóm tắt

Thiết kế ứng dụng AI Native không chỉ đơn giản là thêm tính năng AI vào ứng dụng truyền thống, mà là tái cấu trúc toàn diện từ kiến trúc, tương tác, đến các thực hành kỹ thuật.

Ôn lại các điểm chính của chương này:

1.  **Chuyển đổi kiến trúc**: Từ logic xác định sang suy luận xác suất, ứng dụng AI Native cần tư duy kiến trúc hoàn toàn mới
2.  **Nguyên tắc thiết kế**: Chấp nhận sự bất định, niềm tin tăng dần, minh bạch và giải thích được, hợp tác giữa người và máy, giảm cấp một cách linh hoạt
3.  **Prompt là cốt lõi**: Prompt Engineering là "ngôn ngữ lập trình" của ứng dụng AI, trực tiếp quyết định chất lượng sản phẩm
4.  **Đổi mới tương tác**: Streaming, Multi-turn Conversation, Multimodal, Agent Mode định nghĩa lại trải nghiệm người dùng
5.  **Tư duy toàn chuỗi**: Từ tiền xử lý đầu vào đến giám sát cảnh báo, mỗi giai đoạn đều cần được thiết kế đặc biệt cho các đặc tính của AI

## Đọc thêm

-   [Google PAIR Guidelines](https://pair.withgoogle.com/) - Hướng dẫn thiết kế AI tương tác giữa người và máy của Google
-   [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) - Các thực hành tốt nhất về Prompt Engineering chính thức
-   [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) - Hướng dẫn thiết kế Prompt của Claude
-   [Nielsen Norman Group: AI UX](https://www.nngroup.com/topic/artificial-intelligence/) - Nghiên cứu trải nghiệm người dùng AI
-   [Building LLM Applications](https://www.oreilly.com/library/view/building-llm-powered/9781835462317/) - Hướng dẫn thực hành xây dựng ứng dụng LLM
