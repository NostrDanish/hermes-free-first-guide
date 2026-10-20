from pathlib import Path
import sys, io, json, shutil, zipfile, textwrap, re
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'share-pack'
OUT.mkdir(parents=True, exist_ok=True)
# Replace only this generator's numbered image cards.
for stale in OUT.glob('[0-9][0-9]-*.png'):
    stale.unlink()
W,H=1080,1350
BG='#F4F3EA'; INK='#142D2B'; MUTED='#506762'; GREEN='#C6EE9A'; PANEL='#E5EBDD'; LINE='#CCD7C8'; ORANGE='#F2AE78'; WHITE='#FFFFFF'
REG='/usr/share/fonts/liberation/LiberationSans-Regular.ttf'
BOLD='/usr/share/fonts/liberation/LiberationSans-Bold.ttf'
MONO='/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf'
links=[]; bounds=[]; allpages=[]

def font(size, bold=False, mono=False):
    return ImageFont.truetype(MONO if mono else BOLD if bold else REG,size)

def wrap(text, size, width, bold=False, mono=False):
    f=font(size,bold,mono); result=[]
    for para in text.split('\n'):
        if not para: result.append(''); continue
        line=''
        for word in para.split(' '):
            test=(line+' '+word).strip()
            if f.getlength(test)<=width: line=test
            else:
                if line: result.append(line)
                assert f.getlength(word)<=width, (word,size,width)
                line=word
        result.append(line)
    return result

def txt(text,x,y,size=34,width=948,bold=False,color=INK,mono=False,leading=None):
    lines=wrap(text,size,width,bold,mono); leading=leading or round(size*1.28)
    f=font(size,bold,mono)
    for line in lines:
        draw.text((x,y),line,font=f,fill=color,anchor='lt')
        bounds.append((page,x,y,f.getlength(line),leading,line))
        y+=leading
    return y

def pill(label,x,y,fill=GREEN):
    f=font(24,True); ww=int(f.getlength(label))+34
    draw.rounded_rectangle((x,y,x+ww,y+43),radius=21,fill=fill)
    draw.text((x+17,y+9),label,font=f,fill=INK,anchor='lt')

def begin(n,category,title,sub):
    global im,draw,page,links
    page=n; links=[]
    im=Image.new('RGB',(W,H),BG); draw=ImageDraw.Draw(im)
    draw.rectangle((0,0,W,12),fill=INK)
    txt('HERMES / FREE-FIRST',60,46,24,bold=True)
    pill(category,650,38)
    draw.line((60,107,1020,107),fill=LINE,width=2)
    y=txt(title,60,140,70,width=960,bold=True,leading=74)
    y=txt(sub,60,y+18,30,width=940,color=MUTED,leading=37)
    return y+30

def box(label,body,y,fill=PANEL,body_size=33):
    rows=wrap(body,body_size,864)
    hh=26+44+12+len(rows)*round(body_size*1.24)+22
    draw.rounded_rectangle((60,y,1020,y+hh),radius=24,fill=fill)
    yy=txt(label,88,y+22,34,bold=True,width=860)
    txt(body,88,yy+12,body_size,width=864,leading=round(body_size*1.24))
    return y+hh+18

def code(lines,y,size=27):
    rows=lines.split('\n'); hh=30+len(rows)*37+26
    draw.rounded_rectangle((60,y,1020,y+hh),radius=22,fill=INK)
    for i,line in enumerate(rows):txt(line,85,y+25+i*37,size,width=910,mono=True,color=GREEN,leading=37)
    return y+hh+26

def bullet(title,body,y):
    draw.ellipse((63,y+5,77,y+19),fill=INK)
    y=txt(title,97,y,36,bold=True,width=915)
    y=txt(body,97,y+10,32,width=900,color=MUTED,leading=40)
    return y+29

def link(label,url,y):
    end=txt(label,60,y,29,width=955,bold=True,color=INK,leading=37)
    draw.line((60,end+4, min(1020,60+font(29,True).getlength(label)),end+4),fill=INK,width=1)
    links.append((60,y,1020,end+8,url))
    return end+23

