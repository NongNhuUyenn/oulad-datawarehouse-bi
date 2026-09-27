from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# MÔ TẢ CÁC CỘT OULAD

descriptions = {

    "courses": {
        "code_module": "Mã định danh của module (môn học).",
        "code_presentation": "Mã định danh của lần tổ chức module.",
        "module_presentation_length": "Thời lượng của lần tổ chức module, tính theo ngày."
    },

    "assessments": {
        "code_module": "Mã module chứa bài đánh giá.",
        "code_presentation": "Mã lần tổ chức module chứa bài đánh giá.",
        "id_assessment": "Mã định danh của bài đánh giá.",
        "assessment_type": "Loại bài đánh giá, ví dụ TMA, CMA hoặc Exam.",
        "date": "Ngày kết thúc hoặc hạn của bài đánh giá, tính tương đối từ ngày bắt đầu module.",
        "weight": "Trọng số của bài đánh giá trong kết quả của module."
    },

    "vle": {
        "id_site": "Mã định danh của tài nguyên hoặc hoạt động trên VLE.",
        "code_module": "Mã module mà tài nguyên VLE thuộc về.",
        "code_presentation": "Mã lần tổ chức module mà tài nguyên VLE thuộc về.",
        "activity_type": "Loại hoạt động hoặc tài nguyên trên VLE.",
        "week_from": "Tuần bắt đầu sử dụng hoặc hiển thị tài nguyên.",
        "week_to": "Tuần kết thúc sử dụng hoặc hiển thị tài nguyên."
    },

    "studentInfo": {
        "code_module": "Mã module mà sinh viên theo học.",
        "code_presentation": "Mã lần tổ chức module mà sinh viên theo học.",
        "id_student": "Mã định danh của sinh viên.",
        "gender": "Giới tính của sinh viên.",
        "region": "Khu vực địa lý nơi sinh viên sinh sống.",
        "highest_education": "Trình độ học vấn cao nhất của sinh viên trước khi học module.",
        "imd_band": "Nhóm chỉ số Index of Multiple Deprivation của khu vực sinh viên.",
        "age_band": "Nhóm tuổi của sinh viên.",
        "num_of_prev_attempts": "Số lần trước đó sinh viên đã thử học module.",
        "studied_credits": "Tổng số tín chỉ mà sinh viên đang học.",
        "disability": "Cho biết sinh viên có khai báo khuyết tật hay không.",
        "final_result": "Kết quả cuối cùng của sinh viên trong module."
    },

    "studentRegistration": {
        "code_module": "Mã module mà sinh viên đăng ký.",
        "code_presentation": "Mã lần tổ chức module mà sinh viên đăng ký.",
        "id_student": "Mã định danh của sinh viên.",
        "date_registration": "Ngày sinh viên đăng ký module, tính tương đối từ ngày bắt đầu module.",
        "date_unregistration": "Ngày sinh viên hủy đăng ký module; để trống nếu không hủy."
    },

    "studentAssessment": {
        "id_assessment": "Mã bài đánh giá mà sinh viên thực hiện.",
        "id_student": "Mã định danh của sinh viên.",
        "date_submitted": "Ngày sinh viên nộp bài, tính tương đối từ ngày bắt đầu module.",
        "is_banked": "Cho biết kết quả đánh giá có được chuyển/bảo lưu từ lần học trước hay không.",
        "score": "Điểm số của sinh viên cho bài đánh giá."
    },

    "studentVle": {
        "code_module": "Mã module liên quan đến tương tác VLE.",
        "code_presentation": "Mã lần tổ chức module liên quan đến tương tác VLE.",
        "id_student": "Mã định danh của sinh viên thực hiện tương tác.",
        "id_site": "Mã tài nguyên hoặc hoạt động VLE được tương tác.",
        "date": "Ngày xảy ra tương tác, tính tương đối từ ngày bắt đầu module.",
        "sum_click": "Tổng số lượt click/tương tác được ghi nhận."
    }
}


# ============================================================
# ROLE CỦA CỘT TRONG RELATIONAL SCHEMA ĐÃ KIỂM TRA
# ============================================================

