import json
from pathlib import Path

materials = json.loads(Path("examples/materials/material_master.json").read_text(encoding="utf-8"))
assert isinstance(materials, list)
assert "material_id" in materials[0]
print("Material example basic validation passed.")
