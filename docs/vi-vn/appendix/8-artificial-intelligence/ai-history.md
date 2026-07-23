---
title: 'Lịch sử AI: Từ logic ký hiệu đến các mô hình hàng trăm tỷ tham số'
description: 'AI phát triển 70 năm, trải qua ba làn sóng, hai mùa đông, cuối cùng hội tụ thành kỷ nguyên mô hình lớn ngày nay.'
---

# Lịch sử AI: Từ logic ký hiệu đến các mô hình hàng trăm tỷ tham số

AI phát triển 70 năm, trải qua **ba làn sóng, hai mùa đông**, từ suy luận logic của chủ nghĩa ký hiệu, đến mạng nơ-ron của chủ nghĩa kết nối, rồi đến học tăng cường của chủ nghĩa hành vi, cuối cùng hội tụ thành kỷ nguyên mô hình lớn ngày nay. Hiểu lịch sử AI có thể giúp chúng ta nhìn rõ nguồn gốc bản chất "trí tuệ" của các mô hình lớn hiện nay.

<AiEvolutionDemo />
<DiscriminativeVsGenerativeDemo />

---

## I. Nền tảng lý thuyết và sự ra đời của chủ nghĩa ký hiệu (1940s-1950s)

Trước khi máy tính thực sự phổ biến, những người tiên phong đã bắt đầu suy nghĩ về việc "liệu máy móc có thể suy nghĩ như con người hay không". Nghiên cứu trong giai đoạn này chủ yếu tập trung vào mô hình toán học của thần kinh não bộ, thảo luận về lý thuyết tính toán và tự động hóa suy luận logic. Hội nghị Dartmouth năm 1956 đã chính thức công bố sự ra đời của "Trí tuệ nhân tạo" (Artificial Intelligence) như một ngành khoa học độc lập.

<FoundationDemo />

### 1.1 Các lý thuyết cốt lõi và sự kiện cột mốc
 
- **Ý tưởng ban đầu về mạng nơ-ron (1943)**: Nhà sinh lý học thần kinh Warren McCulloch và nhà toán học Walter Pitts đã đề xuất **mô hình nơ-ron MP**. Họ lần đầu tiên cố gắng trừu tượng hóa cơ chế hoạt động của nơ-ron não người bằng các công thức toán học đơn giản, chứng minh rằng "mạng nơ-ron có thể tính toán được", điều này đã trở thành tổ tiên của tất cả các mạng sâu ngày nay.
- **Câu hỏi cuối cùng của Turing (1950)**: Cha đẻ của khoa học máy tính Alan Turing đã xuất bản một bài báo thay đổi lịch sử mang tên "Máy tính và Trí tuệ", đề xuất **Phép thử Turing** nổi tiếng. Ông tránh xa cuộc tranh luận triết học về "trí tuệ là gì" và đưa ra một tiêu chuẩn thực tế: nếu một cỗ máy trong cuộc đối thoại có thể khiến con người không thể phân biệt được đó là người hay máy, nó có trí tuệ.
- **Sự thành lập chính thức của ngành (1956)**: Tại hội thảo mùa hè ở Dartmouth, các học giả trẻ như John McCarthy, Marvin Minsky đã cùng nhau tụ họp. McCarthy lần đầu tiên sử dụng thuật ngữ "Artificial Intelligence" trong đề xuất của mình, và năm này được gọi là năm đầu tiên của AI.

::: tip Sự trỗi dậy của Chủ nghĩa ký hiệu (Symbolism)
Trong nghiên cứu AI sơ khai, **chủ nghĩa ký hiệu** chiếm ưu thế tuyệt đối. Do máy tính thời đó chủ yếu hoạt động dựa trên mạch logic, các học giả tự nhiên cho rằng: **bản chất của trí tuệ là suy luận ký hiệu**.
Chỉ cần chúng ta biến kiến thức thế giới thành các ký hiệu mà máy tính có thể hiểu (như khái niệm, quy tắc), sau đó sử dụng các công cụ suy luận logic (như quy tắc IF-THEN) để xử lý các ký hiệu này, máy móc sẽ có thể suy nghĩ như con người. Đây là một con đường **từ trên xuống**, phụ thuộc rất nhiều vào đầu vào kiến thức từ chuyên gia con người.
:::

