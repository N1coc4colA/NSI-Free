import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/marketplace.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (255, 255, 255), progress_bg = (200, 200, 200), p_fg_a = (185, 76, 120), p_fg_b = (196, 94, 61), text_color = (29, 134, 163))