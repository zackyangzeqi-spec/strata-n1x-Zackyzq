"""Generate machine-local manifest from actual ARM64 artifacts; never load a model."""
from pathlib import Path
import argparse, hashlib, json, struct
p=argparse.ArgumentParser()
p.add_argument('--exe',type=Path,required=True);p.add_argument('--library',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
a=p.parse_args();exe=a.exe.resolve(strict=True);lib=a.library.resolve(strict=True)
raw=exe.read_bytes();off=struct.unpack_from('<I',raw,60)[0]
if raw[off:off+4]!=b'PE\0\0' or struct.unpack_from('<H',raw,off+4)[0]!=0xaa64: raise SystemExit('Expected Windows ARM64 PE')
if a.out.exists():raise SystemExit('Output exists; preserve or remove it deliberately before regenerating')
data={'kind':'local-source-build','platform':'windows-arm64','arch':'deepseek41','version':'0.1.54-n1x-community','source_commit':'870aedd9e1ebe1c91f94da93b59af17729f6c5c0','exe':str(exe),'files':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [exe,lib]}}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Manifest created locally. Do not commit it: it contains machine paths.')
