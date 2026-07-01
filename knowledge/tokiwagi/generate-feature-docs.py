#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Vietnamese docs/domains/*.md from knowledge/tokiwagi/domain-graph.json"""
import json
import os

# knowledge/tokiwagi/generate-feature-docs.py -> repo root is two levels up
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRAPH_PATH = os.path.join(ROOT, "knowledge/tokiwagi/domain-graph.json")
DOCS_DOMAINS_DIR = os.path.join(ROOT, "docs/domains")

with open(GRAPH_PATH, encoding="utf-8") as f:
    graph = json.load(f)

nodes = {n["id"]: n for n in graph["nodes"]}
edges = graph["edges"]

# ---- Vietnamese translations, keyed by node id: {"name": ..., "summary": ...} ----
VI = {
"domain:booking-reservation-management": {"name": "Quản lý Đặt vé & Đặt chỗ", "summary": "Xử lý toàn bộ vòng đời đặt chỗ tại cơ sở: tạo đặt vé online và offline, mua vé tháng/vé theo lượt, quản lý lịch sử đặt vé, hủy vé, và theo dõi hàng chờ/chỗ trống. Đây là domain nghiệp vụ cốt lõi của ứng dụng, xoay quanh tenant, vé và người dùng."},
"flow:create-online-booking": {"name": "Tạo đặt vé trực tuyến", "summary": "Người dùng chọn tenant, vé và ngày, nhập số lượng/độ tuổi, đồng ý điều khoản miễn trừ trách nhiệm, thanh toán qua GMO/thẻ tín dụng, và nhận xác nhận đặt vé."},
"step:create-online-booking:select-tenant-ticket-date": {"name": "Chọn Tenant, Vé, Ngày", "summary": "Người dùng chọn tenant, loại vé và ngày đặt trong form đặt vé online."},
"step:create-online-booking:enter-quantity-ages": {"name": "Nhập Số lượng & Độ tuổi", "summary": "Người dùng nhập số lượng người lớn/trẻ em và độ tuổi cho đặt vé."},
"step:create-online-booking:accept-disclaimer-terms": {"name": "Đồng ý Điều khoản Miễn trừ", "summary": "Người dùng xem và đồng ý điều khoản miễn trừ trách nhiệm của cơ sở trước khi đặt vé."},
"step:create-online-booking:enter-credit-card": {"name": "Nhập Thẻ tín dụng", "summary": "Người dùng nhập hoặc chọn thẻ tín dụng đã lưu để thanh toán online."},
"step:create-online-booking:submit-booking-request": {"name": "Gửi Yêu cầu Đặt vé", "summary": "Yêu cầu đặt vé được gửi đến API bookings của user để tạo mới."},
"step:create-online-booking:process-gmo-payment": {"name": "Xử lý Thanh toán GMO", "summary": "Cổng thanh toán GMO xác thực và ghi nhận thanh toán online cho đặt vé."},
"step:create-online-booking:show-booking-confirmation": {"name": "Hiển thị Xác nhận Đặt vé", "summary": "Hệ thống hiển thị màn hình xác nhận tóm tắt đặt vé đã hoàn tất."},
"step:create-online-booking:show-booking-completion": {"name": "Hiển thị Hoàn tất Đặt vé", "summary": "Trang hoàn tất đặt vé được hiển thị, kết thúc luồng đặt vé online."},

"flow:create-offline-booking": {"name": "Tạo đặt vé Offline/Admin", "summary": "Admin hoặc nhân viên cơ sở tạo đặt vé thay cho khách vãng lai, chọn loại vé, tính giá, và xác nhận thanh toán offline."},
"step:create-offline-booking:open-offline-booking-form": {"name": "Mở Form Đặt vé Offline", "summary": "Nhân viên mở form đặt vé offline để bắt đầu đặt vé cho khách vãng lai."},
"step:create-offline-booking:select-ticket-plan-type": {"name": "Chọn Loại Vé", "summary": "Nhân viên chọn loại vé như vé tháng hoặc vé theo lượt."},
"step:create-offline-booking:enter-booking-quantities": {"name": "Nhập Số lượng Đặt vé", "summary": "Nhân viên nhập số lượng người lớn/trẻ em và độ tuổi cho đặt vé vãng lai."},
"step:create-offline-booking:calculate-total-price": {"name": "Tính Tổng Giá", "summary": "Hệ thống tính tổng giá đặt vé bao gồm giảm giá cho đặt vé offline."},
"step:create-offline-booking:confirm-offline-booking": {"name": "Xác nhận Đặt vé Offline", "summary": "Nhân viên xem lại và xác nhận thông tin đặt vé offline trước khi gửi."},
"step:create-offline-booking:submit-offline-booking": {"name": "Gửi Đặt vé Offline", "summary": "Đặt vé offline được gửi và lưu qua API bookings của admin."},
"step:create-offline-booking:persist-booking-record": {"name": "Lưu Bản ghi Đặt vé", "summary": "Bản ghi đặt vé được lưu cùng các trường tính toán qua các utility booking phía server."},

"flow:manage-booking-history": {"name": "Quản lý Lịch sử Đặt vé", "summary": "Người dùng xem các đặt vé trong quá khứ và sắp tới, xem chi tiết, cập nhật thông tin đặt vé, hoặc hủy đặt vé hiện có."},
"step:manage-booking-history:list-booking-history": {"name": "Danh sách Lịch sử Đặt vé", "summary": "Người dùng xem danh sách lịch sử đặt vé có phân trang."},
"step:manage-booking-history:view-booking-detail": {"name": "Xem Chi tiết Đặt vé", "summary": "Người dùng xem đầy đủ chi tiết của một đặt vé cụ thể theo ID."},
"step:manage-booking-history:update-booking-info": {"name": "Cập nhật Thông tin Đặt vé", "summary": "Người dùng cập nhật thông tin có thể chỉnh sửa trên đặt vé hiện có."},
"step:manage-booking-history:cancel-booking": {"name": "Hủy Đặt vé", "summary": "Người dùng hủy đặt vé qua API cancel bookings."},
"step:manage-booking-history:show-cancel-success": {"name": "Hiển thị Hủy Thành công", "summary": "Hệ thống xác nhận với người dùng việc hủy đặt vé thành công."},

"flow:booking-queue-vacancy": {"name": "Hàng chờ Đặt vé & Theo dõi Chỗ trống", "summary": "Admin theo dõi và quản lý hàng chờ đặt vé theo thời gian thực (đang chờ/đang gọi/đã hủy) và trạng thái chỗ trống của cơ sở, với cron job tự động hết hạn các mục hàng chờ quá hạn."},
"step:booking-queue-vacancy:view-booking-queue": {"name": "Xem Hàng chờ Đặt vé", "summary": "Admin xem dashboard hàng chờ đặt vé hiện tại."},
"step:booking-queue-vacancy:fetch-waiting-bookings": {"name": "Lấy Đặt vé Đang chờ", "summary": "Hệ thống lấy các đặt vé đang ở trạng thái chờ trong hàng chờ."},
"step:booking-queue-vacancy:call-next-booking": {"name": "Gọi Đặt vé Tiếp theo", "summary": "Admin gọi đặt vé tiếp theo trong hàng chờ để tiến hành check-in."},
"step:booking-queue-vacancy:auto-cancel-overdue": {"name": "Tự động Hủy Quá hạn", "summary": "Hệ thống tự động hủy các đặt vé ở quá lâu trong hàng chờ mà không phản hồi."},
"step:booking-queue-vacancy:view-vacancy-status": {"name": "Xem Trạng thái Chỗ trống", "summary": "Admin xem trạng thái chỗ trống hiện tại của cơ sở, tính từ các đặt vé đang hoạt động."},
"step:booking-queue-vacancy:cron-process-overdue-queue": {"name": "Cron Xử lý Hàng chờ Quá hạn", "summary": "Cron job theo lịch xử lý và làm hết hạn các đặt vé ở trạng thái đang gọi quá hạn."},

"flow:buy-ticket-plans": {"name": "Mua Vé Tháng/Vé Theo lượt", "summary": "Người dùng xem và mua các gói vé định kỳ (vé tháng hoặc vé theo lượt) cho phép đặt vé nhiều lần trong tương lai theo giới hạn sử dụng."},
"step:buy-ticket-plans:browse-monthly-ticket-page": {"name": "Xem Trang Vé Tháng", "summary": "Người dùng xem trang giới thiệu mua vé tháng."},
"step:buy-ticket-plans:browse-times-limit-ticket-page": {"name": "Xem Trang Vé Theo lượt", "summary": "Người dùng xem trang giới thiệu mua vé theo lượt."},
"step:buy-ticket-plans:fill-monthly-booking-form": {"name": "Điền Form Đặt Vé Tháng", "summary": "Người dùng điền form đặt vé tháng để cấu hình mua gói vé."},
"step:buy-ticket-plans:check-monthly-ticket-usage": {"name": "Kiểm tra Sử dụng Vé Tháng", "summary": "Hệ thống kiểm tra vé tháng đã được sử dụng ở tenant khác chưa trước khi cho phép mua."},
"step:buy-ticket-plans:show-monthly-completion": {"name": "Hiển thị Hoàn tất Vé Tháng", "summary": "Hệ thống hiển thị xác nhận hoàn tất đặt vé tháng."},

"domain:user-account-authentication": {"name": "Tài khoản Người dùng & Xác thực", "summary": "Quản lý danh tính người dùng cuối: đăng ký kèm xác thực email, đăng nhập/đăng xuất qua NextAuth, khôi phục mật khẩu và mở khóa tài khoản, và tự quản lý thông tin cá nhân, thẻ tín dụng, tenant yêu thích."},
"flow:user-signup-verification": {"name": "Đăng ký & Xác thực Email", "summary": "Người dùng mới đăng ký tài khoản, hệ thống kiểm tra email trùng lặp, tạo tài khoản, và gửi email xác thực mà người dùng phải xác nhận."},
"step:user-signup-verification:fill-signup-form": {"name": "Điền Form Đăng ký", "summary": "Người dùng điền form đăng ký với thông tin cá nhân và tài khoản."},
"step:user-signup-verification:check-existing-email": {"name": "Kiểm tra Email Đã tồn tại", "summary": "Hệ thống kiểm tra email nhập vào đã được đăng ký hay chưa."},
"step:user-signup-verification:create-account": {"name": "Tạo Tài khoản", "summary": "Tài khoản người dùng mới được tạo qua API signup."},
"step:user-signup-verification:send-verification-email": {"name": "Gửi Email Xác thực", "summary": "Hệ thống gửi link xác thực email cho người dùng mới."},
"step:user-signup-verification:verify-email-token": {"name": "Xác thực Token Email", "summary": "Người dùng xác nhận email bằng cách truy cập link token xác thực."},
"step:user-signup-verification:show-signup-success": {"name": "Hiển thị Đăng ký Thành công", "summary": "Hệ thống hiển thị trang xác nhận đăng ký thành công."},

"flow:login-password-recovery": {"name": "Đăng nhập & Khôi phục Mật khẩu", "summary": "Người dùng đăng nhập qua NextAuth credentials, hoặc khôi phục truy cập qua các luồng quên mật khẩu, đặt lại mật khẩu, và mở khóa tài khoản khi bị khóa."},
"step:login-password-recovery:submit-signin-credentials": {"name": "Gửi Thông tin Đăng nhập", "summary": "Người dùng gửi email/mật khẩu trên trang đăng nhập."},
"step:login-password-recovery:authenticate-nextauth": {"name": "Xác thực qua NextAuth", "summary": "NextAuth xác minh thông tin đăng nhập và thiết lập phiên làm việc."},
"step:login-password-recovery:request-password-reset": {"name": "Yêu cầu Đặt lại Mật khẩu", "summary": "Người dùng yêu cầu link đặt lại mật khẩu qua chức năng quên mật khẩu."},
"step:login-password-recovery:reset-password-with-token": {"name": "Đặt lại Mật khẩu bằng Token", "summary": "Người dùng đặt mật khẩu mới bằng token đặt lại được gửi qua email."},
"step:login-password-recovery:request-unlock-account": {"name": "Yêu cầu Mở khóa Tài khoản", "summary": "Người dùng bị khóa tài khoản yêu cầu email mở khóa sau nhiều lần đăng nhập thất bại."},
"step:login-password-recovery:unlock-account-token": {"name": "Mở khóa Tài khoản bằng Token", "summary": "Người dùng mở khóa tài khoản bằng cách xác nhận link token mở khóa."},

"flow:manage-personal-info": {"name": "Quản lý Thông tin Cá nhân & Tùy chọn", "summary": "Người dùng đã xác thực quản lý hồ sơ của mình: thông tin cá nhân, đổi email/mật khẩu, thẻ tín dụng đã lưu, tenant yêu thích, và xóa tài khoản."},
"step:manage-personal-info:view-personal-info": {"name": "Xem Thông tin Cá nhân", "summary": "Người dùng xem trang thông tin cá nhân."},
"step:manage-personal-info:update-personal-info": {"name": "Cập nhật Thông tin Cá nhân", "summary": "Người dùng cập nhật thông tin hồ sơ cá nhân."},
"step:manage-personal-info:change-email": {"name": "Đổi Email", "summary": "Người dùng đổi email tài khoản, kích hoạt bước xác thực lại."},
"step:manage-personal-info:change-password": {"name": "Đổi Mật khẩu", "summary": "Người dùng đổi mật khẩu tài khoản từ cài đặt thông tin cá nhân."},
"step:manage-personal-info:manage-credit-cards": {"name": "Quản lý Thẻ Tín dụng", "summary": "Người dùng xem và quản lý thẻ tín dụng đã lưu."},
"step:manage-personal-info:manage-favorite-tenants": {"name": "Quản lý Tenant Yêu thích", "summary": "Người dùng xem và quản lý danh sách cơ sở (tenant) yêu thích."},
"step:manage-personal-info:delete-account": {"name": "Xóa Tài khoản", "summary": "Người dùng xóa tài khoản sau khi xác nhận hộp thoại cảnh báo."},

"domain:admin-facility-management": {"name": "Quản lý Cơ sở & Nội dung (Admin)", "summary": "Quản trị back-office cho đơn vị vận hành cơ sở: quản lý tenant (cơ sở), vé/gói vé, tài khoản nhân viên, thông báo tin tức, điều khoản miễn trừ, và cài đặt app/email qua bảng điều khiển admin."},
"flow:tenant-management": {"name": "Quản lý Tenant (Cơ sở)", "summary": "Admin tạo, xem, sửa và liệt kê các tenant (cơ sở) chứa vé có thể đặt."},
"step:tenant-management:list-tenants": {"name": "Danh sách Tenant", "summary": "Admin xem danh sách tenant đã đăng ký."},
"step:tenant-management:create-tenant": {"name": "Tạo Tenant", "summary": "Admin tạo bản ghi tenant cơ sở mới."},
"step:tenant-management:edit-tenant": {"name": "Sửa Tenant", "summary": "Admin sửa cấu hình tenant hiện có."},
"step:tenant-management:view-tenant-detail": {"name": "Xem Chi tiết Tenant", "summary": "Admin xem đầy đủ chi tiết của một tenant cụ thể."},
"step:tenant-management:persist-tenant": {"name": "Lưu Tenant", "summary": "Dữ liệu tenant được lưu qua API admin tenants."},

"flow:ticket-management": {"name": "Quản lý Vé (Gói vé)", "summary": "Admin quản lý các gói vé có thể đặt theo từng tenant, bao gồm cài đặt giá/giảm giá và lịch đặt vé."},
"step:ticket-management:list-tickets": {"name": "Danh sách Vé", "summary": "Admin xem danh sách gói vé."},
"step:ticket-management:create-ticket": {"name": "Tạo Vé", "summary": "Admin tạo gói vé mới."},
"step:ticket-management:edit-ticket": {"name": "Sửa Vé", "summary": "Admin sửa cấu hình gói vé hiện có."},
"step:ticket-management:configure-booking-schedules": {"name": "Cấu hình Lịch Đặt vé", "summary": "Admin cấu hình khung thời gian lịch đặt vé cho gói vé."},
"step:ticket-management:persist-ticket": {"name": "Lưu Vé", "summary": "Dữ liệu gói vé được lưu qua API admin tickets."},

"flow:staff-management": {"name": "Quản lý Tài khoản Nhân viên", "summary": "Admin quản lý tài khoản nhân viên vận hành bảng điều khiển admin và công cụ quét POS."},
"step:staff-management:list-staff": {"name": "Danh sách Nhân viên", "summary": "Admin xem danh sách tài khoản nhân viên."},
"step:staff-management:create-staff": {"name": "Tạo Nhân viên", "summary": "Admin tạo tài khoản nhân viên mới."},
"step:staff-management:edit-staff": {"name": "Sửa Nhân viên", "summary": "Admin sửa tài khoản nhân viên hiện có."},
"step:staff-management:persist-staff": {"name": "Lưu Nhân viên", "summary": "Dữ liệu tài khoản nhân viên được lưu qua API admin staffs."},

"flow:news-disclaimer-management": {"name": "Quản lý Tin tức & Điều khoản Miễn trừ", "summary": "Admin đăng thông báo tin tức hiển thị cho người dùng và quản lý điều khoản miễn trừ trách nhiệm pháp lý hiển thị trong quá trình đặt vé."},
"step:news-disclaimer-management:list-news": {"name": "Danh sách Tin tức", "summary": "Admin xem danh sách tin tức đã đăng."},
"step:news-disclaimer-management:create-news": {"name": "Tạo Tin tức", "summary": "Admin tạo thông báo tin tức mới."},
"step:news-disclaimer-management:edit-news": {"name": "Sửa Tin tức", "summary": "Admin sửa thông báo tin tức hiện có."},
"step:news-disclaimer-management:manage-disclaimers": {"name": "Quản lý Điều khoản Miễn trừ", "summary": "Admin quản lý nội dung điều khoản miễn trừ hiển thị trong luồng đặt vé."},
"step:news-disclaimer-management:persist-news": {"name": "Lưu Tin tức", "summary": "Nội dung tin tức được lưu qua API admin news."},

"flow:app-email-settings-management": {"name": "Quản lý Cài đặt App & Email", "summary": "Admin cấu hình cài đặt ứng dụng toàn cục và tùy chỉnh/kiểm thử mẫu email giao dịch."},
"step:app-email-settings-management:view-app-settings": {"name": "Xem Cài đặt App", "summary": "Admin xem và chỉnh sửa cài đặt ứng dụng toàn cục."},
"step:app-email-settings-management:manage-email-templates": {"name": "Quản lý Mẫu Email", "summary": "Admin xem danh sách mẫu email có thể cấu hình."},
"step:app-email-settings-management:edit-email-setting": {"name": "Sửa Cài đặt Email", "summary": "Admin sửa nội dung của một mẫu email cụ thể."},
"step:app-email-settings-management:preview-email-template": {"name": "Xem trước Mẫu Email", "summary": "Admin xem trước cách mẫu email đã sửa sẽ hiển thị."},
"step:app-email-settings-management:send-preview-email": {"name": "Gửi Email Xem trước", "summary": "Admin gửi email thử/xem trước để kiểm tra kết quả mẫu email."},

"domain:payment-billing": {"name": "Thanh toán & Hóa đơn", "summary": "Xử lý thanh toán online qua cổng thanh toán GMO, quản lý thẻ tín dụng đã lưu, xử lý thanh toán một phần (partial checkout) cho lưu trú kéo dài, và tạo báo cáo doanh thu, xuất kế toán OBIC."},
"flow:online-payment-gmo": {"name": "Thanh toán Online qua GMO", "summary": "Người dùng được chuyển hướng đến trang thanh toán GMO trong quá trình đặt vé online; GMO xử lý giao dịch và gọi callback về hệ thống với kết quả."},
"step:online-payment-gmo:redirect-to-gmo-payment": {"name": "Chuyển hướng đến Thanh toán GMO", "summary": "Người dùng được chuyển hướng đến trang thanh toán online để hoàn tất giao dịch GMO."},
"step:online-payment-gmo:process-payment-gmo-service": {"name": "Xử lý Thanh toán qua GMO Service", "summary": "GMO service xử lý logic xác thực và ghi nhận thanh toán."},
"step:online-payment-gmo:handle-gmo-callback": {"name": "Xử lý Callback GMO", "summary": "Hệ thống xử lý callback kết quả thanh toán GMO bất đồng bộ."},
"step:online-payment-gmo:show-payment-success": {"name": "Hiển thị Thanh toán Thành công", "summary": "Hệ thống hiển thị trang xác nhận thanh toán online thành công."},
"step:online-payment-gmo:show-payment-failure": {"name": "Hiển thị Thanh toán Thất bại", "summary": "Hệ thống hiển thị trang thanh toán thất bại kèm hướng dẫn thử lại."},
"step:online-payment-gmo:configure-gmo-settings": {"name": "Cấu hình Cài đặt GMO", "summary": "Admin cấu hình cài đặt merchant GMO theo từng tenant dùng khi thanh toán."},

"flow:credit-card-management": {"name": "Quản lý Thẻ Tín dụng", "summary": "Người dùng lưu, tìm kiếm và xóa thẻ tín dụng dùng cho thanh toán online và vé định kỳ."},
"step:credit-card-management:enter-credit-card-info": {"name": "Nhập Thông tin Thẻ", "summary": "Người dùng nhập thông tin thẻ tín dụng trong form đặt vé hoặc hồ sơ."},
"step:credit-card-management:save-credit-card": {"name": "Lưu Thẻ Tín dụng", "summary": "Hệ thống lưu thẻ tín dụng qua API tokenize thẻ của GMO."},
"step:credit-card-management:search-credit-card": {"name": "Tìm Thẻ Tín dụng", "summary": "Hệ thống lấy thẻ tín dụng đã lưu của người dùng để dùng lại."},
"step:credit-card-management:delete-credit-card": {"name": "Xóa Thẻ Tín dụng", "summary": "Người dùng xóa thẻ tín dụng đã lưu."},
"step:credit-card-management:show-deletion-success": {"name": "Hiển thị Xóa Thành công", "summary": "Hệ thống xác nhận xóa thẻ tín dụng thành công."},

"flow:partial-checkout-payment": {"name": "Thanh toán Một phần (Partial Checkout)", "summary": "Người dùng hoặc admin xử lý khoản thanh toán bổ sung một phần trên đặt vé hiện có, ví dụ phí lưu trú kéo dài."},
"step:partial-checkout-payment:open-partial-checkout-page": {"name": "Mở Trang Thanh toán Một phần", "summary": "Người dùng mở trang thanh toán một phần cho đặt vé hiện có."},
"step:partial-checkout-payment:submit-partial-checkout": {"name": "Gửi Thanh toán Một phần", "summary": "Khoản thanh toán một phần được gửi qua API bookings partial-checkout."},
"step:partial-checkout-payment:admin-process-partial-checkout": {"name": "Admin Xử lý Thanh toán Một phần", "summary": "Admin xử lý hoặc xem xét thanh toán một phần thay cho khách hàng."},
"step:partial-checkout-payment:show-partial-checkout-success": {"name": "Hiển thị Thanh toán Một phần Thành công", "summary": "Hệ thống xác nhận thanh toán một phần thành công."},

"flow:revenue-obic-accounting": {"name": "Xuất Doanh thu & Kế toán OBIC", "summary": "Admin xem phân tích doanh thu và xuất mã/báo cáo kế toán OBIC cho đặt vé và vé phục vụ đối soát tài chính."},
"step:revenue-obic-accounting:view-revenue-dashboard": {"name": "Xem Dashboard Doanh thu", "summary": "Admin xem dashboard quản lý doanh thu."},
"step:revenue-obic-accounting:query-revenue-counts": {"name": "Truy vấn Số liệu Doanh thu", "summary": "Hệ thống truy vấn số liệu doanh thu tổng hợp cho khoảng thời gian đã chọn."},
"step:revenue-obic-accounting:export-revenue-report": {"name": "Xuất Báo cáo Doanh thu", "summary": "Admin xuất báo cáo doanh thu chi tiết."},
"step:revenue-obic-accounting:backfill-obic-codes": {"name": "Backfill Mã OBIC", "summary": "Hệ thống backfill (bổ sung ngược) mã kế toán OBIC còn thiếu cho vé hiện có."},
"step:revenue-obic-accounting:export-obic-codes": {"name": "Xuất Mã OBIC", "summary": "Admin xuất mã kế toán OBIC cho vé."},
"step:revenue-obic-accounting:force-recompute-obic": {"name": "Buộc Tính lại OBIC", "summary": "Admin buộc tính lại mã OBIC cho một đặt vé cụ thể."},

"domain:pos-checkin-ticketing": {"name": "Check-in POS & Quét vé", "summary": "Xử lý vận hành tại cơ sở: quét mã vạch đặt vé để check-in/check-out khách, theo dõi trạng thái đặt vé/chỗ trống theo thời gian thực, và tích hợp với hệ thống POS Smaregi cho thanh toán và đồng bộ tồn kho."},
"flow:barcode-checkin-checkout": {"name": "Check-in / Check-out bằng Mã vạch", "summary": "Nhân viên cơ sở quét mã vạch đặt vé của khách để check-in hoặc check-out, có khả năng rollback nếu quét nhầm."},
"step:barcode-checkin-checkout:open-barcode-scanner": {"name": "Mở Máy quét Mã vạch", "summary": "Nhân viên mở giao diện quét mã vạch tại lối vào cơ sở."},
"step:barcode-checkin-checkout:scan-booking-barcode": {"name": "Quét Mã vạch Đặt vé", "summary": "Nhân viên quét mã vạch đặt vé của khách để tra cứu thông tin đặt chỗ."},
"step:barcode-checkin-checkout:check-in-booking": {"name": "Check-in Đặt vé", "summary": "Đặt vé được đánh dấu đã check-in tại máy POS."},
"step:barcode-checkin-checkout:check-out-booking": {"name": "Check-out Đặt vé", "summary": "Đặt vé được đánh dấu đã check-out tại máy POS."},
"step:barcode-checkin-checkout:rollback-scan": {"name": "Rollback Lượt Quét", "summary": "Nhân viên rollback lượt quét check-in/out bị nhầm."},

"flow:smaregi-pos-integration": {"name": "Tích hợp POS Smaregi", "summary": "Hệ thống kiểm tra tenant có bật tích hợp POS Smaregi hay không, kiểm soát UI liên quan, hiển thị mã QR Smaregi trên vé, và tính số tiền thanh toán POS."},
"step:smaregi-pos-integration:check-smaregi-enabled": {"name": "Kiểm tra Smaregi Đã bật", "summary": "Hệ thống kiểm tra tích hợp POS Smaregi có được bật cho tenant hiện tại không."},
"step:smaregi-pos-integration:gate-feature-via-hoc": {"name": "Kiểm soát Tính năng qua HOC", "summary": "Các component UI được kiểm soát bởi higher-order component yêu cầu Smaregi phải được bật."},
"step:smaregi-pos-integration:display-smaregi-qrcode": {"name": "Hiển thị QR Code Smaregi", "summary": "Hệ thống hiển thị mã QR Smaregi trên vé để quét tại POS."},
"step:smaregi-pos-integration:calculate-pos-payment": {"name": "Tính Thanh toán POS", "summary": "Hệ thống tính số tiền cần thanh toán tại máy POS Smaregi."},
"step:smaregi-pos-integration:record-smaregi-scan-status": {"name": "Ghi nhận Trạng thái Quét Smaregi", "summary": "Bản ghi đặt vé được cập nhật với trạng thái quét Smaregi."},

"flow:ticket-scan-management": {"name": "Quản lý Quét vé & Trạng thái Chỗ trống", "summary": "Admin theo dõi hoạt động quét theo thời gian thực và trạng thái chỗ trống của cơ sở qua các đặt vé từ dashboard quản lý quét vé."},
"step:ticket-scan-management:view-scan-management-dashboard": {"name": "Xem Dashboard Quản lý Quét vé", "summary": "Admin xem dashboard quản lý quét vé cho hoạt động check-in theo thời gian thực."},
"step:ticket-scan-management:update-booking-status": {"name": "Cập nhật Trạng thái Đặt vé", "summary": "Admin cập nhật thủ công trạng thái check-in/out của đặt vé khi cần."},
"step:ticket-scan-management:bulk-booking-status": {"name": "Trạng thái Đặt vé Hàng loạt", "summary": "Hệ thống lấy thông tin trạng thái đặt vé hàng loạt cho dashboard."},
"step:ticket-scan-management:view-vacancies-status-page": {"name": "Xem Trang Trạng thái Chỗ trống", "summary": "Admin xem trang trạng thái chỗ trống của cơ sở."},
}

