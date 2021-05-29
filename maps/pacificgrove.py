import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/pacificgrove.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (255, 255, 255), progress_bg = (100, 112, 141), p_fg_a = (23, 98, 31), p_fg_b = (0, 155, 153), text_color = (31, 37, 33))