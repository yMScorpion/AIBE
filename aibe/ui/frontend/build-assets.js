const fs = require('fs');
const path = require('path');

const assetsDir = path.join(__dirname, 'public', 'pixel-agents', 'assets');

// 1. Build Asset Index
const characters = fs.readdirSync(path.join(assetsDir, 'characters')).filter(f => f.endsWith('.png'));
const floors = fs.readdirSync(path.join(assetsDir, 'floors')).filter(f => f.endsWith('.png'));
const walls = fs.readdirSync(path.join(assetsDir, 'walls')).filter(f => f.endsWith('.png'));

const assetIndex = {
  characters,
  floors,
  walls,
  defaultLayout: 'default-layout-1.json'
};

fs.writeFileSync(path.join(assetsDir, 'asset-index.json'), JSON.stringify(assetIndex, null, 2));

// 2. Build Furniture Catalog
const furnitureDir = path.join(assetsDir, 'furniture');
const dirs = fs.readdirSync(furnitureDir, { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name).sort();

const catalog = [];
for (const folderName of dirs) {
  const manifestPath = path.join(furnitureDir, folderName, 'manifest.json');
  if (!fs.existsSync(manifestPath)) continue;
  
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  if (manifest.type === 'asset') {
    const file = manifest.file ?? `${manifest.id}.png`;
    catalog.push({
      id: manifest.id,
      name: manifest.name,
      label: manifest.name,
      category: manifest.category,
      file,
      furniturePath: `furniture/${folderName}/${file}`,
      width: manifest.width,
      height: manifest.height,
      footprintW: manifest.footprintW,
      footprintH: manifest.footprintH,
      isDesk: manifest.category === 'desks',
      canPlaceOnWalls: manifest.canPlaceOnWalls,
      canPlaceOnSurfaces: manifest.canPlaceOnSurfaces,
      backgroundTiles: manifest.backgroundTiles,
      orientation: manifest.orientation,
      state: manifest.state,
      groupId: manifest.groupId,
      mirrorSide: manifest.mirrorSide,
      rotationScheme: manifest.rotationScheme,
      animationGroup: manifest.animationGroup,
      frame: manifest.frame,
    });
  }
}

fs.writeFileSync(path.join(assetsDir, 'furniture-catalog.json'), JSON.stringify(catalog, null, 2));

console.log('Done building assets!');
