"""Rebuild cropped PDF excerpts as real SVG text with the original glyph outlines.

The font mappings below were checked against the book's actual math glyphs. The
PDF's legacy symbol encodings otherwise copy as Latin letters or replacement
characters. Graphics and equation rules stay as original vector artwork.
"""
from __future__ import annotations
import base64
from collections import defaultdict
import hashlib
import html
import io
import json
import re
import xml.etree.ElementTree as ET
import pymupdf as fitz
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

SVG='http://www.w3.org/2000/svg'
XLINK='http://www.w3.org/1999/xlink'
MATH_ONE={1:'·',2:'=',3:'+',4:'−',5:'±',7:'×',8:'<',9:'τ',10:' ',11:'π',12:'ρ',14:'≥',15:'Δ',16:'>',17:'′',19:'θ',21:'°',22:'ϕ',23:'∞',24:'≪',25:'≫',26:'ω',27:'I',28:'M',29:'Ω',31:'∂',32:'λ',34:'γ',35:'ε',36:'Φ',42:'Ψ',43:'ℏ'}
GREEK={1:'α',2:'β',3:'κ',4:'μ',5:'θ',6:' ',16:'ψ',19:'ϕ',20:'γ',24:'λ',27:'π',28:'ρ',29:'σ',30:'τ',31:'ω',37:'ε'}
SPECIAL={
 'MathePiSev':GREEK,'MathePiEig':{3:'ρ'},'MathematicalPi-One':MATH_ONE,
 'MathematicalPi-Three':{1:'|',2:'∫',4:'(',5:')',6:'≈',8:'Σ',12:'|',13:'∮',14:'∮',16:'/'},
 'MathematicalPi-Four':{2:' ',3:'·'},'MathematicalPi-Six':{3:'⊥'},
 'MathematicalPi-Two':{1:'ℓ',4:'ℰ'},'Fancy2k':{1:'ℰ'},'Optr2k':{1:'ℓ'},
 'ProgressivePi':{1:'→'},'Rads2K':{1:'√',2:'√',3:'√'},'Symbol':{1:' '},
}


def unicode_char(font, gid, source):
    if font in SPECIAL:
        if gid not in SPECIAL[font]:
            raise ValueError(f'Unmapped math glyph: {font}, {gid}, {source!r}')
        return SPECIAL[font][gid]
    if len(source)!=1 or source=='\ufffd' or 0xe000<=ord(source)<=0xf8ff:
        raise ValueError(f'Unmapped glyph: {font}, {gid}, {source!r}')
    return source


