# Biomedical API Toolkit: hướng dẫn cho người mới

[English](getting-started.md) · [Trang giới thiệu](../README.md) · [Danh mục API](../references/api-catalog.md)

## 1. Toolkit này giúp bạn làm gì?

Biomedical API Toolkit giúp bạn lấy và kiểm tra thông tin từ các nguồn nghiên cứu công khai. Bạn có thể dùng nó để chuẩn bị tìm tài liệu, kiểm tra danh mục tham khảo, tra nghiên cứu đã đăng ký hoặc lấy một bộ dữ liệu thật để học thống kê và dạy phương pháp nghiên cứu.

**API** là cách một chương trình yêu cầu dữ liệu từ dịch vụ. Thay vì mở từng trang và chép từng bản ghi, chương trình gửi câu truy vấn rồi nhận kết quả có cấu trúc. **Skill** là bộ hướng dẫn để AI thực hiện công việc. Toolkit này gồm skill, danh mục nguồn và một script Python hỗ trợ gọi API.

Bạn không cần học hết 14 API. Hãy bắt đầu từ một nhu cầu cụ thể.

| Bạn muốn làm gì? | Nguồn nên bắt đầu | Kết quả có thể yêu cầu AI chuẩn bị |
|---|---|---|
| Tìm bài nghiên cứu y sinh | MeSH, PubMed, Europe PMC | Câu truy vấn và bảng bài ứng viên kèm đường dẫn |
| Kiểm tra tài liệu AI đưa ra | Crossref, PubMed | Bảng tài liệu khớp, sai thông tin, chưa rõ hoặc chưa tìm thấy |
| Tra hồ sơ nghiên cứu đăng ký | ClinicalTrials.gov | Bảng thiết kế, trường thông tin tuyển mẫu, trạng thái và link hồ sơ |
| Học làm sạch dữ liệu, vẽ biểu đồ | World Bank | Dữ liệu gốc, bảng dữ liệu, codebook, script xử lý và biểu đồ |
| Nghiên cứu chuyên sâu về thuốc, sinh học | RxNorm, openFDA, ChEMBL | Dữ liệu được giới hạn theo câu hỏi và giải thích cách diễn giải |

Toolkit phù hợp với học viên, nhà nghiên cứu, giảng viên và lập trình viên. Việc đọc toàn văn và đánh giá phương pháp nghiên cứu vẫn cần thực hiện. Ba hướng phát triển ứng dụng đã lưu trong [lộ trình](../references/roadmap.md); repo hiện cung cấp nền tảng và hướng dẫn, chưa có ba ứng dụng hoàn chỉnh.

## 2. Chọn một trong hai cách dùng

**Cách A — giao việc cho AI:** phù hợp nếu bạn muốn viết yêu cầu bằng ngôn ngữ thông thường. Sau khi cài skill vào ứng dụng hỗ trợ, chẳng hạn Codex, bạn yêu cầu AI tìm tài liệu hoặc kiểm tra trích dẫn. Bạn không cần tự viết Python. Để lấy dữ liệu thật, ứng dụng cần truy cập mạng và công cụ phù hợp; nếu AI chạy script đi kèm thì máy hoặc môi trường thực thi cần Python.

**Cách B — tự chạy Python:** phù hợp nếu bạn muốn kiểm soát câu truy vấn hoặc đưa API vào chương trình riêng. Script cần Python 3.10 trở lên, dùng thư viện chuẩn và không cần cài thêm gói bằng `pip`. Cách này không cần ứng dụng AI. Kết quả là dữ liệu nguồn và thông tin lần gọi, chưa phải bản tổng quan hay danh mục tài liệu đã kiểm chứng.

Repo được phát hành miễn phí theo MIT. Dịch vụ API có thể giới hạn lượt gọi hoặc cần key miễn phí. Chi phí thuê bao và sử dụng ứng dụng AI là khoản riêng. Với ví dụ nhỏ bên dưới, bạn có thể bắt đầu mà chưa cấu hình key; xem [danh mục có ghi ngày kiểm tra](../references/api-catalog.md) trước khi dùng nhiều.

## 3. Cài skill để dùng với AI

### Nhờ trình cài đặt

Trong Codex, nhập:

```text
Dùng $skill-installer để cài skill từ repo:
https://github.com/vuduykien-netizen/biomedical-api-toolkit
File SKILL.md nằm ngay ở thư mục gốc của repo.
```