---

## II. Thời kỳ hoàng kim của chủ nghĩa ký hiệu và làn sóng AI đầu tiên (1960s-1970s)

Trong vài thập kỷ đầu sau khi ra đời, AI đã bước vào một thời kỳ hoàng kim với sự lạc quan mù quáng. Các nhà nghiên cứu tin rằng, vì máy móc đã có thể chứng minh các định lý toán học, việc viết ra các chương trình có thể giải quyết mọi vấn đề của con người chỉ còn là vấn đề thời gian.

### 2.1 Thời kỳ huy hoàng của các hệ chuyên gia

Đỉnh cao của chủ nghĩa ký hiệu là **hệ chuyên gia (Expert Systems)**. Bằng cách nhập "quy tắc kinh nghiệm (Rule)" của các chuyên gia hàng đầu trong từng lĩnh vực vào máy tính, hệ thống có thể thực hiện chẩn đoán hoặc ra quyết định ở cấp độ cao trong một số lĩnh vực chuyên biệt.

| Hệ chuyên gia | Năm ra đời | Ý nghĩa lịch sử và giá trị thực tế |
| --- | --- | --- |
| **Dendral** | 1965 | **Hệ chuyên gia đầu tiên**, có khả năng suy luận cấu trúc phân tử hóa học dựa trên dữ liệu phổ khối, hiệu suất ngang ngửa các chuyên gia hóa học con người. |
| **MYCIN** | 1977 | Được sử dụng để chẩn đoán nhiễm trùng máu và đề xuất kháng sinh, độ chính xác lên tới 69%, thậm chí vượt qua nhiều bác sĩ không chuyên thời bấy giờ. |
| **XCON** | 1980 | Hệ chuyên gia thương mại thành công nhất thời kỳ đầu, được sử dụng để giúp Công ty Thiết bị Kỹ thuật số (DEC) tự động cấu hình hệ thống máy tính theo yêu cầu của khách hàng, tiết kiệm cho công ty 40 triệu USD mỗi năm. |

Tuy nhiên, đằng sau vẻ hào nhoáng của các hệ chuyên gia là những rào cản không thể vượt qua.

### 2.2 Mùa đông AI đầu tiên (1974-1980)

Theo thời gian, người ta nhận ra con đường "biến kiến thức con người thành quy tắc" ngày càng trở nên hẹp hòi. Ba hạn chế chết người của chủ nghĩa ký hiệu cuối cùng đã dẫn đến việc rút toàn bộ kinh phí nghiên cứu:

**Nút thắt cổ chai trong thu thập kiến thức**: Một số kiến thức con người cũng không thể diễn tả rõ ràng (ví dụ: làm thế nào để nhận ra một con mèo), điều này được gọi là "Nghịch lý Polanyi". Hệ chuyên gia chỉ có thể mã hóa cứng những quy tắc có thể diễn đạt rõ ràng, không thể tự động học.

**Bùng nổ tổ hợp & vấn đề dễ vỡ**: Có quá nhiều tình huống thực tế, việc liệt kê tất cả là cực kỳ khó khăn; và thiếu kiến thức thông thường, chỉ cần hơi lệch khỏi kho quy tắc là hệ thống sẽ sụp đổ ngay lập tức.

**Thiếu năng lực tính toán & gián đoạn kinh phí**: Năng lực tính toán phần cứng thời đó hoàn toàn không thể hỗ trợ suy luận logic bùng nổ, dẫn đến việc DARPA cắt giảm mạnh kinh phí nghiên cứu và phát triển.

