# Embedding và Truy vấn Vector

::: tip Lời nói đầu
**Máy tính làm thế nào để hiểu rằng "mèo và chó rất giống nhau, nhưng không giống ô tô"?** Đối với con người, đây là kiến thức thông thường, nhưng đối với máy tính, "mèo", "chó", "ô tô" chỉ là ba chuỗi ký tự không liên quan gì đến nhau. Công nghệ Embedding (nhúng) chính là chìa khóa để giải quyết vấn đề này – nó biến văn bản thành các vector số, giúp máy tính cũng có thể hiểu được sự "gần gũi, thân thiết" về mặt ngữ nghĩa.
:::

**Bài viết này sẽ giúp bạn học được gì?**

Sau khi hoàn thành chương này, bạn sẽ có được:

-   **Hiểu trực quan**: Nắm rõ Embedding là gì, tại sao vector của "mèo" và "chó" lại gần nhau
-   **Tính toán độ tương đồng**: Nắm vững các phương pháp đo lường cốt lõi như Cosine Similarity, Euclidean Distance
-   **Nguyên lý lập chỉ mục**: Hiểu cách cơ sở dữ liệu vector truy vấn hàng triệu dữ liệu trong mili giây
-   **Lựa chọn công nghệ**: Tìm hiểu đặc điểm và kịch bản ứng dụng của các cơ sở dữ liệu vector phổ biến
-   **Quy trình đầu cuối**: Nắm vững Pipeline hoàn chỉnh từ văn bản đến vector đến truy vấn

| Chương | Nội dung | Khái niệm cốt lõi |
|-------|----------|-----------------|
| **Chương 1** | Khái niệm Embedding | Không gian ngữ nghĩa, biểu diễn vector |
| **Chương 2** | Tính toán độ tương đồng | Cosine Similarity, Euclidean Distance |
| **Chương 3** | Lập chỉ mục vector | Tìm kiếm vét cạn vs ANN |
| **Chương 4** | Cơ sở dữ liệu vector | Pinecone, Milvus, Chroma |
| **Chương 5** | Pipeline đầu cuối | Văn bản → Vector → Lưu trữ → Truy vấn |

---

## 0. Toàn cảnh: Cầu nối từ văn bản đến con số

Trong thế giới Xử lý ngôn ngữ tự nhiên, có một thách thức cơ bản: **máy tính chỉ nhận biết các con số, không nhận biết văn bản**.

Cách làm ban đầu là gán cho mỗi từ một mã số (One-Hot encoding), ví dụ "mèo"=001, "chó"=010, "ô tô"=100. Nhưng cách này có một vấn đề chí mạng: **khoảng cách giữa tất cả các từ đều như nhau**. Khoảng cách từ "mèo" đến "chó" hoàn toàn giống với khoảng cách từ "mèo" đến "ô tô" – điều này rõ ràng không phù hợp với trực giác của chúng ta.

Sự cách mạng của Embedding nằm ở chỗ: nó ánh xạ mỗi từ vào một **không gian vector mật độ thấp, dày đặc**, khiến các từ có ngữ nghĩa tương tự tự nhiên tập hợp lại với nhau. Trong không gian này, "mèo" và "chó" nằm rất gần nhau, trong khi "ô tô" lại ở xa – máy tính cuối cùng đã có thể "hiểu" ngữ nghĩa.

::: tip Bước nhảy vọt từ One-Hot đến Embedding
-   **One-Hot**: Chiều = kích thước từ vựng (có thể vài chục nghìn chiều), mỗi vector chỉ có một số 1, còn lại là 0, thưa thớt và không có ngữ nghĩa
-   **Embedding**: Chiều thường là 768~1536, mỗi con số đều có ý nghĩa, dày đặc và chứa nhiều thông tin ngữ nghĩa
-   **Đột phá quan trọng**: Word2Vec (2013) đã chứng minh rằng "ý nghĩa của một từ có thể được định nghĩa bằng ngữ cảnh của nó", mở ra kỷ nguyên Embedding
:::

---

## 1. Khái niệm Embedding: Biến văn bản thành tọa độ

Ý tưởng cốt lõi của Embedding có thể tóm tắt trong một câu: **Sử dụng một tập hợp các con số (vector) để biểu diễn ý nghĩa của một từ hoặc một câu**.

Hãy tưởng tượng một hệ tọa độ hai chiều. Chúng ta đặt "mèo" tại tọa độ (0.2, 0.7), "chó" tại (0.3, 0.6), "ô tô" tại (0.9, 0.1). Bạn sẽ thấy tọa độ của "mèo" và "chó" rất gần nhau, trong khi "ô tô" lại cách xa chúng. Đây chính là trực giác của Embedding – **độ tương đồng ngữ nghĩa biến thành khoảng cách không gian**.

