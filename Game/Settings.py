GRAVITY = 0.5
game_state = "start_menu"
playing_state = "start"
paused = False
player_level = 1
levels = 20
time = 0




def level_load():
    match player_level:
        case 1:
            map_file = "Maps/place_holder_map.tmx"
            start_x = 600
            start_y = 550
            bullet_count = 0
            bullet_max = 4
            

        case 2:
            map_file = "Maps/Level_2_map.tmx"
            start_x = 1072
            start_y = 100
            bullet_count = 0
            bullet_max = 6
            
    
    return map_file, start_x, start_y, bullet_count, bullet_max
