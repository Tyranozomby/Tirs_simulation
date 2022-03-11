import json


class Settings:
    conf_file: str = "settings/conf.json"
    values: dict

    def __init__(self):
        with open(self.conf_file, 'r') as f:
            self.values = json.load(f)

    def __getitem__(self, item):
        return self.values[item]

    def update(self):
        with open(self.conf_file, "w") as f:
            json.dump(self.values, f, indent=2)

    def change_S_SIZE(self, newval: str):
        newval = int(newval)
        self.values["S_SIZE"] = newval
        self.update()

    def change_T_SIZE(self, newval: str):
        newval = int(newval)
        self.values["T_SIZE"] = newval
        self.update()

    def change_PRECISION(self, newval: str):
        newval = int(newval)
        self.values["PRECISION"] = newval
        self.update()

    def change_BOUNCES(self, newval: str):
        newval = int(newval)
        self.values["MAX_BOUNCES"] = newval
        self.update()


settings = Settings()
