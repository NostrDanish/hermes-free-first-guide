#!/usr/bin/env python3
"""Build the complete Markdown handbook and a linked, text-selectable PDF."""
from pathlib import Path
import html
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]


def sections(text):
    pieces = re.split(r'(?m)(?=^## \d+\.)', text)
    return {int(re.match(r'## (\d+)\.', piece).group(1)): piece.strip()
            for piece in pieces if re.match(r'## \d+\.', piece)}


def compose():
    core = sections((ROOT / 'docs/GUIDE-CORE.md').read_text())
    providers = sections((ROOT / 'docs/PROVIDER-CHAPTERS.md').read_text())
    combined = {0: (ROOT / 'docs/HERMES-BASICS.md').read_text().strip(), **providers}
    numbering = {1: 1, 2: 2, 3: 4, 4: 9, 5: 10, 6: 11, 7: 12, 8: 13, 9: 14, 10: 15, 11: 16, 12: 17}
    for old, new in numbering.items():
        combined[new] = re.sub(r'^## \d+\.', f'## {new}.', core[old], count=1)
    assert sorted(combined) == list(range(18))
    titles = [combined[n].splitlines()[0][3:] for n in sorted(combined)]
    front = '''# Hermes: The Complete Free-API Handbook

**Set up Hermes, connect Nous Portal Free and OpenRouter, combine legitimate allowances through FreeLLMAPI, add optional local models, and keep paid use explicit.**

Independent practical setup handbook. Sources/catalogs checked **20 October 2026**. This covers the provider families actually configured in the author's stack plus additional eligible upstreams—not just OpenRouter. Catalogs, pricing, account eligibility, and tool APIs can change. No secret/account database is included and no unlimited-free guarantee is made.

**Access labels matter:** zero-priced route ≠ recurring allowance ≠ trial credits ≠ earned credits ≠ subscription-included usage ≠ discounted paid inference. Each provider chapter identifies the difference.

The PDF has clickable links and selectable text. Use the Markdown version for exact copy/paste commands. Illustrated cards are a quick-start overview; this handbook contains the full setup details.

## Contents

'''
    text = front + '\n'.join('- ' + title for title in titles) + '\n\n---\n\n'
    text += '\n\n'.join(combined[n] for n in sorted(combined)) + '\n'
    text = text.replace('section 10', 'the verification chapter')
    text = text.replace('all 31 unique shared links returned HTTP 200 during the check.',
                        'the original edition’s 31 source links returned HTTP 200. Expanded-edition link checks are recorded in the repository verification notes.')
    text = text.replace('The minimum useful setup is Hermes + one OpenRouter key + a verified free model + free-only fallbacks + explicit paid permission.',
                        'The minimum useful setup is Hermes + one eligible Nous/OpenRouter free route + free-only fallbacks + explicit paid permission.')
    return text


def inline(text):
    # shortcut: handles this handbook's links/bold/code, not arbitrary Markdown HTML.
    pattern = r'(\[[^\]]+\]\(https?://[^)]+\)|<https?://[^>]+>|`[^`]+`|\*\*[^*]+\*\*)'
    result = []
    for token in re.split(pattern, text):
        if token.startswith('[') and '](' in token:
            label, url = token[1:].split('](', 1)
            result.append('<link href="' + html.escape(url[:-1], quote=True) + '" color="#145749">' + html.escape(label) + '</link>')
        elif token.startswith('<http'):
            url = token[1:-1]
            result.append('<link href="' + html.escape(url, quote=True) + '" color="#145749">' + html.escape(url) + '</link>')
        elif token.startswith('`'):
            result.append('<font name="HandbookMono">' + html.escape(token[1:-1]) + '</font>')
        elif token.startswith('**'):
            result.append('<b>' + html.escape(token[2:-2]) + '</b>')
        else:
            result.append(html.escape(token))
    return ''.join(result)


