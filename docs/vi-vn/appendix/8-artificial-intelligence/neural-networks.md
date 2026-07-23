# Mạng Nơ-ron và Học Sâu

::: tip Lời nói đầu
**Mạng nơ-ron là động cơ của cuộc cách mạng AI.** Từ khả năng hiểu ngôn ngữ của ChatGPT đến nhận diện hình ảnh trong xe tự lái, mạng nơ-ron đều đang hoạt động phía sau. Nó không phải là phép thuật, mà là một khung toán học tinh xảo – thông qua lượng lớn dữ liệu để "học" ra mối quan hệ ánh xạ từ đầu vào đến đầu ra. Hiểu các nguyên lý cơ bản của nó sẽ giúp bạn sử dụng và gỡ lỗi các công cụ AI tốt hơn.
:::

**Bài viết này sẽ giúp bạn học được gì?**

Sau khi hoàn thành chương này, bạn sẽ đạt được:

-   **Khái niệm cốt lõi**: Hiểu các nguyên lý cơ bản của nơ-ron, lớp, lan truyền thuận, lan truyền ngược
-   **Các loại mạng**: Tìm hiểu đặc điểm và kịch bản ứng dụng của các kiến trúc chính như CNN, RNN, Transformer
-   **Quá trình huấn luyện**: Hiểu cách mô hình "học" từ dữ liệu
-   **Kỹ thuật quan trọng**: Nắm vững các khái niệm thực tiễn như overfitting, learning rate, regularization
-   **Lộ trình phát triển**: Tìm hiểu lịch sử tiến hóa từ Perceptron đến các Large Language Model

| Chương | Nội dung | Khái niệm cốt lõi |
|-------|----------|-------------------|
| **Chương 1** | Từ Nơ-ron đến Mạng | Perceptron, Activation Function, Lan truyền thuận |
| **Chương 2** | Mạng học như thế nào | Loss Function, Gradient Descent, Lan truyền ngược |
| **Chương 3** | Các kiến trúc mạng chính | CNN, RNN, Transformer |
| **Chương 4** | Nghệ thuật huấn luyện | Overfitting, Regularization, Tối ưu siêu tham số |
| **Chương 5** | Lịch sử phát triển và xu hướng tiên tiến | Từ Perceptron đến GPT |

---

## 1. Từ Nơ-ron đến Mạng

### Nơ-ron đơn lẻ

Đơn vị nhỏ nhất của mạng nơ-ron là **nơ-ron** (Neuron). Nó mô phỏng cách hoạt động của nơ-ron sinh học: nhận nhiều tín hiệu đầu vào, tổng hợp có trọng số, và tạo ra đầu ra thông qua activation function.

```
Đầu vào x1 ──→ ×w1 ──┐
Đầu vào x2 ──→ ×w2 ──┼──→ Σ(Tổng hợp có trọng số) + b(Bias) ──→ f(Activation Function) ──→ Đầu ra
Đầu vào x3 ──→ ×w3 ──┘
```

Biểu thức toán học: **y = f(w₁x₁ + w₂x₂ + w₃x₃ + b)**

<NeuronDemo />

### Activation Function: Tại sao cần phi tuyến tính?

Nếu không có activation function, dù có bao nhiêu lớp nơ-ron chồng lên nhau, kết quả cuối cùng vẫn tương đương với một phép biến đổi tuyến tính (phép nhân ma trận). Activation function giới thiệu **phi tuyến tính**, cho phép mạng học các mẫu phức tạp.

| Activation Function | Công thức | Đặc điểm | Kịch bản thường dùng |
|---------------------|-----------|----------|----------------------|
| ReLU                | max(0, x) | Đơn giản, hiệu quả, huấn luyện nhanh | Lựa chọn mặc định cho các hidden layer |
| Sigmoid             | 1/(1+e⁻ˣ) | Đầu ra 0~1 | Output layer cho phân loại nhị phân |
| Tanh                | (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ) | Đầu ra -1~1 | Thường dùng trong RNN |
| Softmax             | eˣᵢ/Σeˣⱼ  | Đầu ra phân phối xác suất | Output layer cho phân loại đa lớp |

