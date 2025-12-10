import psycopg2
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any, Optional

def get_last_n_trademarks(cur, n: int = 5) -> List[Dict[str, Any]]:
    """
    Получает последние N записей из таблицы fips_rutrademark
    """
    query = """
        SELECT * FROM fips_rutrademark 
        ORDER BY ehd_serial DESC 
        LIMIT %s
    """
    cur.execute(query, (n,))
    
    # Получаем названия колонок
    columns = [desc[0] for desc in cur.description]
    
    results = []
    for row in cur.fetchall():
        row_dict = dict(zip(columns, row))
        results.append(row_dict)
    
    return results

def get_contact_info(cur, contact_uid: str) -> Optional[Dict[str, Any]]:
    """
    Получает информацию о контакте по его UUID
    """
    query = """
        SELECT * FROM fips_contact 
        WHERE contact_uid = %s
        LIMIT 1
    """
    cur.execute(query, (contact_uid,))
    
    row = cur.fetchone()
    if not row:
        return None
    
    # Получаем названия колонок
    columns = [desc[0] for desc in cur.description]
    return dict(zip(columns, row))

def get_applicant_contact(cur, rutmk_uid: str) -> Optional[Dict[str, Any]]:
    """
    Получает контакт заявителя для конкретного товарного знака
    """
    # Сначала ищем в таблице fips_rutmkapplicant
    query = """
        SELECT contact_uid FROM fips_rutmkapplicant 
        WHERE rutmk_uid = %s 
        LIMIT 1
    """
    cur.execute(query, (rutmk_uid,))
    
    row = cur.fetchone()
    if row and row[0]:
        return get_contact_info(cur, row[0])
    
    # Если не нашли в fips_rutmkapplicant, ищем в других таблицах
    # (можно добавить другие таблицы по необходимости)
    return None

def determine_applicant_type(contact: Dict[str, Any]) -> str:
    """
    Определяет тип заявителя на основе данных контакта
    """
    if contact.get('inn'):
        inn = contact['inn']
        # Если ИНН длиной 10 - юридическое лицо
        if len(inn) == 10:
            return 'legal'
        # Если ИНН длиной 12 - ИП или физлицо
        elif len(inn) == 12:
            return 'ip'
    
    # Если есть паспортные данные - физлицо
    if contact.get('passport_number'):
        return 'individual'
    
    # По умолчанию считаем физлицом
    return 'individual'

def split_fio(full_name: str) -> tuple:
    """
    Разбивает полное ФИО на компоненты
    """
    parts = full_name.split()
    if len(parts) >= 3:
        return parts[0], parts[1], ' '.join(parts[2:])
    elif len(parts) == 2:
        return parts[0], parts[1], ''
    elif len(parts) == 1:
        return parts[0], '', ''
    else:
        return '', '', ''

def create_user_element(parent, contact: Dict[str, Any]) -> ET.Element:
    """
    Создает элемент пользователя (физического лица)
    """
    user = ET.SubElement(parent, 'user')
    
    # Разбиваем ФИО
    last_name, first_name, middle_name = split_fio(contact.get('name', ''))
    
    # Пока используем userPersonalDoc как в примере
    # В реальном приложении нужно выбирать тип документа на основе данных
    user_personal_doc = ET.SubElement(user, 'userPersonalDoc')
    
    # Тип документа удостоверяющего личность (1 - паспорт гражданина РФ)
    ET.SubElement(user_personal_doc, 'PersonalDocType').text = '1'
    
    # Номер паспорта (если есть)
    passport = contact.get('passport_number', '')
    ET.SubElement(user_personal_doc, 'number').text = passport if passport else '1234567890'
    
    # ФИО
    ET.SubElement(user_personal_doc, 'lastName').text = last_name if last_name else 'Иванов'
    ET.SubElement(user_personal_doc, 'firstName').text = first_name if first_name else 'Иван'
    
    if middle_name:
        ET.SubElement(user_personal_doc, 'middleName').text = middle_name
    
    # Гражданство (1 - Россия)
    ET.SubElement(user_personal_doc, 'citizenship').text = '1'
    
    return user

