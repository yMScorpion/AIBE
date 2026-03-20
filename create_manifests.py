import os
import json

manifests = {
    "TV": {
        "id": "TV",
        "name": "TV",
        "category": "decor",
        "type": "asset",
        "canPlaceOnWalls": False,
        "canPlaceOnSurfaces": True,
        "backgroundTiles": 0,
        "width": 32,
        "height": 32,
        "footprintW": 2,
        "footprintH": 2
    },
    "POOL_TABLE": {
        "id": "POOL_TABLE",
        "name": "Pool Table",
        "category": "misc",
        "type": "asset",
        "canPlaceOnWalls": False,
        "canPlaceOnSurfaces": False,
        "backgroundTiles": 0,
        "width": 32,
        "height": 48,
        "footprintW": 2,
        "footprintH": 3
    },
    "PING_PONG": {
        "id": "PING_PONG",
        "name": "Ping Pong",
        "category": "misc",
        "type": "asset",
        "canPlaceOnWalls": False,
        "canPlaceOnSurfaces": False,
        "backgroundTiles": 0,
        "width": 32,
        "height": 48,
        "footprintW": 2,
        "footprintH": 3
    }
}

base1 = "c:/Users/ADRIANO/AIDA/aibe/ui/frontend/public/pixel-agents/assets/furniture/"
base2 = "c:/Users/ADRIANO/AIDA/pixel-agents/webview-ui/public/assets/furniture/"

for base in [base1, base2]:
    for key, manifest in manifests.items():
        dir_path = os.path.join(base, key)
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)

print("Manifests created.")
