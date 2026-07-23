---
title: 'Transformer và cơ chế Attention: Động cơ cốt lõi của các mô hình lớn'
description: 'Đi sâu vào kiến trúc Transformer và cơ chế Attention, khám phá nền tảng công nghệ của các mô hình lớn như GPT, BERT.'
---

# Transformer và cơ chế Attention: Động cơ cốt lõi của các mô hình lớn

Năm 2017, kiến trúc Transformer được Google giới thiệu trong bài báo 《Attention Is All You Need》 đã thay đổi hoàn toàn cuộc chơi trong lĩnh vực xử lý ngôn ngữ tự nhiên. Nó loại bỏ mạng nơ-ron hồi quy (RNN) truyền thống, chỉ dựa vào cơ chế Attention để đạt được hiệu suất mạnh mẽ hơn và hiệu quả đào tạo cao hơn. Ngày nay, hầu hết các mô hình ngôn ngữ lớn – GPT, BERT, T5, LLaMA – đều được xây dựng trên nền tảng Transformer.

<TransformerQuickStartDemo />

---

## I. Những hạn chế của RNN và đột phá của Transformer

Trước khi Transformer xuất hiện, phương pháp chủ đạo để xử lý dữ liệu chuỗi (như văn bản, giọng nói) là mạng nơ-ron hồi quy (RNN) và các biến thể của nó như LSTM, GRU. Các mô hình này xử lý từng phần tử trong chuỗi thông qua cấu trúc lặp, đồng thời duy trì một trạng thái ẩn để ghi nhớ thông tin lịch sử.

### 1.1 Ba nhược điểm chí mạng của RNN

**Phụ thuộc tuần tự, không thể song song hóa**: RNN phải chờ bước thời gian trước đó hoàn thành tính toán mới có thể xử lý từ tiếp theo. Điều này dẫn đến tốc độ đào tạo cực kỳ chậm, không thể tận dụng tối đa khả năng tính toán song song của các GPU hiện đại.

**Suy giảm phụ thuộc tầm xa**: Ngay cả LSTM đã được cải tiến, khi xử lý văn bản dài, thông tin ban đầu cũng sẽ dần bị "lãng quên". Ví dụ, trong một bài viết 500 từ, mô hình khó có thể nhớ thông tin quan trọng được đề cập ở đầu bài.

**Gradient biến mất/bùng nổ**: Trong quá trình lan truyền ngược, gradient cần được truyền từng lớp theo các bước thời gian, dễ xảy ra hiện tượng gradient biến mất hoặc bùng nổ, dẫn đến đào tạo không ổn định.

### 1.2 Đột phá mang tính cách mạng của Transformer

Transformer, thông qua **cơ chế Self-Attention**, cho phép mô hình "nhìn thấy toàn bộ" chuỗi cùng lúc, trực tiếp tính toán mối quan hệ giữa hai vị trí bất kỳ mà không cần truyền thông tin từng bước.

<RnnVsTransformerDemo />

::: tip Ưu điểm cốt lõi của Transformer
- **Tính toán song song**: Attention của tất cả các vị trí có thể được tính toán đồng thời, tốc độ đào tạo tăng lên hàng chục lần.
- **Tầm nhìn toàn cục**: Trực tiếp nắm bắt các phụ thuộc tầm xa, không bị giới hạn bởi độ dài chuỗi.
- **Khả năng mở rộng**: Kiến trúc đơn giản, thống nhất, dễ dàng xếp chồng các mạng sâu hơn.
:::

---

## II. Kiến trúc Transformer hoàn chỉnh: Từ tổng thể đến chi tiết

Kiến trúc hoàn chỉnh của Transformer bao gồm hai phần: **Encoder** và **Decoder**, lần lượt chịu trách nhiệm hiểu đầu vào và tạo ra đầu ra.

<TransformerArchitectureDemo />

### 2.1 Encoder

Lấy ví dụ câu "银行账户里的余额不足" (Số dư trong tài khoản ngân hàng không đủ). Khi mô hình xử lý từ "余额" (số dư), nó sẽ tự động tính toán mức độ liên quan với các từ khác:

- "余额" (số dư) có liên quan cao với "账户" (tài khoản) (0.35)
- "余额" (số dư) có liên quan trung bình với "银行" (ngân hàng) (0.20)
- "余额" (số dư) có liên quan thấp với các từ hư từ như "的" (của), "里" (trong) (0.05-0.10)

Mối liên quan này không phải do con người quy định, mà là do mô hình tự động học được thông qua lượng lớn dữ liệu.

<SelfAttentionDemo />

### 2.2 Quá trình tính toán Attention

