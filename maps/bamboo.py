import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/bamboo.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (30, 27, 34), progress_bg = (113, 113, 113), p_fg_a = (97, 176, 160), p_fg_b = (115, 161, 79), text_color = (255, 255, 255))