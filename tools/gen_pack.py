#!/usr/bin/env python3
"""Arcana RPG - generates every JSON file for the behaviour + resource pack.

Target: Minecraft Bedrock / MCPE 1.26.40
  * manifest format_version 2, min_engine_version [1, 26, 40]
  * item / block format_version "1.26.40"
  * recipe format_version "1.20.10" (still the current stable recipe schema)
"""
import json
import os
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BP = os.path.join(ROOT, "src", "ArcanaBP")
RP = os.path.join(ROOT, "src", "ArcanaRP")
NS = "arcana"
VERSION = [1, 0, 0]
ENGINE = [1, 26, 40]
ITEM_FV = "1.26.40"
BLOCK_FV = "1.26.40"
RECIPE_FV = "1.20.10"

# Fixed UUIDs so re-running the generator never breaks an installed world.
UUID_BP_HEADER = "8f2c1a44-6b7e-4d31-9a05-1c7d3e5b9a10"
UUID_BP_MODULE = "8f2c1a44-6b7e-4d31-9a05-1c7d3e5b9a11"
UUID_RP_HEADER = "8f2c1a44-6b7e-4d31-9a05-1c7d3e5b9a12"
UUID_RP_MODULE = "8f2c1a44-6b7e-4d31-9a05-1c7d3e5b9a13"


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ------------------------------------------------------------------ items ----
# name: (kind, display, extra)
ITEMS = {
    # ---- materials -------------------------------------------------------
    "arcanite_ingot": ("material", "Arcanite Ingot", "Batang Arcanite", {}),
    "arcanite_nugget": ("material", "Arcanite Nugget", "Bongkahan Arcanite", {}),
    "void_shard": ("material", "Void Shard", "Pecahan Void", {}),
    "ember_core": ("material", "Ember Core", "Inti Bara", {}),
    "frost_essence": ("material", "Frost Essence", "Sari Embun Beku", {}),
    "storm_feather": ("material", "Storm Feather", "Bulu Badai", {}),
    "rune_stone": ("material", "Rune Stone", "Batu Rune", {}),
    "soul_dust": ("material", "Soul Dust", "Debu Jiwa", {}),
    "gilded_rune": ("material", "Gilded Rune", "Rune Berlapis Emas", {}),
    # ---- weapons & tools -------------------------------------------------
    "arcanite_sword": ("sword", "Arcanite Sword", "Pedang Arcanite",
                       {"damage": 9, "durability": 1200}),
    "arcanite_pickaxe": ("pickaxe", "Arcanite Pickaxe", "Beliung Arcanite",
                         {"damage": 5, "durability": 1200}),
    "arcanite_axe": ("axe", "Arcanite Axe", "Kapak Arcanite",
                     {"damage": 8, "durability": 1200}),
    "void_dagger": ("sword", "Void Dagger", "Belati Void",
                    {"damage": 7, "durability": 900}),
    "ember_staff": ("sword", "Ember Staff", "Tongkat Bara",
                    {"damage": 8, "durability": 1000}),
    "frost_spear": ("sword", "Frost Spear", "Tombak Embun Beku",
                    {"damage": 8, "durability": 1000}),
    "storm_hammer": ("axe", "Storm Hammer", "Palu Badai",
                     {"damage": 11, "durability": 1500}),
    # ---- consumables -----------------------------------------------------
    "mana_potion": ("drink", "Mana Potion", "Ramuan Mana",
                    {"effects": [{"name": "regeneration", "duration": 8,
                                  "amplifier": 1, "chance": 1.0}]}),
    "health_elixir": ("drink", "Health Elixir", "Eliksir Kesehatan",
                      {"effects": [{"name": "instant_health", "duration": 1,
                                    "amplifier": 2, "chance": 1.0}]}),
    "ember_apple": ("food", "Ember Apple", "Apel Bara",
                    {"nutrition": 6, "saturation": 1.2,
                     "effects": [{"name": "fire_resistance", "duration": 20,
                                  "amplifier": 0, "chance": 1.0}]}),
    "void_berry": ("food", "Void Berry", "Beri Void",
                   {"nutrition": 2, "saturation": 0.4,
                    "effects": [{"name": "night_vision", "duration": 15,
                                 "amplifier": 0, "chance": 1.0}]}),
    # ---- arcanite armour -------------------------------------------------
    "arcanite_helmet": ("armor", "Arcanite Helmet", "Helm Arcanite",
                        {"slot": "slot.armor.head", "protection": 3, "durability": 480}),
    "arcanite_chestplate": ("armor", "Arcanite Chestplate", "Rompi Arcanite",
                            {"slot": "slot.armor.chest", "protection": 8, "durability": 480}),
    "arcanite_leggings": ("armor", "Arcanite Leggings", "Celana Arcanite",
                          {"slot": "slot.armor.legs", "protection": 6, "durability": 480}),
    "arcanite_boots": ("armor", "Arcanite Boots", "Sepatu Arcanite",
                       {"slot": "slot.armor.feet", "protection": 3, "durability": 480}),
    # ---- void armour -----------------------------------------------------
    "void_helmet": ("armor", "Void Helmet", "Helm Void",
                    {"slot": "slot.armor.head", "protection": 4, "durability": 620}),
    "void_chestplate": ("armor", "Void Chestplate", "Rompi Void",
                        {"slot": "slot.armor.chest", "protection": 9, "durability": 620}),
    "void_leggings": ("armor", "Void Leggings", "Celana Void",
                      {"slot": "slot.armor.legs", "protection": 7, "durability": 620}),
    "void_boots": ("armor", "Void Boots", "Sepatu Void",
                   {"slot": "slot.armor.feet", "protection": 4, "durability": 620}),
    # ---- misc ------------------------------------------------------------
    "rune_tablet": ("material", "Rune Tablet", "Tablet Rune", {}),
    "arcane_tome": ("material", "Arcane Tome", "Kitab Arcana", {}),
}

