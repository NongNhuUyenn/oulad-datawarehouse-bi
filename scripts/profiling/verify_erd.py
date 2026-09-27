import pandas as pd
from pathlib import Path

DATA = Path("data/raw")

info = pd.read_csv(DATA / "studentInfo.csv")
registration = pd.read_csv(DATA / "studentRegistration.csv")
vle = pd.read_csv(DATA / "vle.csv")
student_vle = pd.read_csv(
    DATA / "studentVle.csv",
    usecols=["id_site"]
)

student_key = [
    "code_module",
    "code_presentation",
    "id_student"
]

print("=" * 60)
print("1. STUDENT_INFO <-> STUDENT_REGISTRATION")
print("=" * 60)

info_keys = info[student_key].drop_duplicates()
reg_keys = registration[student_key].drop_duplicates()

info_to_reg = info_keys.merge(
    reg_keys,
    on=student_key,
    how="left",
    indicator=True
)

reg_to_info = reg_keys.merge(
    info_keys,
    on=student_key,
    how="left",
    indicator=True
)

print("studentInfo unique keys:", len(info_keys))
print("studentRegistration unique keys:", len(reg_keys))

print(
    "studentInfo keys missing in studentRegistration:",
    (info_to_reg["_merge"] == "left_only").sum()
)

print(
    "studentRegistration keys missing in studentInfo:",
    (reg_to_info["_merge"] == "left_only").sum()
)


print("\n" + "=" * 60)
print("2. STUDENT_VLE.id_site -> VLE.id_site")
print("=" * 60)

print("VLE rows:", len(vle))
print("VLE unique id_site:", vle["id_site"].nunique())

unknown_sites = set(student_vle["id_site"]) - set(vle["id_site"])

print("studentVle unique id_site:", student_vle["id_site"].nunique())
print("id_site missing from VLE:", len(unknown_sites))

if len(unknown_sites) > 0:
    print("Example missing IDs:", list(unknown_sites)[:10])


print("\n" + "=" * 60)

if (
    len(info_keys) == len(reg_keys)
    and (info_to_reg["_merge"] == "left_only").sum() == 0
    and (reg_to_info["_merge"] == "left_only").sum() == 0
):
    print("StudentInfo <-> StudentRegistration: VERIFIED 1:1")
else:
    print("StudentInfo <-> StudentRegistration: NOT VERIFIED 1:1")

if len(unknown_sites) == 0 and vle["id_site"].is_unique:
    print("VLE.id_site -> StudentVle.id_site: VERIFIED 1:N")
else:
    print("VLE.id_site -> StudentVle.id_site: NOT VERIFIED 1:N")