<EmbeddingConceptDemo />

::: tip Ba đặc tính quan trọng của Embedding
1.  **Phân cụm ngữ nghĩa**: Các từ có ý nghĩa tương tự sẽ tự động tập hợp lại với nhau (một cụm động vật, một cụm thức ăn, một cụm công nghệ)
2.  **Quan hệ tương tự**: Các phép toán vector có thể biểu diễn quan hệ ngữ nghĩa, ví dụ kinh điển: king - man + woman ≈ queen
3.  **Ý nghĩa chiều**: Mỗi chiều ẩn chứa một đặc trưng ngữ nghĩa nào đó (như "có phải là động vật không", "kích thước", "khuynh hướng cảm xúc", v.v.)
:::

| Phương pháp mã hóa | Chiều | Thông tin ngữ nghĩa | Ứng dụng điển hình |
|--------------------|-------|--------------------|--------------------|
| One-Hot            | Kích thước từ vựng (~50000) | Không               | NLP truyền thống     |
| Word2Vec           | 100~300 | Ngữ nghĩa cấp từ    | Độ tương đồng từ, suy luận tương tự |
| BERT Embedding     | 768   | Ngữ nghĩa ngữ cảnh | Hiểu câu, hỏi đáp   |
| OpenAI text-embedding-3 | 1536~3072 | Ngữ nghĩa sâu sắc   | RAG, tìm kiếm ngữ nghĩa |

---

## 2. Tính toán độ tương đồng: Các vector giữa nhau "gần" đến mức nào?

Khi đã có biểu diễn vector, câu hỏi tiếp theo tự nhiên là: **làm thế nào để đo lường mức độ tương đồng giữa hai vector?** Điều này giống như đo khoảng cách giữa hai thành phố trên bản đồ – bạn có thể đo khoảng cách đường thẳng, hoặc xem hướng có giống nhau không.

<VectorSimilarityDemo />

::: tip Hai phương pháp đo lường cốt lõi
-   **Cosine Similarity**: Đo lường **hướng** của hai vector có giống nhau không, giá trị trong khoảng [-1, 1]. 1 nghĩa là hướng hoàn toàn giống nhau, 0 nghĩa là trực giao (không liên quan), -1 nghĩa là hoàn toàn ngược lại. Là lựa chọn hàng đầu để so sánh ngữ nghĩa văn bản vì nó không bị ảnh hưởng bởi độ dài vector.
-   **Euclidean Distance**: Đo lường **khoảng cách đường thẳng** giữa hai điểm cuối của vector, giá trị trong khoảng [0, ∞). 0 nghĩa là hoàn toàn trùng khớp, giá trị càng lớn càng không tương đồng. Phù hợp với các kịch bản cần xem xét "kích thước tuyệt đối".
:::

| Phương pháp đo lường | Trực giác công thức | Khoảng giá trị | Kịch bản áp dụng |
|----------------------|--------------------|----------------|------------------|
| Cosine Similarity    | Xem hướng, bỏ qua độ dài | [-1, 1]        | Tìm kiếm ngữ nghĩa văn bản, hệ thống gợi ý |
| Euclidean Distance   | Xem khoảng cách đường thẳng giữa các điểm cuối | [0, ∞)         | Đặc trưng hình ảnh, phân tích cụm |
| Dot Product          | Hướng × Độ dài     | (-∞, +∞)       | Tính toán nhanh cho vector đã được chuẩn hóa |
| Manhattan Distance   | Khoảng cách di chuyển dọc theo các trục tọa độ | [0, ∞)         | Vector thưa thớt chiều cao |

---

## 3. Lập chỉ mục vector: Truy vấn hàng triệu vector trong mili giây như thế nào?

Giả sử bạn có 1 triệu tài liệu, mỗi tài liệu đã được chuyển thành vector 1536 chiều. Người dùng đặt một câu hỏi, bạn cần tìm 10 tài liệu tương tự nhất. Phương pháp trực tiếp nhất là tính toán độ tương đồng từng cái một – nhưng điều này có nghĩa là phải thực hiện 1 triệu phép toán vector 1536 chiều, quá chậm.

Đây chính là vấn đề mà **lập chỉ mục vector** cần giải quyết: **đánh đổi không gian lấy thời gian, thông qua tiền xử lý để xây dựng cấu trúc chỉ mục, giúp tốc độ truy vấn giảm từ O(n) xuống xấp xỉ O(log n)**.

<VectorIndexDemo />