# ---- Business rules / cross-domain interactions, keyed by exact English text ----
TXT = {
"A booking must reference a valid ticket and tenant with available vacancy": "Một đặt vé phải tham chiếu đến vé và tenant hợp lệ còn chỗ trống",
"Monthly and times-limit tickets cannot be double-booked/used across tenants beyond their limit": "Vé tháng và vé theo lượt không được đặt/sử dụng trùng giữa các tenant vượt quá giới hạn cho phép",
"Cancelled or expired bookings free up vacancy slots and trigger reminder/cron jobs": "Đặt vé bị hủy hoặc hết hạn sẽ giải phóng chỗ trống và kích hoạt các cron job nhắc nhở",
"Requires authenticated user session": "Yêu cầu phiên đăng nhập người dùng đã xác thực",
"Triggers GMO payment authorization": "Kích hoạt xác thực thanh toán GMO",
"Booking check-in/out is performed via POS/Smaregi scanning": "Check-in/check-out đặt vé được thực hiện qua quét mã POS/Smaregi",

"Email must be verified before an account is fully active": "Email phải được xác thực trước khi tài khoản hoạt động đầy đủ",
"Repeated failed logins can lock an account, requiring an unlock request/token": "Đăng nhập sai nhiều lần liên tiếp có thể khóa tài khoản, yêu cầu gửi request/token mở khóa",
"Password reset and email change require a valid time-limited token": "Đặt lại mật khẩu và đổi email yêu cầu token hợp lệ có giới hạn thời gian",
"Feeds authenticated identity into Booking & Reservation Management": "Cung cấp danh tính đã xác thực cho domain Quản lý Đặt vé & Đặt chỗ",
"Admin accounts are provisioned/managed by Admin Facility Management": "Tài khoản admin được cấp phát/quản lý bởi domain Quản lý Cơ sở & Nội dung (Admin)",

"Only authenticated admin/staff accounts can access management screens": "Chỉ tài khoản admin/nhân viên đã xác thực mới truy cập được các màn hình quản lý",
"Tenants must be configured before tickets can be created against them": "Tenant phải được cấu hình trước khi có thể tạo vé gắn với tenant đó",
"Ticket booking schedules define when a ticket can be booked": "Lịch đặt vé (booking schedule) xác định thời điểm vé có thể được đặt",
"Configures GMO settings consumed by Payment & Billing": "Cấu hình GMO được domain Thanh toán & Hóa đơn sử dụng",
"Configures ticket/tenant data consumed by POS Check-in & Ticketing": "Cấu hình dữ liệu vé/tenant được domain Check-in POS & Quét vé sử dụng",
"Manages staff accounts alongside User Account & Authentication": "Quản lý tài khoản nhân viên song song với domain Tài khoản Người dùng & Xác thực",

"Online bookings cannot be confirmed until GMO payment authorization succeeds": "Đặt vé online không thể được xác nhận cho đến khi xác thực thanh toán GMO thành công",
"Each tenant has its own GMO merchant settings": "Mỗi tenant có cài đặt merchant GMO riêng",
"Partial checkouts require an existing active booking": "Thanh toán một phần yêu cầu phải có đặt vé đang hoạt động",
"OBIC accounting codes must be attached to bookings/tickets for revenue export": "Mã kế toán OBIC phải được gắn vào đặt vé/vé để xuất báo cáo doanh thu",
"Consumes booking data from Booking & Reservation Management": "Sử dụng dữ liệu đặt vé từ domain Quản lý Đặt vé & Đặt chỗ",
"GMO/revenue settings configured by Admin Facility Management": "Cài đặt GMO/doanh thu được cấu hình bởi domain Quản lý Cơ sở & Nội dung (Admin)",

"A booking can only be checked in once it is confirmed and not already checked in": "Một đặt vé chỉ có thể check-in khi đã được xác nhận và chưa check-in trước đó",
"Smaregi integration is opt-in per tenant and gated by a feature flag": "Tích hợp Smaregi là tùy chọn theo từng tenant và được kiểm soát bởi feature flag",
"Scan actions can be rolled back if performed in error": "Hành động quét có thể được rollback nếu thực hiện nhầm",
"Operates on bookings created by Booking & Reservation Management": "Thao tác trên đặt vé được tạo bởi domain Quản lý Đặt vé & Đặt chỗ",
"Uses ticket/tenant configuration from Admin Facility Management": "Sử dụng cấu hình vé/tenant từ domain Quản lý Cơ sở & Nội dung (Admin)",
"Calculates and confirms POS payment amounts tied to Payment & Billing": "Tính toán và xác nhận số tiền thanh toán POS liên kết với domain Thanh toán & Hóa đơn",

# cross_domain edge descriptions
"Booking flows require an authenticated user session and rely on user account data.": "Các luồng đặt vé yêu cầu phiên đăng nhập đã xác thực và phụ thuộc vào dữ liệu tài khoản người dùng.",
"Online and offline bookings trigger GMO payment authorization and credit card charges.": "Đặt vé online và offline kích hoạt xác thực thanh toán GMO và tính phí thẻ tín dụng.",
"Confirmed bookings are later checked in/out and scanned on-site via POS/Smaregi.": "Đặt vé đã xác nhận sau đó được check-in/out và quét tại chỗ qua POS/Smaregi.",
"GMO settings and revenue/OBIC reports are configured and reviewed by admins.": "Cài đặt GMO và báo cáo doanh thu/OBIC được admin cấu hình và xem xét.",
"Ticket and tenant configuration managed by admins drive POS scan and vacancy validation.": "Cấu hình vé và tenant do admin quản lý điều khiển việc quét POS và kiểm tra chỗ trống.",
"Admin manages staff and user accounts through the shared authentication system.": "Admin quản lý tài khoản nhân viên và người dùng qua hệ thống xác thực dùng chung.",
}

