import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/backroads.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (255, 240, 251), progress_bg = (181, 181, 181), p_fg_a = (100, 100, 255), p_fg_b = (255, 150, 150), text_color = (255, 163, 126))