### Từ Nơ-ron đến Mạng

Tổ chức nhiều nơ-ron thành các **lớp**, và nối nhiều lớp lại với nhau sẽ tạo thành mạng nơ-ron:

```
Input layer          Hidden layer 1        Hidden layer 2        Output layer
(Đặc trưng)         (Trích xuất đặc trưng cấp thấp)   (Trích xuất đặc trưng cấp cao)   (Kết quả dự đoán)

 x1 ──→  [○ ○ ○ ○] ──→ [○ ○ ○] ──→  [○ ○]
 x2 ──→  [○ ○ ○ ○] ──→ [○ ○ ○] ──→  Mèo/Chó
 x3 ──→  [○ ○ ○ ○] ──→ [○ ○ ○]
```

| Khái niệm | Giải thích |
|-----------|------------|
| Input layer | Nhận dữ liệu thô (pixel hình ảnh, vector văn bản, v.v.) |
| Hidden layer | Lớp xử lý trung gian, càng nhiều lớp thì mạng càng "sâu" (chữ "sâu" trong Deep Learning) |
| Output layer | Tạo ra dự đoán cuối cùng (xác suất phân loại, giá trị hồi quy, v.v.) |
| Lan truyền thuận | Quá trình dữ liệu chảy từ input layer qua từng lớp đến output layer |

::: tip Tại sao gọi là Deep Learning?
Machine Learning truyền thống thường chỉ có 1-2 lớp. Khi số lượng hidden layer tăng lên hàng chục hoặc thậm chí hàng trăm lớp, nó được gọi là Deep Learning. Mạng sâu hơn có thể học các đặc trưng trừu tượng hơn: lớp đầu tiên học cạnh, lớp thứ hai học texture, lớp thứ ba học các bộ phận, các lớp sâu hơn học được "đây là một con mèo".
:::

---

## 2. Mạng học như thế nào

Bản chất của việc "học" trong mạng nơ-ron là một **bài toán tối ưu hóa**: tìm một tập hợp các trọng số (w) và bias (b) sao cho dự đoán của mạng càng gần với câu trả lời thực tế càng tốt.

### Ba bước huấn luyện

```
1. Lan truyền thuận: Đưa dữ liệu vào, nhận kết quả dự đoán
2. Tính Loss: Sử dụng Loss Function để đo lường sự khác biệt giữa dự đoán và giá trị thực tế
3. Lan truyền ngược: Dựa trên Loss, tính gradient của từng trọng số, cập nhật trọng số
   ↓
Lặp lại các bước trên cho đến khi Loss đủ nhỏ
```

### Loss Function: Đo lường "mức độ sai lệch"

Loss Function định lượng sự khác biệt giữa giá trị dự đoán và giá trị thực tế. Mục tiêu của huấn luyện là tối thiểu hóa Loss.

| Loss Function | Mô tả công thức | Kịch bản áp dụng |
|---------------|-----------------|------------------|
| MSE (Mean Squared Error) | Giá trị trung bình của bình phương hiệu giữa giá trị dự đoán và giá trị thực tế | Bài toán hồi quy |
| Cross-Entropy | -Σ y·log(ŷ) | Bài toán phân loại |
| Binary Cross-Entropy | Phiên bản Cross-Entropy cho phân loại nhị phân | Bài toán phân loại nhị phân |

### Gradient Descent: Tìm điểm thấp nhất

Hãy tưởng tượng bạn đang đứng trên một ngọn núi, bị bịt mắt và phải đi đến điểm thấp nhất. Điều bạn có thể làm là **cảm nhận độ dốc dưới chân, sau đó đi một bước theo hướng dốc xuống**. Đây chính là Gradient Descent.