COMPLEXITY_VI = {"simple": "đơn giản", "moderate": "trung bình", "complex": "phức tạp"}
ENTRY_BADGE = {
    "http": "🌐 HTTP",
    "cli": "⌨️ CLI",
    "event": "⚡ Event",
    "cron": "⏰ Cron",
    "manual": "🖐️ Thao tác thủ công",
}

def vi_name(node):
    return VI.get(node["id"], {}).get("name", node["name"])

def vi_summary(node):
    return VI.get(node["id"], {}).get("summary", node["summary"])

def vi_txt(s):
    return TXT.get(s, s)

def mermaid_label(text):
    return text.replace('"', "'")

def mermaid_step_diagram(step_list):
    """Simple left-to-right flowchart of a flow's steps, in plain language."""
    if not step_list:
        return None
    ids = [f"S{i}" for i in range(1, len(step_list) + 1)]
    lines = ["```mermaid", "flowchart LR"]
    for sid, s in zip(ids, step_list):
        lines.append(f'  {sid}["{mermaid_label(vi_name(s))}"]')
    lines.append("  " + " --> ".join(ids))
    lines.append("```")
    return "\n".join(lines)

domains = [n for n in graph["nodes"] if n["type"] == "domain"]

domain_flows = {}
for e in edges:
    if e["type"] == "contains_flow":
        domain_flows.setdefault(e["source"], []).append(e["target"])