ARMOR_GEOMETRY = {
    "slot.armor.head": ("geometry.humanoid.armor.helmet", "helmet_layer_visible", "armor_head"),
    "slot.armor.chest": ("geometry.humanoid.armor.chestplate", "chest_layer_visible", "armor_torso"),
    "slot.armor.legs": ("geometry.humanoid.armor.leggings", "leg_layer_visible", "armor_legs"),
    "slot.armor.feet": ("geometry.humanoid.armor.boots", "boot_layer_visible", "armor_feet"),
}

# ----------------------------------------------------------------- blocks ----
# name: (display, display_id, seconds, light, map_color, render, group)
BLOCKS = {
    "arcanite_block": ("Arcanite Block", "Blok Arcanite", 4.0, 0, "#5b3fc4", "opaque", "metal"),
    "arcanite_ore": ("Arcanite Ore", "Bijih Arcanite", 3.5, 0, "#7c7c82", "opaque", "ore"),
    "deepslate_arcanite_ore": ("Deepslate Arcanite Ore", "Bijih Arcanite Deepslate", 4.5, 0, "#3a3a40", "opaque", "ore"),
    "void_stone": ("Void Stone", "Batu Void", 3.0, 0, "#241640", "opaque", "stone"),
    "void_brick": ("Void Brick", "Bata Void", 3.5, 0, "#432a72", "opaque", "stone"),
    "ember_block": ("Ember Block", "Blok Bara", 3.0, 7, "#c23a12", "opaque", "metal"),
    "frost_block": ("Frost Block", "Blok Embun Beku", 2.5, 3, "#3a8fc4", "opaque", "stone"),
    "rune_brick": ("Rune Brick", "Bata Rune", 3.5, 0, "#7c7c82", "opaque", "stone"),
    "arcane_lamp": ("Arcane Lamp", "Lampu Arcana", 1.5, 15, "#8f74ee", "opaque", "stone"),
    "soul_crystal": ("Soul Crystal", "Kristal Jiwa", 2.0, 10, "#a45cff", "blend", "stone"),
    "mana_crystal_block": ("Mana Crystal Block", "Blok Kristal Mana", 2.0, 12, "#5b3fc4", "blend", "stone"),
    "obsidian_brick": ("Obsidian Brick", "Bata Obsidian", 8.0, 0, "#2a1f3d", "opaque", "stone"),
    "gilded_rune_block": ("Gilded Rune Block", "Blok Rune Berlapis Emas", 4.0, 4, "#d9a521", "opaque", "metal"),
    "mossy_rune_brick": ("Mossy Rune Brick", "Bata Rune Berlumut", 3.5, 0, "#5c6b4a", "opaque", "stone"),
    "cracked_rune_brick": ("Cracked Rune Brick", "Bata Rune Retak", 3.0, 0, "#4e4e52", "opaque", "stone"),
    "storm_block": ("Storm Block", "Blok Badai", 3.0, 6, "#c9a227", "opaque", "metal"),
    "arcane_pillar": ("Arcane Pillar", "Pilar Arcana", 4.0, 0, "#7c7c82", "opaque", "stone"),
    "void_portal_frame": ("Void Portal Frame", "Rangka Portal Void", 12.0, 8, "#432a72", "opaque", "stone"),
}