Nếu muốn cài thủ công, chọn một cách dưới đây. Nếu đã cài skill, không tạo thêm bản trùng.

### Cài bằng Git

[Tài liệu kỹ năng chính thức](https://learn.chatgpt.com/docs/build-skills) hiện liệt kê `~/.agents/skills` là vị trí skill của người dùng. Một số môi trường dùng `~/.codex/skills` hoặc thư mục tùy chỉnh. Hãy dùng vị trí mà ứng dụng của bạn hỗ trợ. Nếu bản đang có trong `.codex/skills` đã được nhận diện, bạn có thể tiếp tục dùng bản đó.

Windows: mở PowerShell và chạy:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
git clone https://github.com/vuduykien-netizen/biomedical-api-toolkit.git "$env:USERPROFILE\.agents\skills\biomedical-api-toolkit"
```

macOS / Linux: mở Terminal và chạy:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/vuduykien-netizen/biomedical-api-toolkit.git ~/.agents/skills/biomedical-api-toolkit
```

### Cài bằng ZIP, không cần Git

1. Mở [repo GitHub](https://github.com/vuduykien-netizen/biomedical-api-toolkit).
2. Chọn **Code → Download ZIP** rồi giải nén.
3. Đổi tên thư mục giải nén thành `biomedical-api-toolkit`.
4. Đặt thư mục này vào thư mục skills của ứng dụng.
5. Kiểm tra cấu trúc: `skills/biomedical-api-toolkit/SKILL.md`; các thư mục `scripts/`, `references/`, `docs/` nằm cạnh file đó. Tránh đặt thêm một tầng thư mục repo bên trong.

Nếu ứng dụng chưa nhận skill, mở phiên mới hoặc khởi động lại. Trong Codex, gõ `$biomedical-api-toolkit` và kiểm tra có thể chọn skill hay không. Ứng dụng khác có quy tắc cài và gọi riêng. Chỉ gõ tên skill vào một cuộc chat thông thường không tự cài file hoặc cấp quyền truy cập API.

## 4. Giao việc đầu tiên cho AI

Bắt đầu với một yêu cầu nhỏ, dễ đối chiếu nguồn:

```text
Dùng $biomedical-api-toolkit tìm tối đa 5 bài ứng viên trên PubMed về
tăng huyết áp và tuân thủ dùng thuốc. Ghi câu truy vấn, ngày tìm,
tên bài, năm, PMID/DOI nếu có và link nguồn. Giải thích phạm vi chưa
được bao phủ. Không trình bày kết quả này như một tổng quan hệ thống
đã hoàn tất.
```

Kết quả nên có câu truy vấn, bảng bài ứng viên, nguồn và giới hạn. Một số bài có thể thiếu DOI hoặc abstract. Nếu truy cập thất bại, AI cần nói rõ, phân biệt câu truy vấn đề xuất với dữ liệu thực sự đã lấy.

Để yêu cầu rõ hơn, thêm chủ đề, quần thể, khoảng năm, nguồn, số bản ghi tối đa và dạng đầu ra. Bạn có thể viết bằng tiếng Việt; việc truy vấn cơ sở dữ liệu y sinh thường cần thuật ngữ tiếng Anh.

### Ba mẫu yêu cầu có thể sao chép

**Tìm tài liệu:**

```text
Dùng $biomedical-api-toolkit chuẩn bị tìm tài liệu cho câu hỏi: [câu hỏi].
Quần thể: [quần thể]. Khoảng năm: [khoảng năm]. Đề xuất thuật ngữ MeSH
và từ khóa tự do, sau đó lấy tối đa 10 bài ứng viên từ PubMed và Europe PMC.
Lưu câu truy vấn, loại trùng bằng mã định danh và xuất bảng có link nguồn.
```

**Kiểm tra trích dẫn:**

```text
Dùng $biomedical-api-toolkit kiểm tra danh mục tài liệu dưới đây.
Đối chiếu DOI/PMID, tên bài, tác giả, năm và tạp chí. Trả bảng gồm:
khớp, sai thông tin, nhiều khả năng cần xem lại hoặc chưa tìm thấy;
kèm lý do và nguồn. Phân biệt xác nhận danh tính bài với việc bài đó
có hỗ trợ một nhận định cụ thể hay không.
[Dán danh mục tài liệu ở đây.]
```

**Lấy dữ liệu thực hành:**

```text
Dùng $biomedical-api-toolkit lấy tuổi thọ kỳ vọng khi sinh của Việt Nam
giai đoạn 2010–2023 từ World Bank. Lưu phản hồi gốc, câu truy vấn,
thời điểm lấy, định nghĩa và đơn vị chỉ số. Tạo CSV và script xử lý
có thể chạy lại, báo giá trị thiếu và vẽ chuỗi theo năm. Giải thích
giới hạn khi diễn giải dữ liệu cấp quốc gia.
```

AI cần thực hiện thêm việc xử lý để tạo bảng, CSV hoặc biểu đồ. Script gọi API đi kèm chỉ lấy phản hồi nguồn.

## 5. Tự gọi API bằng Python

Tải repo vào một thư mục làm việc hoặc dùng thư mục skill đã cài. Mở terminal **ngay trong thư mục toolkit**, nơi có `SKILL.md`, `scripts/` và `references/`.

Kiểm tra Python:

```bash
python --version
```

Cần phiên bản 3.10 trở lên. Nếu máy dùng lệnh `python3` hoặc Windows `py`, thay `python` bằng lệnh đó trong các ví dụ. Nếu chưa có Python, tải từ [python.org](https://www.python.org/downloads/).

Xem thử yêu cầu mà chưa gọi mạng:

```bash
python scripts/fetch_api.py pubmed --demo --dry-run
```

Sau đó lấy một kết quả nhỏ và lưu file:

```bash
python scripts/fetch_api.py pubmed --demo --output results/pubmed-first.json
```

Demo tìm `diabetes` và yêu cầu một PMID. Nó giúp kiểm tra kết nối, chưa phải chiến lược tìm tài liệu hoàn chỉnh. Phản hồi ESearch có danh sách mã bài; chưa lấy toàn bộ abstract hoặc toàn văn. Muốn lấy thông tin chi tiết, xem [ví dụ EFetch trong danh mục](../references/api-catalog.md) hoặc yêu cầu AI lấy chi tiết cho các PMID đã chọn.

Script tự tạo thư mục `results/` nếu chưa có. Khi chạy lại, đặt tên file mới vì script không ghi đè kết quả cũ. Nếu tải ZIP, phải giải nén trước khi chạy.

### Đọc file kết quả

**JSON** là văn bản có cấu trúc với tên trường và giá trị. Bạn có thể mở file bằng trình soạn thảo văn bản. Các trường bên ngoài ghi thông tin lần gọi; `data` chứa phản hồi của API.

| Trường | Ý nghĩa |
|---|---|
| `provider` | Nguồn được gọi |
| `request.url` | URL truy vấn; thông tin xác thực đã cấu hình được che |
| `retrieved_at_utc` | Thời điểm lấy phản hồi theo giờ UTC |
| `http_status` | Trạng thái HTTP; 200 là phản hồi HTTP thành công |
| `dry_run` | True nếu chỉ xem kế hoạch, chưa gọi mạng |
| `data` | Bản ghi, thông báo hoặc văn bản từ nhà cung cấp |

Với demo PubMed, xem `data.esearchresult.idlist` để biết PMID đã trả về; `data.esearchresult.count` là tổng số bản ghi khớp. Tổng số khớp không phải số đã tải: demo chỉ yêu cầu một mã. HTTP 200 vẫn có thể đi kèm thông báo lỗi hoặc kết quả rỗng trong `data`, nên cần đọc nội dung.

## 6. Thay câu truy vấn

Tìm hai bản ghi thư mục ứng viên:

```bash
python scripts/fetch_api.py crossref --path works --param "query.bibliographic=hypertension medication adherence" --param rows=2 --output results/crossref-first.json
```

Lấy chuỗi chỉ số Việt Nam:

```bash
python scripts/fetch_api.py worldbank --path country/VNM/indicator/SP.DYN.LE00.IN --param date=2010:2023 --param format=json --param per_page=50 --output results/vietnam-life-expectancy.json
```

`VNM` là mã Việt Nam; `SP.DYN.LE00.IN` là mã tuổi thọ kỳ vọng khi sinh. Đọc định nghĩa, đơn vị và nguồn trong [metadata của World Bank](https://api.worldbank.org/v2/indicator/SP.DYN.LE00.IN?format=json). Giữ lại giá trị thiếu và năm dữ liệu trước khi phân tích.

| Thành phần lệnh | Tác dụng |
|---|---|
| Tên nguồn, ví dụ `pubmed` | Chọn API trong danh mục |
| `--demo` | Dùng ví dụ nhỏ đã có |
| `--path` | Chọn endpoint tương đối trong API của nguồn |
| `--param "key=value"` | Truyền tham số; có thể lặp nhiều lần |
| `--dry-run` | Xem yêu cầu, chưa lấy dữ liệu |
| `--output` | Lưu kết quả vào file JSON mới |

Mỗi API có tên tham số riêng. Đặt cả `key=value` trong dấu nháy khi có khoảng trắng. `--path` không nhận URL đầy đủ hay chuỗi query. Với yêu cầu tự viết, thêm `--path` hoặc dùng `--demo`. Xem [ví dụ của từng nguồn](../references/api-catalog.md) để chỉnh tiếp.

## 7. Key, lỗi thường gặp và cập nhật

Có thể thử các ví dụ nhỏ của PubMed, MeSH, Crossref, ClinicalTrials.gov và World Bank mà chưa cần key. Unpaywall cần email liên hệ. Nguồn khác có thể khuyến nghị đăng ký, yêu cầu key hoặc giới hạn phần miễn phí. Xem [cách cấu hình thông tin xác thực](../references/api-catalog.md); dùng biến môi trường, không đưa bí mật vào file public hay tin nhắn. Script không kiểm tra cấu hình thanh toán của tài khoản.

| Hiện tượng | Cách xử lý |
|---|---|
| Không thấy skill | Kiểm tra cấu trúc thư mục và vị trí ứng dụng hỗ trợ; mở phiên mới hoặc khởi động lại |
| Không nhận lệnh `git` | Dùng cách tải ZIP hoặc cài Git từ [git-scm.com](https://git-scm.com/downloads) |
| Không nhận lệnh `python` | Thử `python3` hoặc `py`; nếu cần, cài Python rồi mở terminal mới |
| Không tìm thấy script | Chuyển vào thư mục toolkit có `scripts/` |
| `Provide --path or --demo` | Thêm endpoint hoặc chọn demo |
| `Output already exists` | Đổi tên file đầu ra để giữ kết quả trước |
| HTTP 429 | Dừng gọi liên tục; chờ theo quy định nguồn hoặc dùng key miễn phí được cho phép |
| HTTP 403 | Kiểm tra endpoint chính thức, điều kiện truy cập và hạn chế mạng |
| `Set UNPAYWALL_EMAIL locally` | Cấu hình email liên hệ theo danh mục hoặc dùng nguồn khác |
| Không có bản ghi, thiếu trường | Xem truy vấn, giới hạn năm và thông báo nguồn; ghi rõ thiếu dữ liệu |
| Lỗi mạng | Giữ kết quả đã có, thử lại sau trong phạm vi giới hạn |

Nếu cài bằng Git, lưu các thay đổi riêng rồi chạy `git pull --ff-only` **trong thư mục toolkit đang có** để cập nhật. Nếu Git từ chối do thay đổi local, bảo toàn chúng trước khi giải quyết. Nếu cài ZIP, giải nén bản mới vào thư mục riêng và giữ dữ liệu của bạn. Toolkit không tự tạo lịch cập nhật hay giám sát.

## 8. Hiểu đúng kết quả

Tài liệu khớp DOI xác nhận danh tính bản ghi, chưa chứng minh chất lượng bài hoặc một câu nhận định là đúng. Một lượt tìm nhỏ chưa phải tổng quan hệ thống hoàn chỉnh. Hồ sơ đăng ký nghiên cứu chưa chứng minh hiệu quả điều trị. Dữ liệu cấp quốc gia không xác lập quan hệ nhân quả ở cá nhân; số báo cáo FAERS không dùng để tính tỷ lệ mắc biến cố. Preprint cần ghi rõ và kiểm tra tình trạng xuất bản hiện tại.

Không gửi dữ liệu có thể nhận diện người bệnh vào query API công khai. Kiểm tra giấy phép nguồn trước khi chia sẻ lại văn bản, hình hoặc bộ dữ liệu. Toolkit giúp lưu những giới hạn này cùng với kết quả.

Sau ví dụ đầu tiên, chọn [quy trình phù hợp](../references/workflows.md) và dùng [lộ trình ba hướng](../references/roadmap.md) để triển khai dần.