class SelectableTextBuilder:
    def __init__(self, source):
        self.document=fitz.open(source)
        self.fonts=[]
        self.families=defaultdict(list)
        self.audit=[]

    def font_for(self, family, char, path, width):
        # Separate variant faces when the same Unicode character uses two outlines
        # (for example, different-size integral signs or radicals).
        code=ord(char)
        for index in self.families[family]:
            old=self.fonts[index]['glyphs'].get(code)
            if old is None or old['path']==path:
                self.fonts[index]['glyphs'][code]={'path':path,'width':width}
                return f'PdfText{index}'
        index=len(self.fonts)
        self.families[family].append(index)
        self.fonts.append({'source':family,'glyphs':{code:{'path':path,'width':width}}})
        return f'PdfText{index}'

    def excerpt(self, chapter, piece, number):
        page=self.document[piece['page']-1]
        crop=fitz.Rect(piece['crop'])
        raw=page.get_svg_image(text_as_path=True)
        root=ET.fromstring(raw)
        paths={e.get('id'):e.get('d','') for e in root.iter()
               if e.tag==f'{{{SVG}}}path' and e.get('id','').startswith('font_')}
        uses=[e for e in root.iter() if e.tag==f'{{{SVG}}}use' and 'data-text' in e.attrib]
        chars=[(span,char) for span in page.get_texttrace() for char in span['chars']]
        assert len(uses)==len(chars),(piece['page'],len(uses),len(chars))
        replacements={}
        count=0
        glyph_records=[]
        for glyph_index,(use,(span,char)) in enumerate(zip(uses,chars)):
            if not crop.contains(fitz.Point(char[2])):
                replacements[use]=None
                continue
            source=use.get('data-text')
            gid=char[1]
            family=span['font']
            text=unicode_char(family,gid,source)
            path=paths[use.get(f'{{{XLINK}}}href')[1:]]
            font=self.font_for(family,text,path,(char[3][2]-char[3][0])/span['size']*1000 if span['size'] else 500)
            values=[float(v) for v in re.findall(r'-?\d*\.?\d+(?:e[+-]?\d+)?',use.get('transform'),re.I)]
            assert len(values)==6,values
            a,b,c,d,x,y=values
            # SVG text already flips the font's upward Y axis. Undo the path-only
            # glyph flip while preserving rotations, shears and exact positions.
            matrix=f'{a:.6g},{b:.6g},{-c:.6g},{-d:.6g},{x:.6g},{y:.6g}'
            fill=use.get('fill','#000')
            pos=f'{char[2][0]:.3f} {char[2][1]:.3f} {span["size"]:.3f} {char[3][2]:.3f}'
            opacity=f' opacity="{use.get("opacity")}"' if use.get('opacity') is not None else ''
            replacements[use]={'font':font,'char':text,'matrix':(a,b,-c,-d,x,y),'fill':fill,'pos':pos,'opacity':use.get('opacity'),'gid':glyph_index}
            glyph_records.append({'id':glyph_index,'text':text,'x':char[2][0],'y':char[2][1],'end':char[3][2],'size':span['size']})
            count+=1
        # Group characters into text runs so native browser selection also works.
        # Each tspan retains its original position for accurate plain-text copying.
        ET.register_namespace('',SVG)
        ET.register_namespace('xlink',XLINK)
        for parent in list(root.iter()):
            run=None
            previous=None
            for child in list(parent):
                if child not in replacements:
                    run=None;previous=None
                    continue
                index=list(parent).index(child)
                parent.remove(child)
                item=replacements[child]
                if item is None:
                    run=None;previous=None
                    continue
                a,b,c,d,x,y=item['matrix']
                same=previous and item['font']==previous['font'] and item['fill']==previous['fill'] and item['opacity']==previous['opacity'] and all(abs(v-w)<1e-6 for v,w in zip(item['matrix'][:4],previous['matrix'][:4]))
                dx=dy=0
                if same:
                    px,py=previous['matrix'][4:]
                    det=a*d-b*c
                    dx=(d*(x-px)-c*(y-py))/det
                    dy=(-b*(x-px)+a*(y-py))/det
                    same=abs(dy)<0.001
                if not same:
                    attrs={'font-family':item['font'],'font-size':'1','transform':f'matrix({a:.6g},{b:.6g},{c:.6g},{d:.6g},{x:.6g},{y:.6g})','fill':item['fill']}
                    if item['opacity'] is not None:attrs['opacity']=item['opacity']
                    run=ET.Element(f'{{{SVG}}}text',attrs)
                    parent.insert(index,run)
                    previous=item
                    dx=0
                node=ET.SubElement(run,f'{{{SVG}}}tspan',{'class':'pdf-char','data-p':item['pos'],'data-g':str(item['gid']),'x':f'{dx:.6g}','y':'0'})
                node.text=item['char']
        for parent in list(root.iter()):
            for child in list(parent):
                if child.tag==f'{{{SVG}}}path' and child.get('id','').startswith('font_'):
                    parent.remove(child)
        root.attrib.update({'class':'regenerated-page','width':f'{piece["width"]:.3f}','height':f'{piece["height"]:.3f}','viewBox':f'{crop.x0:.3f} {crop.y0:.3f} {crop.width:.3f} {crop.height:.3f}','data-column':f'{page.rect.width/2:.3f}','aria-label':f'Selectable textbook excerpt, chapter {chapter}, PDF page {piece["page"]}'})
        raw=ET.tostring(root,encoding='unicode')
        # Inline SVGs share the document ID namespace. Prefix every retained ID.
        prefix=f'rv-{chapter}-{number}-'
        ids=re.findall(r'\bid="([^"]+)"',raw)
        for value in sorted(ids,key=len,reverse=True):
            raw=raw.replace(f'id="{value}"',f'id="{prefix}{value}"').replace(f'url(#{value})',f'url(#{prefix}{value})').replace(f'href="#{value}"',f'href="#{prefix}{value}"')
        # Source fonts are embedded once in the page, never fetched from a CDN.
        assert '<use data-text=' not in raw and '�' not in raw
        fractions=self.fractions(page,crop,glyph_records)
        root_data={'page':piece['page'],'fractions':fractions}
        raw=raw.replace('class="regenerated-page"','class="regenerated-page" data-copy-layout="'+html.escape(json.dumps(root_data,separators=(',',':')),quote=True)+'"',1)
        self.audit.append({'chapter':chapter,'page':piece['page'],'glyphs':count,'crop':piece['crop']})
        return raw

    def fractions(self,page,crop,glyphs):
        result=[]
        for drawing in page.get_drawings():
            if drawing['width'] is None or drawing['width']>1.1:continue
            for item in drawing['items']:
                if item[0]!='l':continue
                a,b=item[1:]
                x0,x1=sorted((a.x,b.x));y=(a.y+b.y)/2
                if abs(a.y-b.y)>0.15 or not 3<x1-x0<130 or not crop.contains(a) or not crop.contains(b):continue
                aligned=[g for g in glyphs if g['text'].strip() and g['x']>=x0-1 and g['end']<=x1+1]
                above=[g for g in aligned if 0.3<y-g['y']<max(14,g['size']*1.6)]
                below=[g for g in aligned if 1<g['y']-y<max(16,g['size']*1.9)]
                if not above or not below:continue
                upper=max(g['y'] for g in above);lower=min(g['y'] for g in below)
                above=[g for g in above if upper-g['y']<4.8]
                below=[g for g in below if g['y']-lower<4.8]
                if len(above)>40 or len(below)>40:continue
                size=max(g['size'] for g in above+below)
                # A bar should closely cover its numerator and denominator, unlike
                # plot axes, table dividers, or decorative rules.
                content_width=max(g['end'] for g in above+below)-min(g['x'] for g in above+below)
                if not 0<=x1-x0-content_width<size*1.8:continue
                result.append({'above':[g['id'] for g in above],'below':[g['id'] for g in below],'x':x0,'end':x1,'y':y+size*0.325,'size':size})
        return result

    def font_css(self):
        output=[]
        for i,record in enumerate(self.fonts):
            glyphs=record['glyphs']
            builder=FontBuilder(1000,isTTF=False)
            names=['.notdef']+[f'g{code:x}' for code in sorted(glyphs)]
            builder.setupGlyphOrder(names)
            builder.setupCharacterMap({code:f'g{code:x}' for code in glyphs})
            charstrings={}
            pen=T2CharStringPen(500,None);charstrings['.notdef']=pen.getCharString()
            metrics={'.notdef':(500,0)}
            for code,record in glyphs.items():
                name=f'g{code:x}'
                width=max(0,min(3000,round(record['width'])))
                pen=T2CharStringPen(width,None)
                if record['path']:
                    parse_path(record['path'],TransformPen(pen,(1000,0,0,1000,0,0)))
                charstrings[name]=pen.getCharString()
                metrics[name]=(width,0)
            builder.setupHorizontalMetrics(metrics)
            builder.setupHorizontalHeader(ascent=1100,descent=-400)
            family=f'PdfText{i}'
            builder.setupNameTable({'familyName':family,'styleName':'Regular','uniqueFontIdentifier':family,'fullName':family,'psName':family})
            builder.setupOS2(sTypoAscender=1100,sTypoDescender=-400,usWinAscent=1600,usWinDescent=600)
            builder.setupPost()
            builder.setupCFF(family,{'FullName':family,'FamilyName':family,'Weight':'Regular'},charstrings,{})
            builder.font['head'].created=builder.font['head'].modified=2082844800
            buffer=io.BytesIO();builder.font.flavor='woff2';builder.font.save(buffer)
            encoded=base64.b64encode(buffer.getvalue()).decode()
            output.append(f'@font-face{{font-family:{family};src:url(data:font/woff2;base64,{encoded}) format("woff2");font-weight:normal;font-style:normal;font-display:block}}')
        return '\n'.join(output)
