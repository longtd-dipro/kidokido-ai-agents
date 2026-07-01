# KIDOKIDO — AI Agent System

Hệ thống AI Agent hỗ trợ phát triển dự án KIDOKIDO với 4 persona: **BA · Techlead · Dev · QA**.

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
├── docs/
│   └── features/
│       └── <feature-slug>/     ← 1 folder / feature
│           ├── SPEC.md         ← Output của BA Agent
│           └── tasks/
│               └── task-N.md   ← Output của Techlead Agent
├── .claude/
│   ├── agents/
│   │   ├── ba-agent.md         ← BA persona
│   │   ├── techlead-agent.md   ← Techlead persona
│   │   ├── dev-agent.md        ← Dev persona
│   │   └── qa-agent.md         ← QA persona
│   └── skills/
│       ├── business-analyst/
│       │   └── SKILL.md        ← Discovery/SPEC-writing methodology cho BA
│       ├── task-decomposition/
│       │   └── SKILL.md        ← Methodology cắt task cho Techlead
│       ├── tokiwagi-stack-conventions/
│       │   └── SKILL.md        ← Quy ước code Next.js/Prisma cho Dev
│       └── jest-testing-conventions/
│           └── SKILL.md        ← Quy ước viết unit test Jest cho QA
└── reponsitories/
    └── tokiwagi/               ← Source code dự án (repo riêng)
        └── .understand-anything → ../../knowledge/tokiwagi (symlink)
