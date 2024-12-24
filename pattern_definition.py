from patterns.blue_to_white import blue_to_white
from patterns.candy_cane import candy_cane
from patterns.carnival import carnival
from patterns.chrimbus import chrimbus
from patterns.constipated import constipated
from patterns.dvd_bounce import dvd_bounce
from patterns.linear_gradient import linear_gradient
from patterns.magi_searching_for_a_king import magi_searching_for_a_king
from patterns.pinwheel import pinwheel
from patterns.radial_gradient import radial_gradient
from patterns.rainbow import rainbow
from patterns.random_p import random_p
from patterns.red_to_white import red_to_white
from patterns.rg_chase import rg_chase
from patterns.rg_matrix import rg_matrix
from patterns.skewed_wave import skewed_wave
from patterns.twinkly_snow import twinkly_snow
from patterns.video_patterns import b_video_pattern, up_video_pattern

PATTERNS = {
    "magi_searching_for_a_king": magi_searching_for_a_king,
    "skewed_wave": skewed_wave,
    "red_to_white": red_to_white,
    "blue_to_white": blue_to_white,
    "linear_gradient": linear_gradient,
    "radial_gradient": radial_gradient,
    "pinwheel": pinwheel,
    "rg_matrix": rg_matrix,
    # "mono_rainbow": mono_rainbow,
    "rainbow": rainbow,
    "carnival": carnival,
    "chrimbus": chrimbus,
    "candy_cane": candy_cane,
    "random_p": random_p,
    "twinkly_snow": twinkly_snow,
    "rg_chase": rg_chase,
    "constipated": constipated,
    "b_video": b_video_pattern,
    "up_video": up_video_pattern,
    "dvd_bounce": dvd_bounce,
}