---

## III. Hệ chuyên gia (chương trình dịch kinh nghiệm con người thành mã) và làn sóng AI thứ hai (những năm 1980)

Đến những năm 80, với sự phổ biến của máy tính siêu nhỏ và máy LISP chuyên dụng, các hệ chuyên gia một lần nữa được giới kinh doanh săn đón. Chính phủ Nhật Bản thậm chí còn đưa ra "Kế hoạch Máy tính Thế hệ thứ Năm" đầy tham vọng, cố gắng tạo ra những cỗ máy thông minh có thể hiểu ngôn ngữ tự nhiên, gây ra làn sóng đầu tư hoảng loạn trên toàn cầu.

### 3.1 Sự bùng nổ và sụp đổ của các ứng dụng thương mại

Trong kỷ nguyên này, hầu hết các công ty đa quốc gia lớn đều đang phát triển **hệ chuyên gia (một loại chương trình dịch kinh nghiệm của các chuyên gia con người thành hàng ngàn dòng mã IF-THEN)** của riêng mình. Tuy nhiên, việc bảo trì các hệ thống này trở nên cực kỳ khó khăn. Sau khi kho quy tắc vượt quá vài chục nghìn, việc sửa đổi một quy tắc mới thường dẫn đến xung đột với mười quy tắc cũ khác. Với sự bùng nổ hiệu suất của máy tính cá nhân (PC) đa năng vào cuối những năm 80, các máy AI chuyên dụng đắt đỏ và khép kín trở nên hoàn toàn không có khả năng cạnh tranh.

::: warning ❄️ Mùa đông AI thứ hai (1987-1993)
Năm 1987, thị trường phần cứng AI sụp đổ hoàn toàn. "Kế hoạch Máy tính Thế hệ thứ Năm" cuối cùng bị bỏ dở vì quá xa rời kiến trúc phần cứng thực tế. Các doanh nghiệp đã đổ tiền vào các hệ chuyên gia nhưng không thu lại được gì, nghiên cứu AI lại rơi xuống đáy, thậm chí từ "trí tuệ nhân tạo" còn trở thành một từ mang ý nghĩa tiêu cực trong giới học thuật, ám chỉ việc lừa đảo xin kinh phí.
:::

### 3.2 Chủ nghĩa kết nối ẩn mình trong bóng tối

Trong hai lần thăng trầm này, thực ra còn tồn tại một hướng tư duy hoàn toàn khác – **chủ nghĩa kết nối (Connectionism)**, tức là **mạng nơ-ron** mà chúng ta nói đến ngày nay.

<PerceptronDemo />

Chủ nghĩa kết nối đã được Frank Rosenblatt đề xuất dưới dạng **Perceptron** từ năm 1958. Nó mô phỏng cách não bộ học bằng cách điều chỉnh trọng số kết nối giữa các nơ-ron. Thay vì dạy máy móc những "quy tắc" rõ ràng, tốt hơn là cho máy xem nhiều "ví dụ" và để nó tự tổng hợp. Tuy nhiên, năm 1969, Minsky trong cuốn sách "Perceptrons" đã chứng minh bằng toán học chặt chẽ những hạn chế của mạng một lớp thời đó (không thể giải quyết vấn đề XOR đơn giản). Điều này khiến chủ nghĩa kết nối bị "ngồi ghế dự bị" trong suốt thời kỳ hoàng kim của chủ nghĩa ký hiệu. Cho đến khi bánh xe lịch sử tiến đến những năm 90.

---

## IV. Sự trỗi dậy của Machine Learning và sự hồi sinh của chủ nghĩa kết nối (1990s-2000s)

Sau khi bước vào những năm 90, lĩnh vực AI đã chứng kiến một sự chuyển hướng thực dụng quan trọng. Mọi người không còn ngày ngày nói về cách đạt được "trí tuệ ma thuật như con người" nữa, mà thay vào đó tập trung vào việc sử dụng **các phương pháp thống kê dữ liệu chặt chẽ** để giải quyết các vấn đề phân loại và dự đoán trong đời sống thực. Đây chính là sự trỗi dậy của **Machine Learning** truyền thống.