Cơ chế Self-Attention được thực hiện thông qua ba bước chính:

1.  **Tạo vector Q, K, V**: Mỗi từ thông qua ba phép biến đổi tuyến tính khác nhau, tạo ra ba vector Query, Key và Value.
2.  **Tính toán trọng số Attention**: Sử dụng Query nhân vô hướng (dot product) với tất cả các Key để có được điểm số tương đồng.
3.  **Tổng có trọng số**: Sử dụng trọng số Attention để tổng có trọng số các vector Value, thu được đầu ra cuối cùng.

---

## III. Query, Key, Value: Ba "kiếm khách" của Attention

Cơ chế Attention của Transformer đã học hỏi ý tưởng từ việc truy xuất thông tin, ánh xạ mỗi từ vào ba không gian vector khác nhau.

### 3.1 Vai trò của ba vector

**Query**: Đại diện cho "tôi muốn tìm gì". Ý định truy vấn của từ hiện tại, dùng để khớp với Key của các từ khác.

**Key**: Đại diện cho "tôi là gì". Định danh đặc trưng của mỗi từ, dùng để được Query truy xuất.

**Value**: Đại diện cho "nội dung của tôi là gì". Thông tin thực tế cần truyền tải, được tổng có trọng số dựa trên trọng số Attention.

Điểm khéo léo của thiết kế này là: **tính toán độ tương đồng (Q·K) và truyền tải thông tin (V) được tách rời**. Mô hình có thể học được rằng "những từ nào nên được chú ý" và "sau khi chú ý nên trích xuất thông tin gì" là hai vấn đề độc lập.

<QKVMechanismDemo />

### 3.2 Công thức tính toán Attention

Công thức tính toán Attention đầy đủ là:

