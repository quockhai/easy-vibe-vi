# Tinh chỉnh và Triển khai Mô hình

::: tip Lời nói đầu
**Các mô hình lớn rất mạnh, nhưng chúng không hiểu nghiệp vụ của bạn.** GPT-4 có thể làm thơ, có thể lập trình, nhưng nó không biết các thuật ngữ sản phẩm của công ty bạn, không hiểu các quy tắc chuyên môn trong ngành của bạn. Tinh chỉnh (Fine-tuning) là quá trình giúp các mô hình lớn tổng quát "học" kiến thức chuyên môn của bạn – giống như đào tạo trước khi nhận việc cho một người đa tài uyên bác, để biến họ thành chuyên gia trong lĩnh vực của bạn.
:::

**Bài viết này sẽ giúp bạn học được gì?**

Sau khi hoàn thành chương này, bạn sẽ đạt được:

-   **Nhận thức quy trình**: Nắm vững quy trình tinh chỉnh hoàn chỉnh từ chuẩn bị dữ liệu đến triển khai mô hình
-   **Kỹ thuật dữ liệu**: Hiểu các yêu cầu về định dạng và tiêu chuẩn chất lượng của dữ liệu tinh chỉnh
-   **Tinh chỉnh hiệu quả**: Hiểu nguyên lý và lợi ích của các kỹ thuật tinh chỉnh hiệu quả về tham số như LoRA
-   **Nén mô hình**: Nắm vững cách kỹ thuật lượng tử hóa giúp các mô hình lớn chạy trên phần cứng tiêu dùng
-   **Thực hành triển khai**: Hiểu các kiến trúc dịch vụ mô hình phổ biến và chiến lược lựa chọn

| Chương | Nội dung | Khái niệm cốt lõi |
|-------|----------|------------------|
| **Chương 1** | Quy trình tinh chỉnh | Dữ liệu → Huấn luyện → Đánh giá → Triển khai |
| **Chương 2** | Dữ liệu huấn luyện | Định dạng dữ liệu, kiểm soát chất lượng |
| **Chương 3** | Tinh chỉnh LoRA | Thích ứng hạng thấp, hiệu quả tham số |
| **Chương 4** | Lượng tử hóa mô hình | FP16, INT8, INT4 |
| **Chương 5** | Triển khai mô hình | Dịch vụ suy luận, API Gateway |

---

## 0. Tổng quan: Tại sao cần tinh chỉnh?

Huấn luyện các mô hình ngôn ngữ lớn được chia thành hai giai đoạn: **tiền huấn luyện** và **tinh chỉnh**. Tiền huấn luyện là học khả năng ngôn ngữ trên lượng lớn dữ liệu tổng quát, còn tinh chỉnh là học khả năng chuyên môn trên dữ liệu của một tác vụ cụ thể.

Ví dụ: Tiền huấn luyện giống như đi học đại học – học kiến thức tổng quát, biết một chút về mọi thứ; tinh chỉnh giống như đào tạo trước khi nhận việc – học các kỹ năng chuyên môn cho một vị trí cụ thể.

::: tip Khi nào cần tinh chỉnh?
-   **Định dạng đầu ra cụ thể**: Cần mô hình luôn xuất ra định dạng JSON cố định
-   **Kiến thức chuyên ngành**: Các thuật ngữ và quy tắc chuyên môn trong lĩnh vực y tế, pháp luật, tài chính
-   **Chuyển đổi phong cách ngôn ngữ**: Giúp mô hình trả lời bằng giọng điệu, phong cách cụ thể (ví dụ: lời thoại của nhân viên chăm sóc khách hàng)
-   **Hỗ trợ ngôn ngữ ít phổ biến**: Nâng cao hiệu suất của mô hình trên các ngôn ngữ cụ thể
-   **Tối ưu chi phí**: Sử dụng mô hình nhỏ được tinh chỉnh thay vì gọi mô hình lớn, giảm chi phí suy luận
:::

---

## 1. Quy trình tinh chỉnh: Hành trình hoàn chỉnh từ dữ liệu đến triển khai

Tinh chỉnh không phải là "chỉ cần đưa dữ liệu cho mô hình là xong". Đó là một quy trình kỹ thuật nghiêm ngặt, mỗi khâu đều ảnh hưởng đến kết quả cuối cùng.

