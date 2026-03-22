"""Update biography sections with Godwin's new biographical facts."""
import json
import os

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'atalanta_fugiens_seed.json')

def main():
    with open(SEED_PATH, encoding='utf-8') as f:
        data = json.load(f)

    bio = data['biography']
    bio['title'] = 'Michael Maier (1569-1622)'

    # Section 0: Early Life
    bio['sections'][0]['content'] = (
        "Michael Maier was born in the summer of 1569 in Kiel, on the Baltic Sea, in the Duchy of Holstein, "
        "then under Danish rule. His father, Peter Maier, was an embroiderer in gold and pearls (Goldsicker) "
        "who worked for the nobility of Holstein, including King Friedrich II of Denmark and the powerful "
        "governor Heinrich Rantzau. Peter's professional concern with gold was, as Tilton observes, a portent "
        "of things to come for his son. Peter ensured Michael received a literary education from age five, "
        "preparing him for a scholarly career, but died before 1587.\n\n"

        "At the expense of a maternal relative, the young Maier was sent to the University of Rostock in 1587 "
        "to study philosophy and the Liberal Arts. Between 1589 and 1591 he made one or more journeys to Padua, "
        "where he was honored with the title of Poet Laureate. In 1592 he obtained the Doctorate of Philosophy "
        "from the University of Frankfurt an der Oder. His academic training was completed with the degree of "
        "Doctor of Medicine, granted by the University of Basel in 1596, where his dissertation concerned "
        "epilepsy (no copy survives).\n\n"

        "Maier returned to the Baltic to practice as a physician in Holstein and East Prussia, proudly bearing "
        "three titles from the Schools: Ph.D., M.D., and Poet Laureate. Shortly after his return, he witnessed "
        "a remarkable alchemical cure that reoriented his life entirely. With characteristic systematism, he began "
        "by making a glossary of alchemical terms, then studied the theoretical literature, and made first-hand "
        "study of natural phenomena in mining regions. Finally he proceeded to laboratory practice, setting up "
        "a laboratory in Kiel with his brother-in-law (Maier never married). His alchemical work lasted from "
        "1602 until 1607 or 1608, at the end of which time he claimed to have obtained, by God's grace, the "
        "Universal Medicine, described as being of a bright lemon color. He was unable to proceed further owing "
        "to technical difficulties, and the long experiments had exhausted his funds while making him an object "
        "of hostile curiosity among the provincial burghers of Kiel."
    )

    # Section 1: Court of Rudolf II
    bio['sections'][1]['content'] = (
        "Under such conditions, Maier turned to the court of the Holy Roman Emperor, Rudolf II, the most "
        "important center of alchemical patronage in early modern Europe. Around the middle of 1608, he went "
        "to Prague and presented himself, armed with his Universal Medicine, at the Hradcany Palace. It took "
        "him about a year to penetrate the circles of courtly obstruction surrounding the reclusive Emperor. "
        "Perhaps the door was opened by the publication of his first alchemical book, De Medicina regia et vere "
        "heroica, Coelidonia (Prague, 1609).\n\n"

        "On 19 September 1609 Maier entered the Emperor's service, and ten days later was raised to the "
        "nobility. Rudolf gave him three titles: Personal Physician, Count Palatine, and Knight Exemptus. "
        "This ennoblement, however, came without a grant of land that would provide income commensurate with "
        "such titles. As Godwin observes, Maier was left in the uncomfortable condition of an unlanded "
        "nobleman \u2014 barred from modest employment such as tutoring or general medical practice, yet having "
        "no property or inherited wealth. He was henceforth dependent on attachment to noble households or "
        "diplomatic status.\n\n"

        "The Prague years exposed Maier to the full range of alchemical traditions he would later synthesize "
        "in Atalanta Fugiens: Hermetic philosophy rooted in the Emerald Tablet, the Arabic-Latin compilations "
        "of the Turba Philosophorum, the Rosarium Philosophorum, and the Pseudo-Aristotelian treatises. De "
        "Jong's source-critical analysis reveals a mind steeped in these traditions, capable of weaving them "
        "into a coherent symbolic program spanning fifty emblems.\n\n"

        "Rudolf II's golden years were ending. The melancholy Emperor was forced to abdicate in favor of his "
        "brother Matthias in April 1611 and died, a virtual prisoner in his own palace, on 20 January 1612. "
        "Maier, along with many other courtiers and artists, was obliged to seek another patron."
    )

    # Section 2: The Rosicrucian Moment
    bio['sections'][2]['content'] = (
        "Instead of settling with any of the three alchemically-inclined rulers he approached \u2014 August von "
        "Anhalt-Plotzkau, Moritz von Hessen-Kassel, and Ernst III von Holstein-Schauenburg \u2014 Maier went to "
        "England, arriving before Christmas 1611 and remaining there until 1616.\n\n"

        "His visiting-card to King James I took a most unusual form: a Christmas greeting made of folded "
        "parchment, 33 by 24 inches, on which a central Rose-Cross emblem constructed from words in gold and "
        "red was flanked by four Latin poems. Two poems address the King directly, while the others are put "
        "into the mouths of four archangels and two shepherds attendant on Christ's Nativity. The parchment "
        "includes a musical canon in six parts representing the songs of the angels and shepherds. It is the "
        "earliest known appearance of the Rose-Cross symbol in England, and it displays the verbal ingenuity "
        "and multimedia approach that marked Maier's creative style throughout his career.\n\n"

        "Godwin argues that Maier's five-year English presence was almost certainly the fulfilment of a "
        "diplomatic mission, preparing the ground for the dynastic marriage between Elector Frederick of the "
        "Palatinate and Princess Elizabeth. His status as Count Palatine and familiar of the eirenic Rudolf "
        "made him an acceptable envoy. In London, Maier frequented the circle of Hermetic physicians close "
        "to the Court, including Sir William Paddy, James I's personal physician and a close friend of Robert "
        "Fludd. To Paddy he dedicated his Arcana arcanissima (1614). While no direct evidence proves that "
        "Maier and Fludd met, the circumstantial case is compelling.\n\n"

        "The publication of the Fama Fraternitatis (1614) and Confessio Fraternitatis (1615) during Maier's "
        "English sojourn intensified the Rosicrucian moment. He produced several works engaging directly with "
        "the manifestos, including Silentium post Clamores (1617) and Themis Aurea (1618), systematically "
        "defining what authentic Rosicrucianism meant and distinguishing it from the enthusiasm of self-proclaimed "
        "Brethren."
    )

    # Section 4: Later Works and Death
    bio['sections'][4]['content'] = (
        "Maier must have devoted much of his English years to research and writing, for within two years of "
        "his return to Germany in mid-1616, he published eleven books \u2014 an extraordinary burst of productivity. "
        "He lived for two years in Frankfurt am Main, perhaps supported by the publishers of his numerous books, "
        "dedicating them either to fellow scholars or to Hermetically-inclined Protestant rulers.\n\n"

        "In 1618 Moritz von Hessen, to whom Maier had presented copies of all his books, rewarded him with the "
        "official title Medicus und Chymicus von Haus aus (Original Physician and Alchemist). But political "
        "upheaval soon disrupted this arrangement. The death of Emperor Matthias, the rebellion of the Bohemian "
        "estates, the catastrophic Battle of the White Mountain (1620) \u2014 all weighed heavily on Moritz and "
        "threatened his little realm. He had neither time nor money for esoteric diversions.\n\n"

        "Maier moved north. In 1620 he was in Magdeburg, where he had a potential patron in Markgraf Christian "
        "Wilhelm von Brandenburg. Two years later, in 1622, he was petitioning Herzog Friedrich III von "
        "Schleswig-Holstein-Gottorf, apparently with a view to returning to his Baltic homeland. But his plans "
        "never matured. Maier died in Magdeburg in the late summer of 1622. His last book, the forty-page "
        "Ulysses (published posthumously in 1624), sounded a valedictory note imbued with Christian Stoicism: "
        "it treats of how to recover from the shipwreck of bodily goods and fortune through the virtues of the "
        "intellect.\n\n"

        "Maier's travels had almost come full circle, taking him as far south as Padua, as far west as London, "
        "and all around the states of Germany. While modest by modern standards, they had given him a global "
        "consciousness rare for his time."
    )

    with open(SEED_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print('Biography updated with Godwin facts.')
    for s in bio['sections']:
        print(f"  {s['heading']}: {len(s['content'])} chars")


if __name__ == '__main__':
    main()
