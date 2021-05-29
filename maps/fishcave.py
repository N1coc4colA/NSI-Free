import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/fishcave.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (0, 0, 0), progress_bg = (80, 80, 80), p_fg_a = (98, 29, 73), p_fg_b = (201, 12, 17), text_color = (255, 112, 116))