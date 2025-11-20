from pathlib import Path
import re
path = Path('app.py')
text = path.read_text(encoding='utf-8')
with open('pub_block.txt','r',encoding='utf-8') as f:
    block = f.read()
with open('pub_helpers.txt','r',encoding='utf-8') as f:
    helpers = f.read()
pattern = r'def render_publications_tab\(\).*?def render_benchmark_the_qs_tab'
m = re.search(pattern, text, flags=re.S)
if not m:
    raise SystemExit('pattern not found')
replacement = helpers + '\n' + block + '\n\n' + 'def render_benchmark_the_qs_tab'
text = text[:m.start()] + replacement + text[m.end():]
path.write_text(text, encoding='utf-8')