flow_steps = {}
for e in edges:
    if e["type"] == "flow_step":
        flow_steps.setdefault(e["source"], []).append((e["weight"], e["target"]))
for k in flow_steps:
    flow_steps[k].sort(key=lambda x: x[0])

cross_domain_edges = [e for e in edges if e["type"] == "cross_domain"]

os.makedirs(DOCS_DOMAINS_DIR, exist_ok=True)

def slug(domain_id):
    return domain_id.split(":", 1)[1]

domain_summaries = []

for domain in domains:
    dslug = slug(domain["id"])
    meta = domain.get("domainMeta", {})
    lines = []
    lines.append(f"# {vi_name(domain)}")
    lines.append("")
    lines.append(vi_summary(domain))
    lines.append("")
    lines.append(f"**Độ phức tạp:** `{COMPLEXITY_VI.get(domain['complexity'], domain['complexity'])}` · **Tags:** {', '.join('`'+t+'`' for t in domain.get('tags', []))}")
    lines.append("")

    entities = meta.get("entities", [])
    if entities:
        lines.append("## Entities chính")
        lines.append("")
        for ent in entities:
            lines.append(f"- `{ent}`")
        lines.append("")

    rules = meta.get("businessRules", [])
    if rules:
        lines.append("## Business Rules")
        lines.append("")
        for r in rules:
            lines.append(f"- {vi_txt(r)}")
        lines.append("")

    cross = meta.get("crossDomainInteractions", [])
    if cross:
        lines.append("## Tương tác với domain khác")
        lines.append("")
        for c in cross:
            lines.append(f"- {vi_txt(c)}")
        lines.append("")

    flow_ids = domain_flows.get(domain["id"], [])
    lines.append(f"## Tính năng ({len(flow_ids)})")
    lines.append("")

    flow_summaries_for_overview = []

    for fid in flow_ids:
        flow = nodes[fid]
        fmeta = flow.get("domainMeta", {})
        entry_point = fmeta.get("entryPoint", "—")
        entry_type = fmeta.get("entryType", "")
        step_list = [nodes[sid] for _, sid in flow_steps.get(fid, [])]

        lines.append(f"### {vi_name(flow)}")
        lines.append("")
        lines.append(vi_summary(flow))
        lines.append("")
        lines.append(f"**Bắt đầu từ:** {ENTRY_BADGE.get(entry_type, entry_type)} · **Độ phức tạp:** `{COMPLEXITY_VI.get(flow['complexity'], flow['complexity'])}`")
        lines.append("")

        if step_list:
            diagram = mermaid_step_diagram(step_list)
            if diagram:
                lines.append(diagram)
                lines.append("")

            lines.append("**Các bước:**")
            lines.append("")
            for i, s in enumerate(step_list, 1):
                lines.append(f"{i}. **{vi_name(s)}** — {vi_summary(s)}")
            lines.append("")

            if any(s.get("filePath") for s in step_list):
                lines.append("<details>")
                lines.append("<summary>Chi tiết kỹ thuật — file liên quan trong code (dành cho Dev/Techlead)</summary>")
                lines.append("")
                lines.append(f"Endpoint/trigger: `{entry_point}`")
                lines.append("")
                lines.append("| # | Bước | File |")
                lines.append("|---|---|---|")
                for i, s in enumerate(step_list, 1):
                    fp = s.get("filePath")
                    fp_cell = f"`{fp}`" if fp else "—"
                    lines.append(f"| {i} | {vi_name(s)} | {fp_cell} |")
                lines.append("")
                lines.append("</details>")
                lines.append("")

        flow_summaries_for_overview.append((vi_name(flow), len(step_list)))

    out_path = os.path.join(DOCS_DOMAINS_DIR, f"{dslug}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {out_path} ({len(flow_ids)} flows)")

    domain_summaries.append({
        "id": domain["id"],
        "slug": dslug,
        "name": vi_name(domain),
        "summary": vi_summary(domain),
        "complexity": domain["complexity"],
        "flow_count": len(flow_ids),
        "step_count": sum(n for _, n in flow_summaries_for_overview),
        "flows": flow_summaries_for_overview,
    })

