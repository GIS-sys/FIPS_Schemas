import psycopg2
from typing import List, Dict, Any, Optional
from datetime import datetime

def get_last_n_trademark_ids(cur, n: int = 5) -> List[str]:
    """
    Получает ID последних N записей из основной таблицы товарных знаков
    """
    # Проверим, есть ли таблица fips_rutrademark и какие в ней есть ID-поля
    try:
        # Сначала посмотрим структуру таблицы
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'fips_rutrademark'
            AND column_name LIKE '%uid' 
            ORDER BY ordinal_position
        """)
        
        id_columns = cur.fetchall()
        
        # Если есть rutmk_uid, используем его
        if any('rutmk_uid' in col[0] for col in id_columns):
            cur.execute("""
                SELECT rutmk_uid FROM fips_rutrademark 
                ORDER BY ehd_serial DESC 
                LIMIT %s
            """, (n,))
        else:
            # Иначе попробуем найти другой ID
            cur.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'fips_rutrademark' 
                AND (column_name LIKE '%id%' OR column_name LIKE '%uid%')
                LIMIT 1
            """)
            id_column = cur.fetchone()
            if id_column:
                cur.execute(f"""
                    SELECT {id_column[0]} FROM fips_rutrademark 
                    ORDER BY ehd_serial DESC 
                    LIMIT %s
                """, (n,))
            else:
                # Если не нашли ID колонку, берем все записи
                cur.execute(f"""
                    SELECT * FROM fips_rutrademark 
                    ORDER BY ehd_serial DESC 
                    LIMIT %s
                """, (n,))
                # Вернем пустой список ID, но сохраним данные
                return []
        
        return [row[0] for row in cur.fetchall()]
    
    except Exception as e:
        print(f"Ошибка при получении ID записей: {e}")
        return []

def get_trademark_data(cur, trademark_id: str) -> Dict[str, Any]:
    """
    Получает данные о товарном знаке по ID
    """
    data = {"trademark_id": trademark_id}
    
    try:
        # Пробуем получить данные из fips_rutrademark по rutmk_uid
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'fips_rutrademark'
        """)
        
        columns = [row[0] for row in cur.fetchall()]
        
        if 'rutmk_uid' in columns:
            cur.execute("""
                SELECT * FROM fips_rutrademark 
                WHERE rutmk_uid = %s
            """, (trademark_id,))
        else:
            # Ищем другую ID колонку
            cur.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'fips_rutrademark' 
                AND (column_name LIKE '%id%' OR column_name LIKE '%uid%')
                LIMIT 1
            """)
            id_column = cur.fetchone()
            if id_column:
                cur.execute(f"""
                    SELECT * FROM fips_rutrademark 
                    WHERE {id_column[0]} = %s
                """, (trademark_id,))
            else:
                return data
        
        row = cur.fetchone()
        if row:
            # Получаем названия колонок
            cur.execute("SELECT * FROM fips_rutrademark LIMIT 0")
            col_names = [desc[0] for desc in cur.description]
            
            for col_name, value in zip(col_names, row):
                if value is not None:
                    data[f"trademark_{col_name}"] = value
        
        # Добавим информацию о таблице, откуда взяты данные
        data["source_table"] = "fips_rutrademark"
        
    except Exception as e:
        print(f"Ошибка при получении данных товарного знака: {e}")
    
    return data

