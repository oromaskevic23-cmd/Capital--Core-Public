#!/usr/bin/env python3
"""Offline checks for the sprint's public documentation. No network or credentials."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SECTIONS = (
    'Founder introduction', 'IMPERIAL Core — ecosystem overview',
    'Flagship engineering projects', 'Architecture & technology stack',
    'Zero Trust, AI Governance & Verified Engineering', 'Public technical evidence',
    'Engineering roadmap', 'Collaboration and business inquiries', 'Authorship — RomaskevicH',
)

def main():
    errors = []
    files = json.loads((ROOT/'public-document-manifest.json').read_text())['files']
    for relative in files:
        path = (ROOT/relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            errors.append(f'Missing/unsafe path: {relative}')
            continue
        text = path.read_text(encoding='utf-8')
        if not text.endswith('\n') or '\r' in text:
            errors.append(f'Line endings: {relative}')
        if re.search(r'(?m)^\s*(```|~~~)', text):
            for fence in ('```', '~~~'):
                if sum(line.lstrip().startswith(fence) for line in text.splitlines()) % 2:
                    errors.append(f'Unbalanced fence: {relative}')
        if re.search(r'(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)', text):
            errors.append(f'Possible credential material: {relative}')
        if path.suffix == '.md':
            for match in re.finditer(r'\]\(([^)]*)\)',text):
                url=match.group(1).strip()
                if not url:
                    errors.append(f'Empty Markdown target: {relative}')
                    continue
                parts=urlsplit(url)
                if parts.scheme:
                    if parts.scheme!='https': errors.append(f'Non-HTTPS public link: {relative}')
                    continue
                if parts.netloc: errors.append(f'Protocol-relative link: {relative}')
                if parts.path:
                    target=(path.parent/unquote(parts.path)).resolve()
                    if not target.is_relative_to(ROOT) or not target.exists():
                        errors.append(f'Broken/unsafe local link: {relative}: {url}')
    profile=(ROOT/'profile/README.md').read_text()
    for heading in REQUIRED_SECTIONS:
        if '\n## '+heading+'\n' not in profile: errors.append('Missing profile section: '+heading)
    if 'Chief Systems Architect' in profile: errors.append('Outdated founder role')
    evidence=json.loads((ROOT/'evidence/milestones.json').read_text())
    for item in evidence['milestones']:
        if not re.fullmatch(r'[0-9a-f]{40}',item['commit']): errors.append('Invalid commit')
        counts=item['tests']
        if counts['tests'] != counts['pass'] or any(counts[k] for k in ('fail','skipped','cancelled','todo')):
            errors.append('Inconsistent successful test summary')
        if item['conclusion']!='success' or item['visibility']!='public': errors.append('Unsupported evidence classification')
        for key in ('commit_url','pull_request','run_url','job_url'):
            if not item[key].startswith(item['repository']+'/'): errors.append('Evidence repository mismatch')
    if errors:
        print('\n'.join('FAIL: '+error for error in errors))
        return 1
    print(f'PASS: {len(files)} declared files; local links, nine profile sections, scoped credential patterns and evidence-record consistency')
    print('LIMIT: offline checks do not verify remote links, runtime behavior, deployment or full secret history.')
    return 0

if __name__=='__main__':
    sys.exit(main())
