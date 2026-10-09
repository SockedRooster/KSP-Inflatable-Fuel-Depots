#!/usr/bin/env python3
"""Check that an InflataDepot release ZIP has the expected installable structure."""
from zipfile import ZipFile
from pathlib import Path
import sys

p = Path(sys.argv[1]) if len(sys.argv)>1 else Path('InflataDepot-v1.0.0.zip')
with ZipFile(p) as z:
    assert z.testzip() is None, 'Corrupt ZIP member'
    names=set(z.namelist())
    expected={
       'LICENSE','README.md','CHANGELOG.md',
       'GameData/InflataDepot/Plugins/InflataDepotPlugin.dll',
       'GameData/InflataDepot/InflataDepotFuelLock.cfg',
       'GameData/InflataDepot/InflataDepotTankTypes.cfg',
       'GameData/InflataDepot/Compatibility/VABOrganizer.cfg',
    }
    for size in ('125','250','375'):
        expected.add(f'GameData/InflataDepot/Models/ID_FoldTank_{size}.mu')
        expected.add(f'GameData/InflataDepot/Parts/ID_FoldTank_{size}.cfg')
    missing=expected-names
    assert not missing, f'Missing files: {sorted(missing)}'
    assert all(n.startswith('GameData/InflataDepot/') or n in {'LICENSE','README.md','CHANGELOG.md'} for n in names)
    for size in ('125','250','375'):
        cfg=z.read(f'GameData/InflataDepot/Parts/ID_FoldTank_{size}.cfg').decode('utf-8')
        for phrase in ('category = FuelTank','TechRequired = advFuelSystems','organizerSubcategory = lfo','ModuleB9PartSwitch','ModuleDockingNode'):
            assert phrase in cfg, f'{size}: missing {phrase}'
    for token in ('ModuleInflataFuelLock', 'nominalVolume'):
        assert token.encode() in z.read('GameData/InflataDepot/InflataDepotFuelLock.cfg')
print(f'PASS: {p.name}, {len(names)} release files, 3 configured tanks, plugin included')