```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

Trong đó:
- `QK^T`: Tính tích vô hướng của Query và Key, thu được ma trận độ tương đồng.
- `√d_k`: Hệ số tỷ lệ, ngăn chặn giá trị tích vô hướng quá lớn dẫn đến gradient biến mất trong softmax.
- `softmax`: Chuyển đổi độ tương đồng thành phân phối xác suất (trọng số Attention).
- Cuối cùng nhân với `V`: Sử dụng trọng số Attention để tổng có trọng số các Value.

---

## IV. Multi-Head Attention: Hiểu ngữ nghĩa từ nhiều góc độ

Một Head Attention đơn lẻ chỉ có thể nắm bắt một loại mối quan hệ phụ thuộc. Để mô hình hiểu câu từ nhiều góc độ, Transformer đã giới thiệu **Multi-Head Attention**.

### 4.1 Cơ chế hoạt động của Multi-Head

Multi-Head Attention chiếu đầu vào vào nhiều không gian con khác nhau, mỗi "head" độc lập tính toán Attention, sau đó nối tất cả các đầu ra của các head lại với nhau.

Transformer điển hình sử dụng 8 hoặc 16 Head Attention, mỗi head có thể tập trung vào các hiện tượng ngôn ngữ khác nhau:

- **Head ngữ pháp**: Nhận diện các mối quan hệ ngữ pháp như chủ ngữ-vị ngữ-tân ngữ, định ngữ-trạng ngữ-bổ ngữ.
- **Head ngữ nghĩa**: Nắm bắt mối liên quan về nghĩa của từ (ví dụ: "ngân hàng" và "tài khoản").
- **Head vị trí**: Chú ý đến các phụ thuộc cục bộ của các từ liền kề.
- **Head tham chiếu**: Phân tích sự chỉ định của đại từ (ví dụ: "anh ấy" chỉ "Tiểu Minh").
- **Head cảm xúc**: Nhận diện sắc thái khen chê và xu hướng cảm xúc.
- **Head thực thể**: Nhận diện các thực thể được đặt tên như tên người, địa danh.

<MultiHeadAttentionDemo />

### 4.2 Ưu điểm của Multi-Head

**Khả năng biểu đạt mạnh mẽ hơn**: Các head khác nhau có thể nắm bắt các loại mối quan hệ phụ thuộc khác nhau, tránh giới hạn của một góc nhìn đơn lẻ.

**Tính toán song song**: Nhiều head có thể tính toán đồng thời mà không làm tăng thời gian tính toán.

**Độ bền tốt hơn**: Ngay cả khi một số head học thất bại, các head khác vẫn có thể cung cấp thông tin hiệu quả.

::: tip Biểu diễn toán học của Multi-Head Attention
```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
其中 head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```
Mỗi head có các ma trận trọng số độc lập W^Q, W^K, W^V, cuối cùng thông qua W^O để kết hợp đầu ra của tất cả các head.
:::

---

## V. Kiến trúc Transformer hoàn chỉnh: Encoder và Decoder

Kiến trúc hoàn chỉnh của Transformer bao gồm hai phần: **Encoder** và **Decoder**, lần lượt chịu trách nhiệm hiểu đầu vào và tạo ra đầu ra.

### 5.1 Encoder

Encoder được tạo thành từ nhiều lớp (thường 6-12 lớp) có cấu trúc giống nhau được xếp chồng lên nhau, mỗi lớp bao gồm hai lớp con:

1.  **Lớp Multi-Head Self-Attention**: Nắm bắt các mối quan hệ phụ thuộc bên trong chuỗi đầu vào.
2.  **Mạng nơ-ron truyền thẳng (Feed Forward)**: Thực hiện biến đổi phi tuyến tính độc lập cho từng vị trí.

Mỗi lớp con đều có **Residual Connection** và **Layer Normalization** theo sau, đảm bảo sự ổn định trong quá trình đào tạo các mạng sâu.

### 5.2 Decoder

Decoder cũng được xếp chồng bởi nhiều lớp, nhưng mỗi lớp có ba lớp con:

1.  **Masked Multi-Head Attention**: Chỉ có thể nhìn thấy các từ trước vị trí hiện tại, ngăn chặn việc "gian lận".
2.  **Cross-Attention**: Kết nối Encoder và Decoder, cho phép Decoder chú ý đến chuỗi đầu vào.
3.  **Mạng nơ-ron truyền thẳng**: Giống như Encoder.

<TransformerArchitectureDemo />

### 5.3 Các biến thể hiện đại: Chỉ Encoder so với Chỉ Decoder

Mặc dù Transformer gốc bao gồm cả Encoder và Decoder, nhưng các mô hình lớn hiện đại thường chỉ sử dụng một trong hai:

| Loại kiến trúc | Mô hình đại diện | Nhiệm vụ áp dụng |
| --- | --- | --- |
| **Chỉ Encoder** | BERT, RoBERTa | Phân loại văn bản, nhận diện thực thể có tên, hỏi đáp |
| **Chỉ Decoder** | GPT, LLaMA, Claude | Sinh văn bản, đối thoại, hoàn thành mã |
| **Encoder-Decoder** | T5, BART | Dịch thuật, tóm tắt, viết lại văn bản |

::: tip Tại sao GPT chỉ sử dụng Decoder?
Các mô hình dòng GPT sử dụng phương pháp **sinh tự hồi quy**, dự đoán từng từ tiếp theo. Kiến trúc chỉ Decoder tự nhiên phù hợp với nhiệm vụ tạo sinh này, và cấu trúc cũng đơn giản hơn, dễ dàng mở rộng lên quy mô hàng trăm tỷ tham số.
:::

---

## VI. Positional Encoding: Cho mô hình biết thứ tự từ

Cơ chế Self-Attention của Transformer bản thân nó là **không phụ thuộc vị trí** – nó coi câu như một tập hợp các từ mà không quan tâm đến thứ tự của chúng. Nhưng thứ tự từ lại cực kỳ quan trọng đối với ngữ nghĩa: "Tôi yêu bạn" và "Bạn yêu tôi" có ý nghĩa hoàn toàn khác nhau!

### 6.1 Sự cần thiết của Positional Encoding

Để mô hình nhận biết thông tin vị trí, Transformer thêm **Positional Encoding** vào phần nhúng đầu vào. Positional Encoding là một vector có cùng chiều với nhúng từ, được cộng trực tiếp vào nhúng từ.

<PositionalEncodingDemo />

### 6.2 Positional Encoding dạng hàm sin-cos

Transformer gốc sử dụng hàm sin-cos cố định để tạo Positional Encoding:

```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

Ưu điểm của thiết kế này:
- **Tính duy nhất**: Mỗi vị trí có một mã hóa duy nhất.
- **Vị trí tương đối**: Mô hình có thể học được mối quan hệ khoảng cách tương đối.
- **Khả năng ngoại suy**: Có thể xử lý các chuỗi dài hơn so với khi đào tạo.

### 6.3 Các phương pháp Positional Encoding hiện đại

Khi nghiên cứu đi sâu hơn, nhiều phương pháp Positional Encoding khác đã xuất hiện:

**Positional Encoding có thể học được**: BERT, GPT coi Positional Encoding là các tham số có thể huấn luyện, thay vì hàm cố định.

**Positional Encoding tương đối**: T5, DeBERTa không mã hóa vị trí tuyệt đối, mà mã hóa khoảng cách tương đối giữa các từ.

