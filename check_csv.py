import csv
import re

def check_csv_format():
    with open('dh.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(f'Number of columns in header: {len(header)}')
        print('Header columns:', header)
        
        print('\nChecking row lengths...')
        for i, row in enumerate(reader, 2):
            if len(row) != len(header):
                print(f'Row {i}: {len(row)} columns (should be {len(header)})')
        
        # Reset file pointer
        f.seek(0)
        next(reader)  # Skip header
        
        # Check for empty fields and special characters
        print('\nChecking for empty fields and special characters in first few rows...')
        for i, row in enumerate(reader, 2):
            if i > 5:  # Only check first 5 rows
                break
            print(f'\nRow {i}:')
            for col, val in zip(header, row):
                if not val.strip():
                    print(f'  Empty field in column: {col}')
                # Check for unescaped quotes
                if '"' in val and not val.startswith('"') and not val.endswith('"'):
                    print(f'  Unescaped quote in column: {col}')
                # Check for newlines
                if '\n' in val:
                    print(f'  Newline character in column: {col}')
                # Check for other special characters
                if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', val):
                    print(f'  Control character in column: {col}')

if __name__ == '__main__':
    check_csv_format() 