# Blocks that drop something other than themselves.
ORE_DROPS = {
    "arcanite_ore": ("arcanite_nugget", 2, 5),
    "deepslate_arcanite_ore": ("arcanite_nugget", 3, 6),
    "soul_crystal": ("soul_dust", 1, 3),
    "mana_crystal_block": ("void_shard", 1, 2),
    "frost_block": ("frost_essence", 1, 2),
    "storm_block": ("storm_feather", 1, 2),
    "ember_block": ("ember_core", 1, 2),
}


def item_json(name, kind, extra):
    comps = {
        "minecraft:icon": {"texture": name},
        "minecraft:max_stack_size": 64,
    }
    if kind in ("sword", "pickaxe", "axe"):
        comps["minecraft:max_stack_size"] = 1
        comps["minecraft:hand_equipped"] = True
        comps["minecraft:damage"] = extra["damage"]
        comps["minecraft:durability"] = {"max_durability": extra["durability"]}
        comps["minecraft:enchantable"] = {"value": 14, "slot": "sword" if kind == "sword" else "axe"}
        comps["minecraft:repairable"] = {
            "repair_items": [{"items": ["arcana:arcanite_ingot"], "repair_amount": 300}]
        }
        if kind == "pickaxe":
            comps["minecraft:digger"] = {
                "use_efficiency": True,
                "destroy_speeds": [
                    {"block": {"tags": "stone"}, "speed": 9},
                    {"block": {"tags": "metal"}, "speed": 9},
                ],
            }
    elif kind == "armor":
        comps["minecraft:max_stack_size"] = 1
        comps["minecraft:wearable"] = {
            "slot": extra["slot"],
            "protection": extra["protection"],
        }
        comps["minecraft:durability"] = {"max_durability": extra["durability"]}
        comps["minecraft:enchantable"] = {
            "value": 12, "slot": ARMOR_GEOMETRY[extra["slot"]][2]
        }
        comps["minecraft:repairable"] = {
            "repair_items": [{"items": ["arcana:arcanite_ingot"], "repair_amount": 200}]
        }
    elif kind == "drink":
        comps["minecraft:max_stack_size"] = 1
        comps["minecraft:use_animation"] = "drink"
        comps["minecraft:use_modifiers"] = {"use_duration": 1.6, "movement_modifier": 0.35}
        comps["minecraft:food"] = {
            "nutrition": 0,
            "saturation_modifier": 0,
            "using_converts_to": "minecraft:glass_bottle",
            "effects": extra["effects"],
        }
    elif kind == "food":
        comps["minecraft:use_animation"] = "eat"
        comps["minecraft:use_modifiers"] = {"use_duration": 1.6, "movement_modifier": 0.35}
        comps["minecraft:food"] = {
            "nutrition": extra["nutrition"],
            "saturation_modifier": extra["saturation"],
            "effects": extra["effects"],
        }
    return {
        "format_version": ITEM_FV,
        "minecraft:item": {
            "description": {
                "identifier": "%s:%s" % (NS, name),
                "menu_category": {"category": "equipment" if kind in ("sword", "pickaxe", "axe", "armor") else "items"},
            },
            "components": comps,
        },
    }


