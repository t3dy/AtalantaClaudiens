"""Rewrite scholar profiles to 5-10 paragraph museum-level quality.

Follows docs/WRITING_TEMPLATES.md scholar profile template:
1. Identity and credentials
2. Intellectual formation and approach
3. Contributions to Maier studies
4. Key arguments
5. Relevance to this site

Also removes duplicate Wescott entry (IDs 4 and 12).
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

PROFILES = {
    "H.M.E. de Jong": (
        "Helena Maria Elisabeth De Jong (1933-2016) was a Dutch art historian trained at the University "
        "of Utrecht, where she completed her doctoral dissertation on Michael Maier's Atalanta Fugiens in 1965. "
        "De Jong's monograph, published in expanded form by E.J. Brill in 1969 as Michael Maier's Atalanta Fugiens: "
        "Sources of an Alchemical Book of Emblems, remains the foundational work of Atalanta Fugiens scholarship and "
        "the single most important study of Maier's emblematic method.\n\n"

        "De Jong's approach was source-critical in the tradition of Dutch art history: systematic, archival, and "
        "exhaustive. Rather than offering a general interpretation of Maier's alchemical philosophy, she set out to "
        "identify the precise textual sources behind each of the fifty emblems — the specific passages in the Turba "
        "Philosophorum, the Rosarium Philosophorum, the Aurora Consurgens, Ovid's Metamorphoses, and dozens of other "
        "classical and alchemical texts that Maier quoted, paraphrased, or alluded to in his mottos, discourses, and "
        "epigrams. This source-critical method was unprecedented in alchemical scholarship, which had previously "
        "treated emblem books as self-contained artistic or philosophical statements rather than as compilations "
        "with traceable textual genealogies.\n\n"

        "De Jong's central contribution is demonstrating that Maier was not an original alchemical theorist but a "
        "supremely learned compiler and re-interpreter of earlier traditions. She shows that virtually every element "
        "of the Atalanta Fugiens — each motto, each discourse argument, each source citation — can be traced to "
        "specific passages in the medieval and Renaissance alchemical corpus. The Turba Philosophorum and the Rosarium "
        "Philosophorum emerge as Maier's two most heavily used sources, with the Pseudo-Aristotelian Tractatulus, "
        "the Allegoria Merlini, and the Tabula Smaragdina also playing major roles. De Jong maps these source "
        "relationships emblem by emblem, creating a concordance that reveals the architecture of Maier's learning.\n\n"

        "Perhaps De Jong's most distinctive argument is that alchemical terms operate simultaneously across multiple "
        "registers — material, medical, spiritual, and cosmological — and that Maier's genius lay in orchestrating "
        "these registers through the multi-sensory medium of the emblem book. She shows how a single term like "
        "'Nigredo' carries meaning as a chemical process (blackening through putrefaction), a medical condition "
        "(melancholia and black bile), a spiritual state (the dark night of the soul), and a cosmological principle "
        "(Saturn's dominion). This multi-register model has become the standard framework for understanding "
        "alchemical symbolism.\n\n"

        "De Jong's work also established the frontispiece as the interpretive key to the entire work, demonstrating "
        "that the myth of Atalanta and Hippomenes functions as Maier's pedagogical program — the reader must pursue "
        "wisdom (Atalanta) through the sensory enticements (golden apples) of image, music, and text. Her analysis "
        "of the individual emblem plates, while not her primary focus, provides essential iconographic identifications "
        "that subsequent scholars have built upon.\n\n"

        "This site is fundamentally a showcase of De Jong's findings. Every emblem page's source analysis, every "
        "dictionary term's alchemical significance, and every source authority identification derives from her "
        "meticulous scholarship. Without De Jong's work, the textual traditions behind the Atalanta Fugiens would "
        "remain opaque to modern readers."
    ),

    "Hereward Tilton": (
        "Hereward Tilton is a historian of alchemy and Rosicrucianism whose monograph The Quest for the Phoenix: "
        "Spiritual Alchemy and Rosicrucianism in the Work of Count Michael Maier (Walter de Gruyter, 2003) is "
        "the most comprehensive modern study of Maier's intellectual world. Where De Jong focused narrowly on the "
        "textual sources of the Atalanta Fugiens, Tilton places the entire body of Maier's work within the broader "
        "context of Rosicrucian ideology, Paracelsian iatrochemistry, and the political dynamics of the Habsburg court.\n\n"

        "Tilton's approach is historiographical and contextual, drawing on archival research, close reading of Maier's "
        "full bibliography (some twenty-five published works), and engagement with the scholarly literature on "
        "Rosicrucianism developed by Carlos Gilly and the Bibliotheca Philosophica Hermetica in Amsterdam. His method "
        "places Maier's alchemical writings within the specific political and religious circumstances of their "
        "production — the twilight of Rudolf II's court, the Rosicrucian manifestos, the gathering storm of the "
        "Thirty Years' War — rather than treating them as timeless philosophical statements.\n\n"

        "Tilton's most significant contribution to Atalanta Fugiens scholarship is his identification of the "
        "Rosicrucian dimension in Maier's emblems. He shows how specific emblems encode Rosicrucian themes — the "
        "fourfold fire-ball of Emblem XVII reflecting Rosicrucian enigmas, the Aqua Foetida imagery of Emblems X and "
        "XXXVII connecting to Paracelsian pharmaceutical debates, and the Duenech allegory of Emblem XXVIII deriving "
        "from the Allegoria Merlini within a specifically Rosicrucian interpretive framework. Tilton also provides "
        "the most detailed discussion of Maier's claim to have produced the Universal Medicine during his Kiel "
        "laboratory period (1602-1608), a claim documented in Maier's letter to August von Anhalt.\n\n"

        "Tilton argues that Maier was not merely sympathetic to Rosicrucianism but was actively working to transform "
        "the Rosicrucian 'ludibrium' (prank or fiction) into a genuine spiritual and scientific movement. His Atalanta "
        "Fugiens, in this reading, is both an alchemical textbook and a Rosicrucian manifesto — a work designed to "
        "attract serious seekers to the Brotherhood's ideals while encoding its deepest teachings in the multi-layered "
        "medium of the emblem.\n\n"

        "For this site, Tilton's work enriches the scholarly commentary on fifteen emblems where his Rosicrucian "
        "readings add a dimension absent from De Jong's source-critical approach. His biographical research also "
        "informs the biography page, particularly regarding Maier's time at Rudolf's court and his English sojourn."
    ),

    "J.B. Craven": (
        "The Reverend J.B. Craven, D.D., was a Scottish clergyman and antiquarian whose Count Michael Maier, Doctor "
        "of Philosophy and of Medicine, Alchemist, Rosicrucian, Mystic, 1568-1622 (Kirkwall: William Peace & Son, 1910) "
        "was the first English-language monograph on Maier and remained the sole book-length study for over half a century "
        "until De Jong's dissertation in 1965. Joscelyn Godwin called it 'still indispensable for anyone without a "
        "complete set of Maier's works on their shelves.'\n\n"

        "Craven's approach was that of a Victorian antiquarian: exhaustive, encyclopedic, and reverential. Writing "
        "at a time when few of Maier's works had been studied in any detail, Craven undertook the monumental task of "
        "surveying, describing, and summarizing Maier's entire published output, providing English-language paraphrases "
        "of the Latin texts and detailed descriptions of the engravings. His work is more a descriptive catalog than "
        "an analytical study, but its comprehensiveness made it the standard reference for generations.\n\n"

        "Craven's most valuable contribution is his detailed description of the Atalanta Fugiens frontispiece, which "
        "remains one of the most precise verbal accounts of the engraving: the race of Atalanta and Hippomenes at the "
        "bottom, Venus handing the golden apples at the side, the lovers embracing in the temple entrance before emerging "
        "as lion and lioness, and Hercules approaching the Hesperides above. He also provides extensive biographical "
        "detail drawn from sources that were largely inaccessible before the archival discoveries of Figala and Neumann.\n\n"

        "Craven's treatment of the alchemical content is sympathetic but uncritical — he accepts Maier's claims at face "
        "value and does not attempt the kind of source analysis that De Jong would later perform. His discussions of "
        "individual emblems tend toward paraphrase rather than interpretation. Nevertheless, his English-language "
        "summaries of the emblem discourses remain useful as a quick reference.\n\n"

        "For this site, Craven provides survey-level scholarly references for seventeen emblems, including the "
        "frontispiece. His biographical detail supplements Tilton's more archivally grounded reconstruction, and his "
        "frontispiece description informs the visual analysis of Emblem 0."
    ),

    "Joscelyn Godwin": (
        "Joscelyn Godwin (born 1945, England) is a musicologist and historian of esoteric traditions, educated at "
        "Magdalene College, Cambridge, with a Ph.D. in Musicology from Cornell University. Since 1971 he has taught "
        "at Colgate University in Hamilton, New York. Godwin occupies a unique position in Maier scholarship as both "
        "the editor of the standard English edition of the Atalanta Fugiens (Grand Rapids: Phanes Press, 1989) and "
        "the author of the biographical essay 'The Deepest of the Rosicrucians: Michael Maier' in The Rosicrucian "
        "Enlightenment Revisited (1999).\n\n"

        "Godwin's musicological training gives him a distinctive perspective on Maier's multi-sensory project. "
        "Where De Jong focused on textual sources and Tilton on Rosicrucian context, Godwin approaches the Atalanta "
        "Fugiens as a total artwork — a Gesamtkunstwerk avant la lettre — in which the fifty three-voice fugues are "
        "not mere decoration but integral to the work's pedagogical and philosophical program. His edition of the "
        "fugues, with modern musical notation and performance suggestions, made the musical dimension of the work "
        "accessible to a modern audience for the first time.\n\n"

        "Godwin's biographical essay, drawing on the archival discoveries of Karin Figala and Ulrich Neumann (Munich), "
        "provides the most detailed narrative reconstruction of Maier's life available in English. He established key "
        "facts including Maier's birth in Kiel in 1569, his father's profession as an embroiderer in gold and pearls, "
        "his claim to have produced the Universal Medicine 'of a bright lemon color' during the Kiel laboratory "
        "period (1602-1608), and the economic precariousness of his position as an unlanded nobleman after Rudolf II's "
        "ennoblement. Godwin also identifies Maier's five-year English sojourn (1611-1616) as 'almost certainly the "
        "fulfilment of a diplomatic mission' preparing the ground for the Frederick-Elizabeth dynastic marriage.\n\n"

        "Godwin characterizes Maier's creative method as distinctively 'multimedia,' visible from the Christmas greeting "
        "to James I (1611) — a folded parchment combining a Rose-Cross emblem in gold and red, four Latin poems, and "
        "a six-part musical canon — through to the Atalanta Fugiens itself, with its integrated program of image, text, "
        "and music. He argues that this multimedia approach was Maier's signature contribution to the emblem tradition.\n\n"

        "Godwin's title — borrowed from Frances Yates's confession that she found Maier's emblems incomprehensible but "
        "sensed he 'may have been the deepest of the Rosicrucians' — frames the fundamental challenge of Maier "
        "scholarship: a body of work so densely layered that no single disciplinary approach can fully unlock it. "
        "For this site, Godwin's biographical research informs the biography page, his musicological perspective "
        "enriches the discussion of Maier's pedagogical method, and his edition of the fugues is the standard "
        "reference for the musical dimension of each emblem."
    ),

    "Walter Pagel": (
        "Walter Pagel (1898-1983) was a German-born British historian of medicine, one of the foremost scholars of "
        "Paracelsus and the Paracelsian tradition in the twentieth century. His review of De Jong's Atalanta Fugiens "
        "monograph, published in Medical History (1973), brought the perspective of medical history to bear on Maier's "
        "work, emphasizing the iatrochemical and Empedoclean dimensions that De Jong's art-historical approach had "
        "touched on but not fully developed.\n\n"

        "Pagel's approach was rooted in the history of medical and scientific thought, particularly the intersection "
        "of alchemy, medicine, and natural philosophy in the early modern period. He was uniquely qualified to assess "
        "the medical content of Maier's emblems, having spent decades studying the Paracelsian reformation of medicine "
        "and its impact on seventeenth-century science. His major works on Paracelsus, William Harvey, and Jan "
        "Baptista van Helmont established him as the leading authority on the relationship between alchemy and early "
        "modern medicine.\n\n"

        "In his review, Pagel identifies specific emblems where the medical register of alchemical symbolism is "
        "particularly prominent. He draws attention to the humoral medicine embedded in Emblem XXVIII (the steam bath "
        "as therapeutic purification), the Empedoclean cosmology underlying Emblem X (fire to fire, Mercury to Mercury), "
        "and the medical analogies in Emblems II, XIII, XVI, and XLVIII. Pagel argues that Maier's training as a "
        "physician was not incidental to his alchemical work but foundational — the medical register was not a metaphor "
        "but a genuine theoretical framework within which Maier understood chemical transformations.\n\n"

        "For this site, Pagel provides twelve emblem-specific scholarly references that foreground the medical dimension "
        "of Maier's emblematic program. His perspective is particularly valuable for the multi-register dictionary "
        "definitions, where the 'medical' register entries draw on his identification of humoral and iatrochemical "
        "themes in specific emblems."
    ),

    "Paul Miner": (
        "Paul Miner is a literary historian and iconographer whose article 'Blake and Atalanta Fugiens: Two Plates, "
        "Three Conjectures' (Notes and Queries, 2012) investigates the visual influence of Maier's engravings on the "
        "art of William Blake. Miner's work opens a reception-history dimension largely absent from other Atalanta "
        "Fugiens scholarship, which has tended to focus on Maier's sources rather than his influence.\n\n"

        "Miner's approach is comparative iconographic analysis, placing specific Blake designs alongside Maier's "
        "engravings to identify compositional borrowings, shared motifs, and transformed symbolic elements. He is not "
        "concerned with Maier's alchemical philosophy per se but with the visual afterlife of the Atalanta Fugiens "
        "plates in English Romantic art — a question that connects Maier's seventeenth-century emblems to the broader "
        "history of Hermetic visual culture.\n\n"

        "Miner identifies specific iconographic connections between Blake and four AF emblems: the Hermaphrodite lying "
        "in darkness (Emblems XXXIII and XXXIV) and the standing Hermaphrodite (Emblem XXXVIII). He argues that "
        "Blake's hermaphroditic and hierogamos imagery — the union of contraries that is central to Blake's mythology — "
        "draws directly on Maier's visual compositions, suggesting that Blake had access to the Atalanta Fugiens "
        "or to derivative works that reproduced Maier's plates.\n\n"

        "For this site, Miner provides four emblem-specific references and a unique reception-history perspective. "
        "His work demonstrates that the Atalanta Fugiens was not merely a period piece but a visual resource that "
        "continued to shape artistic production two centuries after its publication."
    ),

    "Douglas Leedy": (
        "Douglas Leedy (1938-2015) was an American composer, musicologist, and performer specializing in early music "
        "and alternative tuning systems. His review of Joscelyn Godwin's edition of the Atalanta Fugiens (Notes, 1991) "
        "provides a detailed musicological assessment of Maier's fifty three-voice fugues — the only sustained "
        "technical analysis of the musical component of the work in our corpus.\n\n"

        "Leedy's approach was that of a practicing musician evaluating the fugues as compositions: their modal "
        "structures, contrapuntal technique, text-painting devices, and relationship to the visual and textual "
        "elements of each emblem. He brought to this analysis decades of experience with Renaissance and early "
        "Baroque polyphony, giving him a sensitivity to the musical idiom of Maier's period that few other Atalanta "
        "Fugiens scholars possess.\n\n"

        "Leedy's most important observation is that the fugues are not mere accessories but are musically sophisticated "
        "compositions that repay careful analysis. He identifies modal choices that correspond to the alchemical content "
        "of specific emblems, text-painting techniques where the musical lines mirror the allegorical action described "
        "in the mottos, and structural features that suggest Maier (or his musical collaborator, if one existed) "
        "possessed genuine compositional skill. This challenges the dismissive view, common in musicological "
        "literature, that the fugues are crude or amateurish.\n\n"

        "For this site, Leedy's review validates the musical dimension of the Atalanta Fugiens as worthy of serious "
        "attention and provides the technical vocabulary for discussing the fugues' relationship to the emblematic "
        "program."
    ),

    "Pamela H. Smith": (
        "Pamela H. Smith is Seth Low Professor of History at Columbia University and a leading historian of science "
        "and material culture in the early modern period. Her review in Medical History (2009) of Thomas Hofmeier's "
        "German translation of the Atalanta Fugiens (Chymisches Cabinet, 2008) addresses the work's significance "
        "within the broader history of artisanal knowledge and the relationship between craft practice and natural "
        "philosophy.\n\n"

        "Smith's approach is informed by her influential work on the 'body of the artisan' — the argument that early "
        "modern natural knowledge was produced not only through reading and reasoning but through bodily engagement "
        "with materials in workshops and laboratories. She brings this materialist perspective to the Atalanta Fugiens, "
        "reading Maier's emblems not merely as symbolic puzzles but as representations of actual craft practices — "
        "smelting, distilling, washing, firing — that encode genuine chemical knowledge.\n\n"

        "Smith's review situates the Hofmeier edition within the context of contemporary efforts to reconstruct "
        "early modern making knowledge, including the Making and Knowing Project at Columbia, which she directs. "
        "She emphasizes the importance of the 1708 German edition as evidence of the work's continued practical "
        "relevance nearly a century after its original publication.\n\n"

        "For this site, Smith's materialist perspective provides a valuable counterpoint to the purely textual "
        "and symbolic readings of De Jong and Tilton. Her emphasis on the practical, artisanal dimension of "
        "Maier's emblems enriches the discussion of specific emblems where craft processes are depicted."
    ),

    "Donna Bilak": (
        "Donna Bilak is an art historian specializing in steganography, visual cryptography, and the hidden codes "
        "embedded in early modern alchemical imagery. Her work on the Atalanta Fugiens approaches the engravings "
        "as steganographic objects — images that conceal messages within their visual structure, accessible only "
        "to viewers trained in the conventions of alchemical reading.\n\n"

        "Bilak's approach draws on the theory of steganography developed by Trithemius and Porta, arguing that "
        "Maier and his engraver Matthaeus Merian deliberately embedded coded information in the composition, "
        "geometry, and iconographic details of the fifty plates. This goes beyond the conventional reading of "
        "alchemical symbolism (recognizing that a toad represents sulphur, for instance) to propose that the "
        "plates contain a second layer of meaning encoded in their formal properties — spatial relationships, "
        "geometric proportions, and visual puns.\n\n"

        "Bilak's contribution to the Furnace and Fugue digital edition of the Atalanta Fugiens (published by the "
        "Science History Institute) represents the most technologically sophisticated engagement with Maier's "
        "work, combining high-resolution image analysis with interactive digital tools for exploring the "
        "multi-layered structure of each emblem. Her work has been instrumental in bringing the Atalanta Fugiens "
        "to the attention of digital humanities scholars.\n\n"

        "For this site, Bilak's steganographic approach represents an emerging dimension of Atalanta Fugiens "
        "scholarship that extends beyond De Jong's source-critical method into questions of visual encoding "
        "and hidden communication."
    ),

    "Tara Nummedal": (
        "Tara Nummedal is a historian of science at Brown University whose work on early modern alchemy, fraud, "
        "and entrepreneurship has reshaped understanding of alchemy's place in the economic and social history of "
        "early modern Europe. Her involvement with the Furnace and Fugue project — a collaborative digital edition "
        "of the Atalanta Fugiens hosted by the Science History Institute — represents the most ambitious digital "
        "humanities engagement with Maier's work.\n\n"

        "Nummedal's approach situates alchemy within the history of commerce, patronage, and fraud rather than "
        "treating it as a purely intellectual or spiritual pursuit. Her monograph Alchemy and Authority in the Holy "
        "Roman Empire (University of Chicago Press, 2007) demonstrates that alchemical practitioners operated within "
        "complex networks of patronage, investment, and legal regulation — the same networks that shaped Maier's "
        "career as he moved from Rudolf II's court through England to the courts of Moritz von Hessen and Christian "
        "Wilhelm von Brandenburg.\n\n"

        "The Furnace and Fugue project, which Nummedal co-directs, provides an interactive digital edition of the "
        "Atalanta Fugiens with high-resolution images, musical performances, and scholarly commentary. It represents "
        "a new model for presenting multi-sensory works like Maier's, allowing users to experience the integration "
        "of image, text, and music that Maier intended.\n\n"

        "For this site, Nummedal's work provides the institutional and methodological context for digital humanities "
        "engagement with the Atalanta Fugiens. The Furnace and Fugue project is the primary alternative digital "
        "resource for studying Maier's work."
    ),

    "Catherine Morris Wescott": (
        "Catherine Morris Wescott is a scholar of music and alchemy whose analysis of the Atalanta Fugiens fugues "
        "provides the most detailed examination of the modal and contrapuntal structure of Maier's musical compositions "
        "in our corpus. Her work, published in the AthanorX journal, combines musicological analysis with alchemical "
        "interpretation, reading the fugues as musical encodings of alchemical processes.\n\n"

        "Wescott's approach is uniquely interdisciplinary, combining technical music theory (modal analysis, interval "
        "identification, cantus firmus technique) with alchemical symbolism to argue that the musical and visual "
        "dimensions of each emblem are not merely parallel but mutually reinforcing. She demonstrates that Maier's "
        "modal choices — Dorian, Phrygian, Mixolydian — correspond to planetary associations (Saturn, Mars, Jupiter) "
        "that in turn relate to the alchemical stages depicted in the emblem plates.\n\n"

        "Wescott provides detailed analysis of the planetary-modal correspondences in several emblems, showing how "
        "the three voices of each fugue (typically representing Atalanta fleeing, Hippomenes pursuing, and the golden "
        "apple as cantus firmus) enact the alchemical drama described in the motto and discourse. Her analysis of "
        "Emblems XXIV, XXVIII, XXXI, and XLIV is particularly detailed, combining musical and iconographic readings.\n\n"

        "For this site, Wescott provides fifteen scholarly references spanning both musical and alchemical "
        "interpretation. Her work is essential for understanding the fugues as integral to Maier's emblematic "
        "program rather than as decorative additions."
    ),
}


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Remove duplicate Wescott (ID 4 is the old one, ID 12 is the new one from extract_secondary)
    # Keep ID 12 (Catherine Morris Wescott) since it was added by the secondary extraction
    # But update it with the full profile
    # First check which one has more refs
    refs_4 = c.execute('SELECT count(*) FROM scholarly_refs WHERE bib_id IN (SELECT id FROM bibliography WHERE source_id LIKE "%wescott%")').fetchone()[0]
    print(f'Wescott refs via bibliography: {refs_4}')

    # Update profiles
    updated = 0
    for name, overview in PROFILES.items():
        result = c.execute('UPDATE scholars SET overview = ? WHERE name = ?', (overview, name))
        if result.rowcount > 0:
            updated += 1
            print(f'  Updated: {name} ({len(overview)} chars)')
        else:
            print(f'  NOT FOUND: {name}')

    # Check for old duplicate Wescott "C. Morris Wescott" and remove if exists
    old = c.execute('SELECT id, name FROM scholars WHERE name = ?', ('C. Morris Wescott',)).fetchone()
    if old:
        # Move any scholar_works references
        c.execute('UPDATE scholar_works SET scholar_id = (SELECT id FROM scholars WHERE name = ?) WHERE scholar_id = ?',
                  ('Catherine Morris Wescott', old[0]))
        c.execute('DELETE FROM scholars WHERE id = ?', (old[0],))
        print(f'  Removed duplicate: {old[1]} (ID {old[0]})')

    conn.commit()
    conn.close()
    print(f'\nUpdated {updated} scholar profiles.')


if __name__ == '__main__':
    main()
