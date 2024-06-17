import requests
import numpy as np
import time


class Printer:
    def __init__(self, base_url="http://3dcm.lan:7125"):
        self.base_url = base_url
        self._session = requests.session()

    def send_gcode(self, gcode, wait_move=False):
        self._session.post(
            self.base_url + '/printer/gcode/script', {"script": gcode})
        if wait_move:
            self.wait_move()

    def move_to(self, x, y, z, relative=False, wait_move=True):
        self.send_gcode(f"""{'G91' if relative else 'G90'}
            G0 X{x} Y{y} Z{z} F600
            G90""", wait_move)

    def wait_move(self):
        time.sleep(.5)  # lookahead hack :(

        def check_move():
            r = self._session.get(
                self.base_url + "/printer/objects/query?gcode_move&motion_report&idle_timeout")
            status = r.json()["result"]["status"]
            motion_report = status["motion_report"]
            gcode_move = status["gcode_move"]
            idle_timeout = status["idle_timeout"]

            gcode_position = gcode_move["gcode_position"]
            position = gcode_move["position"]
            live_velocity = motion_report["live_velocity"]

            if position[0] == gcode_position[0] and position[1] == gcode_position[1] and position[2] == gcode_position[
                2] and np.isclose(live_velocity, 0.0, rtol=1e-05, atol=1e-08, equal_nan=False) and idle_timeout[
                "state"] != "Printing":
                return True

        while not check_move():
            pass

    def get_motion_report(self):
        r = self._session.get(
            self.base_url + "/printer/objects/query?motion_report")
        return r.json()["result"]["status"]["motion_report"]

    def get_position(self):
        pos = self.get_motion_report()['live_position']
        return {"x": pos[0], "y": pos[1], "z": pos[2]}
