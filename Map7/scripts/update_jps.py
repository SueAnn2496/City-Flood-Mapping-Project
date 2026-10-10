"""Read the same public station table used by JPS Public Infobanjir.
No credentials, mock readings, or guessed coordinates are used.
"""
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

URL = 'https://publicinfobanjir.water.gov.my/wp-content/themes/shapely/agency/searchresultrainfall.php?state=SEL&district=ALL&station=ALL&loginStatus=0&language=en'
OUTPUT = Path(__file__).resolve().parents[1] / 'data/jps-selangor.json'

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    stations = []
    # JPS currently emits malformed tr tags; group cells by its No attribute.
    for table in soup.select('table.normaltable'):
        cells = table.select('tbody td')
        groups = []
        for cell in cells:
            if cell.get('data-th') == 'No':
                groups.append([])
            if groups:
                groups[-1].append(cell)
        for group in groups:
            if len(group) != 13 or group[1].get('data-th') != 'Station ID' or 'info' not in group[-1].get('class', []):
                raise ValueError('JPS table layout changed; refusing to guess rainfall column')
            values = [c.get_text(' ', strip=True) for c in group]
            if values[3] not in ('Petaling', 'Klang'):
                continue
            observed = datetime.strptime(values[4], '%d/%m/%Y %H:%M:%S').replace(tzinfo=timezone(timedelta(hours=8)))
            raw = values[-1]
            mm = float(raw) if re.fullmatch(r'\d+(?:\.\d+)?', raw) else None
            stations.append(dict(id=values[1], name=values[2], district=values[3], lastUpdated=observed.isoformat(), oneHourMm=mm))
    if not stations or not all(any(s['district'] == d for s in stations) for d in ('Petaling', 'Klang')):
        raise ValueError('No usable Petaling/Klang station table returned by JPS')
    return stations

def main():
    failed = False
    try:
        if len(sys.argv) > 1:
            html = Path(sys.argv[1]).read_text()
        else:
            with urlopen(Request(URL, headers={'User-Agent': 'Map7-Rainfall-Monitor/1.0'}), timeout=60) as response:
                html = response.read().decode('utf-8', errors='replace')
        data = dict(schemaVersion=1, ok=True, fetchedAt=datetime.now(timezone.utc).isoformat(), sourceUrl=URL, stations=parse(html))
    except Exception as error:
        failed = True
        # Replace old readings with an explicit failure, never mark them fresh.
        data = dict(schemaVersion=1, ok=False, fetchedAt=datetime.now(timezone.utc).isoformat(), sourceUrl=URL, error=str(error), stations=[])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print('JPS stations:', len(data['stations']), '| ok:', data['ok'])
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())

