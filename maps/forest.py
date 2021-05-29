import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/forest.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (20, 24, 22), progress_bg = (41, 56, 50), p_fg_a = (113, 137, 65), p_fg_b = (216, 226, 170), text_color = (0, 0, 0))