def render_pdf(text, destination):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    fonts = {'Handbook': '/usr/share/fonts/liberation/LiberationSans-Regular.ttf',
             'HandbookBold': '/usr/share/fonts/liberation/LiberationSans-Bold.ttf',
             'HandbookMono': '/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf'}
    for name, path in fonts.items():
        pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily('Handbook', normal='Handbook', bold='HandbookBold', italic='Handbook', boldItalic='HandbookBold')
    styles = getSampleStyleSheet()
    body = ParagraphStyle('Body', fontName='Handbook', fontSize=10.7, leading=15.2,
                          textColor=colors.HexColor('#18322e'), spaceAfter=8, splitLongWords=True)
    title = ParagraphStyle('Title', parent=body, fontName='HandbookBold', fontSize=28, leading=33, spaceAfter=20)
    h1 = ParagraphStyle('Section', parent=body, fontName='HandbookBold', fontSize=20, leading=25, spaceBefore=18, spaceAfter=12, keepWithNext=True)
    h2 = ParagraphStyle('Subsection', parent=body, fontName='HandbookBold', fontSize=14, leading=18, spaceBefore=13, spaceAfter=8, keepWithNext=True)
    h3 = ParagraphStyle('SmallHeading', parent=h2, fontSize=12, leading=15)
    code = ParagraphStyle('Code', fontName='HandbookMono', fontSize=7.9, leading=10.8,
                          backColor=colors.HexColor('#edf1e8'), borderPadding=9, spaceBefore=5, spaceAfter=12)
    cell = ParagraphStyle('Cell', parent=body, fontSize=8.6, leading=12, spaceAfter=0)
    story = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith('```'):
            block = []; index += 1
            while index < len(lines) and not lines[index].startswith('```'):
                raw = lines[index]
                block.extend(textwrap.wrap(raw, width=98, replace_whitespace=False,
                                            drop_whitespace=False, subsequent_indent='    ') or [''])
                index += 1
            story.append(Preformatted('\n'.join(block), code))
        elif line.startswith('|'):
            rows = []
            while index < len(lines) and lines[index].startswith('|'):
                row = [value.strip() for value in lines[index].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', value) for value in row):
                    rows.append([Paragraph(inline(value), cell) for value in row])
                index += 1
            index -= 1
            if rows:
                count = max(map(len, rows)); width = A4[0] - 96
                table = Table(rows, colWidths=[width/count]*count, repeatRows=1, hAlign='LEFT')
                table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#d9ebc9')),
                                           ('VALIGN',(0,0),(-1,-1),'TOP'), ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#c3cdc0')),
                                           ('LEFTPADDING',(0,0),(-1,-1),7), ('RIGHTPADDING',(0,0),(-1,-1),7),
                                           ('TOPPADDING',(0,0),(-1,-1),7), ('BOTTOMPADDING',(0,0),(-1,-1),7)]))
                story.extend([table, Spacer(1,12)])
        elif line.startswith('# '):
            story.append(Paragraph(inline(line[2:]), title))
        elif line.startswith('## '):
            story.append(Paragraph(inline(line[3:]), h1))
        elif line.startswith('### '):
            story.append(Paragraph(inline(line[4:]), h2))
        elif line.startswith('#### '):
            story.append(Paragraph(inline(line[5:]), h3))
        elif not line.strip() or line.strip() == '---':
            pass
        else:
            paragraph = [line]
            while (index+1 < len(lines) and lines[index+1].strip()
                   and not re.match(r'^(#|\||```|[-*] |\d+\. |>)', lines[index+1])):
                index += 1; paragraph.append(lines[index])
            textline = ' '.join(paragraph)
            if textline.startswith('- '):
                story.append(Paragraph('• ' + inline(textline[2:]), body))
            elif textline.startswith('> '):
                story.append(Paragraph(inline(textline[2:]), body))
            else:
                story.append(Paragraph(inline(textline), body))
        index += 1

    class HandbookDoc(SimpleDocTemplate):
        def afterFlowable(self, flowable):
            if isinstance(flowable, Paragraph) and flowable.style.name == 'Section':
                key = 'section-' + str(len(self._bookmarks))
                self._bookmarks.append(key)
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(flowable.getPlainText(), key, 0)

    document = HandbookDoc(str(destination), pagesize=A4, rightMargin=48, leftMargin=48,
                           topMargin=44, bottomMargin=46,
                           title='Hermes: The Complete Free-API Handbook', author='Independent community guide')
    document._bookmarks = []
    def footer(canvas, doc):
        canvas.setFont('Handbook',8)
        canvas.setFillColor(colors.HexColor('#607369'))
        canvas.drawString(48,25,'HERMES / FREE API HANDBOOK · Source check: 20 Oct 2026')
        canvas.drawRightString(A4[0]-48,25,str(doc.page))
    document.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    text = compose()
    (ROOT / 'docs/SETUP.md').write_text(text)
    destination = ROOT / 'downloads/HERMES-FULL-FREE-API-HANDBOOK.pdf'
    render_pdf(text, destination)
    print('Handbook words:', len(text.split()))
    print('Numbered chapters:', len(re.findall(r'^## \d+\.',text,re.M)))
    print('PDF:', destination.name, 'bytes:', destination.stat().st_size)


if __name__ == '__main__':
    main()
