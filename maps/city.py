import defaultMap

class Map(defaultMap.Map):
    def __init__(self):
        defaultMap.Map.__init__(self, image_fp="./maps/city.image" , win_size = (1200, 800), max_y = 780, min_y = 121, pop_border_padding = 15, bg = (255, 255, 255), progress_bg = (80, 80, 80), p_fg_a = (95, 80, 225), p_fg_b = (251, 28, 233), text_color = (255, 255, 255))