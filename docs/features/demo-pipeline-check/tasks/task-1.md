# Task 1 — Thêm API debug ping

## Mục tiêu
Thêm 1 API route mới trả về trạng thái server, dùng để demo/kiểm tra pipeline (không phải nhu cầu nghiệp vụ thật).

## Context (đọc trước khi code)
- SPEC.md: `docs/features/demo-pipeline-check/SPEC.md`
- File liên quan (từ semantic-query): không có — đây là route hoàn toàn mới, semantic-query không trả về file trùng lặp/liên quan (`node knowledge/tokiwagi/semantic-query.mjs "pages api" --layer "API Routes"` → 0 kết quả liên quan tới debug/health).
- Blast radius (từ --dependents): không áp dụng — file mới tạo, chưa có dependents.

## Yêu cầu implement
### Tạo mới: `reponsitories/tokiwagi/src/pages/api/debug/ping.ts`
- Next.js API Route (pages/api), method GET.
- Handler trả `200` với JSON `{ status: 'ok', timestamp: new Date().toISOString() }`.
- Method khác GET → trả `405 Method Not Allowed`.
- Không đọc/ghi DB, không gọi service ngoài, không cần auth (theo SPEC — Out of Scope: không expose ở production, ghi rõ trong code/README nếu cần).

## Unit Tests (bắt buộc)
- Test file: `reponsitories/tokiwagi/src/pages/api/debug/ping.test.ts`
- Cover:
  - GET → 200, body có `status: 'ok'` và `timestamp` là ISO string hợp lệ (theo AC trong SPEC.md)
  - POST (hoặc method khác) → 405

## Non-Regression Table
| Tính năng hiện có | File liên quan | Cách verify |
|---|---|---|
| (không có) | (route mới, không đụng file nào khác) | N/A |

## Không được làm
- Không sửa file ngoài scope task này
- Không thêm route này vào bất kỳ luồng nghiệp vụ thật nào khác

## Definition of Done
- [ ] Build/lint pass
- [ ] Unit test pass
- [ ] Non-Regression verify đủ (N/A — không có luồng cũ bị ảnh hưởng)
