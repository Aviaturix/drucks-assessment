import struct
import math

def parse_stl(filename):
    triangles = []
    with open(filename, 'rb') as f:
        header = f.read(80)
        num_triangles = struct.unpack('<I', f.read(4))[0]
        for _ in range(num_triangles):
            f.read(12)
            v1 = struct.unpack('<3f', f.read(12))
            v2 = struct.unpack('<3f', f.read(12))
            v3 = struct.unpack('<3f', f.read(12))
            f.read(2)
            triangles.append((v1, v2, v3))
    return triangles

def signed_tet_volume(v1, v2, v3):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    x3, y3, z3 = v3
    return (x1 * (y2 * z3 - y3 * z2)
          - y1 * (x2 * z3 - x3 * z2)
          + z1 * (x2 * y3 - x3 * y2)) / 6.0

def compute_volume(triangles):
    total = 0.0
    for v1, v2, v3 in triangles:
        total += signed_tet_volume(v1, v2, v3)
    return abs(total)

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

def get_cross_section_segments(triangles, z):
    segments = []
    for v1, v2, v3 in triangles:
        pts = []
        for a, b in [(v1,v2), (v2,v3), (v3,v1)]:
            if (a[2] <= z <= b[2]) or (b[2] <= z <= a[2]):
                if abs(b[2] - a[2]) < 1e-9:
                    continue
                t = (z - a[2]) / (b[2] - a[2])
                x = a[0] + t * (b[0] - a[0])
                y = a[1] + t * (b[1] - a[1])
                pts.append((x, y))
        if len(pts) == 2:
            segments.append((pts[0], pts[1]))
    return segments

def estimate_print_time(triangles, z_min, z_max, layer_height=0.2, speed=60):
    total_length = 0.0
    z = z_min + layer_height / 2
    while z < z_max:
        segments = get_cross_section_segments(triangles, z)
        for a, b in segments:
            total_length += math.dist(a, b)
        z += layer_height
    return total_length / 60  # seconds to minutes

if __name__ == "__main__":
    filename = "DrucksShoe.stl"

    print("Parsing STL file...")
    triangles = parse_stl(filename)
    print(f"Loaded {len(triangles)} triangles")

    print("\n--- Task 1: Volume ---")
    volume = compute_volume(triangles)
    print(f"Volume: {volume:.2f} mm³")

    print("\n--- Task 2: Bounding Box ---")
    bb = compute_bounding_box(triangles)
    print(f"X: {bb['x'][0]:.2f} to {bb['x'][1]:.2f} mm")
    print(f"Y: {bb['y'][0]:.2f} to {bb['y'][1]:.2f} mm")
    print(f"Z: {bb['z'][0]:.2f} to {bb['z'][1]:.2f} mm")
    z_min, z_max = bb['z']
    height = z_max - z_min
    layers = compute_layer_count(z_min, z_max)
    print(f"Height: {height:.2f} mm")
    print(f"Layer count at 0.2mm: {layers}")

    print("\n--- Task 3: Print Time ---")
    t = estimate_print_time(triangles, z_min, z_max)
    print(f"Estimated print time: {t:.1f} minutes")