def block_json(name, display, seconds, light, map_color, render):
    comps = {
        "minecraft:material_instances": {
            "*": {"texture": name, "render_method": render}
        },
        "minecraft:geometry": "minecraft:geometry.full_block",
        "minecraft:destructible_by_mining": {"seconds_to_destroy": seconds},
        "minecraft:destructible_by_explosion": {"explosion_resistance": max(1, int(seconds))},
        "minecraft:map_color": map_color,
        "minecraft:loot": "loot_tables/blocks/%s.json" % name,
    }
    if light:
        comps["minecraft:light_emission"] = light
    return {
        "format_version": BLOCK_FV,
        "minecraft:block": {
            "description": {
                "identifier": "%s:%s" % (NS, name),
                "menu_category": {"category": "construction"},
            },
            "components": comps,
        },
    }


def loot_json(name):
    if name in ORE_DROPS:
        item, lo, hi = ORE_DROPS[name]
        entry = {
            "type": "item",
            "name": "%s:%s" % (NS, item),
            "weight": 1,
            "functions": [{"function": "set_count", "count": {"min": lo, "max": hi}}],
        }
    else:
        entry = {"type": "item", "name": "%s:%s" % (NS, name), "weight": 1,
                 "functions": [{"function": "set_count", "count": {"min": 1, "max": 1}}]}
    return {"pools": [{"rolls": 1, "entries": [entry]}]}


def attachable_json(name, slot):
    geometry, layer_var, _enchant_slot = ARMOR_GEOMETRY[slot]
    layer = 1 if slot in ("slot.armor.head", "slot.armor.chest") else 2
    family = "arcanite" if name.startswith("arcanite") else "void"
    return {
        "format_version": "1.10.0",
        "minecraft:attachable": {
            "description": {
                "identifier": "%s:%s" % (NS, name),
                "materials": {"default": "armor", "enchanted": "armor_enchanted"},
                "textures": {
                    "default": "textures/models/armor/%s_layer_%d" % (family, layer),
                    "enchanted": "textures/misc/enchanted_actor_glint",
                },
                "geometry": {"default": geometry},
                "scripts": {
                    "parent_setup": "variable.%s = 0.0;" % layer_var
                },
                "render_controllers": ["controller.render.armor"],
            }
        },
    }


# ---------------------------------------------------------------- recipes ----
def shaped(identifier, pattern, keys, result, count=1):
    return {
        "format_version": RECIPE_FV,
        "minecraft:recipe_shaped": {
            "description": {"identifier": "%s:%s" % (NS, identifier)},
            "tags": ["crafting_table"],
            "pattern": pattern,
            "key": {k: {"item": v} for k, v in keys.items()},
            "result": {"item": "%s:%s" % (NS, result), "count": count},
        },
    }


def shapeless(identifier, ingredients, result, count=1):
    return {
        "format_version": RECIPE_FV,
        "minecraft:recipe_shapeless": {
            "description": {"identifier": "%s:%s" % (NS, identifier)},
            "tags": ["crafting_table"],
            "ingredients": [{"item": i} for i in ingredients],
            "result": {"item": "%s:%s" % (NS, result), "count": count},
        },
    }


def furnace(identifier, ingredient, result, count=1):
    return {
        "format_version": RECIPE_FV,
        "minecraft:recipe_furnace": {
            "description": {"identifier": "%s:%s" % (NS, identifier)},
            "tags": ["furnace", "blast_furnace"],
            "input": ingredient,
            "output": "%s:%s" % (NS, result),
        },
    }


