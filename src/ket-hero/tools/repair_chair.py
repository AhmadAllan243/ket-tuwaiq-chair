"""
Re-splits the AI-generated Tuwaiq chair into clean parts and closes the holes.

The source GLB is one fused surface cut into ChairBase / SeatCushion / SeatBack, but the
cut is poor: the backrest is only an outer skin, ChairBase carries the backrest front and
both seat ends, and SeatCushion carries a stray piece of metal leg. Faces are reassigned
by texture colour (black = metal, orange = wood, everything else = fabric) and position,
then every remaining boundary loop is capped with a flat patch in a matching colour.

usage: python3 repair_chair.py in.glb out.glb [fabric-photo.png]

Patches (closed openings + recoloured lining) get a seamless swatch cut from a real product
photo, box-projected so it doesn't stretch; the missing rear corners of the top rail are rebuilt
as metal tube.
"""
import sys, colorsys
import numpy as np, trimesh
from scipy.sparse import coo_matrix

SRC, DST = sys.argv[1], sys.argv[2]
FABRIC_PHOTO = sys.argv[3] if len(sys.argv) > 3 else None
sc = trimesh.load(SRC, process=False)
parts = {}
for node in sc.graph.nodes_geometry:
    T, gname = sc.graph[node]
    parts[node] = sc.geometry[gname]
mat = parts['ChairBase'].visual.material
tex = np.asarray(mat.baseColorTexture.convert('RGB')) / 255.0
H, W = tex.shape[:2]

def sample(uv):
    px = np.clip((uv[..., 0] * W).astype(int), 0, W - 1)
    py = np.clip(((1 - uv[..., 1]) * H).astype(int), 0, H - 1)
    return tex[py, px]

def classify(m):
    """per-face: 0 fabric, 1 metal, 2 wood (median of centroid + 3 corners)"""
    uv = m.visual.uv[m.faces]                          # F,3,2
    pts = np.concatenate([uv, uv.mean(1, keepdims=True)], 1)
    c = np.median(sample(pts), axis=1)                 # F,3
    mx, mn = c.max(1), c.min(1)
    v = mx; s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    h = np.array([colorsys.rgb_to_hsv(*x)[0] for x in c])
    lab = np.zeros(len(c), int)
    lab[v < 0.16] = 1
    lab[(h > 0.05) & (h < 0.11) & (s > 0.45) & (v > 0.45)] = 2
    return lab

def topo(m):
    q = np.round(m.vertices, 5)
    _, inv = np.unique(q, axis=0, return_inverse=True)
    return inv.reshape(-1)

def smooth(m, lab, iters=3):
    """majority filter over edge-adjacent faces, so texture noise doesn't speckle the split"""
    t = topo(m); f = t[m.faces]
    e = np.vstack([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]]); e.sort(1)
    fid = np.tile(np.arange(len(f)), 3)
    key = e[:, 0].astype(np.int64) * (t.max() + 1) + e[:, 1]
    order = np.argsort(key); key, fid = key[order], fid[order]
    same = key[1:] == key[:-1]
    a, b = fid[:-1][same], fid[1:][same]
    adj = coo_matrix((np.ones(len(a) * 2), (np.r_[a, b], np.r_[b, a])), shape=(len(f), len(f))).tocsr()
    for _ in range(iters):
        votes = np.stack([adj @ (lab == k).astype(float) for k in range(3)], 1)
        votes[np.arange(len(lab)), lab] += 0.5
        lab = votes.argmax(1)
    return lab

def components(m, faces_idx):
    """connected components (by shared vertex position) of a face subset; returns list of index arrays"""
    from scipy.sparse.csgraph import connected_components
    if len(faces_idx) == 0: return []
    t = topo(m); f = t[m.faces[faces_idx]]
    n = t.max() + 1
    rows = np.r_[f[:, 0], f[:, 1], f[:, 2]]; cols = np.r_[f[:, 1], f[:, 2], f[:, 0]]
    A = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    _, lab = connected_components(A, directed=False)
    fl = lab[f[:, 0]]
    return [faces_idx[fl == k] for k in np.unique(fl)]

def is_sheet(m, idx):
    """flat dark panels (cushion undersides) vs thin metal tubes: area relative to the two largest extents"""
    tri = m.triangles[idx]; area = trimesh.triangles.area(tri).sum()
    ext = np.sort(np.ptp(tri.reshape(-1, 3), 0))[::-1]
    return ext[1] > 0.12 and area / max(ext[0] * ext[1], 1e-6) > 0.55