```
Giá trị Loss
  ↑
  │    ╱╲
  │   ╱  ╲      ← Vị trí hiện tại
  │  ╱    ╲    ↙ Đi xuống theo hướng gradient
  │ ╱      ╲╱   ← Cực tiểu cục bộ
  │╱            ╲╱  ← Cực tiểu toàn cục
  └──────────────→ Giá trị trọng số
```

| Khái niệm | Giải thích |
|-----------|------------|
| Gradient | Đạo hàm riêng của Loss Function đối với mỗi trọng số, chỉ ra "điều chỉnh theo hướng nào để giảm Loss" |
| Learning rate | Mỗi bước đi bao xa. Quá lớn sẽ bỏ qua điểm thấp nhất, quá nhỏ sẽ hội tụ chậm |
| Batch size | Số lượng mẫu dùng để tính gradient mỗi lần. Toàn bộ quá chậm, một mẫu quá dao động, mini-batch là sự thỏa hiệp |

### Lan truyền ngược: Chiến thắng của quy tắc chuỗi

Lan truyền ngược (Backpropagation) là một thuật toán hiệu quả để tính gradient. Nó sử dụng **quy tắc chuỗi** của vi tích phân, bắt đầu từ output layer, tính toán ngược từng lớp để xác định đóng góp của mỗi trọng số vào Loss.

```
Lan truyền thuận: Đầu vào → Hidden layer 1 → Hidden layer 2 → Đầu ra → Loss
Lan truyền ngược: Loss → Đầu ra → Hidden layer 2 → Hidden layer 1 → Cập nhật tất cả trọng số
```

::: tip Hiểu trực quan về Lan truyền ngược
Hãy tưởng tượng mạng nơ-ron như một dây chuyền sản xuất. Khi sản phẩm (dự đoán) gặp vấn đề (Loss lớn), bạn cần bắt đầu kiểm tra ngược từ công đoạn cuối cùng, xem mỗi công đoạn (trọng số của mỗi lớp) đã đóng góp bao nhiêu vào vấn đề cuối cùng, sau đó điều chỉnh theo mức độ đóng góp. Đóng góp lớn thì điều chỉnh nhiều, đóng góp nhỏ thì điều chỉnh ít.
:::

---

## 3. Các kiến trúc mạng chính

Các loại dữ liệu khác nhau yêu cầu các kiến trúc mạng khác nhau. Chọn đúng kiến trúc sẽ đạt hiệu quả gấp đôi.

<NetworkLayersDemo />

### 3.1 CNN (Mạng nơ-ron tích chập)

CNN là "ông vua" xử lý hình ảnh. Ý tưởng cốt lõi: sử dụng các kernel tích chập nhỏ trượt trên hình ảnh để trích xuất các đặc trưng cục bộ.

```
Hình ảnh đầu vào → [Lớp tích chập→Activation→Pooling] × N → Lớp Fully Connected → Đầu ra
  28×28      Trích xuất cạnh/texture/hình dạng        Kết quả phân loại
```

| Đặc điểm | Giải thích |
|----------|------------|
| Kết nối cục bộ | Mỗi nơ-ron chỉ nhìn một vùng nhỏ, chứ không phải toàn bộ hình ảnh |
| Chia sẻ tham số | Cùng một kernel tích chập được tái sử dụng trên toàn bộ hình ảnh, giảm đáng kể số lượng tham số |
| Bất biến dịch chuyển | Mèo ở bên trái hay bên phải hình ảnh đều có thể được nhận diện |
| Đặc trưng phân cấp | Các lớp nông học cạnh, các lớp sâu học ngữ nghĩa |

Các mô hình tiêu biểu: LeNet, AlexNet, VGG, ResNet, EfficientNet

### 3.2 RNN (Mạng nơ-ron hồi quy)

