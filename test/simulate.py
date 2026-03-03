import psycopg2
import uuid
import random
import csv
import datetime
import sys
import os
from psycopg2 import sql

import validate
import util


# ========== Load sample data from CSV files ==========
def load_csv_to_dict_list(filepath: str):
    """Read CSV file and return list of dictionaries (one per row)."""
    rows = []
    try:
        with open(os.path.join(util.OUTPUT_DIR, filepath), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Some operations may use defaults.")
    return rows

FIPS_RUTRADEMARK_SAMPLES = load_csv_to_dict_list('fips_rutrademark.csv')
FIPS_CONTACT_SAMPLES = load_csv_to_dict_list('fips_contact.csv')
OBJECTS_SAMPLES = load_csv_to_dict_list('Objects.csv')
SEARCH_ATTRIBUTES_SAMPLES = load_csv_to_dict_list('SearchAttributes.csv')





# ========== Global state (in‑memory) ==========
ALPHABET = "qwertyuiopasdfghjklzxcvbnm"
DIGITS_NO_ZERO = "123456789"
DIGITS = DIGITS_NO_ZERO + "0"

# Trademarks added during this session
added_trademarks = []  # each is dict of rows
added_objects = []  # each is a row

# ========== Helpers ==========
def random_word(length: int = 5, alphabet=ALPHABET) -> str:
    return "".join([random.choice(alphabet) for _ in range(length)])

def now():
    """Current timestamp in ISO format."""
    return datetime.datetime.now().isoformat()

def new_uuid():
    """Generate a new UUID4 string."""
    return str(uuid.uuid4())

def random_appl_number():
    """Generate a plausible application number (10 digits)."""
    return f"2025{random.randint(100000, 999999)}"

def insert_dict(cursor, table: str, data: dict):
    """
    Insert a dictionary into the specified table.
    Keys are column names, values are the values (None becomes SQL NULL).
    """
    data = {k: v for k, v in data.items() if v is not None}
    columns = list(data.keys())
    values = [data[col] for col in columns]
    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    cursor.execute(query, values)

def get_ogrn(t: str) -> str:
    if t == "UL":
        main = random.choice(("1", "5")) + random_word(11, DIGITS_NO_ZERO)
        return main + validate.get_control_ogrn(t, main)
    if t == "IP":
        main = "3" + random_word(13, DIGITS_NO_ZERO)
        return main + validate.get_control_ogrn(t, main)
    raise Exception(f"get_ogrn expected t in [UL, IP], got {t}")

def get_kpp() -> str:
    return random_word(4, DIGITS_NO_ZERO) + "01" + random_word(3, DIGITS_NO_ZERO)

def get_snils() -> str:
    main = random_word(9, DIGITS_NO_ZERO)
    return main + validate.get_control_snils(main)

def get_inn(t: str) -> str:
    if t == "UL":
        main = random_word(9, DIGITS_NO_ZERO)
        return main + validate.get_control_inn(t, main)
    if t == "IP" or t == "FL":
        main = random_word(10, DIGITS_NO_ZERO)
        return main + validate.get_control_inn(t, main)
    raise Exception(f"get_inn expected t in [FL, UL, IP], got {t}")

def list_choices(items, display_func):
    """Print enumerated list of items and return a dict mapping index->item."""
    for idx, item in enumerate(items):
        print(f"  {idx}: {display_func(item)}")
    return {str(idx): item for idx, item in enumerate(items)}

def select_from_list(prompt: str, items, display_func = str):
    """
    Prompt user to select an item from a list by index.
    Returns the selected item or None if empty list.
    """
    if not items:
        print("No items available.")
        return None
    choices = list_choices(items, display_func)
    while True:
        inp = input(prompt).strip()
        if inp in choices:
            return choices[inp]
        print("Invalid selection. Try again.")

def select_binary(prompt: str) -> bool:
    """
    Returns True if yes, False if No
    """
    return select_from_list(prompt, ["Нет", "Да"]) == "Да"





# ========== Operation 1: Add trademark + contact ==========
# new_applicant_type_str, new_applicant_name, snils, inn, ogrn, kpp
BASE_USERS = [
    ("FL", "Человек Без Документов", None, None, None, None),
    ("FL", "Человек СНИЛС", get_snils(), None, None, None),
    ("FL", "Человек ИНН", None, get_inn("FL"), None, None),
    ("FL", "Человек СНИЛС ИНН", get_snils(), get_inn("FL"), None, None),
    ("UL", "ООО <БЕЗ ДОКУМЕНТОВ>", None, None, None, None),
    ("UL", "ООО <ОГРН>", None, None, get_ogrn("UL"), None),
    ("UL", "ООО <КПП>", None, None, None, get_kpp()),
    ("UL", "ООО <ОГРН КПП>", None, None, get_ogrn("UL"), get_kpp()),
    ("UL", "ООО <ИНН>", None, get_inn("UL"), None, None),
    ("UL", "ООО <ИНН ОГРН>", None, get_inn("UL"), get_ogrn("UL"), None),
    ("UL", "ООО <ИНН КПП>", None, get_inn("UL"), None, get_kpp()),
    ("UL", "ООО <ИНН ОГРН КПП>", None, get_inn("UL"), get_ogrn("UL"), get_kpp()),
    ("UL", "ООО <ИНН ОГРН КПП>", None, get_inn("UL"), get_ogrn("UL"), get_kpp()),
    ("IP", "Без Документов", None, None, None, None),
    ("IP", "ИНН", None, get_inn("IP"), None, None),
    ("IP", "ОГРН", None, None, get_ogrn("IP"), None),
    ("IP", "Я ЛЮБЛЮ ИНН ОГРН", None, get_inn("IP"), get_ogrn("IP"), None),
    ("IP", "ИНН ОГРН", None, get_inn("IP"), get_ogrn("IP"), None),
    ("IP", "ИП ИНН ОГРН", None, get_inn("IP"), get_ogrn("IP"), None),
    ("IP", "ИндиВИдуальный предприниматель ИНН ОГРН", None, get_inn("IP"), get_ogrn("IP"), None),

    ("FL", "Человек Невалидный СНИЛС+100", str(int(''.join([c for c in get_snils() if c in DIGITS]))+100), None, None, None),
    ("FL", "Человек Невалидный ИННЮЛ", None, get_inn("UL"), None, None),
    ("FL", "Человек Невалидный ИНН+100", None, str(int(get_inn("FL"))+100), None, None),
    ("UL", "ООО Невалидный ИННФЛ КПП", None, get_inn("FL"), None, get_kpp()),
    ("UL", "ООО Невалидный ИННЮЛ+10 КПП", None, str(int(get_inn("UL"))+10), None, get_kpp()),
    ("UL", "ООО Невалидный ОГРНИП", None, None, get_ogrn("IP"), None),
    ("UL", "ООО Невалидный ОГРН+10", None, None, str(int(get_ogrn("UL"))+10), None),
    ("IP", "ИП Невалидный ИННЮЛ ОГРН", None, get_inn("UL"), get_ogrn("IP"), None),
    ("IP", "ИП Невалидный ИНН+1000 ОГРН", None, str(int(get_inn("IP"))+1000), get_ogrn("IP"), None),
    ("IP", "ИП Невалидный ИНН ОГРНЮЛ", None, get_inn("IP"), get_ogrn("UL"), None),
    ("IP", "ИП Невалидный ИНН ОГРН+1000", None, get_inn("IP"), str(int(get_ogrn("IP"))+1000), None),
    ("UNK", "нЕвАлИдНыЙ тИп", get_snils(), get_inn("FL"), get_ogrn("UL"), get_kpp()),
]
OCCODES = ["004", "010", "700", "730", "940"]

def op_add_base(cursor, new_applicant_type_str: str = None, new_applicant_name: str = None, snils: str = None, inn: str = None, ogrn: str = None, kpp: str = None, no_input: bool = False):
    """Add a new row to fips_rutrademark and linked rows to fips_contact and Objects."""
    if not FIPS_RUTRADEMARK_SAMPLES:
        raise Exception("Cannot add trademark: no sample data available.")
    if not FIPS_CONTACT_SAMPLES:
        raise Exception("Cannot add contact: no sample data available.")
    if not OBJECTS_SAMPLES:
        raise Exception("Cannot add object: no sample data available.")
    if not SEARCH_ATTRIBUTES_SAMPLES:
        raise Exception("Cannot add search attributes: no sample data available.")

    # 1. Choose random templates from CSV
    template_rutrademark = random.choice(FIPS_RUTRADEMARK_SAMPLES)
    template_contact = random.choice(FIPS_CONTACT_SAMPLES)
    template_object = random.choice(OBJECTS_SAMPLES)

    # 2. Generate new UUIDs
    new_trademark_uid = new_uuid()
    new_contact_uid = new_uuid()
    new_object_uid = new_uuid()
    new_object_parent_uid = new_uuid()
    arr = ["FL", "UL", "IP"]
    if not new_applicant_type_str and not no_input:
        new_applicant_type_str = select_from_list("Enter contact_type: ", arr)
    new_applicant_type_int = arr.index(new_applicant_type_str) if new_applicant_type_str in arr else -1
    if not new_applicant_name and not no_input:
        if select_binary("Want to enter applicant name yourself?"):
            new_applicant_name = input("name: ")
        else:
            if new_applicant_type_str == "FL":
                new_applicant_name = f"{random_word()} {random_word()} {random_word()}"
            elif new_applicant_type_str == "UL":
                new_applicant_name = f"ООО {random_word()}"
            elif new_applicant_type_str == "IP":
                name_prefix = select_from_list("Select name prefix: ", ["ИП", "Индивидуальный предприниматель", ""])
                new_applicant_name = f"{name_prefix} {random_word()} {random_word()} {random_word()}"
            else:
                raise Exception(f"Unknown {new_applicant_type_str=}")

    # 3. Build trademark row
    trademark = template_rutrademark.copy()
    trademark['rutmk_uid'] = new_trademark_uid
    trademark['object_uid'] = new_object_uid
    trademark['applicants'] = new_applicant_name
    trademark['appl_number'] = random_appl_number()
    trademark['appl_date'] = now()[:10]
    trademark['appl_receiving_date'] = now()[:10]
    trademark['update_time'] = now()
    trademark['delete_time'] = None
    trademark['effective_date'] = None

    # 4. Build contact row
    contact = template_contact.copy()
    contact['contact_uid'] = new_contact_uid
    contact['name'] = new_applicant_name
    contact['contact_type'] = new_applicant_type_int
    if new_applicant_type_str == "FL":
        contact['snils'] = snils if snils or no_input else (get_snils() if select_binary("Add СНИЛС? ") else None)
        contact['inn'] = inn if inn or no_input else (get_inn(new_applicant_type_str) if select_binary("Add ИНН? ") else None)
    elif new_applicant_type_str == "UL":
        contact['ogrn'] = ogrn if ogrn or no_input else (get_ogrn("UL") if select_binary("Add ОГРН? ") else None)
        contact['inn'] = inn if inn or no_input else (get_inn(new_applicant_type_str) if select_binary("Add ИНН? ") else None)
        contact['customer_number'] = kpp if kpp or no_input else (get_kpp() if select_binary("Add КПП? ") else None)
    elif new_applicant_type_str == "IP":
        contact['ogrn'] = ogrn if ogrn or no_input else (get_ogrn("IP") if select_binary("Add ОГРН? ") else None)
        contact['inn'] = inn if inn or no_input else (get_inn(new_applicant_type_str) if select_binary("Add ИНН? ") else None)
    else:
        if not no_input:
            print(f"Unknown {new_applicant_type_str=}")
    contact['language_code'] = 'ru'
    contact['update_time'] = now()
    contact['delete_time'] = None

    # 5. Build contact-trademark connection row
    rutmkapplicant = {
        'contact_uid': new_contact_uid,
        'rutmk_uid': new_trademark_uid,
    }

    # 6. Build PARENT Objects row (new)
    parent_obj = template_object.copy()
    parent_obj['Number'] = new_object_parent_uid
    parent_obj['ParentNumber'] = None          # root parent, adjust if needed
    parent_obj['UpdateDate'] = now()
    parent_obj['CreatedDate'] = now()
    parent_obj['Kind'] = 150001                # typical parent kind

    # 7. Build CHILD Objects row (linked to trademark)
    child_obj = template_object.copy()
    child_obj['Number'] = new_object_uid
    child_obj['ParentNumber'] = new_object_parent_uid
    child_obj['UpdateDate'] = now()
    child_obj['CreatedDate'] = now()
    child_obj['Kind'] = 150000                 # typical kind for trademark object

    # 8. Insert all rows (no SearchAttributes inserted here)
    try:
        # Insert parent object first (no FK dependency)
        insert_dict(cursor, 'Objects', parent_obj)
        insert_dict(cursor, 'fips_rutrademark', trademark)
        insert_dict(cursor, 'fips_contact', contact)
        insert_dict(cursor, 'Objects', child_obj)
        insert_dict(cursor, 'fips_rutmkapplicant', rutmkapplicant)
        print(f"\n{new_applicant_name}")
        print(f"✅ Added trademark {trademark}")
        print(f"✅ Added contact {contact} for this applicant")
        print(f"✅ Added parent object {parent_obj['Number']} (kind={parent_obj['Kind']})")
        print(f"✅ Added child object {child_obj['Number']} (kind={child_obj['Kind']}) linked to trademark")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return

    # 9. Remember for later operations
    added_trademarks.append({
        'trademark_row': trademark,
        'contact_row': contact,
        'parent_object_row': parent_obj,
        'child_object_row': child_obj,
    })

# ========== Operation 2: Add another Object with Kind=150002 ==========
def op_add_object_trigger(cursor, parent_uuid: str = None, kind: int = 150002):
    """Insert a new Object row with a new Number and an existing parent."""
    if not OBJECTS_SAMPLES:
        raise Exception("Cannot add object: no sample data available.")
    if len(added_trademarks) == 0:
        print("No parent Objects available.")
        return

    # 1. Choose random templates from CSV
    template_object = random.choice(OBJECTS_SAMPLES)
    template_search_attributes = random.choice(SEARCH_ATTRIBUTES_SAMPLES)

    # 2. Select parent (the parent object inserted in op_add_base)
    def obj_display(trademark):
        t = trademark['trademark_row']
        p = trademark['parent_object_row']      # now we have parent object stored
        return f"Parent: {p['Number']} (kind={p['Kind']}) – trademark: {t['applicants']}"
    if not parent_uuid:
        parent_trademark = select_from_list("Choose parent Object (by index): ", added_trademarks, obj_display)
        if not parent_trademark:
            return
        parent_uuid = parent_trademark['parent_object_row']['Number']

    # 3. Generate new UUID for this child Object
    new_object_uid = new_uuid()
    new_sa_date_uid = new_uuid()
    new_sa_code_uid = new_uuid()

    # 4. Build object row (Kind = 150002)
    obj = template_object.copy()
    obj['Number'] = new_object_uid
    obj['ParentNumber'] = parent_uuid
    obj['UpdateDate'] = now()
    obj['CreatedDate'] = now()
    obj['Kind'] = kind
    # Keep other fields as in template

    # 5. Build search attributes rows for the new object
    sa_date = template_search_attributes.copy()
    sa_date['ID'] = new_sa_date_uid
    sa_date['ParentNumber'] = new_object_uid
    sa_date['Name'] = "OCDate"
    sa_date['TextValue'] = now()[:10]
    sa_date['TextValue'] = '.'.join(reversed(sa_date['TextValue'].split('-')))
    sa_date['CreatedDate'] = now()

    sa_code = template_search_attributes.copy()
    sa_code['ID'] = new_sa_code_uid
    sa_code['ParentNumber'] = new_object_uid
    sa_code['Name'] = "OCCode"
    sa_code['TextValue'] = random.choice(OCCODES)
    sa_code['CreatedDate'] = now()

    # 6. Insert rows
    try:
        insert_dict(cursor, 'Objects', obj)
        insert_dict(cursor, 'SearchAttributes', sa_date)
        insert_dict(cursor, 'SearchAttributes', sa_code)
        print(f"✅ Added child Object {new_object_uid} with parent {parent_uuid} (kind=150002)")
        print(f"✅ Added SearchAttribute (OCDate) for this object")
        print(f"✅ Added SearchAttribute (OCCode) for this object")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return

    added_objects.append(obj)





# ========== Main interactive loop ==========
def main():
    print("=== Database Simulator ===")
    print("Connecting to database...")
    try:
        conn = psycopg2.connect(**util.load_config(config_path=util.CONFIG_PATH_TEST))
        conn.autocommit = True
        cursor = conn.cursor()
    except Exception as e:
        print(f"Cannot connect to database: {e}")
        sys.exit(1)

    print("Connected. Tables must already exist (use fill_database_data.py if needed).")
    print("Type a command and press Enter.\n")

    while True:
        print("\n--- Commands ---")
        print("1 : Add trademark + contact + object")
        print("2 : Add another Object with same parent and Kind=150002")
        print("9 : Add ALL KINDS of new records automatically")
        print("q : quit")
        cmd = input("> ").strip().lower()

        if cmd == 'q':
            break
        elif cmd == '1':
            op_add_base(cursor)
        elif cmd == '2':
            op_add_object_trigger(cursor)
        elif cmd == '3':
            raise NotImplementedError()
            # op_add_search_attribute(cursor)
        elif cmd == '9':
            # Add all base users
            for d in BASE_USERS:
                op_add_base(
                    cursor,
                    new_applicant_type_str = d[0],
                    new_applicant_name = d[1],
                    snils = d[2],
                    inn = d[3],
                    ogrn = d[4],
                    kpp = d[5],
                    no_input=True,
                )

            # Define how many extra objects to add for each base user (0 - 3)
            object_counts = [(i % 4) for i in range(len(BASE_USERS))]

            # For each added trademark, add the specified number of objects under its parent
            for i, trademark_info in enumerate(added_trademarks):
                count = object_counts[i]
                parent_uuid = trademark_info['parent_object_row']['Number']
                for _ in range(count):
                    op_add_object_trigger(cursor, parent_uuid=parent_uuid)
        else:
            print("Unknown command.")

    cursor.close()
    conn.close()
    print("Bye.")

if __name__ == '__main__':
    main()

