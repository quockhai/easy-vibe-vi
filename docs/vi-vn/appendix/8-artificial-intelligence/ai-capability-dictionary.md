# Từ điển năng lực AI
Với sự ứng dụng rộng rãi của công nghệ AI tạo sinh trong các sản phẩm và kịch bản kinh doanh khác nhau, một câu hỏi ngày càng thực tế đang đặt ra trước mỗi chúng ta: **Có những năng lực AI nào có thể sử dụng?** Trong các yêu cầu cụ thể, **nên chọn năng lực nào, loại mô hình nào hay sản phẩm nào để triển khai?**

Đối mặt với sự bối rối này, cách tiếp cận trực quan nhất có lẽ là "nước đến chân mới nhảy": **khi gặp yêu cầu, hãy tìm kiếm API sản phẩm của các nhà cung cấp dịch vụ đám mây trên thị trường, hoặc các mô hình tương ứng, tìm kiếm các giải pháp thương mại trên thị trường và xử lý theo tài liệu và Demo.** Khi có nhu cầu về hình ảnh, nghĩ đến tạo ảnh; khi gặp tác vụ văn bản, tìm đến các mô hình lớn; khi liên quan đến tương tác giọng nói, nhớ đến ASR và TTS, sau đó so sánh giữa vô số API và dịch vụ. Tuy nhiên, việc ghép nối các sản phẩm rời rạc lại với nhau và việc lập kế hoạch, lựa chọn và kết hợp các năng lực AI một cách có hệ thống trong các kịch bản cấp doanh nghiệp là hai việc hoàn toàn khác nhau. Chỉ dựa vào việc tra cứu tài liệu tạm thời và kinh nghiệm sẽ dẫn đến một loạt thách thức nghiêm trọng như nhận thức năng lực rời rạc, thiết kế giải pháp tùy tiện và khó tái sử dụng năng lực.

Để giải quyết những vấn đề này, bài viết này ra đời với ý tưởng cốt lõi là "bức tranh toàn cảnh về năng lực AI". Trong cuốn sổ tay này, chúng tôi không muốn chất đống các thuật ngữ, mà muốn giúp bạn nhanh chóng làm rõ ba điều: **"Việc này có thể làm bằng năng lực AI nào? Nên chọn loại mô hình hoặc sản phẩm nào? Tiếp theo nên dùng những từ khóa nào để tìm API, dự án hoặc dịch vụ để thử?"** Thông qua việc sắp xếp có hệ thống từ các modal (văn bản, hình ảnh, âm thanh, video, 3D, đa modal) đến các lớp kiến trúc (mô hình, truy xuất, Agent, kỹ thuật nền tảng), **chúng ta có thể tìm thấy năng lực AI tương ứng, mô hình/sản phẩm đại diện, và các ứng dụng phổ biến trong kinh doanh thực tế cho từng loại nhu cầu và kịch bản điển hình**, giúp đội ngũ xây dựng hệ thống AI với chi phí thử nghiệm thấp hơn, hiệu quả ra quyết định cao hơn và khả năng tái sử dụng mạnh mẽ hơn.

Trong cuốn sổ tay này, chúng tôi sẽ giới thiệu một cách có hệ thống bản đồ năng lực AI chính thống hiện nay, từ một modal đơn lẻ đến tích hợp đa modal, từ mô hình đơn điểm đến khung tổng thể của nền tảng và kỹ thuật, kết hợp với các dạng sản phẩm và kịch bản ứng dụng phổ biến, đưa ra các tài liệu tham khảo về lựa chọn năng lực hướng tới thực hành.

> Do **nội dung khá nhiều**, bạn có thể tham khảo sổ tay khi gặp các vấn đề về lựa chọn mô hình trong quá trình thực hành; khuyến nghị bạn **dựa trên hướng ứng dụng cụ thể, để AI tham khảo sổ tay này và đưa ra các đề xuất lựa chọn mô hình, đề xuất gọi API giải pháp.**

Nếu bạn chỉ muốn tìm hiểu về các danh mục tương ứng mà không muốn xem nội dung cụ thể, bạn chỉ cần đọc nội dung của mỗi chương lớn ban đầu, ví dụ như nội dung của 1.1, 1.2, nhưng không cần xem nội dung của 1.1.1 hoặc 1.1.2.

**Khuyến nghị chỉ tham khảo các phần tương ứng hoặc chỉ duyệt qua các thư mục cấp một của sổ tay này khi cần thiết, nếu có hứng thú thì hãy duyệt toàn bộ văn bản.**

