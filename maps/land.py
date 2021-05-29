import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/land.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (255, 255, 255), progress_bg = (200, 200, 200), p_fg_a = (18, 179, 200), p_fg_b = (136, 247, 248), text_color = (0, 0, 0))