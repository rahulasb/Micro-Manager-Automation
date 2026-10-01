from laser_backend import LaserBackend


laser = LaserBackend()

print()
print("Available laser modes:")
print("GREEN_ONLY")
print("BLUE_ONLY")
print("ALL_ON")
print("ALL_OFF")
print()

mode = input("Enter laser mode: ").strip().upper()

green_power = float(input("Enter Green power: "))
blue_power = float(input("Enter Blue power: "))

print()
print("Applying laser configuration...")

ready = laser.configure(
    mode=mode,
    green_power=green_power,
    blue_power=blue_power
)

print()
laser.get_status()

if ready:
    print()
    print("Laser configuration successful.")
else:
    print()
    print("Laser configuration failed.")

print()
turn_off = input("Turn all lasers OFF now? (Y/N): ").strip().upper()

if turn_off == "Y":
    laser.set_mode("ALL_OFF")
    print()
    laser.get_status()