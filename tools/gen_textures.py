#!/usr/bin/env python3
"""Arcana RPG - pixel-art texture generator.

Every texture is authored as SVG (one <rect> per pixel, crisp edges) and then
rasterised to PNG with rsvg-convert, because Minecraft only accepts PNG.
"""
import os
import subprocess
import math
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, "art", "svg")
RP = os.path.join(ROOT, "src", "ArcanaRP")
ITEM_PNG = os.path.join(RP, "textures", "items")
BLOCK_PNG = os.path.join(RP, "textures", "blocks")
ARMOR_PNG = os.path.join(RP, "textures", "models", "armor")

# ---------------------------------------------------------------- palette ----
P = {
    "arc_d": "#2b1d63", "arc": "#5b3fc4", "arc_l": "#8f74ee", "arc_xl": "#c3b2ff",
    "void_d": "#0d0718", "void": "#241640", "void_l": "#432a72", "void_g": "#a45cff",
    "emb_d": "#5c1a06", "emb": "#c23a12", "emb_l": "#ff7a2f", "emb_xl": "#ffc46b",
    "fro_d": "#17415e", "fro": "#3a8fc4", "fro_l": "#7fd8ff", "fro_xl": "#d6f6ff",
    "sto_d": "#8a6a10", "sto": "#c9a227", "sto_l": "#ffe066", "sto_xl": "#fff8c4",
    "gold_d": "#8a5f0a", "gold": "#d9a521", "gold_l": "#ffd24a", "gold_xl": "#fff0a8",
    "wood_d": "#4a2c12", "wood": "#7a4a22", "wood_l": "#a9713c",
    "stone_d": "#4e4e52", "stone": "#7c7c82", "stone_l": "#a8a8b0",
    "leather_d": "#3d2716", "leather": "#6b4a2f", "leather_l": "#8f6a45",
    "bone": "#e8e2d0", "bone_d": "#b3ab95",
    "white": "#ffffff", "black": "#0a0a0f",
    "glass": "#cfe9ff", "glass_d": "#8fb8d8",
    "red": "#d63b3b", "green": "#4fbf5f", "blue": "#3f7fd6",
}


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = {}

    def set(self, x, y, c):
        x, y = int(x), int(y)
        if c and 0 <= x < self.w and 0 <= y < self.h:
            self.px[(x, y)] = c

    def get(self, x, y):
        return self.px.get((int(x), int(y)))

    def rect(self, x, y, w, h, c):
        for yy in range(int(y), int(y + h)):
            for xx in range(int(x), int(x + w)):
                self.set(xx, yy, c)

    def frame(self, x, y, w, h, c):
        for xx in range(int(x), int(x + w)):
            self.set(xx, y, c)
            self.set(xx, y + h - 1, c)
        for yy in range(int(y), int(y + h)):
            self.set(x, yy, c)
            self.set(x + w - 1, yy, c)

    def line(self, x0, y0, x1, y1, c, thick=1):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for ox in range(thick):
                for oy in range(thick):
                    self.set(x0 + ox, y0 + oy, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for y in range(int(cy - r), int(cy + r) + 1):
            for x in range(int(cx - r), int(cx + r) + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.set(x, y, c)

    def ring(self, cx, cy, r, c):
        for y in range(int(cy - r - 1), int(cy + r) + 2):
            for x in range(int(cx - r - 1), int(cx + r) + 2):
                d = math.hypot(x - cx, y - cy)
                if r - 0.6 <= d <= r + 0.4:
                    self.set(x, y, c)

    def diamond(self, cx, cy, r, c):
        for y in range(int(cy - r), int(cy + r) + 1):
            for x in range(int(cx - r), int(cx + r) + 1):
                if abs(x - cx) + abs(y - cy) <= r:
                    self.set(x, y, c)

    def svg(self):
        out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
               'viewBox="0 0 %d %d" shape-rendering="crispEdges">'
               % (self.w, self.h, self.w, self.h)]
        for (x, y), c in sorted(self.px.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            out.append('<rect x="%d" y="%d" width="1" height="1" fill="%s"/>' % (x, y, c))
        out.append("</svg>")
        return "".join(out)


# ------------------------------------------------------------ item shapes ----
def sword(c, blade, blade_l, blade_d, guard, grip):
    c.line(4, 12, 11, 5, blade_d, 2)
    c.line(4, 11, 10, 5, blade, 2)
    c.line(4, 11, 10, 5, blade_l, 1)
    c.line(3, 12, 6, 15, guard, 2)      # crossguard
    c.line(2, 13, 4, 15, grip, 2)       # grip
    c.set(2, 15, guard)
    c.set(1, 14, guard)


def dagger(c, blade, blade_l, blade_d, guard, grip):
    c.line(6, 10, 11, 5, blade_d, 2)
    c.line(6, 9, 10, 5, blade, 2)
    c.line(6, 9, 10, 5, blade_l, 1)
    c.line(5, 10, 8, 13, guard, 2)
    c.line(4, 11, 6, 13, grip, 2)


def pickaxe(c, head, head_l, head_d, stick, stick_d):
    c.line(3, 13, 11, 5, stick_d, 2)
    c.line(3, 12, 11, 4, stick, 2)
    c.line(2, 4, 12, 4, head_d, 2)
    c.line(2, 3, 12, 3, head, 2)
    c.line(3, 2, 11, 2, head_l, 1)
    c.set(1, 5, head_d); c.set(13, 5, head_d)
    c.set(2, 5, head); c.set(12, 5, head)


def axe(c, head, head_l, head_d, stick, stick_d):
    c.line(4, 14, 10, 6, stick_d, 2)
    c.line(4, 13, 10, 5, stick, 2)
    c.rect(8, 2, 5, 6, head_d)
    c.rect(8, 2, 4, 5, head)
    c.rect(8, 2, 2, 4, head_l)
    c.set(7, 3, head_d); c.set(7, 4, head_d); c.set(7, 5, head_d)


def ingot(c, base, light, dark):
    c.rect(3, 6, 10, 5, dark)
    c.rect(4, 5, 9, 5, base)
    c.rect(5, 5, 7, 2, light)
    c.rect(4, 9, 9, 1, dark)
    c.set(3, 6, dark); c.set(12, 6, dark)


def nugget(c, base, light, dark):
    c.disc(8, 8, 3.2, dark)
    c.disc(8, 8, 2.6, base)
    c.disc(7, 7, 1.2, light)


def shard(c, base, light, dark, glow):
    c.diamond(8, 8, 5, dark)
    c.diamond(8, 8, 4, base)
    c.line(8, 4, 8, 12, light)
    c.line(6, 7, 8, 5, light)
    c.set(8, 8, glow); c.set(7, 9, glow)


def crystal(c, base, light, dark, glow):
    c.rect(6, 3, 4, 10, dark)
    c.rect(6, 3, 3, 9, base)
    c.rect(6, 3, 1, 8, light)
    c.set(7, 2, light); c.set(8, 2, light)
    c.set(7, 13, dark); c.set(8, 13, dark)
    c.set(7, 7, glow); c.set(8, 8, glow)


def dust(c, base, light, dark):
    c.disc(8, 10, 4, dark)
    c.disc(8, 10, 3.2, base)
    c.set(6, 8, light); c.set(9, 7, light); c.set(10, 9, light)
    c.set(5, 11, light); c.set(11, 11, dark)


def feather(c, base, light, dark):
    c.line(4, 13, 11, 3, dark, 1)
    for i in range(6):
        c.line(5 + i, 11 - i, 8 + i, 8 - i, base, 1)
    c.line(5, 12, 10, 4, light, 1)


def potion(c, liquid, liquid_l, glass, cork):
    c.rect(6, 2, 4, 2, cork)
    c.rect(6, 4, 4, 2, glass)
    c.rect(4, 6, 8, 8, glass)
    c.rect(5, 8, 6, 5, liquid)
    c.rect(5, 8, 2, 4, liquid_l)
    c.set(4, 6, glass); c.set(11, 6, glass)
    c.set(5, 13, glass); c.set(10, 13, glass)


def apple(c, body, body_l, body_d, stem, leaf):
    c.disc(8, 9, 4.4, body_d)
    c.disc(8, 9, 3.8, body)
    c.disc(6, 7, 1.4, body_l)
    c.rect(8, 3, 1, 3, stem)
    c.rect(9, 3, 2, 1, leaf)


def berry(c, body, body_l, body_d):
    for (cx, cy, r) in ((6, 9, 2.4), (10, 9, 2.4), (8, 6, 2.4)):
        c.disc(cx, cy, r, body_d)
        c.disc(cx, cy, r - 0.7, body)
        c.set(cx - 1, cy - 1, body_l)


def tome(c, cover, cover_l, cover_d, page, rune):
    c.rect(3, 3, 10, 11, cover_d)
    c.rect(4, 3, 9, 10, cover)
    c.rect(4, 3, 2, 10, cover_l)
    c.rect(11, 4, 2, 9, page)
    c.rect(6, 6, 4, 1, rune)
    c.rect(6, 8, 4, 1, rune)
    c.rect(6, 10, 3, 1, rune)


def tablet(c, base, light, dark, rune):
    c.rect(3, 2, 10, 12, dark)
    c.rect(4, 3, 8, 10, base)
    c.rect(4, 3, 8, 1, light)
    c.rect(6, 5, 4, 1, rune)
    c.rect(5, 7, 6, 1, rune)
    c.rect(6, 9, 4, 1, rune)
    c.rect(7, 11, 2, 1, rune)


def staff(c, shaft, shaft_d, orb, orb_l, orb_d):
    c.line(4, 14, 10, 6, shaft_d, 2)
    c.line(4, 13, 10, 5, shaft, 2)
    c.disc(11, 4, 3.2, orb_d)
    c.disc(11, 4, 2.4, orb)
    c.set(10, 3, orb_l); c.set(11, 3, orb_l)


def spear(c, shaft, shaft_d, tip, tip_l, tip_d):
    c.line(3, 14, 10, 7, shaft_d, 2)
    c.line(3, 13, 10, 6, shaft, 2)
    c.diamond(11, 5, 3, tip_d)
    c.diamond(11, 5, 2, tip)
    c.set(11, 4, tip_l)


def core(c, base, light, dark, glow):
    c.disc(8, 8, 5, dark)
    c.disc(8, 8, 4, base)
    c.disc(8, 8, 2.4, glow)
    c.set(7, 6, light); c.set(6, 7, light)


def rune_stone(c, base, light, dark, rune):
    c.disc(8, 8, 5.2, dark)
    c.disc(8, 8, 4.4, base)
    c.line(8, 4, 8, 12, rune)
    c.line(5, 7, 11, 7, rune)
    c.set(6, 10, rune); c.set(10, 10, rune)


def helmet(c, base, light, dark, trim):
    c.rect(3, 5, 10, 7, dark)
    c.rect(4, 4, 8, 7, base)
    c.rect(4, 4, 8, 2, light)
    c.rect(4, 9, 8, 2, dark)
    c.rect(6, 8, 4, 3, trim)
    c.set(3, 6, dark); c.set(12, 6, dark)


def chestplate(c, base, light, dark, trim):
    c.rect(3, 3, 10, 10, dark)
    c.rect(4, 4, 8, 8, base)
    c.rect(4, 4, 8, 2, light)
    c.rect(7, 4, 2, 8, trim)
    c.rect(4, 10, 8, 2, dark)


def leggings(c, base, light, dark, trim):
    c.rect(4, 2, 8, 4, dark)
    c.rect(4, 2, 8, 3, base)
    c.rect(4, 2, 8, 1, light)
    c.rect(4, 6, 3, 8, base)
    c.rect(9, 6, 3, 8, base)
    c.rect(4, 6, 3, 1, trim)
    c.rect(9, 6, 3, 1, trim)
    c.rect(4, 13, 3, 1, dark)
    c.rect(9, 13, 3, 1, dark)


def boots(c, base, light, dark, trim):
    c.rect(3, 6, 4, 7, base)
    c.rect(9, 6, 4, 7, base)
    c.rect(3, 6, 4, 1, light)
    c.rect(9, 6, 4, 1, light)
    c.rect(3, 12, 5, 2, dark)
    c.rect(8, 12, 5, 2, dark)
    c.rect(3, 9, 4, 1, trim)
    c.rect(9, 9, 4, 1, trim)


# ----------------------------------------------------------- block shapes ----
def block_plain(c, base, light, dark, accent=None, density=0.18, seed=1):
    rnd = random.Random(seed)
    c.rect(0, 0, 16, 16, base)
    for y in range(16):
        for x in range(16):
            r = rnd.random()
            if r < density:
                c.set(x, y, dark)
            elif r < density * 2:
                c.set(x, y, light)
    c.rect(0, 0, 16, 1, light)
    c.rect(0, 0, 1, 16, light)
    c.rect(0, 15, 16, 1, dark)
    c.rect(15, 0, 1, 16, dark)
    if accent:
        for _ in range(6):
            c.set(rnd.randrange(2, 14), rnd.randrange(2, 14), accent)


def block_bricks(c, base, light, dark, mortar, seed=2):
    rnd = random.Random(seed)
    c.rect(0, 0, 16, 16, mortar)
    rows = [(0, 7), (8, 15)]
    for (y0, y1) in rows:
        c.rect(0, y0, 16, 7, base)
        c.rect(0, y0, 16, 1, light)
        c.rect(0, y1, 16, 1, dark)
    c.rect(7, 0, 1, 7, mortar)
    c.rect(3, 8, 1, 7, mortar)
    c.rect(11, 8, 1, 7, mortar)
    for _ in range(10):
        c.set(rnd.randrange(16), rnd.randrange(16), dark)


def block_ore(c, stone, stone_l, stone_d, ore, ore_l, seed=3):
    block_plain(c, stone, stone_l, stone_d, density=0.22, seed=seed)
    rnd = random.Random(seed + 50)
    for _ in range(5):
        cx, cy = rnd.randrange(3, 13), rnd.randrange(3, 13)
        c.disc(cx, cy, 1.6, ore)
        c.set(cx, cy, ore_l)


def block_crystal(c, base, light, dark, glow, seed=4):
    rnd = random.Random(seed)
    c.rect(0, 0, 16, 16, dark)
    for i in range(0, 16, 4):
        c.rect(i, 0, 2, 16, base)
        c.rect(i, 0, 1, 16, light)
    for _ in range(14):
        c.set(rnd.randrange(16), rnd.randrange(16), glow)
    c.rect(0, 0, 16, 1, light)
    c.rect(0, 15, 16, 1, dark)


def block_lamp(c, base, light, dark, glow, seed=5):
    c.rect(0, 0, 16, 16, dark)
    c.rect(1, 1, 14, 14, base)
    c.rect(2, 2, 12, 12, glow)
    c.rect(4, 4, 8, 8, light)
    c.frame(0, 0, 16, 16, dark)
    c.frame(1, 1, 14, 14, base)
    for (x, y) in ((3, 3), (12, 3), (3, 12), (12, 12)):
        c.set(x, y, dark)


def block_pillar(c, base, light, dark, accent, seed=6):
    c.rect(0, 0, 16, 16, base)
    c.rect(0, 0, 16, 2, light)
    c.rect(0, 14, 16, 2, dark)
    c.rect(2, 2, 12, 12, dark)
    c.rect(3, 3, 10, 10, base)
    c.rect(6, 3, 4, 10, accent)
    c.rect(6, 3, 1, 10, light)
    c.rect(0, 0, 1, 16, light)
    c.rect(15, 0, 1, 16, dark)


def block_portal_frame(c, base, light, dark, glow, seed=7):
    c.rect(0, 0, 16, 16, dark)
    c.rect(1, 1, 14, 14, base)
    c.rect(2, 2, 12, 12, dark)
    c.rect(3, 3, 10, 10, base)
    c.ring(8, 8, 4.2, glow)
    c.ring(8, 8, 2.2, light)
    c.set(8, 8, glow)
    c.frame(0, 0, 16, 16, dark)


# ------------------------------------------------------------ definitions ----
ITEMS = {
    # materials
    "arcanite_ingot": lambda c: ingot(c, P["arc"], P["arc_l"], P["arc_d"]),
    "arcanite_nugget": lambda c: nugget(c, P["arc"], P["arc_l"], P["arc_d"]),
    "void_shard": lambda c: shard(c, P["void_l"], P["void_g"], P["void_d"], P["void_g"]),
    "ember_core": lambda c: core(c, P["emb"], P["emb_xl"], P["emb_d"], P["emb_l"]),
    "frost_essence": lambda c: crystal(c, P["fro"], P["fro_xl"], P["fro_d"], P["fro_l"]),
    "storm_feather": lambda c: feather(c, P["sto_l"], P["sto_xl"], P["sto_d"]),
    "rune_stone": lambda c: rune_stone(c, P["stone"], P["stone_l"], P["stone_d"], P["arc_l"]),
    "soul_dust": lambda c: dust(c, P["void_l"], P["void_g"], P["void_d"]),
    "gilded_rune": lambda c: rune_stone(c, P["gold"], P["gold_xl"], P["gold_d"], P["emb_l"]),
    # weapons / tools
    "arcanite_sword": lambda c: sword(c, P["arc"], P["arc_xl"], P["arc_d"], P["gold"], P["wood"]),
    "arcanite_pickaxe": lambda c: pickaxe(c, P["arc"], P["arc_xl"], P["arc_d"], P["wood"], P["wood_d"]),
    "arcanite_axe": lambda c: axe(c, P["arc"], P["arc_xl"], P["arc_d"], P["wood"], P["wood_d"]),
    "void_dagger": lambda c: dagger(c, P["void_l"], P["void_g"], P["void_d"], P["stone_l"], P["leather"]),
    "ember_staff": lambda c: staff(c, P["wood"], P["wood_d"], P["emb_l"], P["emb_xl"], P["emb_d"]),
    "frost_spear": lambda c: spear(c, P["wood"], P["wood_d"], P["fro_l"], P["fro_xl"], P["fro_d"]),
    "storm_hammer": lambda c: axe(c, P["sto"], P["sto_xl"], P["sto_d"], P["wood"], P["wood_d"]),
    # consumables
    "mana_potion": lambda c: potion(c, P["arc"], P["arc_xl"], P["glass"], P["wood"]),
    "health_elixir": lambda c: potion(c, P["red"], "#ff8a8a", P["glass"], P["wood"]),
    "ember_apple": lambda c: apple(c, P["emb_l"], P["emb_xl"], P["emb_d"], P["wood_d"], P["green"]),
    "void_berry": lambda c: berry(c, P["void_l"], P["void_g"], P["void_d"]),
    # armor - arcanite
    "arcanite_helmet": lambda c: helmet(c, P["arc"], P["arc_xl"], P["arc_d"], P["gold_l"]),
    "arcanite_chestplate": lambda c: chestplate(c, P["arc"], P["arc_xl"], P["arc_d"], P["gold_l"]),
    "arcanite_leggings": lambda c: leggings(c, P["arc"], P["arc_xl"], P["arc_d"], P["gold_l"]),
    "arcanite_boots": lambda c: boots(c, P["arc"], P["arc_xl"], P["arc_d"], P["gold_l"]),
    # armor - void
    "void_helmet": lambda c: helmet(c, P["void_l"], P["void_g"], P["void_d"], P["arc_l"]),
    "void_chestplate": lambda c: chestplate(c, P["void_l"], P["void_g"], P["void_d"], P["arc_l"]),
    "void_leggings": lambda c: leggings(c, P["void_l"], P["void_g"], P["void_d"], P["arc_l"]),
    "void_boots": lambda c: boots(c, P["void_l"], P["void_g"], P["void_d"], P["arc_l"]),
    # misc
    "rune_tablet": lambda c: tablet(c, P["stone"], P["stone_l"], P["stone_d"], P["arc_l"]),
    "arcane_tome": lambda c: tome(c, P["arc_d"], P["arc"], P["void_d"], P["bone"], P["gold_l"]),
}

BLOCKS = {
    "arcanite_block": lambda c: block_plain(c, P["arc"], P["arc_l"], P["arc_d"], P["arc_xl"], 0.16, 11),
    "arcanite_ore": lambda c: block_ore(c, P["stone"], P["stone_l"], P["stone_d"], P["arc"], P["arc_xl"], 12),
    "deepslate_arcanite_ore": lambda c: block_ore(c, "#3a3a40", "#4e4e56", "#26262b", P["arc"], P["arc_xl"], 13),
    "void_stone": lambda c: block_plain(c, P["void"], P["void_l"], P["void_d"], P["void_g"], 0.2, 14),
    "void_brick": lambda c: block_bricks(c, P["void_l"], P["void_g"], P["void_d"], P["void_d"], 15),
    "ember_block": lambda c: block_plain(c, P["emb"], P["emb_l"], P["emb_d"], P["emb_xl"], 0.2, 16),
    "frost_block": lambda c: block_crystal(c, P["fro"], P["fro_l"], P["fro_d"], P["fro_xl"], 17),
    "rune_brick": lambda c: block_bricks(c, P["stone"], P["stone_l"], P["stone_d"], P["arc_d"], 18),
    "arcane_lamp": lambda c: block_lamp(c, P["arc_d"], P["arc_xl"], P["void_d"], P["arc_l"], 19),
    "soul_crystal": lambda c: block_crystal(c, P["void_l"], P["void_g"], P["void_d"], P["arc_xl"], 20),
    "mana_crystal_block": lambda c: block_crystal(c, P["arc"], P["arc_xl"], P["arc_d"], P["arc_xl"], 21),
    "obsidian_brick": lambda c: block_bricks(c, "#2a1f3d", "#3d2d57", "#150f22", "#0d0718", 22),
    "gilded_rune_block": lambda c: block_plain(c, P["gold"], P["gold_xl"], P["gold_d"], P["emb_l"], 0.18, 23),
    "mossy_rune_brick": lambda c: block_bricks(c, "#5c6b4a", "#7d8f66", "#3d4a30", P["arc_d"], 24),
    "cracked_rune_brick": lambda c: block_bricks(c, P["stone_d"], P["stone"], "#3a3a40", P["arc_d"], 25),
    "storm_block": lambda c: block_plain(c, P["sto"], P["sto_xl"], P["sto_d"], P["sto_l"], 0.22, 26),
    "arcane_pillar": lambda c: block_pillar(c, P["stone"], P["stone_l"], P["stone_d"], P["arc"], 27),
    "void_portal_frame": lambda c: block_portal_frame(c, P["void_l"], P["void_g"], P["void_d"], P["arc_xl"], 28),
}

ARMOR_LAYERS = {
    "arcanite_layer_1": (P["arc"], P["arc_l"], P["arc_d"], P["gold_l"]),
    "arcanite_layer_2": (P["arc"], P["arc_l"], P["arc_d"], P["gold_l"]),
    "void_layer_1": (P["void_l"], P["void_g"], P["void_d"], P["arc_l"]),
    "void_layer_2": (P["void_l"], P["void_g"], P["void_d"], P["arc_l"]),
}


def armor_layer(base, light, dark, trim, layer):
    """64x32 armour UV sheet: head/body/arms (layer 1) or legs/boots (layer 2).

    The sheet is a UV atlas, not a picture, so detail is added as plating bands
    and rivets that read correctly once wrapped onto the player model.
    """
    c = Canvas(64, 32)
    c.rect(0, 0, 64, 32, dark)
    if layer == 1:
        boxes = [(0, 0, 32, 16), (16, 16, 24, 16), (40, 16, 16, 16)]
    else:
        boxes = [(0, 16, 16, 16), (16, 16, 24, 16), (0, 0, 16, 16), (16, 0, 24, 16)]
    for (x, y, w, h) in boxes:
        c.rect(x, y, w, h, base)
        # vertical plating: alternate a slightly darker column every 4px
        for xx in range(x + 2, x + w - 2, 4):
            c.rect(xx, y + 1, 1, h - 2, dark)
        # horizontal plate seams
        for yy in range(y + 4, y + h - 2, 5):
            c.rect(x + 1, yy, w - 2, 1, dark)
            c.rect(x + 1, yy + 1, w - 2, 1, light)
        # top highlight / bottom shadow
        c.rect(x, y, w, 1, light)
        c.rect(x, y + h - 1, w, 1, dark)
        c.rect(x, y, 1, h, light)
        c.rect(x + w - 1, y, 1, h, dark)
        # trim band + rivets
        c.rect(x + 1, y + 2, w - 2, 1, trim)
        for xx in range(x + 3, x + w - 3, 6):
            c.set(xx, y + 2, light)
            c.set(xx, y + h - 4, trim)
    return c


def pack_icon():
    """128x128 pack icon: rune circle over a void-purple field."""
    c = Canvas(128, 128)
    for y in range(128):
        for x in range(128):
            d = math.hypot(x - 64, y - 64) / 90.0
            if d < 0.35:
                c.set(x, y, "#3a2470")
            elif d < 0.7:
                c.set(x, y, "#241640")
            else:
                c.set(x, y, "#120b22")
    c.ring(64, 64, 46, "#8f74ee")
    c.ring(64, 64, 42, "#5b3fc4")
    c.ring(64, 64, 30, "#c3b2ff")
    # rune spokes
    for i in range(8):
        a = i * math.pi / 4
        c.line(64 + 30 * math.cos(a), 64 + 30 * math.sin(a),
               64 + 42 * math.cos(a), 64 + 42 * math.sin(a), "#8f74ee", 2)
    # central diamond
    c.diamond(64, 64, 20, "#5b3fc4")
    c.diamond(64, 64, 15, "#8f74ee")
    c.diamond(64, 64, 8, "#c3b2ff")
    c.diamond(64, 64, 4, "#ffffff")
    # corner sparks
    for (x, y) in ((18, 18), (110, 18), (18, 110), (110, 110)):
        c.diamond(x, y, 4, "#ffd24a")
        c.diamond(x, y, 2, "#fff0a8")
    return c


def write_svg(name, canvas, folder):
    path = os.path.join(SVG_DIR, folder, name + ".svg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(canvas.svg())
    return path


def convert(svg_path, png_path):
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    subprocess.run(["rsvg-convert", "-o", png_path, svg_path], check=True)


def main():
    made = []
    for name, fn in ITEMS.items():
        c = Canvas(16, 16)
        fn(c)
        svg = write_svg(name, c, "items")
        png = os.path.join(ITEM_PNG, name + ".png")
        convert(svg, png)
        made.append(png)

    for name, fn in BLOCKS.items():
        c = Canvas(16, 16)
        fn(c)
        svg = write_svg(name, c, "blocks")
        png = os.path.join(BLOCK_PNG, name + ".png")
        convert(svg, png)
        made.append(png)

    for name, (base, light, dark, trim) in ARMOR_LAYERS.items():
        layer = 1 if name.endswith("_1") else 2
        c = armor_layer(base, light, dark, trim, layer)
        svg = write_svg(name, c, "armor")
        png = os.path.join(ARMOR_PNG, name + ".png")
        convert(svg, png)
        made.append(png)

    icon = pack_icon()
    svg = write_svg("pack_icon", icon, ".")
    for pack in ("ArcanaRP", "ArcanaBP"):
        convert(svg, os.path.join(ROOT, "src", pack, "pack_icon.png"))

    print("generated %d textures" % len(made))


if __name__ == "__main__":
    main()
