# How To Use — KIDOKIDO Knowledge Graph

## Yêu cầu

- Node.js >= 22 (`node -v`)
- pnpm >= 10 (`pnpm -v`)
- Claude Code CLI đã cài understand-anything plugin

---

## 1. Chạy Dashboard (xem knowledge graph)

```bash
# Mở Claude Code trong thư mục gốc
cd AI_AGENT_KIDOKIDO

# Gõ lệnh trong Claude Code
/understand-dashboard reponsitories/tokiwagi
```

Sau khi chạy, Claude sẽ in ra URL dạng:
```
http://127.0.0.1:5173/?token=<TOKEN>
```

Mở URL đó trên browser để xem dashboard.

---

## 2. Rebuild Knowledge Graph (khi code thay đổi)

### Full rebuild (xây lại từ đầu)

```bash
/understand reponsitories/tokiwagi --full
```

### Incremental update (chỉ re-analyze files đã thay đổi)

```bash
/understand reponsitories/tokiwagi
```
Plugin tự so sánh git commit hash — chỉ phân tích lại files đã sửa kể từ lần build trước.

---

## 3. Query Semantic Memory (dùng trong AI agents)

Không cần mở dashboard, dùng trực tiếp trong terminal:

```bash
cd reponsitories/tokiwagi

# Tìm file theo keyword
node .understand-anything/semantic-query.mjs "booking" --limit 10

# Tìm trong layer cụ thể
node .understand-anything/semantic-query.mjs "payment" --layer "API Routes"

# Xem file nào đang import file này (blast radius)
node .understand-anything/semantic-query.mjs --dependents "src/services/gmo.service.ts"

# Xem file này đang import những gì
node .understand-anything/semantic-query.mjs --imports "src/pages/api/bookings/index.ts"

# Filter theo tag
node .understand-anything/semantic-query.mjs --tag "auth" --limit 10

# Kết hợp keyword + layer
node .understand-anything/semantic-query.mjs "admin" --layer "Frontend Pages" --limit 10
```

---

## 4. Các file quan trọng

| File | Mô tả | Token |
|---|---|---|
| `knowledge-graph.json` | Full graph (1,632 nodes, 1,654 edges) | ~220K — không load thẳng |
| `semantic-index.json` | Compact index theo layer + tag | ~1,700 — load nhanh |
| `semantic-query.mjs` | Script query graph | 0 input, ~500 output |
| `meta.json` | Git commit hash + timestamp của lần build | — |

---

## 5. Layers có sẵn

| Layer | Đường dẫn tương ứng |
|---|---|
| `Frontend Pages` | `src/pages/` (trừ api/) |
| `Frontend Components` | `src/components/` |
| `API Routes` | `src/pages/api/` |
| `Backend Services` | `src/services/`, `src/libs/`, `src/utils/` |
| `State Management` | `src/stores/` |
| `Database` | `prisma/` |
| `Configuration` | tsconfig, next.config, .env |
| `Infrastructure` | `docker/`, `jenkins/` |
| `Shared Utilities` | `src/types/`, `src/constants/`, `src/contexts/` |
| `Styling` | `*.scss`, `src/styles/` |

---

## 6. Lưu ý

- Dashboard chạy ở background — nhấn `Ctrl+C` trong terminal để dừng
- Mỗi lần chạy dashboard sinh ra token mới — URL cũ sẽ hết hạn
- Nếu port 5173 bị chiếm, Vite tự chọn port tiếp theo (5174, 5175,...)
- Semantic query cần Node.js >= 22 và `knowledge-graph.json` phải tồn tại
