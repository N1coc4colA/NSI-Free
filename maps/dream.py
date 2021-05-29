import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/dream.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (252, 255, 244), progress_bg = (169, 163, 163), p_fg_a = (60, 72, 56), p_fg_b = (168, 172, 95), text_color = (80, 80, 80))