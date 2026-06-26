# KIDOKIDO — AI Agent System

Hệ thống AI Agent hỗ trợ phát triển dự án KIDOKIDO với 3 persona: **BA · Dev · QA**.

---

## Tổng quan

```
AI_AGENT_KIDOKIDO/              ← repo này (clone để dùng AI agents)
├── CLAUDE.md                   ← Context tự động load cho mọi session
├── POLICIES.md                 ← Luật bất biến cho mọi agent
├── README.md                   ← File này
├── knowledge/
│   └── tokiwagi/               ← Knowledge graph (commit vào repo này)
│       ├── knowledge-graph.json   ← Semantic memory (full, 884KB)
│       ├── semantic-index.json    ← Semantic memory (compact, 6.7KB)
│       ├── semantic-query.mjs     ← Query script
│       └── How_To_Use.md         ← Hướng dẫn chạy graph server
├── .claude/
│   └── agents/
│       ├── ba-agent.md         ← BA persona
│       ├── dev-agent.md        ← Dev persona
│       └── qa-agent.md         ← QA persona
└── reponsitories/
    └── tokiwagi/               ← Source code dự án (repo riêng)
        └── .understand-anything → ../../knowledge/tokiwagi (symlink)
```

> `knowledge/` được commit vào `AI_AGENT_KIDOKIDO` — team clone repo này là có graph ngay.
> `reponsitories/tokiwagi/.understand-anything` là symlink → data thực nằm ở `knowledge/tokiwagi/`.
> Source code repo (`tokiwagi`) gitignore `.understand-anything` → không bị ảnh hưởng.

---

## 3 AI Agents

### BA Agent — Phân tích yêu cầu

**Dùng khi:** Có yêu cầu tính năng mới, cần viết SPEC, cần phân tích business logic.

**Cách gọi:**
```
Bạn là BA Agent. [Mô tả yêu cầu]
```

**BA Agent sẽ:**
1. Query knowledge graph để hiểu những gì đã có trong codebase
2. Hỏi 10 câu checklist (actor, trigger, happy path, edge case, data, API, UI, permission, integration, rollback)
3. Viết SPEC.md mô tả yêu cầu rõ ràng

**Output:** File `SPEC.md` trong thư mục task tương ứng.

---

### Dev Agent — Implement code

**Dùng khi:** Đã có SPEC, cần implement tính năng hoặc fix bug.

**Cách gọi:**
```
Bạn là Dev Agent. Implement task: [tên task hoặc đường dẫn SPEC.md]
```

**Dev Agent sẽ:**
1. Đọc SPEC.md
2. Query knowledge graph tìm đúng file cần sửa
3. Check blast radius trước khi thay đổi interface
4. Implement trong scope — không refactor ngoài task
5. Báo cáo khi xong, chờ user confirm trước khi commit

**Không được:** Tự commit, tự push, sửa file ngoài scope.

---

### QA Agent — Kiểm thử

**Dùng khi:** Dev implement xong, cần viết test hoặc kiểm tra chất lượng.

**Cách gọi:**
```
Bạn là QA Agent. Viết test cho: [tên module hoặc đường dẫn file]
```

**QA Agent sẽ:**
1. Query knowledge graph tìm file implementation và test files đã có
2. Query `--imports` để biết dependencies cần mock
3. Viết unit test với Jest
4. Chạy test suite, báo cáo coverage
5. Viết QA report nếu phát hiện bug

**Không được:** Sửa source code logic, chỉ được sửa test files.

---

## Knowledge Graph (Semantic Memory)

Toàn bộ codebase `tokiwagi` đã được phân tích và lưu thành knowledge graph.

**Vị trí:**
```
knowledge/tokiwagi/         ← data thực (commit vào repo này)
reponsitories/tokiwagi/.understand-anything  ← symlink → ../../knowledge/tokiwagi
```

**Xem hướng dẫn chi tiết:** [`knowledge/tokiwagi/How_To_Use.md`](knowledge/tokiwagi/How_To_Use.md)

**Mở dashboard:**
```
/understand-dashboard reponsitories/tokiwagi
```

**Query nhanh (không cần dashboard):**
```bash
# Tìm file liên quan đến feature
node knowledge/tokiwagi/semantic-query.mjs "booking" --limit 10

# Tìm trong layer cụ thể
node knowledge/tokiwagi/semantic-query.mjs "auth" --layer "API Routes"
```

---

## Khi có yêu cầu mới — Làm theo thứ tự này

> Không bỏ qua bước nào. Không để Dev implement khi chưa có SPEC được confirm.

## Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        YÊU CẦU MỚI TỪ USER                         │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  BƯỚC 1 · BA AGENT — Phân tích & Viết SPEC                         │
│                                                                     │
│  1. Query semantic graph     ←  "Đã có gì liên quan trong codebase?"│
│  2. Hỏi 10 câu checklist    ←  actor / trigger / edge case / ...   │
│  3. Viết SPEC.md             →  mô tả AC, data model, API, UI       │
│                                                                     │
│  OUTPUT: SPEC.md                                                    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                        User review SPEC
                               │
                    ┌──────────┴──────────┐
                    │ Cần chỉnh?          │ OK
                    ▼                     ▼
              BA Agent                   │
              sửa SPEC   ───────────────►│
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  BƯỚC 2 · DEV AGENT — Implement                                     │
│                                                                     │
│  1. Đọc SPEC.md              ←  scope, AC, data model               │
│  2. Query semantic graph     ←  tìm đúng file cần sửa               │
│  3. Check blast radius       ←  --dependents trước khi đổi interface│
│  4. Implement trong scope    →  code, không refactor ngoài task      │
│  5. Báo cáo xong             →  chờ user confirm                    │
│                                                                     │
│  OUTPUT: source code đã implement                                   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                        User review code
                               │
                    ┌──────────┴──────────┐
                    │ Cần sửa?            │ OK
                    ▼                     ▼
              Dev Agent                  │
              sửa code   ───────────────►│
                                         │
                              User confirm commit
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  BƯỚC 3 · QA AGENT — Kiểm thử                                      │
│                                                                     │
│  1. Query semantic graph     ←  tìm file impl + test files đã có    │
│  2. Query --imports          ←  biết dependencies cần mock          │
│  3. Viết unit test (Jest)    →  cover happy path + edge case        │
│  4. Chạy test suite          →  pnpm test --coverage                │
│  5. Viết QA report           →  pass / fail / bug found             │
│                                                                     │
│  OUTPUT: test files + QA report                                     │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │ Có bug?             │ All pass
                    ▼                     ▼
              Dev Agent            DONE ✅
              fix bug
              QA re-test
```

### Semantic Memory trong Pipeline

```
                    knowledge-graph.json  (884KB — không load thẳng)
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           BA Agent    Dev Agent    QA Agent
        query domain  query scope  query deps
        trước SPEC    trước code   trước test
              │            │            │
      semantic-query.mjs được gọi tự động
      → chỉ trả về file liên quan (~500 tokens)
      → agent đọc đúng file, không mò codebase
```

---

## Policies

Toàn bộ luật hoạt động của agents xem tại [`POLICIES.md`](POLICIES.md).

Tóm tắt nhanh:
- Chỉ **Dev** được sửa source code
- Mọi agent phải **query knowledge graph trước** khi đọc file
- Không ai được tự `git push`
- Không đưa source code ra ngoài (public tools, external API)
- Stack cứng: TypeORM · REST · TanStack Query v5 · Redux Toolkit v2
