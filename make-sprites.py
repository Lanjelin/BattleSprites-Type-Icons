#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from requests import session
from PIL import Image, ImageChops, ImageDraw

icon_loc = "res/icons/go-icons/"
icon_box = 24
icon_resize = 16
sprite_loc = "res/sprites/battlesprites/"
out_path = "mod/sprites/battlesprites/"

pk_types = ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "fairy"]
pk_types_icons = {}

api_url = "https://pokeapi.co/api/v2/pokemon/"
s = session()
s.headers["User-Agent"] = "Mozilla/5.0"

def read_icons():
    for icon in os.listdir(icon_loc):
        # Finding and setting type
        icon_type = ""
        for pk_type in pk_types:
            if pk_type in icon.lower():
                icon_type = pk_type
        # Making mask 3 times larger than orig, resizing with antialiasing to get smooth edges
        # Finally applying mask and cropping, storing the result in dict as type
        img_src = Image.open(icon_loc+icon).convert('RGBA')
        mask = Image.new('L', ( img_src.size[0] * 3, img_src.size[1] * 3 ), 0)
        box = 26
        x0, y0 = ( img_src.size[0] - icon_box ) / 2, ( img_src.size[1] - icon_box ) / 2
        ImageDraw.Draw(mask).ellipse([x0 * 3, y0 * 3 , (x0 + icon_box) * 3, (y0 + icon_box) * 3], fill=255)
        mask = mask.resize(img_src.size, resample=Image.LANCZOS)
        mask = ImageChops.darker(mask, img_src.split()[-1])
        img_src.putalpha(mask)
        img_src = img_src.crop((x0, y0, x0 + icon_box, y0 + icon_box))
        if icon_resize:
            img_src = img_src.resize((icon_resize,icon_resize), resample=Image.LANCZOS)
        pk_types_icons.update({icon_type: img_src})

def get_types(pk_id):
    my_types = []
    response = s.get(f"{api_url}{pk_id}/")
    if response.status_code != 200:
        print(f"Failed getting data from api: {pk_id}")
        exit()
    json_data = json.loads(response.text)
    for pk_type in json_data["types"]:
        my_types.append(pk_type["type"]["name"])
    return my_types

def generate_sprites():
    for sprite in os.listdir(sprite_loc):
        sprite_types = get_types(sprite.split('-')[0])
        print(f"{sprite}: {sprite_types}")
        img = Image.open(f"{sprite_loc}{sprite}").convert('RGBA')
        count = 0
        for spr_type in sprite_types:
            img.paste(pk_types_icons[spr_type], ((pk_types_icons[spr_type].size[1] * count), 0) ) # (img.size[0]- pk_types_icons[spr_type].size[0])) )
            count += 1
        img.save(f"{out_path}{sprite}")

read_icons()
generate_sprites()
