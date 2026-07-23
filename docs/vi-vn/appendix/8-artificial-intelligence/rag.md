# RAG: Truy vấn Tăng cường Sinh (Retrieval-Augmented Generation)

::: tip Lời nói đầu
**Tại sao ChatGPT đôi khi lại "nói dối một cách nghiêm túc"?** Kiến thức của các mô hình ngôn ngữ lớn đến từ dữ liệu huấn luyện, nhưng dữ liệu huấn luyện có ngày cắt, và cũng không bao gồm các tài liệu nội bộ của công ty bạn. RAG (Retrieval-Augmented Generation) chính là công nghệ cốt lõi để giải quyết vấn đề này – cho phép AI "tra cứu tài liệu" trước khi đưa ra câu trả lời.
:::

**Bài viết này sẽ giúp bạn học được gì?**

Sau khi hoàn thành chương này, bạn sẽ đạt được:

- **Hiểu biết về khái niệm cốt lõi**: Nắm rõ RAG là gì, tại sao cần nó, và cách nó giải quyết vấn đề "ảo giác" của các mô hình lớn
- **Nhận thức về quy trình hoàn chỉnh**: Nắm vững quy trình end-to-end từ tải tài liệu, phân đoạn (chunking), vector hóa đến truy vấn và sinh nội dung
- **Khả năng lựa chọn công nghệ**: Hiểu rõ ưu nhược điểm của các chiến lược phân đoạn và phương pháp truy vấn khác nhau, có thể đưa ra lựa chọn phù hợp với từng kịch bản
- **Góc nhìn về sự phát triển kiến trúc**: Hiểu lộ trình tiến hóa của RAG từ Naive đến Advanced rồi đến Modular
- **Khả năng ra quyết định thực tiễn**: Biết khi nào nên sử dụng RAG và khi nào nên sử dụng fine-tuning

| Chương | Nội dung | Khái niệm cốt lõi |
|-----|------|---------|
| **Chương 1** | Quy trình cơ bản của RAG | Ba giai đoạn: lập chỉ mục, truy vấn, sinh nội dung |
| **Chương 2** | Chiến lược phân đoạn văn bản | Phân đoạn cố định, phân đoạn ngữ nghĩa, phân đoạn đệ quy |
| **Chương 3** | Kỹ thuật truy vấn | Truy vấn vector, truy vấn từ khóa, truy vấn kết hợp |
| **Chương 4** | Tiến hóa kiến trúc | Naive RAG → Advanced RAG → Modular RAG |
| **Chương 5** | RAG vs Fine-tuning | So sánh kịch bản áp dụng của hai giải pháp |

---

## 0. Toàn cảnh: Tại sao các mô hình lớn cần "tra cứu tài liệu"?

Hãy tưởng tượng bạn là một giáo sư uyên bác, đã đọc vô số sách. Nhưng nếu ai đó hỏi bạn "doanh số bán hàng của công ty hôm qua là bao nhiêu", bạn chắc chắn không thể trả lời – vì những thông tin này không có trong sách bạn đã đọc.

Các mô hình ngôn ngữ lớn cũng đối mặt với tình thế khó khăn tương tự:

- **Kiến thức có ngày cắt**: Dữ liệu huấn luyện của GPT-4 có ngày cắt nhất định, những sự kiện xảy ra sau đó nó không biết
- **Thiếu kiến thức riêng tư**: Các tài liệu nội bộ, hướng dẫn sản phẩm, dữ liệu khách hàng của công ty bạn, mô hình chưa bao giờ thấy
- **Dễ tạo ra ảo giác**: Khi mô hình không chắc chắn về câu trả lời, nó có xu hướng "bịa đặt" một câu trả lời có vẻ hợp lý

::: tip Tư tưởng cốt lõi của RAG
Giải pháp của RAG rất trực quan: **trước khi để mô hình trả lời, hãy giúp nó tìm các tài liệu tham khảo liên quan**. Giống như một kỳ thi mở sách – bạn không cần nhớ tất cả kiến thức, chỉ cần biết tìm ở đâu và tìm như thế nào.

RAG = Truy vấn (Retrieval) + Tăng cường (Augmented) + Sinh (Generation)
:::

