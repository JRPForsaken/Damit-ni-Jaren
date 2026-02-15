# Fix the corrupted tree structure by replacing the double-encoded UTF-8
with open('README.md', 'rb') as f:
    content = f.read()

# The corrupted sequences - UTF-8 for the garbled characters we're seeing
corrupted_patterns = [
    (b'\xc3\xa2\xe2\x80\x9d\xc5\x93\xc3\xa2\xe2\x80\x9d\xe2\x82\xac\xc3\xa2\xe2\x80\x9d\xe2\x82\xac', b'├──'),  
    (b'\xc3\xa2\xe2\x80\x9d\xe2\x80\x9a   \xc3\xa2\xe2\x80\x9d\xc5\x93\xc3\xa2\xe2\x80\x9d\xe2\x82\xac', b'│   ├──'),  
    (b'\xc3\xa2\xe2\x80\x9d\xe2\x80\x9a   \xc3\xa2\xe2\x80\x9d\xe2\x80\x9c\xc3\xa2\xe2\x80\x9d\xe2\x82\xac', b'│   └──'),  
    (b'\xc3\xa2\xe2\x80\x9d\xe2\x80\x9a', b'│'),  
    (b'\xc3\xa2\xe2\x80\x9d\xe2\x80\x9c\xc3\xa2\xe2\x80\x9d\xe2\x82\xac', b'└──'),  
]

# Apply replacements
for corrupted, clean in corrupted_patterns:
    content = content.replace(corrupted, clean)

with open('README.md', 'wb') as f:
    f.write(content)

print('✅ Fixed corrupted tree structure in README.md')
