MET_HIKING = 6
KCAL_PER_STEP = 0.04

class HikeSession:
    userID = 0
    username = ""
    sessionID = 0
    start_time = ""
    end_time = ""
    weight = 0.0
    steps = 0
    calories = -1
    distance = 0
    duration = 0.0
    watchID = ""
    coords = []

    # represents a computationally intensive calculation done by genious execution.
    def calc_kcal(self):
        self.calories = MET_HIKING * KCAL_PER_STEP * self.steps
    