RNN được thiết kế đặc biệt cho **dữ liệu chuỗi**. Trạng thái ẩn của nó được truyền đến bước thời gian tiếp theo, giúp mạng có khả năng "ghi nhớ".

```
Bước thời gian t1    Bước thời gian t2    Bước thời gian t3
 "Tôi"  ──→   "thích"  ──→  "mèo"
  ↓           ↓           ↓
 [h1]  ──→  [h2]   ──→  [h3] ──→ Đầu ra
  ↑           ↑           ↑
 Trạng thái ẩn được truyền giữa các bước thời gian (ghi nhớ)
```

| Biến thể | Vấn đề giải quyết | Cơ chế cốt lõi |
|----------|-------------------|----------------|
| RNN gốc | Mô hình hóa chuỗi cơ bản | Kết nối hồi quy đơn giản |
| LSTM     | Vấn đề vanishing gradient trong chuỗi dài | Forget gate, Input gate, Output gate |
| GRU      | Quá nhiều tham số trong LSTM | Đơn giản hóa thành reset gate và update gate |
| Bidirectional RNN | Chỉ có thể nhìn thấy quá khứ | Xử lý đồng thời từ trước ra sau và từ sau ra trước |

::: tip Cơ chế cổng của LSTM
Sự tinh tế của LSTM nằm ở ba "cổng": **Forget gate** quyết định loại bỏ những ký ức cũ nào, **Input gate** quyết định lưu trữ thông tin mới nào, và **Output gate** quyết định nội dung nào sẽ được xuất ra. Giống như khi bạn đọc một cuốn sách, bạn sẽ chọn lọc ghi nhớ những tình tiết quan trọng và quên đi những chi tiết không liên quan.
:::

### 3.3 Transformer: Attention là tất cả

Năm 2017, bài báo "Attention Is All You Need" của Google đã giới thiệu Transformer, thay đổi hoàn toàn lĩnh vực AI. Nó sử dụng **cơ chế self-attention** thay thế cấu trúc hồi quy, là nền tảng của các Large Model như GPT, BERT, Claude.

```
Chuỗi đầu vào → Embedding + Positional Encoding → [Multi-Head Attention → Feed-Forward Network] × N → Đầu ra
                                    ↑
                          Mỗi từ đều có thể "nhìn thấy" tất cả các từ khác
```

| Ưu điểm | Giải thích |
|---------|------------|
| Tính toán song song | Không giống RNN phải xử lý từng bước, Transformer có thể xử lý toàn bộ chuỗi song song |
| Phụ thuộc tầm xa | Thiết lập kết nối trực tiếp giữa hai vị trí bất kỳ, không bị giới hạn bởi khoảng cách |
| Khả năng mở rộng | Mô hình càng lớn, dữ liệu càng nhiều, hiệu quả càng tốt (Scaling Law) |

**Trực giác về Self-Attention**: Khi đọc câu "Con mèo ngồi trên tấm thảm, bởi vì **nó** rất mệt", từ "nó" cần chú ý đến "con mèo" để hiểu ý nghĩa. Self-attention giúp mô hình học được mối liên hệ này – tính toán một "điểm liên quan" cho mỗi cặp từ trong chuỗi.

<NetworkArchitectureDemo />

## 4. Nghệ thuật huấn luyện

Có kiến trúc tốt vẫn chưa đủ, trong quá trình huấn luyện có nhiều "cạm bẫy" cần tránh.

### 4.1 Overfitting vs Underfitting

| Vấn đề | Biểu hiện | Nguyên nhân | Giải pháp |
|--------|----------|------------|-----------|
| Overfitting | Hiệu suất tốt trên tập huấn luyện, kém trên tập kiểm tra | Mô hình quá phức tạp, "học thuộc lòng" thay vì học quy luật | Regularization, Dropout, Data Augmentation, Early Stopping |
| Underfitting | Hiệu suất kém trên cả tập huấn luyện và tập kiểm tra | Mô hình quá đơn giản, không học được quy luật | Tăng dung lượng mô hình, huấn luyện lâu hơn, đặc trưng tốt hơn |

