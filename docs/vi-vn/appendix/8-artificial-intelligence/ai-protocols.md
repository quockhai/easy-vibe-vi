# Giao thức AI Agent (MCP & A2A)

::: tip Vấn đề cốt lõi
**AI Agent giao tiếp với thế giới bên ngoài như thế nào?** Giống như internet cần giao thức HTTP, AI Agent cũng cần các giao thức truyền thông được tiêu chuẩn hóa. Chương này giới thiệu hai giao thức Agent phổ biến nhất: MCP và A2A, chúng lần lượt giải quyết các vấn đề giao tiếp giữa AI với công cụ và giữa Agent với Agent.
:::

---

## 0. Giao thức là gì?

Trong lĩnh vực máy tính, **giao thức (Protocol)** là một bộ quy tắc và quy ước được tiêu chuẩn hóa, cho phép các hệ thống và chương trình khác nhau có thể "hiểu" và "giao tiếp" với nhau.

### 0.1 Tại sao cần giao thức?

Hãy tưởng tượng một kịch bản: bạn gửi một gói hàng cho bạn bè và cần điền địa chỉ. Nếu mỗi người viết địa chỉ theo một định dạng khác nhau, nhân viên giao hàng sẽ không thể phát. Giao thức chính là tiêu chuẩn quy định "cách viết địa chỉ" – tỉnh, thành phố, quận, đường, số nhà, viết theo định dạng này thì ai cũng có thể hiểu.

Máy tính cũng vậy. Hai chương trình muốn giao tiếp phải thống nhất:
- Định dạng dữ liệu là gì? (JSON? Nhị phân?)
- Cách thiết lập kết nối? (Quy trình bắt tay)
- Xử lý lỗi như thế nào? (Xử lý lỗi)

### 0.2 Các giao thức phổ biến trong máy tính

| Giao thức | Tác dụng | Bạn sử dụng hàng ngày |
|------|------|-------------|
| **HTTP** | Giao thức truyền tải trang web | Trình duyệt mở trang web |
| **HTTPS** | HTTP được mã hóa | Ngân hàng trực tuyến, trang thanh toán |
| **TCP/IP** | Giao thức nền tảng internet | Tất cả các giao tiếp mạng |
| **DNS** | Giao thức phân giải tên miền | Chuyển `google.com` thành địa chỉ IP |
| **SMTP** | Giao thức gửi email | Gửi email |
| **WebSocket** | Giao tiếp song công thời gian thực | Phần mềm chat, trò chơi trực tuyến |
| **SSH** | Đăng nhập từ xa an toàn | Kết nối máy chủ |
| **FTP** | Giao thức truyền tải tệp | Tải lên/tải xuống tệp |

Những giao thức này tạo nên nền tảng của internet. Không có chúng, bạn không thể duyệt web, gửi email, xem video.

### 0.3 Giá trị của giao thức

Giá trị cốt lõi của giao thức là **tiêu chuẩn hóa** và **khả năng tương tác**:

- **Tiêu chuẩn hóa**: Mọi người đều làm việc theo cùng một bộ quy tắc, giảm chi phí giao tiếp
- **Khả năng tương tác**: Các hệ thống từ các nhà cung cấp, công nghệ khác nhau có thể kết nối liền mạch

Ví dụ, giao thức HTTP cho phép trình duyệt Chrome truy cập máy chủ Nginx, cho phép trình thu thập dữ liệu Python lấy dữ liệu từ trang web Java. Không cần Chrome và Nginx phải "biết" nhau, chỉ cần cả hai tuân thủ giao thức HTTP là được.

### 0.4 AI Agent cũng cần giao thức

Để AI Agent thực sự "làm việc", chúng cần:
- Gọi các công cụ bên ngoài (kiểm tra thời tiết, gửi email, thao tác cơ sở dữ liệu)
- Hợp tác với các Agent khác (phân công công việc để hoàn thành các nhiệm vụ phức tạp)

Điều này đòi hỏi các giao thức được tiêu chuẩn hóa để quy định "AI gọi công cụ như thế nào" và "các Agent giao tiếp với nhau ra sao". Đây chính là nguồn gốc của **MCP** và **A2A**.

