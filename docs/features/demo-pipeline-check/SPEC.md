# SPEC: Demo Pipeline Check (API debug ping)

> Feature DEMO dùng để kiểm tra cơ chế pipeline BA→Techlead→Dev→QA + status.md/slash command. Không phải feature thật, sẽ xoá thư mục này sau khi test xong.

## Mô tả nghiệp vụ
Thêm 1 API endpoint debug đơn giản để developer kiểm tra server còn sống (healthcheck), trả về trạng thái và thời gian hiện tại. Không có logic nghiệp vụ thật, dùng nội bộ cho dev/staging.

## Actors & Preconditions
- Actor: Developer (nội bộ team)
- Precondition: không cần đăng nhập, không cần quyền đặc biệt

## Happy Path
1. Developer gửi GET request tới `/api/debug/ping`
2. Server trả về `200 OK` kèm JSON `{ status: 'ok', timestamp: '<ISO string>' }`

## Alternative Flows & Edge Cases
- Không có edge case: endpoint không nhận input, không có side effect, không đọc/ghi DB.

## Acceptance Criteria
```
Given: server đang chạy
When: developer gửi GET /api/debug/ping
Then: response 200, body = { status: 'ok', timestamp: <ISO 8601 string hợp lệ> }
```

## Screens
Không có UI.

## Out of Scope
- Không expose endpoint này ở môi trường production
- Không thêm authentication/authorization
- Không dùng để đo hiệu năng/monitoring thật (chỉ ping đơn giản)

## Open Questions
(rỗng — đã có đủ thông tin từ checklist ban đầu)