<FinetuningPipelineDemo />

::: tip Năm giai đoạn của tinh chỉnh
1.  **Chuẩn bị dữ liệu**: Thu thập, làm sạch, gán nhãn dữ liệu huấn luyện, đây là khâu tốn thời gian và quan trọng nhất
2.  **Lựa chọn mô hình**: Chọn mô hình nền tảng (Base Model) phù hợp, như Llama 3, Qwen, Mistral
3.  **Cấu hình huấn luyện**: Thiết lập các siêu tham số như learning rate, batch size, số epoch
4.  **Thực thi huấn luyện**: Chạy huấn luyện trên GPU, theo dõi đường cong loss và các chỉ số đánh giá
5.  **Đánh giá và triển khai**: Đánh giá hiệu quả trên tập kiểm thử, sau khi đạt yêu cầu sẽ triển khai thành dịch vụ API
:::

| Giai đoạn | Hành động chính | Cạm bẫy thường gặp |
|-----------|-----------------|--------------------|
| Chuẩn bị dữ liệu | Làm sạch, loại bỏ trùng lặp, định dạng | Chất lượng dữ liệu kém khiến mô hình "học sai" |
| Lựa chọn mô hình | Đánh giá khả năng của mô hình nền tảng | Mô hình quá lớn không thể huấn luyện, quá nhỏ thì hiệu quả kém |
| Cấu hình huấn luyện | Điều chỉnh siêu tham số | Learning rate quá cao dẫn đến quên lãng thảm khốc |
| Thực thi huấn luyện | Theo dõi loss và các chỉ số | Overfitting, huấn luyện không hội tụ |
| Đánh giá và triển khai | A/B testing, triển khai theo giai đoạn (gray release) | Rò rỉ tập kiểm thử dẫn đến đánh giá quá cao |

---

## 2. Dữ liệu huấn luyện: Giới hạn trên của hiệu quả tinh chỉnh

Trong tinh chỉnh có một câu nói cũ: **"Garbage in, garbage out"** (Rác vào, rác ra). Chất lượng dữ liệu huấn luyện trực tiếp quyết định giới hạn trên của hiệu quả tinh chỉnh. Hiệu quả của 100 mẫu dữ liệu chất lượng cao thường tốt hơn 10000 mẫu dữ liệu chất lượng thấp.

<TrainingDataDemo />

::: tip Ba định dạng phổ biến của dữ liệu tinh chỉnh
1.  **Định dạng hướng dẫn (Instruction)**: Định dạng được sử dụng phổ biến nhất, bao gồm ba trường: instruction (hướng dẫn), input (đầu vào), output (đầu ra mong muốn). Phù hợp để huấn luyện mô hình tuân thủ hướng dẫn.
2.  **Định dạng hội thoại (Chat)**: Dạng hội thoại nhiều lượt, bao gồm danh sách tin nhắn của các vai trò system, user, assistant. Phù hợp để huấn luyện chatbot.
3.  **Định dạng hoàn thành (Completion)**: Cặp prompt-completion đơn giản, phù hợp cho các kịch bản tạo văn bản, hoàn thành mã.
:::

| Khía cạnh chất lượng dữ liệu | Mô tả | Phương pháp kiểm tra |
|-----------------------------|-------|----------------------|
| Độ chính xác | Câu trả lời phải chính xác | Kiểm tra thủ công, xác minh bởi chuyên gia |
| Tính nhất quán | Phong cách trả lời cho các câu hỏi tương tự phải nhất quán | Kiểm tra so sánh mẫu |
| Tính đa dạng | Bao phủ đủ các kịch bản và biến thể | Thống kê phân bố loại câu hỏi |
| Loại bỏ trùng lặp | Tránh các mẫu trùng lặp dẫn đến overfitting | Loại bỏ trùng lặp văn bản, loại bỏ trùng lặp ngữ nghĩa |
| Lượng dữ liệu | Thường 500~5000 mẫu dữ liệu chất lượng cao là đủ | Bắt đầu với số lượng nhỏ, tăng dần |

---

## 3. LoRA: Đạt 90% hiệu quả với 1% tham số

Tinh chỉnh toàn bộ (Full Fine-tuning) yêu cầu cập nhật tất cả các tham số của mô hình – đối với một mô hình có 70B tham số, điều này có nghĩa là cần hàng trăm GB VRAM và lượng lớn sức mạnh tính toán của GPU. Đối với hầu hết các nhóm, điều này là không thực tế.

