# KIDOKIDO — Tài liệu dự án Tokiwagi

Tài liệu dự án **tokiwagi** — hệ thống quản lý đặt phòng/vé cho các cơ sở (tenant), tích hợp thanh toán GMO, tích hợp POS Smaregi, và bảng điều khiển admin.

Stack: Next.js 15 · TypeScript · Express · Prisma/PostgreSQL · NextAuth · Redux · GMO Payment · AWS.

## Nội dung

- **[Tổng quan Tính năng](domains/overview.md)** — bản đồ 5 domain nghiệp vụ / 20 tính năng / 109 bước, kèm sơ đồ (mermaid) cho từng tính năng, ít thuật ngữ kỹ thuật hơn (chi tiết file code gom vào phần "Chi tiết kỹ thuật" thu gọn, chỉ mở khi cần). Trích xuất từ knowledge graph (understand-anything). Tạo lại bằng lệnh `/understand-domain reponsitories/tokiwagi` khi code thay đổi nhiều — xem hướng dẫn chi tiết tại `guideline/How_to_run.md`.
- **[Màn hình thực tế — Admin](screens/admin.md)** / **[User](screens/user.md)** — screenshot + sơ đồ điều hướng chụp trực tiếp từ UI thật, giúp hình dung màn hình tương ứng với từng tính năng. Chỉ xem local, không commit lên git (dữ liệu môi trường test).
- **Pipeline AI Agent** (BA → Techlead → Dev → QA) — xem `README.md` và `POLICIES.md` ở root repo (ngoài `docs/`, không nằm trong site này).
- **Semantic memory / knowledge graph** — xem `knowledge/tokiwagi/How_To_Use.md` ở root repo.
