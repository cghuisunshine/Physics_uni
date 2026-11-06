"""Original, offline scientific illustrations for the formula explanations.

All geometry is authored here. Curves are sampled from their stated functions;
schematics are explicitly described as such. The registry assigns every topic
deliberately, rather than inferring a picture from keywords.
"""
from dataclasses import dataclass
from html import escape
import math
from pathlib import Path

GREEN = '#235c4e'
BLUE = '#286a9a'
ORANGE = '#bd661e'
MUTED = '#66756f'
INK = '#193d37'
PALE = '#e9f1e5'
LIGHT = '#edf4fa'


class Scene:
    def __init__(self):
        self.parts = []

    def add(self, markup):
        self.parts.append(markup)

    def line(self,x1,y1,x2,y2,color=INK,width=2,dash='',arrow=False,id=''):
        attrs = f' stroke-dasharray="{dash}"' if dash else ''
        attrs += f' marker-end="url(#head-{color[1:]})"' if arrow else ''
        attrs += f' id="{id}"' if id else ''
        self.add(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" stroke-width="{width}"{attrs}/>')

    def arrow(self,x1,y1,x2,y2,color=GREEN,id=''):
        self.line(x1,y1,x2,y2,color,3,arrow=True,id=id)

    def rect(self,x,y,w,h,fill='none',stroke=INK,dash='',radius=0):
        extra = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"{extra}/>')

    def circle(self,x,y,r,fill='none',stroke=INK,width=2):
        self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def text(self,x,y,text,color=INK,size=22,anchor='start'):
        self.add(f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}">{escape(text)}</text>')

    def path(self,d,color=GREEN,width=3,fill='none',dash='',id=''):
        extra = f' stroke-dasharray="{dash}"' if dash else ''
        extra += f' id="{id}"' if id else ''
        self.add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"{extra}/>')

    def points(self,points,color=GREEN,width=3,fill='none',id=''):
        d = 'M'+' L'.join(f'{x:.3f},{y:.3f}' for x,y in points)
        self.path(d,color,width,fill,id=id)

    def axes(self,x=75,y=270,w=380,h=210,xlabel='t',ylabel=''):
        self.arrow(x,y,x+w,y,MUTED)
        self.arrow(x,y,x,y-h,MUTED)
        self.text(x+w+10,y+7,xlabel,MUTED)
        if ylabel:self.text(x-12,y-h-16,ylabel,MUTED)

    def dot(self,x,y,label='',color=GREEN,r=8):
        self.circle(x,y,r,color,color)
        if label:self.text(x,y-17,label,color,anchor='middle')

    def spring(self,x1,x2,y,amplitude=12):
        pts=[(x1,y),(x1+12,y)]
        for i in range(12):pts.append((x1+20+(x2-x1-40)*i/11,y+amplitude*(-1 if i%2 else 1)))
        pts += [(x2-12,y),(x2,y)]
        self.points(pts,MUTED,2)

    def wave(self,x1,x2,y,amp=15,cycles=3,color=BLUE,decay=0,phase=0):
        pts=[]
        for i in range(121):
            u=i/120
            pts.append((x1+(x2-x1)*u,y-amp*math.exp(-decay*u)*math.sin(2*math.pi*cycles*u+phase)))
        self.points(pts,color)


def draw_units(s,mode):
    if mode=='density':
        for k,n in enumerate([4,12]):
            x=75+k*245
            s.rect(x,95,125,125,LIGHT if k==0 else PALE)
            for i in range(n):s.dot(x+25+(i%4)*25,125+(i//4)*32,r=6)
            s.text(x+62,265,'Same volume',anchor='middle')
            s.text(x+62,65,'Less mass' if k==0 else 'More mass',anchor='middle')
        return
    for y,label in [(100,'1 m'),(215,'100 cm')]:
        s.line(75,y,445,y,INK,3)
        for i in range(11):s.line(75+i*37,y-10,75+i*37,y+10,INK)
        s.text(260,y-30,label,anchor='middle')
    s.arrow(260,125,260,166,BLUE)
    s.text(260,292,'Same length · different unit',anchor='middle')


def draw_motion(s,mode):
    if mode in ['acceleration','integrals','spring-area']:
        s.axes(xlabel='t' if mode!='spring-area' else 'x',ylabel='v' if mode=='acceleration' else ('F' if mode=='spring-area' else 'rate'))
        start_y=210 if mode=='acceleration' else 270
        s.points([(75,270),(430,270),(430,90),(75,start_y),(75,270)],GREEN,1,PALE)
        s.line(75,start_y,430,90,GREEN,3)
        if mode=='acceleration':s.text(41,216,'v₀',GREEN,size=20)
        if mode=='integrals':
            for i in range(6):
                x=75+i*355/6; h=(i+1)*180/6
                s.rect(x,270-h,355/6,h,'none','#a5b49f')
        s.text(260,240,'area = accumulated change',size=21,anchor='middle')
        s.line(430,280,430,293,MUTED)
        s.text(430,319,'x' if mode=='spring-area' else 't',MUTED,anchor='middle')
        return
    if mode=='rates':
        s.axes(xlabel='t',ylabel='x')
        pts=[(75+355*u,260-170*u*u) for u in [i/100 for i in range(101)]]
        s.points(pts)
        x0,y0=280,260-170*(205/355)**2
        slope=-340*(205/355)/355
        s.line(150,y0+slope*(150-x0),410,y0+slope*(410-x0),ORANGE,3,id='tangent')
        s.dot(x0,y0,color=ORANGE)
        s.text(175,95,'tangent slope',ORANGE)
        s.text(300,155,'velocity',ORANGE)
        return
    s.line(60,205,465,205,MUTED)
    for x,label in [(100,'x₀'),(300,'x₁')]:
        s.dot(x,205,label)
        s.line(x,212,x,225,MUTED)
    s.arrow(110,255,300,255,ORANGE)
    s.text(200,293,'displacement',ORANGE,anchor='middle')
    s.text(260,85,'Change of position',anchor='middle')


def draw_vectors(s,mode):
    if mode=='products':
        s.path('M100 265 L300 265 L450 135 L250 135 Z',BLUE,1,LIGHT)
        s.arrow(100,265,250,135,GREEN,id='vector-a')
        s.arrow(100,265,300,265,ORANGE)
        s.line(250,135,250,265,MUTED,2,'6 5')
        s.text(165,175,'a',GREEN)
        s.text(285,295,'b',ORANGE)
        s.text(260,65,'Dot: parallel projection',anchor='middle')
        s.text(260,335,'Cross: parallelogram area',size=21,anchor='middle')
        return
    s.axes(100,265,340,205,'x','y')
    s.arrow(100,265,350,100,GREEN,id='vector-a')
    s.line(350,100,350,265,BLUE,2,'6 5')
    s.line(100,100,350,100,BLUE,2,'6 5')
    s.text(228,300,'aₓ',BLUE,anchor='middle')
    s.text(373,190,'aᵧ',BLUE)
    s.text(215,155,'a',GREEN)
    if mode=='products':
        s.arrow(100,265,350,265,ORANGE)
        s.text(295,245,'b',ORANGE)
        s.text(95,55,'dot: parallel part',anchor='start')
        s.text(165,335,'cross: perpendicular area',size=21)
        s.path('M100 265 L350 265 L350 100 Z',BLUE,1,LIGHT)
        s.arrow(100,265,350,100,GREEN)
    else:
        s.path('M150 265 A50 50 0 0 0 142 237',MUTED,2)
        s.text(165,250,'θ',MUTED)


def draw_projectile(s,mode):
    s.line(50,270,475,270,MUTED)
    pts=[(80+340*u,270-560*u*(1-u)) for u in [i/100 for i in range(101)]]
    s.points(pts,ORANGE)
    for u in [0,.25,.5,.75,1]:s.dot(80+340*u,270-560*u*(1-u),r=6,color=ORANGE)
    s.arrow(80,270,145,163,GREEN)
    s.arrow(250,130,330,130,GREEN)
    s.arrow(250,130,250,215,BLUE)
    s.text(110,150,'v₀',GREEN)
    s.text(345,135,'vₓ',GREEN)
    s.text(265,205,'g',BLUE)
    s.line(80,308,420,308,MUTED,2)
    s.text(250,338,'equal-height range R',anchor='middle')
    s.text(250,65,'Horizontal motion + vertical fall',size=22,anchor='middle')


def draw_circle(s,mode):
    if mode=='velocity-change':
        s.arrow(110,255,335,255,ORANGE)
        x2,y2=110+225*math.cos(math.pi/6),255-225*math.sin(math.pi/6)
        s.arrow(110,255,x2,y2,ORANGE)
        s.arrow(335,255,x2,y2,GREEN)
        s.text(245,290,'v₁',ORANGE)
        s.text(180,155,'v₂',ORANGE)
        s.text(345,190,'Δv',GREEN)
        s.text(260,70,'Same speed · different direction',size=22,anchor='middle')
        return
    s.circle(250,180,105,'none','#a0b39a')
    s.dot(250,180,'centre',MUTED,4)
    s.dot(355,180,r=10)
    s.arrow(355,180,355,75,ORANGE,id='velocity')
    s.arrow(355,180,265,180,GREEN,id='acceleration')
    s.text(374,100,'v',ORANGE)
    s.text(300,158,'aᵣ',GREEN)
    s.line(250,183,355,183,MUTED,2,'5 5')
    s.text(295,218,'r',MUTED)
    s.text(260,327,'Acceleration points inward',anchor='middle')


def draw_forces(s,mode):
    if mode in ['incline','friction','rolling']:
        # Tangent direction down the plane is (+.866,+.5) in screen coordinates.
        s.line(65,140,450,362,MUTED,3)
        if mode=='rolling':
            cx,cy,r=245,184,50
            s.circle(cx,cy,r,PALE)
            s.line(cx-r,cy,cx+r,cy,GREEN)
            s.arrow(cx,cy,cx+95*.866,cy+95*.5,ORANGE)
            s.text(351,226,'vcm',ORANGE)
            s.dot(220,227,'contact',BLUE,5)
            s.text(90,65,'Translation + rotation',anchor='start')
            s.text(337,134,'ω',GREEN)
            s.path('M265 145 A44 44 0 0 1 285 200',GREEN,3)
            return
        s.add('<g transform="translate(245 198) rotate(30)"><rect x="-40" y="-30" width="80" height="60" fill="#e9f1e5" stroke="#193d37" stroke-width="2"/></g>')
        s.arrow(245,198,245,305,BLUE,id='weight')
        s.arrow(245,198,297,108,GREEN,id='normal')
        s.text(307,106,'N',GREEN)
        s.text(260,303,'mg',BLUE)
        s.arrow(245,198,323,243,ORANGE)
        s.text(335,256,'mg sin θ',ORANGE,size=21)
        if mode=='friction':
            s.arrow(245,198,167,153,GREEN)
            s.text(88,135,'friction',GREEN)
        s.text(260,50,'Resolve weight along the slope',anchor='middle')
        return
    s.line(60,255,460,255,MUTED,3)
    s.rect(210,155,95,95,PALE)
    s.arrow(260,200,420,200,GREEN,id='applied-force')
    s.arrow(260,200,180,200,ORANGE,id='friction-force')
    s.arrow(260,200,260,75,BLUE)
    s.arrow(260,200,260,325,BLUE)
    s.text(370,179,'pull',GREEN)
    s.text(90,225,'friction',ORANGE)
    s.text(280,88,'N',BLUE)
    s.text(280,322,'mg',BLUE)


def draw_drag(s,mode):
    for x,balanced in [(140,False),(390,True)]:
        s.dot(x,165,r=19)
        s.arrow(x,165,x,280,BLUE)
        s.arrow(x,165,x,50 if balanced else 120,ORANGE)
        s.text(x+18,275,'mg',BLUE)
        s.text(x+18,105,'drag',ORANGE)
        s.text(x,30,'Balanced' if balanced else 'Speed grows',anchor='middle')
        s.text(x,323,'a = 0' if balanced else 'a downward',anchor='middle')


def draw_work(s,mode):
    if mode=='spring':
        s.line(75,80,75,250,MUTED,4)
        s.spring(75,300,170)
        s.rect(300,135,65,70,PALE)
        s.line(200,95,200,245,MUTED,2,'5 5')
        s.arrow(330,170,255,170,GREEN)
        s.text(290,118,'spring force',GREEN,size=21,anchor='middle')
        s.arrow(200,270,332,270,ORANGE)
        s.text(266,307,'extension x',ORANGE,anchor='middle')
        s.text(145,65,'relaxed end',MUTED,size=21)
        return
    if mode=='potential':
        s.axes(xlabel='x',ylabel='U')
        pts=[(90+350*u,105+145*(1-(2*u-1)**2)) for u in [i/100 for i in range(101)]]
        s.points(pts)
        s.dot(370,105+145*(1-(2*(280/350)-1)**2),color=ORANGE,r=9)
        s.arrow(370,198,300,198,ORANGE)
        s.text(335,171,'force',ORANGE)
        s.text(260,326,'Force points toward lower U',anchor='middle')
        return
    if mode=='mechanical':
        s.line(75,270,450,270,MUTED)
        s.rect(90,95,100,175,LIGHT)
        s.rect(330,95,100,175,PALE)
        s.text(140,192,'U = mgh',BLUE,size=21,anchor='middle')
        s.text(380,192,'K = ½mv²',GREEN,size=21,anchor='middle')
        s.arrow(210,180,305,180,ORANGE)
        s.text(260,58,'Same total mechanical energy',size=22,anchor='middle')
        s.text(140,315,'before',anchor='middle')
        s.text(380,315,'after',anchor='middle')
        return
    s.line(55,245,465,245,MUTED)
    for x in [100,315]:s.rect(x,170,65,70,PALE)
    s.arrow(130,190,240,190,GREEN)
    s.text(194,165,'F',GREEN,anchor='middle')
    s.arrow(125,285,350,285,ORANGE)
    s.text(240,326,'displacement',ORANGE,anchor='middle')
    s.text(260,75,'Force along motion transfers energy',size=21,anchor='middle')


def draw_momentum(s,mode):
    if mode=='com':
        s.line(65,215,455,215,MUTED,3)
        s.dot(90,215,color=BLUE,r=13)
        s.dot(430,215,color=GREEN,r=23)
        s.text(90,175,'1 kg',BLUE,anchor='middle')
        s.text(430,175,'3 kg',GREEN,anchor='middle')
        s.path('M345 219 L326 253 L364 253 Z',ORANGE,2,'#fff0df')
        s.text(345,290,'centre of mass',ORANGE,size=21,anchor='middle')
        s.text(90,138,'x = 0',anchor='middle')
        s.text(430,138,'x = 4 m',anchor='middle')
        s.text(260,65,'The heavier side shifts the balance',size=21,anchor='middle')
        return
    if mode=='rocket':
        s.path('M180 130 L330 130 L380 175 L330 220 L180 220 Z',INK,2,PALE)
        for i in range(4):s.arrow(160-i*25,155+(i%2)*40,95-i*16,155+(i%2)*40,ORANGE)
        s.arrow(320,90,440,90,GREEN)
        s.text(315,65,'rocket gains momentum',size=21,anchor='middle')
        s.text(133,280,'exhaust backward',ORANGE,size=21,anchor='middle')
        return
    for y,label in [(130,'Before'),(275,'After')]:
        s.text(40,y-55,label)
        s.line(70,y+30,465,y+30,MUTED)
    for x,col in [(120,GREEN),(300,BLUE)]:s.rect(x,90,65,65,PALE,col)
    s.arrow(140,65,245,65,GREEN)
    if mode=='elastic':
        s.rect(120,235,65,65,PALE,GREEN)
        s.rect(300,235,65,65,LIGHT,BLUE)
        s.arrow(320,210,420,210,BLUE)
    else:
        s.rect(255,235,65,65,PALE,GREEN)
        s.rect(320,235,65,65,LIGHT,BLUE)
        s.arrow(290,210,355,210,ORANGE)
    s.text(260,345,'Momentum before = momentum after',size=21,anchor='middle')


def draw_rotation(s,mode):
    if mode=='balance':
        s.line(65,175,455,175,INK,6)
        s.path('M260 181 L235 225 L285 225 Z',MUTED,2,PALE)
        s.arrow(90,175,90,80,GREEN)
        s.arrow(430,175,430,80,GREEN)
        s.arrow(260,175,260,300,BLUE)
        s.text(90,58,'support',GREEN,size=21,anchor='middle')
        s.text(430,58,'support',GREEN,size=21,anchor='middle')
        s.text(285,298,'weight',BLUE)
        return
    if mode=='elasticity':
        s.rect(140,120,240,80,PALE)
        s.rect(120,120,280,80,'none',BLUE,'5 5')
        s.arrow(140,160,65,160,GREEN)
        s.arrow(380,160,455,160,GREEN)
        s.line(140,240,380,240,MUTED)
        s.text(260,275,'original length L',anchor='middle')
        s.text(260,75,'pull → small extension',anchor='middle')
        return
    s.circle(250,180,105,PALE,'#a0b39a')
    s.circle(250,180,55,'none','#a0b39a')
    s.dot(250,180,r=5)
    if mode=='parallel-axis':
        s.line(250,50,250,310,GREEN,3,'5 5')
        s.line(345,50,345,310,ORANGE,3,'5 5')
        s.text(237,36,'COM',GREEN,size=21,anchor='middle')
        s.text(365,36,'shifted',ORANGE,size=21,anchor='middle')
        s.arrow(255,330,340,330,MUTED)
        s.text(295,320,'d',MUTED,anchor='middle')
    elif mode=='torque':
        s.arrow(250,180,355,180,MUTED)
        s.arrow(355,180,355,78,ORANGE)
        s.text(305,210,'r',MUTED)
        s.text(378,100,'F',ORANGE)
        s.text(260,327,'A perpendicular force turns the body',size=21,anchor='middle')
    else:
        s.line(250,180,355,180,GREEN,3)
        s.arrow(355,180,355,75,ORANGE)
        s.arrow(305,180,305,125,ORANGE)
        s.text(375,115,'v = ωr',ORANGE,size=21)
        s.text(260,327,'Farther from the axis → greater speed',size=21,anchor='middle')


def draw_orbit(s,mode):
    if mode=='shell':
        s.circle(260,180,120,LIGHT,BLUE)
        s.circle(260,180,67,PALE,GREEN)
        s.arrow(260,180,327,180,GREEN)
        s.arrow(260,180,260,60,BLUE)
        s.text(295,210,'r',GREEN)
        s.text(278,91,'R',BLUE)
        s.text(260,335,'Only the enclosed mass contributes',size=21,anchor='middle')
        return
    s.circle(235,180,105,'none','#a5b49f')
    s.circle(235,180,32,PALE,GREEN)
    s.text(235,187,'M',GREEN,anchor='middle')
    s.dot(340,180,'m',BLUE,r=8)
    s.arrow(340,180,275,180,GREEN)
    s.arrow(340,180,340,80,ORANGE)
    if mode=='escape':
        s.path('M340 180 Q350 60 470 45',ORANGE)
        s.text(405,105,'escape',ORANGE)
    else:s.text(365,90,'v',ORANGE)
    s.text(285,160,'gravity',GREEN,size=21)
    s.text(260,335,'Gravity bends the path',anchor='middle')


def draw_fluid(s,mode):
    if mode=='pipe':
        s.path('M55 100 L190 100 L285 155 L460 155 L460 225 L285 225 L190 280 L55 280 Z',BLUE,2,LIGHT)
        s.arrow(90,190,170,190,GREEN)
        s.arrow(300,190,435,190,ORANGE)
        s.text(125,80,'wide',anchor='middle')
        s.text(370,132,'narrow',anchor='middle')
        s.text(125,320,'slower flow',GREEN,anchor='middle')
        s.text(370,320,'faster flow',ORANGE,anchor='middle')
        return
    s.rect(105,70,290,220,LIGHT,BLUE)
    s.line(105,95,395,95,BLUE,2,'5 5')
    s.rect(205,155,90,75,PALE,GREEN)
    s.arrow(250,225,250,135,GREEN)
    s.text(310,174,'buoyancy',GREEN,size=21)
    for y,length in [(125,25),(185,45),(250,65)]:s.arrow(395,y,395-length,y,BLUE)
    s.line(80,95,80,250,MUTED)
    s.text(57,186,'h',MUTED)
    s.text(260,335,'Pressure increases with depth',anchor='middle')


def draw_oscillation(s,mode):
    if mode in ['pendulum','physical-pendulum','gyroscope']:
        px,py=250,65
        s.dot(px,py,r=5)
        s.line(px,py,px,275,MUTED,2,'5 5')
        bx,by=350,238
        s.line(px,py,bx,by,GREEN,5 if mode=='physical-pendulum' else 2)
        if mode=='gyroscope':
            s.add('<ellipse cx="350" cy="238" rx="55" ry="20" fill="#e9f1e5" stroke="#235c4e" stroke-width="2"/>')
            s.arrow(350,238,300,151.5,ORANGE,id='spin-angular-momentum')
            s.text(282,183,'L',ORANGE)
            s.path('M190 85 C190 35 320 35 320 85',BLUE)
            s.text(155,125,'precession',BLUE,size=21)
        else:s.circle(bx,by,19,PALE,GREEN)
        s.arrow(bx,by,bx,320,BLUE)
        s.text(bx+20,313,'mg',BLUE)
        s.text(310,151,'ℓ' if mode=='pendulum' else 'h',GREEN)
        s.path('M250 125 A60 60 0 0 0 280 117',MUTED,2)
        s.text(280,150,'θ',MUTED)
        if mode!='gyroscope':s.text(260,352,'Weight supplies a restoring torque',size=21,anchor='middle')
        return
    if mode=='damping':
        s.axes(xlabel='t',ylabel='x')
        s.line(75,165,455,165,MUTED,1)
        s.wave(75,435,165,85,4,GREEN,decay=2)
        for sign in [-1,1]:
            s.points([(75+360*u,165+sign*85*math.exp(-2*u)) for u in [i/80 for i in range(81)]],ORANGE,2)
        s.text(280,75,'decaying envelope',ORANGE,size=21,anchor='middle')
        s.text(260,330,'Energy is transferred to the surroundings',size=21,anchor='middle')
        return
    if mode=='torsion':
        s.line(260,50,260,185,MUTED,4)
        s.add('<ellipse cx="260" cy="210" rx="105" ry="42" fill="#e9f1e5" stroke="#235c4e" stroke-width="2"/>')
        s.line(160,210,360,210,GREEN,3)
        s.path('M330 160 A90 40 0 0 1 360 216',ORANGE,3)
        s.text(390,192,'θ',ORANGE)
        s.text(260,310,'Twist → restoring torque',anchor='middle')
        return
    s.line(75,85,75,240,MUTED,4)
    s.spring(75,280,170)
    s.rect(280,135,65,70,PALE)
    s.line(280,100,280,250,MUTED,2,'5 5')
    s.arrow(315,170,240,170,GREEN)
    s.text(260,75,'Force points toward equilibrium',size=21,anchor='middle')
    s.arrow(280,280,370,280,ORANGE)
    s.text(330,320,'x',ORANGE)
    s.text(185,230,'equilibrium',MUTED,size=21)


def draw_waves(s,mode):
    if mode=='sound':
        for i in range(25):
            x=65+16*i+8*math.sin(i*math.pi/6)
            for y in [135,175,215]:s.dot(x,y,r=4,color=BLUE)
        s.arrow(85,280,425,280,GREEN)
        s.text(260,320,'wave travels this way',GREEN,anchor='middle')
        s.arrow(200,85,240,85,ORANGE)
        s.arrow(200,85,160,85,ORANGE)
        s.text(270,65,'particles move back and forth',size=21,anchor='middle')
        return
    if mode=='doppler':
        # Earlier emissions originate farther left; all fronts share one later observation time.
        for i in range(4):s.circle(180+24*i,185,125-30*i,'none',BLUE)
        s.dot(276,185,r=10,color=ORANGE)
        s.arrow(280,185,370,185,ORANGE)
        s.text(130,40,'longer spacing',BLUE,size=21,anchor='middle')
        s.text(390,65,'shorter',BLUE,size=21,anchor='middle')
        s.text(390,90,'spacing',BLUE,size=21,anchor='middle')
        s.text(260,345,'Approaching source → higher frequency',size=21,anchor='middle')
        return
    if mode=='mach':
        sx,sy=440,180
        s.dot(sx,sy,r=8,color=ORANGE)
        s.line(90,80,sx,sy,BLUE,3)
        s.line(90,280,sx,sy,BLUE,3)
        s.circle(155,180,78,'none','#a3bbcb')
        s.arrow(sx,sy,490,sy,ORANGE)
        s.text(245,160,'θ',BLUE)
        s.text(260,330,'A supersonic source outruns its waves',size=21,anchor='middle')
        return
    if mode in ['standing','pipes']:
        s.line(75,175,445,175,MUTED,1)
        s.wave(75,445,175,65,1,GREEN)
        s.wave(75,445,175,-65,1,BLUE)
        for x in [75,260,445]:s.dot(x,175,r=5)
        s.line(75,90,75,260,MUTED,4)
        s.line(445,90,445,260,MUTED,4)
        s.text(75,293,'node',size=21,anchor='middle')
        s.text(260,293,'node',size=21,anchor='middle')
        s.text(445,293,'node',size=21,anchor='middle')
        s.text(260,65,'Two half-wavelengths fit inside L',size=21,anchor='middle')
        s.text(260,340,'Opposite phases of the same standing mode',size=20,anchor='middle')
        return
    if mode=='beats':
        s.line(65,180,460,180,MUTED,1)
        pts=[(65+390*u,180-68*math.cos(3*math.pi*u)*math.cos(36*math.pi*u)) for u in [i/700 for i in range(701)]]
        s.points(pts,GREEN,2)
        s.text(260,75,'A slow envelope around rapid oscillations',size=21,anchor='middle')
        s.text(260,310,'Beat rate = frequency difference',size=21,anchor='middle')
        return
    s.line(60,180,465,180,MUTED,1)
    s.wave(65,455,180,62,2,GREEN)
    s.arrow(180,85,340,85,ORANGE)
    s.text(260,58,'propagation',ORANGE,anchor='middle')
    s.arrow(115,175,115,115,BLUE)
    s.arrow(115,185,115,245,BLUE)
    s.text(260,320,'The medium oscillates; the pattern travels',size=21,anchor='middle')


def draw_gas(s,mode):
    if mode=='collision':
        s.rect(70,80,320,225,'none',MUTED)
        for x,y in [(115,120),(170,245),(215,120),(135,200),(290,260),(285,165)]:s.dot(x,y,r=6,color=BLUE)
        s.dot(330,190,r=10,color=ORANGE)
        s.arrow(280,170,375,170,ORANGE)
        s.arrow(375,215,285,215,BLUE)
        s.line(390,80,390,305,INK,6)
        s.arrow(395,190,465,190,GREEN)
        s.text(440,155,'force',GREEN,anchor='middle')
        s.text(260,47,'Molecules transfer momentum to a wall',size=21,anchor='middle')
        s.text(280,145,'before',ORANGE,size=21,anchor='middle')
        s.text(285,246,'after',BLUE,size=21,anchor='middle')
        return
    if mode in ['piston','adiabatic']:
        for x,w,h,label in [(65,145,130,'initial'),(305,145,190,'expanded')]:
            s.rect(x,85,w,h,LIGHT,BLUE)
            s.line(x,85+h,x+w,85+h,INK,7)
            s.text(x+w/2,60,label,anchor='middle')
            for j in range(6):s.dot(x+30+(j%3)*40,120+(j//3)*(h-65),r=5,color=BLUE)
        s.arrow(232,190,280,190,ORANGE)
        s.text(260,332,'Expansion does work on a piston',size=21,anchor='middle')
        if mode=='adiabatic':s.text(378,310,'cooler',BLUE,anchor='middle')
        else:s.text(125,264,'heat in',ORANGE,anchor='middle')
        return
    if mode=='free-expansion':
        for x,label in [(55,'Before'),(310,'After')]:
            s.rect(x,100,155,145,'none',BLUE)
            s.line(x+77,100,x+77,245,MUTED,2,'5 5')
            s.text(x+77,65,label,anchor='middle')
        for x,y in [(80,125),(108,145),(87,190),(113,215),(75,225),(115,180)]:s.dot(x,y,r=5)
        for x,y in [(330,125),(420,145),(350,190),(433,215),(385,225),(405,180)]:s.dot(x,y,r=5)
        s.arrow(225,175,295,175,ORANGE)
        s.text(260,320,'More accessible positions; entropy rises',size=21,anchor='middle')
        return
    if mode=='equipartition':
        x,y=245,215
        s.dot(x,y,r=12,color=ORANGE)
        s.arrow(x,y,420,y,GREEN)
        s.arrow(x,y,x,65,BLUE)
        s.arrow(x,y,125,295,ORANGE)
        s.text(440,220,'x',GREEN)
        s.text(260,65,'y',BLUE)
        s.text(100,320,'z',ORANGE)
        s.text(270,340,'Three independent quadratic motions',size=21,anchor='middle')
        return
    if mode=='boltzmann':
        s.rect(65,80,250,205,LIGHT,BLUE)
        for i in range(20):s.dot(85+(i%5)*45,105+(i//5)*48,r=4,color=BLUE)
        s.text(190,55,'reservoir',BLUE,anchor='middle')
        s.rect(380,135,85,85,PALE,GREEN)
        s.text(420,112,'system',GREEN,anchor='middle')
        s.arrow(325,163,372,163,ORANGE)
        s.arrow(372,192,325,192,ORANGE)
        s.text(260,335,'Energy exchange changes the state counts',size=21,anchor='middle')
        return
    if mode=='multiplicity':
        for x,label in [(55,'4 left, 0 right'),(310,'2 left, 2 right')]:
            s.rect(x,100,155,140,'none',BLUE)
            s.line(x+77,100,x+77,240,MUTED)
            s.text(x+77,70,label,size=21,anchor='middle')
        for x,y in [(78,135),(105,135),(78,195),(105,195),(335,135),(335,195),(420,135),(420,195)]:s.dot(x,y,r=7)
        s.text(132,285,'1 assignment',anchor='middle')
        s.text(388,285,'6 assignments',anchor='middle')
        s.text(260,345,'Four labelled particles: choose who is left',size=20,anchor='middle')
        return
    s.axes(xlabel='v',ylabel='P(v)')
    pts=[]
    for i in range(151):
        u=i/150*3
        pts.append((75+u/3*355,270-450*u*u*math.exp(-u*u)))
    s.points(pts,GREEN)
    # Distinct speed statistics in units sqrt(2 kT/m).
    for val,label,col,y in [(1,'vp',GREEN,75),(2/math.sqrt(math.pi),'mean',ORANGE,110),(math.sqrt(1.5),'rms',BLUE,145)]:
        x=75+355*val/3
        curve_y=270-450*val*val*math.exp(-val*val)
        s.line(x,curve_y,x,270,col,2,'5 5')
        s.line(325,y-7,350,y-7,col,3)
        s.text(362,y,label,col)
    s.text(260,335,'Most probable < mean < rms speed',size=21,anchor='middle')


def draw_pv(s,mode):
    s.axes(xlabel='V',ylabel='p')
    if mode=='carnot':
        gamma=5/3
        v1,v2=1,2
        ratio=2**(1/(gamma-1)); v3,v4=v2*ratio,v1*ratio
        sx=lambda v:85+v*61
        sy=lambda p:280-p*95
        funcs=[(v1,v2,lambda v:2/v,ORANGE),(v2,v3,lambda v:(2/v2)*(v2/v)**gamma,GREEN),
               (v3,v4,lambda v:1/v,BLUE),(v4,v1,lambda v:(1/v4)*(v4/v)**gamma,GREEN)]
        for a,b,f,col in funcs:
            pts=[(sx(v),sy(f(v))) for v in [a+(b-a)*i/70 for i in range(71)]]
            s.points(pts,col)
            s.arrow(*pts[33],*pts[39],col)
        states=[(v1,2/v1),(v2,2/v2),(v3,1/v3),(v4,1/v4)]
        for i,(v,p) in enumerate(states,1):
            x,y=sx(v),sy(p);s.dot(x,y,r=4)
            s.text(x+(15 if i in [1,3] else -15),y-12,str(i),anchor='middle')
        s.text(300,102,'hot isotherm',ORANGE,size=21)
        s.text(280,335,'cold isotherm',BLUE,size=21)
        s.add('<metadata id="cycle-states">'+escape(str(states))+'</metadata>')
        return
    points=[(90+350*u,285-195/(1+3*u)) for u in [i/120 for i in range(121)]]
    if mode=='isothermal':
        s.points([(90,270)]+points+[(440,270)],ORANGE,1,'#fff0df')
        s.points(points,ORANGE)
        s.text(285,135,'pV constant',ORANGE,size=21)
        s.text(290,240,'work = area',ORANGE,size=21,anchor='middle')
    else:
        s.points(points,ORANGE)
        ad=[(90+350*u,285-195/(1+3*u)**(5/3)) for u in [i/120 for i in range(121)]]
        s.points(ad,BLUE)
        s.text(280,125,'isothermal',ORANGE,size=21)
        s.text(280,240,'adiabatic',BLUE,size=21)
    s.text(260,350,'Schematic pressure–volume paths',size=21,anchor='middle')


def draw_heat(s,mode):
    if mode=='engine' or mode=='refrigerator':
        s.rect(175,35,170,55,'#fff0df',ORANGE)
        s.rect(175,145,170,65,PALE,GREEN)
        s.rect(175,270,170,55,LIGHT,BLUE)
        s.text(260,70,'hot reservoir',ORANGE,size=21,anchor='middle')
        s.text(260,183,'working fluid',GREEN,size=21,anchor='middle')
        s.text(260,305,'cold reservoir',BLUE,size=21,anchor='middle')
        if mode=='engine':
            s.arrow(260,94,260,140,ORANGE)
            s.arrow(260,215,260,265,BLUE)
            s.arrow(350,177,465,177,GREEN)
        else:
            s.arrow(260,140,260,94,ORANGE)
            s.arrow(260,265,260,215,BLUE)
            s.arrow(465,177,350,177,GREEN)
        s.text(280,121,'Qh',ORANGE)
        s.text(280,247,'Qc',BLUE)
        s.text(410,153,'work',GREEN,anchor='middle')
        return
    if mode=='expansion':
        s.rect(95,125,300,70,PALE,GREEN)
        s.rect(70,125,350,70,'none',ORANGE,'5 5')
        s.arrow(95,250,70,250,ORANGE)
        s.arrow(395,250,420,250,ORANGE)
        s.text(260,85,'Heating increases the dimensions',size=21,anchor='middle')
        s.text(260,300,'Small linear changes add in three axes',size=21,anchor='middle')
        return
    s.rect(175,85,175,215,LIGHT,BLUE)
    s.line(175,85,175,300,ORANGE,7)
    s.line(350,85,350,300,BLUE,7)
    s.arrow(200,190,325,190,ORANGE)
    s.text(110,180,'hot',ORANGE,anchor='middle')
    s.text(405,180,'cold',BLUE,anchor='middle')
    s.text(260,340,'Heat flows down the temperature gradient',size=21,anchor='middle')


def draw_charges(s,mode):
    if mode=='dipole':
        s.dot(180,235,'−q',BLUE,18)
        s.dot(300,135,'+q',ORANGE,18)
        s.arrow(185,230,285,147,GREEN)
        s.text(235,166,'p',GREEN)
        for y in [75,295]:s.arrow(65,y,440,y,MUTED)
        s.text(460,80,'E',MUTED)
        s.arrow(300,135,405,135,ORANGE)
        s.arrow(180,235,75,235,BLUE)
        s.text(260,350,'Opposite forces form a turning couple',size=21,anchor='middle')
        return
    for row,sign2,label in [(110,'+','like charges repel'),(265,'−','unlike charges attract')]:
        s.circle(170,row,25,PALE,GREEN);s.text(170,row+8,'+',GREEN,anchor='middle')
        s.circle(350,row,25,LIGHT,BLUE);s.text(350,row+8,sign2,BLUE,anchor='middle')
        if sign2=='+':s.arrow(140,row,70,row,GREEN);s.arrow(380,row,450,row,BLUE)
        else:s.arrow(200,row,260,row,GREEN);s.arrow(320,row,260,row,BLUE)
        s.text(260,row+63,label,size=21,anchor='middle')


def draw_field(s,mode):
    if mode=='ring':
        s.add('<ellipse cx="175" cy="180" rx="40" ry="105" fill="none" stroke="#286a9a" stroke-width="3"/>')
        s.line(65,180,460,180,MUTED,1,'5 5')
        s.dot(390,180,'P',ORANGE,7)
        for y in [85,275]:
            s.dot(175,y,r=5,color=BLUE)
            s.arrow(330,180+(180-y)*.24,390,180,GREEN)
        s.arrow(390,180,475,180,GREEN)
        s.text(428,155,'Eaxis',GREEN,size=21,anchor='middle')
        s.text(260,335,'Transverse components cancel in pairs',size=21,anchor='middle')
        return
    if mode in ['sphere','shell']:
        s.circle(260,185,105,'none',BLUE)
        s.dot(260,185,'Q',ORANGE,12)
        for a in [0,math.pi/4,math.pi/2,3*math.pi/4,math.pi,5*math.pi/4,3*math.pi/2,7*math.pi/4]:
            s.arrow(260+55*math.cos(a),185+55*math.sin(a),260+145*math.cos(a),185+145*math.sin(a),GREEN)
        s.text(260,355,'Same radial field on a concentric sphere',size=21,anchor='middle')
        return
    if mode=='sheet':
        s.rect(245,65,25,225,LIGHT,BLUE)
        for y in [100,175,250]:
            s.text(257,y+6,'+',BLUE,anchor='middle')
            s.arrow(225,y,125,y,GREEN);s.arrow(290,y,390,y,GREEN)
        s.text(260,335,'Equal normal fields on both sides',size=21,anchor='middle')
        return
    s.circle(260,185,15,PALE,GREEN)
    s.text(260,192,'+',GREEN,anchor='middle')
    for a in [i*math.pi/4 for i in range(8)]:
        s.arrow(260+35*math.cos(a),185+35*math.sin(a),260+135*math.cos(a),185+135*math.sin(a),BLUE)
    s.text(260,355,'A positive test charge follows the field',size=21,anchor='middle')


def draw_potential(s,mode):
    if mode=='pairs':
        s.dot(140,180,'+q₁',GREEN,20)
        s.dot(360,180,'−q₂',BLUE,20)
        s.line(160,180,340,180,MUTED,2,'5 5')
        s.text(250,165,'r',MUTED,anchor='middle')
        s.arrow(445,110,380,165,ORANGE)
        s.text(400,85,'bring in charge',ORANGE,size=21,anchor='middle')
        s.text(260,305,'Count each interacting pair once',size=21,anchor='middle')
        return
    for x,label in [(100,'30 V'),(260,'20 V'),(420,'10 V')]:
        s.line(x,90,x,285,BLUE,2,'6 5')
        s.text(x,65,label,BLUE,anchor='middle')
    for y in [125,210,275]:s.arrow(65,y,465,y,GREEN)
    s.dot(185,210,'+q',ORANGE,9)
    s.text(260,335,'Electric field points toward lower potential',size=21,anchor='middle')


def draw_capacitor(s,mode):
    if mode=='spherical':
        for r,col in [(65,GREEN),(125,BLUE)]:s.circle(260,180,r,'none',col,5)
        s.arrow(260,180,325,180,GREEN)
        s.arrow(260,180,260,55,BLUE)
        s.text(298,214,'a',GREEN)
        s.text(278,88,'b',BLUE)
        s.text(260,350,'Integrate the radial field across the gap',size=21,anchor='middle')
        return
    if mode=='cylinder':
        s.add('<ellipse cx="260" cy="180" rx="125" ry="85" fill="#edf4fa" stroke="#286a9a" stroke-width="3"/>')
        s.add('<ellipse cx="260" cy="180" rx="55" ry="38" fill="#e9f1e5" stroke="#235c4e" stroke-width="3"/>')
        s.arrow(260,180,310,180,GREEN)
        s.arrow(260,180,260,98,BLUE)
        s.text(295,210,'a',GREEN)
        s.text(278,120,'b',BLUE)
        s.text(260,320,'Coaxial conductors: charge on facing surfaces',size=20,anchor='middle')
        return
    if mode=='network':
        for y in [120,240]:
            s.line(85,y,240,y,MUTED);s.line(280,y,435,y,MUTED)
            s.line(240,y-30,240,y+30,GREEN,5);s.line(280,y-30,280,y+30,BLUE,5)
        s.line(85,120,85,240,MUTED);s.line(435,120,435,240,MUTED)
        s.text(260,58,'Parallel: the same voltage',anchor='middle')
        s.text(260,320,'The stored charges add',anchor='middle')
        return
    s.rect(170,90,180,195,LIGHT,'none')
    s.line(165,75,165,300,GREEN,6)
    s.line(355,75,355,300,BLUE,6)
    for y in [105,170,235]:
        s.text(135,y,'+',GREEN,anchor='middle')
        s.text(385,y,'−',BLUE,anchor='middle')
        s.arrow(185,y,335,y,ORANGE)
    s.line(170,325,350,325,MUTED)
    s.text(260,355,'gap d',MUTED,anchor='middle')
    s.text(260,48,'Uniform field between wide plates',size=21,anchor='middle')


def draw_current(s,mode):
    s.rect(65,120,390,115,LIGHT,BLUE)
    for i in range(7):
        x=95+50*i
        s.circle(x,175,9,PALE,GREEN)
        s.text(x,181,'−',GREEN,size=20,anchor='middle')
        s.arrow(x+15,210,x-15,210,GREEN)
    s.arrow(120,80,400,80,ORANGE)
    s.text(260,52,'conventional current I',ORANGE,anchor='middle')
    if mode=='flux':
        s.add('<ellipse cx="275" cy="178" rx="25" ry="58" fill="none" stroke="#bd661e" stroke-width="3"/>')
        s.text(300,280,'area A',ORANGE)
    elif mode=='resistance':
        for i in range(4):s.dot(145+i*75,145,r=4,color=MUTED)
        s.text(260,285,'Length L and cross section A matter',size=21,anchor='middle')
    else:s.text(260,285,'Electrons drift opposite to I',size=21,anchor='middle')
    if mode=='drude':s.text(260,330,'Field acceleration + momentum relaxation',size=20,anchor='middle')


def resistor(s,x,y,w=80):
    s.line(x,y,x+10,y,MUTED)
    pts=[(x+10,y)]
    for i in range(8):pts.append((x+15+(w-30)*i/7,y+(-10 if i%2 else 10)))
    pts.extend([(x+w-10,y),(x+w,y)])
    s.points(pts,MUTED,2)


def draw_circuit(s,mode):
    if mode=='junction':
        s.dot(250,180,r=7)
        s.arrow(70,180,240,180,GREEN)
        s.arrow(255,175,405,90,BLUE)
        s.arrow(255,185,405,270,ORANGE)
        s.text(140,155,'I in',GREEN)
        s.text(365,65,'I₁',BLUE)
        s.text(365,310,'I₂',ORANGE)
        s.text(260,350,'No charge accumulates at the junction',size=21,anchor='middle')
        return
    if mode=='transformer':
        s.rect(205,75,110,215,PALE,MUTED)
        for x,col in [(175,BLUE),(345,ORANGE)]:
            for i in range(5):s.add(f'<ellipse cx="{x}" cy="{108+i*35}" rx="36" ry="18" fill="none" stroke="{col}" stroke-width="2"/>')
        s.text(100,65,'primary',BLUE,anchor='middle')
        s.text(422,65,'secondary',ORANGE,anchor='middle')
        s.text(125,175,'Np',BLUE,anchor='middle')
        s.text(395,175,'Ns',ORANGE,anchor='middle')
        s.text(260,340,'A common changing flux links both coils',size=21,anchor='middle')
        return
    s.line(100,90,210,90,MUTED)
    if mode=='lc':s.line(210,90,310,90,MUTED)
    else:resistor(s,210,90,100)
    s.line(310,90,420,90,MUTED)
    s.line(420,90,420,160,MUTED)
    s.line(420,240,420,290,MUTED)
    if mode=='rlc':
        s.line(420,290,292,290,MUTED)
        s.line(228,290,100,290,MUTED)
        s.circle(260,290,32,'none',ORANGE)
        s.wave(238,282,290,12,1,ORANGE)
    else:s.line(420,290,100,290,MUTED)
    s.line(100,90,100,160,MUTED)
    s.line(100,220,100,290,MUTED)
    if mode!='lc':s.text(260,60,'R',anchor='middle')
    if mode in ['rc','rc-discharge','lc','rlc']:
        s.line(385,178,455,178,BLUE,5)
        s.line(385,208,455,208,BLUE,5)
        s.line(420,160,420,178,MUTED)
        s.line(420,208,420,240,MUTED)
        s.text(465,199,'C',BLUE)
    else:
        s.line(420,160,420,240,MUTED)
    if mode in ['lc','rl','rlc']:
        s.path('M100 160 C125 160 125 175 100 175 C125 175 125 190 100 190 C125 190 125 205 100 205 C125 205 125 220 100 220',GREEN,3)
        s.text(65,199,'L',GREEN)
        if mode=='lc':s.text(260,340,'Electric ↔ magnetic energy',size=21,anchor='middle')
        else:s.text(260,360,'Inductance opposes current changes',size=21,anchor='middle')
    elif mode=='rc-discharge':
        s.line(100,160,100,220,MUTED)
        s.text(260,340,'Stored charge drives the current',size=21,anchor='middle')
    else:
        s.line(70,176,130,176,ORANGE,4)
        s.line(83,200,117,200,ORANGE,4)
        s.line(100,160,100,176,MUTED)
        s.line(100,200,100,220,MUTED)
        s.text(45,194,'+',ORANGE)
        s.text(260,340,'Loop voltage rises and drops balance',size=21,anchor='middle')
    s.arrow(320,125,380,125,ORANGE)
    s.text(350,153,'I',ORANGE,anchor='middle')


def draw_magnet(s,mode):
    if mode=='orbit':
        for x in range(90,460,65):
            for y in range(70,310,60):
                s.line(x-5,y-5,x+5,y+5,MUTED,1)
                s.line(x-5,y+5,x+5,y-5,MUTED,1)
        s.circle(250,180,95,'none',GREEN)
        s.dot(345,180,'+q',ORANGE,9)
        s.arrow(345,180,345,85,ORANGE,id='magnetic-velocity')
        s.arrow(345,180,260,180,GREEN,id='magnetic-force')
        s.text(365,105,'v',ORANGE)
        s.text(285,164,'F',GREEN)
        s.text(260,345,'× means B into the page',size=21,anchor='middle')
        return
    if mode=='ampere':
        s.circle(260,180,20,PALE,GREEN)
        s.dot(260,180,r=5)
        s.circle(260,180,105,'none',BLUE)
        s.arrow(365,190,365,140,BLUE)
        s.arrow(155,170,155,220,BLUE)
        s.text(390,156,'B',BLUE)
        s.text(260,75,'I out of page',GREEN,anchor='middle')
        s.text(260,340,'Field lines circle the current',size=21,anchor='middle')
        return
    if mode in ['solenoid','energy','displacement']:
        for x in range(110,425,35):
            s.dot(x,125,r=4,color=ORANGE)
            s.line(x-4,235-4,x+4,235+4,ORANGE,2)
            s.line(x-4,235+4,x+4,235-4,ORANGE,2)
        s.arrow(90,180,440,180,GREEN)
        s.text(260,75,'Many turns reinforce the inside field',size=21,anchor='middle')
        s.text(260,295,'• toward you     × away from you',size=21,anchor='middle')
        s.text(260,340,'magnetic field B',GREEN,anchor='middle')
        return
    if mode=='faraday':
        s.rect(60,140,165,75,PALE,GREEN)
        s.line(142,140,142,215,GREEN)
        s.text(100,186,'S',GREEN,anchor='middle')
        s.text(185,186,'N',GREEN,anchor='middle')
        s.add('<ellipse cx="380" cy="180" rx="38" ry="95" fill="none" stroke="#286a9a" stroke-width="4"/>')
        s.arrow(150,100,260,100,ORANGE)
        s.text(205,75,'motion',ORANGE,anchor='middle')
        s.arrow(425,180,315,180,BLUE)
        s.text(380,305,'induced field',BLUE,size=21,anchor='middle')
        s.text(260,350,'The induced field opposes the flux increase',size=20,anchor='middle')
        return
    if mode=='wire':
        s.line(75,200,440,200,GREEN,7)
        s.arrow(110,200,260,200,ORANGE)
        s.arrow(285,200,285,80,BLUE)
        s.text(190,233,'I',ORANGE)
        s.text(305,100,'force',BLUE,size=21)
        for x in [120,210,360,440]:
            for y in [120,280]:
                s.line(x-5,y-5,x+5,y+5,MUTED)
                s.line(x-5,y+5,x+5,y-5,MUTED)
        s.text(260,340,'I right, B into page → force upward',size=21,anchor='middle')
        return
    # A cross section of a current loop makes its axial dipole moment visible.
    s.add('<ellipse cx="250" cy="200" rx="115" ry="55" fill="#e9f1e5" stroke="#235c4e" stroke-width="3"/>')
    s.arrow(250,200,250,60,ORANGE)
    s.text(275,75,'μ',ORANGE)
    s.path('M145 179 A115 55 0 0 1 335 164',BLUE,3)
    s.text(385,210,'current',BLUE,size=21)
    s.text(260,330,'A current loop behaves as a magnetic dipole',size=20,anchor='middle')


def draw_em(s,mode):
    if mode=='pressure':
        s.rect(370,75,28,220,PALE,GREEN)
        for y in [120,185,250]:
            s.wave(65,220,y,8,3,ORANGE)
            s.arrow(240,y,355,y,ORANGE)
        s.arrow(405,180,470,180,GREEN)
        s.text(440,150,'force',GREEN,size=21,anchor='middle')
        s.text(260,335,'Stopping light transfers its momentum',size=21,anchor='middle')
        return
    if mode=='displacement':
        s.line(60,180,185,180,ORANGE,3)
        s.line(335,180,460,180,ORANGE,3)
        s.line(185,95,185,270,BLUE,5)
        s.line(335,95,335,270,BLUE,5)
        for y in [130,180,230]:s.arrow(202,y,318,y,GREEN)
        s.arrow(80,180,150,180,ORANGE)
        s.text(100,150,'I',ORANGE)
        s.text(260,75,'changing E',GREEN,anchor='middle')
        s.text(260,330,'No carriers cross the insulating gap',size=21,anchor='middle')
        return
    s.line(55,190,465,190,MUTED,1)
    s.wave(65,450,190,75,1.5,GREEN)
    for u in [.12,.45,.78]:
        x=65+385*u; val=math.sin(3*math.pi*u)
        if val>0:s.circle(x,190,7,BLUE,BLUE)
        else:
            s.line(x-6,184,x+6,196,BLUE,2);s.line(x-6,196,x+6,184,BLUE,2)
    s.arrow(180,75,355,75,ORANGE)
    s.text(270,52,'propagation',ORANGE,anchor='middle')
    s.text(93,122,'E',GREEN)
    s.text(260,300,'B: • out     × in',BLUE,anchor='middle')
    s.text(260,345,'E and B are perpendicular and in phase',size=21,anchor='middle')


def draw_optics(s,mode):
    if mode=='refraction':
        s.rect(50,180,420,145,LIGHT,'none')
        s.line(50,180,470,180,BLUE)
        s.line(260,65,260,320,MUTED,2,'5 5')
        s.arrow(155,55,260,180,ORANGE)
        theta2=math.asin(math.sin(math.radians(40))/1.5)
        s.arrow(260,180,260+135*math.sin(theta2),180+135*math.cos(theta2),GREEN)
        s.text(70,145,'n₁',ORANGE)
        s.text(70,250,'n₂ > n₁',GREEN)
        s.text(285,117,'normal',MUTED,size=21)
        s.text(260,355,'Entering a higher index bends toward normal',size=20,anchor='middle')
        return
    if mode=='polarization':
        s.arrow(90,235,90,95,ORANGE)
        s.arrow(90,165,200,165,MUTED)
        s.rect(230,75,70,210,LIGHT,BLUE)
        s.line(230,240,300,120,BLUE,4)
        s.arrow(330,165,440,165,MUTED)
        s.arrow(385,215,438,123,GREEN)
        s.text(95,65,'incident E',ORANGE,size=21,anchor='middle')
        s.text(260,325,'Only the component along the axis passes',size=21,anchor='middle')
        return
    if mode=='mirror':
        s.line(55,180,455,180,MUTED,1)
        s.path('M375 70 Q425 180 375 290',BLUE,4)
        s.arrow(100,180,100,100,GREEN)
        s.arrow(268,180,268,212,ORANGE)
        s.points([(100,100),(380,100),(268,212)],ORANGE,2)
        s.points([(100,100),(380,180),(268,212)],GREEN,2)
        s.dot(300,180,'F',BLUE,4)
        s.text(110,70,'object',GREEN,size=21)
        s.text(215,260,'image',ORANGE,size=21)
        return
    # Real-image thin lens: do=190, f=90, di=171, image height=-72.
    y=180
    s.line(45,y,480,y,MUTED,1)
    s.add('<ellipse cx="270" cy="180" rx="16" ry="120" fill="#edf4fa" stroke="#286a9a" stroke-width="2"/>')
    s.arrow(80,y,80,100,GREEN)
    s.arrow(441,y,441,252,ORANGE)
    s.points([(80,100),(270,100),(441,252)],ORANGE,2,id='lens-ray-parallel')
    s.points([(80,100),(270,180),(441,252)],GREEN,2,id='lens-ray-central')
    s.dot(360,180,'F',BLUE,4)
    s.text(80,75,'object',GREEN,size=21,anchor='middle')
    s.text(425,295,'image',ORANGE,size=21,anchor='middle')
    s.text(260,350,'The rays meet at the same image point',size=21,anchor='middle')


def draw_interference(s,mode):
    if mode=='film':
        s.rect(65,125,390,110,LIGHT,BLUE)
        s.line(65,125,455,125,BLUE,3);s.line(65,235,455,235,BLUE,3)
        s.arrow(135,45,200,125,ORANGE)
        s.arrow(200,125,265,45,ORANGE)
        s.points([(200,125),(265,235),(330,125)],GREEN)
        s.arrow(330,125,395,45,GREEN)
        s.text(113,105,'air',MUTED)
        s.text(110,185,'film n',BLUE)
        s.text(110,280,'air',MUTED)
        s.line(430,135,430,225,MUTED)
        s.text(446,190,'t',MUTED)
        s.text(260,340,'Compare optical path AND reflection phase',size=20,anchor='middle')
        return
    xslit,screen=155,425
    s.line(xslit,60,xslit,300,INK,9)
    if mode=='grating':centres=list(range(95,280,30))
    elif mode=='single':centres=[180]
    else:centres=[135,225]
    for cy in centres:s.line(xslit,cy-12,xslit,cy+12,'#fff',12)
    for cy in centres:
        s.line(xslit,cy,screen,115,ORANGE,1.7)
        s.line(xslit,cy,screen,245,BLUE,1.7)
    s.line(screen,55,screen,305,MUTED,3)
    # Screen luminance is computed from the interference/diffraction envelope.
    for i in range(100):
        yy=65+i*2.3; u=(yy-180)/28
        sinc=1 if abs(u)<1e-9 else (math.sin(u)/u)**2
        q=u*2.2
        grating=1 if abs(math.sin(q))<1e-9 else (math.sin(len(centres)*q)/(len(centres)*math.sin(q)))**2
        value=sinc if mode=='single' else (grating if mode=='grating' else math.cos(q)**2)
        shade=int(255-180*value)
        s.rect(440,yy,18,2.5,f'rgb({shade},{shade},{shade})','none')
    s.text(145,335,'slit' if mode=='single' else ('many slits' if mode=='grating' else 'two slits'),anchor='middle')
    s.text(420,335,'screen',anchor='middle')
    s.text(260,35,'Path differences create bright and dark bands',size=20,anchor='middle')


def draw_bragg(s,mode):
    if mode=='aperture':
        s.circle(150,180,75,PALE,GREEN)
        for r in [18,40,61,82]:s.circle(380,180,r,'none',BLUE,5 if r==18 else 2)
        s.circle(380,180,17,BLUE,BLUE)
        s.text(150,295,'aperture',GREEN,anchor='middle')
        s.text(380,295,'Airy pattern',BLUE,size=21,anchor='middle')
        s.text(260,65,'A circular opening spreads the wave',size=21,anchor='middle')
        return
    for y in [145,235]:
        s.line(70,y,460,y,MUTED)
        for x in range(85,455,45):s.dot(x,y,r=5,color=BLUE)
    s.arrow(135,50,250,145,ORANGE)
    s.arrow(250,145,365,50,ORANGE)
    s.points([(135,140),(250,235),(365,140)],GREEN)
    s.line(430,145,430,235,BLUE)
    s.text(450,198,'d',BLUE)
    s.text(260,320,'Extra travel: one leg in and one leg out',size=21,anchor='middle')


def draw_relativity(s,mode):
    if mode=='energy':
        s.points([(115,275),(415,275),(415,95),(115,275)],MUTED,2)
        s.text(260,312,'pc',GREEN,anchor='middle')
        s.text(440,195,'mc²',BLUE,anchor='middle')
        s.text(260,160,'E',ORANGE,anchor='middle')
        s.text(260,65,'Total energy is the hypotenuse',size=21,anchor='middle')
        return
    if mode=='lorentz':
        s.axes(250,290,210,235,'x','ct')
        s.line(250,290,65,105,MUTED,1,'5 5')
        s.line(250,290,435,105,MUTED,1,'5 5')
        s.arrow(250,290,355,80,GREEN)
        s.arrow(250,290,450,190,ORANGE)
        s.text(368,83,'ct′',GREEN)
        s.text(457,180,'x′',ORANGE)
        s.text(260,345,'Different frames slice spacetime differently',size=20,anchor='middle')
        return
    if mode=='doppler':
        s.wave(65,250,180,38,3,BLUE)
        s.wave(285,470,180,38,1.5,ORANGE)
        s.text(155,95,'emitted',BLUE,anchor='middle')
        s.text(375,95,'redshifted',ORANGE,anchor='middle')
        s.arrow(165,275,370,275,MUTED)
        s.text(260,320,'Source and detector move apart',size=21,anchor='middle')
        return
    # A transverse light clock, first at rest and then moving sideways.
    for x in [120,350]:
        s.line(x-55,100,x+55,100,BLUE,5)
        s.line(x-55,275,x+55,275,BLUE,5)
    s.arrow(120,270,120,105,ORANGE)
    s.points([(300,275),(350,100),(400,275)],ORANGE,3)
    s.arrow(300,305,400,305,GREEN)
    s.text(120,65,'at rest',anchor='middle')
    s.text(350,65,'moving',anchor='middle')
    s.text(260,350,'Light keeps speed c; the diagonal takes longer',size=20,anchor='middle')


def draw_quantum(s,mode):
    if mode=='photon':
        s.rect(225,70,35,210,PALE,GREEN)
        s.wave(55,205,145,14,4,ORANGE)
        s.arrow(285,145,425,95,BLUE)
        s.dot(335,127,'electron',BLUE,5)
        s.text(100,105,'photon',ORANGE)
        s.rect(90,295,175,32,'#fff0df',ORANGE)
        s.rect(265,295,155,32,LIGHT,BLUE)
        s.text(178,352,'escape cost',ORANGE,size=21,anchor='middle')
        s.text(345,352,'kinetic energy',BLUE,size=21,anchor='middle')
        return
    if mode=='compton':
        s.wave(55,245,180,10,4,ORANGE)
        s.dot(260,180,r=10,color=BLUE)
        s.arrow(260,180,380,75,ORANGE)
        s.arrow(260,180,395,295,GREEN)
        s.line(260,180,440,180,MUTED,1,'5 5')
        s.text(385,55,'photon',ORANGE,size=21)
        s.text(400,325,'electron',GREEN,size=21,anchor='middle')
        s.text(330,160,'θ',MUTED)
        s.text(260,355,'Energy and vector momentum are conserved',size=20,anchor='middle')
        return
    if mode=='barrier':
        s.path('M65 170 H200 V70 H330 V170 H465',MUTED,3)
        s.line(65,125,465,125,ORANGE,2,'6 5')
        s.text(155,110,'E',ORANGE)
        s.text(265,52,'barrier U₀',anchor='middle')
        s.line(65,260,465,260,MUTED,1)
        s.wave(65,200,260,30,3,BLUE,phase=math.pi/2)
        s.points([(200+130*u,260-30*math.exp(-2.6*u)) for u in [i/80 for i in range(81)]],BLUE)
        s.wave(330,465,260,30*math.exp(-2.6),3,BLUE,phase=math.pi/2)
        s.text(260,330,'Amplitude decays inside the forbidden region',size=20,anchor='middle')
        return
    if mode in ['levels','hydrogen','transition']:
        s.arrow(80,300,80,50,MUTED)
        s.text(65,35,'E',MUTED)
        for n,y in [(1,285),(2,133),(3,105)]:
            s.line(145,y,390,y,BLUE,2)
            s.text(415,y+6,f'n = {n}',BLUE,size=21)
        s.line(145,80,390,80,MUTED,1,'5 5')
        s.text(260,62,'ionization limit',MUTED,size=21,anchor='middle')
        s.arrow(270,138,270,277,ORANGE)
        s.text(300,215,'photon',ORANGE,size=21)
        s.text(260,350,'Photon energy equals the level difference',size=20,anchor='middle')
        return
    if mode=='bohr':
        s.circle(250,185,100,'none',BLUE)
        s.circle(250,185,55,'none','#afc4d2')
        s.dot(250,185,'proton',GREEN,12)
        s.dot(350,185,'electron',ORANGE,8)
        s.arrow(350,185,350,100,ORANGE)
        s.text(260,350,'Historical orbit model; not a literal quantum path',size=20,anchor='middle')
        return
    if mode=='angular':
        s.line(185,320,185,45,MUTED,2)
        s.text(170,35,'Lz',MUTED)
        s.circle(185,185,120,'none','#bdccbc')
        for dx,dy,label,col in [(85,-85,'+ℏ',GREEN),(120,0,'0',BLUE),(85,85,'−ℏ',ORANGE)]:
            s.arrow(185,185,185+dx,185+dy,col)
            s.line(185,185+dy,185+dx,185+dy,MUTED,1,'5 5')
            s.text(350,192+dy,label,col)
        s.text(260,350,'Same magnitude · discrete z projections',size=21,anchor='middle')
        return
    if mode=='normalization':
        s.axes(xlabel='x',ylabel='|ψ|²')
        points=[(80+350*u,270-165*math.sin(math.pi*u)**2) for u in [i/120 for i in range(121)]]
        s.points([(80,270)]+points+[(430,270)],BLUE,2,LIGHT)
        s.text(260,225,'total area = 1',BLUE,anchor='middle')
        s.text(260,340,'Probability is an area under the density',size=21,anchor='middle')
        return
    if mode=='uncertainty':
        for y,a,label in [(125,75,'narrow position packet'),(255,140,'broader momentum distribution')]:
            pts=[(70+380*u,y-65*math.exp(-((u-.5)*380/a)**2)) for u in [i/150 for i in range(151)]]
            s.line(65,y,460,y,MUTED)
            s.points(pts,BLUE if y==125 else ORANGE)
            s.text(260,y+34,label,size=21,anchor='middle')
        return
    # Infinite-well eigenfunctions drawn at levels proportional to n squared.
    s.line(105,65,105,285,MUTED,5);s.line(405,65,405,285,MUTED,5)
    s.line(105,285,405,285,MUTED,3)
    for n,y in [(1,265),(2,205),(3,105)]:
        s.line(105,y,405,y,'#afc4d2',1)
        s.wave(105,405,y,17,n/2,BLUE)
        s.text(430,y+6,f'n={n}',BLUE,size=21)
    s.text(105,325,'0',anchor='middle');s.text(405,325,'L',anchor='middle')
    s.text(260,355,'Only waves that vanish at both walls fit',size=21,anchor='middle')


def draw_statistics(s,mode):
    if mode=='fermi':
        s.axes(xlabel='E',ylabel='f(E)')
        for scale,col in [(.18,GREEN),(.65,ORANGE)]:
            pts=[(85+350*u,270-180/(1+math.exp((u-.5)*6/scale))) for u in [i/150 for i in range(151)]]
            s.points(pts,col)
        s.line(260,70,260,270,MUTED,1,'5 5')
        s.text(260,310,'μ',MUTED,anchor='middle')
        s.text(125,65,'colder',GREEN,size=21)
        s.text(330,180,'warmer',ORANGE,size=21)
        s.text(50,97,'1',MUTED)
        return
    if mode=='states':
        s.axes(xlabel='E',ylabel='g(E)')
        pts=[(80+350*u,270-170*math.sqrt(u)) for u in [i/150 for i in range(151)]]
        s.points([(80,270)]+[p for p in pts if p[0]<=285]+[(285,270)],BLUE,1,LIGHT)
        s.points(pts,GREEN)
        s.line(285,90,285,270,ORANGE,2,'5 5')
        s.text(285,310,'EF',ORANGE,anchor='middle')
        s.text(185,215,'filled',BLUE,anchor='middle')
        return
    if mode=='planck':
        s.axes(xlabel='λ',ylabel='radiance')
        def b(l,t):return l**-5/math.expm1(1/(l*t))
        # Use the exact wavelength Planck shape; arbitrary common vertical scale.
        for temp,col in [(1,BLUE),(1.25,ORANGE)]:
            points=[(82+360*u,270-2.6*b(.045+.9*u,temp)) for u in [i/240 for i in range(241)]]
            s.points(points,col)
        s.text(260,80,'hotter',ORANGE,size=21)
        s.text(325,230,'cooler',BLUE,size=21)
        s.text(260,350,'Hotter → stronger emission and shorter peak λ',size=20,anchor='middle')
        return
    if mode=='decay':
        s.axes(xlabel='t',ylabel='N / N₀')
        pts=[(85+350*u,270-185*2**(-3*u)) for u in [i/150 for i in range(151)]]
        s.points(pts)
        for k in [1,2,3]:
            x=85+350*k/3;y=270-185*2**(-k)
            s.dot(x,y,r=4,color=ORANGE)
            s.text(x,310,f'{k}t½',ORANGE,size=21,anchor='middle')
        s.text(260,350,'The same fraction decays each half-life',size=21,anchor='middle')
        return
    s.text(260,65,'Alignment competes with thermal disorder',size=21,anchor='middle')
    for left,aligned in [(65,False),(320,True)]:
        s.rect(left,110,140,150,LIGHT,BLUE)
        for i in range(6):
            x=left+30+(i%2)*70;y=140+(i//2)*45
            angle=0 if aligned else [0,1.6,2.5,3.3,4.4,5.2][i]
            s.arrow(x-15*math.cos(angle),y+15*math.sin(angle),x+15*math.cos(angle),y-15*math.sin(angle),GREEN)
    s.text(135,310,'weak alignment',size=21,anchor='middle')
    s.text(390,310,'more alignment',size=21,anchor='middle')


def draw_nuclear(s,mode):
    if mode=='chain':
        s.dot(90,180,r=11,color=BLUE)
        for y in [110,250]:
            s.arrow(105,180,235,y,BLUE)
            s.dot(250,y,r=11,color=BLUE)
            for yy in [y-40,y+40]:
                s.arrow(265,y,415,yy,BLUE);s.dot(430,yy,r=9,color=BLUE)
        s.text(90,330,'1',anchor='middle');s.text(250,330,'2',anchor='middle');s.text(430,330,'4',anchor='middle')
        s.text(260,45,'Illustrative multiplication factor k = 2',size=21,anchor='middle')
        return
    if mode=='radius':
        for x,r,label in [(100,25,'A'),(250,31.5,'2A'),(410,50,'8A')]:
            s.circle(x,180,r,PALE,GREEN)
            s.text(x,280,label,anchor='middle')
        s.text(260,75,'Eight times the volume → twice the radius',size=21,anchor='middle')
        return
    if mode=='quarks':
        for cx,charges,name in [(140,['+⅔','+⅔','−⅓'],'proton: +1e'),(385,['+⅔','−⅓','−⅓'],'neutron: 0')]:
            s.circle(cx,180,90,LIGHT,BLUE)
            for dx,dy,label in [(-35,-25,charges[0]),(35,-25,charges[1]),(0,45,charges[2])]:
                s.circle(cx+dx,180+dy,28,PALE,GREEN)
                s.text(cx+dx,187+dy,label,GREEN,size=21,anchor='middle')
            s.text(cx,315,name,size=21,anchor='middle')
        return
    if mode=='expansion':
        for cx,scale,label in [(140,1,'earlier'),(380,1.7,'later')]:
            for dx,dy in [(-35,-35),(35,-35),(-35,35),(35,35)]:s.dot(cx+dx*scale,180+dy*scale,r=7,color=BLUE)
            s.line(cx-35*scale,180-35*scale,cx+35*scale,180-35*scale,MUTED,1,'5 5')
            s.text(cx,80,label,anchor='middle')
        s.arrow(240,180,280,180,ORANGE)
        s.text(260,320,'Fixed comoving positions; greater proper distance',size=20,anchor='middle')
        return
    if mode=='binding':
        s.line(95,95,430,95,BLUE,3)
        s.line(95,270,430,270,GREEN,3)
        s.text(260,65,'separated nucleons',BLUE,anchor='middle')
        s.text(260,310,'bound nucleus',GREEN,anchor='middle')
        s.arrow(150,103,150,260,ORANGE)
        s.text(180,190,'binding energy',ORANGE,size=21)
        return
    for x,r in [(115,45),(350,30),(425,25)]:
        s.circle(x,180,r,PALE,GREEN)
        nucleons=[(-22,-12),(0,-20),(22,-12),(-22,12),(0,20),(22,12)] if x==115 else [(-10,-10),(12,-8),(0,13)]
        for dx,dy in nucleons:s.dot(x+dx,180+dy,r=5,color=BLUE)
    s.arrow(185,180,290,180,ORANGE)
    s.wave(320,465,80,10,4,ORANGE)
    s.text(260,335,'A lower final rest mass releases energy',size=21,anchor='middle')


DRAW = {
    'units':draw_units,'motion':draw_motion,'vectors':draw_vectors,'projectile':draw_projectile,
    'circle':draw_circle,'forces':draw_forces,'drag':draw_drag,'work':draw_work,
    'momentum':draw_momentum,'rotation':draw_rotation,'orbit':draw_orbit,'fluid':draw_fluid,
    'oscillation':draw_oscillation,'waves':draw_waves,'gas':draw_gas,'pv':draw_pv,'heat':draw_heat,
    'charges':draw_charges,'field':draw_field,'potential':draw_potential,'capacitor':draw_capacitor,
    'current':draw_current,'circuit':draw_circuit,'magnet':draw_magnet,'em':draw_em,
    'optics':draw_optics,'interference':draw_interference,'bragg':draw_bragg,
    'relativity':draw_relativity,'quantum':draw_quantum,'statistics':draw_statistics,'nuclear':draw_nuclear,
}


@dataclass(frozen=True)
class Diagram:
    topic: str
    scene: str
    mode: str
    title: str
    caption: str
    step: int = 0
    key: str = 'concept'

    @property
    def filename(self):
        return f'{self.topic}-{self.key}.svg'


DIAGRAMS = []


def D(topic,scene,mode,title,caption,step=0,key='concept'):
    DIAGRAMS.append(Diagram(topic,scene,mode,title,caption,step,key))


def svg_for(d):
    s=Scene()
    DRAW[d.scene](s,d.mode)
    colors=[GREEN,BLUE,ORANGE,MUTED,INK]
    markers=''.join(f'<marker id="head-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="{c}" stroke-width="1.5"/></marker>' for c in colors)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="520" height="380" viewBox="0 0 520 380" role="img" aria-labelledby="title description">'
            f'<title id="title">{escape(d.title)}</title><desc id="description">{escape(d.caption)}</desc>'
            f'<defs>{markers}</defs><rect width="520" height="380" fill="#fff"/>'
            '<g font-family="Arial,DejaVu Sans,sans-serif" font-weight="400">'+''.join(s.parts)+'</g></svg>')


def diagrams_for(topic,step=0):
    return [d for d in DIAGRAMS if d.topic==topic and d.step==step]


def figure_html(d):
    proof = 'main' if not d.step else f'step-{d.step}'
    return (f'<figure class="concept-figure" data-diagram="{d.topic}-{d.key}">'
            f'<div class="figure-label">Picture the idea · {escape(d.title)}</div>'
            f'<img src="assets/diagrams/{d.filename}" alt="{escape(d.caption,quote=True)}" width="520" height="380" loading="lazy" decoding="async">'
            f'<figcaption>{escape(d.caption)}<span class="figure-links">'
            f'<a data-proof-link href="#proof-{proof}">Connect the picture to the derivation ↗</a>'
            f'<a href="assets/diagrams/{d.filename}" target="_blank" rel="noopener">Open full-size diagram ↗</a>'
            '</span></figcaption></figure>')


def build_diagrams(root,topics):
    slugs={t['slug'] for t in topics}
    assert {d.topic for d in DIAGRAMS}==slugs, ('Missing diagrams',slugs-{d.topic for d in DIAGRAMS})
    assert len({d.filename for d in DIAGRAMS})==len(DIAGRAMS)
    out=Path(root)/'derivations/assets/diagrams'
    out.mkdir(parents=True,exist_ok=True)
    for d in DIAGRAMS:
        topic=next(t for t in topics if t['slug']==d.topic)
        assert d.step<=len(topic['steps'])
        if d.step:
            assert topic['steps'][d.step-1]['equation'], (d.topic,d.step,'Figure must link to an existing proof')
        (out/d.filename).write_text(svg_for(d))


# Each assignment is specific to the argument on that page. Captions state the
# physical reading of the sketch; these are not decorative chapter thumbnails.
D('units-and-dimensions','units','length','One length, two units',
  'The two rulers represent the same physical length. A conversion changes its numerical value, while the measurement itself stays fixed.')
D('density','units','density','Mass within the same volume',
  'The boxes have equal volume. The one containing more mass has greater density; the dots stand for mass elements, not a particular atomic arrangement.')
D('constant-acceleration','motion','acceleration','Displacement is an area',
  'For a body starting from rest, velocity rises linearly under constant acceleration. The triangular area beneath the velocity–time line is the displacement, explaining the factor one half.')
D('rates-of-change','motion','rates','A rate is a tangent slope',
  'On a position–time curve, the tangent slope gives instantaneous velocity. A changing slope means the velocity is changing and the body is accelerating.')
D('vector-components','vectors','components','Resolve one vector into two components',
  'The green vector is the diagonal of a right triangle. Its signed horizontal and vertical projections provide the cosine and sine components.')
D('vector-products','vectors','products','Parallel projection and perpendicular area',
  'The dot product measures the projection along the orange vector. The cross-product magnitude measures the shaded parallelogram area associated with the two directions.')
D('projectile-motion','projectile','flight','Separate horizontal and vertical motion',
  'The projectile moves right while gravity accelerates it downward. At the highest point its vertical velocity is zero, yet its downward acceleration remains nonzero.')
D('centripetal-acceleration','circle','orbit','Velocity tangent, acceleration inward',
  'At the marked point the orange velocity is tangent to the circle and the green acceleration points toward the centre. Acceleration changes direction even when speed stays constant.')
D('newtons-second-law','forces','flat','A free-body diagram',
  'Add forces as vectors. Here the horizontal pull exceeds opposing friction, while the equal vertical forces balance; the net force is horizontal.')
D('inclined-plane','forces','incline','Resolve weight on an incline',
  'Weight points vertically down, the normal force is perpendicular to the slope, and the orange arrow shows the down-slope component of weight. Components do not represent additional interactions.')
D('friction','forces','friction','Friction opposes the tendency to slide',
  'The orange down-slope component of weight tends to cause sliding. The contact friction shown acts up the slope; static friction adjusts until its limiting value is reached.')
D('terminal-speed','drag','fall','Balance at terminal speed',
  'On the left, drag is smaller than weight and the body speeds up downward. On the right, equal opposing force magnitudes give zero acceleration and constant falling speed.')
D('work-energy','work','work','Force acting through a displacement',
  'Only the force component along the displacement contributes to work. The accumulated net work changes kinetic energy between the two positions.')
D('spring-work','work','spring','A restoring force grows with extension',
  'The dashed line marks the relaxed end. Stretching the spring moves its end right, while the spring force pulls it back toward equilibrium.')
D('potential-energy','work','potential','Force follows the potential-energy slope',
  'The potential-energy curve has a stable minimum. A particle to the right of that minimum feels a force toward lower potential energy, opposite the positive slope.')
D('mechanical-energy','work','mechanical','Potential energy can become kinetic energy',
  'In an ideal lossless fall, the same total mechanical energy changes form from gravitational potential to motion. The equal-height bars represent equal energies, not object heights.')
D('momentum-and-impulse','momentum','sticking','Two carts exchange momentum',
  'A moving cart collides with a stationary cart and they stick together. Their common motion afterward must carry the same total momentum if the external impulse is negligible.')
D('center-of-mass','momentum','com','A mass-weighted balance point',
  'A 1 kg mass at zero and a 3 kg mass at 4 m balance at 3 m. The centre of mass lies closer to the heavier mass, rather than halfway between the positions.')
D('rotational-energy','rotation','disk','Different radii have different speeds',
  'The body shares one angular speed, but a point twice as far from the axis moves twice as fast. This radius dependence produces the squared-radius weighting in moment of inertia.')
D('parallel-axis','rotation','parallel-axis','Shift the axis away from the centre of mass',
  'The dashed axes are parallel and separated by d. The orange axis lies farther from the mass distribution overall, increasing the moment of inertia by the parallel-axis term.')
D('angular-momentum','rotation','torque','A perpendicular force changes angular momentum',
  'The force acts perpendicular to the radius at the marked point. Its turning effect depends on the lever arm; a force directed along the radius would give zero torque.')
D('rolling','forces','rolling','Rolling combines translation and rotation',
  'The wheel centre moves down the slope while the wheel rotates. Under no slip the contact point is instantaneously at rest relative to the fixed slope; the drawn wheel motion is schematic.')
D('static-equilibrium','rotation','balance','Balance forces and turning effects',
  'Upward support forces balance the downward weight. Their lever arms must also balance torques; zero net force alone does not prevent a body from turning.')
D('elasticity','rotation','elasticity','A small tensile deformation',
  'Opposing axial pulls stretch the rod. The dashed outline shows a small extension of its length; the deformation is exaggerated so the strain can be seen.')
D('orbital-speed','orbit','orbit','Gravity supplies the inward force',
  'A satellite moving tangentially continually falls toward the central mass. Gravity bends its path; no separate extra centripetal interaction is added.')
D('escape-speed','orbit','escape','Escape requires enough total energy',
  'The outward path represents an unbound trajectory rather than a circular orbit. Ideal marginal escape reaches arbitrarily large radius with speed tending to zero.')
D('hydrostatic-pressure','fluid','depth','Pressure differences create buoyancy',
  'The arrows at greater depth represent larger pressure. The surrounding fluid gives the immersed block a net upward buoyant force because pressure is larger beneath it.')
D('bernoulli','fluid','pipe','The same volume flow passes every section',
  'In a horizontal ideal pipe, the narrower section needs a larger flow speed. Bernoulli energy balance then relates this speed increase to a pressure decrease under the stated assumptions.')
D('simple-harmonic-motion','oscillation','spring','The force always restores toward equilibrium',
  'The displaced mass feels a spring force back toward the dashed equilibrium position. This force proportional to minus displacement produces harmonic motion.')
D('pendulum','oscillation','pendulum','Weight supplies the pendulum torque',
  'The string length fixes the arc geometry. Weight acts downward, and its tangential component restores the bob toward the vertical equilibrium direction.')
D('wave-speed','waves','travelling','Wave motion differs from material motion',
  'The wave pattern travels horizontally while a string element moves transversely. String tension and mass per length set the propagation speed.')
D('standing-waves','waves','standing','Fixed nodes select allowed wavelengths',
  'This second mode contains two half-wavelengths between fixed endpoints. The green and blue curves show opposite phases of one standing wave, not two different allowed modes.')
D('sound-speed','waves','sound','Sound carries a compression pattern',
  'Particles move back and forth along the direction of travel, producing alternating dense and less dense regions. Elastic compression and inertia together set sound speed.')
D('doppler','waves','doppler','An approaching source crowds its wavefronts',
  'Successive circles were emitted from progressively later positions of a source moving right. Wavefronts are closer together ahead and farther apart behind.')
D('first-law','gas','piston','Energy can enter as heat and leave as work',
  'Gas expands by pushing a piston through a larger volume. Heat supplied to the gas and outward work must be tracked separately when calculating its internal-energy change.')
D('isothermal-work','pv','isothermal','Expansion work is area under the actual path',
  'Along a reversible isothermal ideal-gas path, pressure falls as volume increases. The shaded area is the accumulated boundary work; the curve is a schematic at constant temperature.')
D('ideal-gas','gas','collision','Microscopic collisions produce pressure',
  'The orange velocity toward the wall reverses its normal direction after an elastic collision. The wall receives the opposite momentum change, giving an average force.')
D('adiabatic-gas','pv','adiabatic','Adiabatic expansion cools a reversible ideal gas',
  'The two paths start at the same state. Reversible adiabatic pressure drops more steeply than isothermal pressure because work is supplied by decreasing internal energy.')
D('entropy','gas','free-expansion','Expansion opens more accessible positions',
  'Removing the partition gives the particles access to both halves. An insulated ideal-gas free expansion can increase entropy even though its actual heat transfer and boundary work are zero.')
D('carnot','heat','engine','Heat flow and useful work in an engine',
  'The working fluid absorbs Qh from the hot reservoir, delivers work, and rejects Qc to the cold reservoir. Energy returns to its initial value after a complete cycle.')
D('coulomb','charges','pair','Charge signs determine attraction or repulsion',
  'Like charges push apart, while unlike charges pull together. The two forces in each pair have equal magnitude and act on different objects.')
D('charge-conservation','charges','pair','Charge is signed and interactions preserve its total',
  'Positive and negative charge signs set the force directions. Transferring charge between objects can change each object’s charge while preserving their signed total.')
D('electric-field','field','ring','Symmetry simplifies a ring field',
  'At the axial point P, opposite ring elements produce transverse components that cancel. Their components along the axis reinforce, leaving an axial electric field.')
D('electric-dipole','charges','dipole','A uniform field turns a neutral dipole',
  'The moment p points from negative to positive charge. Equal opposite forces in a rightward uniform field form a couple that tends to align the dipole with the field.')
D('gauss-sphere','field','sphere','A spherical Gaussian surface matches the symmetry',
  'The field is radial and equal in magnitude at every point on the concentric spherical surface. This symmetry is what allows the field to leave the flux integral.')
D('gauss-cylinder-plane','field','sheet','A sheet has equal normal fields on both sides',
  'A pillbox Gaussian surface receives flux through two opposite caps. For a uniform nonconducting sheet, both sides contribute equally to the flux balance.')
D('electric-potential','potential','uniform','Equipotentials cut across the field',
  'The dashed lines are equal-potential surfaces in a uniform field. A positive charge moving right follows the field toward lower electric potential.')
D('electric-energy','potential','pairs','Assemble a configuration pair by pair',
  'Bringing a second charge into the first charge’s potential changes the interaction energy. Each interacting pair contributes once to the total configuration energy.')
D('parallel-plate-capacitance','capacitor','plates','A nearly uniform field fills the plate gap',
  'Opposite plate charges create a nearly uniform interior field when edge effects are negligible. The potential difference accumulates across separation d.')
D('capacitor-energy','capacitor','plates','The field between the plates stores energy',
  'The shaded gap represents the field-filled volume. As more charge is separated onto the plates the voltage rises, so the work per additional charge also rises.')
D('current-drift','current','drift','Drift direction and conventional current differ',
  'Electrons drift left in this wire while conventional current points right. Count carriers crossing a section to connect drift speed to charge flow.')
D('resistance','current','resistance','Geometry and collisions affect conduction',
  'The wire has a finite length and cross section. Charge carriers transfer momentum through collisions; local resistivity and geometry determine the terminal resistance.')
D('kirchhoff','circuit','junction','A junction cannot accumulate charge in steady flow',
  'The incoming current splits between two outgoing branches. Their sum must match the input when no net charge builds up at the node.')
D('rc-circuit','circuit','rc','The rising capacitor voltage reduces the current',
  'A DC source drives charge through the series resistor onto the capacitor. As the capacitor voltage rises, the voltage remaining across the resistor decreases.')
D('magnetic-orbit','magnet','orbit','Magnetic force bends a positive charge',
  'For the positive charge shown, upward velocity and a magnetic field into the page produce an inward leftward force. The force is perpendicular to velocity and changes direction, not speed.')
D('magnetic-wire','magnet','wire','Moving charge makes a magnetic wire force',
  'Conventional current points right and the crosses mark magnetic field into the page. Their cross product gives the upward force on this wire segment.')
D('ampere-wire','magnet','ampere','Magnetic field circles a straight current',
  'The central dot represents current out of the page. The magnetic field follows a counterclockwise circle, with constant magnitude along a concentric circular path.')
D('solenoid','magnet','solenoid','Many coil turns reinforce the inside field',
  'The dots and crosses show currents on opposite sides of the windings. Their fields reinforce along the long solenoid axis; end effects are omitted.')
D('faraday','magnet','faraday','Induction opposes a change of flux',
  'The approaching north pole increases rightward flux through the loop. The induced magnetic field points left, opposing the increase rather than merely opposing any existing field.')
D('inductor-energy','magnet','energy','Current builds a magnetic field',
  'The coil current establishes an axial field. Raising the current requires work against the induced back emf; that work can be stored as magnetic field energy.')
D('lc-oscillations','circuit','lc','Electric and magnetic energy trade places',
  'The ideal loop contains an inductor and capacitor with no resistor. Capacitor charge and inductor current reach their extrema at different times as stored energy moves between their fields.')
D('ac-impedance','circuit','rlc','Three elements respond with different phases',
  'The resistor, inductor and capacitor share the series current. Their voltage amplitudes must be combined with phase, so the reactive drops can oppose rather than simply add.')
D('displacement-current','em','displacement','A changing electric field bridges the current balance',
  'Current charges the plates but carriers do not cross the insulating gap. The changing electric flux contributes displacement current to the Maxwell–Ampère balance.')
D('em-wave-equation','em','wave','Electric and magnetic fields travel together',
  'The electric field oscillates in the page; dots and crosses show the magnetic field perpendicular to it. Their signs change together, so the energy flow keeps the same propagation direction.')
D('em-intensity','em','wave','The field cross product gives energy-flow direction',
  'Electric and magnetic fields are perpendicular and in phase for this vacuum travelling wave. Their cross product points along propagation, while intensity depends on squared field amplitude.')
D('radiation-pressure','em','pressure','An absorber receives incoming light momentum',
  'Light arriving from the left transfers momentum to the absorbing surface and exerts a rightward force. Perfect reversal by reflection would double the normal momentum transfer.')
D('thin-lens','optics','lens','Two principal rays locate the image',
  'One ray enters parallel and refracts toward the far focus; the central ray is undeviated in the thin-lens model. They meet at the same inverted real image.')
D('spherical-mirror','optics','mirror','Reflected rays locate the concave-mirror image',
  'A nearly parallel incident ray returns through the focus. A second paraxial reflected ray meets it at the inverted image; the spherical surface is drawn schematically.')
D('double-slit','interference','double','Two coherent paths interfere on the screen',
  'Rays from the two slit openings reach a common screen point with different path lengths. Their relative phase determines the alternating bright and dark fringes.')
D('thin-film','interference','film','Two reflected paths can acquire different phases',
  'One ray reflects at the top interface; another enters the film, reflects at the lower interface and emerges. Both the extra optical path and reflection phase shifts matter.')
D('single-slit','interference','single','Different parts of one opening interfere',
  'The slit is a continuous coherent opening, not a single ray. Contributions from across its width produce a broad central bright region and weaker side lobes.')
D('diffraction-grating','interference','grating','More slits sharpen the principal maxima',
  'Many equally spaced slits contribute coherent amplitudes. Their principal maxima become narrow because a small phase mismatch accumulates across the whole array.')
D('time-dilation','relativity','clock','A moving light clock has a longer light path',
  'In the clock rest frame the light travels vertically. In the other frame it follows the longer diagonal route while keeping the same light speed, so more coordinate time passes.')
D('relativistic-energy','relativity','energy','An energy–momentum triangle',
  'The triangle is an algebraic picture of the invariant energy relation: legs pc and rest energy mc² combine to give total energy E. It is not a triangle of spatial travel.')
D('photons','quantum','photon','A photon supplies the escape cost and electron motion',
  'Light brings energy to the surface. Part of that energy pays the work-function cost, and the remainder can appear as the emitted electron’s kinetic energy.')
D('compton','quantum','compton','A scattered photon and recoiling electron share momentum',
  'The incoming photon transfers energy and vector momentum to an initially stationary electron. The photon scatters upward and the recoil carries the compensating momentum; angles are schematic.')
D('particle-in-box','quantum','box','Boundary conditions select standing matter waves',
  'Each pictured state vanishes at both infinite walls. The wavefunctions are drawn with schematic amplitudes at their allowed energy heights, which grow as the squared mode number.')
D('tunneling','quantum','barrier','A forbidden region attenuates the wavefunction',
  'The upper sketch shows particle energy below the barrier height. The lower wave is schematic: its envelope decreases inside the barrier and leaves a small transmitted amplitude; exact matching also includes reflection.')
D('hydrogen','quantum','bohr','The Bohr orbit is a historical model',
  'The sketch represents the historical circular-orbit model used to calculate the leading energy scale. Modern quantum theory uses stationary wavefunctions rather than literal electron paths.')
D('atomic-transitions','quantum','transition','A transition produces a photon of definite energy',
  'Only discrete atomic energies are allowed. A downward jump emits a photon carrying the energy difference, while upward absorption requires the corresponding energy input.')
D('drude','current','drude','Field acceleration competes with collisions',
  'Electron drift opposes conventional current. In the Drude model, acceleration by the electric field is balanced on average by momentum relaxation from collisions.')
D('fermi-dirac','statistics','fermi','Thermal energy smooths the occupation edge',
  'The colder curve has a sharper change near the chemical potential. At nonzero temperature the occupation of a single state at that energy is one half.')
D('radioactive-decay','statistics','decay','Equal half-lives remove equal fractions',
  'The exponential curve loses half its remaining expected population during each successive half-life. The absolute loss gets smaller, rather than staying fixed.')
D('binding-energy','nuclear','binding','A bound nucleus has lower rest energy',
  'The lower level represents the bound nucleus and the upper level its separated nucleons. The energy gap is the energy needed for disassembly, corresponding to the mass defect.')
D('nuclear-energy','nuclear','reaction','Rest-energy differences become released energy',
  'This generic reaction sketch represents a rearrangement into products with lower total rest mass. The difference can leave as kinetic energy or radiation; no particular isotope reaction is implied.')
D('chain-reaction','nuclear','chain','Repeated multiplication changes the population',
  'In the illustrative generation model each effective neutron produces two effective successors. The counts become one, two, four; actual reactor multiplication includes losses and other effects.')
D('quark-charges','nuclear','quarks','Constituent charges add to the nucleon charge',
  'The valence charges add to +1e for a proton and zero for a neutron. The colours distinguish drawing elements and do not specify quantum chromodynamic colour charge.')
D('cosmological-redshift','nuclear','expansion','Expansion increases proper separations',
  'The same four comoving locations are farther apart when the scale factor grows. This sketch illustrates a changing distance scale, not galaxies growing in physical size.')
D('integrals','motion','integrals','Add many small changes',
  'Rectangles approximate the accumulated change by multiplying a rate by short input intervals. Refining the intervals gives the area integral under the rate curve.')
D('equipartition','gas','equipartition','Three independent translational motions',
  'The three arrows represent independent Cartesian momentum components, not three different molecules. In classical equilibrium each quadratic component has the same mean energy.')
D('clausius','heat','engine','A reversible cycle balances heat divided by temperature',
  'The engine exchanges heat with two reservoirs and returns to its original state. Reversible-engine comparisons constrain the heat ratio before entropy is introduced as a state function.')
D('relative-motion','motion','displacement','Compose the positions before differentiating',
  'A particle position relative to one origin can be built from the displacement to a second origin and then to the particle. Differentiating that geometric relation gives relative velocity.')
D('power','work','work','Power is the rate of transferring work',
  'A force along motion transfers work as displacement occurs. Dividing the small work by elapsed time connects instantaneous power to the force and velocity component in the same direction.')
D('elastic-collisions','momentum','elastic','Equal masses exchange velocities in the special case shown',
  'A moving cart strikes an identical stationary cart in an ideal elastic collision. Momentum and kinetic-energy conservation make the first stop while the second takes its velocity.')
D('rocket','momentum','rocket','Backward exhaust produces forward rocket momentum',
  'A short ejection interval conserves the momentum of rocket plus exhaust. The rocket mass decreases, so integrating the momentum balance requires retaining its changing mass.')
D('rotational-kinematics','rotation','disk','Angular rates connect to linear motion',
  'All material points share the same angular speed, but their tangential speeds scale with perpendicular radius. Differentiating the arc-length relation gives the corresponding accelerations.')
D('gyroscope','oscillation','gyroscope','Torque changes the direction of a fast spin',
  'In slow steady precession, gravity turns the nearly horizontal spin angular-momentum vector around the support. The perspective and distances are schematic; this is not a full nutation solution.')
D('gravity-sphere-orbits','orbit','shell','Shell symmetry leaves only the enclosed mass',
  'For a spherical body, outer shells exert zero net force at an interior point. With uniform density the enclosed mass grows as the cube of the small radius, giving a linear interior field.')
D('physical-pendulums','oscillation','physical-pendulum','The mass distribution affects the restoring motion',
  'The rigid body rotates about its pivot while weight acts at its centre of mass. Both the pivot-to-centre distance and the inertia about the pivot determine its small-angle period.')
D('damped-driven','oscillation','damping','Damping reduces the oscillation envelope',
  'The decaying envelope follows the amplitude of underdamped motion. In the weak-damping limit, cycle-averaged mechanical energy decreases with the square of that envelope.')
D('travelling-wave-energy','waves','travelling','Transverse velocity and tension transport energy',
  'A string element moves perpendicular to propagation while tension links it to neighbouring elements. Their force and velocity determine the power crossing a section.')
D('sound-energy-pipes','waves','sound','Compression and motion carry sound energy',
  'The compressed and expanded regions propagate while each fluid element oscillates locally. Pressure perturbation and particle velocity together determine the average energy flux.')
D('thermal-expansion','heat','expansion','Small dimensional changes accumulate',
  'The dashed outline represents a heated body with slightly greater dimensions. Expanding three independent lengths explains why isotropic volume expansion is approximately three times the linear coefficient.')
D('heat-conduction','heat','conduction','Steady energy flow through a slab',
  'The hot and cold faces set a temperature gradient across a finite thickness. In steady one-dimensional conduction, the same power crosses every internal section.')
D('gas-statistics','gas','speeds','A distribution gives different characteristic speeds',
  'Most probable speed marks the peak, mean speed averages all speeds, and rms speed weights their squares. The vertical markers show their distinct locations, not three populations.')
D('heat-capacities','gas','equipartition','Count active quadratic energy terms',
  'The three translational components give three contributions to the internal energy. Additional active rotational or vibrational quadratic terms change the heat capacity.')
D('refrigerator','heat','refrigerator','Work moves heat from cold to hot',
  'The arrows reverse the engine flow: heat is extracted from the cold reservoir and discharged to the hot one, with external work supplied to the working fluid.')
D('statistical-entropy','gas','multiplicity','Equal macrostates can contain unequal numbers of microstates',
  'For four labelled particles, all four in one specified half has one occupancy assignment. Putting two in each half has six assignments, so the balanced macrostate has greater multiplicity.')
D('charge-distributions','field','ring','Build a continuous distribution from symmetric elements',
  'Opposite ring elements cancel transverse field components on the axis. Adding rings of different radii builds a disk; scalar potentials can then be accumulated without vector cancellation.')
D('capacitor-geometries','capacitor','spherical','Geometry controls the voltage integral',
  'Concentric conducting shells provide a radial gap from a to b. Gauss’s law sets the radial field, and integrating it across the gap determines capacitance.')
D('capacitor-networks','capacitor','network','Parallel capacitors share a voltage',
  'Both branches connect to the same pair of nodes. Their voltage differences agree, while their stored charges add to determine the equivalent capacitance.')
D('current-flux','current','flux','Count charge crossing an oriented area',
  'The highlighted section is the surface through which current is measured. The normal component of charge flow contributes; the carrier drift can point opposite conventional current.')
D('battery-discharge','circuit','rc-discharge','Stored capacitor energy drives a discharge',
  'The source is removed and the charged capacitor drives current through the resistor. Its charge and the discharge-current magnitude decrease exponentially.')
D('magnetic-geometries','magnet','ampere','Choose geometry to match magnetic symmetry',
  'For a straight current the field is tangential to concentric circles. Other arrangements require integrating current elements or counting enclosed turns using the matching geometry.')
D('rl-mutual','circuit','rl','An inductor resists changes in the current',
  'This source-free resistor–inductor loop illustrates current decay after a source is removed. The induced voltage temporarily drives current in the same direction while field energy is dissipated.')
D('ac-power-transformers','circuit','transformer','The same changing flux links two windings',
  'Winding voltage is proportional to linked turn count in an ideal transformer. Energy conservation then fixes the inverse current ratio and the reflected load resistance.')
D('magnetic-moments','magnet','dipole','Circulating charge has a magnetic moment',
  'A current loop has a moment normal to its plane. Orbital electron motion can be related to this construction, while intrinsic spin requires an independent quantum input.')
D('curie-law','statistics','alignment','Thermal disorder competes with field alignment',
  'The sketches compare disordered dipole orientations with more aligned ones. Curie’s weak-field model averages the component along the field using thermal statistical weights.')
D('polarization-refraction','optics','polarization','A polarizer transmits a projection of the field',
  'The transmission axis selects only the parallel electric-field component. Squaring that amplitude projection gives Malus’s intensity factor.')
D('refracting-instruments','optics','lens','Image geometry is reused in optical instruments',
  'The thin-lens ray construction supplies a real image and a height ratio. Magnifiers, microscopes and telescopes combine such images with the angle subtended at the eye.')
D('apertures-bragg','bragg','aperture','A circular aperture produces a diffraction pattern',
  'The bright central spot and weaker rings are a schematic Airy pattern, not a scale intensity map. The first dark ring sets the circular-aperture angular resolution criterion.')
D('lorentz-transform','relativity','lorentz','Time and space axes depend on the frame',
  'The primed frame axes tilt within a spacetime diagram. Different constant-time slices explain why simultaneity and moving lengths must be handled with the full transformation.')
D('light-doppler','relativity','doppler','Recession stretches the detected wavelength',
  'The orange detected wave has a longer wavelength than the emitted blue wave for receding motion. Light keeps its vacuum speed; its frequency and wavelength transform together.')
D('planck-radiation','statistics','planck','Heating changes both the strength and the peak wavelength',
  'These two normalized Planck-law wavelength spectra use a common vertical scale. The hotter spectrum is higher and peaks at shorter wavelength; the drawn scales are illustrative.')
D('quantum-foundations','quantum','uncertainty','Localization broadens the momentum distribution',
  'The sketches illustrate Fourier-related Gaussian profiles on separate axes, with widths not drawn on a common physical scale. A narrower position packet requires a broader momentum distribution.')
D('quantum-normalization','quantum','normalization','Total probability is an integral',
  'Probability density is nonnegative. Its full area is normalized to one; integrating only part of the shaded area gives the probability of finding the particle in that region.')
D('quantum-angular','quantum','angular','Angular-momentum magnitude and projection differ',
  'For orbital index one, three vectors of the same magnitude have the allowed z projections +ℏ, zero and −ℏ. The drawing illustrates allowed projections, not literal precessing electron paths.')
D('electron-gas-states','statistics','states','Available states and filled states are different',
  'The free-electron density of available states increases with energy. At zero temperature the occupied states fill the shaded region up to the Fermi energy.')
D('nuclear-size-fusion','nuclear','radius','Approximately constant density gives cube-root radius scaling',
  'The three nuclei represent mass numbers in the ratio one, two and eight. At constant nuclear matter density their radii scale as one, cube root of two, and two.')
D('hydrogen-quantum','quantum','hydrogen','Normalizable Coulomb states have discrete energies',
  'The bound Coulomb levels accumulate below the ionization limit. Radial regularity and normalizability select these energies without a literal circular electron orbit.')
D('boltzmann-weights','gas','boltzmann','A reservoir supplies different numbers of compatible states',
  'The small system exchanges energy with a much larger reservoir. A system state is more likely when more reservoir microstates can accompany it at the fixed total energy.')

# Additional pictures at steps whose geometry or bookkeeping benefits from a second view.
D('centripetal-acceleration','circle','velocity-change','The velocity difference',
  'Two equal-length velocity vectors point in different directions. Their tip-to-tip difference is nonzero, so constant speed does not mean zero acceleration.',2,'velocity-change')
D('spring-work','motion','spring-area','Spring work is a triangular area',
  'The required quasistatic external force rises linearly from zero to its final value. The area under that force–extension line is half the enclosing rectangle.',3,'work-area')
D('carnot','pv','carnot','The four reversible Carnot legs',
  'Orange and blue curves are the hot and cold isotherms. Green adiabatic legs connect them; the state order follows the engine cycle used in the derivation.',3,'pv-cycle')
D('clausius','pv','carnot','A reversible-engine reference cycle',
  'An ideal-gas Carnot cycle provides a calculable heat ratio. Reversible-engine comparisons extend that ratio beyond this particular working substance.',2,'reference-cycle')
D('ideal-gas','gas','equipartition','Temperature enters through three kinetic components',
  'Collisions alone give pressure in terms of mean-square velocity. The three equal quadratic translational energy contributions supply the separate temperature relation.',4,'thermal-energy')
D('entropy','heat','engine','Entropy is defined using reversible heat transfer',
  'A reversible-cycle heat balance makes heat divided by absolute temperature path-independent between equilibrium endpoints. That reversible reference can be used even when the actual process is irreversible.',1,'reversible-reference')
D('first-law','gas','free-expansion','Zero heat and work can still accompany expansion',
  'In an insulated free expansion, removing a partition lets the gas fill a larger region against zero external pressure. The ideal-gas temperature remains unchanged even though entropy increases.',5,'free-expansion')
D('double-slit','interference','single','Finite slit width adds an envelope',
  'Each finite-width slit also produces its own diffraction envelope. The two-slit fringes sit inside that envelope rather than remaining equally bright at every angle.',4,'slit-envelope')
D('apertures-bragg','bragg','planes','Two crystal-plane reflections',
  'The lower reflection travels an extra distance on both approach and departure. Constructive interference requires their combined path excess to be an integer number of wavelengths.',5,'bragg-path')
D('capacitor-geometries','capacitor','cylinder','A coaxial gap gives a logarithmic voltage integral',
  'The concentric cross sections represent long cylindrical conductors. A radial field proportional to inverse radius integrates to the logarithm of the radius ratio.',2,'cylindrical-gap')
D('physical-pendulums','oscillation','torsion','Twisting an elastic support restores the orientation',
  'A torsion wire produces a restoring torque approximately proportional to angular displacement. The disk’s inertia then sets the harmonic angular frequency.',2,'torsion')
D('sound-energy-pipes','waves','beats','Nearby frequencies create a slow beat envelope',
  'Two nearby frequency components add into a fast oscillation with a slowly changing envelope. The rate at which envelope magnitudes repeat is the beat frequency.',6,'beats')
D('sound-energy-pipes','waves','mach','A supersonic source produces a tangent cone',
  'The source has advanced farther than an earlier sound front can travel. The cone is tangent to those earlier spherical fronts; its half-angle decreases as source speed increases.',7,'mach-cone')
D('polarization-refraction','optics','refraction','Refraction changes direction when speed changes',
  'At a stationary boundary the frequency stays fixed. Entering the higher-index lower medium bends the ray toward the dashed normal, as required by Snell’s law.',3,'refraction')
D('quantum-normalization','quantum','box','Box boundaries fix nodes before normalization',
  'The wavefunction must vanish at both infinite walls. Only after this boundary condition selects allowed wavenumbers does normalization determine the overall amplitude.',2,'box-states')