LoRA (Low-Rank Adaptation) cung cấp một giải pháp thanh lịch: **đóng băng các tham số mô hình gốc và chỉ huấn luyện một nhóm nhỏ các ma trận hạng thấp mới được thêm vào**. Lượng tham số của các ma trận này thường chỉ chiếm 0.1%~1% so với mô hình gốc, nhưng có thể đạt được hiệu quả gần bằng tinh chỉnh toàn bộ.

<LoRADemo />

::: tip Ý tưởng cốt lõi của LoRA
Ma trận trọng số W của mô hình gốc là một ma trận khổng lồ (ví dụ: 4096×4096). LoRA không trực tiếp sửa đổi W, mà thêm một "đường vòng" bên cạnh: W' = W + BA, trong đó B và A là hai ma trận nhỏ (ví dụ: 4096×8 và 8×4096). Khi huấn luyện chỉ cập nhật B và A, W gốc vẫn giữ nguyên.
-   **Hạng (Rank)**: Giá trị r càng lớn, khả năng biểu đạt càng mạnh, nhưng lượng tham số cũng càng nhiều. Thường r=8~64 là đủ dùng
-   **Triển khai hợp nhất**: Sau khi huấn luyện xong, có thể hợp nhất BA trở lại W, không tốn thêm chi phí khi suy luận
:::

| Phương pháp tinh chỉnh | Tham số có thể huấn luyện | Yêu cầu VRAM | Tốc độ huấn luyện | Hiệu quả |
|------------------------|--------------------------|---------------|-------------------|----------|
| Tinh chỉnh toàn bộ | 100% | Rất cao | Chậm | Tốt nhất |
| LoRA | 0.1%~1% | Thấp | Nhanh | Gần bằng toàn bộ |
| QLoRA | 0.1%~1% | Thấp hơn | Trung bình | Hơi thấp hơn LoRA |
| Prompt Tuning | < 0.01% | Rất thấp | Rất nhanh | Hạn chế |

---

## 4. Lượng tử hóa mô hình: Giúp mô hình lớn "giảm cân"

Một mô hình 70B tham số, nếu lưu trữ bằng FP32 (số dấu phẩy động 32 bit), sẽ cần 280GB VRAM – không có vài chiếc GPU hàng đầu thì không thể chạy được. Kỹ thuật lượng tử hóa (Quantization) nén kích thước mô hình bằng cách giảm độ chính xác số học, cho phép các mô hình lớn chạy trên phần cứng tiêu dùng.

<ModelQuantizationDemo />

::: tip Sự đánh đổi cốt lõi của lượng tử hóa
Lượng tử hóa về bản chất là sự đánh đổi **độ chính xác lấy không gian**. FP32 → FP16 gần như không mất mát, INT8 có mất mát nhẹ, INT4 sẽ có sự suy giảm chất lượng rõ rệt nhưng thường có thể chấp nhận được. Điều quan trọng là tìm ra điểm cân bằng tốt nhất cho trường hợp của bạn.
-   **FP16 (bán chính xác)**: Kích thước giảm một nửa, chất lượng gần như không mất mát, là lựa chọn mặc định cho huấn luyện và suy luận
-   **INT8 (số nguyên 8 bit)**: Kích thước giảm thêm một nửa, mất mát chất lượng rất nhỏ, phù hợp cho hầu hết các kịch bản suy luận
-   **INT4 (số nguyên 4 bit)**: Kích thước chỉ bằng 1/8 của FP32, có mất mát chất lượng nhất định, phù hợp cho các kịch bản tài nguyên hạn chế
:::

| Độ chính xác | Byte mỗi tham số | Kích thước mô hình 70B | Mất mát chất lượng | Trường hợp áp dụng |
|--------------|-------------------|------------------------|--------------------|--------------------|
| FP32 | 4 byte | ~280 GB | Không | Tiêu chuẩn huấn luyện |
| FP16 | 2 byte | ~140 GB | Gần như không | Huấn luyện và suy luận tiêu chuẩn |
| INT8 | 1 byte | ~70 GB | Rất nhỏ | Suy luận sản xuất |
| INT4 | 0.5 byte | ~35 GB | Có thể chấp nhận | Thiết bị biên, triển khai cục bộ |

