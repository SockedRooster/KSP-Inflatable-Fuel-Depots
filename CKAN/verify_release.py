#!/usr/bin/env python3
"""Review-only packaging checks for InflataDepot; cannot replace in-game/NetKAN testing."""
from pathlib import Path
import hashlib, zipfile, sys, re
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
G=ROOT/'GameData'/'InflataDepot'
assert G.exists()
cfgs=list((G/'Parts').glob('*.cfg'))
assert len(cfgs)==3
ids=[]
for cfg in cfgs:
    c=cfg.read_text()
    ids.append(re.search(r'(?m)^\s*name = (ID_FoldTank_\d+)',c).group(1))
    assert c.count('node_stack_')==1 and 'node_stack_bottom' in c
    assert c.count('name = ModuleDockingNode')==1
    assert c.count('name = ModuleB9PartSwitch')==1
    assert 'tankType = InflataDepot_LFOX' in c and 'tankType = InflataDepot_LF' in c
    assert 'isOneShot = true' in c and 'animationName = inflate' in c
assert sorted(ids)==['ID_FoldTank_125','ID_FoldTank_250','ID_FoldTank_375']
assert len(list((G/'Models').glob('*.mu')))==3
assert len(list((G/'Models').glob('*.png')))==3
print('PASS Three tank sizes, one bottom node per tank, deployment and two B9 fuel options')
print('PASS Unique part IDs and three native models')
print('NOT CHECKED: KSP in-game behavior, compatibility and true CKAN indexing')
