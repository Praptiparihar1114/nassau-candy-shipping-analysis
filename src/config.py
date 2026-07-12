# factory locations pulled from the project brief
FACTORY_COORDS = {
    "Lot's O' Nuts":     (32.881893, -111.768036),
    "Wicked Choccy's":   (32.076176, -81.088371),
    "Sugar Shack":       (48.11914,  -96.18115),
    "Secret Factory":    (41.446333, -90.565487),
    "The Other Factory": (35.1175,   -89.971107),
}

# which factory makes which product
PRODUCT_TO_FACTORY = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory",
}

PRODUCT_TO_DIVISION = {
    "Wonka Bar - Nutty Crunch Surprise": "Chocolate",
    "Wonka Bar - Fudge Mallows": "Chocolate",
    "Wonka Bar -Scrumdiddlyumptious": "Chocolate",
    "Wonka Bar - Milk Chocolate": "Chocolate",
    "Wonka Bar - Triple Dazzle Caramel": "Chocolate",
    "Laffy Taffy": "Sugar",
    "SweeTARTS": "Sugar",
    "Nerds": "Sugar",
    "Fun Dip": "Sugar",
    "Fizzy Lifting Drinks": "Other",
    "Everlasting Gobstopper": "Sugar",
    "Hair Toffee": "Sugar",
    "Lickable Wallpaper": "Other",
    "Wonka Gum": "Other",
    "Kazookles": "Other",
}

DELAY_THRESHOLD_DAYS = 5

# raw Ship Date column is broken - Order Date is 2024/25 but Ship Date
# jumps to 2026-2030, and Same Day shipping shows the same ~1300 day
# "lead time" as Standard Class. can't be real. using simulated lead
# times per ship mode instead (see lead_time_simulation.py), seeded
# so it's reproducible
SIMULATED_LEAD_TIME_RANGES = {
    "Same Day":       (0, 1),
    "First Class":    (1, 3),
    "Second Class":   (2, 5),
    "Standard Class": (3, 7),
}
RANDOM_SEED = 42
