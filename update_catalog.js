const fs = require('fs');

const file = 'c:/Users/ADRIANO/AIDA/aibe/ui/frontend/public/pixel-agents/assets/furniture-catalog.json';
const catalog = JSON.parse(fs.readFileSync(file, 'utf8'));

const newItems = [
  {
    "id": "TV",
    "name": "TV",
    "label": "TV",
    "category": "decor",
    "file": "TV.png",
    "furniturePath": "furniture/TV/TV.png",
    "width": 32,
    "height": 32,
    "footprintW": 2,
    "footprintH": 2,
    "isDesk": false,
    "canPlaceOnWalls": false,
    "canPlaceOnSurfaces": true,
    "backgroundTiles": 0
  },
  {
    "id": "POOL_TABLE",
    "name": "Pool Table",
    "label": "Pool Table",
    "category": "misc",
    "file": "POOL_TABLE.png",
    "furniturePath": "furniture/POOL_TABLE/POOL_TABLE.png",
    "width": 32,
    "height": 48,
    "footprintW": 2,
    "footprintH": 3,
    "isDesk": false,
    "canPlaceOnWalls": false,
    "canPlaceOnSurfaces": false,
    "backgroundTiles": 0
  },
  {
    "id": "PING_PONG",
    "name": "Ping Pong",
    "label": "Ping Pong",
    "category": "misc",
    "file": "PING_PONG.png",
    "furniturePath": "furniture/PING_PONG/PING_PONG.png",
    "width": 32,
    "height": 48,
    "footprintW": 2,
    "footprintH": 3,
    "isDesk": false,
    "canPlaceOnWalls": false,
    "canPlaceOnSurfaces": false,
    "backgroundTiles": 0
  }
];

// Avoid duplicates
for (const item of newItems) {
  if (!catalog.find(c => c.id === item.id)) {
    catalog.push(item);
  }
}

fs.writeFileSync(file, JSON.stringify(catalog, null, 2));
console.log('Catalog updated.');