RECIPES = [
    # arcanite ingot from nuggets (9 -> 1) and back
    shapeless("arcanite_ingot_from_nuggets", ["arcana:arcanite_nugget"] * 9, "arcanite_ingot"),
    shapeless("arcanite_nugget_from_ingot", ["arcana:arcanite_ingot"], "arcanite_nugget", 9),
    # storage block
    shaped("arcanite_block", ["III", "III", "III"], {"I": "arcana:arcanite_ingot"}, "arcanite_block"),
    shapeless("arcanite_ingot_from_block", ["arcana:arcanite_block"], "arcanite_ingot", 9),
    # smelting ore
    furnace("arcanite_ingot_from_ore", "arcana:arcanite_ore", "arcanite_ingot"),
    furnace("arcanite_ingot_from_deepslate_ore", "arcana:deepslate_arcanite_ore", "arcanite_ingot"),
    # tools
    shaped("arcanite_sword", ["I", "I", "S"], {"I": "arcana:arcanite_ingot", "S": "minecraft:stick"}, "arcanite_sword"),
    shaped("arcanite_pickaxe", ["III", " S ", " S "], {"I": "arcana:arcanite_ingot", "S": "minecraft:stick"}, "arcanite_pickaxe"),
    shaped("arcanite_axe", ["II", "IS", " S"], {"I": "arcana:arcanite_ingot", "S": "minecraft:stick"}, "arcanite_axe"),
    # armour
    shaped("arcanite_helmet", ["III", "I I"], {"I": "arcana:arcanite_ingot"}, "arcanite_helmet"),
    shaped("arcanite_chestplate", ["I I", "III", "III"], {"I": "arcana:arcanite_ingot"}, "arcanite_chestplate"),
    shaped("arcanite_leggings", ["III", "I I", "I I"], {"I": "arcana:arcanite_ingot"}, "arcanite_leggings"),
    shaped("arcanite_boots", ["I I", "I I"], {"I": "arcana:arcanite_ingot"}, "arcanite_boots"),
    # void gear
    shaped("void_dagger", ["V", "S"], {"V": "arcana:void_shard", "S": "minecraft:stick"}, "void_dagger"),
    shaped("void_helmet", ["VVV", "V V"], {"V": "arcana:void_shard"}, "void_helmet"),
    shaped("void_chestplate", ["V V", "VVV", "VVV"], {"V": "arcana:void_shard"}, "void_chestplate"),
    shaped("void_leggings", ["VVV", "V V", "V V"], {"V": "arcana:void_shard"}, "void_leggings"),
    shaped("void_boots", ["V V", "V V"], {"V": "arcana:void_shard"}, "void_boots"),
    # elemental gear
    shaped("ember_staff", [" E", "S ", "S "], {"E": "arcana:ember_core", "S": "minecraft:stick"}, "ember_staff"),
    shaped("frost_spear", ["  F", " S ", "S  "], {"F": "arcana:frost_essence", "S": "minecraft:stick"}, "frost_spear"),
    shaped("storm_hammer", ["TTT", "TST", " S "], {"T": "arcana:storm_feather", "S": "minecraft:stick"}, "storm_hammer"),
    # consumables
    shapeless("mana_potion", ["minecraft:glass_bottle", "arcana:void_shard", "arcana:rune_stone"], "mana_potion"),
    shapeless("health_elixir", ["minecraft:glass_bottle", "arcana:ember_core", "minecraft:glowstone_dust"], "health_elixir"),
    shapeless("ember_apple", ["minecraft:apple", "arcana:ember_core"], "ember_apple"),
    shapeless("void_berry", ["minecraft:sweet_berries", "arcana:soul_dust"], "void_berry"),
    # decorative blocks
    shaped("void_brick", ["VV", "VV"], {"V": "arcana:void_stone"}, "void_brick", 4),
    shaped("rune_brick", ["RS", "SR"], {"R": "arcana:rune_stone", "S": "minecraft:stone_bricks"}, "rune_brick", 4),
    shaped("obsidian_brick", ["OO", "OO"], {"O": "minecraft:obsidian"}, "obsidian_brick", 4),
    shaped("arcane_lamp", [" R ", "RGR", " R "], {"R": "arcana:rune_stone", "G": "minecraft:glowstone"}, "arcane_lamp"),
    shaped("arcane_pillar", ["S", "R", "S"], {"S": "minecraft:stone", "R": "arcana:rune_stone"}, "arcane_pillar", 2),
    shaped("gilded_rune_block", ["GGG", "GRG", "GGG"], {"G": "arcana:gilded_rune", "R": "arcana:rune_stone"}, "gilded_rune_block"),
    shaped("void_portal_frame", ["VRV", "RVR", "VRV"], {"V": "arcana:void_brick", "R": "arcana:gilded_rune"}, "void_portal_frame", 4),
    shaped("mossy_rune_brick", ["RB", "BR"], {"R": "arcana:rune_brick", "B": "minecraft:vine"}, "mossy_rune_brick", 2),
    # misc
    shaped("rune_tablet", ["RSR", "SRS", "RSR"], {"R": "arcana:rune_stone", "S": "arcana:soul_dust"}, "rune_tablet"),
    shaped("arcane_tome", ["RPR", "PBP", "RPR"],
           {"R": "arcana:rune_stone", "P": "minecraft:paper", "B": "minecraft:book"}, "arcane_tome"),
]


