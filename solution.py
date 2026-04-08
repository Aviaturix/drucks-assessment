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