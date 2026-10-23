from PIL import Image
import glob, os
S='gz3d'; M='/home/claude/ket-tuwaiq-chair/src/media'
bb = eval(open(f'{S}/bbox.txt').read()); W = 264; H = round(W * (bb[3]-bb[1]) / (bb[2]-bb[0]))
for n in ('walk','idle'):
    fr = [Image.open(f).convert('RGBA').crop(bb).resize((W,H), Image.LANCZOS) for f in sorted(glob.glob(f'{S}/{n}_frames/*.webp'))[::2]]
    fr[0].save(f'{M}/gazelle-{n}.webp', save_all=True, append_images=fr[1:], duration=83, loop=0, quality=70, alpha_quality=80, method=6, minimize_size=True, kmin=3, kmax=24)
    print(n, len(fr), (W,H), os.path.getsize(f'{M}/gazelle-{n}.webp'))