def get_contact_data_by_trademark(cur, trademark_id: str) -> Dict[str, Any]:
    """
    Ищет контактные данные, связанные с товарным знаком
    """
    contact_data = {}
    
    # Список таблиц, которые могут содержать связь между товарным знаком и контактом
    link_tables = [
        'fips_rutmkapplicant',  # заявители товарных знаков РФ
        'fips_rutmkholder',     # правообладатели
        'fips_rutmkuser',       # пользователи
        'fips_wktmkapplicant',  # заявители международных товарных знаков
        'fips_softapplicant',   # заявители ПО
        'fips_dbapplicant',     # заявители БД
        'fips_ictapplicant',    # заявители ИКТ
    ]
    
    for table in link_tables:
        try:
            # Проверяем, существует ли таблица и есть ли в ней rutmk_uid
            cur.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s 
                AND column_name = 'rutmk_uid'
            """, (table,))
            
            if cur.fetchone():
                # Ищем contact_uid для данного товарного знака
                cur.execute(f"""
                    SELECT contact_uid FROM {table} 
                    WHERE rutmk_uid = %s 
                    LIMIT 1
                """, (trademark_id,))
                
                result = cur.fetchone()
                if result:
                    contact_uid = result[0]
                    # Получаем данные контакта
                    contact_data.update(get_contact_data(cur, contact_uid))
                    contact_data["contact_source_table"] = table
                    break
        
        except Exception as e:
            # Пропускаем таблицу, если ошибка
            continue
    
    return contact_data

def get_contact_data(cur, contact_uid: str) -> Dict[str, Any]:
    """
    Получает данные контакта по его UUID
    """
    data = {"contact_uid": contact_uid}
    
    try:
        cur.execute("""
            SELECT * FROM fips_contact 
            WHERE contact_uid = %s
        """, (contact_uid,))
        
        row = cur.fetchone()
        if row:
            # Получаем названия колонок
            cur.execute("SELECT * FROM fips_contact LIMIT 0")
            col_names = [desc[0] for desc in cur.description]
            
            for col_name, value in zip(col_names, row):
                if value is not None:
                    # Переименуем некоторые колонки для удобства
                    if col_name == 'name':
                        data['full_name'] = value
                    elif col_name == 'name_translit':
                        data['name_translit'] = value
                    elif col_name == 'phone':
                        data['phone'] = value
                    elif col_name == 'email':
                        data['email'] = value
                    elif col_name == 'inn':
                        data['inn'] = value
                    elif col_name == 'ogrn':
                        data['ogrn'] = value
                    elif col_name == 'snils':
                        data['snils'] = value
                    elif col_name == 'passport_number':
                        data['passport_number'] = value
                    elif col_name == 'address_text':
                        data['address'] = value
                    else:
                        data[col_name] = value
        
        # Получаем адресные данные из fips_correspondenceaddress
        data.update(get_correspondence_address(cur, contact_uid))
        
    except Exception as e:
        print(f"Ошибка при получении данных контакта: {e}")
    
    return data

def get_correspondence_address(cur, contact_uid: str) -> Dict[str, Any]:
    """
    Получает адресные данные для контакта
    """
    address_data = {}
    
    # Ищем адрес в разных таблицах
    address_tables = [
        'fips_correspondenceaddress',
        'fips_rutmkcorrespondenceaddress',
        'fips_wktmkcorrespondenceaddress',
        'fips_softcorrespondenceaddress',
        'fips_dbcorrespondenceaddress',
        'fips_ictcorrespondenceaddress'
    ]
    
    for table in address_tables:
        try:
            # Проверяем, существует ли таблица
            cur.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s 
                AND column_name LIKE '%contact_uid%'
            """, (table,))
            
            if cur.fetchone():
                # Ищем адрес для данного контакта
                cur.execute(f"""
                    SELECT * FROM {table} 
                    WHERE contact_uid = %s 
                    LIMIT 1
                """, (contact_uid,))
                
                row = cur.fetchone()
                if row:
                    # Получаем названия колонок
                    cur.execute(f"SELECT * FROM {table} LIMIT 0")
                    col_names = [desc[0] for desc in cur.description]
                    
                    for col_name, value in zip(col_names, row):
                        if value is not None:
                            address_data[f"address_{col_name}"] = value
                    
                    address_data["address_source_table"] = table
                    break
        
        except Exception as e:
            continue
    
    return address_data

def parse_fio(full_name: str) -> Dict[str, str]:
    """
    Парсит полное имя на составляющие
    """
    result = {
        'first_name': '',
        'last_name': '', 
        'middle_name': '',
        'full_name': full_name
    }
    
    if not full_name:
        return result
    
    parts = full_name.strip().split()
    
    if len(parts) >= 3:
        # Предполагаем формат "Фамилия Имя Отчество"
        result['last_name'] = parts[0]
        result['first_name'] = parts[1]
        result['middle_name'] = ' '.join(parts[2:])
    elif len(parts) == 2:
        result['last_name'] = parts[0]
        result['first_name'] = parts[1]
    elif len(parts) == 1:
        result['last_name'] = parts[0]
    
    return result

