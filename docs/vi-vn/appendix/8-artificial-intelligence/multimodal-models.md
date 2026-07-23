# Mô hình Đa phương thức (Thị giác / Âm thanh / Video)
> 💡 **Hướng dẫn học tập**: Chương này không yêu cầu kiến thức chuyên sâu về thị giác máy tính. Thông qua các bản demo tương tác, bạn sẽ hiểu cách AI có được "đôi mắt". Chúng ta sẽ khám phá các nguyên lý cốt lõi đằng sau các mô hình như GPT-4V, Qwen-VL.

<VlmQuickStartDemo />

## 0. Giới thiệu: Gắn đôi mắt cho bộ não

Trong [Giới thiệu về Mô hình Ngôn ngữ Lớn](./llm-intro), chúng ta đã biết rằng LLM về bản chất là một "bộ não" bị nhốt trong hộp đen, chỉ có thể hiểu thế giới thông qua **văn bản**.

Sự xuất hiện của **Mô hình Đa phương thức Lớn (VLM)** tương đương với việc gắn một đôi **mắt** cho bộ não này.

Nhưng điều này không hề dễ dàng. Bởi vì:

- **Bộ não (LLM)** chỉ hiểu **văn bản** (chính xác hơn là Token ID).
- **Đôi mắt (camera)** nhìn thấy **pixel** (giá trị màu RGB).

Nhiệm vụ cốt lõi của VLM là **dịch "tín hiệu pixel" thành "tín hiệu văn bản"**, khiến LLM cảm thấy việc xem hình ảnh cũng đơn giản như đọc một bài viết.

---

## 1. Bước một: Biến hình ảnh thành "từ" (Visual Tokenization)

Hãy tưởng tượng bạn đang mô tả một bức tranh ghép cho bạn bè qua điện thoại. Bạn không thể nói hết một lúc, bạn phải mô tả từng mảnh một.
Máy tính nhìn hình ảnh cũng tương tự như vậy.

### 1.1 Cắt lát (Patchify) – Tạo ra các từ thị giác

Chúng ta biết rằng, khi xử lý văn bản, Mô hình Ngôn ngữ Lớn (LLM) sẽ phân tách câu thành từng từ (Token). Nếu bạn muốn LLM "đọc hiểu" hình ảnh, cách trực quan nhất là biến hình ảnh thành dạng tương tự như Token.

Để phù hợp với đặc tính "quen đọc từ" của các mô hình lớn, chúng ta cần một kỹ thuật có thể chuyển đổi hình ảnh hai chiều liên tục thành các đoạn rời rạc, điều này dẫn đến khái niệm **cắt lát hình ảnh (Patchify)**: chúng ta cắt một hình ảnh hai chiều hoàn chỉnh, giống như cắt đậu phụ, thành từng ô vuông nhỏ cố định (gọi là Patch).

- **Hình ảnh gốc** = một bài viết hoàn chỉnh
- **Cắt lát hình ảnh (Patch)** = một từ (Token) trong bài viết

Trong thực tế kỹ thuật, chúng ta thường chia hình ảnh thành các kích thước cố định (ví dụ: $16 \times 16$ hoặc $14 \times 14$ pixel) một cách liền mạch. Ví dụ, một hình ảnh đầu vào phổ biến $224 \times 224$ pixel, sau khi cắt sẽ trở thành $14 \times 14 = 196$ khối hình ảnh độc lập.
Thông qua thao tác này, mảng pixel hai chiều liên tục ban đầu được cắt vật lý thành 196 "từ thị giác" rời rạc.

> 🕹️ **Bản demo tương tác**: Nhấp vào nút bên dưới để trải nghiệm cách hình ảnh gốc được cắt thành từng Patch độc lập bằng lưới ô vuông đều đặn.

<PatchifyDemo />

### 1.2 Tuần tự hóa (Flatten) – Xếp thành một câu

Sau khi hoàn thành bước cắt lát ở trên, chúng ta hiện có một ma trận hai chiều $14 \times 14$. Tuy nhiên, cả Transformer truyền thống lẫn LLM hiện đại, về kiến trúc cơ bản, chúng chủ yếu chỉ chấp nhận **đầu vào tuần tự một chiều** (tức là cấu trúc dữ liệu tuyến tính được xếp thành một hàng từ trái sang phải).