### 4.1 Từ quy tắc cứng nhắc đến "tìm kiếm ranh giới toán học"

Năm 1997, mặc dù "Deep Blue" của IBM đã đánh bại nhà vô địch cờ vua thế giới Garry Kasparov, mang lại vinh quang lẫy lừng cho chủ nghĩa ký hiệu, nhưng giới học thuật ngay lập tức nhận ra rằng đây chỉ là một chiến thắng của "năng lực tính toán + mã hóa cứng khổng lồ", Deep Blue không thực sự hiểu thế nào là chơi cờ.

Đồng thời, các thuật toán Machine Learning cổ điển như **máy vector hỗ trợ (SVM)**, cây quyết định, rừng ngẫu nhiên đã nổi lên mạnh mẽ, trở thành xu hướng chủ đạo tuyệt đối trong hơn một thập kỷ tiếp theo.

Nếu các hệ chuyên gia trước đây dạy máy tính rằng: "Nếu email chứa 'trúng thưởng', thì đó là thư rác", thì **tư duy của Machine Learning là: con người trước tiên thiết lập một số đặc trưng cốt lõi (Feature Engineering)**, ví dụ như "độ dài email", "tần suất từ ngữ đặc biệt", "độ tin cậy của người gửi", sau đó nhập hàng vạn email đã được gắn nhãn vào máy tính. Trong không gian đa chiều này, **máy vector hỗ trợ (SVM)** giống như một nhà toán học cầm thước, nó sẽ sử dụng các hàm kernel chặt chẽ để suy luận, vẽ ra một "đường phân cách toán học rộng nhất, an toàn nhất" giữa email bình thường và email rác.

Mặc dù SVM đã thành công lớn trong nhiều tác vụ, nhưng nó có một điểm yếu chí mạng: **Feature Engineering phụ thuộc rất nhiều vào con người.** Ví dụ, để nhận diện một bức ảnh mèo, các nhà khoa học con người phải dạy máy "trước tiên trích xuất các cạnh", "sau đó tìm kiếm đôi tai hình tam giác", bản thân máy không thể tự tìm ra hình dáng con mèo! Điều này khiến giới hạn năng lực của mô hình bị khóa chặt bởi nhận thức của con người.

### 4.2 Backpropagation đưa mạng nơ-ron trở lại ánh sáng

Nền tảng thực sự của Deep Learning đã được đặt trong giai đoạn này:

<BackpropagationDemo />

Trong giai đoạn ẩn mình này, Geoffrey Hinton và các cộng sự đã làm rõ hơn giá trị cốt lõi của **Backpropagation**: khi một mạng nơ-ron đa lớp đưa ra dự đoán sai, nó có thể đẩy ngược lỗi này từng lớp một, giống như sóng nước, để nói với từng nơ-ron cũ ở lớp ẩn: "Bạn phải chịu trách nhiệm bao nhiêu trong lỗi này, lần sau hãy sửa ngay!" Điều này cuối cùng đã phá vỡ những hạn chế đối với mạng nơ-ron trong những năm 60, giúp các mạng có lớp ẩn trở nên khả thi. Tuy nhiên, do dữ liệu quá ít và phần cứng quá yếu (thậm chí không có card đồ họa tốt), mạng nơ-ron vẫn chưa thể hoàn toàn đánh bại các mô hình Machine Learning truyền thống như SVM. Cho đến khi **ba điểm bùng nổ** cùng hội tụ.

---

## V. Cuộc cách mạng Deep Learning và sự thống trị của chủ nghĩa kết nối (những năm 2010)

