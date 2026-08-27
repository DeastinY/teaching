"""
Bake a coffee ring to a PNG.

The look comes from the coffee-ring effect: as the drop evaporates, flow carries
the solute to the pinned contact line, so almost everything ends up in a narrow
band at the rim and the middle stays nearly clean.

RGB is held constant and all the variation lives in the alpha channel — that is
both physically reasonable under a multiply blend (more deposit = darker and
more saturated) and compresses far better than varying colour.
"""
from PIL import Image, ImageFilter
import math, random

S      = 760            # source size
CX = CY = S / 2.0
R0     = S * 0.415      # nominal rim radius
ELL    = 0.972          # cups are rarely set down perfectly flat
TILT   = math.radians(6)
INK    = (66, 40, 22)   # warm dark brown

random.seed(11)

# ---- periodic 1-D noise over the angle, so it wraps seamlessly ---------------
def harmonics(spec):
    return [(k, random.uniform(0, 2 * math.pi), a) for k, a in spec]

def evaluate(h, t):
    return sum(a * math.sin(k * t + p) for k, p, a in h)

# how heavy the deposit is around the circumference
DENSITY = harmonics([(1, .22), (2, .19), (3, .13), (5, .10), (8, .07), (13, .045)])
# fine crenulation of the contact line itself (shape stays essentially round)
CRENEL  = harmonics([(7, .0045), (11, .0032), (19, .0022), (31, .0014), (47, .0009)])

N = 4096
dens_lut  = [evaluate(DENSITY, i * 2 * math.pi / N) for i in range(N)]
crenl_lut = [evaluate(CRENEL,  i * 2 * math.pi / N) for i in range(N)]

# where it pooled a little longer: (angle, angular width, extra alpha)
BLOTS = [(math.radians(196), .20, .30),
         (math.radians(41),  .13, .21),
         (math.radians(300), .09, .14)]

PEAK      = 0.58        # alpha at the heart of the rim deposit
INTERIOR  = 0.021       # the wash left across the middle
TIDE_R    = 0.905       # a secondary line where the level paused
TIDE_A    = 0.052

def radial(x):
    """alpha as a function of r / rim_radius"""
    if x > 1.042:
        return 0.0
    if x > 1.0:                      # outside the contact line: sharp falloff
        return PEAK * max(0.0, 1.0 - (x - 1.0) / 0.040) ** 1.9
    if x > 0.955:                    # the deposit band — narrow, as it really is
        u = (x - 0.955) / 0.045
        return INTERIOR + (PEAK - INTERIOR) * u ** 2.6
    a = INTERIOR * (0.45 + 0.55 * x)  # faint interior wash
    d = abs(x - TIDE_R)              # plus the tide line
    if d < 0.030:
        a += TIDE_A * (1.0 - d / 0.030) ** 2
    return a

img = Image.new("RGBA", (S, S), (INK[0], INK[1], INK[2], 0))
px  = img.load()

cos_t, sin_t = math.cos(-TILT), math.sin(-TILT)
inv2pi = N / (2 * math.pi)

for y in range(S):
    dy0 = y - CY
    for x in range(S):
        dx0 = x - CX
        # un-rotate, then un-squash so the ring is elliptical on the page
        dx =  dx0 * cos_t - dy0 * sin_t
        dy = (dx0 * sin_t + dy0 * cos_t) / ELL
        r  = math.hypot(dx, dy)
        if r > R0 * 1.09:
            continue
        t  = math.atan2(dy, dx)
        i  = int((t % (2 * math.pi)) * inv2pi) & (N - 1)

        rim = R0 * (1.0 + crenl_lut[i])
        a   = radial(r / rim)
        if a <= 0.0:
            continue

        # heavier in some arcs, nearly gone in others
        a *= max(0.0, 1.0 + dens_lut[i] * 1.8)

        # pooled deposits sit on the rim
        for bt, bw, ba in BLOTS:
            d = abs((t - bt + math.pi) % (2 * math.pi) - math.pi)
            if d < bw * 2.5:
                a += ba * math.exp(-(d / bw) ** 2) * math.exp(-((r / rim - 0.985) / 0.05) ** 2)

        # paper tooth breaking the deposit up
        a *= 0.90 + 0.20 * random.random()

        if a > 0.0:
            px[x, y] = (INK[0], INK[1], INK[2], min(255, int(a * 255)))

# soften: the grain above becomes mottling rather than speckle
img = img.filter(ImageFilter.GaussianBlur(0.8))

out = "assets/images/coffee-stain.png"
img.save(out, optimize=True)
print("wrote", out, img.size)
