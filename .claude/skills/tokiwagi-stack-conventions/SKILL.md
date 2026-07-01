---
name: tokiwagi-stack-conventions
description: Quy ước code cho stack thật của tokiwagi — Next.js 15 (pages/api), Express, Prisma/PostgreSQL, NextAuth, Redux Toolkit v2, TanStack Query v5, AWS. Dùng khi dev-agent implement task.
metadata:
  tags: nextjs, express, prisma, postgresql, redux, tanstack-query, tokiwagi
---

# Tokiwagi Stack Conventions

> Áp dụng cho: `dev-agent` khi implement task. Đây là quy ước theo stack THẬT của tokiwagi (Next.js 15 + Express + Prisma + PostgreSQL) — không phải NestJS/TypeORM.

---

## Khi nào dùng skill này

- Trước khi tạo/sửa file trong `prisma/`, `src/pages/api/`, `src/services/`, `src/stores/`, `src/components/`
- Khi không chắc pattern hiện có của tokiwagi cho một loại thay đổi (migration, API handler, service, Redux slice)

---

## 1. Database — Prisma + PostgreSQL

- Schema sống ở `prisma/schema.prisma`. Đổi schema → tạo migration bằng `prisma migrate dev --name <mo-ta-ngan>`, không sửa tay file migration đã generate.
- Không tự ý đổi kiểu cột đã có dữ liệu production mà không hỏi user (rủi ro mất dữ liệu).
- Soft delete: nếu model đã có field kiểu `deletedAt`/tương tự, dùng đúng pattern đó thay vì hard delete — kiểm tra bằng `semantic-query.mjs "<Model>" --layer "Database"` trước khi viết logic xóa.
- Transaction: các thao tác ghi nhiều bảng liên quan (vd. tạo booking + trừ vacancy) phải bọc trong `prisma.$transaction(...)`.
- Tránh N+1: dùng `include`/`select` của Prisma thay vì query lặp trong vòng lặp.

## 2. API Routes — `src/pages/api/`

- Convention path: REST-style, resource theo danh từ số nhiều/CRUD chuẩn (vd. `src/pages/api/user/bookings/index.ts`, `src/pages/api/admin/tickets/index.ts`).
- Mỗi handler: validate input trước khi gọi service/Prisma, trả lỗi rõ ràng theo status code chuẩn (400 validation, 401/403 auth, 404 not found, 409 conflict).
- Business logic KHÔNG viết trực tiếp trong handler — gọi qua `src/services/` hoặc `src/utils/server/` (tham khảo pattern có sẵn: `src/services/gmo.service.ts`, `src/services/email.service.ts`, `src/utils/server/booking.ts`).
- Auth: dùng NextAuth session/middleware hiện có, không tự viết cơ chế auth mới.
- REST only — không thêm GraphQL/tRPC (POLICIES §5).

## 3. Backend Services — `src/services/`, `src/libs/`, `src/utils/`

- 1 service = 1 trách nhiệm rõ ràng (vd. `gmo.service.ts` chỉ xử lý GMO, không trộn business logic booking vào đây).
- External integration (GMO, AWS SES, LINE) luôn qua service riêng, không gọi thẳng API bên ngoài từ page/component.
- Secrets (API key, merchant ID...) lấy từ AWS Parameter Store / biến môi trường đã cấu hình sẵn — không hard-code, không thêm secret mới vào `.env` production.

## 4. State Management

- **Server state** (data từ API): TanStack Query v5, cú pháp object — `useQuery({ queryKey, queryFn })`, không dùng cú pháp positional v4.
- **Client state** (UI/global state không phải data server): Redux Toolkit v2, đặt trong `src/stores/`.
- Không dùng Redux để cache data server (đó là việc của TanStack Query) và không dùng Context API cho auth/global state (POLICIES §5).

## 5. Frontend — `src/components/`, `src/pages/`

- Component mới đặt cạnh component cùng nhóm chức năng hiện có (vd. luồng tạo booking nằm dưới `src/components/CreateBooking/`) — dùng `semantic-query.mjs "<feature>" --layer "Frontend Components"` để tìm đúng chỗ trước khi tạo file mới.
- Không tự tạo pattern UI mới nếu đã có component tương tự — ưu tiên tái sử dụng/mở rộng.

## 6. Testing hook (chi tiết xem skill `jest-testing-conventions` của QA)

- Dev implement task có yêu cầu Unit Tests trong file task-N.md — viết test cùng lúc với code, không để lại cho QA làm từ đầu.
- Không mock Prisma/DB trong test (theo POLICIES — dùng real DB).

---

## Anti-Patterns

- ❌ Viết business logic trực tiếp trong `pages/api/*.ts` handler thay vì tách ra service
- ❌ Query Prisma trong vòng lặp (N+1) thay vì `include`/`select`/`findMany` một lần
- ❌ Dùng Redux Toolkit để lưu data fetch từ API (phải dùng TanStack Query)
- ❌ Sửa file migration đã generate thay vì tạo migration mới
- ❌ Hard-code API key/merchant ID GMO trong code thay vì đọc từ config/secret store
- ❌ Gọi thẳng API GMO/AWS SES/LINE từ component thay vì qua service layer
