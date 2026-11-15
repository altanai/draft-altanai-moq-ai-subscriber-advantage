from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase.pdfmetrics import stringWidth
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = str(ROOT / "output" / "pdf" / "moq_ai_subscriber_advantage_4slides.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, H = 960, 540
BG = HexColor("#FAF8F2")
NAVY = HexColor("#10243A")
INK = HexColor("#182B3C")
MUTED = HexColor("#536578")
TEAL = HexColor("#087E8B")
MINT = HexColor("#E5F0E9")
PALE = HexColor("#EEECE5")
CORAL = HexColor("#D76B52")
WHITE = HexColor("#FFFFFF")
LINE = HexColor("#D8D3C9")
LOGO = str(ROOT / "assets" / "ietf-logo-padded.png")
DRAFT_NAME = "draft-altanai-moq-ai-subscriber-advantage-00"
DRAFT_URL = "https://github.com/altanai/draft-altanai-moq-ai-subscriber-advantage"
MEETING_URL = "https://www.ietf.org/meeting/127/"

c = canvas.Canvas(OUT, pagesize=(W, H), pageCompression=1)
c.setTitle("Authorization and Resource Budgets for MoQ Subscribers")
c.setAuthor("Altanai Bisht")

def para(text, x, y_top, width, font=14, leading=20, color=INK, bold=False, align=TA_LEFT):
    style = ParagraphStyle(
        "p", fontName="Helvetica-Bold" if bold else "Helvetica", fontSize=font,
        leading=leading, textColor=color, alignment=align, spaceAfter=0,
    )
    p = Paragraph(text, style)
    _, h = p.wrap(width, H)
    p.drawOn(c, x, y_top-h)
    return h

def footer(n):
    c.setStrokeColor(LINE); c.setLineWidth(.8); c.line(54,34,W-54,34)
    c.drawImage(LOGO,54,3,width=52,height=29,preserveAspectRatio=True,anchor="sw",mask="auto")
    c.linkURL("https://www.ietf.org/logo/",(54,3,106,32),relative=0)
    x=120; y=16
    c.setFont("Helvetica-Bold",9); c.setFillColor(TEAL); c.drawString(x,y,"IETF 127")
    tw=stringWidth("IETF 127","Helvetica-Bold",9)
    c.linkURL(MEETING_URL,(x,y-2,x+tw,y+10),relative=0)
    x+=tw+8
    c.setFont("Helvetica",8.5); c.setFillColor(MUTED); c.drawString(x,y,"|  Proposed extension  |")
    x+=stringWidth("|  Proposed extension  |","Helvetica",8.5)+8
    c.setFillColor(NAVY); c.drawString(x,y,DRAFT_NAME)
    dw=stringWidth(DRAFT_NAME,"Helvetica",8.5)
    c.linkURL(DRAFT_URL,(x,y-2,x+dw,y+10),relative=0)
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold",9); c.drawRightString(W-113,y,"Altanai Bisht")
    c.setFillColor(MUTED); c.setFont("Helvetica",9); c.drawRightString(W-54,y,f"{n} / 4")

def base(title, n, kicker=None):
    c.setFillColor(BG); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(TEAL); c.rect(0,H-8,W,8,stroke=0,fill=1)
    if kicker:
        c.setFillColor(TEAL); c.setFont("Helvetica-Bold",10); c.drawString(54,H-42,kicker.upper())
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold",28); c.drawString(54,H-82,title)
    footer(n)

def rounded(x,y,w,h,fill,stroke=None,r=12):
    c.setFillColor(fill); c.setStrokeColor(stroke or fill); c.setLineWidth(1)
    c.roundRect(x,y,w,h,r,stroke=1 if stroke else 0,fill=1)

def bullet(x,y,text,width,color=INK,font=14):
    c.setFillColor(TEAL); c.circle(x+4,y-7,3,stroke=0,fill=1)
    return para(text,x+18,y,width-18,font=font,leading=19,color=color)

def arrow(x1,y1,x2,y2,color=TEAL,width=2):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(width)
    c.line(x1,y1,x2,y2)
    import math
    a=math.atan2(y2-y1,x2-x1); L=9; ang=.48
    p=c.beginPath(); p.moveTo(x2,y2)
    p.lineTo(x2-L*math.cos(a-ang),y2-L*math.sin(a-ang))
    p.lineTo(x2-L*math.cos(a+ang),y2-L*math.sin(a+ang)); p.close()
    c.drawPath(p,stroke=0,fill=1)

def icon(name,cx,cy,size,color=TEAL,bg=None):
    """Small, consistent line icon for a concept on the slide."""
    if bg:
        c.setFillColor(bg); c.circle(cx,cy,size*.72,stroke=0,fill=1)
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(max(1.15,size*.095))
    c.setLineCap(1); c.setLineJoin(1)
    s=size
    if name in ("person","group"):
        c.circle(cx,cy+s*.24,s*.16,stroke=1,fill=0)
        p=c.beginPath(); p.moveTo(cx-s*.34,cy-s*.22); p.curveTo(cx-s*.3,cy+s*.02,cx+s*.3,cy+s*.02,cx+s*.34,cy-s*.22); c.drawPath(p,stroke=1,fill=0)
        if name=="group":
            c.circle(cx-s*.36,cy+s*.12,s*.11,stroke=1,fill=0)
            c.circle(cx+s*.36,cy+s*.12,s*.11,stroke=1,fill=0)
            p=c.beginPath(); p.moveTo(cx-s*.55,cy-s*.2); p.curveTo(cx-s*.54,cy-.02*s,cx-s*.35,cy-.02*s,cx-s*.25,cy-s*.1); c.drawPath(p,stroke=1,fill=0)
            p=c.beginPath(); p.moveTo(cx+s*.25,cy-s*.1); p.curveTo(cx+s*.35,cy-.02*s,cx+s*.54,cy-.02*s,cx+s*.55,cy-s*.2); c.drawPath(p,stroke=1,fill=0)
    elif name=="relay":
        pts=[(cx-s*.35,cy+s*.27),(cx+s*.35,cy+s*.27),(cx,cy-s*.3)]
        c.line(*pts[0],*pts[1]); c.line(*pts[0],*pts[2]); c.line(*pts[1],*pts[2])
        for px,py in pts: c.circle(px,py,s*.1,stroke=1,fill=0)
    elif name in ("pulse","priority","bandwidth"):
        p=c.beginPath(); p.moveTo(cx-s*.47,cy)
        if name=="pulse":
            p.lineTo(cx-s*.25,cy); p.lineTo(cx-s*.11,cy+s*.32); p.lineTo(cx+s*.04,cy-s*.3); p.lineTo(cx+s*.2,cy+s*.12); p.lineTo(cx+s*.46,cy+s*.12)
        elif name=="priority":
            p.lineTo(cx-s*.14,cy); p.lineTo(cx-s*.02,cy+s*.25); p.lineTo(cx+s*.08,cy-s*.06); p.lineTo(cx+s*.22,cy+s*.19); p.lineTo(cx+s*.46,cy+s*.19)
        else:
            p.lineTo(cx-s*.25,cy); p.lineTo(cx-s*.1,cy+s*.17); p.lineTo(cx+s*.04,cy-s*.16); p.lineTo(cx+s*.2,cy+s*.28); p.lineTo(cx+s*.46,cy+s*.28)
        c.drawPath(p,stroke=1,fill=0)
    elif name=="shield":
        p=c.beginPath(); p.moveTo(cx,cy+s*.42); p.lineTo(cx+s*.34,cy+s*.27); p.lineTo(cx+s*.29,cy-s*.12); p.lineTo(cx,cy-s*.42); p.lineTo(cx-s*.29,cy-s*.12); p.lineTo(cx-s*.34,cy+s*.27); p.close(); c.drawPath(p,stroke=1,fill=0)
        c.line(cx-s*.14,cy,cx-s*.02,cy-s*.13); c.line(cx-s*.02,cy-s*.13,cx+s*.18,cy+s*.12)
    elif name in ("cache","churn"):
        if name=="cache":
            for yy in (-.22,0,.22): c.roundRect(cx-s*.34,cy+s*yy-s*.08,s*.68,s*.16,s*.04,stroke=1,fill=0)
        else:
            p=c.beginPath(); p.arc(cx-s*.28,cy-s*.28,cx+s*.28,cy+s*.28,30,300); c.drawPath(p,stroke=1,fill=0)
            c.line(cx+s*.25,cy+s*.23,cx+s*.43,cy+s*.24); c.line(cx+s*.25,cy+s*.23,cx+s*.3,cy+s*.06)
    elif name in ("chart","target"):
        if name=="chart":
            c.line(cx-s*.35,cy-s*.32,cx-s*.35,cy+s*.34); c.line(cx-s*.35,cy-s*.32,cx+s*.37,cy-s*.32)
            c.roundRect(cx-s*.2,cy-s*.28,s*.12,s*.28,s*.02,stroke=1,fill=0); c.roundRect(cx,cy-s*.28,s*.12,s*.48,s*.02,stroke=1,fill=0); c.roundRect(cx+s*.2,cy-s*.28,s*.12,s*.62,s*.02,stroke=1,fill=0)
        else:
            c.circle(cx,cy,s*.34,stroke=1,fill=0); c.circle(cx,cy,s*.18,stroke=1,fill=0); c.circle(cx,cy,s*.04,stroke=1,fill=1)

def source_link(label, url, x, y=50):
    c.setFont("Helvetica",8.3); c.setFillColor(TEAL)
    c.drawString(x,y,label)
    w=stringWidth(label,"Helvetica",8.3)
    c.linkURL(url,(x,y-2,x+w,y+10),relative=0)
    return x+w

# Slide 1 - revised proposal direction
c.setFillColor(BG); c.rect(0,0,W,H,stroke=0,fill=1)
c.setFillColor(TEAL); c.rect(0,H-8,W,8,stroke=0,fill=1)
c.setFillColor(TEAL); c.setFont("Helvetica-Bold",10); c.drawString(58,466,"SUBSCRIBER RESOURCES IN MEDIA OVER QUIC")
c.setFillColor(MUTED); c.setFont("Helvetica",10); c.drawRightString(902,466,"PROPOSED EXTENSION")
c.setFillColor(TEAL); c.roundRect(58,170,7,246,3,stroke=0,fill=1)
para("Resource budgets for<br/>MoQ subscribers",88,402,560,font=36,leading=43,color=NAVY,bold=True)
para("Bind service class and usage limits to authorization. Relays account for use and apply temporary restrictions when a stated limit is exceeded.",90,289,520,font=17,leading=24,color=MUTED)
para("Extends the current draft's detection scope.",90,172,520,font=11,leading=15,color=TEAL,bold=True)
# A signed grant and a relay anchor the proposed architecture.
rounded(686,305,204,103,WHITE,stroke=LINE,r=12)
icon("shield",719,375,25,TEAL)
c.setFillColor(NAVY); c.setFont("Helvetica-Bold",13); c.drawString(748,371,"Signed grant")
para("service class<br/>resource budget + expiry",704,348,170,font=11.5,leading=17,color=INK,align=TA_CENTER)
arrow(788,296,788,259,width=1.7)
rounded(686,191,204,60,MINT,stroke=LINE,r=12)
icon("relay",719,220,24,TEAL)
c.setFillColor(NAVY); c.setFont("Helvetica-Bold",13); c.drawString(748,225,"MoQ relay")
para("validate - count - respond",748,214,136,font=9.7,leading=13,color=MUTED)
rounded(90,76,800,65,MINT,r=10)
para("IETF proposal to detect patterns consistent with an advantage, while limiting exposure of subscriber data.",109,122,762,font=14,leading=20,color=NAVY,bold=True)
footer(1)
c.showPage()

# Slide 2 - components and authorization flow
base("Components and data flow",2,"Proposed architecture")
para("An issuer grants permission. The relay checks the grant and tracks use against a defined budget.",54,433,842,font=14,leading=20,color=MUTED)
components=[
    (54,"Grant issuer","issues signed policy<br/>budget + validity","shield",WHITE),
    (278,"Subscriber","presents authorization<br/>requests tracks","group",PALE),
    (502,"MoQ relay","validates + serves<br/>enforces local policy","relay",MINT),
    (726,"Publisher","provides media<br/>to the relay","person",WHITE),
]
for x,title,desc,glyph,fill in components:
    rounded(x,286,180,100,fill,stroke=LINE,r=12)
    icon(glyph,x+90,362,23,TEAL)
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold",13); c.drawCentredString(x+90,337,title)
    para(desc,x+10,325,160,font=10.4,leading=14,color=INK,align=TA_CENTER)
arrow(242,340,270,340,width=1.6)
arrow(466,351,494,351,width=1.6)
arrow(494,309,466,309,width=1.6)
arrow(718,340,690,340,width=1.6)
c.setFillColor(MUTED); c.setFont("Helvetica",8.5)
for x,y,label in [(256,365,"token"),(480,365,"request"),(480,294,"objects"),(704,365,"media")]:
    c.drawCentredString(x,y,label)
# Measured use enters relay accounting; only limited signals enter review.
c.setStrokeColor(TEAL); c.setLineWidth(1.5)
c.line(592,285,592,258); c.line(592,258,515,258)
arrow(515,258,515,237,width=1.5)
c.setFillColor(MUTED); c.setFont("Helvetica",9); c.drawString(605,261,"usage")
for x,w,title,desc,glyph,fill in [
    (54,280,"Privacy + review","Scoped identifiers; window aggregates.<br/>Limit retention and audit detailed access.","shield",PALE),
    (390,250,"Budget ledger","Count use across the budget's sessions.<br/>Track active use, window and expiry.","chart",MINT),
    (696,210,"Policy response","Reject excess requests.<br/>Temporary limits; defined recovery.","target",HexColor("#FCE9E4")),
]:
    rounded(x,122,w,108,fill,stroke=LINE,r=12)
    icon(glyph,x+27,201,20,CORAL if title=="Policy response" else TEAL)
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold",12.5); c.drawString(x+48,197,title)
    para(desc,x+13,177,w-26,font=10.5,leading=15,color=INK,align=TA_CENTER)
arrow(650,173,686,173,width=1.6)
arrow(380,173,344,173,width=1.6)
para("Budget fields and accounting rules are proposed extensions. A token grant does not track remaining usage by itself.",54,92,852,font=10.7,leading=15,color=MUTED)
source_link("MoQT authorization, section 15.3", "https://datatracker.ietf.org/doc/html/draft-ietf-moq-transport-23#section-15.3",54)
source_link("C4M: authorization scopes and revalidation", "https://datatracker.ietf.org/doc/html/draft-ietf-moq-c4m-02",324)
c.showPage()

# Slide 3 - worked budget example and privacy
base("A budget makes excess use explicit",3,"Illustrative worked example")
para("One issuer-scoped budget permits four active subscriptions, counted across all sessions using that budget.",54,433,842,font=14,leading=20,color=MUTED)
rounded(54,167,306,218,WHITE,stroke=LINE,r=12)
icon("shield",80,358,20,TEAL)
c.setFillColor(TEAL); c.setFont("Helvetica-Bold",11); c.drawString(102,354,"EXAMPLE GRANT")
for yy,label,value in [
    (321,"Service class","Standard"),
    (284,"Content scope","live / event"),
    (247,"Active subscriptions","4 across sessions"),
    (210,"Validity","10 minutes"),
]:
    c.setFillColor(MUTED); c.setFont("Helvetica",11); c.drawString(75,yy,label)
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold",11.5); c.drawRightString(340,yy,value)
    if yy>210:
        c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(75,yy-12,340,yy-12)
para("Conceptual policy values; no claim encoding is defined here.",67,151,282,font=9.6,leading=13,color=MUTED)
# Response sequence.
c.setStrokeColor(LINE); c.setLineWidth(1.8); c.line(414,353,414,183)
for yy,num,title,desc,col in [
    (354,"1","Four active subscriptions","Relay admits requests within the grant.",TEAL),
    (297,"2","A fifth subscription is requested","Reject the excess request; return clear feedback.",CORAL),
    (240,"3","Requests continue above the limit","Apply a temporary request limit under local policy.",CORAL),
    (183,"4","The restriction ends","Resume admission when the budget and policy allow.",TEAL),
]:
    c.setFillColor(BG); c.circle(414,yy,13,stroke=0,fill=1)
    c.setFillColor(col); c.circle(414,yy,11,stroke=0,fill=1)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold",10); c.drawCentredString(414,yy-3.5,num)
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold",13); c.drawString(441,yy+4,title)
    para(desc,441,yy-5,448,font=11.5,leading=16,color=MUTED)
rounded(54,68,852,49,MINT,r=9)
icon("shield",78,93,18,TEAL)
para("Privacy: scope budget identifiers to the operator and validity period; retain limited aggregates and restrict detailed review.",99,102,787,font=11.4,leading=16,color=INK)
para("Restrictions follow explicit limit violations. Inferring AI use is unnecessary.",54,53,852,font=9.5,leading=13,color=MUTED)
c.showPage()

# Slide 4 - existing work and proposed contribution
base("Build on existing MoQ authorization",4,"Where the extension fits")
para("Existing drafts supply authorization and relay protections. Resource-budget semantics and accounting need further design.",54,433,842,font=14,leading=20,color=MUTED)
icon("shield",67,378,19,TEAL)
c.setFillColor(NAVY); c.setFont("Helvetica-Bold",16); c.drawString(86,373,"Existing foundations")
c.setStrokeColor(TEAL); c.setLineWidth(2); c.line(54,360,455,360)
for yy,title,desc in [
    (342,"CAT4MOQT / C4M","Tokens authorize actions and content scope; revalidation checks ongoing authorization."),
    (270,"MoQ Relay DoS","Cost tracking, per-client limits and resource isolation already address relay overload."),
    (198,"SIP precedent","RFC 7339 / 7415 control signaling load; RFC 4412 supports authorized resource priority."),
]:
    para(title,54,yy,398,font=12.5,leading=17,color=TEAL,bold=True)
    para(desc,54,yy-22,398,font=11.8,leading=17,color=INK)
icon("target",517,378,19,CORAL)
c.setFillColor(NAVY); c.setFont("Helvetica-Bold",16); c.drawString(536,373,"Design work ahead")
c.setStrokeColor(CORAL); c.setLineWidth(2); c.line(504,360,906,360)
for yy,title,desc in [
    (342,"Define the resource budget","Specify units, windows, bursts and reset rules. A service-class label needs agreed semantics."),
    (270,"Prevent accounting bypass","Define shared counters across sessions or relays; renewing a token must not reset used budget."),
    (198,"Define feedback and recovery","Specify expiry, reauthorization and temporary limits, with scoped identifiers and auditable review."),
]:
    para(title,504,yy,402,font=12.5,leading=17,color=CORAL,bold=True)
    para(desc,504,yy-22,402,font=11.8,leading=17,color=INK)
rounded(54,76,852,44,PALE,r=8)
para("MoQT subscriber priority orders objects within a session. Shared relay budgets need their own accounting and policy.",69,106,822,font=11.2,leading=16,color=NAVY)
source_link("MoQT-23", "https://datatracker.ietf.org/doc/html/draft-ietf-moq-transport-23#section-5.1",54)
source_link("C4M-02 (replaces CAT4MOQT)", "https://datatracker.ietf.org/doc/draft-ietf-moq-c4m/02/",142)
source_link("Relay DoS-02", "https://datatracker.ietf.org/doc/draft-englishm-moq-relay-dos/02/",326)
source_link("RFC 7339", "https://www.rfc-editor.org/rfc/rfc7339.html",440)
source_link("RFC 7415", "https://www.rfc-editor.org/rfc/rfc7415.html",530)
source_link("RFC 4412", "https://www.rfc-editor.org/rfc/rfc4412.html",620)
c.showPage()

c.save()
print(OUT)
