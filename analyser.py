

class Fmt:
    def __init__(self, delta, final_time, split_index, real_time):
        self.delta = delta
        self.final_time = final_time
        self.split_index = split_index
        self.real_time = real_time

    def reset(self) -> str:
        time_freeze = self.real_time
        if self.split_index == "-1" and self.real_time == time_freeze and self.final_time == "0.00.00":
            return "RESET"

    def pb(self) -> str:
        if self.final_time != "0.00.00":
            return self.final_time

    def delta(self):
        delta_freeze = self.delta
        if self.delta != "-":
            pass
