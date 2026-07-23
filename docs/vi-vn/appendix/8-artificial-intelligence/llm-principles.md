# Cách thức hoạt động của các Large Language Model

> 💡 **Hướng dẫn học tập**: Chương này không yêu cầu kiến thức lập trình. Thông qua các minh họa tương tác, bạn sẽ hiểu sâu sắc về nguyên lý hoạt động cơ bản của các Large Language Model (LLM). Chúng ta sẽ bắt đầu từ khái niệm Tokenization cơ bản nhất, cho đến cách GPT được huấn luyện và suy luận.

<LlmQuickStartDemo />

## 0. Giới thiệu: Từ ngôn ngữ con người đến tính toán của máy

Con người giao tiếp bằng ngôn ngữ, máy tính tính toán bằng số.
Bản chất của **Large Language Model (LLM)** chính là một cây cầu nối hai thế giới này.

Nhiệm vụ cốt lõi của nó chỉ có một: **chuyển đổi vấn đề "hiểu ngôn ngữ" thành vấn đề "tính toán toán học".**

Để đạt được mục tiêu này, chúng ta cần giải quyết ba thách thức cốt lõi:

1.  **Dịch thuật**: Làm thế nào để biến văn bản thành số? (Tokenization & Embedding)
2.  **Hiệu quả**: Làm thế nào để máy tính tính toán nhanh chóng? (Phép toán ma trận)
3.  **Ghi nhớ**: Làm thế nào để máy tính hiểu được ngữ cảnh? (Mô hình Transformer)

Hướng dẫn này sẽ đưa bạn từng bước khám phá quá trình xây dựng cây cầu này từ đầu.

---

## 1. Bước đầu tiên: Dịch thuật (Tokenization)

Máy tính không hiểu hai chữ "hamburger", nó chỉ nhận biết các con số.
Vì vậy, nhiệm vụ đầu tiên của chúng ta là: **chia văn bản thành các đơn vị nhỏ nhất mà máy tính có thể hiểu được**.

### 1.1 Tokenization là gì?

Tokenization là quá trình chia một câu thành từng "đơn vị từ" (Token).

- **Tiếng Anh**: Có khoảng trắng tự nhiên, dễ dàng Tokenization (ví dụ: `I love AI`).
- **Tiếng Trung**: Không có khoảng trắng, cần thuật toán để chia (ví dụ: `我爱人工智能`).

#### Tokenizer (Người phiên dịch)

Chương trình thực hiện hành động Tokenization được gọi là **Tokenizer**.
Nó giống như một người phiên dịch, chịu trách nhiệm dịch văn bản của con người thành chuỗi số mà máy có thể đọc được.

Các LLM hiện đại (như GPT-4) thường sử dụng kỹ thuật **Subword Tokenization (Tokenization theo từ con)** (ví dụ: thuật toán BPE).
Điểm thông minh của nó là: **các từ thông dụng được giữ nguyên, các từ hiếm được chia nhỏ**.

Dưới đây là một ví dụ BPE Tokenization thực tế (dựa trên GPT-4 Tokenizer):

**Input**: `"The quick brown fox jumps over the lazy dog. \n今天天气真不错！"`

**Token List**:

```text
index=791,   string='The'
index=4062,  string=' quick'
index=14198, string=' brown'
index=39935, string=' fox'
index=83368, string=' jumps'   <-- Nếu bị chia nhỏ, có thể là ' jump' + 's'
index=927,   string=' over'
index=279,   string=' the'
index=16053, string=' lazy'
index=3290,  string=' dog'
index=13,    string='.'
index=198,   string='\n'       <-- Ký tự xuống dòng
index=33838, string='今天'      <-- Từ thông dụng được gộp trực tiếp
index=54580, string='天气'
index=20265, string='真'
index=57672, string='不错'
index=171,   string='！'
```

> **Về cách xử lý các ký tự hiếm**:
> Nếu gặp một ký tự hiếm không có trong từ điển (giả sử chữ "今" rất hiếm), mô hình sẽ quay lại mã hóa ở cấp độ **Byte**.
> 1.  Raw Input: `今`
> 2.  Bytes: `\xE4 \xBB \x8A`
> 3.  BPE tìm kiếm: Đầu tiên tìm `\xE4\xBB\x8A` -> không tìm thấy -> chia thành `\xE4\xBB` (ID=1001) + `\x8A` (ID=2002).
> 4.  Token cuối cùng: `[1001, 2002]`.
>
> Cơ chế này đảm bảo rằng **bất kể đầu vào là ký tự gì, mô hình đều có thể xử lý, sẽ không bao giờ xảy ra vấn đề OOV (Out Of Vocabulary)**.

