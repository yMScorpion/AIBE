const fs = require('fs');

const cols = 50;
const rows = 40;
const tiles = new Array(cols * rows).fill(255); // VOID

// Helper to fill a rect with a tile
function fillRect(c, r, w, h, tile) {
  for (let y = r; y < r + h; y++) {
    for (let x = c; x < c + w; x++) {
      if (x >= 0 && x < cols && y >= 0 && y < rows) {
        tiles[y * cols + x] = tile;
      }
    }
  }
}

function drawRoom(c, r, w, h, floorTile, doorC, doorR) {
  // Floor
  fillRect(c, r, w, h, floorTile);
  // Walls
  fillRect(c, r, w, 1, 0); // Top
  fillRect(c, r + h - 1, w, 1, 0); // Bottom
  fillRect(c, r, 1, h, 0); // Left
  fillRect(c + w - 1, r, 1, h, 0); // Right
  
  // Door
  if (doorC !== undefined && doorR !== undefined) {
    fillRect(doorC, doorR, 2, 1, floorTile);
  }
}

// 0: WALL, 1: FLOOR_1, 2: FLOOR_2, etc
// Outline wall
fillRect(2, 2, 46, 36, 1); // Fill whole floor with FLOOR_1
// Outer walls
fillRect(2, 2, 46, 1, 0); // Top wall
fillRect(2, 37, 46, 1, 0); // Bottom wall
fillRect(2, 2, 1, 36, 0); // Left wall
fillRect(47, 2, 1, 36, 0); // Right wall

// Corridors
// The main corridor is the space that is left after drawing rooms.
// We will draw the rooms.

// Executive Room (Top Left)
drawRoom(2, 2, 14, 12, 5, 10, 13); // Door at bottom

// Meeting Room (Top Right)
drawRoom(30, 2, 18, 14, 2, 30, 10); // Door at left

// Break Room / Cafe (Middle)
drawRoom(16, 14, 14, 12, 4, 21, 25); // Door at bottom

// Engineering / Dev Room (Bottom Left)
drawRoom(2, 20, 18, 18, 3, 19, 24); // Door at right

// Marketing / Sales (Bottom Right)
drawRoom(28, 24, 20, 14, 6, 28, 28); // Door at left

// Furniture
const furniture = [];
let uidCounter = 0;
function addFurn(type, c, r) {
  furniture.push({ uid: `f-gen-${uidCounter++}`, type, col: c, row: r });
}

// Exec Room Furniture
addFurn("DESK_FRONT", 6, 6);
addFurn("PC_FRONT_OFF", 6, 6);
addFurn("CUSHIONED_CHAIR_SIDE:left", 8, 6);
addFurn("PLANT", 3, 3);
addFurn("LARGE_PAINTING", 6, 2);
addFurn("COFFEE_TABLE", 10, 5);
addFurn("SOFA_FRONT", 10, 4);
addFurn("DOUBLE_BOOKSHELF", 12, 2);

// Meeting Room
addFurn("TABLE_FRONT", 34, 6);
addFurn("TABLE_FRONT", 36, 6);
addFurn("TABLE_FRONT", 38, 6);
addFurn("TABLE_FRONT", 40, 6);
addFurn("WOODEN_CHAIR_BACK", 34, 7);
addFurn("WOODEN_CHAIR_BACK", 36, 7);
addFurn("WOODEN_CHAIR_BACK", 38, 7);
addFurn("WOODEN_CHAIR_BACK", 40, 7);
addFurn("WOODEN_CHAIR_FRONT", 34, 5);
addFurn("WOODEN_CHAIR_FRONT", 36, 5);
addFurn("WOODEN_CHAIR_FRONT", 38, 5);
addFurn("WOODEN_CHAIR_FRONT", 40, 5);
addFurn("WOODEN_CHAIR_SIDE", 33, 6);
addFurn("WOODEN_CHAIR_SIDE:left", 42, 6);
addFurn("PLANT_2", 45, 3);
addFurn("WHITEBOARD", 36, 2);
addFurn("WHITEBOARD", 38, 2);

// Engineering
for(let i=0; i<3; i++) {
  addFurn("DESK_FRONT", 5, 23 + i*4);
  addFurn("PC_FRONT_OFF", 5, 23 + i*4);
  addFurn("CUSHIONED_CHAIR_SIDE", 6, 23 + i*4);

  addFurn("DESK_FRONT", 11, 23 + i*4);
  addFurn("PC_FRONT_OFF", 11, 23 + i*4);
  addFurn("CUSHIONED_CHAIR_SIDE:left", 10, 23 + i*4);
}
addFurn("DOUBLE_BOOKSHELF", 5, 20);
addFurn("PLANT", 3, 21);
addFurn("BIN", 15, 21);

// Marketing
for(let i=0; i<2; i++) {
  addFurn("DESK_FRONT", 31, 26 + i*4);
  addFurn("PC_FRONT_OFF", 31, 26 + i*4);
  addFurn("WOODEN_CHAIR_SIDE", 32, 26 + i*4);

  addFurn("DESK_FRONT", 37, 26 + i*4);
  addFurn("PC_FRONT_OFF", 37, 26 + i*4);
  addFurn("WOODEN_CHAIR_SIDE:left", 36, 26 + i*4);
}
addFurn("PLANT", 45, 25);
addFurn("BIN", 45, 35);
addFurn("WHITEBOARD", 35, 24);

// Cafe
addFurn("COFFEE_TABLE", 18, 18);
addFurn("SOFA_FRONT", 18, 17);
addFurn("SOFA_BACK", 18, 20);
addFurn("COFFEE", 18, 18);
addFurn("BIN", 27, 15);
addFurn("PLANT", 17, 15);
addFurn("TABLE_FRONT", 24, 18);
addFurn("WOODEN_BENCH", 24, 19);
addFurn("WOODEN_BENCH", 24, 17);

// New recreational items
addFurn("POOL_TABLE", 18, 22); // 2x3 footprint
addFurn("PING_PONG", 25, 20);  // 2x3 footprint
addFurn("TV", 26, 15);         // 2x2 footprint

// Hallways / Corridors Plants
addFurn("PLANT_2", 20, 3);
addFurn("PLANT", 20, 35);
addFurn("PLANT", 25, 35);
addFurn("BIN", 25, 23);

const layout = {
  version: 1,
  cols,
  rows,
  layoutRevision: 4,
  tiles,
  furniture
};

fs.writeFileSync('c:/Users/ADRIANO/AIDA/aibe/ui/frontend/public/pixel-agents/assets/default-layout-1.json', JSON.stringify(layout));
console.log('Layout generated');