---

## 1. Các tầng giao thức của Agent

Trước khi đi sâu vào các giao thức cụ thể, hãy cùng xem xét các tầng giao tiếp trong hệ sinh thái Agent:

| Tầng | Giao thức | Vấn đề được giải quyết | So sánh |
|------|------|-----------|------|
| **1** | Function Call | AI gọi hàm cục bộ như thế nào | Não bộ ra lệnh |
| **2** | **MCP** | AI kết nối với công cụ và nguồn dữ liệu bên ngoài như thế nào | Cổng USB-C |
| **3** | **A2A** | Các Agent hợp tác giao tiếp như thế nào | WeChat Work |

::: tip Giải thích từng dòng trong bảng này
**Tầng 1 (Function Call)**: Đây là khả năng cơ bản nhất của các mô hình lớn – kích hoạt thực thi hàm bằng cách xuất dữ liệu có cấu trúc (JSON). Nó là nền tảng của "giao thức", nhưng bản thân nó giống một khả năng hơn là một giao thức tiêu chuẩn.

**Tầng 2 (MCP)**: Model Context Protocol, được Anthropic phát hành vào tháng 11 năm 2024. Nó tiêu chuẩn hóa cách AI kết nối với các công cụ và nguồn dữ liệu bên ngoài, giống như USB-C đã thống nhất các cổng sạc của nhiều thiết bị khác nhau.

**Tầng 3 (A2A)**: Agent-to-Agent Protocol, được Google phát hành vào tháng 4 năm 2025. Nó cho phép các Agent khác nhau có thể tìm thấy, giao tiếp và hợp tác với nhau, giống như WeChat Work cho phép đồng nghiệp gửi nhiệm vụ, trò chuyện.
:::

Chương này tập trung vào hai giao thức chính thức ở tầng 2 và 3: MCP và A2A.

---

## 2. MCP (Model Context Protocol)

### 2.1 Thông tin cơ bản về giao thức

| Mục | Nội dung |
|------|------|
| **Tên đầy đủ** | Model Context Protocol |
| **Bên khởi xướng** | Anthropic |
| **Thời gian phát hành** | 25 tháng 11 năm 2024 |
| **Tài liệu chính thức** | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| **Giấy phép mã nguồn mở** | MIT License |
| **GitHub** | [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol) |

::: tip Tại sao lại gọi là "Context Protocol"?
**Context (ngữ cảnh)** là chìa khóa để mô hình lớn hiểu nhiệm vụ. Ý tưởng cốt lõi của MCP là: **cho phép AI tự động lấy thông tin ngữ cảnh cần thiết**, thay vì nhồi nhét tất cả thông tin vào Prompt.

Ví dụ, khi AI cần đọc một tệp, bạn không cần sao chép và dán nội dung tệp cho nó, mà thông qua MCP, nó có thể truy cập trực tiếp vào hệ thống tệp.
:::

### 2.2 Bối cảnh phát hành

Năm 2024, với sự ra mắt của Claude 3.5 Sonnet, Anthropic nhận thấy một vấn đề: **mỗi công cụ phải được tích hợp riêng lẻ**.

Hãy tưởng tượng:
- Bạn muốn AI đọc kho lưu trữ GitHub → phải viết mã tích hợp GitHub
- Bạn muốn AI truy vấn cơ sở dữ liệu → phải viết mã tích hợp cơ sở dữ liệu
- Bạn muốn AI thao tác hệ thống tệp → phải viết mã tích hợp hệ thống tệp

Mỗi lần tích hợp đều phải viết lại các đoạn mã tương tự: xác thực, xử lý lỗi, chuyển đổi dữ liệu...

Anthropic đã viết trong blog chính thức của mình:
> "We're introducing the Model Context Protocol (MCP), an open protocol that standardizes how applications provide context to LLMs."

**Mục tiêu cốt lõi**: Cho phép các nhà phát triển công cụ viết mã một lần, và tất cả các ứng dụng AI hỗ trợ MCP đều có thể sử dụng.

