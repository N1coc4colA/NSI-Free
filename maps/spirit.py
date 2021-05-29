import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/spirit.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (0, 0, 0), progress_bg = (40, 35, 35), p_fg_a = (102, 143, 152), p_fg_b = (204, 244, 255), text_color = (255, 255, 255))