<TokenizationDemo />

**Điểm mấu chốt**: LLM không xử lý các từ, mà là **Token ID** (một chuỗi chỉ mục số).

---

## 2. Thách thức cốt lõi: Làm thế nào để máy tính “tính toán” ngôn ngữ?

Nhiệm vụ của chúng ta là xử lý ngôn ngữ. Nhưng máy tính chỉ nhận biết các con số.
Ý tưởng trực tiếp nhất là: gán cho mỗi từ một số (ID).

- Táo -> ID 10
- Chuối -> ID 20

### 2.1 Tại sao không dùng ID đơn giản?

Nếu chỉ dùng ID, máy tính sẽ nghĩ rằng "10" và "20" chỉ là hai con số không liên quan gì đến nhau.
Hơn nữa, nếu từ điển có 100.000 từ, chúng ta có thể cần một mảng dài 100.000 phần tử để biểu diễn một từ (mã hóa One-Hot), trong đó 99.999 vị trí là 0, chỉ có một vị trí là 1.

- **Nhược điểm 1: Quá lãng phí** (rỗng, mảng One-Hot quá lớn).
- **Nhược điểm 2: Không có ý nghĩa** (không thể biểu thị "táo" và "chuối" đều là trái cây).

### 2.2 Giải pháp: Embedding (Vector dày đặc)

Để biểu thị một từ một cách **hiệu quả** và **có ý nghĩa**, chúng ta đã phát minh ra **Embedding**.
Nó không còn dùng một mảng 0/1 dài ngoằng nữa, mà dùng một mảng ngắn hơn, chứa đầy các số thập phân (ví dụ: 512 số) để mô tả một từ.

- Ví dụ: `[0.8 (là trái cây), 0.1 (màu đỏ), 0.9 (ngọt)...]`
  Bằng cách này, chúng ta không chỉ nén dữ liệu mà còn biến ý nghĩa của từ thành "tọa độ" có thể tính toán được.

<EmbeddingDemo />

---

## 3. Từ Từ đơn đến Ma trận

Sau khi giải quyết vấn đề biểu diễn "một từ", tiếp theo chúng ta sẽ giải quyết vấn đề biểu diễn "một câu".

### 3.1 Tại sao phải là ma trận?

Bởi vì một câu chứa nhiều từ.

- Một từ = Một hàng số (vector).
- Một câu = Nhiều hàng số xếp chồng lên nhau.
  Đây chính là **ma trận**.

Lý do phải ghép thành ma trận là vì phần cứng cốt lõi của máy tính hiện đại – **GPU (card đồ họa)**, vốn được thiết kế để thực hiện các phép toán ma trận.
Chỉ khi ngôn ngữ được biến thành ma trận, chúng ta mới có thể tận dụng khả năng song song của GPU để đạt được suy luận và huấn luyện **hiệu quả cao**.

### 3.2 Quy trình hoàn chỉnh

Hãy xem lại cách dữ liệu di chuyển:

1.  **Tokenization**: Chia nhỏ văn bản.
2.  **Lập chỉ mục**: Biến các mảnh nhỏ thành ID.
3.  **Embedding**: Biến ID thành vector (để có ngữ nghĩa và nén).
4.  **Xếp chồng**: Ghép các vector thành ma trận (để GPU tính toán hiệu quả).

<TokenizerToMatrix />

---

## 3.5 Xen kẽ: "Mô hình" thực sự là gì?

Trước khi đi sâu vào kiến trúc cụ thể, chúng ta hãy hiểu một cách thông thường về từ "mô hình".

Trong lĩnh vực AI, **mô hình (Model)** thực chất là một **hàm** hoặc **hộp đen** cực kỳ phức tạp.

- **Đầu vào**: Một đống số (ví dụ: các Token ID ở trên).
- **Xử lý**: Trong hộp đen có hàng tỷ tham số (có thể hiểu là hàng tỷ núm điều chỉnh), chúng sẽ thực hiện các phép cộng, trừ, nhân, chia điên cuồng trên dữ liệu đầu vào.
- **Đầu ra**: Một đống số khác (đại diện cho kết quả dự đoán, ví dụ: xác suất của từ tiếp theo).

**Ví dụ:**

Bạn có thể hình dung mô hình như một **đầu bếp lão luyện**:

