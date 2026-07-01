# How To Create Screen Flow — Crawl UI thật bằng Playwright

Quy trình tạo bộ tài liệu screen flow (ảnh chụp từng màn hình + sơ đồ mermaid mô tả luồng điều hướng) bằng cách nhờ Claude viết script Playwright tự động đăng nhập và đi qua các màn hình thật. Output mẫu tại `screen-flow/admin/` (Tokiwagi Admin), script tại `screen-flow/tools/`.

## Thông tin cần cung cấp cho Claude

- **URL** của khu vực cần crawl (vd trang Admin, trang User).
- **Tài khoản test** (email/password) cho từng vai trò muốn crawl — không dùng tài khoản khách hàng thật vì Claude sẽ click thăm dò.
- **HTTP Basic Auth** nếu site có thêm lớp bảo vệ ở tầng hạ tầng (Claude sẽ tự phát hiện qua `curl`, chỉ cần bạn cung cấp user/pass khi được hỏi).
- **Câu hỏi bí mật + câu trả lời** nếu tài khoản bị hỏi ở lần đăng nhập đầu (Claude không tự đoán, sẽ dừng lại hỏi bạn).
- Xác nhận **phạm vi an toàn**: Claude chỉ mở form/dialog để chụp ảnh, không bao giờ bấm nút lưu/xoá/submit thật — nếu muốn giới hạn thêm (vd không đụng vào 1 mục cụ thể), nói rõ trước khi chạy.

## Những gì Claude tự làm

1. Cài Playwright + Chromium trong `screen-flow/tools/` (chỉ 1 lần).
2. Lưu toàn bộ tài khoản/mật khẩu vào `screen-flow/credentials.local.md` (đã gitignore, không lên git).
3. Xử lý đăng nhập nhiều lớp: Basic Auth → form login → câu hỏi bí mật (nếu có) — tự retry khi gặp lỗi selector do UI dùng component đặc thù (MUI Autocomplete, DataGrid...).
4. Tự dò danh sách màn hình theo sidebar sau khi đăng nhập (không hard-code), vì mỗi tài khoản/vai trò có thể thấy menu khác nhau.
5. Với từng màn hình: chụp danh sách, tab con, trang chi tiết (kể cả khi nút xem không phải link thường mà là nút JS), mở thử form tạo mới/sửa/xoá để chụp — **luôn dừng ở bước mở, không submit thật**.
6. Sinh sơ đồ mermaid kiểu "hub" (sidebar là 1 node trung tâm nối tới từng mục) để tránh sơ đồ rối khi có nhiều màn hình.
7. Khi crawl thêm vai trò mới: so sánh với dữ liệu đã có, chỉ bổ sung phần thực sự khác biệt (màn hình mới, quyền bị khoá...) vào cùng 1 bộ tài liệu thay vì tạo bản riêng trùng lặp.
8. Dọn sạch script/ảnh dùng để thăm dò tạm thời sau khi xong, chỉ giữ lại script chính thức tái sử dụng được và output cuối cùng.

## Output

- `screen-flow/<khu-vực>/flow.md` — danh sách màn hình + sơ đồ mermaid + ảnh, xem trực tiếp bằng VSCode/Obsidian hoặc trình Markdown hỗ trợ Mermaid.
- `screen-flow/<khu-vực>/flow.json` — dữ liệu thô nếu cần xử lý lại bằng script khác.
- `screen-flow/<khu-vực>/screenshots/` — toàn bộ ảnh chụp.
- Bản đẹp hơn qua MkDocs: `docs/screens/*.md`, chạy `mkdocs serve -a 127.0.0.1:8765` — xem [`guideline/How_to_run.md`](How_to_run.md#trang-màn-hình-thực-tế-screenshot-ui-thật).

## Lưu ý an toàn

- Ảnh có thể chứa dữ liệu giống PII thật (dữ liệu test) → toàn bộ output đã gitignore, không commit.
- Nếu 1 thao tác đòi hỏi nhập lại mật khẩu để xác nhận (double-auth), đó là dấu hiệu thao tác có tính phá huỷ — Claude sẽ chỉ chụp lại UI rồi huỷ, không nhập mật khẩu thật.
