import struct

def parse_stl(filename):
    triangles = []
    with open(filename, 'rb') as f:
        header = f.read(80)
        num_triangles = struct.unpack('<I', f.read(4))[0]
        print(f"File says there are {num_triangles} triangles")
        
        for _ in range(num_triangles):
            f.read(12)  # skip normal
            v1 = struct.unpack('<3f', f.read(12))
            v2 = struct.unpack('<3f', f.read(12))
            v3 = struct.unpack('<3f', f.read(12))
            f.read(2)
            triangles.append((v1, v2, v3))
    
    return triangles

# Run it
triangles = parse_stl("DrucksShoe.stl")
print(f"Actually loaded: {len(triangles)} triangles")
print(f"First triangle looks like: {triangles[0]}")

def signed_tet_volume(v1, v2, v3):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    x3, y3, z3 = v3
    return (x1 * (y2 * z3 - y3 * z2)
          - y1 * (x2 * z3 - x3 * z2)
          + z1 * (x2 * y3 - x3 * y2)) / 6.0

# Test on first triangle
v1, v2, v3 = triangles[0]
vol = signed_tet_volume(v1, v2, v3)
print(f"Volume of one tetrahedron: {vol}")

def compute_volume(triangles):
    total = 0.0
    for v1, v2, v3 in triangles:
        total += signed_tet_volume(v1, v2, v3)
    return abs(total)

volume = compute_volume(triangles)
print(f"Total volume: {volume:.2f} mm³")

def compute_bounding_box(triangles):
    all_verts = [v for tri in triangles for v in tri]
    xs = [v[0] for v in all_verts]
    ys = [v[1] for v in all_verts]
    zs = [v[2] for v in all_verts]
    return {
        'x': (min(xs), max(xs)),
        'y': (min(ys), max(ys)),
        'z': (min(zs), max(zs))
        
    }


def compute_layer_count(z_min, z_max, layer_height=0.2):
    height = z_max - z_min
    return int(height / layer_height)

bb = compute_bounding_box(triangles)
z_min, z_max = bb['z']
layers = compute_layer_count(z_min, z_max)
print(f"Height: {z_max - z_min:.2f} mm")
print(f"Layers: {layers}")

z_test = (z_min + z_max) / 2  # middle of the shoe
print(f"Testing at z = {z_test:.2f}")

segments = []
for v1, v2, v3 in triangles:
    pts = []
    for a, b in [(v1,v2), (v2,v3), (v3,v1)]:
        if (a[2] <= z_test <= b[2]) or (b[2] <= z_test <= a[2]):
            if abs(b[2] - a[2]) < 1e-9:
                continue
            t = (z_test - a[2]) / (b[2] - a[2])
            x = a[0] + t * (b[0] - a[0])
            y = a[1] + t * (b[1] - a[1])
            pts.append((x, y))
    if len(pts) == 2:
        segments.append((pts[0], pts[1]))

print(f"Found {len(segments)} segments at z={z_test:.2f}")

import math
total = sum(math.dist(a, b) for a, b in segments)
print(f"Total perimeter at this layer: {total:.2f} mm")