**Các bản cập nhật sau này sẽ bao gồm địa chỉ dịch vụ API mô hình được khuyến nghị thử trong mỗi phần.**

# Trong bài học này bạn sẽ học được

-   Bức tranh toàn cảnh về năng lực AI: Cách phân chia năng lực tổng thể từ văn bản, hình ảnh, âm thanh, video, 3D đến đa modal, Agent, RAG, bảo mật và kỹ thuật nền tảng.
-   Các mô hình và sản phẩm tương ứng với từng năng lực: Tìm hiểu các mô hình và dịch vụ đại diện đằng sau các năng lực chính như Embedding, OCR, ASR, TTS, VLM, RAG, v.v.
-   Phương pháp ánh xạ năng lực vào kịch bản: Nắm vững cách chuyển đổi "danh sách năng lực" thành các ứng dụng cụ thể như nội dung sản phẩm, tìm kiếm hỏi đáp, dịch vụ khách hàng thông minh, vận hành tự động, v.v.

Sau khi hoàn thành việc học cuốn sổ tay này, bạn sẽ xây dựng được nhận thức hệ thống ở cấp độ nhập môn về các năng lực AI chính thống, không chỉ biết "có những năng lực nào trên thị trường, thường đi kèm với sản phẩm nào", mà còn hiểu được vị trí và mối quan hệ của chúng trong kiến trúc tổng thể. Bạn sẽ biết cách nhanh chóng định vị năng lực cần thiết khi đối mặt với các yêu cầu kinh doanh cụ thể, đưa ra lựa chọn có căn cứ, đặt nền tảng vững chắc cho việc xây dựng hệ thống năng lực AI.

## Các tham số mô hình được đề cập trong sổ tay

Trước khi đi sâu vào bản đồ năng lực cụ thể, hãy làm rõ một khái niệm thường được nhắc đến nhưng khá trừu tượng: mô hình lớn là gì? mô hình nhỏ là gì?

**Từ góc độ học thuật**, mô hình lớn thường đề cập đến các mô hình tổng quát với hàng tỷ, hàng chục tỷ hoặc thậm chí hàng nghìn tỷ tham số, trong khi mô hình nhỏ là các mô hình chuyên biệt cho các tác vụ hoặc kịch bản cụ thể, với số lượng tham số nhỏ hơn (vài chục triệu đến vài trăm triệu).

**Từ góc độ giá cả**, nếu một API mô hình có chi phí gọi rất rẻ, ví dụ vài xu hoặc vài hào cho mỗi lần gọi, hoặc chỉ vài xu đến vài hào cho mỗi nghìn token, và không đặc biệt nhấn mạnh là mô hình lớn tổng quát, thì đó thường là một mô hình nhỏ điển hình (ví dụ: các mô hình chuyên làm OCR, ASR, phân loại hình ảnh, kiểm duyệt nội dung) hoặc một mô hình lớn phiên bản nhẹ với số lượng tham số nhỏ hơn (được nén hoặc chưng cất đặc biệt cho mục đích xử lý đồng thời cao, chi phí thấp). Nếu giá mỗi lần gọi rõ ràng cao hơn, ví dụ vài nghìn hoặc thậm chí 10 nghìn đồng trở lên cho một lần gọi, thì đó rất có thể là một mô hình lớn.

Ngoài ra, nếu tài liệu sản phẩm nhấn mạnh rõ ràng việc sử dụng LLM, mô hình lớn tổng quát, mô hình lớn đa modal, hoặc đề cập đến việc hoàn thành các tác vụ phức tạp từ đầu đến cuối (ví dụ: chatbot đối thoại đầu cuối, truy xuất hỏi đáp đầu cuối, tạo video đầu cuối), thì thường có thể coi đó là mô hình lớn.

Ngược lại, nếu trọng tâm quảng cáo nằm ở một năng lực cụ thể, ví dụ nhận dạng thẻ ngân hàng, nhận dạng hóa đơn, nhận dạng biển số xe, dự đoán tỷ lệ nhấp quảng cáo, chuyển đổi giọng nói thành văn bản, kiểm duyệt an toàn nội dung, điều đó cho thấy sản phẩm này có nhiều khả năng dựa trên một hoặc một nhóm các mô hình nhỏ.

Do đó, trong phần trình bày tiếp theo của bài viết này, chúng ta có thể đưa ra một quy ước thực tế:

