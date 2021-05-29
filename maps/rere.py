import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/rere.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (0, 0, 0), progress_bg = (80, 80, 80), p_fg_a = (104, 42, 53), p_fg_b = (216, 156, 81), text_color = (255, 255, 255))