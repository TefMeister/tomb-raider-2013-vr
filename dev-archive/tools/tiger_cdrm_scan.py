"""tiger_cdrm_scan.py - walk every CDRM container in Tomb Raider (2013)'s bigfile.*.tiger archives, inflate its zlib
blocks, and count compiled shaders (DXBC) and names inside them. Reads the game's files only; writes nothing.

CDRM layout as read here (checked by parsing all 171,698 containers with no error, 2026-10-01): 'CDRM', u32 version 0,
u32 block count, u32 pad; then per block u32 (type in the low byte: 1 = stored, 2 = zlib; unpacked size in the
upper 24 bits) and u32 packed size; block data follows, each start aligned to 16 bytes.

Usage: python tiger_cdrm_scan.py   (edit G for another install path)
"""
import mmap, glob, os, struct, zlib, sys
G = r"D:/Program Files (x86)/Steam/steamapps/common/Tomb Raider"
stats = dict(cdrm=0, blocks=0, zlib=0, raw=0, bad=0, dxbc=0, stereo=0, scenebuffer=0)
hits = []
for f in sorted(glob.glob(G + "/bigfile.*.tiger")):
    with open(f, 'rb') as fh:
        m = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
        i = m.find(b'CDRM')
        while i != -1:
            try:
                ver, count = struct.unpack_from('<II', m, i + 4)
                if ver != 0 or not 0 < count < 4096:
                    raise ValueError
                stats['cdrm'] += 1
                p = i + 16 + count * 8
                p = (p + 15) & ~15
                out = bytearray()
                for k in range(count):
                    packed, csize = struct.unpack_from('<II', m, i + 16 + k * 8)
                    kind, usize = packed & 0xff, packed >> 8
                    blob = m[p:p + csize]
                    stats['blocks'] += 1
                    if kind == 2:
                        out += zlib.decompress(blob); stats['zlib'] += 1
                    elif kind == 1:
                        out += blob; stats['raw'] += 1
                    p = (p + csize + 15) & ~15
                if kind == 2 or True:
                    n = out.count(b'DXBC'); s = out.count(b'StereoOffset')
                    stats['dxbc'] += n; stats['stereo'] += s; stats['scenebuffer'] += out.count(b'SceneBuffer')
                    if s and len(hits) < 10:
                        hits.append((os.path.basename(f), hex(i), n, s))
                i = m.find(b'CDRM', p)
            except Exception:
                stats['bad'] += 1
                i = m.find(b'CDRM', i + 4)
        m.close()
    print(os.path.basename(f), stats, flush=True)
print("files with StereoOffset:", hits)
