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