import psycopg2
from tabulate import tabulate

def explore_relevant_tables(cur):
    """
    Исследует только релевантные таблицы для работы с ЕЛК
    """
    # Таблицы, которые с наибольшей вероятностью содержат нужные данные
    priority_tables = [
        'Requests', 'Movement', 'Comments', 'Parameters',
        'fips_contact', 'fips_correspondenceaddress',
        'fips_wktmkuser', 'fips_rutmkuser', 'fips_madridtmkuser',
        'DraftFiles', 'Storage', 'Links', 'Package',
        'review_history', 'UnifiedStatus'
    ]
    
    # Также проверяем все таблицы с префиксом fips_, которые могут содержать данные заявителей
    fips_tables = [
        'fips_ruapluser', 'fips_ruaplcertuser', 'fips_rutmkapplicant',
        'fips_wktmkapplicant', 'fips_madridtmkapplicant',
        'fips_softapplicant', 'fips_dbapplicant', 'fips_ictapplicant'
    ]
    
    all_tables = priority_tables + fips_tables
    
    results = []
    
    print("Исследование таблиц для формирования XML ЕЛК\n")
    print("=" * 100)
    
    for table in all_tables:
        try:
            # Проверяем существование таблицы
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                )
            """, (table,))
            
            exists = cur.fetchone()[0]
            
            if not exists:
                results.append([table, "❌ Таблица не существует", "", "", ""])
                continue
            
            # Получаем информацию о колонках
            cur.execute("""
                SELECT 
                    column_name,
                    data_type,
                    character_maximum_length,
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, (table,))
            
            columns = cur.fetchall()
            
            # Получаем количество записей
            cur.execute(f'SELECT COUNT(*) FROM "{table}"')
            count = cur.fetchone()[0]
            
            # Ищем ключевые колонки, которые могут быть полезны для ЕЛК
            key_columns = {
                'id_columns': [],
                'date_columns': [],
                'status_columns': [],
                'person_columns': [],
                'document_columns': []
            }
            
            for col_name, data_type, max_len, nullable, default in columns:
                col_name_lower = col_name.lower()
                
                # Идентификаторы
                if any(keyword in col_name_lower for keyword in ['id', 'uuid', 'guid']):
                    key_columns['id_columns'].append(col_name)
                
                # Даты и время
                if any(keyword in col_name_lower for keyword in 
                       ['date', 'time', 'created', 'updated', 'modified', 'timestamp']):
                    key_columns['date_columns'].append(col_name)
                
                # Статусы
                if any(keyword in col_name_lower for keyword in 
                       ['status', 'state', 'stage']):
                    key_columns['status_columns'].append(col_name)
                
                # Данные персон
                if any(keyword in col_name_lower for keyword in 
                       ['name', 'lastname', 'firstname', 'middlename', 
                        'inn', 'snils', 'ogrn', 'kpp', 'phone', 'email']):
                    key_columns['person_columns'].append(col_name)
                
                # Документы и номера
                if any(keyword in col_name_lower for keyword in 
                       ['number', 'num', 'doc', 'trademark', 'application']):
                    key_columns['document_columns'].append(col_name)
            
            # Получаем пример данных (первые 2 строки)
            cur.execute(f'SELECT * FROM "{table}" LIMIT 2')
            sample_rows = cur.fetchall()
            
            # Формируем описание
            column_summary = []
            for col in columns[:5]:  # Показываем первые 5 колонок
                col_desc = f"{col[0]} ({col[1]})"
                if col[2]:
                    col_desc += f"[{col[2]}]"
                column_summary.append(col_desc)
            
            column_info = "\n".join(column_summary)
            if len(columns) > 5:
                column_info += f"\n... и еще {len(columns) - 5} колонок"
            
            # Ключевые колонки для вывода
            key_info = []
            if key_columns['id_columns']:
                key_info.append(f"ID: {', '.join(key_columns['id_columns'][:2])}")
            if key_columns['date_columns']:
                key_info.append(f"Даты: {', '.join(key_columns['date_columns'][:2])}")
            if key_columns['status_columns']:
                key_info.append(f"Статусы: {', '.join(key_columns['status_columns'][:2])}")
            if key_columns['person_columns']:
                key_info.append(f"Персоны: {', '.join(key_columns['person_columns'][:3])}")
            if key_columns['document_columns']:
                key_info.append(f"Документы: {', '.join(key_columns['document_columns'][:2])}")
            
            key_info_str = "\n".join(key_info) if key_info else "Нет ключевых колонок"
            
            results.append([
                table,
                f"✓ {len(columns)} колонок",
                f"📊 {count} записей",
                column_info,
                key_info_str
            ])
            
        except Exception as e:
            results.append([table, f"❌ Ошибка: {str(e)[:50]}...", "", "", ""])
    
    # Выводим результаты в виде таблицы
    headers = ["Таблица", "Статус", "Записей", "Колонки (первые 5)", "Ключевые поля"]
    print(tabulate(results, headers=headers, tablefmt="grid", maxcolwidths=[20, 15, 10, 30, 30]))
    
    # Дополнительная информация о наиболее вероятных таблицах
    print("\n" + "=" * 100)
    print("РЕКОМЕНДАЦИИ ПО ТАБЛИЦАМ:")
    print("\n1. ОСНОВНЫЕ ТАБЛИЦЫ (вероятно содержат данные заявок):")
    
    for table in ['Requests', 'Movement', 'Comments', 'Parameters']:
        if any(table in row[0] for row in results if "✓" in row[1]):
            print(f"   • {table} - исследуйте первым делом")
    
    print("\n2. ТАБЛИЦЫ С ДАННЫМИ ЗАЯВИТЕЛЕЙ:")
    person_tables = [row[0] for row in results if "Персоны:" in row[4] and "fips_" in row[0]]
    for table in person_tables[:5]:  # Показываем первые 5
        print(f"   • {table}")
    
    print("\n3. СЛЕДУЮЩИЕ ШАГИ:")
    print("   • Проверьте таблицу 'Requests' - скорее всего, это основная таблица заявок")
    print("   • Найдите связь между 'Requests' и таблицами с данными заявителей")
    print("   • Ищите поля с номерами заявок (orderNumber в XML)")
    print("   • Ищите поля со статусами и датами их изменения")
    
    return results

