CREATE TABLE PITCHES (game_id text, atbat_num int, pitcher_id int, spin_rate float,
                    pitch_type text, start_speed float, end_speed float, nasty int,
                    outcome_shorthand text, outcome text, inning_num int, p_num int,
                    outs_after_bat int, PRIMARY KEY(game_id, inning_num, p_num));