Để tương thích với quy tắc đầu vào của mô hình lớn, chúng ta phải thực hiện **tuần tự hóa (Flatten) và chiếu tuyến tính (Linear Projection)**:
1.  **Làm phẳng (Flatten)**: Nối các khối hình ảnh từ nhiều hàng lại với nhau, "làm phẳng" ma trận hai chiều thành một trục dài một chiều chỉ có thứ tự trước sau.
2.  **Kéo dài đặc trưng (Projection)**: 196 khối này hiện tại chỉ là "thịt sống" được xếp chồng từ các pixel đỏ, xanh lá, xanh dương. Chúng ta cần sử dụng một mạng nơ-ron nhỏ (thường là một lớp kết nối đầy đủ) để xử lý từng khối, nén và chuyển đổi chúng thành một vector đặc trưng có độ dài cố định (ví dụ: một danh sách số có độ dài 768).

Sau bước này, một hình ảnh mới thực sự trở thành một chuỗi "tuần tự từ thị giác" (Visual Token Sequence).

> 🕹️ **Bản demo tương tác**: Quan sát hoạt ảnh bên dưới để hiểu cách **một khối pixel đơn thuần (Patch)** trải qua quá trình kéo dài ma trận, cuối cùng được ánh xạ thành một **vector** đa chiều chứa các chiều đặc trưng phong phú.

<LinearProjectionDemo />

---

## 2. Bước hai: Dịch chéo loài (Projection)

Lúc này, mặc dù hình ảnh đã được chuyển đổi thành một chuỗi "từ thị giác" liên tục một chiều, nhưng chuỗi này đối với LLM cuối cùng vẫn là một đống mã hỗn loạn không thể đọc được.

Tại sao không đọc được? Bởi vì **không gian đặc trưng khác nhau** (tức là chúng nói các ngôn ngữ khác nhau).
Bộ mã hóa thị giác (như ViT) trích xuất **đặc trưng pixel không gian** (ví dụ, nó chỉ có thể cho bạn biết "đây là một thứ được tạo thành từ nhiều đường cong màu đen", "đây là một vùng màu đỏ lớn"); trong khi LLM bên trong hiểu **đặc trưng ngữ nghĩa sâu sắc** (ví dụ, các khái niệm như "mèo", "cây", "nguy hiểm").

Giữa hai hệ thống ngôn ngữ hoàn toàn khác biệt này, chúng ta cần xây dựng một cây cầu, đó chính là phiên dịch viên đa phương thức của chúng ta: **Projector (Bộ chiếu/Bộ điều hợp)**.

### 2.1 Vai trò của phiên dịch viên (Latent Space Alignment)

Bản chất học thuật của Projector là thực hiện **sự căn chỉnh không gian ẩn đặc trưng (Latent Space Alignment)**. Điều này giống như một phiên dịch viên đồng thời trong đời thực:

-   **Đầu vào (Source)**: "Đặc trưng thị giác" do ViT tạo ra (tập trung vào các biểu diễn đặc trưng đa chiều liên tục như hình học, màu sắc, quy luật kết cấu).
-   **Xử lý (Translation)**: Projector sử dụng một cấu trúc mạng nơ-ron (có thể là vài lớp biến đổi tuyến tính đơn giản, hoặc các lớp attention phức tạp) để tìm ra mối quan hệ toán học giữa hai ngôn ngữ trong quá trình này.
-   **Đầu ra (Target)**: Tạo ra "ngôn ngữ LLM" hoàn toàn phù hợp với khẩu vị và kỳ vọng của LLM (Token nhúng văn bản tương đương được chuyển đổi từ đặc trưng hình ảnh, làm cho hình ảnh có ý nghĩa có thể đối thoại).

