from datetime import datetime, timedelta
from lib.annex import Annex

annex = Annex()
old_timestamp = datetime.now() - timedelta(days=90)
for filename in annex.find('--metadata', 'in_webdrasil=1').split('\n'):
    try:
        metadata = annex.get_metadata(filename)
    except ValueError:
        continue
    current_timestamp = datetime.strptime(metadata['in_webdrasil-lastchanged'][0], '%Y-%m-%d@%H-%M-%S')
    if old_timestamp > current_timestamp:
        annex.remove_metadata(filename, 'in_webdrasil', metadata['in_webdrasil'][0])
        annex.drop(filename)