```

> `knowledge/` được commit vào `AI_AGENT_KIDOKIDO` — team clone repo này là có graph ngay.
> `reponsitories/tokiwagi/.understand-anything` là symlink → data thực nằm ở `knowledge/tokiwagi/`.
> Source code repo (`tokiwagi`) gitignore `.understand-anything` → không bị ảnh hưởng.

---

## 4 AI Agents

Pipeline: **BA → Techlead → Dev → QA**, mỗi bước có gate người dùng duyệt trước khi qua bước tiếp theo (xem [Pipeline Flow](#pipeline-flow) bên dưới).

| Agent | Dùng khi | Skill | Input | Output |
|---|---|---|---|---|
| BA | Có yêu cầu tính năng mới | `business-analyst` | Mô tả yêu cầu (lời) | `SPEC.md` |
| Techlead | SPEC.md đã được duyệt | `task-decomposition` | `SPEC.md` | `tasks/task-N.md` |
| Dev | Có task-N.md (hoặc SPEC.md) | `tokiwagi-stack-conventions` | `task-N.md` | Source code + unit test |
| QA | Dev implement xong | `jest-testing-conventions` | `task-N.md` hoặc module | Unit test + QA report |

Gọi agent bằng ngôn ngữ tự nhiên ("Bạn là ... Agent, ...") — không có slash command riêng, mọi agent tự đọc skill + semantic graph tương ứng khi được invoke (xem chi tiết từng agent bên dưới).

### BA Agent — Phân tích yêu cầu

**Dùng khi:** Có yêu cầu tính năng mới, cần viết SPEC, cần phân tích business logic.

**Skill dùng:** `.claude/skills/business-analyst/SKILL.md` (discovery, phân biệt business rule vs UI rule, viết AC dạng Given-When-Then).

**Cách gọi:**
```
Bạn là BA Agent. [Mô tả yêu cầu]
```

Ví dụ thực tế:
```
Bạn là BA Agent. Thêm tính năng cho phép user hủy vé tháng đang active
và được hoàn lại một phần tiền theo tỷ lệ ngày chưa dùng.
```

**BA Agent sẽ:**
1. Đọc skill `business-analyst`, query knowledge graph để hiểu những gì đã có trong codebase (vd. domain "Booking & Reservation Management" đã có sẵn luồng hủy vé thường, chỉ khác ở phần hoàn tiền)
2. Hỏi 10 câu checklist (actor, trigger, happy path, edge case, data, API, UI, permission, integration, rollback) — vd. hỏi rõ "tỷ lệ hoàn tiền tính theo ngày hay theo lượt còn lại?"
3. Viết SPEC.md theo cấu trúc cố định (Mô tả nghiệp vụ, Actors, Happy Path, Edge Cases, Acceptance Criteria, Screens, Out of Scope, Open Questions)

**Output:** `docs/features/<feature-slug>/SPEC.md` — vd. `docs/features/huy-ve-thang-hoan-tien/SPEC.md`.

---

### Techlead Agent — Phân rã task

**Dùng khi:** SPEC.md đã được user duyệt, cần cắt ra task cụ thể cho Dev.

**Skill dùng:** `.claude/skills/task-decomposition/SKILL.md` (INVEST criteria, phân nhóm theo layer, dependency detection, estimation).

**Cách gọi:**
```
Bạn là Techlead Agent. Đọc SPEC.md và tạo task: [đường dẫn SPEC.md]
```

Ví dụ thực tế:
```
Bạn là Techlead Agent. Đọc SPEC.md và tạo task: docs/features/huy-ve-thang-hoan-tien/SPEC.md
```

**Techlead Agent sẽ:**
1. Đọc SPEC.md + skill `task-decomposition`
2. Query knowledge graph để xác định chính xác file/module bị ảnh hưởng (vd. tìm ra `src/services/gmo.service.ts`, `src/pages/api/user/bookings/cancel.ts` liên quan tới luồng hủy vé/hoàn tiền)
3. Check blast radius (`--dependents`) cho từng file dự kiến sửa — vd. nếu `cancel.ts` đang được nhiều luồng khác gọi, cảnh báo user trước
4. Cắt task theo INVEST criteria, mỗi task implementable trong 1 session (~4-8h) — vd. tách "task-1: tính tỷ lệ hoàn tiền (service)" và "task-2: API endpoint gọi service + validate"
5. Viết task file(s) kèm Context, Yêu cầu implement, Non-Regression Table, Definition of Done

**Output:** `docs/features/<feature-slug>/tasks/task-N.md`.

**Không được:** Sửa source code, commit/push.

---

### Dev Agent — Implement code

**Dùng khi:** Đã có task file từ Techlead (hoặc SPEC.md, nếu giao task trực tiếp), cần implement tính năng hoặc fix bug.

**Skill dùng:** `.claude/skills/tokiwagi-stack-conventions/SKILL.md` (Prisma, API Routes, Service layer, Redux/TanStack Query — đúng stack thật của tokiwagi).

**Cách gọi:**
```
Bạn là Dev Agent. Implement task: [đường dẫn task-N.md]
```

Ví dụ thực tế:
```
Bạn là Dev Agent. Implement task: docs/features/huy-ve-thang-hoan-tien/tasks/task-1.md
```

**Dev Agent sẽ:**
1. Đọc skill `tokiwagi-stack-conventions` + task-N.md (hoặc SPEC.md nếu chưa có task file)
2. Query knowledge graph tìm đúng file cần sửa
3. Check blast radius trước khi thay đổi interface
4. Implement trong scope — không refactor ngoài task, viết Unit Test kèm theo (theo yêu cầu trong task-N.md)
5. Báo cáo khi xong, chờ user confirm trước khi commit

**Không được:** Tự commit, tự push, sửa file ngoài scope.

---

### QA Agent — Kiểm thử

**Dùng khi:** Dev implement xong, cần viết test hoặc kiểm tra chất lượng.

**Skill dùng:** `.claude/skills/jest-testing-conventions/SKILL.md` (mock strategy, cấu trúc AAA, map AC → test case).

**Cách gọi:**
```
Bạn là QA Agent. Viết test cho: [tên module, đường dẫn file, hoặc task-N.md]
```

Ví dụ thực tế:
```
Bạn là QA Agent. Viết test cho: docs/features/huy-ve-thang-hoan-tien/tasks/task-1.md
```

**QA Agent sẽ:**
1. Đọc skill `jest-testing-conventions`, query knowledge graph tìm file implementation và test files đã có
2. Query `--imports` để biết dependencies cần mock (vd. mock `gmo.service.ts` khi test hàm tính hoàn tiền, KHÔNG mock Prisma)
3. Viết unit test với Jest, map từng Acceptance Criteria trong SPEC/task sang 1 test case
4. Chạy test suite, báo cáo coverage
5. Viết QA report nếu phát hiện bug

**Không được:** Sửa source code logic, chỉ được sửa test files.

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
│  OUTPUT: docs/features/<feature-slug>/SPEC.md                       │
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
│  BƯỚC 2 · TECHLEAD AGENT — Phân rã task                            │
│                                                                     │
│  1. Đọc SPEC.md + skill task-decomposition                          │
│  2. Query semantic graph     ←  xác định chính xác file/module      │
│  3. Check blast radius       ←  --dependents cho từng file dự kiến sửa│
│  4. Cắt task theo INVEST     →  mỗi task ≤ 8h, testable             │
│  5. Viết task-N.md           →  Context, Yêu cầu, Non-Regression, DoD│
│                                                                     │
│  OUTPUT: docs/features/<feature-slug>/tasks/task-N.md               │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                        User review task(s)
                               │
                    ┌──────────┴──────────┐
                    │ Cần chỉnh?          │ OK
                    ▼                     ▼
              Techlead Agent              │
              sửa task    ───────────────►│
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  BƯỚC 3 · DEV AGENT — Implement                                     │
│                                                                     │
│  1. Đọc task-N.md            ←  scope, file liên quan, blast radius │
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
│  BƯỚC 4 · QA AGENT — Kiểm thử                                      │
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
         ┌─────────────┬───┴──────────┬─────────────┐
         ▼             ▼              ▼             ▼
      BA Agent   Techlead Agent    Dev Agent     QA Agent
   query domain  query scope +   query scope   query deps
   trước SPEC    blast radius    trước code    trước test
                 trước task
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
- Stack cứng: Prisma · REST · TanStack Query v5 · Redux Toolkit v2