1.  **Đầu vào (nguyên liệu)**: Bạn đưa cho anh ta thịt bò, khoai tây, cà chua.
2.  **Mô hình (bộ não của đầu bếp)**: Anh ta dựa trên hàng ngàn công thức đã học (dữ liệu huấn luyện), nhanh chóng tính toán trong đầu: thái thịt bò, gọt khoai tây, kiểm soát lửa...
3.  **Đầu ra (món ăn)**: Cuối cùng, anh ta mang ra một đĩa thịt bò hầm khoai tây.

Cái gọi là **huấn luyện (Training)**, chính là để đầu bếp này bắt đầu từ một người học việc, cho anh ta thử sai hàng tỷ lần. Nấu mặn thì điều chỉnh "núm muối", nấu nhạt thì điều chỉnh "núm lửa", cho đến khi anh ta có thể ổn định nấu ra những món ăn ngon.

LLM hiện nay chính là một đầu bếp siêu hạng "đã đọc tất cả sách vở của nhân loại", chỉ có điều anh ta không nấu món ăn mà là "xào" chữ.

## 4. Con đường tiến hóa: Từ RNN đến Transformer

Có dữ liệu (Token), có đầu bếp (Model), tiếp theo chúng ta sẽ xem đầu bếp này suy nghĩ như thế nào.

Trong lịch sử tiến hóa của AI, có hai "cách suy nghĩ" (kiến trúc) chính: **RNN** và **Transformer**.

### 4.1 Cách làm cũ kém hiệu quả: RNN (Trò chơi truyền tin)

Các Model đời đầu (RNN, Recurrent Neural Network) khi xử lý một câu, giống như chúng ta đang chơi **trò chơi truyền tin**.

**Cách hoạt động:**

1.  Đọc từ thứ 1 "Tôi", ghi nhớ trong đầu, truyền cho bước thứ 2.
2.  Đọc từ thứ 2 "thích", kết hợp với ký ức vừa rồi, cập nhật thông tin trong đầu, rồi truyền cho bước thứ 3.
3.  Đọc từ thứ 3 "ăn", lại cập nhật ký ức...
4.  ...cho đến khi đọc hết từ cuối cùng.

**Điều này dẫn đến hai nhược điểm chí mạng:**

1.  **Chậm (không thể song song)**: Phải đợi người trước truyền tin xong, người sau mới có thể bắt đầu. Không thể để 100 người cùng làm việc một lúc.
2.  **Quên (quên xa)**: Khi tin tức được truyền đến người thứ 100, anh ta có thể đã quên người thứ 1 nói là "tôi" hay "bạn". Điều này khiến Model khi viết bài dài dễ bị "đầu voi đuôi chuột".

### 4.2 Thiết kế thiên tài hiện nay: Transformer (Hội nghị bàn tròn)

Năm 2017, Google đã đề xuất một kiến trúc hoàn toàn mới – **Transformer**. Nó đã thay đổi hoàn toàn luật chơi, biến "trò chơi truyền tin" thành **hội nghị bàn tròn**.

**Cách hoạt động:**
Transformer không còn truyền tin từng từ một nữa, mà để **tất cả các từ cùng ngồi vào bàn một lúc**.

1.  **Góc nhìn toàn năng (tính toán song song)**: Tất cả các từ cùng vào cuộc, không cần xếp hàng. Mọi người viết thông tin của mình lên giấy, trải ra giữa bàn.
2.  **Cơ chế Attention (Chú ý)**: Đây là vũ khí bí mật của nó. Mỗi từ đều có thể **trực tiếp** xem thông tin của bất kỳ từ nào khác trên bàn.
    - Ví dụ, khi đọc đến chữ "nó", Model không cần nhớ lại lời truyền tin trước đó, mà trực tiếp nhìn thấy "con mèo" ở phía trước, ngay lập tức hiểu "nó = con mèo".

**Điều này đã giải quyết hoàn hảo các vấn đề của RNN:**

- **Nhanh**: Mọi người cùng xem tài liệu, GPU có thể hoạt động hết công suất, hiệu quả cực cao.
- **Không quên**: Bất kể câu dài bao nhiêu, khoảng cách giữa từ thứ 1 và từ thứ 10000 đều là "một bước", muốn xem từ nào thì xem từ đó.

> **Tóm tắt**:
>
> - **RNN**: Giống như đi mê cung, mò mẫm từng bước, dễ lạc đường.
> - **Transformer**: Giống như có góc nhìn toàn năng để xem bản đồ, điểm cuối và điểm đầu đều nằm trong tầm mắt.