```
Sai số
  ↑
  │ ╲  Sai số huấn luyện          Sai số kiểm tra  ╱
  │  ╲                          ╱
  │   ╲─────────────────╱
  │    Underfitting ← Điểm tối ưu → Overfitting
  └──────────────────────────→ Độ phức tạp của mô hình
```

### 4.2 Các siêu tham số quan trọng

Siêu tham số là các tham số cần được thiết lập thủ công trước khi huấn luyện (không phải do mô hình tự học):

| Siêu tham số | Tác dụng | Phạm vi phổ biến | Gợi ý điều chỉnh |
|--------------|----------|------------------|------------------|
| Learning rate | Mức độ cập nhật mỗi bước | 1e-5 ~ 1e-1 | Siêu tham số quan trọng nhất, thường bắt đầu từ 1e-3 |
| Batch size | Số lượng mẫu dùng để huấn luyện mỗi lần | 16 ~ 512 | Càng lớn huấn luyện càng ổn định, nhưng cần nhiều VRAM hơn |
| Số Epoch huấn luyện | Số lần duyệt qua toàn bộ tập dữ liệu | 10 ~ 100+ | Kết hợp với Early Stopping, dừng khi tập validation không còn cải thiện |
| Optimizer | Chiến lược cập nhật gradient | Adam, SGD | Adam là lựa chọn mặc định, SGD + Momentum phù hợp để tinh chỉnh |

### 4.3 Các kỹ thuật Regularization

Các phương pháp phổ biến để ngăn overfitting:

| Kỹ thuật | Nguyên lý | Cách sử dụng |
|----------|-----------|--------------|
| Dropout | Ngẫu nhiên tắt một phần nơ-ron trong quá trình huấn luyện | Thường p=0.1~0.5 |
| Weight Decay | Thêm hình phạt cho độ lớn của trọng số vào Loss Function | L2 Regularization, λ=1e-4 |
| Data Augmentation | Thực hiện các biến đổi ngẫu nhiên trên dữ liệu huấn luyện (lật, cắt, xoay) | Cần thiết cho các tác vụ hình ảnh |
| Early Stopping | Dừng huấn luyện khi Loss trên tập validation không còn giảm | patience=5~10 |
| Batch Normalization | Chuẩn hóa phân phối đầu vào của mỗi lớp | Tăng tốc hội tụ, có hiệu ứng regularization nhẹ |

::: tip Quy tắc kinh nghiệm khi huấn luyện
1.  Đầu tiên, chạy toàn bộ quy trình với một tập dữ liệu nhỏ để xác nhận mã không có lỗi
2.  Bắt đầu fine-tuning từ các mô hình pre-trained có sẵn, thay vì huấn luyện từ đầu
3.  Learning rate là siêu tham số đáng dành thời gian để điều chỉnh nhất
4.  Nếu Loss huấn luyện không giảm, hãy kiểm tra dữ liệu và mã trước, sau đó mới nghi ngờ mô hình
:::

---

## 5. Lịch sử phát triển và xu hướng tiên tiến

Sự phát triển của mạng nơ-ron đã trải qua vài "mùa đông" và "phục hưng", mỗi đột phá đều bắt nguồn từ những đổi mới công nghệ then chốt.