---

## 1. Quy trình cơ bản của RAG: Lập chỉ mục, Truy vấn, Sinh nội dung

Quy trình làm việc của RAG có thể chia thành hai giai đoạn: **lập chỉ mục ngoại tuyến** và **truy vấn trực tuyến**.

Giai đoạn ngoại tuyến giống như công việc lập danh mục của thư viện – phân loại, đánh số, đưa tất cả sách lên kệ, thuận tiện cho việc tra cứu sau này. Giai đoạn trực tuyến là quá trình độc giả đến thư viện tra cứu tài liệu – tìm sách liên quan dựa trên câu hỏi, sau đó tổng hợp thông tin để đưa ra câu trả lời.

<RAGPipelineDemo />

::: tip Ba giai đoạn cốt lõi
1.  **Giai đoạn lập chỉ mục (Indexing)**: Tải, làm sạch, phân đoạn các tài liệu gốc, sau đó chuyển đổi thành vector thông qua mô hình nhúng (embedding model) và lưu vào cơ sở dữ liệu vector. Đây là công việc chuẩn bị một lần.
2.  **Giai đoạn truy vấn (Retrieval)**: Khi người dùng đặt câu hỏi, câu hỏi cũng được chuyển đổi thành vector, sau đó tìm kiếm các đoạn tài liệu tương tự nhất trong cơ sở dữ liệu vector.
3.  **Giai đoạn sinh nội dung (Generation)**: Nối các đoạn tài liệu đã truy vấn được và câu hỏi của người dùng lại với nhau thành một Prompt, sau đó giao cho mô hình ngôn ngữ lớn để tạo ra câu trả lời cuối cùng.
:::

| Giai đoạn | Đầu vào | Đầu ra | Kỹ thuật chính |
|------|------|------|---------|
| Lập chỉ mục | Tài liệu gốc | Cơ sở dữ liệu vector | Phân đoạn văn bản, mô hình nhúng |
| Truy vấn | Câu hỏi người dùng | Top-K đoạn tài liệu | Độ tương đồng vector, Reranking |
| Sinh nội dung | Câu hỏi + Ngữ cảnh | Câu trả lời cuối cùng | Prompt engineering, LLM |

---

## 2. Phân đoạn văn bản: Đưa voi vào tủ lạnh

Phân đoạn văn bản là khâu dễ bị bỏ qua nhất trong RAG, nhưng lại có ảnh hưởng lớn nhất đến hiệu quả. Tại sao cần phân đoạn? Bởi vì cửa sổ ngữ cảnh của các mô hình lớn có giới hạn, chúng ta không thể nhét cả một cuốn sách vào đó. Quan trọng hơn, **chất lượng của việc phân đoạn trực tiếp quyết định chất lượng của việc truy vấn**.

Hãy tưởng tượng bạn đang tìm một điểm kiến thức cụ thể trong một cuốn sách ở thư viện. Nếu cả cuốn sách là một "đoạn" (chunk), việc truy vấn được cũng vô ích – bạn vẫn phải lật hết cả cuốn sách. Nhưng nếu phân đoạn theo chương hoặc thậm chí đoạn văn, bạn có thể định vị chính xác nội dung mình cần.

<ChunkingStrategyDemo />

::: tip Lựa chọn chiến lược phân đoạn
-   **Phân đoạn kích thước cố định**: Cắt theo số ký tự hoặc số token, đơn giản nhưng có thể cắt đứt ngữ nghĩa
-   **Phân đoạn đệ quy**: Đầu tiên phân theo đoạn văn, nếu đoạn quá dài thì phân theo câu, giữ nguyên tính toàn vẹn ngữ nghĩa
-   **Phân đoạn ngữ nghĩa**: Sử dụng mô hình nhúng để xác định ranh giới ngữ nghĩa, cắt tại những điểm thay đổi độ tương đồng đột ngột
-   **Phân đoạn theo cấu trúc tài liệu**: Sử dụng thông tin cấu trúc như tiêu đề Markdown, thẻ HTML để phân đoạn