pieces = {k: [] for k in ['ChairBase', 'SeatCushion', 'SeatBack']}   # (mesh, face mask)
LABELS, DEST = {}, {}
for name, m in parts.items():
    lab = smooth(m, classify(m)); LABELS[id(m)] = lab
    cen = m.triangles_center
    x, y, z = cen[:, 0], cen[:, 1], cen[:, 2]
    dest = np.full(len(lab), name, dtype=object)
    fabric = lab == 0
    cushion_of = lambda yy, zz: np.where((zz < -0.2) & (yy > 0.12), 'SeatBack', 'SeatCushion')
    dest[fabric] = cushion_of(y[fabric], z[fabric])
    # dark/wood faces: thin tubes and arms belong to the frame, flat dark panels to a cushion
    for comp in components(m, np.where(~fabric)[0]):
        if lab[comp].max() == 2 or not is_sheet(m, comp):
            dest[comp] = 'ChairBase'
        else:
            cc = cen[comp].mean(0); dest[comp] = cushion_of(np.array([cc[1]]), np.array([cc[2]]))[0]
    DEST[id(m)] = (m, dest)

# dark faces sitting inside a cushion's footprint are that cushion's lining, not frame
def body_box(part):
    pts = [m.triangles_center[(d == part) & (LABELS[id(m)] == 0)] for m, d in DEST.values()]
    pts = np.vstack(pts); return np.quantile(pts, 0.01, 0), np.quantile(pts, 0.99, 0)
for part, pad in (('SeatCushion', 0.05), ('SeatBack', 0.04)):
    lo, hi = body_box(part)
    for m, d in DEST.values():
        c = m.triangles_center; lab = LABELS[id(m)]
        inside = np.all((c > lo + [pad, -0.12, pad]) & (c < hi - [pad, 0.0, pad]), 1)
        mv = inside & (lab == 1) & (d == 'ChairBase')
        for comp in components(m, np.where(mv)[0]):      # tubes stay with the frame
            if len(comp) < 400 and not is_sheet(m, comp): mv[comp] = False
        d[mv] = part
        if mv.any(): print(f'lining -> {part}: {int(mv.sum())} faces')
for m, d in DEST.values():
    for k in pieces:
        sel = d == k
        if sel.any(): pieces[k].append((m, sel))

# loose fragments: hand every small connected piece to whichever part's main body is nearest
from scipy.spatial import cKDTree
def masks_to_faces(name):
    return [(m, np.where(sel)[0]) for m, sel in pieces[name]]
bodies, frags = {}, []
for name in pieces:
    pts = []
    for m, idx in masks_to_faces(name):
        for comp in components(m, idx):
            if len(comp) >= 400: pts.append(m.triangles_center[comp])
            else: frags.append((name, m, comp))
    bodies[name] = cKDTree(np.vstack(pts))
moved = 0
for name, m, comp in frags:
    c = m.triangles_center[comp].mean(0)
    best = min(bodies, key=lambda k: bodies[k].query(c)[0])
    if best != name:
        for i, (mm, sel) in enumerate(pieces[name]):
            if mm is m: sel = sel.copy(); sel[comp] = False; pieces[name][i] = (mm, sel)
        hit = [i for i, (mm, _) in enumerate(pieces[best]) if mm is m]
        if hit:
            mm, sel = pieces[best][hit[0]]; sel = sel.copy(); sel[comp] = True; pieces[best][hit[0]] = (mm, sel)
        else:
            sel = np.zeros(len(m.faces), bool); sel[comp] = True; pieces[best].append((m, sel))
        moved += 1
print('fragments re-homed:', moved, 'of', len(frags))

def build(chunks, patch=False, hidden_zone=None):
    """gathers the selected faces; on cushions, dark lining panels are returned separately
    (as triangle soup) so they can wear the fabric swatch"""
    V, N, UV, F, off = [], [], [], [], 0
    soup = []
    for m, sel in chunks:
        keep = sel.copy()
        if patch:
            extra = sel & (LABELS[id(m)] == 1)
            for comp in components(m, np.where(extra)[0]):   # keep thin dark piping as it is
                if len(comp) < 400 and not is_sheet(m, comp): extra[comp] = False
            if hidden_zone is not None:   # dark-baked area the backrest covers when assembled
                uvc = m.visual.uv[m.faces].mean(1)
                extra |= sel & hidden_zone(m.triangles_center) & (sample(uvc).max(1) < 0.42)
            keep &= ~extra
            if extra.any(): soup.append(m.triangles[extra]); print(f'  {int(extra.sum())} lining faces -> fabric swatch')
        sub = m.faces[keep]; used, inv = np.unique(sub, return_inverse=True)
        V.append(m.vertices[used]); UV.append(m.visual.uv[used])
        N.append(m.vertex_normals[used]); F.append(inv.reshape(-1, 3) + off); off += len(used)
    soup = np.vstack(soup) if soup else np.zeros((0, 3, 3))
    return np.vstack(V), np.vstack(N), np.vstack(UV), np.vstack(F), soup