Thông qua lớp dịch và lọc này, mô hình lớn sẽ ngạc nhiên phát hiện ra: "Ồ? Chuỗi số được truyền vào này, chẳng phải là sự kết hợp của những từ mang tính mô tả mà mình thường đọc sao!", từ đó xử lý đặc trưng hình ảnh và ngôn ngữ tự nhiên một cách hợp lý.

<ProjectorDemo />

### 2.2 Các trường phái dịch thuật khác nhau

Để quá trình "dịch thuật" căn chỉnh đặc trưng này diễn ra nhanh hơn và chính xác hơn, giới học thuật và công nghiệp đã phát triển một số giải pháp thiết kế kết nối phần cứng mang tính đại diện cao:

1.  **Trường phái dịch thẳng (Linear Projection)**:
    -   **Cách làm**: Cực kỳ đơn giản và trực tiếp, chỉ sử dụng một hoặc vài chục lớp mạng đa lớp (MLP / lớp chiếu tuyến tính) để thực hiện biến đổi ma trận toán học trực tiếp.
    -   **Đặc điểm**: **Tổn thất thông tin cực thấp, giữ nguyên chi tiết hình ảnh gốc**; nhưng nhược điểm là truyền toàn bộ hàng trăm đến hàng nghìn visual Token đã cắt cho mô hình ngôn ngữ, dẫn đến tăng vọt khối lượng tính toán sau này.
    -   **Đại diện**: Dòng LLaVA.

2.  **Trường phái dịch ý (Q-Former / Resampler)**:
    -   **Cách làm**: Không truyền nguyên bản, mà đưa vào giữa một "mạng trinh sát nhỏ" có khả năng tóm tắt trừu tượng. Đại lý trung gian này trước tiên nhanh chóng hiểu toàn bộ hình ảnh, sau đó tinh lọc ra vài chục điểm cốt lõi được cô đọng cao.
    -   **Đặc điểm**: **Thông tin được tinh gọn và cô đọng cao, ít Token, tiết kiệm đáng kể hiệu suất tính toán của LLM**; nhược điểm là có thể bỏ qua những manh mối quan sát cực kỳ nhỏ ở rìa hình ảnh gốc trong quá trình tinh lọc.
    -   **Đại diện**: BLIP-2, Gemini (một phần cơ chế tương tự).

3.  **Trường phái dung hòa (C-Abstractor / Pooling)**:
    -   **Cách làm**: Sử dụng pooling tích chập hoặc tái cấu trúc vùng cục bộ, nén và đóng gói các khối pixel $2 \times 2$ hoặc lớn hơn liền kề thành một đơn vị biểu đạt hoàn chỉnh.
    -   **Đặc điểm**: Vừa nén hợp lý giới hạn độ dài của Token, vừa giữ lại một phần cảm giác cục bộ và không gian phụ thuộc lẫn nhau.
    -   **Đại diện**: Qwen-VL-Max.

---

## 3. Bước ba: Hợp thể (The Architecture)

Có các bộ phận, có tiêu chuẩn kết nối, bây giờ chúng ta hãy xem nó hoàn thành việc trang bị toàn thân như thế nào. Các mô hình ngôn ngữ thị giác đa phương thức (Vision-Language Model) chính thống về cơ bản đều tuân theo **kiến trúc "ba giai đoạn"** thống nhất.

### 3.1 Cấu trúc cơ thể của VLM

<ModelArchitectureComparisonDemo />

Một thực thể VLM theo mô hình điển hình chủ yếu bao gồm ba phần sau đây hoạt động phối hợp:

1.  **"Đôi mắt" nhận biết đặc trưng (Vision Encoder - Bộ mã hóa thị giác)**:
    -   **Chức năng**: Là cửa ngõ đầu tiên của đầu vào hình ảnh, chịu trách nhiệm xem hình ảnh và trừu tượng hóa các đặc trưng thị giác đa chiều.
    -   **Lựa chọn**: Hầu hết các nhà sản xuất sẽ không huấn luyện đôi mắt từ đầu, mà trực tiếp sử dụng các thành phần trưởng thành đã được huấn luyện trước trên hàng trăm triệu cặp dữ liệu "hình ảnh-văn bản" (như tháp thị giác của mô hình CLIP của OpenAI, hoặc mô hình SigLIP của Google).
    -   *Ví von hình ảnh: Đây chính là vùng tế bào cảm quang võng mạc chuyên biệt hóa cao của cơ thể sinh vật.*