roles = {
    "courses": {
        "code_module": "PK (composite)",
        "code_presentation": "PK (composite)"
    },

    "assessments": {
        "id_assessment": "PK",
        "code_module": "FK (composite)",
        "code_presentation": "FK (composite)"
    },

    "vle": {
        "id_site": "PK",
        "code_module": "FK (composite)",
        "code_presentation": "FK (composite)"
    },

    "studentInfo": {
        "code_module": "PK/FK (composite)",
        "code_presentation": "PK/FK (composite)",
        "id_student": "PK (composite)"
    },

    "studentRegistration": {
        "code_module": "PK/FK (composite)",
        "code_presentation": "PK/FK (composite)",
        "id_student": "PK/FK (composite)"
    },

    "studentAssessment": {
        "id_assessment": "PK/FK (composite)",
        "id_student": "PK (composite)"
    },

    "studentVle": {
        "code_module": "FK (composite)",
        "code_presentation": "FK (composite)",
        "id_student": "FK (composite)",
        "id_site": "FK"
    }
}


files = {
    "courses": "courses.csv",
    "assessments": "assessments.csv",
    "vle": "vle.csv",
    "studentInfo": "studentInfo.csv",
    "studentRegistration": "studentRegistration.csv",
    "studentAssessment": "studentAssessment.csv",
    "studentVle": "studentVle.csv"
}



# TABLE DESCRIPTION


table_descriptions = {
    "courses":
        "Thông tin về các module và các lần tổ chức module.",

    "assessments":
        "Thông tin về các bài đánh giá được sử dụng trong từng module.",

    "vle":
        "Thông tin về các tài nguyên và hoạt động trên môi trường học tập trực tuyến VLE.",

    "studentInfo":
        "Thông tin nhân khẩu học, thông tin học tập và kết quả cuối cùng của sinh viên.",

    "studentRegistration":
        "Thông tin đăng ký và hủy đăng ký module của sinh viên.",

    "studentAssessment":
        "Thông tin bài nộp và kết quả đánh giá của sinh viên.",

    "studentVle":
        "Nhật ký tương tác của sinh viên với các tài nguyên và hoạt động trên VLE."
}



# PROFILING


dictionary_rows = []
table_rows = []

for table_name, filename in files.items():

    print(f"Processing {filename} ...")

    path = DATA_DIR / filename
    df = pd.read_csv(path)

    rows, cols = df.shape
    size_mb = path.stat().st_size / (1024 ** 2)

    total_null = int(df.isna().sum().sum())

    table_rows.append({
        "table": table_name,
        "file": filename,
        "rows": rows,
        "columns": cols,
        "size_mb": round(size_mb, 2),
        "total_null": total_null,
        "description": table_descriptions[table_name]
    })

    for column in df.columns:

        null_count = int(df[column].isna().sum())
        null_percent = (null_count / rows * 100) if rows else 0

        dictionary_rows.append({
            "table": table_name,
            "column": column,
            "data_type": str(df[column].dtype),
            "key_role": roles.get(table_name, {}).get(column, ""),
            "null_count": null_count,
            "null_percent": round(null_percent, 2),
            "unique_values": int(df[column].nunique(dropna=True)),
            "description": descriptions[table_name].get(column, "")
        })


# CREATE DATAFRAMES


table_summary = pd.DataFrame(table_rows)
data_dictionary = pd.DataFrame(dictionary_rows)


# SAVE CSV


table_summary.to_csv(
    OUTPUT_DIR / "oulad_table_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

data_dictionary.to_csv(
    OUTPUT_DIR / "oulad_data_dictionary.csv",
    index=False,
    encoding="utf-8-sig"
)



# PRINT RESULTS

print("\n" + "=" * 80)
print("TABLE SUMMARY")
print("=" * 80)

print(table_summary.to_string(index=False))

print("\n" + "=" * 80)
print("DATA DICTIONARY")
print("=" * 80)

print(data_dictionary.to_string(index=False))

print("\n" + "=" * 80)
print("FINISHED")
print("=" * 80)

print("Created:")
print(OUTPUT_DIR / "oulad_table_summary.csv")
print(OUTPUT_DIR / "oulad_data_dictionary.csv")