def fabric_uv():
    """a texel whose colour is close to the median fabric colour — used for caps"""
    ys, xs = np.mgrid[0:H:8, 0:W:8]; c = tex[ys, xs].reshape(-1, 3)
    mx = c.max(1); keep = (mx > 0.3) & (c[:, 0] > c[:, 2])
    med = np.median(c[keep], 0); i = np.argmin(((c - med) ** 2).sum(1) + (~keep) * 9)
    return np.array([xs.reshape(-1)[i] / W, 1 - ys.reshape(-1)[i] / H]), med

def metal_uv():
    """the darkest, flattest texel in the atlas: matches the black frame"""
    ys, xs = np.mgrid[0:H:4, 0:W:4]; c = tex[ys, xs].reshape(-1, 3)
    i = np.argmin(c.max(1) * 3 + c.std(1))
    return np.array([xs.reshape(-1)[i] / W, 1 - ys.reshape(-1)[i] / H])

FAB_UV, FAB_RGB = fabric_uv(); MET_UV = metal_uv()

def cap_triangles(V, F, min_edges=3, max_extent=10.0):
    """Closes every cluster of open edges with a fan to its centroid; edge-by-edge, so branching
    boundaries (common on AI-generated meshes) still close. Returns triangle soup."""
    from scipy.sparse.csgraph import connected_components
    q = np.round(V, 5); _, t = np.unique(q, axis=0, return_inverse=True); t = t.reshape(-1)
    rep = np.zeros(t.max() + 1, int); rep[t] = np.arange(len(t))
    tf = t[F]
    he = np.vstack([tf[:, [0, 1]], tf[:, [1, 2]], tf[:, [2, 0]]])
    und = np.sort(he, 1); key = und[:, 0].astype(np.int64) * (t.max() + 1) + und[:, 1]
    _, inv, cnt = np.unique(key, return_inverse=True, return_counts=True)
    bnd = he[cnt[inv] == 1]
    if len(bnd) == 0: return np.zeros((0, 3, 3)), 0, 0
    n = t.max() + 1
    A = coo_matrix((np.ones(len(bnd)), (bnd[:, 0], bnd[:, 1])), shape=(n, n))
    _, lab = connected_components(A, directed=False)
    elab = lab[bnd[:, 0]]
    tris, count = [], 0
    for k in np.unique(elab):
        E = bnd[elab == k]
        if len(E) < min_edges: continue
        P = V[rep[np.unique(E)]]
        if np.ptp(P, 0).max() > max_extent: continue
        c = P.mean(0)
        a, b = V[rep[E[:, 0]]], V[rep[E[:, 1]]]
        tris.append(np.stack([b, a, np.broadcast_to(c, a.shape)], 1))   # opposite winding to the open half-edge
        count += 1
    return (np.vstack(tris) if tris else np.zeros((0, 3, 3))), count, len(bnd)

def box_uv_mesh(tris, scale=0.42):
    """triangle soup -> mesh with box-projected UVs (per-triangle dominant axis, no stretching)"""
    tris = np.asarray(tris); n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    ax = np.abs(n).argmax(1)
    V = tris.reshape(-1, 3); axr = np.repeat(ax, 3)
    U = np.where(axr == 0, V[:, 2], V[:, 0]); W = np.where(axr == 1, V[:, 2], V[:, 1])
    UV = np.stack([U, W], 1) / scale
    F = np.arange(len(V)).reshape(-1, 3)
    m = trimesh.Trimesh(V, F, process=False)
    return m, UV

