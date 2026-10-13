import numpy as np, math, os
from PIL import Image, ImageDraw, ImageFont
MONO='/home/claude/fonts/SpaceMono-Bold.ttf';ANTON='/home/claude/fonts/Anton-Regular.ttf'
S=4   # supersample factor
def _canvas(w,h):return Image.new('L',(w*S,h*S),0)
def _glyph(ch,H=1000):
    f=ImageFont.truetype(ANTON,1000);bb=f.getbbox(ch);sz=int(1000*H/(bb[3]-bb[1]));f=ImageFont.truetype(ANTON,sz);bb=f.getbbox(ch)
    im=Image.new('L',(bb[2]-bb[0]+8,bb[3]-bb[1]+8),0);ImageDraw.Draw(im).text((4-bb[0],4-bb[1]),ch,font=f,fill=255)
    a=np.array(im);ys,xs=np.where(a>8);return Image.fromarray(a[ys.min():ys.max()+1,xs.min():xs.max()+1])
def ligature(H=1000,overlap=-52,skew=0.13):
    """Unified 73: the 3 tucks into the 7 so they read as one fused glyph (single shape, italic)."""
    g7,g3=_glyph('7',H),_glyph('3',H);W=g7.width+overlap+g3.width;a=np.zeros((H+2,W),np.uint8)
    a[H+2-g7.height:,:g7.width]=np.array(g7);x3=g7.width+overlap;a[H+2-g3.height:,x3:x3+g3.width]=np.maximum(a[H+2-g3.height:,x3:x3+g3.width],np.array(g3))
    ext=int(skew*H);im=Image.fromarray(a).transform((W+ext,H+2),Image.AFFINE,(1,skew,-skew*H,0,1,0),Image.BICUBIC);return im
def trim(m):
    a=np.array(m);ys,xs=np.where(a>6);return m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
def seal(size=1000,lig=None):
    """Plain seal: double ring, four small marks, fused 73 in the centre. No lettering."""
    im=_canvas(size,size);d=ImageDraw.Draw(im);c=size//2*S
    for r,wd in ((size*0.485,size*0.022),(size*0.415,size*0.008)):
        d.ellipse((c-r*S,c-r*S,c+r*S,c+r*S),outline=255,width=int(wd*S))
    for i in range(4):                                        # four quiet marks between the rings
        a=math.pi/2*i-math.pi/4;rr=size*0.45*S;x=c+rr*math.cos(a);y=c+rr*math.sin(a);q=size*0.012*S
        d.polygon([(x,y-q*1.6),(x+q,y),(x,y+q*1.6),(x-q,y)],fill=255)
    g=trim(lig or ligature());gh=int(size*0.40);gw=int(g.width*gh/g.height);g=g.resize((gw*S,gh*S),Image.LANCZOS);im.paste(255,((size*S-g.width)//2,(size*S-g.height)//2),g)
    return im.resize((size,size),Image.LANCZOS)
def tinted(mask,rgb):
    a=np.array(mask);o=np.zeros(a.shape+(4,),np.uint8);o[...,:3]=rgb;o[...,3]=a;return Image.fromarray(o,'RGBA')
def mark_mask():return trim(ligature())                   # wordmark 73 (header / hero)
def seal_mask():return seal()
def lockup_mask(name,use_seal=True,width_frac=1.0,gap=60):
    m=np.array(seal_mask() if use_seal else mark_mask());m=Image.fromarray(m);W=m.width
    f=ImageFont.truetype(MONO,100);cap=f.getbbox('H');sc=int(100*(W*0.058)/(cap[3]-cap[1]));f=ImageFont.truetype(MONO,sc)
    name=name.upper();adv=[f.getlength(c) for c in name];tot=sum(adv);n=len(name);sp=max(6,min((W*0.5*width_frac-tot)/max(n-1,1),W*0.06))
    rowW=tot+sp*(n-1);row=Image.new('L',(W,int(sc*2)),0);d=ImageDraw.Draw(row);x=(W-rowW)/2
    for c,a in zip(name,adv):d.text((x,sc*0.3),c,font=f,fill=255);x+=a+sp
    row=trim(row);out=Image.new('L',(W,m.height+gap+row.height),0);out.paste(m,(0,0));out.paste(row,((W-row.width)//2,m.height+gap));return out
digits_mask=mark_mask
def board(A,B):
    ml=mark_mask();sl=seal_mask()
    for nm,c in (('white',(250,250,247)),('black',(10,10,10))):
        im=tinted(ml,c);im.resize((int(im.width*0.7),int(im.height*0.7)),Image.LANCZOS).save(A+f'logo_{nm}.png',optimize=True);im.save(B+f'73-mark-{nm}.png',optimize=True)
        sm=tinted(sl,c);sm.resize((600,600),Image.LANCZOS).save(A+f'seal_{nm}.png',optimize=True);sm.save(B+f'73-seal-{nm}.png',optimize=True)
    for nm in ('HENTY','GILBERT','EDWARDES'):
        lm=lockup_mask(nm);tinted(lm,(250,250,247)).save(B+f'73-seal-lockup-{nm.lower()}-white.png',optimize=True);tinted(lm,(10,10,10)).save(B+f'73-seal-lockup-{nm.lower()}-black.png',optimize=True)
    def square(sz,bg,fg,which,pad=0.16):
        im=Image.new('RGB',(sz,sz),bg);t=tinted(which,fg);w=int(sz*(1-2*pad));h=int(w*which.height/which.width);t=t.resize((w,h),Image.LANCZOS);im.paste(t,((sz-w)//2,(sz-h)//2),t);return im
    square(512,(10,10,10),(250,250,247),sl,0.08).save(A+'icon_512.png');square(180,(10,10,10),(250,250,247),sl,0.06).save(A+'apple-touch-icon.png');square(64,(10,10,10),(250,250,247),ml,0.14).save(A+'favicon.png')
    og=Image.new('RGB',(1200,630),(10,10,10));t=tinted(sl,(250,250,247)).resize((420,420),Image.LANCZOS);og.paste(t,((1200-420)//2,60),t)
    d=ImageDraw.Draw(og);f=ImageFont.truetype(MONO,28);txt='73  —  MELBOURNE STREETWEAR';w=d.textlength(txt,font=f);d.text(((1200-w)/2,520),txt,font=f,fill=(250,250,247));og.save(A+'og_image.jpg',quality=90)
if __name__=='__main__':
    board('/home/claude/site/assets/','/home/claude/brand/');print('brand assets built')
