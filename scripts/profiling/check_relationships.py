import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")


def load(name):
    print(f"Loading {name}...")
    return pd.read_csv(DATA_DIR / name)


# LOAD DATA

courses = load("courses.csv")
assessments = load("assessments.csv")
vle = load("vle.csv")
student_info = load("studentInfo.csv")
student_registration = load("studentRegistration.csv")
student_assessment = load("studentAssessment.csv")
student_vle = load("studentVle.csv")


# FUNCTION: CHECK CANDIDATE PRIMARY KEY

def check_pk(df, columns, table_name):
    duplicates = df.duplicated(subset=columns).sum()

    print("\n" + "=" * 70)
    print(f"PK CHECK: {table_name}")
    print("Candidate key:", columns)
    print("Rows:", len(df))
    print("Duplicate keys:", duplicates)

    if duplicates == 0:
        print("RESULT: UNIQUE - candidate key is valid")
    else:
        print("RESULT: NOT UNIQUE")


# PRIMARY KEY CHECKS

check_pk(
    courses,
    ["code_module", "code_presentation"],
    "courses"
)

check_pk(
    assessments,
    ["id_assessment"],
    "assessments"
)

check_pk(
    vle,
    ["id_site"],
    "vle"
)

check_pk(
    student_info,
    ["code_module", "code_presentation", "id_student"],
    "studentInfo"
)

check_pk(
    student_registration,
    ["code_module", "code_presentation", "id_student"],
    "studentRegistration"
)

check_pk(
    student_assessment,
    ["id_assessment", "id_student"],
    "studentAssessment"
)


# FUNCTION: CHECK FOREIGN KEY

def check_fk(child, parent, child_cols, parent_cols, relationship_name):

    child_keys = child[child_cols].drop_duplicates()
    parent_keys = parent[parent_cols].drop_duplicates()

    parent_keys.columns = child_cols

    result = child_keys.merge(
        parent_keys,
        on=child_cols,
        how="left",
        indicator=True
    )

    missing = result[result["_merge"] == "left_only"]

    print("\n" + "=" * 70)
    print("FK CHECK:", relationship_name)
    print("Child key:", child_cols)
    print("Parent key:", parent_cols)
    print("Missing FK values:", len(missing))

    if len(missing) == 0:
        print("RESULT: VALID")
    else:
        print("RESULT: INVALID / UNMATCHED VALUES EXIST")
        print(missing.head(10))


# FOREIGN KEY CHECKS

check_fk(
    assessments,
    courses,
    ["code_module", "code_presentation"],
    ["code_module", "code_presentation"],
    "assessments -> courses"
)

check_fk(
    vle,
    courses,
    ["code_module", "code_presentation"],
    ["code_module", "code_presentation"],
    "vle -> courses"
)

check_fk(
    student_info,
    courses,
    ["code_module", "code_presentation"],
    ["code_module", "code_presentation"],
    "studentInfo -> courses"
)

check_fk(
    student_registration,
    courses,
    ["code_module", "code_presentation"],
    ["code_module", "code_presentation"],
    "studentRegistration -> courses"
)

check_fk(
    student_assessment,
    assessments,
    ["id_assessment"],
    ["id_assessment"],
    "studentAssessment -> assessments"
)

check_fk(
    student_vle,
    vle,
    ["code_module", "code_presentation", "id_site"],
    ["code_module", "code_presentation", "id_site"],
    "studentVle -> vle"
)

check_fk(
    student_vle,
    student_info,
    ["code_module", "code_presentation", "id_student"],
    ["code_module", "code_presentation", "id_student"],
    "studentVle -> studentInfo"
)

check_fk(
    student_registration,
    student_info,
    ["code_module", "code_presentation", "id_student"],
    ["code_module", "code_presentation", "id_student"],
    "studentRegistration -> studentInfo"
)

print("\n" + "=" * 70)
print("FINISHED")
print("=" * 70)