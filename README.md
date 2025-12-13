 docker run -it -v "$(pwd):/app" -w /app python:3.11 sh -c "pip install psycopg2 tabulate && python analyze.py" > test_analyze.txt

# TODO
- do some sort of cycle to continuously read new
- update LAST_INDEX in db_connector
- datatempalte fill_template do
- datatemplateelement to_value do

```
rutmk_uid: d3d5e534-59b0-3fa1-9a0a-7ba6e4bec660
appl_receiving_date: 2025-03-04
appl_number: 2025880254
status_date: 2025-03-04
applicants: Дроздов Ярослав Даниилович
applicants_count: 1
mark_category: Service mark
goods: бальзам канадский;белила свинцовые;блестки для использования в краске;автобусы;автобусы дальнего следования;автожиры / гирокоптеры;белье купальное [за исключением одежды]
representatives: Общество с ограниченной ответственностью «Научно-производственное объединение «Медный путь»
ehd_serial: 22474
update_time: 2025-03-04 11:00:46.853000
object_uid: 1c1e5e06-2116-4d00-eb59-08dd57c96be1
doctype: 0
is_artificial: False
is_old: True
feature_category: 550
status_code_st27: A-1-1-W10-W00-X000
```