Vào những năm 2010, với sự **trưởng thành của Big Data (như dự án ImageNet)**, **sự bùng nổ năng lực tính toán (GPU được ứng dụng rộng rãi trong tính toán song song)** và **những cải tiến về thuật toán (giải quyết vấn đề gradient biến mất)**, "Deep Learning" đã mở ra làn sóng AI thứ ba một cách mạnh mẽ.

**Sự khác biệt bản chất giữa Deep Learning và Machine Learning truyền thống là gì? Dấu hiệu chính là: tự động trích xuất đặc trưng (Representation Learning).** Chỉ cần số lớp mạng đủ sâu (vài chục đến hàng trăm lớp), mạng nơ-ron có thể trực tiếp tiếp nhận các pixel thô nhất, lớp dưới cùng của nó tự học cách nhận diện đường nét, lớp giữa học cách nhận diện kết cấu lông, và lớp cao hơn trực tiếp nhận ra đây là một con "mèo". Trong cuộc cách mạng này, con người kiêu ngạo cuối cùng đã trao quyền, để mạng lưới tự tìm kiếm các đặc trưng hình ảnh, giọng nói và văn bản quan trọng nhất.

### 5.1 Đột phá toàn diện về hình ảnh và thi đấu

Năm 2012, **AlexNet (mạng nơ-ron tích chập CNN kinh điển)** do nhóm của Hinton phát triển đã tham gia cuộc thi phân loại hình ảnh ImageNet nổi tiếng. Khi những người khác vẫn đang vất vả sử dụng các phương pháp truyền thống để trích xuất đặc trưng thị giác thủ công, AlexNet đã trực tiếp "giáng đòn" giảm chiều dữ liệu một cách mạnh mẽ, giảm tỷ lệ lỗi từ 26% xuống còn 15.3% trong tích tắc, gây chấn động toàn bộ giới học thuật thị giác máy tính truyền thống. Nhờ sức mạnh thống trị tuyệt đối này, trong những năm sau đó, hầu như không có bất kỳ bài báo nào không sử dụng Deep Learning được chấp nhận tại các hội nghị hàng đầu!

Trong những năm tiếp theo, công nghệ AI đã phát triển với tốc độ chóng mặt từng phút từng giây:

<NeuralNetworkVisualizationDemo />

| Năm đột phá | Thành tựu mang tính biểu tượng | Ảnh hưởng sâu rộng |
| --- | --- | --- |
| **2014** | **GAN (Generative Adversarial Network)** được đề xuất | Hai mạng "đối đầu" (một mạng tạo giả, một mạng phát hiện giả), giúp AI bắt đầu có khả năng tạo ra những hình ảnh tuyệt đẹp và chân thực. |
| **2015** | **ResNet (Residual Network)** ra đời | Đổi mới bằng cách giới thiệu cấu trúc "đường tắt", giải quyết vấn đề mạng không thể huấn luyện bình thường khi được làm sâu hơn, cho phép mạng nơ-ron có thể xếp chồng lên nhau hàng trăm, hàng nghìn lớp. |
| **2016** | **AlphaGo** đánh bại Lee Sedol | Đỉnh cao của sự kết hợp giữa Deep Learning và **Reinforcement Learning**, phá vỡ lời tiên đoán "máy móc sẽ không bao giờ đánh cờ vây thắng con người", gây chấn động toàn cầu. |

::: tip Chủ nghĩa hành vi (Behaviorism) và Reinforcement Learning
AlphaGo đại diện cho chiến thắng của một trường phái khác – **chủ nghĩa hành vi**. Nó cho rằng trí tuệ bắt nguồn từ sự tương tác động giữa chủ thể và môi trường, giống như việc huấn luyện một chú chó ngồi xuống: làm đúng thì được thưởng, làm sai thì bị phạt. Thông qua việc liên tục tự thử và sai, đối đầu trong môi trường ảo khổng lồ, AlphaGo đã tổng kết ra những chiến lược mà ngay cả những kỳ thủ hàng đầu của con người cũng chưa từng phát hiện ra.
:::

