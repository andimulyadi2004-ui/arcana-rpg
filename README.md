# Arcana RPG — Minecraft Bedrock Add-on

Add-on RPG untuk **Minecraft Bedrock / MCPE 1.26.40** (manifest `min_engine_version` = `[1, 26, 40]`).

**30 item · 18 blok · 2 set armor lengkap · 35 resep crafting · 52 tekstur**

Semua tekstur dibuat sebagai **SVG** dulu (pixel-art, satu `<rect>` per piksel) lalu di-*rasterise* ke **PNG** — karena Minecraft hanya menerima PNG.

---

## Isi add-on

### Material (9)
| Item | ID | Kegunaan |
|---|---|---|
| Arcanite Ingot | `arcana:arcanite_ingot` | bahan utama semua gear |
| Arcanite Nugget | `arcana:arcanite_nugget` | hasil tambang, 9 → 1 ingot |
| Void Shard | `arcana:void_shard` | bahan set armor Void |
| Ember Core | `arcana:ember_core` | bahan tongkat & apel bara |
| Frost Essence | `arcana:frost_essence` | bahan tombak es |
| Storm Feather | `arcana:storm_feather` | bahan palu badai |
| Rune Stone | `arcana:rune_stone` | bahan blok dekoratif |
| Soul Dust | `arcana:soul_dust` | drop kristal jiwa |
| Gilded Rune | `arcana:gilded_rune` | bahan portal frame |

### Senjata & alat (7)
| Item | Damage | Durability | Catatan |
|---|---|---|---|
| Arcanite Sword | 9 | 1200 | bisa dienchant `sword` |
| Arcanite Pickaxe | 5 | 1200 | `digger` + efficiency, speed 9 di stone/metal |
| Arcanite Axe | 8 | 1200 | enchant `axe` |
| Void Dagger | 7 | 900 | cepat, ringan |
| Ember Staff | 8 | 1000 | tema api |
| Frost Spear | 8 | 1000 | tema es |
| Storm Hammer | 11 | 1500 | damage tertinggi |

### Consumable (4)
- **Mana Potion** — Regeneration II, 8 detik, jadi `glass_bottle` setelah diminum
- **Health Elixir** — Instant Health III
- **Ember Apple** — 6 hunger + Fire Resistance 20 detik
- **Void Berry** — 2 hunger + Night Vision 15 detik

### Armor (2 set, 8 item)
| Set | Protection (H/C/L/B) | Durability |
|---|---|---|
| **Arcanite** | 3 / 8 / 6 / 3 | 480 |
| **Void** | 4 / 9 / 7 / 4 | 620 |

Keduanya punya **attachable** sendiri (`textures/models/armor/{arcanite,void}_layer_{1,2}.png`) sehingga tampil di badan pemain, bukan cuma ikon di inventory.

### Blok (18)
`arcanite_block`, `arcanite_ore`, `deepslate_arcanite_ore`, `void_stone`, `void_brick`, `ember_block`, `frost_block`, `rune_brick`, `arcane_lamp` (light 15), `soul_crystal` (light 10), `mana_crystal_block` (light 12), `obsidian_brick`, `gilded_rune_block`, `mossy_rune_brick`, `cracked_rune_brick`, `storm_block`, `arcane_pillar`, `void_portal_frame`.

Bijih & kristal punya **loot table** sendiri (mis. Arcanite Ore drop 2–5 nugget, bukan bloknya).

---

## Struktur repo

```
arcana-rpg/
├── art/svg/                  # sumber tekstur (SVG, satu rect per piksel)
│   ├── items/  blocks/  armor/
├── src/
│   ├── ArcanaBP/             # behaviour pack
│   │   ├── manifest.json
│   │   ├── pack_icon.png
│   │   ├── items/            # 30 file
│   │   ├── blocks/           # 18 file
│   │   ├── loot_tables/blocks/
│   │   └── recipes/          # 35 file
│   └── ArcanaRP/             # resource pack
│       ├── manifest.json
│       ├── pack_icon.png
│       ├── attachables/      # 8 file (armor)
│       ├── textures/
│       │   ├── items/  blocks/
│       │   ├── models/armor/
│       │   ├── item_texture.json
│       │   └── terrain_texture.json
│       └── texts/            # en_US.lang, id_ID.lang
├── tools/
│   ├── gen_textures.py       # SVG → PNG
│   ├── gen_pack.py           # generator semua JSON
│   └── validate.py           # validator statis
├── build.sh                  # build .mcpack / .mcaddon
└── dist/
```