def footer(note='Independent guide | checked 20 Oct 2026'):
    draw.line((60,1259,1020,1259),fill=LINE,width=2)
    txt(note,60,1280,22,width=850,color=MUTED)
    txt(f'{page:02d} / 08',918,1278,24,width=110,bold=True)

def save(slug,y):
    assert y<=1232, ('page overflow',page,y)
    footer()
    p=OUT/f'{page:02d}-{slug}.png'; im.save(p,optimize=True)
    allpages.append((p,list(links)))

# 01: Full-stack overview.
y=begin(1,'THE FULL STACK','HERMES.\nFREE API FIRST.','Nous + OpenRouter + FreeLLMAPI. Local when useful. Paid only by choice.')
for label,body,fill in [
    ('HERMES IS THE AGENT','It uses approved tools, models, skills and scheduled jobs.',PANEL),
    ('NOUS + OPENROUTER','Start with an eligible, explicitly free model route.',GREEN),
    ('FREELLMAPI IS THE ROUTER','Combine only the upstream allowances you actually have.',PANEL),
    ('FREE ≠ EVERY SERVICE','Trials, earned credits and paid subscriptions are different.',ORANGE)]:
    y=box(label,body,y,fill=fill,body_size=31)
save('the-strategy',y)

# 02: Hermes installation and basic controls.
y=begin(2,'START / HERMES','INSTALL THE\nAGENT FIRST.','A free cloud API does not require a powerful GPU.')
y=box('1 / USE THE OFFICIAL INSTALLER','Choose the correct desktop or CLI package for your operating system.',y,body_size=32)
y=link('hermes-agent.nousresearch.com','https://hermes-agent.nousresearch.com/',y)
y=code('hermes setup\nhermes model\nhermes doctor',y,30)
y=bullet('TEST A REAL TOOL CALL','In an empty folder, ask it to list files without modifying anything.',y)
y=txt('Keep command approvals on. Review tool backends: free chat does not make search, images or cloud browsers free.',60,y,31,width=950,color=MUTED,leading=39)
save('install-hermes',y)

# 03: Nous is a first-class free route, not an OpenRouter footnote.
y=begin(3,'PROVIDER / NOUS','NOUS PORTAL\nHAS A FREE PLAN.','Free models only. $0 monthly credits is not a budget for paid models.')
y=bullet('CREATE / SIGN INTO YOUR ACCOUNT','Choose the Free plan, then use Hermes model setup → Nous Portal.',y)
y=box('CHECKED STARTER MODEL','poolside/laguna-s-2.1:free',y,fill=GREEN,body_size=32)
y=box('API BASE URL','https://inference-api.nousresearch.com/v1',y,body_size=30)
y=txt('Use exact free IDs from the current catalog. Hosted tools have separate entitlements. Never assume every Portal model or tool is free.',60,y,31,width=950,color=MUTED,leading=39)
y=link('portal.nousresearch.com','https://portal.nousresearch.com/',y+22)
y=link('Free plan and current paid options →','https://portal.nousresearch.com/manage-subscription',y)
save('nous-portal-free',y)

# 04: Independent OpenRouter signup and current free model selection.
y=begin(4,'PROVIDER / OPENROUTER','ADD ANOTHER\nFREE API ROUTE.','Create your own key. Enter it only in trusted local provider settings.')
y=link('openrouter.ai/settings/keys','https://openrouter.ai/settings/keys',y)
y=box('SELECT A VERIFIED FREE MODEL','nvidia/nemotron-3-ultra-550b-a55b:free',y,fill=GREEN,body_size=31)
y=box('OR USE THE FREE ROUTER','openrouter/free selects eligible free models. Do not confuse it with openrouter/auto.',y,body_size=32)
y=bullet('KEEP EVERY FALLBACK FREE / LOCAL','A free main model plus a paid backup can still generate a bill.',y)
y=txt('Free quotas are shared across your account. When exhausted: wait, use local, or ask — do not evade limits.',60,y,31,width=945,color=MUTED,leading=39)
y=link('Browse current free models →','https://openrouter.ai/models?pricing=free',y+20)
save('openrouter-free',y)