### 5.2 Transformer: Cái nôi của các mô hình lớn

Năm 2017, bánh xe định mệnh bắt đầu quay. Google đã đề xuất một kiến trúc Deep Learning hoàn toàn mới trong bài báo "Attention Is All You Need" – **Transformer**.

<AttentionMechanismDemo />

Trước đây, khi xử lý một câu (ví dụ như mô hình RNN), AI chỉ có thể xem từng từ một từ trái sang phải, và dễ quên những từ phía trước sau khi xem xong những từ phía sau. Trong khi đó, **cơ chế tự chú ý (Self-Attention)** của Transformer đã phá vỡ hoàn toàn giới hạn này: nó cho phép AI "nhìn toàn bộ" câu trong một lần, và khi thấy từ "苹果" (quả táo/Apple), nó tự động dựa vào ngữ cảnh để phán đoán xem đó là trái cây hay công ty điện thoại của Steve Jobs. Nó vốn dĩ rất phù hợp với tính toán song song, có thể xử lý lượng dữ liệu vô hạn và có thể được xếp chồng lên nhau vô cùng lớn. Khoảnh khắc này, nền móng của các mô hình lớn (LLM) đã được đặt.

---

## VI. Kỷ nguyên mô hình lớn và bình minh của trí tuệ tổng quát (2018 đến nay)

Khi Transformer gặp gỡ năng lực tính toán khổng lồ không giới hạn chi phí và lượng dữ liệu khổng lồ, mô hình phát triển AI đã thay đổi mãi mãi. Các nhà khoa học đã phát hiện ra một hiện tượng đáng kinh ngạc: kiến trúc dựa trên cơ chế tự chú ý dường như không bao giờ "no". Các mô hình Deep Learning trước đây sẽ gặp phải giới hạn về mức độ thông minh, nhưng Transformer có thể hoàn toàn tương thích với tính toán song song quy mô lớn của GPU, chỉ cần cung cấp càng nhiều dữ liệu và số lớp mạng càng sâu, hiệu suất của nó càng có thể cải thiện vô hạn.

### 6.1 Thiết lập mô hình "Pre-training + Fine-tuning": Từ chuyên gia đến đa năng

Ban đầu, khi chúng ta làm AI, đó là "một nhiệm vụ đi kèm với một mô hình nhỏ": mô hình dịch thuật được huấn luyện riêng cho dịch thuật, mô hình trò chuyện được huấn luyện riêng cho trò chuyện, giống như việc đào tạo từng "chuyên gia" chỉ biết một nghề. Nhưng đến năm 2018, với sự ra mắt của **GPT-1** của OpenAI và **BERT** của Google, tình hình đã chuyển sang mô hình mới **"sức mạnh tạo nên kỳ tích"**.

Đầu tiên là **Pre-training**, đây là 99% trí tuệ cốt lõi của các mô hình ngôn ngữ lớn. Các nhà khoa học đã đổ hàng nghìn tỷ từ ngữ từ các bài viết, tác phẩm kinh điển, mã máy tính và thậm chí cả kiến thức bách khoa toàn thư mà nhân loại để lại trên internet, tất cả vào mạng Transformer khổng lồ. Nhiệm vụ huấn luyện được giao cho nó chỉ đơn giản là **"nối chữ" (dự đoán từ tiếp theo)**.

Để có thể dự đoán cực kỳ chính xác các "từ tiếp theo" trong ngôn ngữ loài người, mô hình đã buộc phải tự nội hóa và cô đọng các quy luật vận hành của toàn bộ thế giới trong hàng trăm tỷ tham số nơ-ron của nó! Nó không chỉ nắm vững ngữ pháp chủ-vị-tân, biết "táo" là một loại trái cây màu đỏ, mà còn có thể nắm bắt logic đằng sau "Newton phát hiện ra lực hấp dẫn vì quả táo rơi". Điều này giống như một đứa trẻ không cố ý học thuộc sách ngữ pháp, nhưng nhờ đọc rộng rãi hàng triệu cuốn sách, đã tự động có khả năng hiểu thế giới phức tạp.

