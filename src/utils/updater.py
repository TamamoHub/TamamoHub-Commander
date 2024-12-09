import requests
from datetime import datetime
import semver
import logging
import json
import os

CURRENT_VERSION = "1.0.0"
GITHUB_REPO = "TamamoHub/TamamoHub-Commander"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}"
RELEASES_URL = f"{GITHUB_API_URL}/releases"

def get_local_version():
    """Отримати локальну версію з файлу version.json"""
    try:
        version_file = os.path.join(os.path.dirname(__file__), '..', '..', 'version.json')
        if os.path.exists(version_file):
            with open(version_file, 'r') as f:
                data = json.load(f)
                return data.get('version', CURRENT_VERSION)
    except Exception as e:
        logging.error(f"Помилка читання версії: {e}")
    return CURRENT_VERSION

def check_updates():
    """Перевірка наявності оновлень"""
    current_version = get_local_version()
    
    try:
        response = requests.get(
            RELEASES_URL,
            headers={
                'Accept': 'application/vnd.github.v3+json'
            },
            timeout=10
        )
        response.raise_for_status()
        
        releases = response.json()
        if not releases:
            return {
                'current_version': current_version,
                'latest_version': current_version,
                'has_updates': False,
                'release_notes': 'Немає доступних релізів',
                'release_date': datetime.now().strftime('%d.%m.%Y'),
                'update_available': False,
                'release_url': ''
            }
            
        latest_release = releases[0]
        latest_version = latest_release['tag_name'].lstrip('v')
        has_updates = semver.compare(latest_version, current_version) > 0
        
        return {
            'current_version': current_version,
            'latest_version': latest_version,
            'has_updates': has_updates,
            'release_notes': latest_release.get('body', ''),
            'release_date': datetime.strptime(
                latest_release['published_at'],
                '%Y-%m-%dT%H:%M:%SZ'
            ).strftime('%d.%m.%Y'),
            'is_prerelease': latest_release.get('prerelease', False),
            'update_available': False,  # Оновлення поки недоступне
            'message': 'Функція автоматичного оновлення в розробці',
            'release_url': latest_release.get('html_url', '')  # URL релізу на GitHub
        }
        
    except Exception as e:
        logging.error(f"Помилка перевірки оновлень: {str(e)}")
        return {
            'current_version': current_version,
            'latest_version': current_version,
            'has_updates': False,
            'release_notes': 'Помилка перевірки оновлень',
            'release_date': datetime.now().strftime('%d.%m.%Y'),
            'update_available': False,
            'message': 'Помилка перевірки оновлень',
            'release_url': ''
        } 

def update_app(version=None):
    """Оновити програму до останньої версії"""
    try:
        # Перевіряємо наявність оновлень
        update_info = check_updates()
        
        if not update_info['has_updates'] and not version:
            return {
                'success': False,
                'message': 'Немає доступних оновлень'
            }
        
        return {
            'success': True,
            'message': 'Будь ласка, завантажте нову версію за посиланням',
            'download_url': update_info['release_url']
        }
        
    except Exception as e:
        logging.error(f"Помилка процесу оновлення: {e}")
        return {
            'success': False,
            'message': f"Помилка оновлення: {str(e)}"
        } 