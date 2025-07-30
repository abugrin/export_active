import csv
import logging
import os

from dotenv import load_dotenv
from y360_orglib import DirectoryClient
from y360_orglib import configure_logger

log = configure_logger(
    level=logging.DEBUG,
    console=True,
    logger_name="export_enabled_users",
    log_file="export_enabled_users.log"
)

def main():
    """
    Экспортирует только активных пользователей организации в CSV файл.
    Включает только колонки Email и DisplayName.
    """
    token = os.getenv('TOKEN', '')
    org_id = os.getenv('ORG_ID', '')
    client = DirectoryClient(api_key=token, org_id=org_id, ssl_verify=True)
    
    output_file = 'enabled_users.csv'
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, [
            'email',
            'name'
        ])
        w.writeheader()
        
        try:
            users = client.get_all_users()
            enabled_users_count = 0
            
            for org_user in users:
                # Фильтруем только активных пользователей
                if org_user.is_enabled:
                    w.writerow({
                        'email': org_user.email,
                        'name': org_user.name.first + ' ' + org_user.name.last
                    })
                    enabled_users_count += 1
            
            log.info(f"Экспортировано {enabled_users_count} активных пользователей в файл {output_file}")
            
        except Exception as e:
            log.error(f"Ошибка при получении пользователей: {e}")
            raise e


if __name__ == '__main__':
    load_dotenv()
    main()