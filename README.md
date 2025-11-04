# Real-lifemaptogamemap

**Kartkonverteringsverktøy for Pokémon Qbone - Pokéliga Edition**

## Oversikt

Dette repositoriet inneholder verktøy og data for å konvertere virkelige kart (OpenStreetMap) til spillkart for Pokémon ROM-hacks, spesifikt for **Pokémon Qbone - Pokéliga Edition**.

## Formål

Prosjektet gjør det mulig å:
- Hente geodata fra OpenStreetMap for Vennesla-området
- Konvertere bygninger, veier og landemerker til spillressurser
- Generere Porymap-kompatible kartfiler
- Automatisere kartutvikling basert på virkelig geografi

## Hovedprosjekt

Dette er et støtteprosjekt for hovedprosjektet:  
🎮 **[Pokémon Qbone - Pokéliga Edition](https://github.com/prebenR93/pokemon-qbone-pokeligaen)**

## Funksjoner

### Planlagte Features

- **OSM Data Fetcher**: Hent bygnings- og veidata fra OpenStreetMap
- **Tileset Generator**: Generer tilesets basert på bygningstyper
- **Map Converter**: Konverter OSM-data til Porymap JSON-format
- **Location Database**: Strukturert database over Vennesla-lokasjoner
- **Coordinate Mapper**: Konverter GPS-koordinater til spillkoordinater

## Struktur

```
Real-lifemaptogamemap/
├── README.md
├── LICENSE
├── tools/
│   ├── osm_fetcher.py       # Hent OSM-data
│   ├── map_converter.py     # Konverter til Porymap
│   └── tileset_gen.py       # Generer tilesets
├── data/
│   ├── vennesla_osm.json    # Rå OSM-data
│   └── buildings.json       # Bygningsdatabase
└── output/
    └── porymap/             # Genererte kartfiler
```

## Installasjon

```bash
# Klon repositoriet
git clone https://github.com/prebenR93/Real-lifemaptogamemap.git
cd Real-lifemaptogamemap

# Installer avhengigheter
pip install -r requirements.txt
```

## Bruk

```bash
# Hent OSM-data for Vennesla
python tools/osm_fetcher.py --area vennesla --output data/vennesla_osm.json

# Konverter til Porymap-format
python tools/map_converter.py --input data/vennesla_osm.json --output output/porymap/

# Generer tilesets
python tools/tileset_gen.py --input data/buildings.json --output output/tilesets/
```

## Status

🚧 **Under utvikling** - Verktøyene er i tidlig planleggingsfase.

## Bidra

Bidrag er velkomne! Se [CONTRIBUTING.md](../pokemon-qbone-pokeligaen/CONTRIBUTING.md) i hovedprosjektet.

## Lisens

MIT License - Se [LICENSE](LICENSE)

## Relaterte Prosjekter

- [Pokémon Qbone - Pokéliga Edition](https://github.com/prebenR93/pokemon-qbone-pokeligaen) - Hovedprosjekt
- [mGBA](https://github.com/prebenR93/mgba) - Emulator for testing

---

*Del av Robstad Interactive Solutions (R-I&S)*