# 05: Gateway, upstream keys and actual entitlement.
y=begin(5,'ROUTER / FREELLMAPI','ONE LOCAL API.\nYOUR OWN ALLOWANCES.','The self-hosted router does not manufacture free provider credits.')
y=bullet('INSTALL THE RIGHT PROJECT','Use tashfeenahmed/freellmapi. Choose its supported desktop or Docker/server path.',y)
y=bullet('ADD LEGITIMATE UPSTREAM KEYS','Use its local Keys UI. Enable and test eligible free models only.',y)
y=box('CONNECT HERMES AS A CUSTOM ENDPOINT','Usual server URL: http://127.0.0.1:3001/v1. Use the unified gateway key — not the admin token.',y,fill=GREEN,body_size=31)
y=txt('Audit the gateway chain AND Hermes fallbacks. auto is only as free as its enabled routes. The optional live catalog subscription is paid.',60,y,30,width=945,color=MUTED,leading=38)
y=link('Correct source and installation guide →','https://github.com/tashfeenahmed/freellmapi',y+22)
save('freellmapi-gateway',y)

# 06: Honest access categories instead of calling every installed route free.
y=begin(6,'MORE PROVIDERS','KNOW WHAT\n“FREE” MEANS.','Installed, connected and free are three different claims.')
y=box('ELIGIBLE FREE ALLOWANCES','Groq, Gemini, Mistral and Cloudflare: check your exact plan, model, limits and data terms.',y,fill=GREEN,body_size=31)
y=box('EARNED CREDITS / TRIALS','Pollinations Quest Pollen is finite. NVIDIA, Cerebras and Cohere have trial/evaluation terms.',y,body_size=31)
y=box('DO NOT LABEL THESE FREE APIs','NanoGPT: web-free is not API-free. Cheaper Inference: paid. HF hosted free accounts: no included credits.',y,fill=ORANGE,body_size=31)
y=txt('The full handbook includes signup links, API setup, entitlement checks and the installed-provider inventory.',60,y,31,width=945,color=MUTED,leading=39)
save('other-provider-allowances',y)

# 07: Local privacy and hidden billing surfaces.
y=begin(7,'CONTROL / SPENDING','LOCAL WHEN USEFUL.\nNO SILENT SPEND.','Private work needs local inference, local auxiliaries and no cloud fallback.')
y=bullet('OPTIONAL LOCAL MODELS','Hermes Settings → Providers → Local Models. Download only a model that fits your hardware.',y)
y=bullet('PIN BACKGROUND WORK','Audit cron pins, workers, subagents, compression, titles, vision and external tools.',y)
y=box('PAID REQUIRES PERMISSION','Only an explicit choice or a bounded, preauthorized exception. Enforce budgets outside the prompt.',y,fill=GREEN,body_size=32)
y=txt('Jev is optional. A confidence score is not spending permission, and a hosted decision API can itself cost money.',60,y,31,width=945,color=MUTED,leading=39)
save('local-and-cost-controls',y)

# 08: Links and safe handoff.
y=begin(8,'VERIFY / SHARE','TEST THE ROUTE.\nSHARE THE GUIDE.','A model claiming it is free is not evidence. Check actual routing and activity.')
y=box('START WITH A HARMLESS TEST','Ask for a real read-only tool call. Inspect the served model, provider, quota and cost before automation.',y,fill=GREEN,body_size=31)
y=link('Hermes docs and setup','https://hermes-agent.nousresearch.com/docs/',y)
y=link('Nous Portal Free plan','https://portal.nousresearch.com/manage-subscription',y)
y=link('OpenRouter free model catalog','https://openrouter.ai/models?pricing=free',y)
y=link('FreeLLMAPI project and install','https://github.com/tashfeenahmed/freellmapi',y)
y=box('FULL HANDBOOK + AI SETUP KIT','The share pack includes the complete linked PDF, copyable Markdown, image cards and sharing caption.',y,body_size=31)
y=txt('Never share keys, auth.json or private logs. Free cloud sends data to third parties; quotas and terms can change.',60,y,30,width=945,color=MUTED,leading=38)
save('verify-and-share',y)

# Small, selectable copy/paste companion: original verified guide, unchanged.
source=ROOT / 'docs' / 'SETUP.md'
shutil.copyfile(source,OUT/'FULL-SETUP-GUIDE.md')
shutil.copyfile(ROOT/'downloads/HERMES-FULL-FREE-API-HANDBOOK.pdf',OUT/'HERMES-FULL-FREE-API-HANDBOOK.pdf')
for archive in ['hermes-free-first-setup-kit.zip', 'hermes-free-first-setup-skill.zip']:
    shutil.copyfile(ROOT/'downloads'/archive, OUT/archive)
