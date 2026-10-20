from pathlib import Path
import sys, io, json, shutil, zipfile, textwrap, re
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'share-pack'
OUT.mkdir(parents=True, exist_ok=True)
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

# 01: Overview, visual route ladder.
y=begin(1,'THE STRATEGY','FREE FIRST.\nPAID BY CHOICE.','Run useful AI without making every task a paid API call.')
steps=[('01','SCRIPT','A normal tool can solve it? Skip the LLM.'),('02','LOCAL','Private data or a small job? Use your hardware.'),('03','FREE CLOUD','Use a capable, verified zero-price model.'),('04','PAID: ASK FIRST','Only by choice, or a bounded preapproved exception.')]
for num,label,body in steps:
    fill=ORANGE if num=='04' else GREEN if num=='03' else PANEL
    draw.rounded_rectangle((60,y,1020,y+139),radius=22,fill=fill)
    txt(num,87,y+27,38,bold=True,width=80)
    txt(label,176,y+23,32,bold=True,width=810)
    txt(body,176,y+70,29,width=805,leading=36)
    y+=157
# Keep the takeaway compact; this is a sequence, not mandatory extra hops.
y=txt('Free cloud can be your daily default. Local is optional, not a mandatory extra hop.',60,y+3,31,width=955,color=MUTED,leading=39)
save('the-strategy',y)

# 02: Real install route, readable link instead of a tiny long shell URL.
y=begin(2,'SETUP / 1','INSTALL\nHERMES','Start with the official app. Free cloud does not need a powerful GPU.')
y=box('1 / DOWNLOAD','Open the official website and follow the installation steps for your operating system.',y)
y=link('hermes-agent.nousresearch.com','https://hermes-agent.nousresearch.com/',y)
y=box('2 / SET UP','Run the setup wizard, then check that Hermes starts correctly.',y)
y=code('hermes setup\nhermes doctor',y,30)
y=txt('Already installed? Back up your active configuration first. Apply changes to the intended profile only.',60,y,32,color=MUTED,width=945,leading=40)
y=link('Official installation instructions →','https://hermes-agent.nousresearch.com/docs/getting-started/installation',y+25)
save('install-hermes',y)

# 03: Connection and exact selectable model ID.
y=begin(3,'SETUP / 2','CONNECT A\nFREE MODEL','Use your own OpenRouter account and API key.')
y=bullet('CREATE YOUR KEY','Open openrouter.ai/settings/keys. Enter the key in Hermes provider setup — never in a chat.',y)
y=code('hermes model',y,31)
y=txt('Choose OpenRouter, then select a currently free, tool-capable model.',60,y,34,width=940,leading=43)
y=box('STARTER MODEL / CATALOG-CHECKED','nvidia/nemotron-3-ultra-550b-a55b:free',y+27,fill=GREEN,body_size=31)
y=box('EASY ALTERNATIVE','openrouter/free selects from eligible free models. It is NOT the same as openrouter/auto.',y,body_size=32)
y=link('openrouter.ai/models?pricing=free','https://openrouter.ai/models?pricing=free',y)
y=txt('Start a new chat after setting your default. Free availability can change.',60,y,29,width=950,color=MUTED,leading=37)
save('connect-free-model',y)

# 04: Main reliability / billing distinction.
y=begin(4,'SETUP / 3','FREE-ONLY\nBACKUPS','A free primary with a paid fallback can still generate a bill.')
y=code('hermes fallback\nhermes fallback list',y,31)
y=box('ADD ONLY VERIFIED FREE / LOCAL ROUTES','For example: poolside/laguna-s-2.1:free or openrouter/free through OpenRouter.',y,fill=GREEN,body_size=32)
y=bullet('SERVICE FAILURE ≠ WRONG ANSWER','Fallback reacts to API errors. It does not determine whether an answer is correct.',y)
y=bullet('QUOTA EXHAUSTED?','Wait, use local, or ask. Another model can share the same daily account limit.',y)
y=txt('Never put a paid model at the end “just in case.” Check upstream proxies and old fallback_model settings too.',60,y,32,width=948,color=MUTED,leading=40)
y=link('Fallback setup and behavior →','https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers',y+25)
save('free-only-backups',y)

# 05: Optional local route.
y=begin(5,'OPTIONAL / LOCAL','KEEP PRIVATE\nWORK LOCAL','No hosted inference bill. Your hardware, electricity and memory still matter.')
y=box('DESKTOP PATH','Settings → Providers → Local Models. Click Install runtime.',y,fill=GREEN,body_size=32)
y=bullet('DOWNLOAD A MODEL THAT FITS','Choose tool support and realistic memory fit, not just the biggest model name.',y)
y=bullet('CLICK USE + TEST A REAL TOOL CALL','A fluent chat reply does not prove the model can execute tools.',y)
y=box('ALREADY HAVE OLLAMA?','Reuse it. The usual endpoint is http://127.0.0.1:11434/v1 — verify your actual port.',y,body_size=31)
y=txt('Local-only means local auxiliary calls and no cloud fallback. Keep unauthenticated servers off the internet.',60,y,30,width=950,color=MUTED,leading=38)
y=link('Official Local Models guide →','https://hermes-agent.nousresearch.com/docs/user-guide/local-models',y+20)
save('optional-local-models',y)

