def build_null_mirror(source_lake):
    import json
    import random
    
    null_name = source_lake.replace("Lake_", "Null_")
    
    with open(source_lake, 'r') as src, open(null_name, 'w') as dst:
        for line in src:
            data = json.loads(line)
            # SCRAMBLE PHYSICS: Keep the ID and Address, randomize the signal
            data['Vdisp'] = random.uniform(70, 400)
            data['zsp'] = random.uniform(0.01, 0.70)
            dst.write(json.dumps(data) + '\n')
    
    print(f"💀 NULL MIRROR GENERATED: {null_name}")