-   Mô hình lớn chủ yếu đề cập đến các mô hình tổng quát, có khả năng đối thoại, có thể lập trình, và thường có giá hơi cao (bao gồm cả các phiên bản đa modal của chúng, ví dụ: GPT-4o, Gemini 1.5 Pro, Claude 3.5 Sonnet, v.v.), chúng có thể bao phủ hầu hết các tác vụ văn bản, mã và đa modal như hình ảnh, âm thanh, video.
-   Mô hình nhỏ đề cập đến các mô hình được tinh chỉnh hoặc tùy chỉnh cho một tác vụ cụ thể, thường có giá rẻ hơn, hiệu suất ổn định và kiểm soát được, nhưng phạm vi ứng dụng hẹp hơn, yêu cầu bạn chủ động kết hợp và sắp xếp trong hệ thống.

Ở đây, chúng ta có thể bổ sung một thay đổi quan trọng trong ngành: nhiều năng lực mô hình được đề cập trong sổ tay này, trước năm 2021, thực tế đều được đảm nhiệm bởi "mô hình nhỏ". Các mô hình chuyên biệt được huấn luyện cho các kịch bản và dữ liệu cụ thể để đáp ứng các nhu cầu chính xác. Tuy nhiên, **ngày nay, hầu hết các kịch bản và tác vụ tổng quát đã có thể được giải quyết trực tiếp bằng cách gọi các API mô hình lớn.**

Từ góc độ theo đuổi tối đa **độ chính xác và chi phí**, việc huấn luyện và ứng dụng mô hình nhỏ vẫn có giá trị không thể thay thế; nhưng **đối với người mới bắt đầu, chúng ta hoàn toàn có thể bắt đầu bằng cách học cách tìm và gọi API mô hình lớn**, sau đó dần dần đi sâu vào các cách chơi nâng cao. Bạn chỉ cần cân nhắc giữa chi phí, độ chính xác và độ trễ, sau đó quyết định nơi nào nên sử dụng mô hình lớn tổng quát, nơi nào tiếp tục giữ lại hoặc giới thiệu mô hình nhỏ chuyên dụng.

> **Từ một số sản phẩm phổ biến, hãy tìm hiểu các mô hình lớn tổng quát về văn bản và đa modal thường dùng:**
>
> -   Dòng OpenAI: GPT-4, GPT-4.1, GPT-4o, GPT-5.1, v.v.
> -   Dòng Google: Gemini 1.5 Pro, Gemini 1.5 Flash, v.v.
> -   Dòng Anthropic: Claude 3.5 Sonnet, Claude 3.5 Haiku, v.v.
> -   Các mô hình trong nước: Dòng Tongyi Qianwen Qwen, Dòng Wenxin Yiyan ERNIE Bot, GLM/Zhipu Qingyan, Tencent Hunyuan, iFlytek Spark, các mô hình lớn đằng sau Kimi của Moonshot AI, Dòng MiniMax MiniMax-M2.7, v.v.
>
> Các mô hình lớn và dịch vụ thiên về hướng thị giác và video hơn, bao gồm:
>
> -   Tạo ảnh: DALL·E, Midjourney, Stable Diffusion, SDXL, Flux, v.v.
> -   Hiểu thị giác đa modal: GPT-4o, GPT-4.1 with Vision, Gemini 1.5 (đa modal hình ảnh-văn bản), Claude 3.5 Sonnet Vision, LLaVA, v.v.
> -   Tạo video: Sora, Kling, Runway Gen-2, Pika, Luma, Veo, v.v.
>
> Các mô hình lớn về giọng nói và âm thanh, bao gồm:
>
> -   Nhận dạng giọng nói ASR: Dòng Whisper (Whisper, Whisper-large-v3, v.v.), Deepgram, các mô hình lớn ASR đầu cuối của các nhà cung cấp dịch vụ đám mây (như iFlytek, Baidu, Volcengine, Alibaba, v.v.)
> -   Đa modal giọng nói và đối thoại giọng nói: GPT-4o (đối thoại giọng nói đầu cuối), OpenAI Realtime, khả năng hiểu âm thanh của Gemini 1.5, v.v.
> -   TTS / Tạo âm thanh và âm nhạc: OpenAI TTS, ElevenLabs, Suno, Udio, MusicGen, v.v.
>
> Các mô hình tạo và hiểu 3D / không gian, bao gồm:
>
> -   Tạo 3D từ văn bản và tạo 3D từ hình ảnh: DreamFusion, Shap-E, GET3D, Zero-1-to-3, TripoSR