# 06: Hidden sources of spend.
y=begin(6,'COST CONTROL','CHECK THE\nHIDDEN CALLS','Your main chat model is only one place that can spend money.')
y=bullet('CRON + SUBAGENTS','Pin free/local models independently. Audit existing jobs and worker overrides.',y)
y=bullet('AUXILIARY MODELS','Check compression, titles, vision and approvals. “Auto” may follow a paid chat model.',y)
y=bullet('PLUGINS + TOOL APIs','Search, images, speech, cloud browsers and memory services can bill separately.',y)
y=box('CHEAPEST AUTOMATION','Use a script-only no-agent job for deterministic checks. Do not wake an LLM just to compare files.',y,fill=GREEN,body_size=32)
y=link('Inspect models and auxiliary settings →','https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models',y)
y=txt('Free quotas are finite. One agent task can consume many API requests.',60,y,31,width=945,color=MUTED,leading=39)
save('background-costs',y)

# 07: The actual tactic / permission.
y=begin(7,'PAID / LAST RESORT','NO SILENT\nPAID UPGRADE.','Recommended mode: ask before spending. Free-route failure is not permission.')
y=box('COPY THIS RULE','Use tools, local, then free models. Paid models require my explicit permission. Keep automatic fallbacks free/local. Verify results.',y,fill=GREEN,body_size=32)
y=bullet('IF YOU AUTHORIZE A PAID STEP','Name the model, scope and budget. Enforce the cap with the provider or a budget-aware dispatcher.',y)
y=bullet('JEV IS OPTIONAL','It can advise retry / stop / escalate. Hosted API use may cost money.',y)
y=box('CONFIDENCE IS NOT CONSENT','A gate threshold of 0.90 is a policy choice, not spending permission or proof of accuracy. No reliable gate? Ask.',y,fill=ORANGE,body_size=32)
save('paid-only-by-permission',y)

# 08: Practical smoke test and useful links.
y=begin(8,'VERIFY + SHARE','TEST IT.\nTHEN SHARE IT.','Do not trust a model simply claiming that it is free or local.')
y=box('ASK IN AN EMPTY TEST DIRECTORY','Use a terminal or file tool to list this directory. Report the actual tool result. Do not modify files.',y,fill=GREEN,body_size=32)
y=bullet('CHECK THE ACTUAL ROUTE','Look at Hermes provider/model metadata and openrouter.ai/activity. Review any charges.',y)
y=txt('USEFUL LINKS / CLICK IN THE PDF',60,y,29,bold=True); y+=54
y=link('Hermes documentation','https://hermes-agent.nousresearch.com/docs/',y)
y=link('Free models + current pricing','https://openrouter.ai/models?pricing=free',y)
y=link('OpenRouter limits and quotas','https://openrouter.ai/docs/api/reference/limits',y)
y=link('Check provider activity','https://openrouter.ai/activity',y)
y=txt('Share images 01–08 as one album, or forward the PDF. Never share API keys or private logs.',60,y+8,30,width=945,bold=True,leading=38)
y+=2
y=txt('Free cloud sends data to third parties. Availability and quotas change. Full commands are in the companion text guide.',60,y,29,width=940,color=MUTED,leading=37)
save('verify-and-share',y)

# Small, selectable copy/paste companion: original verified guide, unchanged.
source=ROOT / 'docs' / 'SETUP.md'
shutil.copyfile(source,OUT/'FULL-SETUP-GUIDE.md')
caption='''HERMES: FREE FIRST, PAID ONLY BY CHOICE\n\nA practical 8-card guide: install Hermes, connect free models, add free-only backups, use optional local models, and keep cron/subagents from silently spending.\n\nStart: https://hermes-agent.nousresearch.com/\nFree models: https://openrouter.ai/models?pricing=free\n\nScripts when possible → local when useful → capable free cloud → paid only with permission or a bounded preapproved exception.\n\nFree does not mean unlimited. Cloud prompts leave your machine. Hosted Jev and external tools may cost money.\n\nSend images 01–08 in order as one Telegram album. Send as files to preserve sharp text. The PDF has clickable links; the Markdown guide has copyable commands. Independent guide; source checks: 20 October 2026.\n'''
(OUT/'TELEGRAM-CAPTION.txt').write_text(caption)
(OUT/'README.txt').write_text('''FREE-FIRST SHARE PACK\n\n01–08 PNG: portrait 1080 x 1350 image guide. Send in numeric order as one album.\nFREE-FIRST-VISUAL-GUIDE.pdf: the same 8 cards, with clickable resource links.\nFULL-SETUP-GUIDE.md: complete setup instructions and copyable commands.\nTELEGRAM-CAPTION.txt: ready-to-paste sharing caption.\n\nThis is an illustrated guide, not screenshots of the application. Model/catalog facts come from the checked companion guide. Availability and quotas may change.\n''')

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
assert b'openrouter.ai/activity' in pdf.read_bytes()
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