def create_organization_element(parent, contact: Dict[str, Any]) -> ET.Element:
    """
    Создает элемент организации (юрлицо или ИП)
    """
    org = ET.SubElement(parent, 'organization')
    inn = contact.get('inn', '')
    
    if len(inn) == 10:  # Юридическое лицо
        ogrn_inn_ul = ET.SubElement(org, 'ogrn_inn_UL')
        
        # Проверяем наличие ОГРН
        if contact.get('ogrn'):
            ET.SubElement(ogrn_inn_ul, 'ogrn').text = contact['ogrn']
        else:
            # Иначе используем ИНН/КПП
            inn_kpp = ET.SubElement(ogrn_inn_ul, 'inn_kpp')
            ET.SubElement(inn_kpp, 'inn').text = inn
            # КПП может отсутствовать
            if contact.get('kio'):
                ET.SubElement(inn_kpp, 'kpp').text = contact['kio']
        
        # Наименование организации
        if contact.get('name'):
            ET.SubElement(ogrn_inn_ul, 'UlTitle').text = contact['name']
    
    elif len(inn) == 12:  # ИП
        ogrn_inn_ip = ET.SubElement(org, 'ogrn_inn_IP')
        
        # ОГРН ИП
        if contact.get('ogrn'):
            ET.SubElement(ogrn_inn_ip, 'ogrn').text = contact['ogrn']
        else:
            ET.SubElement(ogrn_inn_ip, 'ogrn').text = '300000000000000'
        
        # ИНН
        ET.SubElement(ogrn_inn_ip, 'inn').text = inn
        
        # ФИО ИП (если есть в данных)
        if contact.get('name'):
            last_name, first_name, middle_name = split_fio(contact['name'])
            if last_name:
                ET.SubElement(ogrn_inn_ip, 'lastName').text = last_name
            if first_name:
                ET.SubElement(ogrn_inn_ip, 'firstName').text = first_name
            if middle_name:
                ET.SubElement(ogrn_inn_ip, 'middleName').text = middle_name
    
    return org

def create_xml_from_trademarks(trademarks: List[Dict[str, Any]], 
                               contacts_info: List[Optional[Dict[str, Any]]]) -> str:
    """
    Создает XML на основе данных о товарных знаках и контактах
    """
    # Создаем корневой элемент
    ns0 = "http://epgu.gosuslugi.ru/elk/status/1.0.2"
    root = ET.Element(f"{{{ns0}}}ElkOrderRequest")
    root.set("env", "EPGU")
    
    # Добавляем пространство имен
    ET.register_namespace('ns0', ns0)
    
    create_orders_request = ET.SubElement(root, f"{{{ns0}}}CreateOrdersRequest")
    orders = ET.SubElement(create_orders_request, f"{{{ns0}}}orders")
    
    for i, (trademark, contact) in enumerate(zip(trademarks, contacts_info)):
        order = ET.SubElement(orders, f"{{{ns0}}}order")
        
        # Данные заявителя
        if contact:
            applicant_type = determine_applicant_type(contact)
            if applicant_type in ['individual', 'ip'] and len(contact.get('inn', '')) != 12:
                create_user_element(order, contact)
            elif applicant_type == 'legal':
                create_organization_element(order, contact)
            else:
                # Для ИП тоже используем organization
                create_organization_element(order, contact)
        else:
            # Если контакт не найден, создаем заглушку
            user = ET.SubElement(order, 'user')
            user_personal_doc = ET.SubElement(user, 'userPersonalDoc')
            ET.SubElement(user_personal_doc, 'PersonalDocType').text = '1'
            ET.SubElement(user_personal_doc, 'number').text = '1234567890'
            ET.SubElement(user_personal_doc, 'lastName').text = 'Иванов'
            ET.SubElement(user_personal_doc, 'firstName').text = 'Иван'
            ET.SubElement(user_personal_doc, 'middleName').text = 'Иванович'
            ET.SubElement(user_personal_doc, 'citizenship').text = '1'
        
        # ИНН отправителя (организации, предоставляющей услугу)
        ET.SubElement(order, f"{{{ns0}}}senderInn").text = '1234567890'
        
        # Код услуги (заглушка)
        ET.SubElement(order, f"{{{ns0}}}serviceTargetCode").text = '12345678901234567890'
        
        # Регион (заглушка)
        ET.SubElement(order, f"{{{ns0}}}userSelectedRegion").text = '45000000'
        
        # Номер заявки - используем rutmk_uid или генерируем
        order_number = trademark.get('rutmk_uid', '')
        if not order_number:
            order_number = f"trademark_{i+1}"
        ET.SubElement(order, f"{{{ns0}}}orderNumber").text = str(order_number)
        
        # Дата запроса - используем текущую дату
        current_date = datetime.now().isoformat()
        ET.SubElement(order, f"{{{ns0}}}requestDate").text = current_date
        
        # Информация об офисе (заглушка)
        office_info = ET.SubElement(order, f"{{{ns0}}}OfficeInfo")
        ET.SubElement(office_info, f"{{{ns0}}}OfficeName").text = 'МФЦ Центрального района'
        ET.SubElement(office_info, f"{{{ns0}}}ApplicationAcceptance").text = '1'
        
        # История статусов (заглушка)
        status_history_list = ET.SubElement(order, f"{{{ns0}}}statusHistoryList")
        status_history = ET.SubElement(status_history_list, f"{{{ns0}}}statusHistory")
        ET.SubElement(status_history, f"{{{ns0}}}status").text = '1'
        ET.SubElement(status_history, f"{{{ns0}}}IsInformed").text = 'False'
        ET.SubElement(status_history, f"{{{ns0}}}statusDate").text = current_date
    
    # Форматируем XML
    xml_str = ET.tostring(root, encoding='utf-8', method='xml')
    
    # Преобразуем в красивый формат
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ", encoding='utf-8')
    
    return pretty_xml.decode('utf-8')

