world_conquest_tek_scenario_res(4, 6, 40)
local generators = {
	wct_map_generator("classic", "6a", 75, 23, 10, 17770, 8, 10, 7),
	wct_map_generator("maritime", "6b", 75, 23, 10, 17770, 8, 10, 7),
	wct_map_generator("industrial", "6c", 75, 23, 10, 20125, 7, 10, 7),
	wct_map_generator("feudal", "6d", 75, 23, 10, 17770, 8, 10, 7),
}

local function get_enemy_data(enemy_power)
	return {
		gold = 350,
		bonus_gold = 175,
		sides = {
			wct_enemy(5, 3, 9, 2, 0, 21, (1+enemy_power)),
			wct_enemy(6, 2, 8, 0, 0, "$(3+$wc2_difficulty.enemy_power*2)", (2+enemy_power)),
			wct_enemy(7, 3, 1, 7, 0, "$(3+$wc2_difficulty.enemy_power*2)", (1+enemy_power)),
			wct_enemy(8, 2, 1, 0, 0, "$(3+$wc2_difficulty.enemy_power*2)", (1+enemy_power)),
			wct_enemy(9, 2, 0, 2, 1, "$(3+$wc2_difficulty.enemy_power*2)", 11),
			wct_enemy(10, 2, 1, 4, 1, 21, (1+enemy_power)),
		}
	}
end
return { generators = generators, get_enemy_data = get_enemy_data, turns = 40, player_gold = 350 }
