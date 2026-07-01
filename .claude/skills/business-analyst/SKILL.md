---
name: business-analyst
description: Methodology thu thập yêu cầu và viết SPEC.md cho KIDOKIDO — kỹ thuật discovery, cách viết Acceptance Criteria rõ ràng, phân biệt business rule vs UI rule, phát hiện ambiguity. Dùng khi ba-agent nhận yêu cầu tính năng mới.
metadata:
  tags: business-analyst, discovery, requirements, spec-writing, tokiwagi
---

# Business Analyst — tokiwagi

> Áp dụng cho: `ba-agent` khi phân tích yêu cầu và viết SPEC.md

---

## Khi nào dùng skill này

- Nhận một yêu cầu tính năng mới, còn mơ hồ, cần discovery trước khi viết SPEC.md
- Cần quyết định câu hỏi nào phải hỏi user, câu hỏi nào có thể tự suy ra từ codebase hiện có
- Viết Acceptance Criteria sao cho Techlead/Dev/QA hiểu giống nhau, không cần đoán

---

## 1. Trình tự Discovery

```
1. Query semantic memory (đã có trong ba-agent.md Bước 1)
   → hiểu domain/feature đã tồn tại, tránh đề xuất trùng lặp

2. Đọc docs/domains/overview.md hoặc semantic-index.json (theo CLAUDE.md)
   → hiểu bức tranh nghiệp vụ tổng thể trước khi hỏi user

3. Áp dụng checklist 10 câu hỏi (ba-agent.md Bước 2)
   → mỗi câu trả lời PHẢI cụ thể, không được để "TBD" hay giả định ngầm

4. Với mỗi câu trả lời mơ hồ → hỏi lại 1 lần "5 Whys rút gọn":
   hỏi "tại sao cần như vậy?" tối đa 1-2 lần để lộ ra business rule thật,
   không hỏi quá sâu làm loãng cuộc trò chuyện
```

---

## 2. Phân biệt Business Rule vs UI Rule

Đây là lỗi phổ biến nhất khi viết SPEC — trộn lẫn 2 loại làm Dev không biết đâu là ràng buộc bắt buộc, đâu là gợi ý UI có thể đổi.

| Loại | Đặc điểm | Ví dụ | Viết ở đâu trong SPEC |
|---|---|---|---|
| **Business Rule** | Bất biến, đúng với mọi kênh (web/mobile/admin), vi phạm = sai nghiệp vụ | "Vé tháng không được dùng trùng giữa 2 tenant", "Booking phải có tenant còn chỗ trống" | `## Acceptance Criteria` |
| **UI Rule** | Chỉ liên quan cách hiển thị/tương tác, có thể đổi mà không ảnh hưởng nghiệp vụ | "Nút Submit disable khi đang loading", "Field ngày dùng date-picker" | `## Screens` (mô tả màn hình), không phải AC |

Nếu không chắc một quy tắc thuộc loại nào → hỏi user: "Nếu đổi kênh (vd. từ web sang admin tạo hộ), quy tắc này còn áp dụng không?" — còn áp dụng = business rule.

---

## 3. Viết Acceptance Criteria — định dạng Given-When-Then

Mỗi AC nên viết theo dạng kịch bản cụ thể, không viết chung chung:

```
❌ "User có thể đặt vé" — quá chung, không test được
✅ Given: user đã đăng nhập, tenant "Onsen A" còn 3 chỗ trống ngày 15/8
   When: user chọn tenant, chọn vé người lớn x2, thanh toán thành công qua GMO
   Then: booking được tạo với status "confirmed", chỗ trống tenant giảm còn 1,
         user nhận email xác nhận
```

Mỗi flow chính trong SPEC nên có ít nhất: 1 AC happy path + 1 AC cho mỗi edge case đã liệt kê ở Bước 2 (câu hỏi "Edge cases: gì có thể sai?").

---

## 4. Phát hiện Ambiguity — dấu hiệu cần hỏi lại ngay

```
❌ Dấu hiệu SPEC chưa đủ rõ, PHẢI hỏi user trước khi viết tiếp:
- Danh từ số nhiều không rõ giới hạn ("một vài", "nhiều lần" — bao nhiêu?)
- Có 2+ actor có thể thực hiện cùng hành động nhưng chưa rõ ai có quyền
- Có nhắc đến trạng thái mới (status) nhưng chưa liệt kê đủ transition
- Có nhắc external service (GMO, AWS SES, LINE) nhưng chưa rõ xử lý khi service đó lỗi
- Rollback/undo chưa được mô tả cho hành động có thể gây mất dữ liệu
```

Không tự chọn giá trị mặc định hợp lý rồi viết vào SPEC như thể đã chốt — luôn đánh dấu rõ trong `## Open Questions` nếu chưa hỏi được user ngay, và KHÔNG coi SPEC là sẵn sàng cho Techlead đọc cho đến khi mục này rỗng.

---

## 5. Out of Scope — tại sao quan trọng

`## Out of Scope` không phải mục hình thức — nó ngăn Techlead/Dev tự ý mở rộng phạm vi. Với mỗi tính năng, liệt kê rõ ít nhất:
- Các luồng liên quan nhưng KHÔNG làm trong feature này (vd. "không làm refund tự động, chỉ ghi nhận yêu cầu")
- Các kênh KHÔNG áp dụng (vd. "chỉ áp dụng web-admin, không áp dụng mobile app trong lần này")

---

## Anti-Patterns

- ❌ Viết AC dạng "hệ thống hoạt động đúng" — không kiểm chứng được
- ❌ Tự quyết định technical solution trong SPEC (vd. "dùng Redis cache") — đó là việc của Techlead
- ❌ Bỏ qua câu hỏi vì "chắc user cũng nghĩ vậy" — luôn hỏi khi không chắc 100%
- ❌ Gộp nhiều feature không liên quan vào 1 SPEC vì "tiện thể" — mỗi SPEC là 1 feature-slug
- ❌ Để `## Open Questions` còn mục chưa trả lời mà vẫn báo SPEC "sẵn sàng" cho Techlead