# overview.md
lines = []
lines.append("# Tổng quan Feature — tokiwagi")
lines.append("")
lines.append(graph["project"]["description"])
lines.append("")
lines.append(f"**Framework:** {', '.join(graph['project']['frameworks'])} · **Ngôn ngữ:** {', '.join(graph['project']['languages'])}")
lines.append("")
lines.append(f"Trích xuất từ knowledge graph (understand-anything) lúc `{graph['project']['analyzedAt']}`, commit `{graph['project']['gitCommitHash'][:12]}`.")
lines.append("")
total_flows = sum(d["flow_count"] for d in domain_summaries)
total_steps = sum(d["step_count"] for d in domain_summaries)
lines.append(f"**{len(domain_summaries)} domain nghiệp vụ · {total_flows} tính năng · {total_steps} bước**")
lines.append("")

if cross_domain_edges:
    lines.append("## Sơ đồ tổng quan")
    lines.append("")
    diagram = ["```mermaid", "flowchart LR"]
    for d in domain_summaries:
        did = "D_" + d["slug"].replace("-", "_")
        diagram.append(f'  {did}["{mermaid_label(d["name"])}"]')
    for e in cross_domain_edges:
        src_id = "D_" + slug(e["source"]).replace("-", "_")
        tgt_id = "D_" + slug(e["target"]).replace("-", "_")
        diagram.append(f"  {src_id} --> {tgt_id}")
    diagram.append("```")
    lines.append("\n".join(diagram))
    lines.append("")