#### Tại sao vẫn cần thông tin "vị trí"?

Bởi vì Transformer là "gom tất cả vào một rổ", nếu không xử lý đặc biệt, nó sẽ không phân biệt được sự khác biệt giữa "tôi yêu bạn" và "bạn yêu tôi" (các từ đều giống nhau, chỉ khác thứ tự).
Vì vậy, chúng ta sẽ dán cho mỗi từ một **thẻ số (mã hóa vị trí)**, để nói cho Model biết ai ở vị trí thứ 1, ai ở vị trí thứ 2.

> Lưu ý nhỏ: Nhiều LLM là tự hồi quy (dự đoán từ tiếp theo), vì vậy khi tạo ra văn bản vẫn là nhả ra từng Token một; nhưng trong tính toán nội bộ của **mỗi bước tạo ra**, Transformer vẫn có thể tận dụng tốt hơn các tối ưu hóa ma trận song song và bộ nhớ đệm.

### 4.3 Công nghệ đen hiệu quả: KV Cache

Bạn có thể đã nghe nói rằng khi tạo văn bản dài, càng về sau càng chậm, hoặc chiếm nhiều VRAM hơn. Điều này thường là do Model cần "ghi nhớ" tất cả nội dung đã tạo trước đó.

**Transformer "ghi chú" như thế nào?**

Trong cơ chế Attention của Transformer, mỗi từ sẽ tạo ra hai vector `Key (K)` và `Value (V)`, được sử dụng để các từ sau "truy vấn".

- Khi Model tạo ra từ thứ 100, nó cần quay lại xem K và V của 99 từ trước đó.
- Nếu mỗi lần đều tính toán lại K và V của 99 từ trước đó, thì quá lãng phí!

**Tác dụng của KV Cache:**

KV Cache giống như một **"sổ ghi chú tăng dần"**.

1.  **Không tính lại**: Tính xong K và V của từ thứ 1, lưu lại.
2.  **Chỉ tính cái mới**: Khi tạo từ thứ 2, chỉ tính K và V của từ thứ 2, sau đó ghép với K, V của từ thứ 1.
3.  **Càng lưu càng nhiều**: Khi cuộc hội thoại tiếp diễn, "sổ ghi chú" này (VRAM chiếm dụng) sẽ càng ngày càng dày lên.

Đây là lý do tại sao các cuộc hội thoại văn bản dài (Long Context) lại tiêu tốn nhiều VRAM – **không phải Model lớn hơn, mà là ghi chú (KV Cache) quá dày.**

<RNNvsTransformer />

---

## 5. Tiết lộ: Từ “viết tiếp” đến “đối thoại”

Nhiều người lầm tưởng rằng ChatGPT thực sự hiểu chúng ta đang nói gì, nhưng thực ra bản năng của nó chỉ có một: **đoán từ tiếp theo** (Next Token Prediction).

### 5.1 Bản năng: Viết tiếp điên cuồng

Nếu bạn nhập vào một Base Model: "Hôm nay trời đẹp", nó có thể viết tiếp: "Hãy đi công viên chơi nhé."
Nhưng nếu bạn nhập: "Thủ đô của Mỹ là gì?", nó có thể viết tiếp: "Thủ đô của Trung Quốc là gì? Thủ đô của Nhật Bản là gì?" (Bởi vì nó đang bắt chước định dạng của một bài kiểm tra, chứ không phải trả lời câu hỏi).

### 5.2 Kỹ thuật: Dùng "kịch bản" để đối thoại

Để biến nó thành một trợ lý đối thoại, các kỹ sư đã nghĩ ra một cách tuyệt vời: **đóng vai**.
Chúng ta đã âm thầm thêm một số **thẻ đặc biệt (Template)** vào nội dung nhập cho Model, khiến Model nghĩ rằng mình đang viết tiếp một "kịch bản đối thoại".

Ví dụ, bạn thấy là:

> User: Xin chào

Model thực sự thấy là:

> `<|user|>` Xin chào `<|assistant|>`

Model vừa nhìn thấy `<|assistant|>` là biết ngay: "Ồ, đến lượt mình đóng vai trợ lý nói chuyện rồi."

### 5.3 Minh họa tương tác chuyên sâu

Bản demo dưới đây sẽ đưa bạn từng bước hiểu rõ bản chất của LLM. Vui lòng lần lượt nhấp vào **1. Bản năng -> 2. Kỹ thuật -> 3. Nguyên lý -> 4. Nâng cao**, và tự mình thử nghiệm!

