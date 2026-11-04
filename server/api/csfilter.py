"""Rufzeichen-Filter (V1, 04.11.2026): Beleidigungen/Obszönes (EN/DE/ES/PT/RU) und Muster echter Namen.
check(name) -> None (ok) oder Grund: "rude" | "realname" | "contact"."""
import re, unicodedata

LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b", "9": "g", "@": "a", "$": "s"})
CYR2LAT = str.maketrans({"а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "к": "k", "м": "m", "т": "t", "в": "b", "н": "h"})

# Wortstämme, die als Teilstring reichen (lang/eindeutig genug)
RUDE_SUB = """
fuck fuk fck fack phuck shit bitch cunt nigg nigga faggot fagot retard whore slut dick cock pussy penis vagina porn
rape rapist nazi hitler heil kkk jizz wank twat bastard asshole arsch fotze hurensohn wichser schlampe
schwuchtel spast missgeburt kanake neger nutte ficken fick scheiss scheis puta puto pendejo cabron
mierda verga coño cono gilipollas maricon caralho porra buceta viado foder fodase merda arrombado
хуй хуе хуё пизд ебат ебан ёбан еба бляд блят сука мудак пидор пидар гандон шлюх залуп дроч
""".split()
# kurze Wörter nur als ganzes Wort
RUDE_WORD = set("ass fag sex cum tit tits kys hoe nig suka blyat blyad hui huy pizda".split())
ALLOW = ("scunthorpe", "penistone", "cockpit", "cocktail", "dickens", "shitake", "shiitake")

FIRST = set("""
anna maria max paul lukas leon felix jonas elias noah ben finn emma mia sofia sophia lena laura lea hannah lisa
sarah julia marie emily david daniel michael thomas andreas stefan christian peter martin markus alexander jan
tobias florian sebastian simon tim tom luca luis louis john james robert william mary patricia jennifer linda
elizabeth susan jessica karen nancy joseph charles christopher matthew anthony mark donald steven andrew joshua
kevin brian george edward ryan jacob olivia ava isabella sophie charlotte amelia harper evelyn abigail ella
jose juan carlos luis miguel javier antonio francisco manuel pedro pablo diego alejandro sergio fernando
ana lucia carmen isabel elena paula sara marta laura joao gabriel lucas mateus rafael bruno gustavo felipe
mariana beatriz larissa camila amanda leticia ivan dmitri dmitry sergei sergey alexei alexey andrei andrey
nikolai vladimir mikhail pavel anastasia natalia olga tatiana svetlana irina ekaterina daria polina
иван дмитрий сергей алексей андрей николай владимир михаил павел александр максим анна мария анастасия
наталья ольга татьяна светлана ирина екатерина дарья полина елена
""".split())

def _norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s

def check(name):
    raw = name.strip()
    n = _norm(raw)
    if re.search(r"\d{6,}", n) or "@" in raw or re.search(r"(https?|www|\.com|t\.me)", n):
        return "contact"
    flat = re.sub(r"[\s_\-]+", "", n).translate(LEET)
    flat = re.sub(r"(.)\1{2,}", r"\1\1", flat)
    variants = {flat, flat.translate(CYR2LAT), re.sub(r"(.)\1+", r"\1", flat)}
    for v in variants:
        for a in ALLOW:
            v = v.replace(a, "")
        if any(w in v for w in RUDE_SUB):
            return "rude"
    words = [re.sub(r"\d+$", "", w).translate(LEET) for w in re.split(r"[\s_\-]+", n) if w]
    if flat in RUDE_WORD or re.sub(r"[\s_\-]+", "", re.sub(r"\d+$", "", n)).translate(LEET) in RUDE_WORD or any(w in RUDE_WORD for w in words):
        return "rude"
    # «Vorname Nachname»: zwei Wörter aus Buchstaben, erstes ein bekannter Vorname, zweites ≥ 3 Buchstaben
    parts = [p for p in re.split(r"[\s_\-]+", raw) if p]
    if len(parts) == 2 and all(p.isalpha() for p in parts):
        a, b = _norm(parts[0]), _norm(parts[1])
        if a in FIRST and len(b) >= 3 and b not in FIRST:
            return "realname"
    return None

if __name__ == "__main__":
    for t in ["Mart test", "Capy King", "Max Mustermann", "f4ck3r", "Blue_Rosie", "SUKA99", "сука", "Anna Schmidt",
              "Sniper-7", "Hitler", "class act", "Scunthorpe", "assassin", "a s s", "Ivan Petrov", "Rumba", "0664123456", "Cocktail", "Fuchs", "Dickens Fan"]:
        print(t, "->", check(t))
