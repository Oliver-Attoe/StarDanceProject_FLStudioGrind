GRAVITY = 0.5
game_state = "start_menu" 
playing_state = "start"
paused = False
player_level = 1
levels = 20
time = 0
bullet_count = 0
kill_count = 0
max_player_level = 1
gun = 1
signing = False
time_multiplyer = 1
slow_time_duration = 3000
slow_time_start = 0
slow_time_active = False


def level_lock():
    global max_player_level

    if player_level >= max_player_level:
        max_player_level = player_level + 1


def level_load():
    match player_level:

        case 0:
            map_file = "Maps/There is a man level.tmx"
            start_x = 1050
            start_y = 675
            
            bullet_max = 4
            goal_x = 6
            goal_y = 6
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0
        case 1:
            map_file = "Maps/Level_1_map.tmx"
            start_x = 600
            start_y = 550
            
            bullet_max = 4
            goal_x = 245
            goal_y = 663
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0
       

        case 2:
            map_file = "Maps/Level_2_map.tmx"
            start_x = 1072
            start_y = 150
            
            bullet_max = 4
            goal_x = 1050
            goal_y = 450
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0
     

        case 3:
            map_file = "Maps/Level_3_map.tmx"
            start_x = 150
            start_y = 675
            
            bullet_max = 6
            goal_x = 500
            goal_y = 700
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0

        case 4:
            map_file = "Maps/Level_4_map.tmx"#
            start_x = 200
            start_y = 550
            
            bullet_max = 4
            goal_x = 700
            goal_y = 700
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0


        case 5:
            map_file = "Maps/Level_5_map.tmx"
            start_x = 150
            start_y = 450
            
            bullet_max = 5
            goal_x = 550
            goal_y = 250
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0

        case 6:
            map_file = "Maps/Level_6_map.tmx"
            start_x = 1100
            start_y = 650
        
            bullet_max = 4
            goal_x = 200
            goal_y = 700
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0

        case 7:
            map_file = "Maps/Level_7_map.tmx"
            start_x = 200
            start_y = 500
            
            bullet_max = 2
            goal_x = 1100
            goal_y = 700
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0#

        case 8:
            map_file = "Maps/Level_8_map.tmx"
            start_x = 1100
            start_y = 650
        
            bullet_max = 4
            goal_x = 200
            goal_y = 700
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0

        case 9:

            map_file = "Maps/Level_9_map.tmx"
            start_x = 1100
            start_y = 650
        
            bullet_max = 4
            goal_x = 200
            goal_y = 700
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0


               
    return map_file, start_x, start_y, bullet_max, goal_x, goal_y, m_stars, m_stars_required, kill_is_req, kills_req

def set_gun_image():

    match gun:
        case 0:
            return "GUN0.png"

        case 1:
            return "GUN.png"

        case 2:
            return "GUN2.png"