<TrainingInferenceDemo />

---

## 6. Từ “nói bậy” đến “trợ lý tốt” (Alignment)

Chỉ biết đối thoại thôi chưa đủ. Model nguyên bản có thể dạy người ta chế tạo bom, hoặc nói tục.
Để nó trở thành một trợ lý lịch sự, an toàn và đáng tin cậy như ChatGPT, cần thêm hai bước hoàn thiện cuối cùng:

1.  **SFT (Supervised Fine-Tuning)**:
    - Tìm các chuyên gia con người viết nhiều cặp hỏi đáp chất lượng cao, dạy Model "cách nói chuyện tử tế".
    - Mục tiêu: Giúp Model hiểu các chỉ thị, không còn viết tiếp lung tung.
    - _Ví dụ dữ liệu (định dạng JSON)_:
      ```json
      // Ví dụ dữ liệu huấn luyện SFT
      {
        "messages": [
          { "role": "user", "content": "Hãy dịch câu này sang tiếng Anh: “Xin chào”." },
          { "role": "assistant", "content": "Hello." }
        ]
      }
      // Model đã học được: khi nghe lệnh “dịch”, phải trực tiếp đưa ra kết quả, chứ không phải viết tiếp “Bạn khỏe không”
      ```

2.  **RLHF (Reinforcement Learning from Human Feedback)**:
    - **Đánh giá**: Cho Model tạo ra một vài câu trả lời, giáo viên con người sẽ đánh giá (câu nào an toàn hơn? câu nào lịch sự hơn?).
    - **Thưởng phạt**: Nếu Model nói tốt thì được thưởng, nói không tốt thì bị phạt. Dần dần, Model sẽ học được cách "Alignment" với các giá trị của con người.
    - _Ví dụ dữ liệu (định dạng JSON)_:
      ```json
      // Ví dụ dữ liệu ưu tiên RLHF (DPO/PPO)
      {
        "prompt": "Làm thế nào để chế tạo bom?",
        "chosen": "Xin lỗi, tôi không thể trả lời câu hỏi này.", // Câu trả lời được con người ưa thích hơn (an toàn)
        "rejected": "Đầu tiên bạn cần..." // Câu trả lời bị con người từ chối (nguy hiểm)
      }
      ```

**Trong bản demo phía trên, nhấp vào tab thứ 4 "Nâng cao: Alignment", bạn có thể tự mình trải nghiệm sự khác biệt lớn trước và sau khi Alignment.**

---

## 7. Khám phá tiên tiến: Các Thinking Model, kiến trúc MoE và cơ chế Linear Attention

Với sự phát triển của công nghệ, chúng ta nhận thấy rằng chỉ dựa vào "dự đoán từ tiếp theo" đôi khi sẽ mắc lỗi ngớ ngẩn, đặc biệt khi xử lý các vấn đề toán học và logic.
Do đó, thế hệ **Thinking Models** mới (như OpenAI o1, DeepSeek-R1) đã ra đời.

### 7.1 "Suy nghĩ" là gì? (Thinking Models)

Con người khi trả lời các câu hỏi phức tạp (ví dụ: 9.11 và 9.9 cái nào lớn hơn?) sẽ không nói ra ngay lập tức, mà sẽ suy nghĩ trong đầu trước.
Thinking Model chính là Model đã học được khả năng **suy nghĩ chậm (System 2)** này.

- **Suy nghĩ nhanh (System 1)**: Dựa vào trực giác, nói ra ngay. Dễ mắc lỗi.
- **Suy nghĩ chậm (System 2)**: Thông qua việc tạo ra một "chuỗi suy nghĩ (Chain of Thought)", suy luận từng bước, cuối cùng đưa ra câu trả lời.

<ThinkingModelDemo />

### 7.2 Tiết lộ về huấn luyện: Từ “bắt chước” đến “khám phá”

Tại sao các Model trước đây không suy nghĩ như vậy? Bởi vì phương pháp huấn luyện đã thay đổi.

#### Chế độ truyền thống (SFT - Học bắt chước)

- **Phương pháp**: Cho Model xem quá trình tư duy của con người, để nó **bắt chước**.
- **Hạn chế**: Giới hạn của Model là dữ liệu của con người và chất lượng của nó. Nếu con người tự mình cũng không thể suy nghĩ rõ ràng (ví dụ: các bài toán cực khó), Model cũng không học được.

#### Chế độ suy nghĩ (RL - Học tăng cường)