Không có chiến lược phân đoạn "tốt nhất", chỉ có chiến lược phù hợp nhất với dữ liệu của bạn. Thông thường, nên bắt đầu với phân đoạn đệ quy, kích thước chunk từ 200-500 tokens, overlap 10-20%.
:::

---

## 3. Kỹ thuật truy vấn: Làm thế nào để tìm nội dung liên quan nhất?

Sau khi hoàn tất phân đoạn, câu hỏi quan trọng tiếp theo là: **Khi người dùng đặt một câu hỏi, làm thế nào để tìm ra những đoạn tài liệu liên quan nhất từ hàng ngàn đoạn tài liệu?**

Điều này giống như việc tìm sách trong một thư viện khổng lồ. Bạn có thể tìm kiếm theo từ khóa tên sách (truy vấn từ khóa), hoặc mô tả bạn muốn nội dung gì để thủ thư giúp bạn tìm (truy vấn ngữ nghĩa), cách tốt nhất là kết hợp cả hai (truy vấn kết hợp).

<RetrievalDemo />

| Phương thức truy vấn | Nguyên lý | Ưu điểm | Nhược điểm |
|---------|------|------|------|
| Truy vấn từ khóa (BM25) | Dựa trên tần suất từ và tần suất tài liệu nghịch đảo | Khớp chính xác, tốc độ nhanh | Không thể hiểu ngữ nghĩa, từ đồng nghĩa không hiệu quả |
| Truy vấn vector | Dựa trên độ tương đồng cosine của vector nhúng | Hiểu ngữ nghĩa, hỗ trợ khớp mờ | Không nhạy cảm với thuật ngữ chuyên ngành |
| Truy vấn kết hợp | Kết hợp kết quả truy vấn từ khóa và vector | Cân bằng giữa độ chính xác và ngữ nghĩa | Cần điều chỉnh trọng số, độ phức tạp cao |

::: tip Sắp xếp lại (Reranking)
Sau khi truy vấn được các tài liệu ứng viên, thường cần thêm một bước "sắp xếp lại". Truy vấn ban đầu ưu tiên độ bao phủ (cố gắng không bỏ sót), sắp xếp lại ưu tiên độ chính xác (đặt những tài liệu liên quan nhất lên đầu). Các mô hình reranking phổ biến bao gồm Cohere Rerank, BGE Reranker, v.v., chúng sử dụng bộ mã hóa chéo (cross-encoder) để chấm điểm chi tiết cho cặp query-document.
:::

---

## 4. Tiến hóa kiến trúc: Từ đơn giản đến thông minh

Công nghệ RAG đã trải qua ba thế hệ tiến hóa chỉ trong hai năm, mỗi thế hệ đều giải quyết các vấn đề của thế hệ trước.

<RAGArchitectureDemo />

::: tip So sánh ba thế hệ kiến trúc RAG
-   **Naive RAG (2023)**: Quy trình "lập chỉ mục → truy vấn → sinh nội dung" cơ bản nhất, triển khai đơn giản nhưng hiệu quả hạn chế. Các vấn đề bao gồm: chất lượng truy vấn không ổn định, không thể xử lý các truy vấn phức tạp, dễ đưa vào ngữ cảnh nhiễu.
-   **Advanced RAG (2024)**: Dựa trên Naive RAG, bổ sung các bước tối ưu hóa như viết lại truy vấn, truy vấn kết hợp, reranking, nén ngữ cảnh, v.v., giúp cải thiện đáng kể độ chính xác của truy vấn và chất lượng sinh nội dung.
-   **Modular RAG (2025)**: Phân tách RAG thành các module có thể cắm ghép, hỗ trợ các khả năng nâng cao như phán đoán định tuyến, truy vấn thích ứng, tự phản tư. Có thể lựa chọn quy trình xử lý tối ưu một cách linh hoạt dựa trên loại truy vấn.
:::

---

## 5. RAG vs Fine-tuning: Nên chọn cái nào?

Khi bạn muốn mô hình ngôn ngữ lớn nắm vững kiến thức trong một lĩnh vực cụ thể, thường có hai con đường: RAG và fine-tuning. Chúng không loại trừ lẫn nhau mà là bổ trợ cho nhau.