def main(cur, num_records: int = 5):
    """
    Основная функция для формирования XML
    """
    print(f"Получаем последние {num_records} записей из fips_rutrademark...")
    
    # 1. Получаем товарные знаки
    trademarks = get_last_n_trademarks(cur, num_records)
    
    if not trademarks:
        print("Нет данных в таблице fips_rutrademark")
        return None
    
    print(f"Найдено {len(trademarks)} записей")
    
    # 2. Для каждого товарного знака получаем данные заявителя
    contacts_info = []
    for i, tm in enumerate(trademarks):
        rutmk_uid = tm.get('rutmk_uid')
        if rutmk_uid:
            print(f"\nОбработка записи {i+1}: {rutmk_uid}")
            contact = get_applicant_contact(cur, rutmk_uid)
            contacts_info.append(contact)
            
            if contact:
                print(f"  Найден контакт: {contact.get('name', 'Без имени')}")
                if contact.get('inn'):
                    print(f"  ИНН: {contact['inn']}")
            else:
                print("  Контакт не найден")
        else:
            print(f"\nЗапись {i+1}: отсутствует rutmk_uid")
            contacts_info.append(None)
    
    # 3. Формируем XML
    print(f"\nФормируем XML...")
    xml_content = create_xml_from_trademarks(trademarks, contacts_info)
    
    return xml_content

def save_xml_to_file(xml_content: str, filename: str = "output.xml"):
    """
    Сохраняет XML в файл
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"XML сохранен в файл: {filename}")

# Функция для быстрого тестирования
def test_with_sample_data():
    """
    Тестовая функция с примером данных
    """
    # Пример данных товарного знака
    sample_trademark = {
        'rutmk_uid': '123e4567-e89b-12d3-a456-426614174000',
        'application_number': '20231234567',
        'application_date': '2023-12-10'
    }
    
    # Пример данных контакта
    sample_contact = {
        'name': 'Иванов Иван Иванович',
        'inn': '1234567890',
        'ogrn': '1234567890123',
        'passport_number': '1234567890',
        'phone': '+7 (999) 123-45-67',
        'email': 'test@example.com'
    }
    
    xml_content = create_xml_from_trademarks([sample_trademark], [sample_contact])
    return xml_content

# Пример использования
if __name__ == "__main__":
    # Подключение к БД (замените на свои параметры)
    conn = psycopg2.connect(
        host="10.2.53.15",
        port=5432,
        #database="smev_adapter_single",
        database="uad_int",
        user="gegorov",
        password="87zerkaLo22"
    )
    cur = conn.cursor()
    
    try:
        # Получаем XML с 5 записями
        xml_content = main(cur, num_records=5)
        
        if xml_content:
            # Сохраняем в файл
            save_xml_to_file(xml_content, "elk_request.xml")
            
            # Выводим первые 1000 символов для проверки
            print("\nПервые 1000 символов XML:")
            print("-" * 50)
            print(xml_content[:1000])
            if len(xml_content) > 1000:
                print("... (полный XML в файле)")
        
        # Тест с примером данных
        print("\n" + "="*50)
        print("Тест с примером данных:")
        test_xml = test_with_sample_data()
        save_xml_to_file(test_xml, "test_output.xml")
        print("Тестовый XML сохранен в test_output.xml")
        
    finally:
        cur.close()
        conn.close()