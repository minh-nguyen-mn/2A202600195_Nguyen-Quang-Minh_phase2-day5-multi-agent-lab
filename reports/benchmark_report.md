# 📊 Benchmark Report: Single-Agent vs Multi-Agent

## 1. Mô tả bài toán

Query: "Explain multi-agent systems"

---

## 2. Kết quả Single-Agent

- Thời gian: ~7.5s
- Số bước: 1 (1 lần gọi LLM)
- Output: Một câu trả lời tổng quát

### Ưu điểm:
- Nhanh
- Đơn giản
- Chi phí thấp

### Nhược điểm:
- Không có kiểm chứng nguồn
- Không có phân tích trung gian
- Dễ hallucination

---

## 3. Kết quả Multi-Agent

- Thời gian: ~10–12s
- Số bước:
  - researcher → analyst → writer → done
- Có trace rõ ràng

### Ưu điểm:
- Có pipeline rõ ràng
- Có nguồn (sources)
- Có phân tích trước khi viết
- Dễ debug

### Nhược điểm:
- Chậm hơn
- Chi phí cao hơn
- Phức tạp hơn

---

## 4. So sánh trực tiếp

| Tiêu chí        | Single-Agent | Multi-Agent |
|----------------|------------|------------|
| Latency        | ✅ Nhanh    | ❌ Chậm hơn |
| Explainability | ❌ Không    | ✅ Có trace |
| Reliability    | ❌ Thấp     | ✅ Cao hơn |
| Debugability   | ❌ Khó      | ✅ Dễ |

---

## 5. Kết luận

Multi-agent phù hợp cho:
- Bài toán phức tạp
- Cần kiểm chứng
- Cần explainability

Single-agent phù hợp cho:
- Task đơn giản
- Cần tốc độ
- MVP nhanh