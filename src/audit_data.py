from pathlib import Path

import pandas as pd

from src.config import RAW_DIR, REFERENCES_DIR


def file_size(path):
    size=path.stat().st_size
    for unit in ('B','KB','MB','GB'):
        if size < 1024:
            return f'{size:.1f} {unit}'
        size/=1024
    return f'{size:.1f} TB'


def list_files(root):
    rows=[]
    for path in sorted(root.rglob('*')):
        if path.is_file() and path.name != '.gitkeep':
            rows.append({
                'file_name':path.name,
                'path':str(path),
                'size':file_size(path),
                'suffix':path.suffix.lower()
            })
    return pd.DataFrame(rows)


def main():
    raw_files=list_files(RAW_DIR)
    doc_files=list_files(REFERENCES_DIR / 'raw_docs')

    print('\nraw data files')
    print(raw_files.to_string(index=False) if len(raw_files) else 'No raw data files found.')

    print('\nraw documentation files')
    print(doc_files.to_string(index=False) if len(doc_files) else 'No raw documentation files found.')


if __name__ == '__main__':
    main()