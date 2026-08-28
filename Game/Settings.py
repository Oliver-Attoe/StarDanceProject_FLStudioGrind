GRAVITY = 0.5
game_state = "start_menu"
playing_state = "start"
paused = False
player_level = 1
levels = 50
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

total_stars = 0
level_stars = [[False, False, False] for _ in range(levels)]

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
			goal_x = 750
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 1:
			map_file = "Maps/c_level_1.tmx"
			start_x = 600
			start_y = 550
			
			bullet_max = 4
			goal_x = 245
			goal_y = 663
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 4

		case 2:
			map_file = "Maps/c_level_2.tmx"
			start_x = 1072
			start_y = 150
			
			bullet_max = 5
			goal_x = 1050
			goal_y = 450
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 6

		case 3:
			map_file = "Maps/c_level_3.tmx"
			start_x = 150
			start_y = 675
			
			bullet_max = 6
			goal_x = 500
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 8

		case 4:
			map_file = "Maps/c_level_4.tmx"
			start_x = 200
			start_y = 550
			
			bullet_max = 4
			goal_x = 700
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 4

		case 5:
			map_file = "Maps/c_level_5.tmx"
			start_x = 150
			start_y = 450
			
			bullet_max = 5
			goal_x = 550
			goal_y = 250
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 6

		case 6:
			map_file = "Maps/c_level_6.tmx"
			start_x = 1100
			start_y = 650
			
			bullet_max = 4
			goal_x = 200
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 4

		case 7:
			map_file = "Maps/c_level_7.tmx"
			start_x = 1050
			start_y = 650
			
			bullet_max = 6
			goal_x = 80
			goal_y = 725
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 7

		case 8:
			map_file = "Maps/c_level_8.tmx"
			start_x = 600
			start_y = 150
			
			bullet_max = 4
			goal_x = 1100
			goal_y = 725
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 6

		case 9:
			map_file = "Maps/c_level_9.tmx"
			start_x = 950
			start_y = 225
			
			bullet_max = 6
			goal_x = 1120
			goal_y = 725
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 6

		case 10:
			map_file = "Maps/c_level_10.tmx"
			start_x = 600
			start_y = 600
			
			bullet_max = 5
			goal_x = 650
			goal_y = 240
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 6

		case 11:
			map_file = "Maps/c_level_11.tmx"
			start_x = 600
			start_y = 450
			
			bullet_max = 7
			goal_x = 150
			goal_y = 100
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 10

		case 12:
			map_file = "Maps/c_level_12.tmx"
			start_x = 1000
			start_y = 600
			
			bullet_max = 7
			goal_x = 75
			goal_y = 100
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 15

		case 13:
			map_file = "Maps/c_level_13.tmx"
			start_x = 150
			start_y = 500
			
			bullet_max = 2
			goal_x = 600
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 14:
			map_file = "Maps/c_level_14.tmx"
			start_x = 600
			start_y = 250
			
			bullet_max = 1
			goal_x = 100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 15:
			map_file = "Maps/c_level_15.tmx"
			start_x = 1075
			start_y = 550
			
			bullet_max = 4
			goal_x = 775
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 16:
			map_file = "Maps/c_level_16.tmx"
			start_x = 400
			start_y = 100
			
			bullet_max = 6
			goal_x = 1100
			goal_y = 450
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 17:
			map_file = "Maps/c_level_17.tmx"
			start_x = 1100
			start_y = 200
			
			bullet_max = 6
			goal_x = 100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 18:
			map_file = "Maps/c_level_18.tmx"
			start_x = 600
			start_y = 700
			
			bullet_max = 8
			goal_x = 975
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 19:
			map_file = "Maps/c_level_19.tmx"
			start_x = 150
			start_y = 550
			
			bullet_max = 6
			goal_x = 600
			goal_y = 425
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 20:
			map_file = "Maps/c_level_20.tmx"
			start_x = 600
			start_y = 600
			
			bullet_max = 5
			goal_x = 100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 21:
			map_file = "Maps/c_level_21.tmx"
			start_x = 100
			start_y = 600
			
			bullet_max = 7
			goal_x = 1100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 22:
			map_file = "Maps/c_level_22.tmx"
			start_x = 950
			start_y = 200
			
			bullet_max = 5
			goal_x = 1100
			goal_y = 600
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 23:
			map_file = "Maps/c_level_23.tmx"
			start_x = 175
			start_y = 400
			
			bullet_max = 12
			goal_x = 866
			goal_y = 400
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 24:
			map_file = "Maps/c_level_24.tmx"
			start_x = 125
			start_y = 250
			
			bullet_max = 5
			goal_x = 425
			goal_y = 250
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 25:
			map_file = "Maps/c_level_25.tmx"
			start_x = 900
			start_y = 200
			
			bullet_max = 6
			goal_x = 1100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 26:
			map_file = "Maps/c_level_26.tmx"
			start_x = 1075
			start_y = 550
			
			bullet_max = 9
			goal_x = 460
			goal_y = 150
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 27:
			map_file = "Maps/c_level_27.tmx"
			start_x = 150
			start_y = 200
			
			bullet_max = 7
			goal_x = 900
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 28:
			map_file = "Maps/c_level_28.tmx"
			start_x = 1000
			start_y = 600
			
			bullet_max = 8
			goal_x = 150
			goal_y = 700
			m_stars = True
			m_stars_required = 2
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 29:
			map_file = "Maps/c_level_29.tmx"
			start_x = 550
			start_y = 150
			
			bullet_max = 8
			goal_x = 1100
			goal_y = 700
			m_stars = True
			m_stars_required = 1
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 30:
			map_file = "Maps/c_level_30.tmx"
			start_x = 150
			start_y = 650
			
			bullet_max = 4
			goal_x = 0
			goal_y = 0
			m_stars = True
			m_stars_required = 3
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 31:
			map_file = "Maps/c_level_31.tmx"
			start_x = 1000
			start_y = 300
			
			bullet_max = 10
			goal_x = 1100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = True
			kills_req = 4
			bonus_time = 0

		case 32:
			map_file = "Maps/c_level_32.tmx"
			start_x = 750
			start_y = 150
			
			bullet_max = 8
			goal_x = 1100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = True
			kills_req = 3
			bonus_time = 0

		case 33:
			map_file = "Maps/c_level_33.tmx"
			start_x = 300
			start_y = 150
			
			bullet_max = 6
			goal_x = 1100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 34:
			map_file = "Maps/c_level_34.tmx"
			start_x = 150
			start_y = 600
			
			bullet_max = 4
			goal_x = 1100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 35:
			map_file = "Maps/c_level_35.tmx"
			start_x = 150
			start_y = 250
			
			bullet_max = 5
			goal_x = 1050
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 36:
			map_file = "Maps/c_level_36.tmx"
			start_x = 150
			start_y = 550
			
			bullet_max = 7
			goal_x = 1050
			goal_y = 400
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 37:
			map_file = "Maps/c_level_37.tmx"
			start_x = 150
			start_y = 100
			
			bullet_max = 6
			goal_x = 150
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 38:
			map_file = "Maps/c_level_38.tmx"
			start_x = 500
			start_y = 175
			
			bullet_max = 5
			goal_x = 1100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 39:
			map_file = "Maps/c_level_39.tmx"
			start_x = 1000
			start_y = 150
			
			bullet_max = 5
			goal_x = 400
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 40:
			map_file = "Maps/c_level_40.tmx"
			start_x = 200
			start_y = 400
			
			bullet_max = 7
			goal_x = 650
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = True
			kills_req = 1
			bonus_time = 0

		case 41:
			map_file = "Maps/c_level_41.tmx"
			start_x = 150
			start_y = 450
			
			bullet_max = 7
			goal_x = 1100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = True
			kills_req = 1
			bonus_time = 0

		case 42:
			map_file = "Maps/c_level_42.tmx"
			start_x = 1050
			start_y = 350
			
			bullet_max = 3
			goal_x = 1100
			goal_y = 400
			m_stars = False
			m_stars_required = 0
			kill_is_req = True
			kills_req = 1
			bonus_time = 0

		case 43:
			map_file = "Maps/c_level_43.tmx"
			start_x = 150
			start_y = 300			
			bullet_max = 10
			goal_x = 1100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = True
			kills_req = 1
			bonus_time = 0

		case 44:
			map_file = "Maps/c_level_44.tmx"
			start_x = 550
			start_y = 100
			
			bullet_max = 5
			goal_x = 1100
			goal_y = 350
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 45:
			map_file = "Maps/c_level_45.tmx"
			start_x = 600
			start_y = 250
			
			bullet_max = 6
			goal_x = 100
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = True
			kills_req = 1
			bonus_time = 0

		case 46:
			map_file = "Maps/c_level_46.tmx"
			start_x = 1075
			start_y = 550
			
			bullet_max = 10
			goal_x = 225
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 47:
			map_file = "Maps/c_level_47.tmx"
			start_x = 250
			start_y = 650
			
			bullet_max = 6
			goal_x = 600
			goal_y = 700
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 48:
			map_file = "Maps/c_level_48.tmx"
			start_x = 575
			start_y = 250
			
			bullet_max = 12
			goal_x = 575
			goal_y = 250
			m_stars = True
			m_stars_required = 2
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 49:
			map_file = "Maps/c_level_49.tmx"
			start_x = 0
			start_y = 0
			
			bullet_max = 12
			goal_x = 0
			goal_y = 0
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

		case 50:
			map_file = "Maps/c_level_50.tmx"
			start_x = 0
			start_y = 0
			
			bullet_max = 12
			goal_x = 0
			goal_y = 0
			m_stars = False
			m_stars_required = 0
			kill_is_req = False
			kills_req = 0
			bonus_time = 0

	return map_file, start_x, start_y, bullet_max, goal_x, goal_y, m_stars, m_stars_required, kill_is_req, kills_req, bonus_time


def set_gun_image():

	match gun:
		case 0:
			return "GUN0.png"

		case 1:
			return "GUN.png"

		case 2:
			return "GUN2.png"

