import numpy as np, glob, os, sys
from PIL import Image
from scipy import ndimage
S = sys.argv[1]
fr = sorted(glob.glob(f'{S}/peekfr3/*.png')); out = []
for f in fr:
    L = np.asarray(Image.open(f).convert('L')).astype(np.float32)
    lab, n = ndimage.label(L > 170)
    seeds = set(np.unique(lab[0, :])) | set(np.unique(lab[:, -1])); seeds.discard(0)
    bg = np.isin(lab, list(seeds))
    bgd = ndimage.binary_dilation(bg, iterations=1)
    a = np.where(bgd, np.clip((255 - L) * 1.25, 0, 255), 255).astype(np.uint8)
    g = np.where(bgd, 17, np.clip(L * 1.06, 0, 255)).astype(np.uint8)
    out.append(Image.merge('RGBA', [Image.fromarray(g)]*3 + [Image.fromarray(a)]))
out[0].save(f'{S}/peek_check.png'); out[-1].save(f'{S}/peek_check_end.png')
M = '/home/claude/ket-tuwaiq-chair/src/media'
out[0].save(f'{M}/gazelle-peek.webp', save_all=True, append_images=out[1:], duration=83, loop=1, quality=55, alpha_quality=70, method=6)
out[-1].save(f'{M}/gazelle-peek-end.webp', quality=85)
print(len(out), out[0].size, os.path.getsize(f'{M}/gazelle-peek.webp'))