def tube(points, radius, segments=14, samples=90):
    """smooth metal tube along a Catmull-Rom curve through points"""
    P = np.asarray(points, float)
    def cr(p0, p1, p2, p3, t):
        return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
    ext = np.vstack([P[0] * 2 - P[1], P, P[-1] * 2 - P[-2]])
    C = []
    per = max(2, samples // (len(P) - 1))
    for i in range(1, len(ext) - 2):
        for t in np.linspace(0, 1, per, endpoint=False): C.append(cr(ext[i - 1], ext[i], ext[i + 1], ext[i + 2], t))
    C.append(P[-1]); C = np.array(C)
    T = np.gradient(C, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
    up = np.array([0, 1.0, 0]); Vs, Ns = [], []
    for c, tng in zip(C, T):
        nrm = np.cross(tng, up); nrm /= max(np.linalg.norm(nrm), 1e-9); bi = np.cross(tng, nrm)
        for k in range(segments):
            a = 2 * np.pi * k / segments; d = np.cos(a) * nrm + np.sin(a) * bi
            Vs.append(c + radius * d); Ns.append(d)
    Fs = []
    for i in range(len(C) - 1):
        for k in range(segments):
            a, b = i * segments + k, i * segments + (k + 1) % segments
            c2, d2 = a + segments, b + segments
            Fs += [[a, c2, b], [b, c2, d2]]
    return np.array(Vs), np.array(Ns), np.array(Fs)

# fabric swatch material from a real product photo (mirror-tiled so it repeats seamlessly)
patch_mat = None
if FABRIC_PHOTO:
    from PIL import Image, ImageOps
    crop = Image.open(FABRIC_PHOTO).convert('RGB').crop((480, 200, 980, 500))
    tile = Image.new('RGB', (crop.width * 2, crop.height * 2))
    tile.paste(crop, (0, 0)); tile.paste(ImageOps.mirror(crop), (crop.width, 0))
    tile.paste(ImageOps.flip(crop), (0, crop.height)); tile.paste(ImageOps.flip(ImageOps.mirror(crop)), (crop.width, crop.height))
    patch_mat = trimesh.visual.material.PBRMaterial(name='FabricSwatch', baseColorTexture=tile.resize((1024, 1024)),
                                                     metallicFactor=0.0, roughnessFactor=0.9, doubleSided=True)

# the rear top rail was barely modelled (it sits behind the backrest): the generated middle piece
# is rough and the corners are missing, so the whole rail is replaced by one smooth tube
RAIL_Y, RAIL_R = 0.663, 0.03
_half = [(-0.778, -0.56), (-0.775, -0.70), (-0.70, -0.80), (-0.56, -0.865), (-0.36, -0.905), (-0.18, -0.928)]
RAIL_PATH = [(x, RAIL_Y, z) for x, z in _half] + [(0.0, RAIL_Y, -0.935)] + [(-x, RAIL_Y, z) for x, z in reversed(_half)]
def drop_old_rail(V, F):
    c = V[F].mean(1)
    band = (c[:, 1] > 0.60) & (c[:, 1] < 0.73)
    old = band & (((c[:, 2] < -0.84) & (np.abs(c[:, 0]) < 0.5)) |      # rough middle piece
                  ((c[:, 2] < -0.72) & (np.abs(c[:, 0]) < 0.77)))      # leftover stubs near the arms
    print(f'  removed {int(old.sum())} faces of the rough rail piece')
    return F[~old]

out = trimesh.Scene()
for name in ['ChairBase', 'SeatCushion', 'SeatBack']:
    zone = (lambda c: (c[:, 2] < -0.12) & (c[:, 1] > -0.15)) if name == 'SeatCushion' else None
    V, N, UV, F, lining = build(pieces[name], patch=name != 'ChairBase' and patch_mat is not None, hidden_zone=zone)
    # find openings on the whole surface (lining included) so swatch faces aren't capped twice
    V2 = np.vstack([V, lining.reshape(-1, 3)]) if len(lining) else V
    F2 = np.vstack([F, np.arange(len(lining) * 3).reshape(-1, 3) + len(V)]) if len(lining) else F
    caps, nl, nb = cap_triangles(V2, F2, max_extent=0.08 if name == 'ChairBase' else 2.0)
    if name == 'ChairBase':
        F = drop_old_rail(V, F)
        tv, tn, tfc = tube(RAIL_PATH, RAIL_R, segments=20, samples=160)
        F = np.vstack([F, tfc + len(V)]); V = np.vstack([V, tv]); N = np.vstack([N, tn]); UV = np.vstack([UV, np.tile(MET_UV, (len(tv), 1))])
        if len(caps):
            cv = caps.reshape(-1, 3); F = np.vstack([F, np.arange(len(cv)).reshape(-1, 3) + len(V)])
            cn = np.repeat(np.cross(caps[:, 1] - caps[:, 0], caps[:, 2] - caps[:, 0]), 3, 0); cn /= np.maximum(np.linalg.norm(cn, axis=1, keepdims=True), 1e-9)
            V = np.vstack([V, cv]); N = np.vstack([N, cn]); UV = np.vstack([UV, np.tile(MET_UV, (len(cv), 1))])
        print('  rebuilt rear rail as one smooth tube')
    m = trimesh.Trimesh(V, F, vertex_normals=N, process=False, visual=trimesh.visual.TextureVisuals(uv=UV, material=mat))
    out.add_geometry(m, node_name=name, geom_name=name)
    if name != 'ChairBase' and patch_mat is not None:
        soup = np.vstack([caps, lining]) if len(lining) else caps
        pm, puv = box_uv_mesh(soup)
        pm.visual = trimesh.visual.TextureVisuals(uv=puv, material=patch_mat)
        out.add_geometry(pm, node_name=f'{name}Fabric', geom_name=f'{name}Fabric', parent_node_name=name)
        print(f'  {name}Fabric: {len(soup)} swatch faces')
    print(f'{name}: {len(F)} faces, capped {nl} openings ({nb} open edges)')
out.export(DST)
print('wrote', DST)
