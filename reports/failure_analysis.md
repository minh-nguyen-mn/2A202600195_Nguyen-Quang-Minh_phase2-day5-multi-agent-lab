# ⚠️ Failure Mode Analysis & Fix

## 1. Failure Mode gặp phải

Trong quá trình chạy Multi-Agent Workflow, hệ thống đã gặp một số vấn đề chính:

### (1) Object không serialize được khi output JSON
- Lỗi:
```
TypeError: Object of type ResearchQuery is not JSON serializable
```

- Nguyên nhân:
  - `ResearchQuery` là Pydantic object
  - Python `json.dumps()` không tự động serialize custom object
  - CLI cố gắng dump toàn bộ state trực tiếp

---

### (2) Sai kiểu dữ liệu khi print result
- Lỗi:
```
AttributeError: 'dict' object has no attribute 'model_dump_json'
```

- Nguyên nhân:
  - `workflow.run()` trả về `dict` trong một số trường hợp
  - Nhưng CLI lại assume luôn là Pydantic model
  - Thiếu consistency giữa return type

---

### (3) SupervisorAgent chưa production-safe
- Vấn đề:
  - Default mode luôn raise `StudentTodoError`
  - Chỉ chạy thật khi `_production = True`

- Hệ quả:
  - Nếu quên set flag → workflow dừng ngay

---

## 2. Root Cause

Các lỗi trên đến từ 3 vấn đề thiết kế:

1. **Không thống nhất data model output**
   - lúc thì dict
   - lúc thì Pydantic model

2. **Thiếu serialization layer**
   - chưa chuẩn hóa output trước khi print/log

3. **Separation giữa dev mode và production mode chưa rõ**
   - logic test vs runtime bị trộn trong SupervisorAgent

---

## 3. Cách Fix

### Fix 1: Chuẩn hóa output serialization
Trong CLI, luôn normalize output:

```python
import json

def safe_serialize(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return obj
```

➡️ và dùng:

```python
output = safe_serialize(result)
console.print(json.dumps(output, indent=2))
```

---

### Fix 2: Chuẩn hóa state model
Đảm bảo tất cả agent trả về:

- Pydantic model hoặc
- dict nhưng phải consistent

👉 Khuyến nghị: LUÔN dùng Pydantic model

---

### Fix 3: Tách rõ test mode vs production mode

Hiện tại:

```python
if not getattr(state, "_production", False):
    raise StudentTodoError(...)
```

👉 Cải tiến:

- dùng enum mode rõ ràng:

```python
state.mode = "test" | "production"
```

- tránh boolean flag mơ hồ

---

## 4. Kết luận

Failure chính không nằm ở logic multi-agent, mà nằm ở:

- thiếu chuẩn hóa output format
- thiếu serialization layer
- thiếu strict typing giữa các stage

Sau khi fix, hệ thống sẽ:

- ổn định hơn khi log/trace
- dễ debug hơn
- tránh crash khi CLI render output