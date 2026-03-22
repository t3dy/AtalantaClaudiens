"""Classify all 50 emblems by alchemical stage (NIGREDO/ALBEDO/CITRINITAS/RUBEDO).

Based on De Jong's analysis and standard Maier scholarship:
- NIGREDO: dissolution, putrefaction, death, blackening, killing, devouring
- ALBEDO: washing, whitening, purification, lunar imagery, resurrection from black
- CITRINITAS: yellowing, ripening, fire mastery, solar dawn, transition to gold
- RUBEDO: reddening, completion, philosopher's stone, king crowned, final union

Classification uses discourse content, motto symbolism, and canonical_label.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

# Scholarly classification based on De Jong's analysis of Maier's opus
# Each emblem mapped to its dominant alchemical stage
STAGE_MAP = {
    # I-V: Early opus — earth/nurturing/dissolution
    1: ('NIG', 'Earth as nurse — prima materia in dark earth'),
    2: ('NIG', 'Earth as nurse — prima materia nourishment'),
    3: ('ALB', 'Washing sheets — purification/whitening imagery'),
    4: ('NIG', 'Brother-sister conjunction — initial coniunctio in darkness'),
    5: ('NIG', 'Toad suckling — venomous putrefaction'),

    # VI-X: Sowing/growing/fire
    6: ('ALB', 'Sowing gold in white earth — albedo planting'),
    7: ('CIT', 'Bird flying and falling — volatile spirit, solar aspiration'),
    8: ('NIG', 'Egg pierced by fiery sword — dissolution of cosmic egg'),
    9: ('NIG', 'Old man in celestial dew — putrefaction and renewal'),
    10: ('CIT', 'Fire to fire, Mercury to Mercury — fire mastery'),

    # XI-XV: Whitening/washing
    11: ('ALB', 'Make Latona white — explicit albedo reference'),
    12: ('ALB', 'Tear up the books — purification through destruction of false knowledge'),
    13: ('ALB', 'Dropsical ore washed in Jordan — washing/purification'),
    14: ('NIG', 'Serpent devouring serpent becomes dragon — devouring/transformation'),
    15: ('ALB', 'Potter\'s work — forming through wet and dry (opus figuli)'),

    # XVI-XX: Fire/transformation
    16: ('CIT', 'Winged and wingless lion — volatile and fixed, solar beast'),
    17: ('CIT', 'Fourfold fire-ball — fire mastery and control'),
    18: ('CIT', 'Fire continuation — solar fire governs the work'),
    19: ('NIG', 'Kill one of four — death/dissolution of elements'),
    20: ('ALB', 'Nature teaches nature — washing/learning from nature'),

    # XXI-XXV: Geometric/philosophical/royal
    21: ('RUB', 'Circle-square-triangle — geometric perfection, completion'),
    22: ('ALB', 'White lead obtained — explicit albedo product'),
    23: ('CIT', 'Golden rain — solar gold descending, ripening'),
    24: ('NIG', 'Wolf devours king — royal death, nigredo of the king'),
    25: ('NIG', 'Dragon killed for Golden Fleece — death before attainment'),

    # XXVI-XXX: Wisdom/cooking/salamander
    26: ('RUB', 'Tree of Life / Lady Sapientia — wisdom achieved, completion'),
    27: ('CIT', 'Three cooking processes — ripening/maturation'),
    28: ('NIG', 'King in steam bath — dissolution through heat'),
    29: ('CIT', 'Salamander lives in fire — fire mastery, endurance'),
    30: ('RUB', 'Hermaphrodite / Rebis — final union of opposites'),

    # XXXI-XXXV: Growth/multiplication/stone
    31: ('RUB', 'Vegetable stone grows — multiplication, completion'),
    32: ('RUB', 'Coral grows underwater — stone solidifies, completion'),
    33: ('NIG', 'Hermaphrodite in darkness — darkness/dissolution before fire'),
    34: ('RUB', 'Celestial conception / hierogamy — sacred marriage, completion'),
    35: ('ALB', 'Philosopher\'s Stone found — sowing in white earth (albedo ref)'),

    # XXXVI-XL: Stone thrown/building/sources
    36: ('NIG', 'Stone thrown on earth — prima materia cast down'),
    37: ('CIT', 'Three things for mastery — building/construction, fire/smoke/bath'),
    38: ('RUB', 'Hermaphrodite standing — completed union of male/female'),
    39: ('ALB', 'Wonder sources/Sphinx — purification through riddling/water'),
    40: ('RUB', 'Two waters made one — final unification'),

    # XLI-XLV: Death/resurrection/two stones
    41: ('NIG', 'Adonis killed by boar — death of the beloved'),
    42: ('RUB', 'Tabula Smaragdina — Hermes\' complete work'),
    43: ('ALB', 'Naaman washed in Jordan — purification/cleansing'),
    44: ('NIG', 'Osiris killed and resurrected — death phase of resurrection cycle'),
    45: ('RUB', 'Two Stones given — dual completion'),

    # XLVI-L: Eagles/wolves/final
    46: ('CIT', 'Two eagles from East and West — solar/fire convergence'),
    47: ('NIG', 'Wolf from East, Dog from West — devouring/struggle'),
    48: ('RUB', 'King Duenech receives potion — royal restoration, completion'),
    49: ('CIT', 'Philosophical Child with three fathers — maturation/ripening'),
    50: ('NIG', 'Dragon kills woman, she kills it — mutual destruction/nigredo'),
}

STAGE_NAMES = {'NIG': 'NIGREDO', 'ALB': 'ALBEDO', 'CIT': 'CITRINITAS', 'RUB': 'RUBEDO'}


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    updated = 0
    print(f'{"#":>3} {"Roman":>7} {"Stage":>10} | Evidence')
    print('-' * 80)

    for num, (stage_code, evidence) in sorted(STAGE_MAP.items()):
        stage = STAGE_NAMES[stage_code]
        roman = c.execute('SELECT roman_numeral FROM emblems WHERE number = ?', (num,)).fetchone()
        if not roman:
            continue
        roman = roman[0]

        c.execute('UPDATE emblems SET alchemical_stage = ? WHERE number = ?', (stage, num))
        updated += 1
        print(f'{num:>3} {roman:>7} {stage:>10} | {evidence}')

    conn.commit()
    conn.close()

    # Summary counts
    counts = {}
    for _, (code, _) in STAGE_MAP.items():
        name = STAGE_NAMES[code]
        counts[name] = counts.get(name, 0) + 1

    print(f'\nClassified {updated}/50 emblems:')
    for stage, count in sorted(counts.items()):
        print(f'  {stage}: {count}')


if __name__ == '__main__':
    main()