def main():
    # ---- manifests -------------------------------------------------------
    dump(os.path.join(BP, "manifest.json"), {
        "format_version": 2,
        "header": {
            "name": "pack.name",
            "description": "pack.description",
            "uuid": UUID_BP_HEADER,
            "version": VERSION,
            "min_engine_version": ENGINE,
        },
        "modules": [{
            "type": "data",
            "uuid": UUID_BP_MODULE,
            "version": VERSION,
        }],
        "metadata": {
            "authors": ["Arcana RPG"],
            "license": "MIT",
            "product_type": "addon",
        },
    })
    dump(os.path.join(RP, "manifest.json"), {
        "format_version": 2,
        "header": {
            "name": "pack.name",
            "description": "pack.description",
            "uuid": UUID_RP_HEADER,
            "version": VERSION,
            "min_engine_version": ENGINE,
        },
        "modules": [{
            "type": "resources",
            "uuid": UUID_RP_MODULE,
            "version": VERSION,
        }],
        "metadata": {
            "authors": ["Arcana RPG"],
            "license": "MIT",
            "product_type": "addon",
        },
        "dependencies": [{"uuid": UUID_BP_HEADER, "version": VERSION}],
    })

    # ---- items -----------------------------------------------------------
    for name, (kind, en, idn, extra) in ITEMS.items():
        dump(os.path.join(BP, "items", name + ".json"), item_json(name, kind, extra))
        if kind == "armor":
            dump(os.path.join(RP, "attachables", name + ".json"),
                 attachable_json(name, extra["slot"]))

    # ---- blocks ----------------------------------------------------------
    for name, (en, idn, secs, light, color, render, group) in BLOCKS.items():
        dump(os.path.join(BP, "blocks", name + ".json"),
             block_json(name, en, secs, light, color, render))
        dump(os.path.join(BP, "loot_tables", "blocks", name + ".json"), loot_json(name))

    # ---- recipes ---------------------------------------------------------
    for r in RECIPES:
        key = list(r.values())[1]["description"]["identifier"].split(":")[1]
        dump(os.path.join(BP, "recipes", key + ".json"), r)

    # ---- item_texture.json ----------------------------------------------
    dump(os.path.join(RP, "textures", "item_texture.json"), {
        "resource_pack_name": "arcana_rpg",
        "texture_name": "atlas.items",
        "texture_data": {
            name: {"textures": "textures/items/%s" % name} for name in ITEMS
        },
    })

    # ---- terrain_texture.json -------------------------------------------
    dump(os.path.join(RP, "textures", "terrain_texture.json"), {
        "resource_pack_name": "arcana_rpg",
        "texture_name": "atlas.terrain",
        "padding": 8,
        "num_mip_levels": 4,
        "texture_data": {
            name: {"textures": "textures/blocks/%s" % name} for name in BLOCKS
        },
    })

    # ---- language files --------------------------------------------------
    for lang, idx in (("en_US", 1), ("id_ID", 2)):
        lines = [
            "pack.name=Arcana RPG",
            "pack.description=Add-on RPG lengkap: 30 item, 18 blok, 2 set armor, dan resep crafting." if lang == "id_ID"
            else "A full RPG add-on: 30 items, 18 blocks, 2 armour sets and crafting recipes.",
        ]
        for name, (kind, en, idn, extra) in ITEMS.items():
            label = en if lang == "en_US" else idn
            lines.append("item.%s:%s=%s" % (NS, name, label))
            lines.append("item.%s:%s.name=%s" % (NS, name, label))
        for name, (en, idn, *_rest) in BLOCKS.items():
            label = en if lang == "en_US" else idn
            lines.append("tile.%s:%s.name=%s" % (NS, name, label))
        os.makedirs(os.path.join(RP, "texts"), exist_ok=True)
        with open(os.path.join(RP, "texts", lang + ".lang"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    print("items=%d blocks=%d recipes=%d attachables=%d"
          % (len(ITEMS), len(BLOCKS), len(RECIPES),
             sum(1 for v in ITEMS.values() if v[0] == "armor")))


if __name__ == "__main__":
    main()