lines.append("## Domain")
lines.append("")
lines.append("| Domain | Độ phức tạp | Số tính năng | Số bước |")
lines.append("|---|---|---|---|")
for d in domain_summaries:
    lines.append(f"| [{d['name']}]({d['slug']}.md) | `{COMPLEXITY_VI.get(d['complexity'], d['complexity'])}` | {d['flow_count']} | {d['step_count']} |")
lines.append("")

for d in domain_summaries:
    lines.append(f"### [{d['name']}]({d['slug']}.md)")
    lines.append("")
    lines.append(d["summary"])
    lines.append("")
    lines.append("Tính năng:")
    for fname, scount in d["flows"]:
        lines.append(f"- {fname} ({scount} bước)")
    lines.append("")

if cross_domain_edges:
    lines.append("## Quan hệ liên Domain")
    lines.append("")
    lines.append("| Từ | Đến | Mô tả |")
    lines.append("|---|---|---|")
    for e in cross_domain_edges:
        src_name = vi_name(nodes[e["source"]])
        tgt_name = vi_name(nodes[e["target"]])
        src_slug = slug(e["source"])
        tgt_slug = slug(e["target"])
        lines.append(f"| [{src_name}]({src_slug}.md) | [{tgt_name}]({tgt_slug}.md) | {vi_txt(e.get('description', ''))} |")
    lines.append("")

overview_path = os.path.join(DOCS_DOMAINS_DIR, "overview.md")
with open(overview_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {overview_path}")

# sanity: report any missing translations
missing = [nid for nid in nodes if nid not in VI]
print(f"\nnodes without VI translation (fallback to English): {len(missing)}")
for m in missing[:20]:
    print("  MISSING:", m)