2.  **"Dây thần kinh thị giác" chuyển đổi tín hiệu (Projector - Bộ chiếu phương thức)**:
    -   **Chức năng**: Kết nối bộ mã hóa và nền tảng ngôn ngữ, chịu trách nhiệm nén chiều tín hiệu, kết nối và dịch ngữ nghĩa đa phương thức.
    -   **Lựa chọn**: Đây là **trọng tâm của quá trình huấn luyện tiếp theo** của toàn bộ hệ thống đa phương thức. Số lượng tham số của nó thường không lớn (so với LLM), nhưng nó quyết định liệu "văn bản" và "hình ảnh" có thể hiểu nhau hay không.
    -   *Ví von hình ảnh: Nó giống như trung tâm thần kinh thị giác chịu trách nhiệm chuyển đổi và truyền tín hiệu điện đến vỏ não.*

3.  **"Bộ não" động cơ nhận thức (LLM Backbone - Nền tảng mô hình ngôn ngữ)**:
    -   **Chức năng**: Đảm nhận công việc quan sát cuối cùng, gọi kiến thức thông thường, suy luận logic sâu sắc và tạo ra phản hồi giống người.
    -   **Lựa chọn**: Thường sử dụng các mô hình ngôn ngữ lớn mã nguồn mở thông minh nhất trong ngành làm điểm gắn kết (như Qwen, Llama 3, Vicuna, v.v.).
    -   *Ví von hình ảnh: Đây là trung tâm ngôn ngữ và ra quyết định của bộ não với kho kiến thức thế giới, nó đưa ra phán đoán tư duy cấp cao dựa trên tín hiệu đã được xử lý từ dây thần kinh thị giác.*

---

## 4. Nó học cách nhìn hình ảnh như thế nào? (Training)

Tốt, bây giờ các bộ phận cơ thể đã được ghép lại với nhau. Nhưng trước khi chính thức "tiếp khách", VLM vừa được lắp ráp thực tế đang ở trạng thái "mù lòa và hỗn loạn" giống như trẻ sơ sinh – bởi vì dây thần kinh thị giác mới (Projector) là một tờ giấy trắng, bên trong toàn là những giá trị ngẫu nhiên vô nghĩa.

Để con quái vật được ghép nối này có khả năng nhìn hình ảnh và nói chuyện, giới khoa học đã tổng kết một bộ **"quy tắc huấn luyện hai giai đoạn (Two-Stage Training)"** hiệu quả.

### Giai đoạn một: Nhận diện vật thể (Feature Alignment – Huấn luyện trước nhận diện vật thể)

Giai đoạn này, nhiệm vụ chính là để Projector ngẫu nhiên thiết lập mối quan hệ ánh xạ đa phương thức ban đầu. Quá trình này rất giống việc dạy trẻ sơ sinh dùng "thẻ nhận thức" để ghi nhớ từ vựng một cách cưỡng bức.

-   **Cho nó xem (đầu vào huấn luyện)**: Hàng loạt (thường là hàng trăm triệu) cặp hình ảnh-văn bản cực kỳ đơn giản chứa một chủ thể nổi bật duy nhất (ví dụ: ảnh "mèo" trên nền trắng).
-   **Nói cho nó biết (đầu ra mục tiêu)**: Kèm theo các từ khóa ngắn gọn ("một con mèo vàng").
-   **Mục tiêu tối ưu hóa**: Buộc Projector học cách thông qua biến đổi ma trận, làm cho đặc trưng thị giác tương ứng của con mèo (sau khi được dịch) và vector Token "mèo" trong ngôn ngữ tự nhiên trùng khớp và căn chỉnh càng nhiều càng tốt.
-   **Trạng thái kiểm soát tham số (Freeze Strategy)**: Để tránh làm hỏng trí tuệ của mô hình gốc, trong giai đoạn này, các nhà nghiên cứu sẽ **đóng băng (Freeze)** hàng chục đến hàng trăm tỷ tham số của "mắt" (ViT) và "não" (LLM) một cách nghiêm ngặt, **chỉ kích hoạt huấn luyện vài triệu tham số của chính "dây thần kinh thị giác" (Projector)**.