Lấy một ví dụ: **fine-tuning giống như cho học sinh đi học thêm**, giúp kiến thức được nội hóa vào não; **RAG giống như phát sách tham khảo cho học sinh**, có thể lật xem khi thi. Cả hai phương pháp đều có ưu nhược điểm riêng, điều quan trọng là nhu cầu cụ thể của bạn.

<RAGvsFineTuningDemo />

| Khía cạnh | RAG | Fine-tuning |
|------|-----|------|
| Cập nhật kiến thức | Cập nhật theo thời gian thực, chỉ cần sửa tài liệu | Cần huấn luyện lại |
| Chi phí | Thấp (không cần huấn luyện bằng GPU) | Cao (cần tài nguyên huấn luyện) |
| Khả năng giải thích | Cao (có thể truy xuất nguồn gốc) | Thấp (kiến thức được nội hóa trong trọng số) |
| Kịch bản áp dụng | Hỏi đáp cơ sở tri thức, truy vấn tài liệu | Chuyển đổi phong cách, tối ưu hóa tác vụ cụ thể |
| Kiểm soát ảo giác | Tốt hơn (có cơ sở tham chiếu) | Trung bình (vẫn có thể ảo giác) |

::: tip Lời khuyên thực tiễn
Trong hầu hết các trường hợp, **hãy thử RAG trước**. Ưu điểm của RAG là: không cần huấn luyện, kiến thức có thể cập nhật theo thời gian thực, câu trả lời có thể truy xuất nguồn gốc. Chỉ khi bạn cần thay đổi "chế độ hành vi" của mô hình (ví dụ: định dạng đầu ra, phong cách ngôn ngữ, cách suy luận), thì mới xem xét fine-tuning. Giải pháp mạnh mẽ nhất thường là sự kết hợp của **RAG + fine-tuning**.
:::

---

## Tóm tắt

RAG là một trong những công nghệ thực tiễn nhất hiện nay để đưa các mô hình ngôn ngữ lớn "vào thực tế". Giá trị cốt lõi của nó nằm ở việc: giúp câu trả lời của mô hình có cơ sở, kiến thức có thể cập nhật theo thời gian thực, và ảo giác có thể được kiểm soát hiệu quả.

Ôn lại các điểm chính trong chương này:

1.  **Vấn đề cốt lõi RAG giải quyết**: Kiến thức của mô hình lớn lỗi thời, thiếu dữ liệu riêng tư, dễ ảo giác
2.  **Quy trình ba giai đoạn**: Lập chỉ mục (chuẩn bị ngoại tuyến) → Truy vấn (tìm kiếm trực tuyến) → Sinh nội dung (tổng hợp câu trả lời)
3.  **Phân đoạn là nền tảng**: Chất lượng phân đoạn trực tiếp quyết định chất lượng truy vấn, việc lựa chọn chiến lược phân đoạn phù hợp là cực kỳ quan trọng
4.  **Truy vấn là chìa khóa**: Truy vấn kết hợp + Reranking là sự kết hợp mang lại hiệu quả tốt nhất hiện nay
5.  **Kiến trúc đang tiến hóa**: Từ Naive RAG đến Modular RAG, hệ thống ngày càng thông minh và linh hoạt
6.  **RAG và fine-tuning bổ trợ nhau**: Trong hầu hết các trường hợp, hãy thử RAG trước, chỉ khi cần thay đổi hành vi của mô hình thì mới xem xét fine-tuning

## Đọc thêm

- [Hướng dẫn RAG của LangChain](https://python.langchain.com/docs/tutorials/rag/) - Hướng dẫn thực hành framework RAG phổ biến nhất
- [Tài liệu LlamaIndex](https://docs.llamaindex.ai/) - Framework tập trung vào RAG, cung cấp nhiều trình kết nối dữ liệu phong phú
- [Bài báo RAG Survey](https://arxiv.org/abs/2312.10997) - Tổng quan toàn diện về công nghệ RAG
- [Chunking Strategies](https://www.pinecone.io/learn/chunking-strategies/) - Giải thích chi tiết các chiến lược phân đoạn của Pinecone
- [So sánh cơ sở dữ liệu vector](https://superlinked.com/vector-db-comparison) - So sánh tính năng của các cơ sở dữ liệu vector phổ biến