def get_table_details(cur, table_name):
    """
    Получает детальную информацию о конкретной таблице
    """
    try:
        print(f"\n{'='*60}")
        print(f"ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О ТАБЛИЦЕ: {table_name}")
        print('='*60)
        
        # Полная информация о колонках
        cur.execute("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        
        columns = cur.fetchall()
        
        print("\nСтруктура таблицы:")
        print("-" * 80)
        col_data = []
        for col_name, data_type, max_len, nullable, default in columns:
            col_info = f"  {col_name:<30} {data_type:<20}"
            if max_len:
                col_info += f" [{max_len}]"
            col_info += f" {'NULL' if nullable == 'YES' else 'NOT NULL'}"
            if default:
                col_info += f" DEFAULT: {default}"
            col_data.append(col_info)
        
        print("\n".join(col_data))
        
        # Примеры данных
        print(f"\nПримеры данных (первые 3 записи):")
        print("-" * 80)
        
        cur.execute(f'SELECT * FROM "{table_name}" LIMIT 3')
        sample_data = cur.fetchall()
        
        if sample_data:
            # Получаем названия колонок
            cur.execute(f'SELECT * FROM "{table_name}" LIMIT 0')
            col_names = [desc[0] for desc in cur.description]
            
            for i, row in enumerate(sample_data, 1):
                print(f"\nЗапись #{i}:")
                for col_name, value in zip(col_names, row):
                    if value is not None:
                        print(f"  {col_name}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
                    else:
                        print(f"  {col_name}: NULL")
        else:
            print("Таблица пустая")
        
        # Связи с другими таблицами (по внешним ключам)
        print(f"\nВозможные связи с другими таблицами:")
        print("-" * 80)
        
        cur.execute("""
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM 
                information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
            WHERE 
                tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_name = %s
        """, (table_name,))
        
        foreign_keys = cur.fetchall()
        
        if foreign_keys:
            for fk in foreign_keys:
                print(f"  {fk[1]} -> {fk[2]}.{fk[3]}")
        else:
            print("  Внешние ключи не найдены")
        
    except Exception as e:
        print(f"Ошибка при получении информации о таблице {table_name}: {e}")

# Основная функция
def main(cur):
    """
    Основная функция для исследования таблиц
    """
    print("=" * 100)
    print("СКРИПТ ДЛЯ ИССЛЕДОВАНИЯ ТАБЛИЦ ДЛЯ ФОРМИРОВАНИЯ XML ЕЛК")
    print("=" * 100)
    
    # Шаг 1: Обзор релевантных таблиц
    results = explore_relevant_tables(cur)
    
    # Шаг 2: Детальное исследование ключевых таблиц
    key_tables_to_inspect = ['Requests', 'Movement', 'fips_contact']
    
    for table in key_tables_to_inspect:
        # Проверяем, что таблица существует в результатах
        if any(table in row[0] for row in results if "✓" in row[1]):
            get_table_details(cur, table)
    
    print("\n" + "=" * 100)
    print("СОВЕТЫ ДЛЯ ДАЛЬНЕЙШЕЙ РАБОТЫ:")
    print("1. В таблице 'Requests' ищите поля:")
    print("   - Номер заявки (возможно order_number, external_id)")
    print("   - Дата создания (created_date, request_date)")
    print("   - Статус (status_id, state)")
    print("   - ID заявителя (user_id, applicant_id)")
    print("   - Тип услуги (service_type, service_code)")
    
    print("\n2. Для получения данных заявителя:")
    print("   - Найдите связь Requests -> fips_* таблицы")
    print("   - Ищите ФИО, ИНН, СНИЛС, паспортные данные")
    
    print("\n3. Для истории статусов:")
    print("   - Проверьте таблицу 'Movement' или 'review_history'")
    print("   - Ищите даты изменения статусов, коды статусов")


if __name__ == "__main__":
    conn = psycopg2.connect(
        host="10.2.53.15",
        port=5432,
        #database="smev_adapter_single",
        database="uad_int",
        user="gegorov",
        password="87zerkaLo22"
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
    """)
    tables = cur.fetchall()
    print(tables)

    main(cur)

    cur.close()
    conn.close()

