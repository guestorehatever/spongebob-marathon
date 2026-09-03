#!/usr/bin/env python3
"""Build /home/user/src -> /home/user/site (self-contained pages).

NOTE: this lives in tools/, NOT build/ -- a directory named "build" is
excluded from workspace snapshots and gets wiped between turns.
"""
import base64, json, os, re, sys

ROOT = '/home/user'
SRC  = os.path.join(ROOT, 'src')
OUT  = os.path.join(ROOT, 'site')
TOOLS= os.path.join(ROOT, 'tools')

PAGES = ['index.html', 'trivia.html', 'bingo.html', 'games.html',
         'quiz.html', 'episodes.html', 'watch.html', 'offline.html']

CHARS = ['spongebob', 'patrick', 'squidward', 'krabs',
         'sandy', 'plankton', 'gary', 'mrspuff', 'sad']


def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {'.png': 'image/png', '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg', '.webp': 'image/webp'}[ext]
    with open(path, 'rb') as f:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(f.read()).decode())


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


NAV  = read(os.path.join(TOOLS, '_nav.html'))
FOOT = read(os.path.join(TOOLS, '_foot.html'))

fonts  = read(os.path.join(TOOLS, 'fonts.css'))
style  = read(os.path.join(SRC, 'css', 'style.css'))
common = read(os.path.join(SRC, 'js', 'common.js'))

HLS = read(os.path.join(TOOLS, 'hls.min.js'))

EPS = json.load(open(os.path.join(TOOLS, 'episodes.json')))
EPS_JS = json.dumps(EPS, separators=(',', ':'))

assets = {'{{HERO}}': data_uri(os.path.join(OUT, 'assets', 'hero_opt.jpg')),
          '{{LOGO}}': data_uri(os.path.join(OUT, 'assets', 'logo_opt.png'))}
for c in CHARS:
    assets['{{%s}}' % c] = data_uri(os.path.join(OUT, 'assets', 'chars', c + '.png'))


def build(page):
    html = read(os.path.join(SRC, page))

    # nav / footer
    html = html.replace('<!--NAV-->', NAV).replace('<!--FOOT-->', FOOT)

    # inline css: fonts first, then the stylesheet
    html = html.replace(
        '<link rel="stylesheet" href="css/style.css">',
        '<style>%s\n%s</style>' % (fonts, style))

    # inline shared js
    html = html.replace('<script src="js/common.js"></script>',
                        '<script>%s</script>' % common)

    # hls.js (watch page only)
    html = html.replace('<!--HLS-->', '<script>%s</script>' % HLS)

    # episode data
    html = html.replace('/*EPISODES*/[]', EPS_JS)

    # images
    for k, v in assets.items():
        html = html.replace(k, v)

    # mark the current page in the nav
    html = re.sub(r'<a href="%s">' % re.escape(page), '<a class="on" href="%s">' % page, html, count=1)
    html = re.sub(r'<a class="([^"]*)" href="%s">' % re.escape(page),
                  lambda m: '<a class="%s on" href="%s">' % (m.group(1), page), html, count=1)

    leftover = re.findall(r'\{\{[a-zA-Z_]+\}\}', html)
    assert not leftover, '%s: unresolved tokens %s' % (page, set(leftover))
    assert '<!--NAV-->' not in html and '<!--FOOT-->' not in html, page
    return html


def main():
    os.makedirs(OUT, exist_ok=True)
    # remove built pages that no longer have a source
    for f in os.listdir(OUT):
        if f.endswith('.html') and f not in PAGES:
            os.remove(os.path.join(OUT, f))
            print('  removed stale %s' % f)
    for page in PAGES:
        html = build(page)
        with open(os.path.join(OUT, page), 'w', encoding='utf-8') as f:
            f.write(html)
        print('%-18s %4d KB' % (page, len(html.encode()) // 1024))


if __name__ == '__main__':
    main()
