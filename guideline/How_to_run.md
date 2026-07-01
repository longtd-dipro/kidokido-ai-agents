# How To Run Doc — Tài liệu tính năng KIDOKIDO

Repo này có 2 hệ thống xem tài liệu độc lập, chạy song song trên 2 cổng khác nhau:

| Session | Công cụ | Xem gì | Cổng mặc định |
|---|---|---|---|
| 1 | MkDocs | Tài liệu tính năng dạng bài viết (`docs/`) — domain, flow, business rule, step → file code | tự chọn (vd `8765`) |
| 2 | understand-anything Dashboard | Knowledge graph trực quan (sơ đồ node/edge) — cấu trúc code (`knowledge-graph.json`) và domain/feature (`domain-graph.json`) | Vite tự chọn (thường `5173`) |

Có thể chạy đồng thời cả 2 vì khác cổng.

---

## Session 1 — Chạy MkDocs (tài liệu tính năng)

### Yêu cầu
- `mkdocs` đã cài (`mkdocs --version` để kiểm tra). Nếu chưa có: `brew install mkdocs` (macOS) hoặc `pip3 install mkdocs`.
- Theme dùng là `readthedocs` (có sẵn trong mkdocs core, không cần cài thêm gói).

### Chạy dev server (xem trực tiếp, tự reload khi sửa file)

```bash
# Từ thư mục gốc AI_AGENT_KIDOKIDO
mkdocs serve -a 127.0.0.1:8765
```

Mở trình duyệt tại **http://127.0.0.1:8765/**. MkDocs tự rebuild khi bạn sửa file trong `docs/` hoặc `mkdocs.yml` — chỉ cần refresh trình duyệt.

Nếu cổng 8765 đang bận, đổi sang cổng khác: `mkdocs serve -a 127.0.0.1:<port-khac>`. Bỏ hẳn `-a` sẽ dùng mặc định `127.0.0.1:8000`.

Dừng server: `Ctrl+C` trong terminal đang chạy `mkdocs serve`.

### Build tĩnh (không cần server, để archive/deploy)

```bash
mkdocs build
```

Output nằm ở `site/` (đã thêm vào `.gitignore`, không commit). Mở `site/index.html` trực tiếp bằng trình duyệt nếu không muốn chạy server.

### Cập nhật nội dung tài liệu tính năng khi code `tokiwagi` thay đổi

Tài liệu trong `docs/domains/*.md` được sinh tự động từ `knowledge/tokiwagi/domain-graph.json`. Khi code thay đổi nhiều (thêm/sửa/xóa tính năng), làm theo thứ tự sau:

```bash
# 1. Cập nhật knowledge graph gốc (chỉ phân tích lại file đã đổi)
/understand reponsitories/tokiwagi

# Hoặc rebuild toàn bộ nếu vừa refactor lớn
/understand reponsitories/tokiwagi --full

# 2. Trích xuất lại domain/feature graph từ knowledge graph
/understand-domain reponsitories/tokiwagi
# → ghi ra knowledge/tokiwagi/domain-graph.json (qua symlink .understand-anything)

# 3. Sinh lại docs/domains/*.md bằng tiếng Việt từ domain-graph.json
python3 knowledge/tokiwagi/generate-feature-docs.py

# 4. Xem lại
mkdocs serve -a 127.0.0.1:8765
```

**Lưu ý:** `generate-feature-docs.py` dịch tên/mô tả sang tiếng Việt bằng một bảng dịch cố định theo `id` node. Nếu `/understand-domain` sinh ra domain/flow/step **mới** (id chưa từng có), script sẽ in cảnh báo `MISSING` và tự động fallback dùng nguyên văn tiếng Anh cho node đó — cần bổ sung bản dịch thủ công vào dict `VI`/`TXT` đầu file script rồi chạy lại. Script cũng tự sinh sơ đồ Mermaid cho mỗi tính năng và gom bảng file kỹ thuật vào khối `<details>` thu gọn.

### Sơ đồ Mermaid — cần internet để render

Trang MkDocs nạp `mermaid.js` từ CDN (`unpkg.com`) qua `extra_javascript` trong `mkdocs.yml` (không cài `mkdocs-material`, tránh đụng vào Python env của Homebrew). Nếu máy không có internet khi mở trình duyệt, sơ đồ sẽ không render (vẫn xem được text bên dưới sơ đồ bình thường).

### Trang "Màn hình thực tế" (screenshot UI thật)

`docs/screens/admin.md` chứa screenshot + sơ đồ điều hướng chụp từ UI admin thật (copy từ `screen-flow/admin/`, xem `screen-flow/tools/` để chạy crawl lại nếu cần). Toàn bộ `docs/screens/` đã thêm vào `.gitignore` (có thể chứa dữ liệu môi trường test) — chỉ xem local qua `mkdocs serve`, không commit.

---

## Session 2 — Chạy Understand-Anything Dashboard (knowledge graph trực quan)

### Yêu cầu
- Node.js ≥ 22, `pnpm` ≥ 10.
- Claude Code CLI đã cài plugin `understand-anything` (đã bật sẵn trong `.claude/settings.json` của repo này).

### Chạy dashboard

Trong Claude Code, gõ lệnh (không phải terminal thường — đây là slash command của Claude Code):

```
/understand-dashboard reponsitories/tokiwagi
```

Claude sẽ tự cài dependency, build, khởi động Vite dev server nền, và in ra URL dạng:

```
🔑  Dashboard URL: http://127.0.0.1:<PORT>?token=<TOKEN>
```

Mở **đúng URL này (bao gồm cả phần `?token=...`)** trên trình duyệt — thiếu token sẽ bị chặn ở màn hình "Access Token Required".

Dashboard hiển thị cả hai graph nếu đã tạo:
- `knowledge-graph.json` — cấu trúc code (node = file, edge = import/call)
- `domain-graph.json` — domain/feature nghiệp vụ (node = domain/flow/step) — chọn view tương ứng trên giao diện dashboard.

### Dừng dashboard

Dashboard chạy nền (background process của Vite). Dừng bằng `Ctrl+C` trong terminal nếu chạy foreground, hoặc:

```bash
pkill -f "vite --host 127.0.0.1"
```

### Rebuild knowledge graph gốc (không phải domain graph)

Xem chi tiết đầy đủ (layers, query semantic memory, các flag) tại [`knowledge/tokiwagi/How_To_Use.md`](../knowledge/tokiwagi/How_To_Use.md).

```bash
# Incremental (chỉ file đã đổi, dựa theo git commit hash)
/understand reponsitories/tokiwagi

# Full rebuild
/understand reponsitories/tokiwagi --full
```

---

## Tóm tắt lệnh nhanh

```bash
# Session 1: MkDocs
mkdocs serve -a 127.0.0.1:8765          # → http://127.0.0.1:8765/

# Session 2: understand-anything Dashboard (gõ trong Claude Code)
/understand-dashboard reponsitories/tokiwagi   # → http://127.0.0.1:<port>?token=<token>
```