<FeatureAlignmentDemo />

### Giai đoạn hai: Đối thoại (Visual Instruction Tuning – Thực hành đối thoại)

Nếu giai đoạn đầu tiên chỉ khiến mô hình trở thành một cỗ máy nhận diện từ như đọc danh sách, thì nhiệm vụ của giai đoạn thứ hai là kích thích trí thông minh cấp cao của nó, để nó thực sự có thể giải đáp các chỉ dẫn phức tạp kết hợp hình ảnh và văn bản của con người dựa trên ngữ cảnh.

-   **Cho nó xem (đầu vào huấn luyện)**: Các cặp hỏi đáp huấn luyện chất lượng cao được thiết kế cẩn thận. Ví dụ, cung cấp một bức ảnh toàn cảnh giao thông thành phố phức tạp.
-   **Yêu cầu nó trả lời (đầu ra mục tiêu)**: Người dùng hỏi: "`<img>` Người đàn ông đi xe đạp màu trắng ở góc dưới bên trái có đội mũ bảo hiểm không?" Trợ lý trả lời: "Không, anh ấy không đội gì trên đầu, đây là hành vi rất nguy hiểm trong thành phố."
-   **Mục tiêu tối ưu hóa**: Để mô hình lớn không chỉ có thể tiếp nhận các manh mối thị giác, mà còn có thể kết hợp với kiến thức thông thường tích lũy từ trước, hòa nhập hoàn toàn logic văn bản với biểu diễn đa phương thức và đưa ra suy luận.
-   **Trạng thái kiểm soát tham số (Freeze Strategy)**: Lúc này, dây thần kinh thị giác đã cơ bản được điều chỉnh. Trong giai đoạn tinh chỉnh này, thông thường sẽ tiếp tục đóng băng một phần trọng số lớp dưới của bộ mã hóa thị giác, đồng thời **hoàn toàn giải phóng và kích hoạt LLM và Projector** (hoặc sử dụng cấu hình LoRA), để thực hiện điều chỉnh lan truyền ngược quy mô lớn toàn cầu.

<VLMInferenceDemo />

---

## 5. Nâng cao: Nhìn rõ hơn (Advanced Tricks)

Mặc dù kiến trúc trên đã hỗ trợ mô hình đa phương thức ban đầu, nhưng các mô hình VLM thế hệ đầu tiên tồn tại một nhược điểm cơ bản rất đau đầu – **cận thị (thị lực bẩm sinh kém)**.

Các bộ mã hóa thị giác ViT đời đầu, do lý do thiết kế lịch sử, bẩm sinh chỉ có thể xử lý các hình ảnh nhỏ với độ phân giải cực thấp như $224 \times 224$ hoặc $336 \times 336$. Điều này giống như việc cố gắng quan sát thế giới thông qua một camera cổ điển vài trăm nghìn pixel mờ, chất lượng thấp; các chi tiết nhỏ hơn như biển báo văn bản trong hình ảnh sẽ hoàn toàn bị nhòe thành một đống pixel, dù bộ não có thông minh đến mấy cũng "khó mà làm nên cơm cháo" (thiếu nguyên liệu).

Để khắc phục căn bệnh "mờ mắt", các nhà sản xuất mô hình tiên tiến (như nhóm Qwen-VL, LLaVA-NeXT, v.v.) đã sử dụng một số kỹ thuật kỹ thuật rất tinh xảo:

### 5.1 Bố cục cắt lát độ phân giải cao động (Dynamic High-Resolution Mapping)

Nếu trực tiếp nhập hình ảnh lớn sẽ dẫn đến tràn bộ nhớ GPU, còn thu nhỏ một cách thô bạo lại làm mất hết chi tiết, vậy làm thế nào để phá vỡ bế tắc? Giải pháp hiện tại là: **chiến lược "cận cảnh cục bộ + toàn cảnh tổng thể" với hai góc nhìn**.

