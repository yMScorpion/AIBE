import { setCharacterTemplates } from './office/sprites/spriteData';
import { setFloorSprites } from './office/floorTiles';
import { setWallSprites } from './office/wallTiles';
import { buildDynamicCatalog } from './office/layout/furnitureCatalog';

export const PNG_ALPHA_THRESHOLD = 2;
export const WALL_PIECE_WIDTH = 16;
export const WALL_PIECE_HEIGHT = 32;
export const WALL_GRID_COLS = 4;
export const WALL_BITMASK_COUNT = 16;
export const FLOOR_TILE_SIZE = 16;
export const CHARACTER_DIRECTIONS = ['down', 'up', 'right'] as const;
export const CHAR_FRAME_W = 16;
export const CHAR_FRAME_H = 32;
export const CHAR_FRAMES_PER_ROW = 7;
export const CHAR_COUNT = 6;

export interface CharacterDirectionSprites {
  down: string[][][];
  up: string[][][];
  right: string[][][];
}

interface DecodedPng {
  width: number;
  height: number;
  data: Uint8ClampedArray;
}

function rgbaToHex(r: number, g: number, b: number, a: number): string {
  if (a < PNG_ALPHA_THRESHOLD) return '';
  const rgb =
    `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
  if (a >= 255) return rgb;
  return `${rgb}${a.toString(16).padStart(2, '0').toUpperCase()}`;
}

function getPixel(
  data: Uint8ClampedArray,
  width: number,
  x: number,
  y: number,
): [number, number, number, number] {
  const idx = (y * width + x) * 4;
  return [data[idx], data[idx + 1], data[idx + 2], data[idx + 3]];
}

function readSprite(
  png: DecodedPng,
  width: number,
  height: number,
  offsetX = 0,
  offsetY = 0,
): string[][] {
  const sprite: string[][] = [];
  for (let y = 0; y < height; y++) {
    const row: string[] = [];
    for (let x = 0; x < width; x++) {
      const [r, g, b, a] = getPixel(png.data, png.width, offsetX + x, offsetY + y);
      row.push(rgbaToHex(r, g, b, a));
    }
    sprite.push(row);
  }
  return sprite;
}

async function decodePng(url: string): Promise<DecodedPng> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch PNG: ${url} (${res.status})`);
  }
  const blob = await res.blob();
  const bitmap = await createImageBitmap(blob);
  const canvas = document.createElement('canvas');
  canvas.width = bitmap.width;
  canvas.height = bitmap.height;
  const ctx = canvas.getContext('2d');
  if (!ctx) {
    bitmap.close();
    throw new Error('Failed to create 2d canvas context for PNG decode');
  }
  ctx.drawImage(bitmap, 0, 0);
  bitmap.close();
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  return { width: canvas.width, height: canvas.height, data: imageData.data };
}

export async function loadPixelAgentsAssets(basePath = '/pixel-agents/') {
  try {
    // 1. Load Asset Index and Catalog
    const indexRes = await fetch(`${basePath}assets/asset-index.json`);
    const assetIndex = await indexRes.json();
    
    const catalogRes = await fetch(`${basePath}assets/furniture-catalog.json`);
    const catalog = await catalogRes.json();

    // 2. Decode Characters
    const characters: CharacterDirectionSprites[] = [];
    for (const relPath of assetIndex.characters) {
      const pathStr = relPath.startsWith('characters/') ? relPath : `characters/${relPath}`;
      const png = await decodePng(`${basePath}assets/${pathStr}`);
      const byDir: CharacterDirectionSprites = { down: [], up: [], right: [] };

      for (let dirIdx = 0; dirIdx < CHARACTER_DIRECTIONS.length; dirIdx++) {
        const dir = CHARACTER_DIRECTIONS[dirIdx];
        const rowOffsetY = dirIdx * CHAR_FRAME_H;
        const frames: string[][][] = [];
        for (let frame = 0; frame < CHAR_FRAMES_PER_ROW; frame++) {
          frames.push(readSprite(png, CHAR_FRAME_W, CHAR_FRAME_H, frame * CHAR_FRAME_W, rowOffsetY));
        }
        byDir[dir] = frames;
      }
      characters.push(byDir);
    }
    setCharacterTemplates(characters);

    // 3. Decode Floors
    const floors: string[][][] = [];
    for (const relPath of assetIndex.floors) {
      const pathStr = relPath.startsWith('floors/') ? relPath : `floors/${relPath}`;
      const png = await decodePng(`${basePath}assets/${pathStr}`);
      floors.push(readSprite(png, FLOOR_TILE_SIZE, FLOOR_TILE_SIZE));
    }
    setFloorSprites(floors);

    // 4. Decode Walls
    const wallSets: string[][][][] = [];
    for (const relPath of assetIndex.walls) {
      const pathStr = relPath.startsWith('walls/') ? relPath : `walls/${relPath}`;
      const png = await decodePng(`${basePath}assets/${pathStr}`);
      const set: string[][][] = [];
      for (let mask = 0; mask < WALL_BITMASK_COUNT; mask++) {
        const ox = (mask % WALL_GRID_COLS) * WALL_PIECE_WIDTH;
        const oy = Math.floor(mask / WALL_GRID_COLS) * WALL_PIECE_HEIGHT;
        set.push(readSprite(png, WALL_PIECE_WIDTH, WALL_PIECE_HEIGHT, ox, oy));
      }
      wallSets.push(set);
    }
    setWallSprites(wallSets);

    // 5. Decode Furniture
    const furnitureSprites: Record<string, string[][]> = {};
    for (const entry of catalog) {
      const png = await decodePng(`${basePath}assets/${entry.furniturePath}`);
      furnitureSprites[entry.id] = readSprite(png, entry.width, entry.height);
    }
    buildDynamicCatalog({ catalog, sprites: furnitureSprites });

    // 6. Fetch Layout
    let layout = null;
    if (assetIndex.defaultLayout) {
      const layoutRes = await fetch(`${basePath}assets/${assetIndex.defaultLayout}`);
      layout = await layoutRes.json();
    }

    return { layout, loadedAssets: { catalog, sprites: furnitureSprites } };
  } catch (err) {
    console.error('Failed to load PixelAgents assets:', err);
    return null;
  }
}