<GPTEvolutionDemo />

Từ GPT-2 (1.5 tỷ tham số) đến GPT-3 (175 tỷ tham số), các nhà khoa học đã kinh ngạc phát hiện ra **khả năng tự xuất hiện (Emergent Abilities)** – khi mô hình đủ lớn, sự thay đổi về lượng đã dẫn đến sự thay đổi về chất đáng sợ. Ngay cả khi không được huấn luyện có chủ đích, mô hình với số lượng tham số khổng lồ đã tự "ngộ" ra khả năng suy luận logic, viết mã và học theo ngữ cảnh. Điều này hoàn toàn không cần con người phải dạy nó thông qua mã.

### 6.2 Sự bùng nổ của Generative AI và khoảnh khắc "bùng nổ hạt nhân" của ChatGPT

Sau khi có một mô hình Pre-training khổng lồ, uyên bác và chứa đựng kiến thức thông thường của thế giới, chỉ còn một bước cuối cùng để tạo ra một trợ lý AI cá nhân hoàn hảo: **Fine-tuning**. Bởi vì mô hình Pre-training chỉ quen với việc mù quáng tiếp tục viết văn bản, nó không hiểu "chỉ thị" của người dùng và cũng không biết cách tương tác hỏi đáp một cách có quy tắc.

Tháng 11 năm 2022, OpenAI đã khéo léo giới thiệu công nghệ **RLHF (Reinforcement Learning from Human Feedback)**. Họ đã thuê một lượng lớn chuyên gia để đánh giá và sửa chữa các câu trả lời của mô hình. Điều này giống như việc đặt ra các ranh giới giao tiếp và hướng dẫn về phép tắc rõ ràng cho một thiên tài cực kỳ thông minh nhưng nói năng bạt mạng, buộc nó phải trở thành một trợ lý đối thoại ôn hòa, có trật tự và hiểu chuyện. Và thế là, **ChatGPT** ra đời.

Chỉ sau một đêm, AI không còn là món đồ chơi khô khan trong phòng thí nghiệm, mà đã trở thành bộ não thông minh đa năng trong tay mỗi người bình thường.

Sau đó, kỷ nguyên đa phương thức đầy sóng gió đã bắt đầu:
* **2023: Mở khóa đa giác quan.** Các mô hình tạo hình ảnh như Midjourney, Stable Diffusion đã định hình lại ngành công nghiệp nghệ thuật số. **GPT-4** ra mắt cùng năm đã tích hợp khả năng hiểu hình ảnh thị giác cực kỳ phức tạp và hệ thống suy luận logic liên kết dài hạn.
* **2024 bùng nổ đến nay: Mô phỏng thế giới vật lý.** Với sự ra mắt của các mô hình tạo video chân thực như Sora, cùng với sự triển khai toàn diện của các mô hình ngôn ngữ lớn giọng nói đầu cuối theo thời gian thực về sắc thái cảm xúc, AI đã nhanh chóng mở rộng từ việc chỉ xử lý văn bản sang nhận thức toàn diện về một thế giới đầy đủ bao gồm không gian ba chiều, sự chuyển động của ánh sáng và bóng tối, thậm chí cả những sắc thái cảm xúc tinh tế của giọng điệu.

---

## VII. Sự hội tụ của ba trường phái AI và triển vọng tương lai

Nhìn lại 70 năm qua, từ việc cho máy móc suy luận các định lý toán học (chủ nghĩa ký hiệu), đến việc tìm kiếm các ranh giới thống kê (Machine Learning truyền thống), đến việc chiến thắng cờ vây thông qua thử và sai (chủ nghĩa hành vi/Reinforcement Learning), rồi đến các mô hình lớn nuốt chửng dữ liệu khổng lồ để tạo ra kiến thức thông thường (hình thái cực đoan của chủ nghĩa kết nối), sự phát triển của trí tuệ nhân tạo chưa bao giờ ngừng lại.

