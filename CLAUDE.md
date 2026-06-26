# KIDOKIDO — AI Agent Context

## Policies
Đọc và tuân thủ toàn bộ `POLICIES.md` trước khi hành động. Đây là luật, không thương lượng.

## Repositories
- `reponsitories/tokiwagi/` — Next.js 15, TypeScript, Express, Prisma/PostgreSQL, NextAuth, Redux, GMO Payment, AWS

## Semantic Memory — BẮT BUỘC dùng trước khi đọc code

Khi nhận task liên quan đến repo **tokiwagi**, PHẢI chạy semantic query trước khi đọc bất kỳ file nào:

```bash
# Bước 1: Tìm file liên quan theo keyword của task
node knowledge/tokiwagi/semantic-query.mjs "<keyword>" --limit 10

# Bước 2 (nếu biết layer): Thu hẹp phạm vi
node knowledge/tokiwagi/semantic-query.mjs "<keyword>" --layer "<layer>"

# Bước 3 (khi sắp sửa file): Kiểm tra blast radius
node knowledge/tokiwagi/semantic-query.mjs --dependents "<file-path>"
```

**10 layers có sẵn:**
- `Frontend Pages` — src/pages/ (trừ api/)
- `Frontend Components` — src/components/
- `API Routes` — src/pages/api/
- `Backend Services` — src/services/, src/libs/, src/utils/
- `State Management` — src/stores/
- `Database` — prisma/
- `Configuration` — tsconfig, next.config, .env
- `Infrastructure` — docker/, jenkins/
- `Shared Utilities` — src/types/, src/constants/, src/contexts/
- `Styling` — *.scss, src/styles/

**Compact index** (~1,700 tokens, load khi cần định vị nhanh):
`knowledge/tokiwagi/semantic-index.json`

### Quy tắc dùng semantic memory

1. **Nhận task** → query keyword trước, KHÔNG đọc file ngay
2. **Query trả về file list** → đọc đúng những file đó
3. **Trước khi sửa interface/export** → query `--dependents` để biết blast radius
4. **Không query rộng** — keyword phải cụ thể theo task (vi phạm POLICIES §3)
