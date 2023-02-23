import json


class Score:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.formatTime = None
        self.start_timer = False
        self.time = 0

    def timer(self):
        if self.start_timer:
            self.time += 1 / 60
            self.formatTime = format(self.time, '.2f')

    def save_score(self):
        try:
            with open("data/score.json", "r") as file:
                data = json.load(file)

        except ValueError:
            data = {
                "Current score": 0,
                "Score": 0
            }

        data["Current score"] = self.time

        if data["Current score"] < data["Score"] or data["Score"] == 0:
            data["Score"] = data["Current score"]

        with open("data/score.json", "w") as file:
            json.dump(data, file, indent=4)

    def update(self):
        self.save_score()

    def draw(self):
        try:
            with open("data/score.json", "r") as file:
                data = json.load(file)

        except ValueError:
            data = {
                "Current score": 0,
                "Score": 0
            }

        self.text_rect = self.font.render("CURRENT TIME", True, "white")
        self.current_time_rect = self.font.render(self.formatTime, True, "white")
        self.text_time_rect = self.font.render("BEST TIME", True, "white")
        self.best_time_rect = self.font.render(format(data["Score"], '.2f'), True, "white")

        self.screen.blit(self.text_rect, (875, 90))
        self.screen.blit(self.current_time_rect, (970, 170))
        self.screen.blit(self.text_time_rect, (915, 300))
        self.screen.blit(self.best_time_rect, (970, 370))
