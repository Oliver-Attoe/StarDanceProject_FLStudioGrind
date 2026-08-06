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
            map_file = "Maps/Level_1_map.tmx"
            start_x = 600
            start_y = 550
            bullet_count = 0
            bullet_max = 4
            goal_x = 245
            goal_y = 663
            

        case 2:
            map_file = "Maps/Level_2_map.tmx"
            start_x = 1072
            start_y = 550
            bullet_count = 0
            bullet_max = 5
            goal_x = 191
            goal_y = 681

        case 3:
            map_file = "Maps/Level_3_map.tmx"
            start_x = 850
            start_y = 400
            bullet_count = 0
            bullet_max = 5
            goal_x = 1250
            goal_y = 850
            
    
    return map_file, start_x, start_y, bullet_count, bullet_max, goal_x, goal_y
