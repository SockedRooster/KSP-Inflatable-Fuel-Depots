#!/usr/bin/env python3
"""Generate native KSP1 .mu model, wrap textures, and configs for InflataDepot.
No Blender or external plugin DLL required for the basic animation.
Rebuilding assets requires Python, NumPy, and Pillow.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math, struct, zipfile, re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent if HERE.name == 'Source' else HERE
GAMEDATA=ROOT/'GameData'/'InflataDepot'
MODEL=GAMEDATA/'Models'
PARTS=GAMEDATA/'Parts'
MODEL.mkdir(parents=True,exist_ok=True)
PARTS.mkdir(parents=True,exist_ok=True)

# --- Procedural hand-painted UV textures ---
rng=np.random.default_rng(73518)
SIZE=1024
y,x=np.mgrid[0:SIZE,0:SIZE]
# Folded white ceramic-fabric look, with longitudinal seams, ripples and woven grain.
weave=1.7*np.cos(2*np.pi*x/5.7)*np.cos(2*np.pi*y/5.7)
wrinkle=3.2*np.sin(x*0.11+y*0.013)+2.2*np.sin(y*0.32+x*.037)
base=216 + weave+wrinkle + rng.normal(0,1.2,(SIZE,SIZE))
base-=7*(np.sin(2*np.pi*x/(SIZE/12))**24)
arr=np.stack([base+3,base+7,base+11],axis=-1)
arr=np.uint8(np.clip(arr,0,255))
im=Image.fromarray(arr,'RGB')
d=ImageDraw.Draw(im)
for xx in range(0,SIZE+1,85):
    d.line([(xx,0),(xx,SIZE)],fill=(100,122,134),width=3)
    d.line([(xx+3,0),(xx+3,SIZE)],fill=(245,245,240),width=2)
    for yy in range(14,SIZE,26):
        d.line([(xx-5,yy),(xx+5,yy+2)], fill=(126,149,158),width=1)
for yy in [80,950]:
    d.rectangle([0,yy,SIZE,yy+12],fill=(104,127,138))
    d.line([(0,yy+14),(SIZE,yy+14)],fill=(247,238,203),width=3)
# Brand label at UV middle, useful for identification in VAB.
d.rounded_rectangle([376,410,650,515],radius=17,fill=(38,60,74),outline=(225,190,89),width=6)
d.text((407,435),'INFLATA',fill=(244,246,248))
d.text((452,469),'DEPOT',fill=(240,199,88))
im.save(MODEL/'fabric.png',compress_level=6)

size=512
y,x=np.mgrid[0:size,0:size]
noise=rng.normal(0,3,(size,size))
streak=5*np.cos(y*.19)+2*np.sin(y*.039)
base=112+noise+streak
metal=np.stack([base+10,base+25,base+31],axis=-1)
mim=Image.fromarray(np.uint8(np.clip(metal,0,255)),'RGB')
d=ImageDraw.Draw(mim)
for xx in [24,250,487]:
    d.line([(xx,0),(xx,511)],fill=(53,68,76),width=4)
    for yy in range(30,500,54):
        d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=(192,203,206),outline=(50,60,70))
d.rectangle((4,4,507,507),outline=(39,52,64),width=8)
mim.save(MODEL/'metal.png')

b=Image.new('RGB',(512,512),(205,143,50));d=ImageDraw.Draw(b)
for xx in range(-300,800,60):
    d.polygon([(xx,0),(xx+25,0),(xx+280,512),(xx+255,512)],fill=(47,54,61))
for yy in range(0,512,32):
    d.line((0,yy,512,yy),fill=(224,169,73),width=1)
b.save(MODEL/'straps.png')

# --- Meshes: KSP1/Unity left-handed coordinates; local +Y is deployment ---
class Mesh:
    def __init__(self):
        self.verts=[];self.normals=[];self.uv=[];self.tris=[]
    def add(self,pos,normal,uv):
        self.verts.append(pos);self.normals.append(normal);self.uv.append(uv)
        return len(self.verts)-1
    def tri(self,a,b,c):self.tris.append((a,b,c))
    def stitch(self,rings,n):
        for lo,hi in zip(rings,rings[1:]):
            for j in range(n):
                a,b,c,d=lo[j],hi[j],lo[j+1],hi[j+1]
                self.tri(a,b,c);self.tri(c,b,d)

def cyl(radius,y0,y1,segments=64):
    m=Mesh();rings=[]
    for yy,t in [(y0,0),(y1,1)]:
        row=[]
        for j in range(segments+1):
            a=2*math.pi*j/segments;c,s=math.cos(a),math.sin(a)
            row.append(m.add((radius*c,yy,radius*s),(c,0,s),(j/segments,t)))
        rings.append(row)
    m.stitch(rings,segments)
    return m

def torus(major,minor,ypos,segments=72,tube=12):
    m=Mesh();rings=[]
    for k in range(tube+1):
        phi=2*math.pi*k/tube;rr=major+minor*math.cos(phi)
        y=ypos+minor*math.sin(phi);row=[]
        for j in range(segments+1):
            th=2*math.pi*j/segments;c,s=math.cos(th),math.sin(th)
            row.append(m.add((rr*c,y,rr*s),(c*math.cos(phi),math.sin(phi),s*math.cos(phi)),(j/segments,k/tube)))
        rings.append(row)
    m.stitch(rings,segments)
    return m

def inflatable_drum(radius, height, ybase, segments=96):
    """Cylinder with modestly convex caps, soft rounded shoulders, and textile panels.

    Entire geometry sits ABOVE the bottom docking base so scaling its Y axis
    leaves the docking interface stationary throughout the deploy animation.
    """
    m=Mesh(); rings=[]
    profile=[
        (0.02,0.018),(.20,0.018),(.55,0.019),(.79,0.032),(.92,0.060),
        (0.985,0.105),(1,0.140),(1,0.23),(1,0.40),(1,0.60),(1,0.77),
        (1,0.86),(.985,.895),(.92,.94),(.79,.968),(.55,.981),(.20,.982),(.02,.982),
    ]
    for k,(factor,hy) in enumerate(profile):
        row=[]
        for j in range(segments+1):
            th=2*math.pi*j/segments;c,s=math.cos(th),math.sin(th)
            # subtle 12-panel scallops across the flexible membrane
            rad=radius*factor*(1-.005*math.cos(12*th))
            yy=ybase+height*hy
            # Endcap normals blend toward Y using profile gradient
            prev=profile[max(0,k-1)];nxt=profile[min(len(profile)-1,k+1)]
            dx=(nxt[0]-prev[0])*radius;dy=(nxt[1]-prev[1])*height
            radial=max(-1.,min(1.,dy/(abs(dx)+abs(dy)+1.e-6)))
            vertical=max(-1.,min(1.,-dx/(abs(dx)+abs(dy)+1.e-6)))
            norm=(radial*c,vertical,radial*s)
            mag=math.sqrt(sum(v*v for v in norm)) or 1
            row.append(m.add((rad*c,yy,rad*s),tuple(v/mag for v in norm),(j/segments,hy)))
        rings.append(row)
    m.stitch(rings,segments)
    return m


# --- Simple low-polygon convex collider following the animated membrane ---
def inflatable_collision_mesh(radius, height, ybase, segments=16):
    """Slightly inset convex closed cylinder with tapered ends (66 vertices).

    Attached to InflatableAssembly, so the existing KSP inflation scale
    curves scale this collider in every axis, including after save/load.
    This is a preview physics feature: test carefully before release.
    """
    m=Mesh(); rings=[]
    profile=[(.75,.09),(.945,.175),(.945,.825),(.75,.91)]
    for f,yf in profile:
        row=[]
        for j in range(segments):
            th=2*math.pi*j/segments; c,si=math.cos(th),math.sin(th)
            row.append(m.add((radius*f*c,ybase+height*yf,radius*f*si),(c,0,si),(j/segments,yf)))
        rings.append(row)
    for a,b in zip(rings,rings[1:]):
        for j in range(segments):
            k=(j+1)%segments
            m.tri(a[j],b[j],a[k]);m.tri(a[k],b[j],b[k])
    bot=m.add((0,ybase+height*.052,0),(0,-1,0),(.5,.5))
    top=m.add((0,ybase+height*.948,0),(0,1,0),(.5,.5))
    for j in range(segments):
        k=(j+1)%segments
        m.tri(bot,rings[0][j],rings[0][k])
        m.tri(top,rings[-1][k],rings[-1][j])
    return m

# --- Independent KSP .mu v5 writer (animation not yet game-validated) ---
class Binary:
    def __init__(self,path):self.file=open(path,'wb')
    def close(self):self.file.close()
    def i(self,*values):self.file.write(struct.pack('<'+'i'*len(values),*values))
    def f(self,*values):self.file.write(struct.pack('<'+'f'*len(values),*values))
    def b(self,n):self.file.write(bytes([n]))
    def string(self,s):
        val=s.encode('utf-8');n=len(val)
        while n>=128:self.b((n&127)|128);n>>=7
        self.b(n);self.file.write(val)
    def xyz(self,p):self.f(*p)

def transform(w,name,pos=(0,0,0),sc=(1,1,1),mesh=None,mat=None,collider=None,collider_mesh=None):
    w.string(name);w.xyz(pos);w.f(0,0,0,1);w.xyz(sc)
    w.i(24);w.string('Untagged');w.i(0)
    if collider is not None:
        w.i(28);w.b(0);w.xyz(collider);w.xyz((0,0,0))
    if collider_mesh is not None:
        # ET_MESH_COLLIDER2 = 25, isTrigger = false, convex = true.
        m=collider_mesh
        w.i(25);w.b(0);w.b(1)
        w.i(13,len(m.verts),1)
        w.i(14)
        for vertex in m.verts:w.xyz(vertex)
        w.i(15)
        for uv in m.uv:w.f(*uv)
        w.i(17)
        for norm in m.normals:w.xyz(norm)
        w.i(19,len(m.tris)*3)
        for tri in m.tris:w.i(*tri)
        w.i(22)
    if mesh is not None:
        if len(mesh.verts)>=65535:raise ValueError('Mesh too large for MU legacy indices')
        w.i(7);w.i(13,len(mesh.verts),1)
        w.i(14)
        for pos in mesh.verts:w.xyz(pos)
        w.i(15)
        for u,v in mesh.uv:w.f(u,v)
        w.i(17)
        for norm in mesh.normals:w.xyz(norm)
        w.i(19,len(mesh.tris)*3)
        for tri in mesh.tris:w.i(*tri)
        w.i(22)
        w.i(8);w.b(1);w.b(1);w.i(1,mat)

def animate(w,packed_radial,packed_height,bounds):
    w.i(2,1);w.string('inflate')
    w.xyz((0,0,0));w.xyz(bounds);w.i(1)
    w.i(3)
    for prop,a in [('m_LocalScale.x',packed_radial),('m_LocalScale.y',packed_height),('m_LocalScale.z',packed_radial)]:
        w.string('InflatableAssembly');w.string(prop);w.i(0,1,1,2)
        slope=(1-a)/20
        for t,val in [(0,a),(20,1.)]:
            w.f(t,val,slope,slope);w.i(0)
    w.string('inflate');w.b(0)

def child(w,name,mesh,material):
    w.i(0);transform(w,name,mesh=mesh,mat=material);w.i(1)

def build_mu(p):
    # The 2.5m prototype's body expands to ~4.9m wide, ~4.7m high.
    s=p['scale'];radius=2.45*s;height=4.70*s;base=0.115*s
    radial=p['diameter']/(2*radius)
    packed_height=0.09
    dock=p['dockrad']
    out=MODEL/(p['id']+'.mu');w=Binary(out)
    w.i(76543,5);w.string(p['id'])
    transform(w,'InflataDepot')
    animate(w,radial,packed_height,(radius*2,height+base,radius*2))
    # A single permanent underside dock base. No top hub, no top stack node.
    child(w,'DockShell',cyl(dock*1.08,-.31*s,.12*s),1)
    child(w,'DockLowerLip',torus(dock*1.03,.043*s,-.32*s),1)
    child(w,'DockFaceGuide',torus(dock*.82,.027*s,-.325*s),1)
    child(w,'DockUpperCollar',torus(dock*1.10,.035*s,.075*s),1)
    child(w,'DockSocket',cyl(dock*.46,-.34*s,-.12*s),1)
    # Fixed metal docking base collider. The membrane has its own animated collider below.
    w.i(0)
    transform(w,'DockCollider',collider=(dock*2.2,.44*s,dock*2.2))
    w.i(1)
    w.i(0)
    transform(w,'InflatableAssembly',sc=(radial,packed_height,radial))
    child(w,'FabricCylinder',inflatable_drum(radius,height,base),0)
    # Collider is INSIDE the inflatable subtree (not the rigid docking base).
    # It grows with the animation and has a flat-ish cylindrical footprint.
    w.i(0)
    transform(w,'InflatableCollider',collider_mesh=inflatable_collision_mesh(radius,height,base))
    w.i(1)
    for idx,fract in enumerate([.15,.34,.52,.70,.85]):
        child(w,f'RestraintBand{idx:02d}',torus(radius+.006*s,.025*s,base+height*fract),2)
    w.i(1)
    w.i(10,3)
    for mat,idx in [('FabricCeramic',0),('DockTitanium',1),('ReinforcedBands',2)]:
        w.string(mat);w.string('KSP/Diffuse');w.i(2)
        w.string('_Color');w.i(0);w.f(1,1,1,1)
        w.string('_MainTex');w.i(4,idx);w.f(1,1);w.f(0,0)
    w.i(12,3)
    for tx in ['fabric','metal','straps']:w.string(tx);w.i(0)
    w.close()
    return out

# KSP part names intentionally kept for save compatibility with LF/OX beta IDs.
parts=[
    dict(id='ID_FoldTank_125',diameter=1.25,scale=.5,size='1.25 m',dockrad=.31,docktype='size0',capacity=2250,mass=.38,cost=2800,entry=6000,profile='size1',node=1,tech='advFuelSystems',docklabel='Clamp-O-Tron Jr.'),
    dict(id='ID_FoldTank_250',diameter=2.5,scale=1.,size='2.5 m',dockrad=.625,docktype='size1',capacity=18000,mass=2.2,cost=10000,entry=17500,profile='size2',node=2,tech='largeVolumeContainment',docklabel='Clamp-O-Tron'),
    dict(id='ID_FoldTank_375',diameter=3.75,scale=1.5,size='3.75 m',dockrad=1.25,docktype='size2',capacity=60750,mass=7.0,cost=27500,entry=38000,profile='size3',node=3,tech='largeVolumeContainment',docklabel='Clamp-O-Tron Sr.'),
]
for path in PARTS.glob('*.cfg'):path.unlink()
for path in MODEL.glob('*.mu'):path.unlink()

# Tank types use UNIQUE names to avoid collisions with other mods.
# KSP tank-volume units: LF/OX 0.45 LF + 0.55 OX; LF 1.0 LF.
(GAMEDATA/'InflataDepotTankTypes.cfg').write_text("""B9_TANK_TYPE
{
    name = InflataDepot_LFOX
    title = LF + Oxidizer
    tankMass = 0
    tankCost = 0
    percentFilled = 0
    RESOURCE
    {
        name = LiquidFuel
        unitsPerVolume = 0.45
    }
    RESOURCE
    {
        name = Oxidizer
        unitsPerVolume = 0.55
    }
}
B9_TANK_TYPE
{
    name = InflataDepot_LF
    title = Liquid Fuel Only
    tankMass = 0
    tankCost = 0
    percentFilled = 0
    RESOURCE
    {
        name = LiquidFuel
        unitsPerVolume = 1
    }
}
""")

for p in parts:
    model=build_mu(p)
    bottom=round(-.33*p['scale'],5)
    part=f"""PART
{{
    name = {p['id']}
    module = Part
    author = SockedRooster
    MODEL
    {{
        model = InflataDepot/Models/{p['id']}
    }}
    rescaleFactor = 1
    node_stack_bottom = 0.0, {bottom}, 0.0, 0.0, -1.0, 0.0, {p['node']}
    TechRequired = {p['tech']}
    entryCost = {p['entry']}
    cost = {p['cost']}
    category = FuelTank
    subcategory = 0
    title = ID-{int(p['diameter']*100):03} Pancake Inflatable Fuel Depot
    manufacturer = Inflata Aerospace Works
    description = Launch as a compact pancake. After reaching orbit inflate into a cylindrical propellant depot, then fill it from tankers. The only attach/dock port is on the rigid bottom face. Configure propellant with B9 Part Switch in the VAB. Requires B9 Part Switch and ModuleManager.
    attachRules = 1,0,1,1,0
    bulkheadProfiles = {p['profile']}
    tags = inflatable pancake deploy cylinder orbital depot refuel docking storage liquidfuel oxidizer
    mass = {p['mass']}
    dragModelType = default
    maximum_drag = 0.2
    minimum_drag = 0.2
    angularDrag = 2
    crashTolerance = 10
    breakingForce = 250
    breakingTorque = 250
    maxTemp = 2000
    skinMaxTemp = 2500
    fuelCrossFeed = True

    MODULE
    {{
        name = ModuleDockingNode
        referenceAttachNode = bottom
        nodeType = {p['docktype']}
        stagingEnabled = False
    }}
    MODULE
    {{
        name = ModuleAnimateGeneric
        animationName = inflate
        startEventGUIName = Inflate Fuel Depot
        endEventGUIName = Inflated
        actionGUIName = Inflate Fuel Depot
        animSpeed = 1
        isOneShot = true
        eventAvailableEditor = false
        eventAvailableFlight = true
        eventAvailableEVA = false
        instantAnimInEditor = true
        allowDeployLimit = false
    }}
    MODULE
    {{
        name = ModuleB9PartSwitch
        moduleID = InflataFuel
        switcherDescription = Fuel Configuration
        switcherDescriptionPlural = Fuel Configurations
        baseVolume = {p['capacity']}
        switchInFlight = false
        SUBTYPE
        {{
            name = LFOX
            title = LF + Oxidizer
            tankType = InflataDepot_LFOX
            descriptionSummary = Standard bipropellant storage, empty at launch.
        }}
        SUBTYPE
        {{
            name = LF
            title = Liquid Fuel Only
            tankType = InflataDepot_LF
            descriptionSummary = All tank volume allocated to LiquidFuel, empty at launch.
        }}
    }}
}}
"""
    (PARTS/(p['id']+'.cfg')).write_text(part)
    print('MODEL',model.name,model.stat().st_size,'PART',p['size'],'capacity',p['capacity'])

# Release metadata/documentation are intentionally maintained separately.
# Regeneration overwrites GameData assets; review resulting diffs before publishing.
zip_path=ROOT/'dist'/'InflataDepot-rebuilt.zip'
zip_path.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for f in sorted(GAMEDATA.rglob('*')):
        if f.is_file():z.write(f,f.relative_to(ROOT))
print('Rebuilt GameData ZIP:',zip_path, '(',zip_path.stat().st_size,'bytes)')
