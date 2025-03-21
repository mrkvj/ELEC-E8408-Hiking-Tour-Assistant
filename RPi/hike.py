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
'''
    def __repr__(self):
        return f"HikeSession{{{self.id}, {self.m}(m), {self.steps}(steps), {self.kcal:.2f}(kcal)}}"
'''
'''
def to_list(hs: HikeSession) -> list:
    return [hs.id, hs.m, hs.steps, hs.kcal]
'''
'''
def from_list(l: list) -> HikeSession:
    hs = HikeSession()
    hs.username = l[0]
    hs.sessionID = l[1]
    hs.start_time = l[2]
    hs.weight = l[3]
    hs.steps = l[4]
    hs.kcal = l[5]
    hs.distance = l[6]
    hs.watchID = l[7]
    return hs
    '''