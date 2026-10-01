from pycromanager import Core


class LaserBackend:
    def __init__(self):
        self.core = Core()

        self.green_device = "Green_Sapphire"
        self.blue_device = "Blue_Sapphire"

        self.green_min_power = 20
        self.green_max_power = 220

        self.blue_min_power = 15
        self.blue_max_power = 165

    def get_green_state(self):
        return self.core.get_property(
            self.green_device,
            "State"
        )

    def get_blue_state(self):
        return self.core.get_property(
            self.blue_device,
            "State"
        )

    def get_green_power(self):
        return float(
            self.core.get_property(
                self.green_device,
                "PowerSetpoint"
            )
        )

    def get_blue_power(self):
        return float(
            self.core.get_property(
                self.blue_device,
                "PowerSetpoint"
            )
        )

    def set_green(self, state):
        self.core.set_property(
            self.green_device,
            "State",
            state
        )

    def set_blue(self, state):
        self.core.set_property(
            self.blue_device,
            "State",
            state
        )

    def set_green_power(self, power):
        if power < self.green_min_power or power > self.green_max_power:
            print("ERROR: Green power out of range")
            print("Allowed range: 20 to 220")
            return False

        self.core.set_property(
            self.green_device,
            "PowerSetpoint",
            str(power)
        )

        actual_power = self.get_green_power()

        print("Green power requested:", power)
        print("Green power actual:   ", actual_power)

        if actual_power == float(power):
            print("GREEN_POWER_READY = TRUE")
            return True

        print("GREEN_POWER_READY = FALSE")
        return False

    def set_blue_power(self, power):
        if power < self.blue_min_power or power > self.blue_max_power:
            print("ERROR: Blue power out of range")
            print("Allowed range: 15 to 165")
            return False

        self.core.set_property(
            self.blue_device,
            "PowerSetpoint",
            str(power)
        )

        actual_power = self.get_blue_power()

        print("Blue power requested:", power)
        print("Blue power actual:    ", actual_power)

        if actual_power == float(power):
            print("BLUE_POWER_READY = TRUE")
            return True

        print("BLUE_POWER_READY = FALSE")
        return False

    def verify_state(self, expected_green, expected_blue):
        actual_green = self.get_green_state()
        actual_blue = self.get_blue_state()

        print("Green requested:", expected_green)
        print("Green actual:   ", actual_green)

        print("Blue requested: ", expected_blue)
        print("Blue actual:    ", actual_blue)

        if actual_green == expected_green and actual_blue == expected_blue:
            print("LASER_STATE_READY = TRUE")
            return True

        print("LASER_STATE_READY = FALSE")
        return False

    def set_mode(self, mode):
        mode = mode.upper()

        if mode == "GREEN_ONLY":
            self.set_blue("0")
            self.set_green("1")
            return self.verify_state("1", "0")

        elif mode == "BLUE_ONLY":
            self.set_green("0")
            self.set_blue("1")
            return self.verify_state("0", "1")

        elif mode == "ALL_ON":
            self.set_green("1")
            self.set_blue("1")
            return self.verify_state("1", "1")

        elif mode == "ALL_OFF":
            self.set_green("0")
            self.set_blue("0")
            return self.verify_state("0", "0")

        else:
            print("ERROR: Invalid laser mode")
            print("LASER_STATE_READY = FALSE")
            return False

    def get_status(self):
        green_state = self.get_green_state()
        blue_state = self.get_blue_state()

        green_power = self.get_green_power()
        blue_power = self.get_blue_power()

        status = {
            "green_state": green_state,
            "blue_state": blue_state,
            "green_power": green_power,
            "blue_power": blue_power
        }

        print()
        print("----- LASER STATUS -----")
        print("Green State:", green_state)
        print("Green Power:", green_power)
        print("Blue State: ", blue_state)
        print("Blue Power: ", blue_power)
        print("------------------------")

        return status

    def configure(self, mode, green_power, blue_power):
        print()
        print("----- LASER CONFIGURATION START -----")

        mode = mode.upper()

        valid_modes = [
            "GREEN_ONLY",
            "BLUE_ONLY",
            "ALL_ON",
            "ALL_OFF"
        ]

        if mode not in valid_modes:
            print("ERROR: Invalid laser mode")
            print("LASER_READY = FALSE")
            return False

        if green_power < self.green_min_power or green_power > self.green_max_power:
            print("ERROR: Green power out of range")
            print("LASER_READY = FALSE")
            return False

        if blue_power < self.blue_min_power or blue_power > self.blue_max_power:
            print("ERROR: Blue power out of range")
            print("LASER_READY = FALSE")
            return False

        green_power_ready = self.set_green_power(green_power)

        blue_power_ready = self.set_blue_power(blue_power)

        state_ready = self.set_mode(mode)

        if green_power_ready and blue_power_ready and state_ready:
            print()
            print("LASER_READY = TRUE")
            print("----- LASER CONFIGURATION COMPLETE -----")
            return True

        print()
        print("LASER_READY = FALSE")
        print("----- LASER CONFIGURATION FAILED -----")
        return False