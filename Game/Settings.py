GRAVITY = 0.5
game_state = "start_menu"
playing_state = "start"
paused = False
player_level = 1
levels = 20
time = 0
kill_count = 0



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
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0
       

        case 2:
            map_file = "Maps/Level_2_map.tmx"
            start_x = 1072
            start_y = 550
            bullet_count = 0
            bullet_max = 5
            goal_x = 191
            goal_y = 681#
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0
     

        case 3:
            map_file = "Maps/Level_3_map.tmx"
            start_x = 850
            start_y = 400
            bullet_count = 0
            bullet_max = 5
            goal_x = 200
            goal_y = 700
            m_stars = True
            m_stars_required = 2
            kill_is_req = False
            kills_req = 0
          

        case 4:
            map_file = "Maps/Level_4_map.tmx"#
            start_x = 200
            start_y = 100
            bullet_count = 0
            bullet_max = 7
            goal_x = 1100
            goal_y = 325
            m_stars = False
            m_stars_required = 0
            kill_is_req = False
            kills_req = 0


        case 5:
            map_file = "Maps/Level_5_map.tmx"
            start_x = 400
            start_y = 500
            bullet_count = 0
            bullet_max = 7
            goal_x = 1100
            goal_y = 220
            m_stars = False
            m_stars_required = 0
            kill_is_req = True
            kills_req = 5
    
    return map_file, start_x, start_y, bullet_count, bullet_max, goal_x, goal_y, m_stars, m_stars_required, kill_is_req, kills_req
