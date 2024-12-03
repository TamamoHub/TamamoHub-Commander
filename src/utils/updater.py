import requests
from datetime import datetime
import semver

CURRENT_VERSION = "1.0.0"
GITHUB_REPO = "TamamoHub/TamamoHub-Commander"

def check_updates():
    try:
        response = requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest")
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release['tag_name'].lstrip('v')
            
            has_updates = semver.compare(latest_version, CURRENT_VERSION) > 0
            
            return {
                'current_version': CURRENT_VERSION,
                'latest_version': latest_version,
                'has_updates': has_updates,
                'release_notes': latest_release['body'],
                'release_date': datetime.strptime(
                    latest_release['published_at'], 
                    '%Y-%m-%dT%H:%M:%SZ'
                ).strftime('%d.%m.%Y')
            }
    except Exception as e:
        print(f"Помилка перевірки оновлень: {e}")
    
    return {
        'current_version': CURRENT_VERSION,
        'latest_version': CURRENT_VERSION,
        'has_updates': False,
        'release_notes': '',
        'release_date': datetime.now().strftime('%d.%m.%Y')
    } 