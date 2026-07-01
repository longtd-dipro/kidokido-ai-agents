---
name: jest-testing-conventions
description: Quy ước viết unit test Jest cho tokiwagi — mock strategy, cấu trúc AAA, coverage gợi ý theo layer, cách cover Acceptance Criteria. Dùng khi qa-agent viết/chạy test.
metadata:
  tags: jest, testing, unit-test, tokiwagi
---

# Jest Testing Conventions — tokiwagi

> Áp dụng cho: `qa-agent` khi viết/chạy unit test. KHÔNG phải methodology test thủ công (manual test case) — chỉ áp dụng cho unit/integration test tự động bằng Jest.

---

## Khi nào dùng skill này

- Trước khi viết file `*.test.ts`/`*.spec.ts` mới
- Khi cần quyết định mock gì, không mock gì
- Khi cần map Acceptance Criteria trong SPEC.md/task-N.md sang test case cụ thể

---

## 1. Cấu trúc test — AAA (Arrange-Act-Assert)

```typescript
describe('<TênModule/Function>', () => {
  it('<mô tả behavior, không mô tả implementation>', async () => {
    // Arrange: chuẩn bị input, mock dependency bên ngoài
    // Act: gọi function/handler đang test
    // Assert: kiểm tra output/side-effect — luôn có ít nhất 1 expect()
  });
});
```

Tên test case mô tả **behavior** ("trả về 404 khi booking không tồn tại"), không mô tả cách code hoạt động bên trong ("gọi prisma.findUnique 1 lần").

## 2. Mock Strategy

| Loại | Mock hay không | Lý do |
|---|---|---|
| Database (Prisma/PostgreSQL) | ❌ Không mock | POLICIES yêu cầu test với real DB — dùng DB test riêng, không mock `PrismaClient` |
| External service (GMO, AWS SES, LINE) | ✅ Mock | Không gọi API thật trong unit test — mock `src/services/gmo.service.ts`, `email.service.ts`,... |
| NextAuth session | ✅ Mock/stub | Giả lập session hợp lệ/không hợp lệ để test authorization |
| Internal service khác cùng codebase (không phải external) | Tuỳ — mock nếu test đơn vị (unit), dùng thật nếu test tích hợp (integration) giữa 2 service liên quan chặt |

Xác định dependency cần mock bằng `node knowledge/tokiwagi/semantic-query.mjs --imports "<file-cần-test>"` (đã có trong qa-agent.md Bước 1) — mock đúng những gì `--imports` liệt kê là external/service, không mock Prisma.

## 3. Map Acceptance Criteria → Test Case

Với mỗi AC trong SPEC.md/task-N.md (dạng Given-When-Then, xem skill `business-analyst`), viết tối thiểu 1 test case tương ứng:

```
AC: Given user đã đăng nhập, tenant còn chỗ trống
    When user đặt vé thành công qua GMO
    Then booking tạo với status "confirmed", vacancy giảm

→ it('tạo booking với status confirmed và giảm vacancy khi thanh toán GMO thành công', ...)
```

Với mỗi edge case đã liệt kê trong SPEC (câu hỏi số 4 của BA) → thêm 1 test case riêng, không gộp chung với happy path.

## 4. Coverage — gợi ý theo layer (không phải số cứng, điều chỉnh theo độ phức tạp thật)

| Layer | Gợi ý coverage | Ưu tiên |
|---|---|---|
| `src/services/` (business logic, payment, external integration) | Cao | Test kỹ nhất — đây là nơi bug ảnh hưởng tiền/dữ liệu thật |
| `src/pages/api/` (API route handler) | Trung bình-cao | Test validate input, status code, error case |
| `src/utils/server/` | Trung bình-cao nếu chứa logic tính toán (giá, vacancy...) | |
| `src/components/` (UI thuần, không logic) | Thấp-trung bình | Ưu tiên component có logic điều kiện phức tạp |

Ưu tiên file được `semantic-query.mjs` gắn tag/complexity `complex` trước (đã có trong qa-agent.md).

## 5. Chạy test

```bash
pnpm test                 # chạy toàn bộ
pnpm test -- <file>       # chạy 1 file
pnpm test --coverage      # kèm coverage report
```

---

## Anti-Patterns

- ❌ Mock `PrismaClient`/database — vi phạm POLICIES (phải dùng real DB)
- ❌ `skip`/`xtest` một test fail mà không ghi lý do trong comment + báo user
- ❌ Test tên mô tả implementation ("calls service.foo()") thay vì behavior
- ❌ Gộp nhiều assertion không liên quan vào 1 `it()` — khó biết chỗ nào fail
- ❌ Bỏ qua edge case đã liệt kê trong SPEC.md chỉ test happy path
- ❌ Gọi API thật (GMO/AWS SES/LINE) trong unit test thay vì mock
