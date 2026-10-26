#!/usr/bin/env python3
"""Read-only verification of public release bytes. Never infers Google indexing."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

def fetch(job):
    url, expected = job
    row = {'url':url,'expected_sha256':expected}
    try:
        with urlopen(Request(url,headers={'User-Agent':'IMPERIAL-Public-Verification/1.0'}),timeout=20) as response:
            body=response.read()
            row.update(http_status=response.status,final_url=response.url,
                       actual_sha256=hashlib.sha256(body).hexdigest(),
                       x_robots_tag=response.headers.get('X-Robots-Tag',''))
            row['matches']=response.status==200 and row['actual_sha256']==expected
    except HTTPError as exc: row.update(http_status=exc.code,matches=False)
    except Exception as exc: row.update(http_status=None,error=str(exc),matches=False)
    return row

def main():
    jobs=[]; bases=[]
    for kind in ['founder','ecosystem']:
        manifest=json.loads((ROOT/kind/'publication-manifest.json').read_text())
        base=manifest['canonical_origin'];bases.append(base)
        for record in manifest['files']:
            if record['path'] in ['.nojekyll','404.html']: continue
            path=record['path']
            if path.endswith('index.html'):path=path[:-10]
            jobs.append((base+'/'+path,record['sha256']))
    with ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(fetch,jobs))
    robots=[]
    for origin in sorted({urlsplit(b).scheme+'://'+urlsplit(b).netloc for b in bases}):
        row={'url':origin+'/robots.txt','permits_googlebot':None}
        try:
            with urlopen(Request(row['url'],headers={'User-Agent':'IMPERIAL-Public-Verification/1.0'}),timeout=20) as response:
                body=response.read().decode();rp=RobotFileParser();rp.parse(body.splitlines())
                row.update(http_status=response.status,permits_googlebot=all(rp.can_fetch('Googlebot',b+'/') for b in bases))
        except HTTPError as exc:
            row['http_status']=exc.code
            if exc.code==404:row['permits_googlebot']=True
        except Exception as exc:row['error']=str(exc)
        robots.append(row)
    published=all(row['matches'] for row in rows)
    crawlable=published and all(r['permits_googlebot'] is True for r in robots) and all('noindex' not in r.get('x_robots_tag','').lower() for r in rows)
    result={'observed_at':datetime.now(timezone.utc).isoformat(),'published_bytes_verified':published,'crawlable':crawlable,'google_indexed':'NOT_VERIFIED','files':rows,'root_robots':robots}
    destination=ROOT/'evidence/live-verification.json'
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['files','root_robots']},indent=2))
    return 0 if crawlable else 1

if __name__=='__main__':sys.exit(main())