**Rotary Positional Encoding (RoPE)**: Phương pháp được LLaMA, GPT-NeoX sử dụng, thông qua việc xoay các vector Q và K để đưa thông tin vị trí vào, mang lại hiệu suất ngoại suy tốt hơn.

**ALiBi**: Đạt được nhận thức vị trí bằng cách thêm một số hạng thiên vị vào điểm Attention, không cần thêm tham số.

---

## VII. Ảnh hưởng và tương lai của Transformer

Sự xuất hiện của Transformer không chỉ là sự ra đời của một kiến trúc mới, mà còn là sự thay đổi mô hình nghiên cứu AI toàn diện.

### 7.1 Mô hình tiền đào tạo thống nhất

Transformer đã biến "tiền đào tạo + tinh chỉnh" thành quy trình tiêu chuẩn của NLP. Bằng cách tiền đào tạo trên lượng lớn văn bản không gắn nhãn, mô hình học được biểu diễn ngôn ngữ chung, sau đó chỉ cần một lượng nhỏ dữ liệu gắn nhãn là có thể thích ứng với các nhiệm vụ downstream khác nhau.

### 7.2 Kiến trúc đa phương thức chung

Thành công của Transformer không chỉ giới hạn ở văn bản. Nó đã được áp dụng thành công vào:

- **Thị giác máy tính**: Vision Transformer (ViT) vượt trội hơn CNN trong phân loại hình ảnh.
- **Nhận dạng giọng nói**: Whisper sử dụng Transformer để chuyển đổi giọng nói đa ngôn ngữ thành văn bản.
- **Dự đoán cấu trúc protein**: AlphaFold 2 sử dụng Transformer để dự đoán cấu trúc 3D của protein.
- **Học tăng cường**: Decision Transformer chuyển đổi vấn đề RL thành mô hình hóa chuỗi.

### 7.3 Nền tảng của kỷ nguyên mô hình lớn

Từ 175 tỷ tham số của GPT-3 đến hàng nghìn tỷ tham số của GPT-4, Transformer đã thể hiện khả năng mở rộng đáng kinh ngạc. Đặc tính tính toán song song của nó cho phép chúng ta đào tạo các mô hình khổng lồ chưa từng có, và quan sát thấy **khả năng nổi bật (Emergent Abilities)** – khi mô hình đủ lớn, nó tự động "ngộ" ra các khả năng như suy luận, viết mã, đa ngôn ngữ.

### 7.4 Thách thức và định hướng tương lai

Mặc dù Transformer đã đạt được thành công lớn, nhưng vẫn đối mặt với những thách thức:

**Độ phức tạp tính toán**: Độ phức tạp của Self-Attention là O(n²), khi xử lý văn bản dài, lượng tính toán rất lớn.

**Mô hình hóa văn bản dài**: Mặc dù về lý thuyết có thể xử lý độ dài tùy ý, nhưng thực tế bị giới hạn bởi bộ nhớ GPU và tài nguyên tính toán.

**Khả năng giải thích**: Mặc dù trọng số Attention cung cấp một mức độ giải thích nhất định, nhưng quá trình ra quyết định của các mạng sâu vẫn là một hộp đen.

Các hướng nghiên cứu hiện tại bao gồm:
- **Transformer hiệu quả**: Linformer, Performer, Flash Attention, v.v., giảm độ phức tạp.
- **Mô hình hóa ngữ cảnh dài**: Sparse Attention, Sliding Window, cơ chế Memory.
- **Kết hợp đa phương thức**: Kiến trúc đa phương thức gốc xử lý thống nhất văn bản, hình ảnh, âm thanh.

---

## VIII. Tóm tắt

Sự ra đời của Transformer và cơ chế Attention đánh dấu sự chuyển đổi hoàn toàn của học sâu từ "thiết kế đặc trưng thủ công" sang "học end-to-end". Nó không chỉ giải quyết các nút thắt kỹ thuật của RNN, mà quan trọng hơn, nó cung cấp một kiến trúc đơn giản, chung chung và có khả năng mở rộng, trở thành nền tảng của kỷ nguyên mô hình lớn.

Hiểu Transformer chính là hiểu cốt lõi của AI hiện đại. Từ mã hóa hai chiều của BERT, đến tạo sinh tự hồi quy của GPT, và biểu diễn thống nhất của các mô hình đa phương thức lớn, tất cả những đột phá này đều được xây dựng trên nền tảng của Transformer.

Trong tương lai, cùng với sự nâng cao về năng lực tính toán và tối ưu hóa thuật toán, Transformer sẽ tiếp tục phát triển, thúc đẩy AI tiến tới những hướng mạnh mẽ và phổ quát hơn.