1.  **Tổng quan toàn bộ**: Đầu tiên, thu nhỏ trực tiếp hình ảnh gốc độ phân giải cao khổng lồ xuống $336 \times 336$, rồi đưa cho "mắt" xem. Điều này giúp mô hình nắm bắt **cấu trúc bố cục vĩ mô tổng thể** của hình ảnh (bầu trời ở đâu? mặt đất ở đâu?).
2.  **Cắt lát và phóng to**: Cắt hình ảnh gốc độ phân giải cao thành hàng chục khối cắt lát cận cảnh cục bộ độc lập, không mất dữ liệu, kích thước $336 \times 336$ (Slice).
3.  **Kiểm tra từng phần và ghép lại không gian**: Để bộ máy thị giác lần lượt dùng kính lúp quét qua hàng chục mặt cắt không mất dữ liệu này để thu thập chi tiết độ phân giải cao. Sau đó, Projector sẽ ghép các khối chi tiết này lại với ngữ cảnh tổng thể ban đầu như một trò chơi xếp hình.

Cách làm này giống như bạn dùng điện thoại chụp toàn cảnh một tờ báo (để xem bố cục trang), sau đó lại dí điện thoại sát tờ báo và liên tục chụp hàng chục bức ảnh cận cảnh từng đoạn.

### 5.2 Thay một đôi mắt lớn bẩm sinh (Scaling the Vision Encoder)

Một cách làm khác thuần túy thể hiện vẻ đẹp bạo lực là: vì đôi mắt ban đầu bẩm sinh có khuyết tật gen, vậy thì tôi sẽ luyện chế lại từ đầu một đôi mắt siêu việt nhất.

Với mô hình mã nguồn mở xuất sắc của Trung Quốc là **InternVL** làm đại diện kinh điển, nó đã từ bỏ các mô hình thị giác quy mô nhỏ thường dùng, mà trực tiếp tiêu tốn lượng lớn tài nguyên để huấn luyện riêng một nền tảng bộ mã hóa thị giác tiền xử lý siêu khổng lồ với số lượng tham số lên đến hàng tỷ (ví dụ: InternViT-6B với 6 tỷ tham số) từ dưới lên.
Nhờ khả năng hấp thụ dữ liệu cực mạnh, nó sinh ra đã là một "kính viễn vọng không gian Hubble" hỗ trợ đầu vào độ phân giải cao liền mạch. Thiết kế này đã giảm đáng kể chi phí kỹ thuật phức tạp và rủi ro sai lệch đặc trưng do hệ thống phải cắt và ghép hình ảnh, trực tiếp đạt được khả năng nhận thức thị giác độ nét cao "nhìn rõ mọi thứ".

---

## 6. Tóm tắt

Mô hình đa phương thức lớn (VLM) không có phép thuật gì. Nó chỉ làm một việc:

**Dịch "hình ảnh" - một ngoại ngữ, thành "văn bản" - tiếng mẹ đẻ, rồi đưa cho LLM.**

Chỉ cần hiểu được điều này, bạn đã hiểu tất cả về VLM.

---

## 7. Bảng tra cứu thuật ngữ (Glossary)

| Tên gọi        | Tên đầy đủ             | Giải thích                                                       |
| :------------ | :-------------------- | :--------------------------------------------------------- |
| **VLM**       | Vision-Language Model | **Mô hình đa phương thức lớn**. GPT có thể hiểu hình ảnh.   |
| **ViT**       | Vision Transformer    | **Mô hình thị giác**. "Đôi mắt" của VLM, chịu trách nhiệm biến pixel thành vector. |
| **Patch**     | -                     | **Khối hình ảnh**. Các ô vuông nhỏ được cắt từ hình ảnh, tương đương với "từ thị giác". |
| **Projector** | -                     | **Bộ chiếu/Phiên dịch viên**. Cây cầu nối giữa mắt và não.  |
| **Alignment** | -                     | **Căn chỉnh**. Làm cho đặc trưng hình ảnh và đặc trưng văn bản "hiểu nhau" trong cùng một không gian. |