| Niên đại | Cột mốc | Đột phá quan trọng |
|---------|--------|--------------------|
| 1958    | Perceptron | Mô hình mạng nơ-ron đầu tiên, chỉ có thể xử lý các vấn đề tuyến tính |
| 1986    | Thuật toán Backpropagation | Giúp việc huấn luyện mạng đa lớp trở nên khả thi |
| 1998    | LeNet (CNN) | Mạng tích chập đạt thành công lớn trong nhận diện chữ số viết tay |
| 2012    | AlexNet | Deep CNN vượt trội các phương pháp truyền thống trên ImageNet, Deep Learning bùng nổ |
| 2014    | GAN (Generative Adversarial Network) | Hai mạng huấn luyện đối kháng, có thể tạo ra hình ảnh chân thực |
| 2017    | Transformer | "Attention Is All You Need", cơ chế attention thay thế RNN |
| 2018    | BERT | Mô hình Pre-training + Fine-tuning, NLP đột phá toàn diện |
| 2020    | GPT-3 | 175 tỷ tham số, thể hiện khả năng emergent của Large Model |
| 2022    | ChatGPT | Kỹ thuật căn chỉnh RLHF, AI đi vào tầm nhìn của công chúng |
| 2023+   | Large Model đa phương thức | GPT-4V, Claude, v.v., đồng thời hiểu văn bản và hình ảnh |

### Xu hướng hiện tại

| Hướng | Giải thích |
|-------|------------|
| Large Model (LLM) | Số lượng tham số từ hàng tỷ đến hàng nghìn tỷ, xuất hiện các khả năng như suy luận, lập trình |
| Đa phương thức | Cùng một mô hình xử lý văn bản, hình ảnh, âm thanh, video |
| Fine-tuning hiệu quả | Các kỹ thuật như LoRA, QLoRA cho phép các nhà phát triển thông thường cũng có thể fine-tune Large Model |
| AI Agent | Cho phép Large Model sử dụng công cụ, lập kế hoạch nhiệm vụ, tự chủ hoàn thành các mục tiêu phức tạp |
| Model Distillation cho Small Model | Sử dụng kiến thức của Large Model để huấn luyện Small Model, triển khai trên thiết bị biên |

::: tip Lời khuyên cho các nhà phát triển
Bạn không cần phải huấn luyện mạng nơ-ron từ đầu. Phát triển AI hiện đại chủ yếu là **gọi API** (như OpenAI, Claude API) hoặc **fine-tune các mô hình pre-trained** (như sử dụng Hugging Face). Nhưng việc hiểu các nguyên lý cơ bản có thể giúp bạn lựa chọn mô hình tốt hơn, thiết kế prompt hiệu quả hơn và chẩn đoán vấn đề.
:::

---

## Tóm tắt

| Khái niệm cốt lõi | Tóm tắt trong một câu |
|-------------------|----------------------|
| Nơ-ron | Tổng hợp có trọng số + Activation Function, đơn vị tính toán nhỏ nhất của mạng |
| Lan truyền thuận | Dữ liệu chảy từ input layer qua từng lớp đến output layer, tạo ra dự đoán |
| Lan truyền ngược | Bắt đầu từ Loss, tính gradient từng lớp, cập nhật trọng số |
| CNN | Kernel tích chập trích xuất đặc trưng cục bộ, lựa chọn hàng đầu cho xử lý hình ảnh |
| RNN/LSTM | Kết nối hồi quy duy trì bộ nhớ, xử lý dữ liệu chuỗi |
| Transformer | Self-attention xử lý song song, kiến trúc nền tảng của Large Model |
| Overfitting | Mô hình "học thuộc lòng", sử dụng Regularization, Dropout và các phương pháp khác để ngăn chặn |
| Transfer Learning | Đứng trên vai người khổng lồ, sử dụng mô hình pre-trained để fine-tune giải quyết vấn đề mới |

---

## Đọc thêm

-   [3Blue1Brown - Loạt video về mạng nơ-ron](https://www.3blue1brown.com/topics/neural-networks) — Giải thích trực quan nhất bằng hình ảnh
-   [Stanford CS231n](http://cs231n.stanford.edu/) — Khóa học kinh điển về Convolutional Neural Network
-   [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — Giải thích kiến trúc Transformer bằng hình ảnh
-   [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/) — Tài liệu học trực tuyến miễn phí
-   [Khóa học Hugging Face](https://huggingface.co/learn) — Thực hành Transformer và Large Model
