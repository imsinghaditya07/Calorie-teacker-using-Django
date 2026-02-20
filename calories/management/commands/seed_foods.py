from django.core.management.base import BaseCommand
from calories.models import FoodItem

# ─────────────────────────────────────────────────────────────────────────────
# (name, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, category)
# All values are per 100g of the food as typically served/described.
# ─────────────────────────────────────────────────────────────────────────────
FOODS = [
    # ── INDIAN BREADS ────────────────────────────────────────────────────────
    ("Roti / Chapati (plain)",        297, 10.0, 53.0,  6.0, 4.0, "grains"),
    ("Phulka (thin roti)",            271,  9.0, 50.0,  4.5, 3.8, "grains"),
    ("Paratha (plain)",               340,  8.0, 50.0, 12.0, 3.5, "grains"),
    ("Aloo Paratha",                  300,  7.0, 47.0, 10.0, 3.2, "grains"),
    ("Paneer Paratha",                320,  9.5, 45.0, 12.0, 3.0, "grains"),
    ("Puri",                          370,  7.5, 48.0, 17.0, 2.5, "grains"),
    ("Bhatura",                       400,  8.5, 55.0, 17.0, 2.0, "grains"),
    ("Naan (plain)",                  310, 10.0, 50.0,  8.0, 2.1, "grains"),
    ("Butter Naan",                   360, 10.0, 50.0, 13.0, 2.0, "grains"),
    ("Garlic Naan",                   320, 10.0, 51.0,  9.0, 2.0, "grains"),
    ("Tandoori Roti",                 265,  9.5, 49.0,  4.0, 3.5, "grains"),
    ("Missi Roti",                    280, 11.0, 48.0,  5.5, 5.0, "grains"),
    ("Makki ki Roti",                 260,  6.0, 53.0,  4.0, 6.0, "grains"),

    # ── INDIAN RICE DISHES ───────────────────────────────────────────────────
    ("Basmati Rice (cooked)",         130,  2.7, 28.0,  0.3, 0.4, "grains"),
    ("White Rice (cooked)",           130,  2.7, 28.6,  0.3, 0.4, "grains"),
    ("Brown Rice (cooked)",           111,  2.6, 23.0,  0.9, 1.8, "grains"),
    ("Jeera Rice",                    145,  3.0, 29.5,  2.5, 0.5, "grains"),
    ("Biryani (Chicken)",             200, 12.0, 25.0,  6.0, 1.0, "grains"),
    ("Biryani (Mutton)",              215, 13.5, 24.0,  7.5, 1.0, "grains"),
    ("Biryani (Veg)",                 160,  5.0, 28.0,  3.5, 2.0, "grains"),
    ("Pulao (Vegetable)",             150,  4.0, 27.0,  3.0, 1.5, "grains"),
    ("Khichdi",                       110,  5.5, 20.0,  1.5, 2.5, "grains"),
    ("Pongal",                        130,  4.0, 22.0,  3.5, 1.0, "grains"),
    ("Curd Rice",                     130,  4.5, 21.0,  3.5, 0.5, "grains"),
    ("Lemon Rice",                    150,  3.5, 28.0,  3.0, 1.0, "grains"),
    ("Fried Rice (Veg)",              180,  4.5, 31.0,  4.5, 1.5, "grains"),

    # ── INDIAN DALS & LEGUMES ────────────────────────────────────────────────
    ("Dal Tadka (cooked)",            105,  6.5, 14.0,  2.5, 3.5, "legumes"),
    ("Dal Makhani",                   140,  7.0, 14.0,  6.0, 4.0, "legumes"),
    ("Moong Dal (cooked)",             97,  7.0, 16.0,  0.4, 2.5, "legumes"),
    ("Masoor Dal (Red Lentils, cooked)",116, 9.0, 20.1, 0.4, 7.9, "legumes"),
    ("Chana Dal (cooked)",            164,  8.9, 27.4,  2.6, 7.6, "legumes"),
    ("Toor / Arhar Dal (cooked)",     118,  7.2, 21.0,  0.5, 3.8, "legumes"),
    ("Urad Dal (cooked)",             105,  7.5, 18.0,  0.5, 3.8, "legumes"),
    ("Rajma Curry (cooked)",          130,  7.8, 19.0,  3.5, 5.0, "legumes"),
    ("Chole / Chana Masala",          155,  8.5, 21.0,  4.5, 7.0, "legumes"),
    ("Kadala Curry",                  160,  8.0, 22.0,  5.0, 6.0, "legumes"),
    ("Sambhar",                        55,  3.5,  8.0,  1.0, 2.5, "legumes"),
    ("Panchmel Dal",                  120,  7.5, 18.0,  2.5, 4.5, "legumes"),

    # ── INDIAN PANEER & DAIRY ────────────────────────────────────────────────
    ("Paneer (fresh)",                265, 18.3,  1.2, 20.8, 0.0, "dairy"),
    ("Paneer Butter Masala",          175, 10.0,  8.0, 12.0, 1.5, "dairy"),
    ("Palak Paneer",                  150, 10.0,  6.0, 10.0, 2.5, "dairy"),
    ("Shahi Paneer",                  195, 10.5,  9.0, 14.0, 1.2, "dairy"),
    ("Kadai Paneer",                  165, 10.0,  7.0, 11.5, 1.5, "dairy"),
    ("Matar Paneer",                  145,  9.5, 10.0,  8.5, 2.5, "dairy"),
    ("Paneer Bhurji",                 220, 13.0,  5.0, 16.0, 1.5, "dairy"),
    ("Dahi / Curd (plain)",            98,  3.5, 11.0,  4.5, 0.0, "dairy"),
    ("Lassi (plain, full fat)",       120,  5.0, 14.0,  5.5, 0.0, "dairy"),
    ("Lassi (salted)",                 65,  3.5,  5.0,  3.5, 0.0, "dairy"),
    ("Chaas / Buttermilk",             40,  3.0,  5.0,  1.5, 0.0, "dairy"),
    ("Raita",                          74,  3.5,  7.5,  3.5, 0.5, "dairy"),
    ("Khoya / Mawa",                  421, 21.0, 26.0, 31.0, 0.0, "dairy"),

    # ── INDIAN CHICKEN DISHES ───────────────────────────────────────────────
    ("Butter Chicken (Murgh Makhani)", 150, 14.0,  6.0,  8.5, 1.0, "protein"),
    ("Chicken Tikka Masala",           155, 15.0,  9.0,  7.0, 1.5, "protein"),
    ("Chicken Tikka",                  164, 26.0,  2.5,  5.5, 0.5, "protein"),
    ("Tandoori Chicken",               151, 24.0,  1.5,  5.5, 0.5, "protein"),
    ("Chicken Curry",                  145, 17.0,  5.0,  7.0, 1.0, "protein"),
    ("Chicken Korma",                  185, 16.0,  6.0, 11.0, 1.0, "protein"),
    ("Chicken 65",                     290, 22.0,  8.0, 19.0, 1.0, "protein"),
    ("Kadai Chicken",                  160, 18.0,  5.5,  8.0, 1.5, "protein"),
    ("Achari Chicken",                 155, 17.0,  5.0,  8.0, 1.2, "protein"),

    # ── INDIAN MUTTON / LAMB ─────────────────────────────────────────────────
    ("Mutton Curry",                   195, 20.0,  4.0, 11.0, 0.5, "protein"),
    ("Mutton Rogan Josh",              200, 20.0,  5.0, 12.0, 1.0, "protein"),
    ("Keema (Minced Mutton)",          215, 22.0,  5.0, 12.0, 0.5, "protein"),
    ("Nihari",                         180, 18.0,  5.0, 10.0, 0.5, "protein"),
    ("Haleem",                         165, 13.0, 12.0,  7.0, 2.5, "protein"),

    # ── INDIAN EGGS / SEAFOOD ────────────────────────────────────────────────
    ("Egg Curry",                      160, 12.0,  5.0, 11.0, 0.8, "protein"),
    ("Prawn / Shrimp Masala",          120, 17.0,  5.0,  4.0, 1.0, "protein"),
    ("Fish Curry",                     130, 16.0,  5.0,  5.5, 0.5, "protein"),
    ("Fried Fish",                     250, 21.0,  6.0, 16.0, 0.5, "protein"),

    # ── INDIAN VEGETABLE CURRIES ─────────────────────────────────────────────
    ("Aloo Gobi (Potato & Cauliflower)",100, 3.0, 14.0,  4.0, 3.0, "vegetables"),
    ("Aloo Matar (Potato & Peas)",     110,  3.5, 16.5,  4.0, 3.0, "vegetables"),
    ("Baingan Bharta (Smoked Eggplant)",80, 2.5, 10.0, 3.5, 3.5, "vegetables"),
    ("Bhindi Masala (Lady's Finger)",   80,  3.0,  9.0,  3.5, 2.5, "vegetables"),
    ("Palak (Spinach) Curry",           80,  4.5,  7.0,  4.0, 3.5, "vegetables"),
    ("Methi (Fenugreek) Sabzi",         95,  4.5,  8.0,  4.5, 4.0, "vegetables"),
    ("Lauki (Bottle Gourd) Curry",      50,  1.5,  8.0,  1.5, 2.5, "vegetables"),
    ("Karela (Bitter Gourd) Sabzi",     75,  2.5,  8.0,  3.5, 3.0, "vegetables"),
    ("Tinda (Round Gourd) Sabzi",       55,  1.5,  8.5,  1.5, 2.0, "vegetables"),
    ("Parwal (Pointed Gourd) Sabzi",    60,  2.0,  9.0,  1.5, 2.5, "vegetables"),
    ("Arbi / Colocasia Curry",         100,  2.5, 19.0,  1.5, 3.0, "vegetables"),
    ("Gajar Matar (Carrot & Peas)",     90,  3.0, 13.0,  3.0, 3.5, "vegetables"),
    ("Mixed Veg Curry",                 95,  3.5, 11.0,  4.0, 3.0, "vegetables"),
    ("Sarson ka Saag",                 110,  5.0,  9.0,  6.0, 5.0, "vegetables"),
    ("Undhiyu",                        145,  5.0, 18.0,  6.0, 4.5, "vegetables"),
    ("Avial",                          120,  3.5, 12.0,  6.5, 4.0, "vegetables"),
    ("Kootu (South Indian Veg)",        90,  4.0, 12.0,  3.0, 4.0, "vegetables"),

    # ── INDIAN RAW VEGETABLES ──────────────────────────────────────────────
    ("Brinjal / Eggplant (raw)",        25,  1.0,  5.9,  0.2, 3.0, "vegetables"),
    ("Lady's Finger / Okra (raw)",      33,  1.9,  7.5,  0.2, 3.2, "vegetables"),
    ("Bitter Gourd (raw)",              17,  1.0,  3.7,  0.2, 2.8, "vegetables"),
    ("Bottle Gourd (raw)",              14,  0.6,  3.4,  0.0, 0.5, "vegetables"),
    ("Ridge Gourd (raw)",               20,  1.2,  4.0,  0.1, 0.6, "vegetables"),
    ("Cluster Beans / Guvar (raw)",     26,  1.8,  5.8,  0.2, 3.0, "vegetables"),
    ("Fenugreek Leaves / Methi",        49,  4.4,  6.0,  0.9, 2.7, "vegetables"),
    ("Drumstick / Moringa (raw)",       37,  2.1,  8.5,  0.2, 3.2, "vegetables"),
    ("Raw Banana (Plantain)",           89,  1.3, 23.0,  0.3, 2.3, "vegetables"),
    ("Lotus Root (raw)",                74,  2.6, 17.2,  0.1, 4.9, "vegetables"),
    ("Colocasia / Taro (raw)",         112,  1.5, 26.5,  0.2, 4.1, "vegetables"),
    ("Yam (raw)",                      118,  1.5, 27.9,  0.2, 4.1, "vegetables"),
    ("Green Banana (Kachche Kele)",     89,  1.3, 23.0,  0.3, 2.3, "vegetables"),
    ("Raw Jackfruit (Kathal)",          51,  1.7, 11.8,  0.3, 1.5, "vegetables"),
    ("Sweet Corn (raw)",                96,  3.4, 21.0,  1.5, 2.4, "vegetables"),
    ("Suran / Elephant Yam",           79,  1.5, 18.4,  0.1, 3.0, "vegetables"),

    # ── SOUTH INDIAN FOODS ───────────────────────────────────────────────────
    ("Idli",                            39,  2.0,  8.0,  0.2, 0.5, "grains"),
    ("Dosa (plain)",                   163,  4.0, 29.0,  4.0, 0.5, "grains"),
    ("Masala Dosa",                    175,  4.5, 29.0,  5.0, 1.5, "grains"),
    ("Uttapam",                        145,  4.5, 24.0,  3.5, 1.5, "grains"),
    ("Medu Vada",                      251,  8.5, 27.0, 12.5, 1.5, "snacks"),
    ("Rava Upma",                      150,  4.0, 25.0,  4.5, 1.5, "grains"),
    ("Pesarattu",                      150,  8.0, 22.0,  3.0, 2.0, "grains"),
    ("Puttu",                          121,  2.5, 26.0,  0.5, 1.5, "grains"),
    ("Appam",                          130,  2.5, 26.5,  1.5, 0.5, "grains"),
    ("Rava Dosa",                      165,  4.0, 27.0,  5.0, 0.5, "grains"),
    ("Rasam",                           25,  1.5,  5.0,  0.5, 1.0, "vegetables"),
    ("Kozhukattai",                    155,  3.5, 32.0,  2.0, 1.0, "grains"),

    # ── INDIAN SNACKS & STREET FOOD ──────────────────────────────────────────
    ("Samosa (veg, fried)",            308,  5.5, 35.0, 16.0, 3.0, "snacks"),
    ("Kachori",                        410,  8.5, 45.0, 22.0, 3.5, "snacks"),
    ("Pakora / Bhajiya",               285,  6.5, 30.0, 16.0, 3.0, "snacks"),
    ("Onion Bhaji",                    280,  6.0, 28.0, 16.5, 3.0, "snacks"),
    ("Pav Bhaji",                      180,  5.0, 25.0,  7.0, 4.0, "snacks"),
    ("Vada Pav",                       295,  7.0, 40.0, 12.0, 3.0, "snacks"),
    ("Sev Puri",                       290,  6.0, 38.0, 13.0, 3.5, "snacks"),
    ("Pani Puri / Gol Gappa",          175,  4.0, 30.0,  5.0, 2.0, "snacks"),
    ("Papdi Chaat",                    280,  7.0, 38.0, 11.0, 3.0, "snacks"),
    ("Bhel Puri",                      175,  4.5, 29.0,  5.0, 3.0, "snacks"),
    ("Dahi Puri",                      215,  6.0, 32.0,  7.0, 2.0, "snacks"),
    ("Aloo Tikki",                     205,  4.5, 28.0,  9.0, 3.0, "snacks"),
    ("Raj Kachori",                    335,  8.0, 44.0, 14.0, 4.0, "snacks"),
    ("Dabeli",                         280,  6.0, 40.0, 10.0, 3.0, "snacks"),
    ("Puffed Rice / Murmura",          402, 10.0, 89.0,  3.5, 3.0, "snacks"),
    ("Mathri",                         490,  9.0, 55.0, 27.0, 2.0, "snacks"),
    ("Chakli",                         465,  8.5, 60.0, 22.0, 3.0, "snacks"),

    # ── INDIAN SWEETS & DESSERTS ─────────────────────────────────────────────
    ("Gulab Jamun",                    385,  5.5, 55.5, 17.0, 0.5, "snacks"),
    ("Rasgulla",                       186,  5.0, 37.5,  2.0, 0.0, "snacks"),
    ("Jalebi",                         395,  4.0, 77.0,  9.5, 0.5, "snacks"),
    ("Barfi (Milk Barfi)",             360, 10.0, 53.0, 12.5, 0.0, "snacks"),
    ("Besan Ladoo",                    435, 10.5, 55.0, 20.0, 3.5, "snacks"),
    ("Motichoor Ladoo",                415,  7.5, 62.5, 16.5, 1.5, "snacks"),
    ("Kheer / Rice Pudding",           110,  4.0, 18.5,  2.5, 0.0, "snacks"),
    ("Gajar Halwa (Carrot Halwa)",     205,  4.5, 30.0,  8.0, 2.5, "snacks"),
    ("Sooji Halwa",                    310,  5.0, 47.0, 12.0, 1.5, "snacks"),
    ("Sandesh",                        280, 14.0, 33.0, 10.0, 0.0, "snacks"),
    ("Rasmalai",                       185,  6.5, 26.0,  6.5, 0.0, "snacks"),
    ("Mysore Pak",                     530, 10.0, 58.0, 30.0, 2.0, "snacks"),
    ("Peda",                           355,  9.5, 57.0, 10.5, 0.0, "snacks"),
    ("Kulfi",                          170,  4.5, 23.0,  7.5, 0.0, "snacks"),

    # ── INDIAN BEVERAGES ─────────────────────────────────────────────────────
    ("Masala Chai (with milk & sugar)", 55,  2.0,  8.0,  1.5, 0.0, "beverages"),
    ("Masala Chai (without sugar)",     35,  2.0,  3.5,  1.5, 0.0, "beverages"),
    ("Mango Lassi",                    110,  3.5, 19.0,  2.5, 0.5, "beverages"),
    ("Rose Sharbat",                    80,  0.2, 19.5,  0.0, 0.0, "beverages"),
    ("Aam Panna",                       55,  0.3, 14.0,  0.0, 0.5, "beverages"),
    ("Thandai",                        145,  4.5, 22.0,  5.0, 1.0, "beverages"),
    ("Filter Coffee (with milk)",       45,  1.5,  6.0,  1.5, 0.0, "beverages"),

    # ── COMMON VEGETABLES ────────────────────────────────────────────────────
    ("Broccoli",            34,  2.8,  6.6,  0.4, 2.6, "vegetables"),
    ("Spinach",             23,  2.9,  3.6,  0.4, 2.2, "vegetables"),
    ("Carrot",              41,  0.9,  9.6,  0.2, 2.8, "vegetables"),
    ("Tomato",              18,  0.9,  3.9,  0.2, 1.2, "vegetables"),
    ("Cucumber",            16,  0.7,  3.6,  0.1, 0.5, "vegetables"),
    ("Sweet Potato",        86,  1.6, 20.1,  0.1, 3.0, "vegetables"),
    ("Bell Pepper (Capsicum)",31, 1.0,  7.0,  0.3, 1.2, "vegetables"),
    ("Cauliflower",         25,  1.9,  5.0,  0.3, 2.0, "vegetables"),
    ("Onion",               40,  1.1,  9.3,  0.1, 1.7, "vegetables"),
    ("Garlic",             149,  6.4, 33.1,  0.5, 2.1, "vegetables"),
    ("Potato (raw)",        77,  2.0, 17.0,  0.1, 2.2, "vegetables"),
    ("Peas (green)",        81,  5.4, 14.5,  0.4, 5.1, "vegetables"),
    ("Asparagus",           20,  2.2,  3.9,  0.1, 2.1, "vegetables"),
    ("Kale",                49,  4.3,  8.8,  0.9, 3.6, "vegetables"),
    ("Zucchini",            17,  1.2,  3.1,  0.3, 1.0, "vegetables"),
    ("Beetroot",            43,  1.6,  9.6,  0.2, 2.8, "vegetables"),
    ("Cabbage",             25,  1.3,  5.8,  0.1, 2.5, "vegetables"),
    ("Celery",              16,  0.7,  3.0,  0.2, 1.6, "vegetables"),
    ("Mushroom (button)",   22,  3.1,  3.3,  0.3, 1.0, "vegetables"),
    ("Ginger (raw)",        80,  1.8, 18.0,  0.8, 2.0, "vegetables"),
    ("Green Chilli",        40,  2.0,  9.5,  0.2, 1.5, "vegetables"),
    ("Coriander Leaves",    23,  2.1,  3.7,  0.5, 2.8, "vegetables"),
    ("Mint Leaves",         70,  3.8, 14.9,  0.9, 8.0, "vegetables"),

    # ── COMMON FRUITS ────────────────────────────────────────────────────────
    ("Apple",               52,  0.3, 14.0,  0.2, 2.4, "fruits"),
    ("Banana",              89,  1.1, 22.8,  0.3, 2.6, "fruits"),
    ("Orange",              47,  0.9, 11.8,  0.1, 2.4, "fruits"),
    ("Mango (Alphonso)",    70,  0.5, 17.0,  0.3, 1.8, "fruits"),
    ("Mango (raw/green)",   60,  0.5, 14.8,  0.3, 1.6, "fruits"),
    ("Grapes",              69,  0.7, 18.1,  0.2, 0.9, "fruits"),
    ("Watermelon",          30,  0.6,  7.6,  0.2, 0.4, "fruits"),
    ("Strawberry",          32,  0.7,  7.7,  0.3, 2.0, "fruits"),
    ("Blueberry",           57,  0.7, 14.5,  0.3, 2.4, "fruits"),
    ("Pineapple",           50,  0.5, 13.1,  0.1, 1.4, "fruits"),
    ("Avocado",            160,  2.0,  9.0, 15.0, 6.7, "fruits"),
    ("Papaya",              43,  0.5, 11.0,  0.3, 1.7, "fruits"),
    ("Guava",               68,  2.6, 14.3,  1.0, 5.4, "fruits"),
    ("Pomegranate",         83,  1.7, 18.7,  1.2, 4.0, "fruits"),
    ("Jackfruit (ripe)",    95,  1.7, 23.2,  0.6, 1.5, "fruits"),
    ("Litchi / Lychee",     66,  0.8, 16.5,  0.4, 1.3, "fruits"),
    ("Chikoo / Sapodilla", 83,  0.4, 19.9,  1.1, 5.3, "fruits"),
    ("Kiwi",                61,  1.1, 14.7,  0.5, 3.0, "fruits"),
    ("Pear",                57,  0.4, 15.2,  0.1, 3.1, "fruits"),
    ("Peach",               39,  0.9,  9.5,  0.3, 1.5, "fruits"),
    ("Coconut (fresh)",    354,  3.3, 15.2, 33.5, 9.0, "fruits"),
    ("Amla / Indian Gooseberry", 44, 0.9, 10.2, 0.6, 4.3, "fruits"),

    # ── GRAINS & CEREALS (Global) ─────────────────────────────────────────────
    ("Oats (rolled)",      389, 17.0, 66.0,  7.0,10.6, "grains"),
    ("Whole Wheat Bread",  247,  9.0, 41.0,  3.5, 6.0, "grains"),
    ("White Bread",        265,  8.9, 49.2,  3.3, 2.7, "grains"),
    ("Pasta (cooked)",     131,  5.0, 25.2,  1.1, 1.8, "grains"),
    ("Quinoa (cooked)",    120,  4.4, 21.3,  1.9, 2.8, "grains"),
    ("Cornflakes",         357,  7.5, 84.0,  0.4, 3.8, "grains"),
    ("Suji / Semolina (raw)",360, 10.0, 73.0, 1.5, 3.0, "grains"),
    ("Besan / Chickpea Flour",387, 22.0, 58.0, 7.0, 10.0, "grains"),
    ("Millet / Bajra",     361, 11.6, 67.5,  5.0, 1.3, "grains"),
    ("Jowar / Sorghum",    349, 10.4, 72.6,  1.9, 6.7, "grains"),
    ("Ragi / Finger Millet",328, 7.3, 72.0,  1.9,11.5, "grains"),
    ("Poha / Flattened Rice",333,  6.9, 76.9,  0.8, 1.5, "grains"),
    ("Sabudana / Tapioca", 352,  0.2, 86.9,  0.0, 0.9, "grains"),

    # ── PROTEIN & MEAT (Global) ───────────────────────────────────────────────
    ("Chicken Breast (cooked)", 165, 31.0, 0.0,  3.6, 0.0, "protein"),
    ("Chicken Thigh (cooked)",  209, 26.0, 0.0, 11.0, 0.0, "protein"),
    ("Ground Beef (lean)",      215, 26.1, 0.0, 12.0, 0.0, "protein"),
    ("Salmon",                  208, 20.0, 0.0, 13.0, 0.0, "protein"),
    ("Tuna (canned in water)",  116, 25.5, 0.0,  1.0, 0.0, "protein"),
    ("Egg (whole, boiled)",     155, 13.0, 1.1, 11.0, 0.0, "protein"),
    ("Egg White",                52, 11.0, 0.7,  0.2, 0.0, "protein"),
    ("Shrimp",                   99, 24.0, 0.2,  0.3, 0.0, "protein"),
    ("Turkey Breast",            135, 30.0, 0.0,  1.0, 0.0, "protein"),
    ("Tofu (firm)",               76,  8.0, 1.9,  4.5, 0.3, "protein"),
    ("Tempeh",                   193, 18.5, 9.4, 10.8, 0.0, "protein"),
    ("Sardines (canned)",        208, 24.6, 0.0, 11.5, 0.0, "protein"),

    # ── DAIRY (Global) ────────────────────────────────────────────────────────
    ("Whole Milk",               61,  3.2,  4.8,  3.3, 0.0, "dairy"),
    ("Skimmed Milk",             34,  3.4,  4.9,  0.2, 0.0, "dairy"),
    ("Greek Yogurt (plain)",     59, 10.0,  3.6,  0.4, 0.0, "dairy"),
    ("Cheddar Cheese",          402, 25.0,  1.3, 33.0, 0.0, "dairy"),
    ("Mozzarella",              280, 18.0,  2.2, 22.0, 0.0, "dairy"),
    ("Cottage Cheese",           98, 11.0,  3.4,  4.3, 0.0, "dairy"),
    ("Butter",                  717,  0.9,  0.1, 81.0, 0.0, "dairy"),
    ("Whey Protein (unflavoured)",358,80.0,  5.0,  4.0, 0.0, "dairy"),

    # ── NUTS & SEEDS ──────────────────────────────────────────────────────────
    ("Almonds",                 579, 21.2, 21.7, 49.9,12.5, "nuts"),
    ("Cashews",                 553, 18.2, 30.2, 43.8, 3.3, "nuts"),
    ("Walnuts",                 654, 15.2, 13.7, 65.2, 6.7, "nuts"),
    ("Peanuts",                 567, 25.8, 16.1, 49.2, 8.5, "nuts"),
    ("Peanut Butter",           588, 25.1, 20.0, 50.4, 6.0, "nuts"),
    ("Chia Seeds",              486, 16.5, 42.1, 30.7,34.4, "nuts"),
    ("Flaxseeds",               534, 18.3, 28.9, 42.2,27.3, "nuts"),
    ("Sunflower Seeds",         584, 20.8, 20.0, 51.5, 8.6, "nuts"),
    ("Pumpkin Seeds",           559, 30.2, 10.7, 49.1, 6.0, "nuts"),
    ("Sesame Seeds (Til)",      573, 17.7, 23.4, 49.7,11.8, "nuts"),
    ("Pistachios",              562, 20.6, 27.2, 45.3,10.3, "nuts"),
    ("Macadamia Nuts",          718,  7.9, 13.8, 75.8, 8.6, "nuts"),
    ("Coconut (desiccated)",    660,  6.9, 23.7, 65.8,16.3, "nuts"),

    # ── LEGUMES ───────────────────────────────────────────────────────────────
    ("Chickpeas (cooked)",      164,  8.9, 27.4,  2.6, 7.6, "legumes"),
    ("Black Beans (cooked)",    132,  8.9, 23.7,  0.5, 8.7, "legumes"),
    ("Kidney Beans (cooked)",   127,  8.7, 22.8,  0.5, 6.4, "legumes"),
    ("Edamame",                 121, 11.9,  8.9,  5.2, 5.2, "legumes"),
    ("Hummus",                  177,  5.0, 14.3, 10.0, 6.0, "legumes"),
    ("Soya Chunks (dry)",       345, 52.0, 33.0,  0.5,13.0, "legumes"),
    ("Soya Chunks (cooked)",    149, 22.0, 14.0,  0.2, 5.5, "legumes"),

    # ── SNACKS & JUNK FOOD (Global) ───────────────────────────────────────────
    ("Potato Chips",            536,  7.0, 53.0, 35.0, 4.8, "snacks"),
    ("Dark Chocolate (70%)",    598,  7.8, 46.0, 42.6,10.9, "snacks"),
    ("Milk Chocolate",          535,  7.3, 59.4, 29.7, 3.4, "snacks"),
    ("Popcorn (air-popped)",    387, 12.9, 77.9,  4.5,14.5, "snacks"),
    ("Pizza (cheese)",          266, 11.4, 30.3, 10.4, 2.3, "snacks"),
    ("Burger (beef patty)",     295, 17.0, 24.0, 14.0, 1.0, "snacks"),
    ("French Fries",            312,  3.4, 41.4, 15.0, 3.8, "snacks"),
    ("Protein Bar",             350, 20.0, 40.0, 10.0, 5.0, "snacks"),
    ("Granola Bar",             471,  9.8, 64.2, 19.7, 4.1, "snacks"),
    ("Ice Cream (vanilla)",     207,  3.5, 24.0, 11.0, 0.0, "snacks"),

    # ── OILS & FATS ───────────────────────────────────────────────────────────
    ("Olive Oil",               884,  0.0,  0.0,100.0, 0.0, "oils"),
    ("Coconut Oil",             862,  0.0,  0.0,100.0, 0.0, "oils"),
    ("Mustard Oil",             884,  0.0,  0.0,100.0, 0.0, "oils"),
    ("Sunflower Oil",           884,  0.0,  0.0,100.0, 0.0, "oils"),
    ("Ghee",                    900,  0.0,  0.0,100.0, 0.0, "oils"),
    ("Mayonnaise",              680,  1.0,  0.6, 75.0, 0.0, "oils"),
    ("Cream",                   345,  2.1,  2.8, 36.0, 0.0, "oils"),

    # ── BEVERAGES ─────────────────────────────────────────────────────────────
    ("Orange Juice",             45,  0.7, 10.4,  0.2, 0.2, "beverages"),
    ("Apple Juice",              46,  0.1, 11.4,  0.1, 0.2, "beverages"),
    ("Coca-Cola",                42,  0.0, 10.6,  0.0, 0.0, "beverages"),
    ("Coffee (black)",            2,  0.3,  0.0,  0.0, 0.0, "beverages"),
    ("Latte (whole milk)",       54,  3.0,  5.0,  2.5, 0.0, "beverages"),
    ("Green Tea",                 1,  0.2,  0.0,  0.0, 0.0, "beverages"),
    ("Almond Milk (unsweetened)", 15,  0.6,  0.6,  1.0, 0.5, "beverages"),
    ("Coconut Water",             19,  0.7,  3.7,  0.2, 1.1, "beverages"),
    ("Protein Shake (with milk)",150, 20.0, 12.0,  4.0, 0.5, "beverages"),
]


class Command(BaseCommand):
    help = 'Seed the database with 300+ foods including comprehensive Indian cuisine'

    def handle(self, *args, **kwargs):
        created_count = 0
        skipped_count = 0
        for name, calories, protein, carbs, fat, fiber, category in FOODS:
            _, created = FoodItem.objects.get_or_create(
                name=name,
                defaults={
                    'calories_per_100g': calories,
                    'protein_g': protein,
                    'carbs_g': carbs,
                    'fat_g': fat,
                    'fiber_g': fiber,
                    'category': category,
                    'is_custom': False,
                }
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ Food database seeded! '
            f'{created_count} new items added, '
            f'{skipped_count} already existed. '
            f'({FoodItem.objects.count()} total foods)'
        ))
