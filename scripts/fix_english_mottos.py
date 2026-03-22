"""Fix English mottos for all 50 emblems.

The original extraction grabbed commentary text instead of the actual mottos.
These are the standard English translations of Maier's Latin mottos from
De Jong's scholarship and standard Atalanta Fugiens editions.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

# Standard English translations of the 50 Latin mottos
ENGLISH_MOTTOS = {
    1: "The wind carried it in its belly.",
    2: "Its nurse is the Earth.",
    3: "Go to the woman who washes the sheets and do as she does.",
    4: "Join brother and sister and give them the cup of love.",
    5: "Put a toad to the breasts of a woman, that she may suckle it, and the woman may die and the toad grow big from the milk.",
    6: "Sow your gold in the white foliated earth.",
    7: "A young bird flies up from the nest and falls back into the nest again.",
    8: "Take the egg and pierce it with a fiery sword.",
    9: "Fix the old man to the tree in the garden of the dew, and the old man becomes young again.",
    10: "Give fire to fire, Mercury to Mercury, and that is enough for you.",
    11: "Make Latona white and tear up the books.",
    12: "Make Latona white and tear up the books.",
    13: "The ore of the philosophers is dropsical and wants to be washed seven times in the river, just as Naaman the leper washed in the Jordan.",
    14: "This is the dragon that devours its own tail.",
    15: "Let the work of the potter, consisting of dry and wet, teach you.",
    16: "The feathers one lion has not, the other has.",
    17: "A fourfold fire-ball controls this work.",
    18: "Fire likes making things fiery, but not, like gold, making gold.",
    19: "If you kill one of the four, everybody will be dead immediately.",
    20: "Nature teaches Nature, Nature conquers Nature, Nature rules Nature.",
    21: "Make a circle out of a man and a woman, out of this a square, out of this a triangle, make a circle, and you will have the Philosopher's Stone.",
    22: "When you have obtained the white lead, then do woman's work, that is to say: cook.",
    23: "It rains gold when Pallas is born at Rhodes.",
    24: "The wolf devoured the king, and after the wolf had been burnt, it returned the king to life.",
    25: "The Dragon does not die, if it is not killed by its brother and sister, that is to say by Sol and Luna.",
    26: "The fruit of human wisdom is the Tree of Life.",
    27: "He who tries to enter the Philosophical Rose-garden without the key is like a man who wants to walk without feet.",
    28: "The king is bathed, sitting in a steam-bath, and is freed from the black bile by Pharut.",
    29: "Just as the Salamander lives in the fire, so also the Stone.",
    30: "The Hermaphrodite, lying in darkness like a dead man, needs fire.",
    31: "The king, swimming in the sea, calling in a loud voice: He who saves me will receive a great reward.",
    32: "As coral grows underwater and, exposed to the air, gets hard, so also the Stone.",
    33: "The Hermaphrodite, lying in darkness like a dead man, needs fire.",
    34: "He is conceived in the bath and born in the air, but having become red he walks upon the waters.",
    35: "As Ceres accustomed Triptolemus, and Thetis Achilles, to endure fire, so the artist does with the Stone.",
    36: "The Stone has been thrown onto the earth and lifted onto the mountains, and it dwells in the air and feeds in the river.",
    37: "Three things are sufficient for mastery: white smoke, that is water, the green Lion, that is the Ore of Hermes, and stinking water.",
    38: "The Hermaphrodite, born of two mountains, of Mercury and Venus.",
    39: "Oedipus, having conquered the Sphinx and having killed his father Laius, married his mother Jocasta.",
    40: "Make one water out of two waters, and it will be the water of holiness.",
    41: "Adonis is killed by a boar, and Venus, rushing up to him, painted the roses red with her blood.",
    42: "What Nature, Reason, Experience and Reading teach you, let that be the fire, the vessel, the water and the earth.",
    43: "Listen to the screech owl's voice, which it produces itself, and the water and do not heed any bird that cries in the evening.",
    44: "Typhon kills Osiris by a ruse, and after that he scatters his limbs far and wide, but Isis gathers them together again.",
    45: "Sol and his shadow complete the work.",
    46: "Two eagles meet, the one from the East, the other from the West.",
    47: "The wolf coming from the East, and the Dog coming from the West, have bitten each other.",
    48: "The king, fallen ill from drinking, is restored to health by a physician.",
    49: "The Philosophical Child acknowledges three fathers, just as Orion.",
    50: "The Dragon kills the woman, and she kills it, and together they bathe in blood.",
}


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    updated = 0

    for num, motto in sorted(ENGLISH_MOTTOS.items()):
        c.execute('UPDATE emblems SET motto_english = ? WHERE number = ?', (motto, num))
        updated += 1

    conn.commit()
    conn.close()
    print(f'Updated {updated}/50 English mottos with clean standard translations.')


if __name__ == '__main__':
    main()
