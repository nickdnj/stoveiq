import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "firmware" / "src" / "web_server.c"
src = SRC.read_text(encoding='utf-8')

start = src.index('static const char FALLBACK_HTML[] =')
# find terminating ";" at the end of the literal chain
end = src.index('</html>\\n";', start) + len('</html>\\n";')
blob = src[start:end]
blob = blob[blob.index('=')+1:]

# strip C comments
blob = re.sub(r'/\*.*?\*/', '', blob, flags=re.S)

# pull every double-quoted C string literal
lits = re.findall(r'"((?:[^"\\]|\\.)*)"', blob)

def unescape(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            n = s[i+1]
            mapping = {'n':'\n','t':'\t','r':'\r','"':'"','\\':'\\',"'":"'",'0':'\0'}
            if n in mapping:
                out.append(mapping[n]); i += 2; continue
            if n == 'x':
                m = re.match(r'\\x([0-9a-fA-F]{1,2})', s[i:])
                if m:
                    out.append(chr(int(m.group(1),16))); i += m.end(); continue
            out.append(n); i += 2; continue
        out.append(c); i += 1
    return ''.join(out)

html = ''.join(unescape(l) for l in lits)
OUT = Path(__file__).parent / 'index.html'
OUT.write_text(html, encoding='utf-8')
print(f"extracted {len(lits)} string literals -> {OUT} ({len(html)} bytes)")