---

## 5. Triển khai mô hình: Từ phòng thí nghiệm đến môi trường sản xuất

Mô hình đã được huấn luyện, đã được lượng tử hóa và nén, bước cuối cùng là triển khai nó thành một dịch vụ có thể gọi được. Triển khai mô hình không chỉ là "chạy mô hình", mà còn liên quan đến các vấn đề kỹ thuật như xử lý đồng thời, cân bằng tải, kiểm soát chi phí.

<ModelServingDemo />

::: tip Ba giải pháp triển khai phổ biến
1.  **Nhà cung cấp dịch vụ API**: Trực tiếp sử dụng API của các nhà cung cấp như OpenAI, Anthropic. Không cần vận hành, tính phí theo token, phù hợp cho việc xác minh nhanh và sử dụng quy mô vừa và nhỏ.
2.  **Dịch vụ suy luận tự host**: Sử dụng các framework như vLLM, TGI để triển khai trên máy chủ GPU của riêng bạn. Chi phí có thể kiểm soát, dữ liệu không rời khỏi miền, phù hợp cho các kịch bản có yêu cầu về quyền riêng tư hoặc gọi API quy mô lớn.
3.  **Suy luận Serverless**: Sử dụng các nền tảng như AWS SageMaker, Replicate, tính phí theo yêu cầu, tự động mở rộng/thu hẹp. Phù hợp cho các kịch bản có lưu lượng truy cập biến động lớn.
:::

| Giải pháp triển khai | Mô hình chi phí | Độ trễ | Độ phức tạp vận hành | Trường hợp áp dụng |
|----------------------|-----------------|--------|---------------------|--------------------|
| Nhà cung cấp dịch vụ API | Tính phí theo token | Trung bình | Không | Tạo mẫu nhanh, quy mô vừa và nhỏ |
| vLLM tự triển khai | Chi phí thuê GPU | Thấp | Cao | Quy mô lớn, nhạy cảm về quyền riêng tư |
| Serverless | Tính phí theo yêu cầu | Khởi động nguội cao | Thấp | Lưu lượng truy cập biến động lớn |
| Triển khai biên | Đầu tư phần cứng một lần | Rất thấp | Trung bình | Trường hợp ngoại tuyến, IoT |

---

## Tóm tắt

Tinh chỉnh và triển khai mô hình là các khâu then chốt giúp biến các mô hình lớn từ "công cụ tổng quát" thành "trợ lý chuyên nghiệp". Từ chuẩn bị dữ liệu đến triển khai mô hình, mỗi bước đều đòi hỏi tư duy và thực hành kỹ thuật.

Điểm chính của chương này:

1.  **Tinh chỉnh là đào tạo trước khi nhận việc**: Giúp mô hình tổng quát học kiến thức và hành vi của một lĩnh vực cụ thể
2.  **Chất lượng dữ liệu quyết định giới hạn trên**: 100 mẫu dữ liệu chất lượng cao tốt hơn 10000 mẫu dữ liệu chất lượng thấp
3.  **LoRA là vua hiệu quả**: Đạt được hiệu quả gần bằng tinh chỉnh toàn bộ với chưa đến 1% tham số
4.  **Lượng tử hóa là công cụ triển khai hữu hiệu**: Lượng tử hóa INT4 giúp mô hình 70B chạy trên một card đồ họa duy nhất
5.  **Giải pháp triển khai tùy thuộc vào tình hình thực tế**: Xác minh nhanh dùng API, quy mô lớn dùng tự triển khai, lưu lượng biến động dùng Serverless

## Đọc thêm

-   [Hugging Face PEFT 文档](https://huggingface.co/docs/peft) - Tài liệu chính thức của thư viện tinh chỉnh hiệu quả tham số
-   [vLLM 文档](https://docs.vllm.ai/) - Công cụ suy luận LLM hiệu suất cao
-   [Unsloth](https://github.com/unslothai/unsloth) - Framework tinh chỉnh LoRA tăng tốc 2 lần
-   [GGUF 格式说明](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md) - Định dạng mô hình lượng tử hóa được sử dụng bởi llama.cpp
-   [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning) - Hướng dẫn tinh chỉnh chính thức của OpenAI
