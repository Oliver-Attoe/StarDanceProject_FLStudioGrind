import pygame
import pytmx
from pytmx.util_pygame import load_pygame


tmx_data = None
tiles = []
open_gates = set()
broken_tiles = set()

portals = []
abilities = []
bad_guys = []
buttons = []

def load_collision():

    tiles.clear()

    for layer in tmx_data.visible_layers:

        if isinstance(layer, pytmx.TiledTileLayer):

            for x, y, gid in layer:

                tile = tmx_data.get_tile_image_by_gid(gid)
                properties = tmx_data.get_tile_properties_by_gid(gid)

                if tile:

                    rect = pygame.Rect(
                        x * tmx_data.tilewidth,
                        y * tmx_data.tileheight,
                        tmx_data.tilewidth,
                        tmx_data.tileheight
                    )

                    tiles.append({
                        "rect": rect,
                        "property": properties
                    })

def load_objects():
    

    for obj in tmx_data.get_layer_by_name("object_layer"):

        if obj.properties.get("portal_type") == "portal":

            portals.append({
                "rect": pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                ),
                "portal_id": obj.properties["portal_id"],
                "portal_target": obj.properties["portal_target"],
                "portal_rotation": obj.properties["portal_rotation"]
            })

        if obj.properties.get("ability_type") == "clock":
            
            abilities.append({"rect": pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                ),
                "collected": False,
                "ability_type": "clock"})

        if obj.properties.get("ability_type") == "reverse_rotation":
            
            abilities.append({"rect": pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                ),
                "collected": False,
                "ability_type": "reverse_rotation"})

        if obj.properties.get("ability_type") == "bullet_pickup":
            
            abilities.append({"rect": pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                ),
                "collected": False,
                "ability_type": "bullet_pickup"})

        if obj.properties.get("ability_type") == "slow_time":
            
            abilities.append({"rect": pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                ),
                "collected": False,
                "ability_type": "slow_time"})
            
        if obj.properties.get("ability_type") == "gravity_swap":
            
            abilities.append({"rect": pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                ),
                "collected": False,
                "ability_type": "gravity_swap"})

        if obj.properties.get("obj_type") == "bad_guy":
            
            bad_guys.append({"rect": pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                ),
                "killed": False})  

        if obj.properties.get("obj_type") == "button":
            
            buttons.append({"rect": pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                ),
                "pressed": False,
                "name": obj.name})  


        


   
 
def draw_map(screen):

    for layer in tmx_data.visible_layers:

        if isinstance(layer, pytmx.TiledTileLayer):

            for x, y, gid in layer:

                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile is None:
                    continue

                properties = tmx_data.get_tile_properties_by_gid(gid)

                tile_type = None

                if properties:
                    tile_type = properties.get("type")

                
                if tile_type in open_gates:

                    image = tile.copy()
                    image.set_alpha(50)

                    screen.blit(
                        image,
                        (
                            x * tmx_data.tilewidth,
                            y * tmx_data.tileheight
                        )
                    )

                if tile_type in broken_tiles:

                    image = tile.copy()
                    image.set_alpha(0)

                    screen.blit(
                        image,
                        (
                            x * tmx_data.tilewidth,
                            y * tmx_data.tileheight
                        )
                    )


                else:

                    screen.blit(
                        tile,
                        (
                            x * tmx_data.tilewidth,
                            y * tmx_data.tileheight
                        )
                    )

def load_level(map_file):

    global tmx_data

    tmx_data = load_pygame(map_file)

    tiles.clear()
    portals.clear()
    abilities.clear()
    bad_guys.clear()
    buttons.clear()

    load_collision()
    load_objects()

    
