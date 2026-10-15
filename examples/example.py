from huestep import HueStep

print(HueStep.rgb("Purple text", 170, 85, 255))
print(HueStep.gradient("Text with an RGB gradient"))

print(HueStep.autorgb("Connecting..."))
print(HueStep.autorgb("Loading..."))
print(HueStep.autorgb("Ready."))