Các mô hình lớn ngày nay dường như đã từ bỏ việc viết ra các "quy tắc" cứng nhắc do con người tạo ra (ý định ban đầu của chủ nghĩa ký hiệu), nhưng trên thực tế, chúng đã học và đóng gói những "quy tắc ẩn" sâu sắc hơn nhiều so với logic của con người trong hàng nghìn lớp mạng với vô số tham số ẩn. Phương pháp suy luận dài hạn **Chain of Thought** trong các mô hình Pre-training lớn ngày nay, chẳng phải là sự tái sinh của tư tưởng cổ điển về xác minh logic và các bước chặt chẽ mà trường phái ký hiệu từng theo đuổi trong mạng nơ-ron sao?

**Đứng trên đỉnh cao của kỷ nguyên mô hình lớn nhìn xuống, Trí tuệ nhân tạo tổng quát (AGI) trong tương lai đang tiến triển theo những con đường khám phá cực kỳ rộng lớn và sâu sắc sau đây:**

1.  **Hướng tới trung tâm thần kinh thống nhất nguyên bản (đa phương thức nguyên bản):** Các mô hình tương lai sẽ không còn là Frankenstein được ghép nối từ "mô hình văn bản + mô hình giọng nói". Kiến trúc đại diện như GPT-4o trực tiếp sử dụng cùng một siêu mạng để đồng thời tiếp nhận, cảm nhận và hiểu văn bản, hình ảnh, luồng video và giọng nói dạng sóng 3D có cảm xúc cao với độ trễ cực thấp.
2.  **Trí tuệ hiện thân (Embodied AI):** Khi "bộ não" có chỉ số IQ cực cao chỉ có thể bị giam cầm trong các trung tâm dữ liệu silicon, nó sẽ không thể xác minh sự thật từ thế giới vật lý. Thông qua sự kết hợp với Boston Dynamics và robot hình người, siêu AI được kỳ vọng sẽ mọc ra đôi tay và học được những quy luật vật lý khách quan giống hệt chúng ta thông qua quá trình va chạm và mài giũa.
3.  **Hệ thống tác nhân thông minh (Agentic AI):** Hiện tại, hầu hết các LLM vẫn dừng lại ở giai đoạn "máy tính văn bản thụ động hỏi đáp một lần". Trong khi đó, kỷ nguyên AI Agent, các mô hình lớn được trao hoàn toàn **quyền hành động độc lập**. Chỉ cần bạn đưa ra một chỉ thị ngôn ngữ tự nhiên tổng quát (ví dụ: "Giúp tôi nghiên cứu và lên kế hoạch tất cả vé máy bay, khách sạn để đi Na Uy xem cực quang vào tuần tới và tạo lịch trình"), AI Agent sẽ dựa vào bộ nhớ dài hạn, tự động phân tách thành hàng chục nhiệm vụ con, mở trình duyệt ảo để gọi các API tìm kiếm của các hãng hàng không thực tế, hoàn thành các xác minh phức tạp và thậm chí so sánh xác nhận. Chúng không còn là bức tường vọng lại thụ động chờ đợi những cú gõ, mà là một tập hợp các lực lượng lao động kỹ thuật số không mệt mỏi.

Trên hành trình công nghệ dài và xoắn ốc này, lịch sử luôn tương tự một cách đáng kinh ngạc nhưng không bao giờ lặp lại. Chúng ta đang trực tiếp trải nghiệm một lát cắt lịch sử thú vị nhất, từ "nhập quy tắc cứng nhắc vào thuật toán" đến "máy móc tự động định nghĩa các quy luật thế giới".

<AIErasComparisonDemo />
