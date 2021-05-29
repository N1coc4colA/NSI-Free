import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/temple.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (31, 33, 28), progress_bg = (80, 80, 80), p_fg_a = (57, 114, 72), p_fg_b = (116, 162, 143), text_color = (200, 200, 200))