- **Phương pháp**: **Không cung cấp** dữ liệu quá trình, chỉ cung cấp **bộ xác minh (Verifier)** cuối cùng.
  - Ví dụ: đưa một bài toán, Model tự mình thử lung tung.
  - Thử sai -> phạt.
  - Thử đúng -> thưởng.
- **Khoảnh khắc giác ngộ (Aha Moment)**:
  Sau hàng ngàn lần tự thử nghiệm, Model ngạc nhiên phát hiện: **"Nếu tôi viết thêm vài bước suy luận trên giấy nháp trước khi đưa ra câu trả lời, xác suất nhận được phần thưởng sẽ tăng lên đáng kể!"**
  Và thế là, kiểu hành vi "suy nghĩ trước, trả lời sau" này đã được tăng cường và cố định. Điều này giống như AlphaGo tự đấu với chính mình, cuối cùng vượt qua các kỳ thủ cờ vây của con người.

### 7.3 Hướng dẫn thực chiến: Thay đổi lớn trong phong cách Prompt

Khi sử dụng Thinking Model (như DeepSeek-R1, OpenAI o1), chiến lược Prompt của bạn cần thay đổi hoàn toàn.

| Đặc điểm       | Model truyền thống (GPT-4o, Claude 3.5)            | Thinking Model (R1, o1)                                  |
| :------------- | :------------------------------------------------ | :------------------------------------------------------- |
| **Logic cốt lõi** | **System 1 (Trực giác)**                          | **System 2 (Logic)**                                     |
| **Kỹ thuật Prompt** | Cần hướng dẫn Chain of Thought (CoT)<br>Ví dụ: "Hãy suy nghĩ từng bước..." | **Không nên** thêm thắt<br>Model tự có Chain of Thought, hướng dẫn thủ công sẽ làm nhiễu nó |
| **Độ rõ ràng của chỉ thị** | Cần chia nhỏ nhiệm vụ phức tạp thành các nhiệm vụ con | Trực tiếp đưa ra mục tiêu cuối cùng, để Model tự chia nhỏ |
| **Kịch bản áp dụng** | Viết sáng tạo, dịch thuật đơn giản, trò chuyện   | Toán học phức tạp, tái cấu trúc mã, suy luận logic       |

> ⚠️ **Lưu ý**: Đối với Thinking Model, càng ít can thiệp càng tốt. Bạn chỉ cần định nghĩa rõ ràng **"kết quả nhiệm vụ hoàn hảo là gì"**, chứ không cần định nghĩa **"phải làm thế nào"**.

### 7.4 Xu hướng tương lai: Kết hợp nhanh-chậm

Trong tương lai, chúng ta có thể không cần phân biệt "Thinking Model" và "Model thông thường" nữa.
AI lý tưởng nên giống như con người, có khả năng **tính toán thích ứng (Adaptive Compute)**:

- Gặp "1+1=?": Ngay lập tức gọi System 1, trả lời trong tích tắc.
- Gặp "Chứng minh giả thuyết Riemann": Tự động chuyển sang System 2, suy nghĩ ba ngày ba đêm rồi mới trả lời.
- **Người dùng không cảm nhận được sự chuyển đổi**: Bạn chỉ cần đặt câu hỏi, Model tự quyết định dùng bao nhiêu "năng lực não bộ" để giải quyết.

### 7.5 Tiến hóa kiến trúc: Từ “toàn năng” đến “nhóm chuyên gia” (Dense vs MoE)

Khi các Model ngày càng lớn (ví dụ: GPT-4, DeepSeek-V3), nếu mỗi lần tạo ra một chữ mà phải tính toán tất cả các neuron, tốc độ sẽ chậm đến mức không thể chấp nhận được.
Do đó, kiến trúc **MoE (Mixture of Experts, hỗn hợp chuyên gia)** đã ra đời.

- **Dense (Mô hình dày đặc)**:
  - **Ví von**: Một **thiên tài toàn năng**. Bất kể hỏi vấn đề gì, anh ta đều huy động toàn bộ bộ não để trả lời.
  - **Đặc điểm**: Ổn định, nhưng khi lượng kiến thức tăng lên, phản ứng càng chậm.
  - **Đại diện**: GPT-3, Llama-2.

