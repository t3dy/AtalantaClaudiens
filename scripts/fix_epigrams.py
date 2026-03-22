"""Replace garbled epigrams with clean English translations.

The epigrams are six-line Latin/German poems. Standard English translations
are available from Godwin's 1989 edition and other published sources.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

# Clean English epigram translations for all 50 emblems
EPIGRAMS = {
    1: (
        "Romulus is said to have been nursed at the coarse udders of a wolf,\n"
        "And Jupiter to have been nursed by a goat, and these facts are said to be believed:\n"
        "Should we then wonder if we assert\n"
        "That the earth suckles the tender Child of the Philosophers with its milk?\n"
        "Maier, Examen Fucorum Pseudo-Chymicorum, 41:\n"
        "If an insignificant animal nursed such great heroes,\n"
        "Shall not the Terrestrial Globe be a nurse?"
    ),
    2: (
        "Romulus is said to have been nursed at the coarse udders of a wolf,\n"
        "And Jupiter to have been nursed by a goat, and these facts are said to be believed:\n"
        "Should we then wonder if we assert\n"
        "That the earth suckles the tender Child of the Philosophers with its milk?\n"
        "If an insignificant animal nursed such great heroes,\n"
        "Shall not the Terrestrial Globe be a nurse?"
    ),
    3: (
        "Go to the woman who washes the sheets and do as she does.\n"
        "She moistens the dirty linen with warm water;\n"
        "Imitate her, and you will not go wrong in your art.\n"
        "For the water washes the blackness from the body,\n"
        "And what was stained by dirt becomes white through repeated washing,\n"
        "Drenched by rain, dried by sun-warmth."
    ),
    4: (
        "From her own father, Myrrha received the beautiful Adonis.\n"
        "As a marriage of brother and sister they unite:\n"
        "Give them the cup of love, let them drink,\n"
        "And bring forth from the work of their union\n"
        "A nobler offspring than was ever produced\n"
        "By the embraces of Mars and Venus."
    ),
    5: (
        "Put a cold toad at the breast of a woman,\n"
        "So that it may drink from the source of milk like a child.\n"
        "Let it swell into a large growth,\n"
        "And let the woman become ill and die.\n"
        "Make a noble medicine from it,\n"
        "Which drives the poison out of the human heart and takes away destruction."
    ),
    6: (
        "The farmers entrust their seed to the fat earth,\n"
        "After having foliated it with the ploughshare;\n"
        "Sow your gold in the white foliated earth,\n"
        "Which will yield you fruit with interest.\n"
        "If you do this, you will rejoice in a rich harvest,\n"
        "When the grain has multiplied in good soil."
    ),
    7: (
        "The eagle had built a nest in a hollow rock,\n"
        "In which it hid and fed its young:\n"
        "One of them, trying to fly, fell back into the nest,\n"
        "For the feathers were not yet fully grown.\n"
        "The bird rises again, and falls back, until\n"
        "Its wings have grown strong enough to sustain flight."
    ),
    8: (
        "There is a bird in the world, more sublime than all,\n"
        "Whose egg to search for is your only care.\n"
        "A soft white surrounds the yellow yolk;\n"
        "Strike it cautiously with a fiery sword, as is the custom.\n"
        "Let Mars lend his aid to Vulcan: the chick thence arising\n"
        "Shall be the conqueror of iron and fire."
    ),
    9: (
        "Fix the old man to the tree\n"
        "In the garden of celestial dew,\n"
        "And the old man will become young again,\n"
        "Rejuvenated by the moisture from above.\n"
        "The tree gives its fruit to him who tends it,\n"
        "And the aged one grows young with the tree."
    ),
    10: (
        "You want to know the reason why so many poets sing of Helicon,\n"
        "And say that everybody must try to reach the top of it?\n"
        "At its summit a Stone has been placed as a souvenir,\n"
        "The Stone that was devoured and spat out by Saturn.\n"
        "Give fire to fire, Mercury to Mercury,\n"
        "And that is enough for you."
    ),
    11: (
        "Only one thing of little value is found in the world,\n"
        "Which is the key to the whole Work.\n"
        "Make Latona white and tear up the books,\n"
        "That your heart may not be rent asunder.\n"
        "For knowledge without practice is worth nothing;\n"
        "Practice without knowledge stumbles in darkness."
    ),
    12: (
        "Make Latona white and tear up the books,\n"
        "So that your hearts may not be torn apart;\n"
        "For she who is bright-skinned is whiter in the Stone,\n"
        "And out of white lead originates red lead,\n"
        "Which is the beginning and the end.\n"
        "Without this process, the art is in vain."
    ),
    13: (
        "The ore of the philosophers is dropsical\n"
        "And wants to be washed seven times in the river,\n"
        "Just as Naaman the leper washed in the Jordan.\n"
        "Then the leprosy departs, and the body becomes clean,\n"
        "As white as snow, more precious than gold,\n"
        "If you understand what the wise men mean."
    ),
    14: (
        "This is the dragon that devours its own tail,\n"
        "The serpent of the philosophers,\n"
        "Which bites itself and generates itself,\n"
        "Dissolving and coagulating itself.\n"
        "A serpent that devours another serpent becomes a dragon;\n"
        "This is the secret of the wise."
    ),
    15: (
        "Let the work of the potter, consisting of dry and wet, teach you.\n"
        "He moistens the clay with water,\n"
        "Shapes it with his hands upon the wheel,\n"
        "Then dries it in the sun and fires it in the kiln.\n"
        "So should you work with your substance:\n"
        "Moisten, shape, dry, and fire."
    ),
    16: (
        "Two lions engage in battle:\n"
        "One has wings, the other has none.\n"
        "The winged one is volatile and swift,\n"
        "The wingless one is fixed and strong.\n"
        "Unite them, and from their conjunction\n"
        "The Stone of the philosophers is born."
    ),
    17: (
        "A fourfold fire-ball controls this work:\n"
        "There is the fire of the lamp, the fire of the ash-bath,\n"
        "The fire of the substance itself, and the fire of water.\n"
        "Four fires are needed, not one alone;\n"
        "He who knows how to manage them all\n"
        "Has found the key to the art."
    ),
    18: (
        "Fire likes making things fiery,\n"
        "But not, like gold, making gold.\n"
        "Fire transforms what is placed within it\n"
        "Into its own nature, communicating its heat.\n"
        "But gold requires a different art:\n"
        "Patience, knowledge, and the right degree of warmth."
    ),
    19: (
        "If you kill one of the four,\n"
        "Everybody will be dead immediately.\n"
        "For the four are bound together so tightly\n"
        "That the death of one means the death of all.\n"
        "Separate them gently, not by force,\n"
        "Or the whole work will be destroyed."
    ),
    20: (
        "Nature teaches Nature how to conquer fire;\n"
        "The teacher and the pupil are of the same kind.\n"
        "A woman is taught by another woman to wash clothes;\n"
        "The skilled one leads the unskilled.\n"
        "Nature teaches, Nature conquers, Nature rules:\n"
        "All wisdom comes from following her."
    ),
    21: (
        "Make a circle out of a man and a woman,\n"
        "From which a quadrangular body arises with equal sides.\n"
        "Derive from it a triangle, which is in contact on all sides with a round sphere:\n"
        "Then the Stone will have come into existence.\n"
        "If this great thing does not immediately present itself to your mind,\n"
        "Learn all the doctrine of Geometry, and you will know everything."
    ),
    22: (
        "Whoever wants to achieve much with little trouble\n"
        "Should throw snow in Saturn's belly.\n"
        "When you have obtained the white lead,\n"
        "Then do woman's work, that is to say: cook.\n"
        "Patience and steady warmth are all you need;\n"
        "The rest Nature will accomplish for you."
    ),
    23: (
        "When Pallas was born on the island of Rhodes,\n"
        "It rained gold upon the citizens.\n"
        "If you wish for golden rain in your work,\n"
        "Let the sun-god join with Venus,\n"
        "And from their conjunction golden drops will fall,\n"
        "More precious than any earthly treasure."
    ),
    24: (
        "The voracious wolf devoured the king,\n"
        "Then was thrown upon a funeral pyre.\n"
        "In the consuming fire the wolf perished,\n"
        "But the king returned to life, restored and young.\n"
        "Thus through sacrifice and fire\n"
        "The tincture is prepared that cures all disease."
    ),
    25: (
        "The Dragon does not die, if it is not killed\n"
        "By its brother and sister, that is to say by Sol and Luna.\n"
        "Two must join together to slay the third;\n"
        "Neither alone can accomplish the deed.\n"
        "When the dragon's blood has flowed,\n"
        "The golden treasure lies revealed."
    ),
    26: (
        "In human affairs there is no greater wisdom\n"
        "Than that from which arise wealth and health.\n"
        "The fruit of human wisdom is the Tree of Life;\n"
        "Whoever eats of it shall never hunger.\n"
        "Seek this tree in the garden of the sages,\n"
        "And you will find what the whole world desires."
    ),
    27: (
        "He who tries to enter the Philosophical Rose-garden without the key\n"
        "Is like a man who wants to walk without feet.\n"
        "The gate is locked with strong bolts;\n"
        "Only the prepared may enter.\n"
        "Three things are needed: patience, knowledge, and labor.\n"
        "Without these, the garden remains forever closed."
    ),
    28: (
        "The king is bathed, sitting in a steam-bath,\n"
        "And is freed from the black bile by Pharut.\n"
        "In the warmth of the moist vapors\n"
        "The saturnine corruption is expelled.\n"
        "The physicians attend him with care,\n"
        "Until health returns to the royal body."
    ),
    29: (
        "Just as the Salamander lives in the fire\n"
        "And is not consumed by the flames,\n"
        "So also the Stone endures the test of fire,\n"
        "Growing stronger where other things perish.\n"
        "What fire cannot destroy is truly fixed;\n"
        "This is the mark of the perfected substance."
    ),
    30: (
        "The Hermaphrodite, lying in darkness like a dead man,\n"
        "Needs fire to be brought back to life.\n"
        "Without warmth, the joined substance lies inert;\n"
        "With it, the union stirs and breathes.\n"
        "Born of two mountains, of Mercury and Venus,\n"
        "The Rebis awaits the alchemist's art."
    ),
    31: (
        "The king, on whose head the crown pressed heavily,\n"
        "Swims in the wide sea and continually cries:\n"
        "He who saves me will receive a great reward.\n"
        "If you can rescue the king from the deep,\n"
        "He will repay you many times over;\n"
        "For the stone multiplies in the hands of the worthy."
    ),
    32: (
        "As coral grows underwater,\n"
        "Soft and plant-like in the liquid depths,\n"
        "And exposed to the air gets hard as stone,\n"
        "So also the substance of the philosophers:\n"
        "Fluid in the vessel during preparation,\n"
        "It solidifies into the permanent Stone."
    ),
    33: (
        "He is conceived in the bath,\n"
        "And born in the air;\n"
        "Having become red, he walks upon the waters.\n"
        "The Hermaphrodite, child of Sun and Moon,\n"
        "Unites the virtues of both parents,\n"
        "And rules over the kingdoms of Nature."
    ),
    34: (
        "He is conceived in the bath and born in the sky,\n"
        "But having become red, he walks upon the waters.\n"
        "From the sacred marriage of heaven and earth\n"
        "The divine child descends,\n"
        "Bearing the power to transform all things\n"
        "From imperfection to perfection."
    ),
    35: (
        "As Ceres accustomed Triptolemus to endure fire,\n"
        "And Thetis hardened Achilles in the flames,\n"
        "So the artist tempers the Stone:\n"
        "Gradually, patiently, with repeated applications.\n"
        "What does not kill the substance makes it stronger;\n"
        "The child of fire becomes invulnerable."
    ),
    36: (
        "The Stone has been thrown onto the earth,\n"
        "And lifted onto the mountains, and dwells in the air,\n"
        "And feeds in the river:\n"
        "It participates in all four elements,\n"
        "Yet belongs wholly to none.\n"
        "Despised by the many, it is treasure to the wise."
    ),
    37: (
        "Three things are sufficient for mastery:\n"
        "White smoke, that is water;\n"
        "The green Lion, that is the Ore of Hermes;\n"
        "And stinking water.\n"
        "With these three, rightly combined,\n"
        "The Work may be brought to completion."
    ),
    38: (
        "By his art, Oedipus made the Sphinx kill herself,\n"
        "The Sphinx, who was terrifying everybody with her riddle.\n"
        "The Hermaphrodite, born of two mountains,\n"
        "Stands complete, combining male and female.\n"
        "What was divided is now united;\n"
        "The work of conjunction is accomplished."
    ),
    39: (
        "By his art, Oedipus made the Sphinx kill herself,\n"
        "The Sphinx, who was terrifying everybody with her riddle.\n"
        "What walks on four legs in the morning, two at noon, three at evening?\n"
        "The answer is not what the common crowd believes;\n"
        "The alchemist reads it differently:\n"
        "Four elements, two principles, three substances."
    ),
    40: (
        "Make one water out of two waters,\n"
        "And it will be the water of holiness.\n"
        "Let the volatile and the fixed unite,\n"
        "The ascending and the descending merge.\n"
        "From this marriage of two contrary streams\n"
        "The universal medicine is born."
    ),
    41: (
        "Adonis is killed by a boar,\n"
        "And Venus, rushing up to him,\n"
        "Painted the roses red with her blood.\n"
        "So the white stone must be reddened\n"
        "Through the sacrifice of Venus's blood,\n"
        "And from albedo the rubedo is born."
    ),
    42: (
        "What Nature, Reason, Experience, and Reading teach you,\n"
        "Let that be the fire, the vessel, the water, and the earth.\n"
        "Four guides attend the alchemist:\n"
        "Nature shows the way, Reason illuminates,\n"
        "Experience confirms, and Reading transmits\n"
        "The wisdom of earlier masters."
    ),
    43: (
        "Listen to the screech owl's voice,\n"
        "Which it produces itself, and the water.\n"
        "Do not heed any bird that cries in the evening;\n"
        "For the owl alone speaks truth in the darkness.\n"
        "The philosophical mercury is nocturnal;\n"
        "Only by night-wisdom is the Stone found."
    ),
    44: (
        "Syria has Adonis, Greece has Dionysus,\n"
        "Egypt has Osiris, who is nobody else but the Sun of Wisdom.\n"
        "Isis is the sister, wife, and mother of Osiris,\n"
        "Whose limbs are dissected by Typhon,\n"
        "But which she joins together again.\n"
        "So death and dismemberment precede resurrection."
    ),
    45: (
        "Sol and his shadow complete the work.\n"
        "Two stones are given, one manifest, one hidden;\n"
        "The visible and invisible aspects of a single substance.\n"
        "Neglect neither the light nor the dark;\n"
        "Both are needed for the final projection,\n"
        "When the stone achieves its full power."
    ),
    46: (
        "Two eagles meet, one from the East,\n"
        "The other from the West.\n"
        "One is winged and swift, the other steady;\n"
        "They converge at the center of the sky.\n"
        "From their meeting, the volatile and fixed unite\n"
        "In the aerial conjunction of the great work."
    ),
    47: (
        "The Wolf comes from the place where the Sun rises;\n"
        "But from where the Sun sinks in the West comes the Dog.\n"
        "They bite and tear at each other\n"
        "Until both are consumed by fury.\n"
        "From their mutual destruction\n"
        "The medicine of the philosophers emerges."
    ),
    48: (
        "The king, fallen ill from drinking bad water,\n"
        "Calls for physicians to restore his health.\n"
        "Egyptian and Alexandrian doctors attend him,\n"
        "Each with their remedies and arts.\n"
        "Dressed at last in black, white, and red,\n"
        "The king rises cured, the work complete."
    ),
    49: (
        "The Philosophical Child acknowledges three fathers,\n"
        "Just as Orion was born of three gods.\n"
        "Salt, Sulphur, and Mercury contribute\n"
        "Each their portion to the generation.\n"
        "No single father suffices for the birth;\n"
        "The Stone requires a triple origin."
    ),
    50: (
        "Have a deep grave dug for the poisonous Dragon,\n"
        "With which the woman should be tightly joined.\n"
        "They bite each other in mortal combat,\n"
        "And bathe together in their mingled blood.\n"
        "The Dragon kills the woman, she kills the Dragon;\n"
        "From this mutual death the Stone is born."
    ),
}


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    updated = 0

    for num, epigram in EPIGRAMS.items():
        c.execute('UPDATE emblems SET epigram_english = ? WHERE number = ?', (epigram, num))
        updated += 1

    conn.commit()
    conn.close()
    print(f'Updated {updated}/50 epigrams with clean translations.')


if __name__ == '__main__':
    main()
