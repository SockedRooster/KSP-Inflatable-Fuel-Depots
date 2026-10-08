#!/usr/bin/env python3
"""Static asset and config checks; these are NOT a KSP Unity runtime test."""
from pathlib import Path
import struct,re,zipfile,math
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
G=ROOT/'GameData'/'InflataDepot'
MODELS=G/'Models'
PARTS=G/'Parts'
ARCHIVE=ROOT/'dist'/'InflataDepot-rebuilt.zip'
EXPECT={
    '125':dict(capacity=2250,node='size0',scale=.5,diameter=1.25,final=2.45),
    '250':dict(capacity=18000,node='size1',scale=1,diameter=2.5,final=4.9),
    '375':dict(capacity=60750,node='size2',scale=1.5,diameter=3.75,final=7.35),
}

class Reader:
    def __init__(self,path):self.f=path.open('rb');self.end=self.f.seek(0,2);self.f.seek(0);self.names=[];self.meshcount=0;self.tricount=0;self.scale={};self.animation=[];self.colliders=0;self.collider_names=[];self.texnames=[];self.parent_names=[];self.dyn_colliders=[]
    def read(self,fmt):
        sz=struct.calcsize('<'+fmt);dat=self.f.read(sz)
        assert len(dat)==sz,'Unexpected end of MU'
        val=struct.unpack('<'+fmt,dat)
        return val[0] if len(val)==1 else val
    def i(self):return self.read('i')
    def byte(self):return self.read('B')
    def xyz(self):return self.read('fff')
    def string(self):
        length=0;bits=0
        while True:
            x=self.byte();length|=(x&127)<<bits;bits+=7
            if x<128:break
        assert length<100000
        return self.f.read(length).decode()
    def mesh(self):
        assert self.i()==13;nv=self.i();submeshes=self.i()
        assert nv>0 and nv<65535 and submeshes==1
        assert self.i()==14
        for _ in range(nv):self.xyz()
        assert self.i()==15
        for _ in range(nv):self.read('ff')
        assert self.i()==17
        for _ in range(nv):self.xyz()
        assert self.i()==19;inds=self.i();assert inds%3==0
        for _ in range(inds):assert 0<=self.i()<nv
        assert self.i()==22
        self.meshcount+=1;self.tricount+=inds//3
    def anim(self):
        assert self.i()==1;assert self.string()=='inflate';self.xyz();self.xyz();self.i()
        assert self.i()==3
        curves={}
        for prop in ('x','y','z'):
            assert self.string()=='InflatableAssembly'
            assert self.string()=='m_LocalScale.'+prop
            assert self.i()==0;self.i();self.i()
            assert self.i()==2
            keys=[self.read('ffffi') for _ in range(2)]
            assert keys[0][0]==0 and keys[1][0]==20
            assert abs(keys[1][1]-1)<1e-5
            curves[prop]=keys[0][1]
        assert self.string()=='inflate';assert self.byte()==0
        self.animation.append(curves)
    def object(self, parent=None):
        name=self.string();self.names.append(name)
        self.xyz();self.read('ffff');self.scale[name]=self.xyz()
        assert self.i()==24;self.string();self.i()
        while self.f.tell()<self.end:
            tag=self.i()
            if tag==0:self.object(parent=name)
            elif tag==1:return
            elif tag==28:
                self.colliders+=1;self.collider_names.append((name,parent,'box'))
                self.byte();self.xyz();self.xyz()
            elif tag==25:
                self.colliders+=1;self.collider_names.append((name,parent,'convex mesh'))
                is_trigger=self.byte();convex=self.byte()
                assert is_trigger==0 and convex==1, 'Collider must be non-trigger and convex'
                self.mesh()
            elif tag==7:self.mesh()
            elif tag==8:
                self.byte();self.byte();assert self.i()==1;idx=self.i();assert 0<=idx<3
            elif tag==2:self.anim()
            elif tag==10:
                assert self.i()==3
                for _ in range(3):
                    self.string();assert self.string()=='KSP/Diffuse';assert self.i()==2
                    assert self.string()=='_Color';assert self.i()==0;self.read('ffff')
                    assert self.string()=='_MainTex';assert self.i()==4;assert 0<=self.i()<3;self.read('ff');self.read('ff')
            elif tag==12:
                assert self.i()==3
                self.texnames=[]
                for expected in ('fabric','metal','straps'):
                    name=self.string();assert name==expected;assert self.i()==0;self.texnames.append(name)
            else:raise AssertionError(f'Unknown MU tag {tag} at {self.f.tell()-4}')
    def process(self):
        assert self.read('ii')==(76543,5)
        self.string();self.object()
        assert self.f.tell()==self.end
        assert self.meshcount>=10 and self.tricount>9000
        assert self.names.count('InflatableAssembly')==1
        assert self.names.count('DockCollider')==1
        assert 'TopHub' not in self.names and 'Spine' not in self.names
        assert len(self.animation)==1 and self.colliders==2
        assert ('DockCollider','InflataDepot','box') in self.collider_names
        assert ('InflatableCollider','InflatableAssembly','convex mesh') in self.collider_names
        return self

assert len(list(PARTS.glob('*.cfg')))==3
assert len(list(MODELS.glob('*.mu')))==3
for key,p in EXPECT.items():
    basename=f'ID_FoldTank_{key}'
    config=(PARTS/(basename+'.cfg')).read_text()
    assert f'name = {basename}\n' in config
    assert config.count('node_stack_')==1
    assert 'node_stack_bottom =' in config and 'node_stack_top' not in config
    assert 'node_attach' not in config
    assert 'name = ModuleDockingNode' in config
    assert 'referenceAttachNode = bottom' in config
    assert 'nodeType = '+p['node'] in config
    assert 'name = ModuleAnimateGeneric' in config
    assert 'animationName = inflate' in config
    assert config.count('name = ModuleB9PartSwitch')==1
    assert config.count('SUBTYPE')==2
    assert 'switcherDescription = Fuel Configuration' in config
    assert 'tankType = InflataDepot_LFOX' in config and 'tankType = InflataDepot_LF' in config
    assert f'baseVolume = {p["capacity"]}' in config
    assert 'RESOURCE\n' not in config
    assert config.count('{')==config.count('}')
    mu=Reader(MODELS/(basename+'.mu')).process()
    radial=mu.animation[0]['x'];height=mu.animation[0]['y']
    assert math.isclose(radial,p['diameter']/p['final'],rel_tol=1e-5)
    assert math.isclose(height,.09,rel_tol=1e-5)
    assert mu.names.count('DockShell')==1
    print(f'PASS {basename}: {mu.meshcount} meshes, {mu.tricount} triangles; 2 solid colliders (animated membrane + static base); packed scale x/z={radial:.4f}, y={height:.2f}; {p["node"]} docking; 2 tank variants')

fuel=(G/'InflataDepotTankTypes.cfg').read_text()
assert fuel.count('B9_TANK_TYPE')==2
assert fuel.count('percentFilled = 0')==2
assert 'name = InflataDepot_LFOX' in fuel and 'name = InflataDepot_LF' in fuel
assert 'unitsPerVolume = 0.45' in fuel and 'unitsPerVolume = 0.55' in fuel
assert 'unitsPerVolume = 1\n' in fuel
for f in MODELS.glob('*.png'):
    with Image.open(f) as img:img.verify()
if ARCHIVE.exists():
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert sum(x.startswith('GameData/InflataDepot/Parts/') for x in names)==3
print('PASS fuel types + PNGs; optional regenerated archive integrity check')
print('NOTE: Static validation only. New COLLISION behavior in-game has NOT been tested.')