- **MoE (Mô hình hỗn hợp chuyên gia)**:
  - **Ví von**: Một **nhóm chuyên gia trên dây chuyền sản xuất** (mỗi khi xử lý một chữ thì thay người một lần).
  - **Cơ chế cốt lõi (Token-Level Routing)**:
    Tinh túy của MoE nằm ở **Token-Level Routing nguyên bản**. Nó **hoàn toàn không** phân công theo "loại nhiệm vụ" (ví dụ: giao tất cả các bài toán cho chuyên gia toán học), mà là **phân công theo "chữ đang được tạo ra" theo thời gian thực**.
    - Khi Model tạo ra "`def`", nó được định tuyến đến **chuyên gia mã hóa**.
    - Khi Model tạo ra "`love`", nó được định tuyến đến **chuyên gia văn học**.
    - Khi Model tạo ra "`3.14`", nó được định tuyến đến **chuyên gia toán học**.
    Điều này có nghĩa là, ngay cả trong cùng một câu, các chữ khác nhau thường được xử lý bởi các chuyên gia khác nhau.
  - **Đặc điểm**: Mặc dù tổng số người nhiều (số lượng tham số lớn), nhưng khi xử lý mỗi chữ chỉ có vài người làm việc (số lượng tham số kích hoạt ít). **Vừa uyên bác, vừa nhanh**.
  - **Đại diện**: GPT-4, DeepSeek-V3, Mixtral.

<MoEDemo />

### 7.6 Cách mạng hiệu quả: Vượt qua giới hạn độ dài (Linear Attention)

Ngoài MoE, còn một vấn đề cốt lõi khác: **độ dài ngữ cảnh**.
Transformer truyền thống (như GPT-4) sử dụng **cơ chế Attention tiêu chuẩn**, khối lượng tính toán của nó **tăng theo cấp số nhân** khi số lượng từ tăng lên.

- Đọc 10.000 từ, khối lượng tính toán là 100 triệu lần.
- Đọc 100.000 từ, khối lượng tính toán là 10 tỷ lần!

Để giải quyết vấn đề này, các Model như MiniMax (dòng abab) và RWKV đã áp dụng **cơ chế Linear Attention**.

### Tại sao một cái là “mạng lưới”, một cái là “tuyến tính”?

Sự khác biệt cơ bản nằm ở chỗ: **bạn chọn "giữ lại tất cả lời gốc", hay chọn "tóm tắt bất cứ lúc nào"?**

- **Standard Attention (mạng lưới) – Tại sao phải nhìn lại?**
  - **Lý do cốt lõi**: Để **"tìm kiếm sự liên quan"**.
  - **Ví dụ**: Ví dụ câu "Tôi đưa **quả táo** cho **nó**...". Khi bạn đọc đến chữ "**nó**", để làm rõ "nó" chỉ ai, Model phải quay lại quét tất cả các từ phía trước (tôi, đưa, quả táo, cho).
  - **Quá trình**: "Nó" phát ra một tín hiệu truy vấn (Query), để khớp với các nhãn (Key) của tất cả các từ phía trước.
    - Khớp với "tôi"? 0 điểm.
    - Khớp với "quả táo"? **100 điểm!**
  - **Cái giá**: Bởi vì Model không biết từ nào quan trọng, nên **phải kiểm tra tất cả các từ phía trước, không bỏ sót một từ nào**. Đó là lý do tại sao các đường nối tạo thành một mạng lưới.

- **Linear Attention (tuyến tính) – Tại sao có thể không nhìn lại?**
  - **Nguyên lý**: Model học cách "ghi chú". Đọc xong "quả táo", nó nén thông tin "có một quả táo" vào **trạng thái (State)**; khi đọc đến "nó", trực tiếp tra cứu trạng thái trong tay, là có thể biết "nó = quả táo".
  - **Cái giá**: Mặc dù nhanh, nhưng trong quá trình "nén" có thể mất một số chi tiết (ví dụ: quên mất quả táo màu đỏ).

<LinearAttentionDemo />

### 7.7 So sánh kiến trúc lớn: RNN vs Transformer vs RWKV

| Kiến trúc         | Cơ chế cốt lõi | Độ phức tạp (độ dài N) | Huấn luyện song song | Tốc độ suy luận | Vấn đề quên | Model đại diện |
| :---------------- | :------------- | :--------------------- | :------------------ | :-------------- | :---------- | :------------- |
| **RNN**           | Đệ quy tuần tự  | $O(N)$ (Thấp)          | ❌ Không thể        | Chậm (tuần tự)  | Nghiêm trọng (quên xa) | LSTM, GRU      |
| **Transformer**   | Attention toàn cục | $O(N^2)$ (Cực cao)     | ✅ Có thể           | Trung bình (KV Cache) | Không (nhưng bị giới hạn bởi cửa sổ) | GPT-4, Llama   |
| **RWKV / Linear** | Linear Attention | $O(N)$ (Thấp)          | ✅ Có thể           | Nhanh (VRAM cố định) | Nhẹ (có tổn thất nén) | RWKV, MiniMax  |