### 2.3 MCP là gì?

<McpVisualDemo />

**Ba khả năng cốt lõi**:

| Khả năng | Tiếng Anh | Tác dụng | Ví dụ |
|------|------|------|------|
| **Công cụ** | Tools | Chức năng AI có thể gọi | Kiểm tra thời tiết, gửi email |
| **Tài nguyên** | Resources | Dữ liệu AI có thể đọc | Nội dung tệp, bản ghi cơ sở dữ liệu |
| **Lời nhắc** | Prompts | Mẫu lời nhắc được định nghĩa trước | Mẫu đánh giá mã, mẫu viết bài |

### 2.4 Cách triển khai nội bộ của MCP

<McpDetailedDemo />

### 2.5 Hiểu theo cách so sánh: Cổng USB-C

MCP giống như **cổng USB-C**:

- **Trước đây**: Mỗi thiết bị có cổng sạc riêng (cổng tròn, cổng dẹt, nam châm...)
- **Bây giờ**: USB-C đã thống nhất việc sạc và truyền dữ liệu cho tất cả các thiết bị
- **MCP**: Thống nhất cách AI kết nối với tất cả các công cụ

Các nhà phát triển công cụ chỉ cần triển khai MCP Server một lần, tất cả các ứng dụng AI hỗ trợ MCP (Claude, Cursor, Windsurf, v.v.) đều có thể sử dụng trực tiếp.

### 2.6 Các trường hợp ứng dụng điển hình của MCP

| Kịch bản | Mô tả | Ví dụ |
|------|------|------|
| **Thao tác tệp cục bộ** | Cho phép AI đọc/sửa đổi tệp cục bộ | Đọc kho mã, phân tích tệp nhật ký |
| **Truy vấn cơ sở dữ liệu** | Cho phép AI trực tiếp truy vấn cơ sở dữ liệu | Truy vấn SQL, phân tích dữ liệu |
| **Gọi API** | Cho phép AI gọi các dịch vụ bên thứ ba | GitHub API, Slack, email |
| **Tích hợp công cụ phát triển** | Cho phép AI sử dụng công cụ phát triển | Thao tác Git, lệnh terminal |

**Các trường hợp thực tế**:
- **Cursor/Windsurf**: Kết nối hệ thống tệp, Git, terminal thông qua MCP
- **Claude Desktop**: Kết nối phần mềm ghi chú, ứng dụng email thông qua MCP
- **Script tự động hóa**: Cho phép AI thực hiện các tác vụ tự động hóa (sao lưu, triển khai, đồng bộ hóa dữ liệu)

---

## 3. A2A (Agent-to-Agent Protocol)

### 3.1 Thông tin cơ bản về giao thức