::: tip Tìm kiếm vét cạn vs. Approximate Nearest Neighbor (ANN)
-   **Tìm kiếm vét cạn (Flat)**: So sánh từng cái một, độ chính xác 100% nhưng tốc độ chậm. Phù hợp với dữ liệu nhỏ (< 100 nghìn).
-   **IVF (Inverted File Index)**: Đầu tiên chia không gian vector thành nhiều vùng (phân cụm), khi truy vấn chỉ tìm kiếm trong vài vùng gần nhất. Giống như chia thư viện theo chủ đề, khi tìm sách chỉ đến khu vực liên quan.
-   **HNSW (Hierarchical Navigable Small World Graph)**: Xây dựng cấu trúc đồ thị đa lớp, điều hướng từng lớp từ thô đến mịn. Giống như trước tiên xem bản đồ thế giới để định vị quốc gia, sau đó xem bản đồ cấp tỉnh, cuối cùng xem bản đồ đường phố.
-   **PQ (Product Quantization)**: Nén vector chiều cao thành mã ngắn, hy sinh một chút độ chính xác để tiết kiệm đáng kể bộ nhớ. Phù hợp với tập dữ liệu siêu lớn.
:::

| Loại chỉ mục | Tốc độ xây dựng | Tốc độ truy vấn | Tỷ lệ thu hồi | Chiếm dụng bộ nhớ | Quy mô áp dụng |
|--------------|-----------------|-----------------|---------------|-------------------|-----------------|
| Flat (vét cạn) | Không cần xây dựng | Chậm            | 100%          | Cao               | < 100 nghìn     |
| IVF          | Trung bình      | Nhanh           | 95%+          | Trung bình        | 100 nghìn~10 triệu |
| HNSW         | Chậm            | Rất nhanh       | 99%+          | Cao               | 100 nghìn~10 triệu |
| PQ           | Trung bình      | Nhanh           | 90%+          | Rất thấp          | > 10 triệu      |
| IVF-PQ       | Trung bình      | Nhanh           | 92%+          | Thấp              | > 100 triệu     |

---

## 4. Cơ sở dữ liệu vector: Công cụ lưu trữ chuyên biệt cho vector

Với các thuật toán vector và chỉ mục, bạn cần một nơi để lưu trữ và quản lý chúng. Các cơ sở dữ liệu truyền thống (MySQL, PostgreSQL) giỏi xử lý dữ liệu có cấu trúc, nhưng lại yếu trong việc tìm kiếm độ tương đồng của vector chiều cao. **Cơ sở dữ liệu vector** được thiết kế đặc biệt cho kịch bản này.

<VectorDatabaseDemo />

::: tip Khả năng cốt lõi của cơ sở dữ liệu vector
1.  **Lưu trữ hiệu quả**: Định dạng lưu trữ được tối ưu hóa cho vector dấu phẩy động chiều cao
2.  **Truy vấn ANN**: Tích hợp nhiều thuật toán chỉ mục Approximate Nearest Neighbor (HNSW, IVF, v.v.)
3.  **Lọc siêu dữ liệu**: Hỗ trợ lọc đồng thời theo nhãn, thời gian và các điều kiện khác trong khi tìm kiếm vector
4.  **Cập nhật thời gian thực**: Hỗ trợ thêm, xóa, sửa vector động, không cần xây dựng lại toàn bộ chỉ mục
5.  **Mở rộng theo chiều ngang**: Kiến trúc phân tán hỗ trợ quy mô hàng tỷ vector
:::

| Cơ sở dữ liệu | Loại           | Đặc điểm           | Kịch bản áp dụng |
|---------------|----------------|--------------------|------------------|
| Pinecone      | Dịch vụ đám mây được quản lý hoàn toàn | Không cần vận hành, sẵn sàng sử dụng | Tạo mẫu nhanh, sản xuất quy mô vừa và nhỏ |
| Milvus        | Phân tán mã nguồn mở | Hiệu suất cao, có thể mở rộng | Môi trường sản xuất quy mô lớn |
| Chroma        | Mã nguồn mở nhẹ | Nhúng, API đơn giản | Phát triển cục bộ, dự án nhỏ |
| Weaviate      | Mã nguồn mở Cloud-native | Tích hợp vector hóa, GraphQL | Kịch bản cần vector hóa tự động |
| Qdrant        | Mã nguồn mở hiệu suất cao | Triển khai bằng Rust, lọc mạnh mẽ | Kịch bản cần lọc phức tạp |
| pgvector      | Tiện ích mở rộng của PG | Tái sử dụng cơ sở hạ tầng PG hiện có | Các nhóm đã có PostgreSQL |

---

## 5. Pipeline đầu cuối: Quy trình hoàn chỉnh từ văn bản đến truy vấn

Sau khi hiểu các thành phần, hãy kết nối chúng lại để xem một hệ thống truy vấn vector hoàn chỉnh hoạt động như thế nào.

Toàn bộ quy trình được chia thành hai luồng: **ghi ngoại tuyến** (biến tài liệu thành vector và lưu trữ) và **truy vấn trực tuyến** (biến câu hỏi thành vector và tìm kiếm).