> **RWKV / Linear Attention** cố gắng kết hợp ưu điểm của hai loại trước: huấn luyện song song như Transformer, suy luận hiệu quả như RNN.

---

## 8. Tóm tắt và lộ trình học tập

Bây giờ bạn đã thông suốt từ "Tokenization" đến "ChatGPT":

1.  **Tokenization**: Văn bản được chia thành các Token.
2.  **Embedding**: Token được ánh xạ thành vector ngữ nghĩa.
3.  **Transformer**: Sử dụng cơ chế Attention để xử lý chuỗi, trích xuất đặc trưng song song.
4.  **Training**: Sử dụng Template để định dạng dữ liệu, huấn luyện song song thông qua Teacher Forcing.
5.  **Inference**: Tạo ra từng từ một theo kiểu tự hồi quy.

**Đề xuất các bước tiếp theo**:

- Nếu bạn quan tâm đến toán học, có thể tìm hiểu sâu về **đại số tuyến tính** (phép toán ma trận) và **lý thuyết xác suất**.
- Nếu bạn muốn thực hành, có thể thử sử dụng thư viện `transformers` của Python để tải một Model nhỏ (như GPT-2) và thử nghiệm.

---

## 9. Bảng tra cứu thuật ngữ (Glossary)

| Thuật ngữ          | Tên đầy đủ                                  | Giải thích                                                                                              |
| :----------------- | :----------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| **LLM**            | Large Language Model                       | Large Language Model. Mô hình AI được huấn luyện trên lượng lớn văn bản, có khả năng hiểu và tạo ngôn ngữ con người. |
| **Token**          | -                                          | **Token**. Đơn vị nhỏ nhất mà văn bản được chia thành (như từ, chữ cái hoặc đoạn ký tự). Model đọc và ghi đều là Token ID. |
| **Embedding**      | -                                          | **Vector từ**. Ánh xạ Token vào không gian số chiều cao (ví dụ: 4096 chiều), nắm bắt mối quan hệ ngữ nghĩa của từ. |
| **Transformer**    | -                                          | Kiến trúc cốt lõi của các LLM hiện đại. Dựa trên cơ chế Attention, có khả năng xử lý văn bản dài song song. |
| **Attention**      | Attention Mechanism                        | **Cơ chế Attention**. Cho phép Model khi xử lý một từ, có thể động thái chú ý đến các từ liên quan khác trong ngữ cảnh. |
| **Context Window** | -                                          | **Cửa sổ ngữ cảnh**. Số lượng Token tối đa mà Model có thể "ghi nhớ" trong một lần suy luận (ví dụ: 128k). |
| **Pre-training**   | -                                          | **Huấn luyện trước**. Huấn luyện Model trên lượng lớn văn bản không có nhãn, để nó học các quy luật cơ bản của ngôn ngữ và kiến thức thế giới. |
| **SFT**            | Supervised Fine-Tuning                     | **Điều chỉnh tinh chỉnh có giám sát**. Sử dụng dữ liệu hỏi đáp chất lượng cao, dạy Model tuân thủ các chỉ thị của con người. |
| **RLHF**           | Reinforcement Learning from Human Feedback | **Học tăng cường từ phản hồi của con người**. Thông qua đánh giá của con người, điều chỉnh thêm hành vi của Model để phù hợp với giá trị của con người (Alignment). |
| **CoT**            | Chain of Thought                           | **Chuỗi suy nghĩ**. Kỹ thuật hướng dẫn Model tạo ra các bước suy luận trước khi đưa ra câu trả lời cuối cùng. |
| **MoE**            | Mixture of Experts                         | **Mô hình hỗn hợp chuyên gia**. Bao gồm nhiều Model con "chuyên gia", tự động chọn kích hoạt phần chuyên gia nào tùy theo vấn đề, hiệu quả cao hơn. |
| **Temperature**    | -                                          | **Nhiệt độ**. Tham số kiểm soát tính ngẫu nhiên của việc tạo ra của Model. Nhiệt độ càng cao, câu trả lời càng sáng tạo nhưng càng khó kiểm soát; nhiệt độ càng thấp, câu trả lời càng chắc chắn. |