## Build dari source

Butuh `python3`, `rsvg-convert` (paket `librsvg2-bin`), dan `zip`.

```bash
sudo apt install -y librsvg2-bin zip
./build.sh
```

Hasil di `dist/`:
- `ArcanaRPG.mcaddon` — **pakai ini** (BP + RP sekaligus)
- `ArcanaRPG_BP.mcpack` — behaviour pack saja
- `ArcanaRPG_RP.mcpack` — resource pack saja

## Validasi

```bash
python3 tools/validate.py
```

Yang dicek: semua JSON parse, identifier unik & ber-namespace, setiap ikon/tekstur menunjuk PNG yang benar-benar ada, setiap bahan resep ada, loot table ada, setiap armor punya attachable, dan setiap item/blok punya nama di `en_US` + `id_ID`.

---

## Ambil add-on di Termux lewat GitHub (`gh`)

### 1. Install `gh` di Termux

```bash
pkg update && pkg install -y gh unzip
gh auth login          # pilih GitHub.com → HTTPS → login via browser/token
```

### 2. Download rilis terbaru

```bash
REPO="andimulyadi2004-ui/arcana-rpg"
mkdir -p ~/storage/downloads/ArcanaRPG
gh release download v1.0.0 --repo "$REPO" --pattern "*.mcaddon" --dir ~/storage/downloads/ArcanaRPG --clobber
ls -lh ~/storage/downloads/ArcanaRPG
```

Kalau `~/storage` belum ada, jalankan `termux-setup-storage` dulu.

### 3. Import ke Minecraft

Buka file `.mcaddon` dari aplikasi Files/Downloads → **Open with Minecraft**. Minecraft akan memasang behaviour pack + resource pack sekaligus.

Atau lewat command line, salin manual ke folder Minecraft:

```bash
# Android 11+ (akses /Android/data dibatasi; pakai ini kalau berhasil)
DEST=/sdcard/Android/data/com.mojang.minecraftpe/files/games/com.mojang
mkdir -p "$DEST/behavior_packs" "$DEST/resource_packs"
unzip -o ~/storage/downloads/ArcanaRPG/ArcanaRPG.mcaddon -d /tmp/arcana
cp -r /tmp/arcana/ArcanaRPG_BP "$DEST/behavior_packs/"
cp -r /tmp/arcana/ArcanaRPG_RP "$DEST/resource_packs/"
```

> Di Android 11+ folder `Android/data` sering tidak bisa diakses tanpa root/SAF. Cara paling aman tetap: buka `.mcaddon` lewat **Open with Minecraft**.

### 4. Aktifkan di world

1. Buat/edit world → **Behavior Packs** → aktifkan **Arcana RPG**
2. **Resource Packs** → aktifkan **Arcana RPG** (biasanya otomatis ikut)
3. Pastikan **"Holiday Creator Features"** / experimental toggle **tidak perlu** — add-on ini pakai format stabil 1.26.40

### 5. Ambil item di creative

```
/give @s arcana:arcanite_sword
/give @s arcana:arcanite_chestplate
/give @s arcana:arcane_lamp 16
```

Atau cari di inventory creative tab **Items** / **Construction** / **Equipment**.

### 6. Update ke versi baru

```bash
gh release download --repo "$REPO" --pattern "*.mcaddon" --dir ~/storage/downloads/ArcanaRPG --clobber
```

Versi lebih tinggi otomatis menimpa yang lama saat diimpor.

---

## Catatan teknis

- **Manifest** `format_version: 2`, `min_engine_version: [1, 26, 40]`, `product_type: "addon"`. RP punya `dependencies` ke UUID BP supaya keduanya selalu aktif bersama.
- **Item** pakai `format_version: "1.26.40"` dan `minecraft:icon` berupa string (format baru), bukan objek `{texture: ...}`.
- **Block** pakai `minecraft:geometry: "minecraft:geometry.full_block"` + `material_instances` (bukan `minecraft:block_light_emission` lama).
- **Armor** memakai `minecraft:wearable` + attachable dengan `parent_setup` yang menyembunyikan layer vanilla (`variable.chest_layer_visible = 0.0;` dst) supaya tidak tumpang tindih.
- **Tekstur** 16×16 untuk item/blok, 64×32 untuk armor UV sheet, 128×128 untuk pack icon.

## Lisensi

MIT — bebas dipakai, dimodifikasi, dan dibagikan ulang.
