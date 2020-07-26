My KB would be used for a self driving car. 

I came up with the rules using road rules and my experience with driving.
--> for example: If you are turning right and there is a red light, treat the red light as a stop sign:
	stop_sign <-- turn_right & red_light

To simplify the rules I assumed that the self driving car would be on a 2 lane road.
For simplicity I also assumed that crosswalks would only appear where there is a light or a stop sign.

Examples of how to use the KB

	Example 1: Turning right after stopping at a red light
	load a4_q2_kb.txt
	tell right_lane red_light right_turn_signal stopped no_crosswalk no_cars
	infer_all

	This would infer "turn_right" using: turn_right <-- right_lane & right_turn_signal
	It would also infer "traffic_clear" using: traffic_clear <-- no_cars & no_crosswalk
	Then it could infer "stop_sign" using: stop_sign <-- turn_right & red_light
	Which would then cause it to infer "go" using: go <-- stop_sign & stopped & traffic_clear
	And then that would infer "gas" using: gas <-- go & stopped

	Example 2: Turning left after stopping at a red light
	load a4_q2_kb.txt
	tell left_lane red_light left_turn_signal
	infer_all

	This would infer "turn_left" using: turn_left <-- left_lane & left_turn_signal
	Then it would infer "stop" using: stop <-- turn_left & red_light
	Which would then cause it to infer "brake" using: brake <-- stop

	Example 3: Turning left at a left turn light
	load a4_q2_kb.txt
	tell left_lane left_turn_light left_turn_signal
	infer_all

	This would infer "turn_left" using: turn_left <-- left_lane & left_turn_signal
	Then it would infer "go" using: go <-- turn_left & left_turn_light