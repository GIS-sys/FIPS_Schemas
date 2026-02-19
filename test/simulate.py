import psycopg2
import uuid
import random
import csv
import datetime
import sys
import os
from psycopg2 import sql

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
    columns = list(data.keys())
    values = [data[col] for col in columns]
    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    cursor.execute(query, values)

def get_ogrn() -> str:
    return random_word(13, DIGITS_NO_ZERO)

def get_kpp() -> str:
    return random_word(9, DIGITS_NO_ZERO)

def get_snils() -> str:
    return random_word(11, DIGITS_NO_ZERO)

def get_inn_for_type(t: str) -> str:
    if t == "FL":
        return random_word(12, DIGITS_NO_ZERO)
    if t == "UL":
        return random_word(10, DIGITS_NO_ZERO)
    if t == "IP":
        return random_word(12, DIGITS_NO_ZERO)
    raise Exveption(f"get_inn_for_type expected t in [FL, UL, IP], got {t}")

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
def op_add_base(cursor):
    """Add a new row to fips_rutrademark and linked rows to fips_contact and Objects."""
    if not FIPS_RUTRADEMARK_SAMPLES:
        raise Exception("Cannot add trademark: no sample data available.")
    if not FIPS_CONTACT_SAMPLES:
        raise Exception("Cannot add contact: no sample data available.")
    if not OBJECTS_SAMPLES:
        raise Exception("Cannot add object: no sample data available.")

    # 1. Choose a random template from CSV
    template_rutrademark = random.choice(FIPS_RUTRADEMARK_SAMPLES)
    template_contact = random.choice(FIPS_CONTACT_SAMPLES)
    template_object = random.choice(OBJECTS_SAMPLES)

    # 2. Generate new UUIDs
    new_trademark_uid = new_uuid()
    new_contact_uid = new_uuid()
    new_object_uid = new_uuid()
    new_object_parent_uid = new_uuid()
    new_applicant_type_str = select_from_list("Enter contact_type: ", ["FL", "UL", "IP"])
    new_applicant_type_int = ["FL", "UL", "IP"].index(new_applicant_type_str)
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

    # 3. Build trademark row (copy most fields, override a few)
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
    # Keep other fields as in template

    # 4. Build contact row
    contact = template_contact.copy()
    contact['contact_uid'] = new_contact_uid
    contact['name'] = new_applicant_name
    contact['contact_type'] = new_applicant_type_int
    if new_applicant_type_str == "FL":
        contact['snils'] = get_snils() if select_binary("Add СНИЛС? ") else None
        contact['inn'] = get_inn_for_type(new_applicant_type_str) if select_binary("Add ИНН? ") else None
    elif new_applicant_type_str == "UL":
        contact['ogrn'] = get_ogrn() if select_binary("Add ОГРН? ") else None
        contact['inn'] = get_inn_for_type(new_applicant_type_str) if select_binary("Add ИНН? ") else None
        contact['customer_number'] = get_kpp() if select_binary("Add КПП? ") else None
    elif new_applicant_type_str == "IP":
        contact['ogrn'] = get_ogrn() if select_binary("Add ОГРН? ") else None
        contact['inn'] = get_inn_for_type(new_applicant_type_str) if select_binary("Add ИНН? ") else None
    else:
        raise Exception(f"Unknown {new_applicant_type_str=}")
    contact['language_code'] = 'ru'
    contact['update_time'] = now()
    contact['delete_time'] = None
    # Keep other fields as in template

    # 5. Build contact-trademark connection row
    rutmkapplicant = {
        'contact_uid': new_contact_uid,
        'rutmk_uid': new_trademark_uid,
    }

    # 5. Build object row
    obj = template_object.copy()
    obj['Number'] = new_object_uid
    obj['ParentNumber'] = new_object_parent_uid
    obj['UpdateDate'] = now()
    obj['CreatedDate'] = now()
    obj['Kind'] = 150000
    # Keep other fields as in template

    # 6. Insert all rows
    try:
        insert_dict(cursor, 'fips_rutrademark', trademark)
        insert_dict(cursor, 'fips_contact', contact)
        insert_dict(cursor, 'Objects', obj)
        insert_dict(cursor, 'fips_rutmkapplicant', rutmkapplicant)
        print(f"✅ Added trademark {new_trademark_uid} (applicant: {new_applicant_name})")
        print(f"✅ Added contact {new_contact_uid} for this applicant")
        print(f"✅ Added object {new_object_uid} for this trademark (parent: {new_object_parent_uid})")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return

    # 7. Remember for later operations
    added_trademarks.append({
        'trademark_row': trademark,
        'contact_row': contact,
        'object_row': obj,
    })

# ========== Operation 2: Add another Object with Kind=150002 ==========
def op_add_object_trigger(cursor):
    """Insert a new Object row with a new Number and an existing parent."""
    if not OBJECTS_SAMPLES:
        raise Exception("Cannot add object: no sample data available.")
    if len(added_trademarks) == 0:
        print("No parent Objects available.")
        return

    # 1. Choose a random template from CSV
    template_object = random.choice(OBJECTS_SAMPLES)

    # 2. Select parent
    def obj_display(trademark):
        t = trademark['trademark_row']
        o = trademark['object_row']
        return f"{o['Number']} (parent={o['ParentNumber']}, applicant={t['applicants']})"
    parent = select_from_list("Choose parent Object (by index): ", added_trademarks, obj_display)
    if not parent:
        return
    parent_uuid = parent['object_row']['ParentNumber']

    # 3. Generate new UUID for this child Object
    new_object_uid = new_uuid()

    # 4. Build object row
    obj = template_object.copy()
    obj['Number'] = new_object_uid
    obj['ParentNumber'] = parent_uuid
    obj['UpdateDate'] = now()
    obj['CreatedDate'] = now()
    obj['Kind'] = 150002
    # Keep other fields as in template

    # 5. Insert all rows
    try:
        insert_dict(cursor, 'Objects', obj)
        print(f"✅ Added child Object {new_object_uid} with parent {parent_uuid}")
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
        print("3 : (TODO) Add SearchAttributes for a trademark (requires existing Object)")
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
        else:
            print("Unknown command.")

    cursor.close()
    conn.close()
    print("Bye.")

if __name__ == '__main__':
    main()

