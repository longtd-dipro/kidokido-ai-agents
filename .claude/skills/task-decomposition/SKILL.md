---
name: task-decomposition
description: Methodology phân rã SPEC.md thành task files atomic cho tokiwagi — INVEST criteria, dependency detection, estimation heuristics cho Next.js/Express/Prisma. Dùng khi techlead-agent cần quyết định cắt task ở đâu và estimate bao nhiêu giờ.
metadata:
  tags: task-decomposition, agile, story-splitting, estimation, tokiwagi
---

# Task Decomposition — tokiwagi

> Áp dụng cho: `techlead-agent` khi phân rã SPEC.md → task files

---

## Khi nào dùng skill này

- Quyết định cắt 1 feature thành bao nhiêu tasks
- Detect dependency ẩn giữa các tasks
- Estimate giờ cho từng task Next.js/Express/Prisma
- Quyết định tasks nào có thể làm song song vs phải tuần tự

---

## 1. INVEST Criteria — kiểm tra mỗi task trước khi tạo

Mỗi task phải pass đủ 6 tiêu chí:

| Tiêu chí | Câu hỏi kiểm tra | Fail → hành động |
|---|---|---|
| **I**ndependent | Task này có thể implement mà không cần task khác chưa xong? | Split hoặc reorder |
| **N**egotiable | Scope có thể điều chỉnh nếu phát sinh vấn đề? | Ghi "Không được làm" rõ ràng |
| **V**aluable | Task này deliver giá trị gì (dù nhỏ)? | Merge vào task khác nếu không có giá trị độc lập |
| **E**stimable | Có thể ước lượng giờ trong khoảng ±50%? | Break nhỏ hơn nếu không estimate được |
| **S**mall | ≤ 8h thực hiện? | Split thành 2+ tasks nếu > 8h |
| **T**estable | Có thể viết unit test verify behavior? | Thiếu unit test = task chưa đủ spec |

---

## 2. Nhóm task theo layer (tokiwagi là 1 repo monolith, không cần Phase cross-repo)

Khi feature chạm nhiều layer, gợi ý thứ tự implement (không bắt buộc numbering Phase 1-4 như dự án multi-repo — chỉ dùng khi thật sự cần tuần tự):

```
1. Database   — prisma/schema.prisma + migration
   └─ Tạo/sửa model, chạy `prisma migrate dev`
   └─ KHÔNG viết business logic ở bước này

2. Backend Services — src/services/, src/libs/, src/utils/
   └─ Service method + business logic + unit test

3. API Routes — src/pages/api/
   └─ Handler gọi service, validate input, trả response

4. Frontend — src/components/, src/pages/, src/stores/
   └─ Component / page + Redux slice (nếu cần state mới)
```

**Rule:** Backend Services chỉ bắt đầu khi model Prisma đã tồn tại. Frontend chỉ bắt đầu khi API Route đã có shape response rõ ràng (ghi trong task, không để Frontend tự đoán field).

---

## 3. Dấu hiệu task cần split

```
❌ Cần split khi:
- Estimate > 8h
- Task chạm > 3 file lớn không liên quan (service + model + API route + 2 component cùng lúc)
- Task vừa tạo Prisma model vừa viết business logic (luôn tách DB và Service)
- Task Frontend vừa tạo component vừa tạo API call + Redux slice (tách UI vs data layer nếu cả 2 đều lớn)
- "Implement module X" không có file path cụ thể → chưa đủ spec

✅ Không cần split khi:
- API Route handler + validate input cùng 1 endpoint (cohesive, < 4h)
- Prisma model + migration của cùng 1 bảng (atomic DB change)
- React component + local hook của component đó (không phải shared hook)
```

---

## 4. Dependency Detection — các pattern ẩn thường gặp

### Pattern 1: Shared Prisma model
```
task-1 tạo model Booking trong schema.prisma  →  task-2 dùng model Booking trong service
→ task-2 depends on task-1, không song song được
```

### Pattern 2: Shared service function
```
task-2 export hàm createBooking() trong src/services/  →  task-3 (API route) gọi hàm đó
→ task-3 chỉ bắt đầu sau khi task-2 xong (interface — tên hàm, tham số, return type — đã chốt)
```

### Pattern 3: Shared API response shape
```
task-3 định nghĩa response { id, status, ... } của API route
→ task-4 (Frontend) fetch API này — phải ghi rõ response shape vào task-4,
  Frontend không tự đoán field
```

### Pattern 4: Shared Redux slice / store
```
task-4a thêm field mới vào 1 slice trong src/stores/
task-4b cũng sửa cùng slice đó
→ Nếu cả 2 cùng sửa 1 slice → SEQUENTIAL, không song song
→ Nếu chỉ đọc (useSelector) → song song OK
```

---

## 5. Estimation Heuristics — tokiwagi (Next.js/Express/Prisma)

> Baseline. Tăng 50% nếu: task chạm nhiều bảng liên quan phức tạp, cần debug DB, hoặc có edge case payment (GMO).

| Loại task | Estimate |
|---|---|
| Migration Prisma (thêm field/index) | 1h |
| Migration Prisma (tạo model mới) | 2h |
| Service function đơn giản (CRUD) | 2h |
| Service function có business logic phức tạp | 3–4h |
| API route handler (1 endpoint, có validate) | 2h |
| API route CRUD (nhiều method cùng resource) | 4h |
| Middleware / guard mới | 2–3h |
| React component/page mới (list + filter) | 5–6h |
| React component/page mới (form create/edit) | 4–5h |
| Shared component đơn giản (< 100 dòng) | 2h |
| Redux slice mới | 2h |
| Unit test viết song song với code | 1–2h |
| Unit test retro (code đã có sẵn) | 2–3h |

---

## 6. Checklist trước khi finalize task list

- [ ] Mỗi task ≤ 8h?
- [ ] Mỗi task có file path cụ thể (không phải "implement module X")?
- [ ] Database tách khỏi Service/API nếu cả hai đều đáng kể?
- [ ] Dependency giữa các task được ghi rõ trong task file?
- [ ] Mọi task code mới đều có section Unit Tests?
- [ ] Non-Regression table đã điền từ kết quả `--dependents`?

---

## Anti-Patterns

- ❌ Task "Implement toàn bộ booking module" — quá rộng, phải break down
- ❌ Task Service tạo Prisma model trong lúc viết business logic — 2 việc khác nhau
- ❌ Estimate "1–2 ngày" — phải quy về giờ cụ thể
- ❌ Frontend task không ghi rõ response shape của API — dẫn đến làm lại khi field sai
- ❌ Bỏ qua Non-Regression table — dễ gây regression bug ở service/API dùng chung