caption='''HERMES: THE COMPLETE FREE-API SETUP\n\nNous Portal Free + OpenRouter free models + FreeLLMAPI + optional local inference. The full handbook explains account signup, keys, endpoints, free-only routing, background jobs and verification.\n\nNot every installed provider is free: Pollinations can use earned Pollen, NanoGPT API allowances are paid-plan usage, and Cheaper Inference is paid. Trials and quotas have limits.\n\nStart: https://hermes-agent.nousresearch.com/\nNous: https://portal.nousresearch.com/\nOpenRouter: https://openrouter.ai/models?pricing=free\nFreeLLMAPI: https://github.com/tashfeenahmed/freellmapi\n\nForward the complete handbook PDF, or send images 01–08 in order. Send images as files for sharper text. Never forward keys or private configuration. Independent guide; source check: 20 October 2026.\n'''
(OUT/'TELEGRAM-CAPTION.txt').write_text(caption)
(OUT/'README.txt').write_text('''FREE-FIRST SHARE PACK\n\n01–08 PNG: portrait 1080 x 1350 image guide. Send in numeric order as one album.\nFREE-FIRST-VISUAL-GUIDE.pdf: the same 8 cards, with clickable resource links.\nHERMES-FULL-FREE-API-HANDBOOK.pdf: complete Hermes/provider setup with selectable text and links.\nFULL-SETUP-GUIDE.md: complete setup instructions and copyable commands.\nhermes-free-first-setup-kit.zip: setup helper, portable AI skill, instructions and tests.\nhermes-free-first-setup-skill.zip: standalone portable skill folder.\nTELEGRAM-CAPTION.txt: ready-to-paste sharing caption.\n\nThis is an illustrated guide, not screenshots of the application. Model/catalog facts come from the checked companion guide. Availability and quotas may change.\n''')

pdf=OUT/'FREE-FIRST-VISUAL-GUIDE.pdf'
c=canvas.Canvas(str(pdf),pagesize=(540,675),pageCompression=1)
c.setTitle('Hermes Free-First — A Visual Setup Guide')
c.setAuthor('Independent community guide')
c.setSubject('Free models, optional local inference, and explicit paid permission')
for p,rectangles in allpages:
    c.drawImage(str(p),0,0,width=540,height=675)
    for x1,y1,x2,y2,url in rectangles:
        c.linkURL(url,(x1/2,(H-y2)/2,x2/2,(H-y1)/2),relative=0,thickness=0)
    c.showPage()
c.save()

# Automated layout / content / packaging checks.
assert len(allpages)==8
for n,x,y,width,height,text in bounds:
    assert x>=0 and x+width<=W+1,(n,'horizontal overflow',text)
    assert y>=0 and y+height<=H,(n,'vertical overflow',text)
for p,_ in allpages:
    with Image.open(p) as check:
        assert check.size==(1080,1350)
        check.verify()
assert pdf.read_bytes().startswith(b'%PDF-')
assert len(re.findall(rb'/Type\s*/Page\b',pdf.read_bytes()))==8
# ReportLab leaves annotation URL strings directly inspectable.
assert b'portal.nousresearch.com/manage-subscription' in pdf.read_bytes()
manifest={'pages':8,'image_dimensions':[1080,1350],'pdf_link_annotations':sum(len(ls) for _,ls in allpages),'layout_text_runs':len(bounds),'files':[{'name':p.name,'bytes':p.stat().st_size} for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'verification.json']}
(OUT/'verification.json').write_text(json.dumps(manifest,indent=2))
zip_path=ROOT/'downloads'/'HERMES-FREE-FIRST-SHARE-PACK.zip'
zip_path.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()):
        if p.is_file():z.write(p,p.name)
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if n.endswith('.png')])==8
print(json.dumps({'output':str(OUT),'pdf':str(pdf),'zip':str(zip_path),'zip_bytes':zip_path.stat().st_size,**manifest},indent=2))
