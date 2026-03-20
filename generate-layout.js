const fs = require('fs');

const cols = 100;
const rows = 80;
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

// Outline wall
fillRect(2, 2, 96, 76, 1); // Fill whole floor with FLOOR_1
// Outer walls
fillRect(2, 2, 96, 1, 0); // Top wall
fillRect(2, 77, 96, 1, 0); // Bottom wall
fillRect(2, 2, 1, 76, 0); // Left wall
fillRect(97, 2, 1, 76, 0); // Right wall

const furniture = [];
let uidCounter = 0;
function addFurn(type, c, r, uid = null) {
  furniture.push({ uid: uid || `f-gen-${uidCounter++}`, type, col: c, row: r });
}

// Function to populate a standard department room
function populateDeptRoom(c, r, w, h, deptName) {
  // Add desks and chairs
  // Put them in 2 rows
  let seatIdx = 0;
  for(let i=0; i<2; i++) {
    for(let j=0; j<2; j++) {
      let dx = c + 4 + i * 6;
      let dy = r + 4 + j * 6;
      addFurn("DESK_FRONT", dx, dy);
      addFurn("PC_FRONT_OFF", dx, dy);
      addFurn("CUSHIONED_CHAIR_SIDE", dx + 1, dy, `seat-${deptName}-${seatIdx++}`);
    }
  }
  addFurn("DOUBLE_BOOKSHELF", c + 2, r + 2);
  addFurn("PLANT", c + w - 3, r + 2);
  addFurn("BIN", c + w - 3, r + h - 3);
  addFurn("WHITEBOARD", c + w - 2, r + Math.floor(h/2));
}

// Top row rooms (y=2 to 22) -> w=16, h=20
// Rooms: Exec, Research, Evo, Product, Marketing
let xOffsets = [2, 22, 42, 62, 82];
let floors = [5, 2, 3, 6, 7];
let deptsTop = ["executive", "research", "evolution", "product", "marketing"];

for (let i = 0; i < 5; i++) {
  let x = xOffsets[i];
  drawRoom(x, 2, 16, 20, floors[i], x + 7, 21); // door at bottom
  populateDeptRoom(x, 2, 16, 20, deptsTop[i]);
}

// Bottom row rooms (y=58 to 78) -> w=16, h=20
// Rooms: Social, Security, Sales, ML, Finance
let floorsBottom = [8, 9, 2, 3, 4];
let deptsBottom = ["social", "security", "sales", "ml", "finance"];
for (let i = 0; i < 5; i++) {
  let x = xOffsets[i];
  drawRoom(x, 58, 16, 20, floorsBottom[i], x + 7, 58); // door at top
  populateDeptRoom(x, 58, 16, 20, deptsBottom[i]);
}

// Meeting Room: x=4 to 48, y=28 to 52 (w=44, h=24)
drawRoom(4, 28, 44, 24, 2, 24, 28); // Door at top
// Huge meeting table
for(let i=0; i<10; i++) {
  addFurn("TABLE_FRONT", 12 + i*2, 38);
  addFurn("WOODEN_CHAIR_BACK", 12 + i*2, 39, `seat-meeting-top-${i}`);
  addFurn("WOODEN_CHAIR_FRONT", 12 + i*2, 37, `seat-meeting-bottom-${i}`);
}
addFurn("WOODEN_CHAIR_SIDE", 11, 38);
addFurn("WOODEN_CHAIR_SIDE:left", 32, 38);
addFurn("WHITEBOARD", 24, 29);
addFurn("WHITEBOARD", 26, 29);
addFurn("PLANT_2", 6, 30);
addFurn("PLANT_2", 44, 30);

// Break Room: x=52 to 96, y=28 to 52 (w=44, h=24)
drawRoom(52, 28, 44, 24, 4, 72, 28); // Door at top
// Break room furniture
addFurn("COFFEE_TABLE", 60, 36);
addFurn("SOFA_FRONT", 60, 35);
addFurn("SOFA_BACK", 60, 38);
addFurn("COFFEE", 60, 36);

addFurn("TABLE_FRONT", 75, 36);
addFurn("WOODEN_BENCH", 75, 37);
addFurn("WOODEN_BENCH", 75, 35);

addFurn("TABLE_FRONT", 85, 36);
addFurn("WOODEN_BENCH", 85, 37);
addFurn("WOODEN_BENCH", 85, 35);

addFurn("POOL_TABLE", 65, 45); // 2x3 footprint
addFurn("PING_PONG", 75, 45);  // 2x3 footprint
addFurn("TV", 85, 45);         // 2x2 footprint

addFurn("PLANT", 55, 30);
addFurn("PLANT", 90, 30);
addFurn("BIN", 90, 50);

const layout = {
  version: 1,
  cols,
  rows,
  layoutRevision: 5,
  tiles,
  furniture
};

fs.writeFileSync('c:/Users/ADRIANO/AIDA/aibe/ui/frontend/public/pixel-agents/assets/default-layout-1.json', JSON.stringify(layout));
console.log('Layout generated with 10 rooms, meeting room, and break room.');
