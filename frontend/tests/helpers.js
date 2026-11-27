// Utilità condivise dai test: caricano catalogo e fixture dal repository.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const radice = join(dirname(fileURLToPath(import.meta.url)), "..", "..");

export function caricaJson(...percorso) {
  return JSON.parse(readFileSync(join(radice, ...percorso), "utf-8"));
}

export const catalogo = caricaJson("frontend", "static", "data", "kpi-catalog.json");