<EmbeddingPipelineDemo />

::: tip Quy trình ghi ngoại tuyến
1.  **Tải tài liệu**: Đọc văn bản gốc từ nhiều nguồn khác nhau (PDF, trang web, cơ sở dữ liệu)
2.  **Tiền xử lý văn bản**: Làm sạch, loại bỏ nhiễu, chuẩn hóa (loại bỏ thẻ HTML, ký tự đặc biệt, v.v.)
3.  **Phân đoạn văn bản**: Chia văn bản dài thành các đoạn có kích thước phù hợp theo chiến lược (200~500 tokens)
4.  **Vector hóa**: Gọi mô hình Embedding (như OpenAI text-embedding-3-small) để chuyển mỗi đoạn thành vector
5.  **Lưu vào cơ sở dữ liệu vector**: Ghi vector cùng với văn bản gốc và siêu dữ liệu vào cơ sở dữ liệu
:::

::: tip Quy trình truy vấn trực tuyến
1.  **Tiếp nhận truy vấn**: Người dùng nhập câu hỏi bằng ngôn ngữ tự nhiên
2.  **Vector hóa truy vấn**: Sử dụng cùng một mô hình Embedding để chuyển câu hỏi thành vector
3.  **Truy vấn độ tương đồng**: Tìm kiếm Top-K đoạn tài liệu tương tự nhất trong cơ sở dữ liệu vector
4.  **Hậu xử lý**: Sắp xếp lại, loại bỏ trùng lặp, lọc siêu dữ liệu
5.  **Trả về kết quả**: Trả về các đoạn tài liệu liên quan nhất cho bên gọi (hoặc chuyển cho LLM để tạo câu trả lời)
:::

| Giai đoạn | Lựa chọn quan trọng | Giải pháp đề xuất |
|-----------|--------------------|-------------------|
| Mô hình Embedding | Độ chính xác vs. Chi phí vs. Tốc độ | OpenAI text-embedding-3-small (hiệu suất/chi phí tốt) |
| Chiến lược phân đoạn | Độ chi tiết vs. Tính toàn vẹn ngữ nghĩa | Phân đoạn đệ quy, 200~500 tokens |
| Cơ sở dữ liệu vector | Quy mô vs. Chi phí vận hành | Dự án nhỏ dùng Chroma, sản xuất dùng Pinecone/Milvus |
| Đo lường độ tương đồng | Ngữ nghĩa vs. Chính xác | Cosine Similarity (lựa chọn hàng đầu cho kịch bản văn bản) |
| Giá trị Top-K | Tỷ lệ thu hồi vs. Nhiễu | Đầu tiên truy vấn 20 mục, sau khi sắp xếp lại lấy Top 5 |

---

## Tóm tắt

Embedding và truy vấn vector là cầu nối giữa "ngôn ngữ con người" và "sự hiểu biết của máy móc", đồng thời là cơ sở hạ tầng cho các ứng dụng AI như RAG, tìm kiếm ngữ nghĩa, hệ thống gợi ý.

Ôn lại các điểm chính của chương này:

1.  **Bản chất của Embedding**: Ánh xạ văn bản vào không gian vector chiều cao, biến độ tương đồng ngữ nghĩa thành khoảng cách không gian
2.  **Đo lường độ tương đồng**: Cosine Similarity tập trung vào hướng (phù hợp với văn bản), Euclidean Distance tập trung vào khoảng cách tuyệt đối
3.  **Chỉ mục là chìa khóa hiệu suất**: HNSW và IVF giúp truy vấn hàng triệu vector trong mili giây
4.  **Lựa chọn cơ sở dữ liệu vector**: Dự án nhỏ dùng Chroma/pgvector, môi trường sản xuất dùng Pinecone/Milvus
5.  **Tư duy đầu cuối**: Từ tải tài liệu đến truy vấn cuối cùng, lựa chọn ở mỗi giai đoạn đều ảnh hưởng đến kết quả cuối cùng

## Đọc thêm

-   [Tài liệu OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) - Hướng dẫn sử dụng mô hình Embedding chính thức
-   [Trung tâm học tập Pinecone](https://www.pinecone.io/learn/) - Hướng dẫn hệ thống về cơ sở dữ liệu vector và truy vấn
-   [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki) - Tài liệu thư viện truy vấn vector mã nguồn mở của Facebook
-   [Bài báo gốc Word2Vec](https://arxiv.org/abs/1301.3781) - Tác phẩm mở đầu kỷ nguyên Embedding
-   [Bảng xếp hạng MTEB](https://huggingface.co/spaces/mteb/leaderboard) - Bảng so sánh hiệu suất mô hình Embedding
