# KIDOKIDO — AI Agent Context

## Policies
Đọc và tuân thủ toàn bộ `POLICIES.md` trước khi hành động. Đây là luật, không thương lượng.

## Repositories
- `reponsitories/tokiwagi/` — Next.js 15, TypeScript, Express, Prisma/PostgreSQL, NextAuth, Redux, GMO Payment, AWS

## AI Agents

Pipeline: BA → Techlead → Dev → QA. Vai trò/quy trình đầy đủ: `.claude/agents/*.md` và `README.md`.

- `.claude/agents/ba-agent.md` — BA
- `.claude/agents/techlead-agent.md` — Techlead
- `.claude/agents/dev-agent.md` — Dev
- `.claude/agents/qa-agent.md` — QA

BA, Techlead, Dev bắt buộc làm đủ các bước ở mục Semantic Memory bên dưới trước khi thực thi (viết SPEC / tạo task / viết code) — không được nhảy thẳng vào việc khi chưa đọc.

## Semantic Memory — BẮT BUỘC dùng trước khi đọc code

Khi nhận task liên quan đến repo **tokiwagi**:

```bash
# Bước 0: Đọc mô tả dự án / bản đồ tính năng hiện có trước (tránh trùng/xung đột)
#   docs/domains/overview.md (tiếng Việt) hoặc knowledge/tokiwagi/semantic-index.json (~1,700 token)

# Bước 1: Tìm file liên quan theo keyword của task — KHÔNG đọc file trước khi query
node knowledge/tokiwagi/semantic-query.mjs "<keyword>" --limit 10

# Bước 2 (nếu biết layer): Thu hẹp phạm vi
node knowledge/tokiwagi/semantic-query.mjs "<keyword>" --layer "<layer>"

# Bước 3: Trước khi sửa interface/export — kiểm tra blast radius (BẮT BUỘC)
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

**Không query rộng** — keyword phải cụ thể theo task (vi phạm POLICIES §3). Bỏ qua các bước trên là vi phạm nguyên tắc "Đọc trước, hành động sau" (POLICIES §1).
