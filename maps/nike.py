import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/nike.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (0, 0, 0), progress_bg = (200, 200, 200), p_fg_a = (168, 0, 64), p_fg_b = (233, 0, 74), text_color = (80, 80, 80))