| Mục | Nội dung |
|------|------|
| **Tên đầy đủ** | Agent-to-Agent Protocol |
| **Bên khởi xướng** | Google |
| **Thời gian phát hành** | 9 tháng 4 năm 2025 |
| **Tài liệu chính thức** | [google.github.io/A2A](https://google.github.io/A2A) |
| **Giấy phép mã nguồn mở** | Apache 2.0 |
| **GitHub** | [github.com/google/A2A](https://github.com/google/A2A) |

::: tip Tại sao lại là Google khởi xướng?
Google đã phát hành A2A tại hội nghị Cloud Next 2025, điều này liên quan chặt chẽ đến chiến lược AI cấp doanh nghiệp của họ.

Google tin rằng: AI doanh nghiệp trong tương lai không phải là một Agent siêu việt duy nhất, mà là **nhiều Agent chuyên biệt hợp tác** – có Agent chịu trách nhiệm phân tích dữ liệu, có Agent chịu trách nhiệm tạo mã, có Agent chịu trách nhiệm xử lý tài liệu.

Các Agent này cần một cách tiêu chuẩn hóa để giao tiếp với nhau, và A2A ra đời từ đó.
:::

### 3.2 Bối cảnh phát hành

MCP đã giải quyết vấn đề "AI kết nối công cụ như thế nào", nhưng vẫn còn một vấn đề: **nhiều Agent hợp tác như thế nào?**

Hãy tưởng tượng một kịch bản:
- Agent A là "chuyên gia phân tích yêu cầu"
- Agent B là "chuyên gia tạo mã"
- Agent C là "chuyên gia kiểm thử"

Người dùng nói: "Hãy giúp tôi phát triển một chức năng đăng nhập"

Agent A sau khi phân tích yêu cầu, cần giao nhiệm vụ cho Agent B; Agent B sau khi viết mã xong, cần nhờ Agent C kiểm thử. Chúng giao tiếp với nhau như thế nào?

Google đã viết trong blog chính thức của mình:
> "A2A is an open protocol that enables AI agents to communicate with each other, facilitating collaboration across different frameworks and vendors."

**Mục tiêu cốt lõi**: Cho phép các Agent được phát triển bởi các nhà cung cấp và framework khác nhau có thể hợp tác liền mạch.

### 3.3 A2A là gì?

<A2AVisualDemo />

**Ba khái niệm cốt lõi**:

| Khái niệm | Tiếng Anh | Tác dụng | So sánh |
|------|------|------|------|
| **Thẻ Agent** | Agent Card | Mô tả khả năng của Agent | Thẻ nhân viên |
| **Nhiệm vụ** | Task | Đơn vị công việc cần thực hiện | Phiếu công việc |
| **Tin nhắn** | Message | Nội dung giao tiếp giữa các Agent | Lịch sử trò chuyện |

### 3.4 Cách triển khai nội bộ của A2A

<A2ADetailedDemo />

### 3.5 Hiểu theo cách so sánh: WeChat Work

A2A giống như **WeChat Work**:

- **Agent Card**: Danh thiếp của mỗi người, hiển thị tên, phòng ban, trách nhiệm
- **Giao nhiệm vụ**: @một người nào đó, giao một nhiệm vụ
- **Trò chuyện giao tiếp**: Có thể giao tiếp bất cứ lúc nào trong quá trình thực hiện nhiệm vụ
- **Theo dõi nhiệm vụ**: Có thể xem tiến độ và trạng thái của nhiệm vụ

Các Agent khác nhau giống như các đồng nghiệp khác nhau, A2A cho phép họ hợp tác để hoàn thành các dự án phức tạp.

### 3.6 Các trường hợp ứng dụng điển hình của A2A

| Kịch bản | Mô tả | Ví dụ |
|------|------|------|
| **Phát triển phần mềm** | Nhiều Agent hợp tác hoàn thành nhiệm vụ phát triển | Phân tích yêu cầu → Mã hóa → Kiểm thử → Triển khai |
| **Quy trình làm việc doanh nghiệp** | Các Agent của các phòng ban khác nhau hợp tác xử lý nghiệp vụ | HR Agent + Tài chính Agent + Pháp lý Agent |
| **Dịch vụ khách hàng thông minh** | Nhiều Agent chuyên biệt phân công xử lý | Tiếp nhận → Giải đáp → Chuyển tiếp → Ghi nhận |
| **Phân tích dữ liệu** | Nhiều Agent hợp tác phân tích dữ liệu | Thu thập → Làm sạch → Phân tích → Trực quan hóa → Báo cáo |

**Các trường hợp thực tế**:
- **Google Agent Space**: Nhiều Agent nội bộ doanh nghiệp hợp tác xử lý tài liệu, email, lịch trình
- **Nhóm phát triển phần mềm**: Agent Yêu cầu → Agent Mã hóa → Agent Kiểm thử → Agent Triển khai
- **Hệ thống dịch vụ khách hàng thông minh**: Agent Tiếp nhận → Agent Giải đáp chuyên nghiệp → Agent Chuyển tiếp thủ công

---

## 4. MCP so với A2A: So sánh và mối quan hệ

### 4.1 Sự khác biệt cốt lõi

| Khía cạnh | MCP | A2A |
|------|-----|-----|
| **Bên khởi xướng** | Anthropic (11/2024) | Google (04/2025) |
| **Định vị** | Kết nối AI với công cụ | Hợp tác giữa Agent với Agent |
| **Phạm vi giao tiếp** | Client-Server | Peer-to-Peer |
| **Định dạng dữ liệu** | JSON-RPC 2.0 | HTTP + JSON |
| **So sánh** | Cổng USB-C | WeChat Work |

### 4.2 Mối quan hệ giữa hai giao thức

MCP và A2A **không phải là mối quan hệ cạnh tranh, mà là mối quan hệ bổ sung**:

<ProtocolComparisonDemo />

### 4.3 Lựa chọn như thế nào?

| Kịch bản | Lựa chọn |
|------|------|
| Cho phép AI gọi hàm cục bộ hoặc công cụ | Function Call |
| Sử dụng công cụ bên thứ ba (cơ sở dữ liệu, API, hệ thống tệp) | MCP |
| Xây dựng hệ thống hợp tác đa Agent | A2A |
| Đồng thời cần tích hợp công cụ và hợp tác đa Agent | MCP + A2A |

---

## 5. Xu hướng tương lai của giao thức

### 5.1 Phát triển hệ sinh thái

**Hệ sinh thái MCP** (tính đến đầu năm 2025):
- Server chính thức được cung cấp: hệ thống tệp, SQLite, Git, PostgreSQL, v.v.
- Server do cộng đồng đóng góp: Slack, Notion, Figma, Stripe, v.v.
- Các ứng dụng hỗ trợ MCP: Claude Desktop, Cursor, Windsurf, Zed, v.v.

**Hệ sinh thái A2A** (mới phát hành):
- Các sản phẩm Agent của Google là những sản phẩm đầu tiên hỗ trợ
- Cộng đồng mã nguồn mở đang phát triển SDK cho nhiều ngôn ngữ khác nhau
- Các ứng dụng cấp doanh nghiệp đang được khám phá

### 5.2 Quá trình tiêu chuẩn hóa

Hiện tại, các giao thức Agent vẫn đang trong "thời kỳ chiến quốc":
- MCP và A2A là hai giao thức phổ biến nhất
- Còn có các giao thức mới nổi khác như ANP, AGP, v.v.
- Trong tương lai có thể sẽ hợp nhất hoặc thống nhất

So sánh với sự phát triển của internet:
- Giai đoạn đầu: Nhiều giao thức mạng cục bộ cùng tồn tại
- Sau đó: TCP/IP trở thành tiêu chuẩn
- Hiện tại: Các giao thức Agent cũng có thể sẽ hướng tới sự thống nhất

---

## 6. Tóm tắt

::: tip Các điểm cốt lõi
| Giao thức | Hiểu đơn giản | Thời gian phát hành | Bên khởi xướng | Kịch bản áp dụng |
|------|-----------|---------|--------|---------|
| **MCP** | "USB-C" để AI kết nối công cụ | 11/2024 | Anthropic | Tích hợp công cụ, kết nối nguồn dữ liệu |
| **A2A** | "WeChat Work" để Agent hợp tác | 04/2025 | Google | Hợp tác đa Agent, ủy thác nhiệm vụ |

**Thông tin chi tiết quan trọng**:
1. MCP giải quyết vấn đề "AI lấy khả năng bên ngoài như thế nào"
2. A2A giải quyết vấn đề "nhiều AI hợp tác như thế nào"
3. Cả hai bổ sung cho nhau, và có thể được sử dụng kết hợp trong tương lai
4. Lựa chọn giao thức phải dựa trên kịch bản cụ thể, không có giải pháp vạn năng
:::

---

## Tài liệu tham khảo

1. **Tài liệu chính thức của MCP**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
2. **GitHub của MCP**: [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
3. **Blog phát hành của Anthropic**: "Introducing the Model Context Protocol" (25-11-2024)
4. **Tài liệu chính thức của A2A**: [google.github.io/A2A](https://google.github.io/A2A)
5. **GitHub của A2A**: [github.com/google/A2A](https://github.com/google/A2A)
6. **Blog của Google Cloud**: "Announcing the Agent-to-Agent Protocol" (09-04-2025)
