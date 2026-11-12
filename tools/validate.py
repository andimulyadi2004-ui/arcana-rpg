#!/usr/bin/env python3
"""Arcana RPG - static validator.

Checks the things that actually break an add-on in game:
  * every JSON parses
  * every item/block identifier is namespaced and unique
  * every icon / terrain texture reference resolves to a real PNG
  * every recipe ingredient exists (our namespace or a known vanilla id)
  * every block loot table path exists
  * every attachable identifier matches an existing armour item
  * every item/block has a name in both .lang files
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BP = os.path.join(ROOT, "src", "ArcanaBP")
RP = os.path.join(ROOT, "src", "ArcanaRP")
NS = "arcana"

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- 1. JSON ----
json_files = glob.glob(os.path.join(ROOT, "src", "**", "*.json"), recursive=True)
for p in json_files:
    try:
        load(p)
    except Exception as e:
        err("invalid JSON %s: %s" % (os.path.relpath(p, ROOT), e))

# ------------------------------------------------------- 2. identifiers ----
items = {}
for p in glob.glob(os.path.join(BP, "items", "*.json")):
    d = load(p)["minecraft:item"]
    ident = d["description"]["identifier"]
    if not ident.startswith(NS + ":"):
        err("item %s not namespaced" % ident)
    if ident in items:
        err("duplicate item identifier %s" % ident)
    items[ident] = (p, d)

blocks = {}
for p in glob.glob(os.path.join(BP, "blocks", "*.json")):
    d = load(p)["minecraft:block"]
    ident = d["description"]["identifier"]
    if not ident.startswith(NS + ":"):
        err("block %s not namespaced" % ident)
    if ident in blocks:
        err("duplicate block identifier %s" % ident)
    blocks[ident] = (p, d)

# ---------------------------------------------------------- 3. textures ----
item_tex = load(os.path.join(RP, "textures", "item_texture.json"))["texture_data"]
terrain_tex = load(os.path.join(RP, "textures", "terrain_texture.json"))["texture_data"]

for key, val in item_tex.items():
    path = os.path.join(RP, val["textures"] + ".png")
    if not os.path.exists(path):
        err("item_texture '%s' -> missing %s" % (key, val["textures"]))
for key, val in terrain_tex.items():
    path = os.path.join(RP, val["textures"] + ".png")
    if not os.path.exists(path):
        err("terrain_texture '%s' -> missing %s" % (key, val["textures"]))

for ident, (p, d) in items.items():
    icon = d["components"].get("minecraft:icon")
    if icon is None:
        err("item %s has no minecraft:icon" % ident)
        continue
    key = icon if isinstance(icon, str) else icon.get("texture")
    if key not in item_tex:
        err("item %s icon '%s' not in item_texture.json" % (ident, key))

for ident, (p, d) in blocks.items():
    mi = d["components"].get("minecraft:material_instances", {})
    for face, cfg in mi.items():
        key = cfg.get("texture")
        if key not in terrain_tex:
            err("block %s face %s texture '%s' not in terrain_texture.json"
                % (ident, face, key))

# ----------------------------------------------------------- 4. recipes ----
VANILLA = {
    "minecraft:stick", "minecraft:glass_bottle", "minecraft:glowstone_dust",
    "minecraft:apple", "minecraft:sweet_berries", "minecraft:stone_bricks",
    "minecraft:obsidian", "minecraft:glowstone", "minecraft:stone",
    "minecraft:vine", "minecraft:paper", "minecraft:book",
}
recipe_count = 0
for p in glob.glob(os.path.join(BP, "recipes", "*.json")):
    d = load(p)
    body = list(d.values())[1]
    recipe_count += 1
    refs = []
    if "key" in body:
        refs += [v["item"] for v in body["key"].values()]
    if "ingredients" in body:
        refs += [i["item"] for i in body["ingredients"]]
    if "input" in body:
        refs.append(body["input"])
    refs.append(body["result"]["item"] if isinstance(body.get("result"), dict)
                else body.get("output"))
    for r in refs:
        if r is None:
            continue
        if r.startswith(NS + ":"):
            if r not in items and r not in blocks:
                err("recipe %s references unknown %s"
                    % (os.path.basename(p), r))
        elif r not in VANILLA:
            warn("recipe %s uses unverified vanilla item %s"
                 % (os.path.basename(p), r))

# ------------------------------------------------------- 5. loot tables ----
for ident, (p, d) in blocks.items():
    loot = d["components"].get("minecraft:loot")
    if not loot:
        err("block %s has no loot table" % ident)
        continue
    lp = os.path.join(BP, loot)
    if not os.path.exists(lp):
        err("block %s loot table missing: %s" % (ident, loot))
        continue
    for pool in load(lp)["pools"]:
        for entry in pool["entries"]:
            name = entry.get("name")
            if name and name.startswith(NS + ":") and name not in items and name not in blocks:
                err("loot %s drops unknown item %s" % (loot, name))

# ------------------------------------------------------ 6. attachables ----
armor_items = {i for i, (p, d) in items.items()
               if "minecraft:wearable" in d["components"]}
attached = set()
for p in glob.glob(os.path.join(RP, "attachables", "*.json")):
    d = load(p)["minecraft:attachable"]["description"]
    ident = d["identifier"]
    attached.add(ident)
    if ident not in armor_items:
        err("attachable %s has no matching wearable item" % ident)
    tex = d["textures"]["default"]
    if not os.path.exists(os.path.join(RP, tex + ".png")):
        err("attachable %s texture missing: %s" % (ident, tex))
    geo = d["geometry"]["default"]
    if not geo.startswith("geometry.humanoid.armor."):
        err("attachable %s uses unexpected geometry %s" % (ident, geo))
for a in armor_items - attached:
    err("armour item %s has no attachable (would render invisible)" % a)

# ------------------------------------------------------------ 7. lang ----
for lang in ("en_US", "id_ID"):
    lp = os.path.join(RP, "texts", lang + ".lang")
    if not os.path.exists(lp):
        err("missing lang file %s" % lang)
        continue
    text = open(lp, encoding="utf-8").read()
    for ident in items:
        if "item.%s=" % ident not in text:
            err("%s missing name for %s" % (lang, ident))
    for ident in blocks:
        if "tile.%s.name=" % ident not in text:
            err("%s missing name for %s" % (lang, ident))

# --------------------------------------------------------- 8. manifest ----
for pack, module_type in ((BP, "data"), (RP, "resources")):
    m = load(os.path.join(pack, "manifest.json"))
    if m["header"]["min_engine_version"] != [1, 26, 40]:
        err("%s min_engine_version is %s" % (pack, m["header"]["min_engine_version"]))
    if m["modules"][0]["type"] != module_type:
        err("%s module type is %s" % (pack, m["modules"][0]["type"]))
    if not os.path.exists(os.path.join(pack, "pack_icon.png")):
        err("%s has no pack_icon.png" % pack)

# ------------------------------------------------------------- report ----
print("items:      %d" % len(items))
print("blocks:     %d" % len(blocks))
print("recipes:    %d" % recipe_count)
print("attachables:%d" % len(attached))
print("json files: %d" % len(json_files))
print()
for w in warnings:
    print("WARN  " + w)
for e in errors:
    print("ERROR " + e)
print()
if errors:
    print("FAILED with %d error(s)" % len(errors))
    sys.exit(1)
print("PASS - no errors (%d warning(s))" % len(warnings))