def enhance_contact_data(contact_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Улучшает и структурирует данные контакта
    """
    enhanced = contact_data.copy()
    
    # Парсим ФИО
    if 'full_name' in contact_data:
        fio_data = parse_fio(contact_data['full_name'])
        enhanced.update(fio_data)
    
    # Определяем тип лица
    if 'inn' in contact_data:
        inn = contact_data['inn']
        if len(inn) == 10:
            enhanced['entity_type'] = 'legal_entity'
            enhanced['inn_length'] = 10
        elif len(inn) == 12:
            enhanced['entity_type'] = 'individual_entrepreneur'
            enhanced['inn_length'] = 12
        else:
            enhanced['entity_type'] = 'unknown'
    elif 'passport_number' in contact_data:
        enhanced['entity_type'] = 'individual'
    else:
        enhanced['entity_type'] = 'unknown'
    
    # Извлекаем email и телефон
    if 'email' in contact_data and contact_data['email']:
        emails = contact_data['email'].split(',')
        enhanced['email_list'] = [email.strip() for email in emails]
        enhanced['primary_email'] = emails[0].strip() if emails else None
    
    if 'phone' in contact_data and contact_data['phone']:
        phones = contact_data['phone'].split(';')
        enhanced['phone_list'] = [phone.strip() for phone in phones]
        enhanced['primary_phone'] = phones[0].strip() if phones else None
    
    # Добавляем timestamp
    enhanced['data_collected_at'] = datetime.now().isoformat()
    
    return enhanced

def get_data_dict_by_id(cur, record_id: str) -> Dict[str, Any]:
    """
    Основная функция: собирает все данные по ID записи
    """
    print(f"\nСбор данных для записи: {record_id}")
    print("-" * 50)
    
    # 1. Получаем данные товарного знака
    trademark_data = get_trademark_data(cur, record_id)
    print(f"Данные товарного знака: {len(trademark_data)} полей")
    
    # 2. Получаем контактные данные
    contact_data = get_contact_data_by_trademark(cur, record_id)
    print(f"Контактные данные: {len(contact_data)} полей")
    
    # 3. Объединяем и улучшаем данные
    combined_data = {
        'record_id': record_id,
        'trademark': {k: v for k, v in trademark_data.items() if not k.startswith('trademark_')},
        'contact': enhance_contact_data(contact_data),
        'collection_info': {
            'collected_at': datetime.now().isoformat(),
            'trademark_fields_count': len(trademark_data),
            'contact_fields_count': len(contact_data)
        }
    }
    
    # Добавляем данные товарного знака с префиксом
    for key, value in trademark_data.items():
        if key.startswith('trademark_'):
            field_name = key.replace('trademark_', '')
            combined_data['trademark'][field_name] = value
    
    print(f"Всего собрано полей: {len(combined_data['trademark']) + len(combined_data['contact'])}")
    
    return combined_data

def get_all_records_data(cur, num_records: int = 5) -> List[Dict[str, Any]]:
    """
    Получает данные для N последних записей
    """
    print(f"Получение данных для {num_records} последних записей...")
    
    # Получаем ID последних записей
    record_ids = get_last_n_trademark_ids(cur, num_records)
    
    if not record_ids:
        print("Не удалось получить ID записей. Пробуем альтернативный подход...")
        
        # Пробуем получить данные напрямую
        try:
            cur.execute("""
                SELECT rutmk_uid FROM fips_rutrademark 
                LIMIT %s
            """, (num_records,))
            record_ids = [row[0] for row in cur.fetchall()]
        except:
            try:
                cur.execute("SELECT * FROM fips_rutrademark LIMIT %s", (num_records,))
                rows = cur.fetchall()
                if rows:
                    # Берем первые 5 записей
                    cur.execute("SELECT * FROM fips_rutrademark LIMIT 0")
                    col_names = [desc[0] for desc in cur.description]
                    
                    # Создаем словари для каждой записи
                    all_data = []
                    for i, row in enumerate(rows):
                        record_data = {}
                        for col_name, value in zip(col_names, row):
                            if value is not None:
                                record_data[col_name] = value
                        
                        if record_data:
                            enhanced_data = {
                                'record_id': f"record_{i+1}",
                                'trademark': record_data,
                                'contact': {},
                                'collection_info': {
                                    'collected_at': datetime.now().isoformat(),
                                    'note': 'Данные получены напрямую из fips_rutrademark'
                                }
                            }
                            all_data.append(enhanced_data)
                    
                    return all_data
            except Exception as e:
                print(f"Ошибка: {e}")
                return []
    
    print(f"Найдено ID записей: {len(record_ids)}")
    
    # Собираем данные для каждой записи
    all_data = []
    for record_id in record_ids:
        try:
            record_data = get_data_dict_by_id(cur, record_id)
            all_data.append(record_data)
        except Exception as e:
            print(f"Ошибка при сборе данных для {record_id}: {e}")
            all_data.append({
                'record_id': record_id,
                'error': str(e),
                'trademark': {},
                'contact': {}
            })
    
    return all_data

def print_record_summary(record: Dict[str, Any]):
    """
    Выводит краткую информацию о записи
    """
    print(f"\n{'='*60}")
    print(f"Запись ID: {record.get('record_id', 'N/A')}")
    print(f"{'='*60}")
    
    # Данные товарного знака
    trademark = record.get('trademark', {})
    if trademark:
        print("\nДАННЫЕ ТОВАРНОГО ЗНАКА:")
        print("-" * 40)
        
        # Выводим ключевые поля
        key_fields = ['rutmk_uid', 'application_number', 'application_date', 
                     'registration_number', 'registration_date', 'mark_verbal_element_text']
        
        for field in key_fields:
            if field in trademark:
                value = trademark[field]
                if value:
                    print(f"{field:30} : {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
    
    # Контактные данные
    contact = record.get('contact', {})
    if contact:
        print("\nКОНТАКТНЫЕ ДАННЫЕ:")
        print("-" * 40)
        
        if 'full_name' in contact and contact['full_name']:
            print(f"{'Полное имя':30} : {contact['full_name']}")
        
        if 'last_name' in contact and contact['last_name']:
            print(f"{'Фамилия':30} : {contact['last_name']}")
        if 'first_name' in contact and contact['first_name']:
            print(f"{'Имя':30} : {contact['first_name']}")
        if 'middle_name' in contact and contact['middle_name']:
            print(f"{'Отчество':30} : {contact['middle_name']}")
        
        if 'inn' in contact and contact['inn']:
            print(f"{'ИНН':30} : {contact['inn']} ({contact.get('entity_type', 'тип не определен')})")
        
        if 'email' in contact and contact['email']:
            print(f"{'Email':30} : {contact['email']}")
        
        if 'phone' in contact and contact['phone']:
            print(f"{'Телефон':30} : {contact['phone']}")
        
        if 'address' in contact and contact['address']:
            print(f"{'Адрес':30} : {contact['address'][:100]}{'...' if len(contact['address']) > 100 else ''}")
    
    # Информация о сборе
    collection_info = record.get('collection_info', {})
    if collection_info:
        print(f"\n{'Информация о сборе':30} : {collection_info.get('collected_at', 'N/A')}")
        print(f"{'Полей товарного знака':30} : {collection_info.get('trademark_fields_count', 0)}")
        print(f"{'Полей контакта':30} : {collection_info.get('contact_fields_count', 0)}")
    
    print(f"\nВсего полей в записи: {len(record)}")

# Основная функция для тестирования
def main():
    """
    Основная функция для сбора данных
    """
    # Здесь будет ваш код подключения к БД
    conn = psycopg2.connect(
        host="10.2.53.15",
        port=5432,
        #database="smev_adapter_single",
        database="uad_int",
        user="gegorov",
        password="87zerkaLo22"
    )
    cur = conn.cursor()
    
    # Для примера, покажем структуру
    print("СКРИПТ ДЛЯ СБОРА ДАННЫХ ИЗ БАЗЫ ДАННЫХ")
    print("=" * 60)
    print("Этот скрипт собирает данные из таблиц fips_rutrademark и fips_contact")
    print("и формирует структурированные словари с данными.")
    
    # Пример использования (раскомментируйте для работы с реальной БД):
    try:
        # Подключение к БД
        conn = psycopg2.connect(
            host="ваш_хост",
            database="ваша_бд",
            user="ваш_пользователь",
            password="ваш_пароль"
        )
        cur = conn.cursor()
        
        # Получаем данные для 5 записей
        records_data = get_all_records_data(cur, 5)
        
        # Выводим краткую информацию по каждой записи
        for i, record in enumerate(records_data):
            print(f"\n{'#'*60}")
            print(f"ЗАПИСЬ #{i+1}")
            print_record_summary(record)
            
            # Если нужен полный вывод:
            # print(f"\nПолные данные записи #{i+1}:")
            # print(record)
        
        print(f"\n{'='*60}")
        print(f"Всего обработано записей: {len(records_data)}")
        
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
