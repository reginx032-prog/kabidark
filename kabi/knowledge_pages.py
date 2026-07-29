# -*- coding: utf-8 -*-
"""Baza wiedzy Kabi-Chemie — jedno źródło prawdy, gotowe pod backend/CMS.

Cała sekcja `/baza-wiedzy/` jest generowana z dwóch list danych:

    CATEGORIES  — kategorie (pillary)
    ARTICLES    — wpisy; każdy ma pole ``category`` (slug) i własny ``slug``

Adresy budujemy jako klaster tematyczny (hub-and-spoke):

    /baza-wiedzy/                          → hub
    /baza-wiedzy/{kategoria}/              → kategoria
    /baza-wiedzy/{kategoria}/{wpis}/       → wpis

Listy (hub, lista w kategorii, „ostatnie materiały") wyliczają się z danych,
więc dodanie kategorii lub wpisu = dopisanie jednego słownika. Ten sam model
1:1 przełoży się na tabele w backendzie (categories, articles).
Wygląd jest wspólny ze stronami rozwiązań (komponenty solution-*).
"""

BODY_CLASS = "has-dark-hero firm-page solution-page knowledge-page"
ROOT = "/baza-wiedzy/"


def _join(items):
    return "".join(items)


def _faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


# ---------------------------------------------------------------- ścieżki (URL)
def cat_path(cat):
    return f"{ROOT}{cat['slug']}/"


def art_path(art):
    return f"{ROOT}{art['category']}/{art['slug']}/"


def cat_by_slug(slug):
    for c in CATEGORIES:
        if c["slug"] == slug:
            return c
    return None


def articles_in(slug):
    return [a for a in ARTICLES if a["category"] == slug]


def art_image(a):
    """Grafika wpisu = własna, a jeśli jej nie ma — grafika kategorii-rodzica."""
    cat = cat_by_slug(a["category"])
    return a.get("image") or (cat["image"] if cat else "")


# ---------------------------------------------------------------- komponenty
_PHONE_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 '
    '19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 '
    '1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 '
    '1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg>'
)


def _hero(image, kicker, h1, lead, facts, primary, secondary, hub=False):
    """Pełnoekranowe, redakcyjne hero (jak na stronach rozwiązań)."""
    panel = _join(
        f"<div><span>{label}</span><strong>{value}</strong></div>"
        for label, value in facts
    )
    hero_class = " knowledge-hero--hub" if hub else ""
    facts_inline = ""
    side_panel = f'<aside class="solution-hero__panel knowledge-hero__panel reveal-right">{panel}</aside>'
    if hub:
        facts_inline = '<ul class="knowledge-hero__facts" aria-label="Zakres bazy wiedzy">' + _join(
            f'<li><img src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true"><strong>{value}</strong></li>'
            for _, value in facts
        ) + '</ul>'
        side_panel = ""
    return f"""
<section class="solution-hero knowledge-hero{hero_class}" style="--solution-image:url('{image}'); --solution-position:center center" id="top">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner solution-hero__inner--editorial">
    <div class="solution-hero__copy reveal-left">
      <p class="firm-kicker">{kicker}</p>
      <h1>{h1}</h1>
      <p>{lead}</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="{primary[1]}">{primary[0]}</a>
        <a class="{'knowledge-hero__link' if hub else 'btn btn-ghost-light'}" href="{secondary[1]}">{secondary[0]}{' <span aria-hidden="true">↗</span>' if hub else ''}</a>
      </div>
      {facts_inline}
    </div>
    {side_panel}
  </div>
</section>"""


def _related(items):
    links = _join(
        f'<a href="{href}"><span>{eyebrow}</span><strong>{title}</strong>'
        f'<i aria-hidden="true">↗</i></a>'
        for eyebrow, title, href in items
    )
    return (
        '<nav class="solution-related" aria-label="Powiązane strony"><div class="wrap">'
        '<p>Powiązane strony</p>'
        f'<div class="solution-related__links">{links}</div></div></nav>'
    )


def _faq(items,
         title="Najczęstsze pytania",
         intro="Krótkie odpowiedzi na pytania, które najczęściej pojawiają się przy tym temacie."):
    details = _join(
        f'<details{" open" if i == 0 else ""}><summary><span>{q}</span>'
        f'<i aria-hidden="true"></i></summary>'
        f'<div class="solution-faq__answer"><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(items)
    )
    return (
        '<section class="solution-faq" id="faq"><div class="wrap solution-faq__grid">'
        '<header class="solution-faq__intro reveal-left">'
        '<p class="solution-kicker"><span></span>FAQ</p>'
        f'<h2>{title}</h2><p>{intro}</p></header>'
        f'<div class="solution-faq__list">{details}</div></div></section>'
    )


def _cta():
    return (
        '<section class="solution-cta"><span class="solution-cta__mark" aria-hidden="true"></span>'
        '<div class="wrap solution-cta__inner"><div>'
        '<p class="solution-kicker"><span></span>Następny krok</p>'
        '<h2>Sprawdź, ile zaoszczędzi Twój zakład.</h2>'
        '<p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>'
        '<div class="solution-cta__actions">'
        '<a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>'
        f'<a class="solution-phone-link" href="tel:+48662792875">{_PHONE_SVG}'
        '<span>Zadzwoń: +48 662 792 875</span></a>'
        '</div></div></section>'
    )


def _stream_row(art, label):
    return (
        f'<a class="reveal" href="{art_path(art)}"><img src="{art_image(art)}" alt="" width="160" height="104" loading="lazy">'
        f'<span>{label}</span><strong>{art["excerpt"]}</strong></a>'
    )


def _consult_final():
    return (
        '<section class="solution-cta"><span class="solution-cta__mark" aria-hidden="true"></span>'
        '<div class="wrap solution-cta__inner"><div>'
        '<p class="solution-kicker"><span></span>Nie widzisz swojego problemu?</p>'
        '<h2>Opisz instalację. Podpowiemy pierwszy temat.</h2>'
        '<p>Możemy wskazać artykuł, zaproponować analizę wody albo umówić krótką rozmowę z inżynierem.</p></div>'
        '<div class="solution-cta__actions">'
        '<a class="btn btn-primary" href="/kontakt/">Zapytaj eksperta</a>'
        f'<a class="solution-phone-link" href="tel:+48662792875">{_PHONE_SVG}'
        '<span>Zadzwoń: +48 662 792 875</span></a>'
        '</div></div></section>'
    )


# ---------------------------------------------------------------- render stron
def render_hub():
    hero = _hero(
        HUB["image"], HUB["kicker"], HUB["h1"], HUB["lead"], HUB["facts"],
        ("Czytaj artykuły", "#artykuly"), ("Zapytaj eksperta", "/kontakt/"), hub=True,
    )
    featured = ARTICLES[0]
    fcat = cat_by_slug(featured["category"])
    kb_cards = _join(
        f'''<a class="kbcard reveal" href="{art_path(a)}" aria-label="Przeczytaj: {a['title']}">
        <span class="kbcard__num">{i:02d}</span>
        <span class="kbcard__meta">{cat_by_slug(a['category'])['title']} · {a['read']}</span>
        <h3 class="kbcard__title">{a['title']}</h3>
        <p class="kbcard__desc">{a['excerpt'][:1].upper() + a['excerpt'][1:]}</p>
        <span class="kbcard__go">Przeczytaj <i aria-hidden="true">↗</i></span>
      </a>'''
        for i, a in enumerate(ARTICLES[:3], 1)
    )
    mag = f"""
<section class="knowledge-branze" id="artykuly">
  <div class="wrap">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Artykuły</p>
      <h2>Wiedza z prawdziwych instalacji.</h2>
    </div>
    <div class="knowledge-branze__media reveal" style="--kb-img:url('{art_image(featured)}')" aria-hidden="true"></div>
    <div class="knowledge-branze__grid">{kb_cards}</div>
  </div>
</section>"""
    idx_cards = _join(
        f'''<a class="kccard reveal" href="{cat_path(c)}" aria-label="{c['title']}">
        <span class="kccard__img" style="--kc-img:url('{c["image"]}')" aria-hidden="true"></span>
        <span class="kccard__body">
          <span class="kccard__no">{i:02d}</span>
          <span class="kccard__title">{c["title"]}</span>
          <span class="kccard__desc">{c["hub_blurb"][:1].upper() + c["hub_blurb"][1:]}</span>
          <span class="kccard__go">Zobacz <i aria-hidden="true">↗</i></span>
        </span>
      </a>'''
        for i, c in enumerate(CATEGORIES, 1)
    )
    index = f"""
<section class="knowledge-cards">
  <div class="wrap">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Kategorie wiedzy</p>
      <h2>Wybierz obszar instalacji do uporządkowania.</h2>
    </div>
    <div class="knowledge-cards__grid">{idx_cards}</div>
  </div>
</section>"""
    return hero + mag + index + _consult_final()


def render_category(c):
    hero = _hero(
        c["image"], c["kicker"], c["h1"], c["lead"], c["facts"],
        ("Umów konsultację", "/bezplatna-konsultacja/"),
        ("Wróć do bazy wiedzy", ROOT),
    )
    arts = articles_in(c["slug"])
    if arts:
        rows = _join(_stream_row(a, a["short"]) for a in arts)
        stream = f"""
<section class="knowledge-stream">
  <div class="wrap knowledge-stream__grid">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Artykuły w tej kategorii</p>
      <h2>{c['stream_title']}</h2>
    </div>
    <div class="knowledge-stream__list">{rows}</div>
  </div>
</section>"""
    else:
        stream = f"""
<section class="knowledge-stream">
  <div class="wrap knowledge-stream__grid">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Artykuły w tej kategorii</p>
      <h2>{c['stream_title']}</h2>
      <p>Przygotowujemy materiały w tej kategorii. W międzyczasie sprawdź powiązane strony poniżej lub napisz do inżyniera.</p>
    </div>
  </div>
</section>"""
    editorial = ""
    if c["slug"] == "membrany-ro":
        editorial = """
<section class="membrane-category-intro">
  <span class="membrane-category-intro__mark" aria-hidden="true"></span>
  <div class="wrap membrane-category-intro__grid">
    <header class="firm-section-head reveal-left">
      <p class="firm-kicker">Punkt wyjścia</p>
      <h2>Stabilny odzysk zaczyna się przed RO.</h2>
      <p>Wydajności RO nie poprawia się jedną dawką. Najpierw trzeba połączyć jakość wody zasilającej, warunki pracy i rzeczywisty trend instalacji.</p>
    </header>
    <ol class="membrane-category-intro__steps">
      <li class="reveal"><span>01</span><div><strong>Sprawdź wodę zasilającą</strong><p>Twardość, krzemionka, przewodność i żelazo określają ryzyko osadu oraz foulingu.</p></div></li>
      <li class="reveal"><span>02</span><div><strong>Ustal punkt pracy</strong><p>Odzysk, ciśnienie i przepływy porównujemy z projektem oraz aktualnym obciążeniem instalacji.</p></div></li>
      <li class="reveal"><span>03</span><div><strong>Potwierdzaj trendem</strong><p>Spadek wydajności, wzrost różnicy ciśnień i jakość permeatu pokazują, kiedy reagować.</p></div></li>
    </ol>
  </div>
</section>"""
    return hero + editorial + stream + _related(c["related"]) + _cta()


def render_article(a):
    cat = cat_by_slug(a["category"])
    facts = [
        ("Kategoria", cat["title"] if cat else "Baza wiedzy"),
        ("Czas czytania", a["read"]),
        ("Dla kogo", a.get("audience", "Utrzymanie ruchu i decyzje techniczne.")),
    ]
    kicker = f"Baza wiedzy · {cat['title']}" if cat else "Baza wiedzy"
    hero = _hero(
        art_image(a), kicker, a["title"], a["lead"], facts,
        ("Umów konsultację", "/bezplatna-konsultacja/"),
        (f"Wróć do: {cat['title']}" if cat else "Wróć do bazy wiedzy",
         cat_path(cat) if cat else ROOT),
    )
    body = (
        '<section class="section knowledge-article reveal">'
        f'<div class="wrap narrow prose">{a["prose"]}</div></section>'
    )
    return hero + body + _related(a["related"]) + _faq(a["faq"]) + _cta()


# ================================================================== DANE: HUB
HUB = {
    "image": "/assets/blog/blog-baza-wiedzy.jpg",
    "kicker": "Baza wiedzy Kabi-Chemie",
    "h1": "Praktyczna wiedza o wodzie przemysłowej.",
    "lead": "Artykuły o kamieniu, korozji, biofilmie, membranach RO i parametrach wody. Konkretne przyczyny, pomiary i działania dla zakładu przemysłowego.",
    "facts": [
        ("Tematy", "Kotły, chłodnictwo, RO i korozja"),
        ("Dla kogo", "Technika i utrzymanie ruchu"),
        ("Cel", "Decyzje oparte na danych"),
    ],
}


# ================================================================== KATEGORIE
CATEGORIES = [
    {
        "slug": "kotly-parowe",
        "title": "Kotły parowe i para",
        "kicker": "Baza wiedzy · Kotły parowe",
        "h1": "Kotły parowe i para wodna - Artykuły eksperckie",
        "lead": "Wszystko o kondycjonowaniu wody w kotłach parowych, jak zapobiegać awariom, usuwać kamień i oszczędzać paliwo.",
        "hub_blurb": "kamień, kondensat, odsalanie i ochrona przed korozją.",
        "stream_title": "Kamień, para i stabilna praca kotłowni.",
        "image": "/assets/blog/blog-kotly-parowe.jpg",
        "facts": [
            ("Zakres", "Kamień, kondensat, odsalanie i ochrona kotła."),
            ("Dla kogo", "Kotłownie, utrzymanie ruchu i energetyka zakładowa."),
            ("Następny krok", "Umów konsultację techniczną."),
        ],
        "related": [
            ("Rozwiązania", "Kotły parowe", "/kotly-parowe/"),
            ("Baza wiedzy", "Parametry wody", "/baza-wiedzy/parametry-wody/"),
            ("Case study", "Kocioł parowy Fako", "/case-study/kociol-parowy-fako/"),
        ],
    },
    {
        "slug": "wieze-chlodnicze",
        "title": "Wieże chłodnicze i skraplacze",
        "kicker": "Baza wiedzy · Wieże chłodnicze",
        "h1": "Wieże chłodnicze i obiegi chłodzące - Baza wiedzy",
        "lead": "Optymalizacja pracy wież chłodniczych i obiegów, biofilm, biocydy i usuwanie kamienia ze skraplaczy.",
        "hub_blurb": "biofilm, biocydy, odkamienianie i zużycie wody.",
        "stream_title": "Czysty obieg i stabilne chłodzenie.",
        "image": "/assets/blog/blog-wieze-chlodnicze.jpg",
        "facts": [
            ("Zakres", "Biofilm, biocydy, odkamienianie i zużycie wody."),
            ("Dla kogo", "Chłodnictwo przemysłowe i utrzymanie ruchu."),
            ("Następny krok", "Umów konsultację techniczną."),
        ],
        "related": [
            ("Rozwiązania", "Układy chłodnicze", "/uklady-chlodnicze/"),
            ("Rozwiązania", "Skraplacze amoniakalne", "/uklady-chlodnicze/skraplacze-amoniakalne/"),
            ("Baza wiedzy", "Korozja i ochrona", "/baza-wiedzy/korozja/"),
        ],
    },
    {
        "slug": "korozja",
        "title": "Korozja i ochrona metalu",
        "kicker": "Baza wiedzy · Korozja i ochrona",
        "h1": "Korozja w instalacjach przemysłowych - Zapobieganie",
        "lead": "Jak chronić instalacje przemysłowe przed korozją, inhibitory, pasywacja stali i rodzaje korozji.",
        "hub_blurb": "inhibitory, pasywacja, rodzaje korozji i objawy w instalacji.",
        "stream_title": "Objawy, przyczyny i ochrona metalu.",
        "image": "/assets/blog/blog-korozja.jpg",
        "facts": [
            ("Zakres", "Inhibitory, pasywacja i rodzaje korozji."),
            ("Dla kogo", "Utrzymanie ruchu i służby techniczne."),
            ("Następny krok", "Umów konsultację techniczną."),
        ],
        "related": [
            ("Rozwiązania", "Ochrona antykorozyjna", "/ochrona-antykorozyjna/"),
            ("Rozwiązania", "Pasywacja stali", "/ochrona-antykorozyjna/pasywacja-stali/"),
            ("Baza wiedzy", "Kotły parowe", "/baza-wiedzy/kotly-parowe/"),
        ],
    },
    {
        "slug": "parametry-wody",
        "title": "Parametry wody i oszczędności",
        "kicker": "Baza wiedzy · Parametry wody",
        "h1": "Przewodność i pH wody przemysłowej - Poradniki",
        "lead": "Zrozum parametry wody w przemyśle, wpływ pH, twardości i przewodności na pracę kotłów i układów chłodniczych.",
        "hub_blurb": "pH, przewodność, twardość, TDS, ścieki i energia.",
        "stream_title": "Parametry, które decydują o kosztach.",
        "image": "/assets/blog/blog-parametry-wody.jpg",
        "facts": [
            ("Zakres", "pH, przewodność, twardość, TDS i odsalanie."),
            ("Dla kogo", "Technolodzy i utrzymanie ruchu."),
            ("Następny krok", "Umów analizę wody."),
        ],
        "related": [
            ("Usługi", "Analiza wody", "/uslugi/analiza-wody/"),
            ("Rozwiązania", "Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
            ("Baza wiedzy", "Kotły parowe", "/baza-wiedzy/kotly-parowe/"),
        ],
    },
    {
        "slug": "membrany-ro",
        "title": "Membrany RO",
        "kicker": "Baza wiedzy · Membrany RO",
        "h1": "Membrany RO pod kontrolą.",
        "lead": "Jak chronić membrany przed osadem i foulingiem, utrzymać stabilny odzysk oraz planować CIP na podstawie danych z instalacji.",
        "hub_blurb": "antyskalanty, fouling, płukanie i ochrona wydajności.",
        "stream_title": "Ochrona membran i stabilny odzysk.",
        "image": "/assets/blog/blog-membrany-ro-v2.webp",
        "facts": [
            ("Zakres", "Antyskalanty, fouling, płukanie i wydajność."),
            ("Dla kogo", "Operatorzy stacji RO i utrzymanie ruchu."),
            ("Następny krok", "Umów konsultację techniczną."),
        ],
        "related": [
            ("Rozwiązania", "Membrany RO", "/membrany-ro/"),
            ("Usługi", "Analiza wody", "/uslugi/analiza-wody/"),
            ("Baza wiedzy", "Parametry wody", "/baza-wiedzy/parametry-wody/"),
        ],
    },
]


# ================================================================== WPISY
ARTICLES = [
    {
        "slug": "kamien-kotlowy",
        "category": "kotly-parowe",
        "short": "Kamień kotłowy",
        "title": "Co to jest kamień kotłowy i dlaczego niszczy kotły parowe?",
        "excerpt": "mechanizm powstawania kamienia i jego wpływ na koszty pracy kotła.",
        "lead": "Kamień kotłowy to osad soli twardości na gorących powierzchniach kotła. Działa jak izolator, podnosi zużycie paliwa i grozi przegrzaniem rur.",
        "read": "8 min",
        "audience": "Utrzymanie ruchu i decyzje techniczne.",
        "feature_stats": [
            ("+10%", "więcej paliwa już przy 1 mm kamienia"),
            ("3 → 12 mies.", "dłuższy cykl między czyszczeniami (Fako)"),
        ],
        "prose": (
            "<h2>Jak powstaje kamień kotłowy?</h2>"
            "<p>Podgrzewana woda traci zdolność utrzymania rozpuszczonych soli wapnia i magnezu. "
            "Wytrącają się one na najgorętszych powierzchniach, tworząc twardą skorupę.</p>"
            "<h2>Jak kamień wpływa na rachunki za paliwo?</h2>"
            "<p>Już <strong>1 mm kamienia</strong> może zwiększyć zużycie paliwa o około 10%, "
            "bo ciepło trudniej przenika do wody.</p>"
            "<h2>Jak usunąć kamień kotłowy?</h2>"
            "<ul><li>Chemiczne odkamienianie dobranym preparatem</li>"
            "<li>Płukanie i pasywacja powierzchni</li>"
            "<li>Wdrożenie kondycjonowania, by kamień nie wracał</li></ul>"
            "<p class=\"note\">Information gain: w realizacji Fako po wdrożeniu programu KCAQUA "
            "cykl czyszczenia wydłużył się z 3 do 12 miesięcy (dane przykładowe).</p>"
        ),
        "faq": [
            ("Jak często należy odkamieniać kocioł?",
             "Zależy od jakości wody, obciążenia i historii osadów. Przy prawidłowym kondycjonowaniu potrzeba czyszczeń wyraźnie maleje."),
            ("Czy można kondycjonować wodę bez wyłączania kotła?",
             "Tak, samo kondycjonowanie prowadzimy w trakcie pracy. Odkamienianie planujemy zależnie od stanu układu."),
            ("Po czym poznać, że w kotle narasta kamień?",
             "Typowe objawy to rosnące zużycie paliwa, gorsza wymiana ciepła, częstsze alarmy, osady w wodzie i problemy z utrzymaniem stabilnych parametrów."),
            ("Czy 1 mm kamienia naprawdę ma znaczenie?",
             "Tak. Nawet cienka warstwa osadu działa jak izolacja cieplna. Kocioł musi zużyć więcej paliwa, aby przekazać tę samą ilość energii do wody."),
            ("Jak zapobiec powrotowi kamienia po czyszczeniu?",
             "Po odkamienianiu warto wdrożyć stałą kontrolę twardości, przewodności i pH oraz dobrać program KCAQUA do pracy konkretnej kotłowni."),
        ],
        "related": [
            ("Rozwiązania", "Odkamienianie kotłów parowych", "/kotly-parowe/odkamienianie/"),
            ("Rozwiązania", "Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
            ("Case study", "Kocioł parowy Fako", "/case-study/kociol-parowy-fako/"),
        ],
    },
    {
        "slug": "biofilm-w-ukladzie-chlodniczym",
        "category": "wieze-chlodnicze",
        "short": "Biofilm w układzie chłodniczym",
        "title": "Biofilm w układzie chłodniczym: jak rozpoznać i usunąć osady?",
        "excerpt": "jak rozpoznać problem, zanim spadnie sprawność skraplacza.",
        "lead": "Biofilm to warstwa mikroorganizmów na powierzchniach układu chłodniczego. Pogarsza wymianę ciepła, sprzyja korozji i bywa siedliskiem bakterii.",
        "read": "7 min",
        "audience": "Utrzymanie ruchu i chłodnictwo przemysłowe.",
        "prose": (
            "<h2>Dlaczego biofilm jest groźny?</h2>"
            "<p>Biofilm izoluje powierzchnie wymiany ciepła i chroni mikroorganizmy przed działaniem chemii. "
            "Może też sprzyjać rozwojowi bakterii Legionella.</p>"
            "<h2>Jak usunąć i kontrolować biofilm?</h2>"
            "<ul><li>Dozowanie biocydów (np. w ramach programu KCAQUA 305)</li>"
            "<li>Kontrola parametrów obiegu i przewodności</li>"
            "<li>Okresowe czyszczenie układu</li></ul>"
        ),
        "faq": [
            ("Jak chronić wieżę przed Legionellą?",
             "Podstawą jest kontrola biofilmu, właściwy biocyd, regularny monitoring wody i utrzymanie czystości powierzchni kontaktu z wodą."),
            ("Czy sam biocyd wystarczy do usunięcia biofilmu?",
             "Nie zawsze. Biofilm może chronić mikroorganizmy przed chemią, dlatego często potrzebna jest korekta programu, czyszczenie i kontrola parametrów obiegu."),
            ("Jakie objawy wskazują na biofilm w układzie chłodniczym?",
             "Najczęściej widać spadek wydajności chłodzenia, śliski osad, wzrost zużycia wody, nieprzyjemny zapach i większą podatność instalacji na korozję."),
            ("Czy biofilm wpływa na koszty energii?",
             "Tak. Warstwa biologiczna pogarsza wymianę ciepła, więc układ musi pracować ciężej, aby utrzymać wymaganą temperaturę procesu."),
            ("Jak często trzeba kontrolować wodę w wieży chłodniczej?",
             "Częstotliwość zależy od obciążenia i jakości wody. W praktyce warto kontrolować przewodność, pH, biologię i skuteczność programu chemicznego w stałym harmonogramie."),
        ],
        "related": [
            ("Rozwiązania", "Ochrona wież chłodniczych", "/uklady-chlodnicze/ochrona-wiez-chlodniczych/"),
            ("Rozwiązania", "Odkamienianie układów chłodniczych", "/uklady-chlodnicze/odkamienianie/"),
            ("Baza wiedzy", "Korozja i ochrona", "/baza-wiedzy/korozja/"),
        ],
    },
    {
        "slug": "antyskalant-ro",
        "category": "membrany-ro",
        "short": "Antyskalant do membran RO",
        "title": "Antyskalant do membran RO: kiedy naprawdę chroni membranę?",
        "excerpt": "kiedy realnie chroni membranę, a kiedy maskuje problem z jakością wody.",
        "lead": "Antyskalant to preparat zapobiegający wytrącaniu soli na membranach odwróconej osmozy. Chroni membrany przed kamieniem i wydłuża ich żywotność.",
        "read": "6 min",
        "audience": "Operatorzy stacji RO i utrzymanie ruchu.",
        "prose": (
            "<h2>Jak działa antyskalant?</h2>"
            "<p>Antyskalant utrzymuje sole twardości w roztworze, zapobiegając ich krystalizacji "
            "na powierzchni membrany i spadkowi wydajności stacji RO.</p>"
            "<h2>Dlaczego chlor i chlorki są groźne dla membran?</h2>"
            "<p>Degradują strukturę membrany. Dlatego ważna jest ich kontrola, "
            "nasz preparat potrafi wiązać te gazy.</p>"
        ),
        "faq": [
            ("Jak dobrać antyskalant do mojej wody?",
             "Na podstawie analizy wody surowej, odzysku instalacji RO i parametrów pracy membran. Najlepiej zacząć od badania wody."),
            ("Po czym poznać, że membrany RO są zagrożone osadem?",
             "Sygnałem jest spadek wydajności, wzrost różnicy ciśnień, pogorszenie jakości permeatu i częstsza potrzeba płukania chemicznego."),
            ("Czy antyskalant zastępuje prawidłową filtrację wstępną?",
             "Nie. Antyskalant chroni przed wytrącaniem soli, ale filtracja, kontrola żelaza, chloru i zawiesiny nadal są kluczowe dla żywotności membran."),
            ("Jak często trzeba kontrolować dawkę antyskalantu?",
             "Dawkę warto weryfikować przy zmianie jakości wody, odzysku, przepływu lub ciśnienia. Stała kontrola ogranicza ryzyko przewymiarowania i niedozowania."),
            ("Czy pomagacie dobrać chemię do istniejącej stacji RO?",
             "Tak. Analizujemy wodę, parametry pracy i historię awarii. Na tej podstawie dobieramy antyskalant oraz zalecenia dla obsługi stacji."),
        ],
        "related": [
            ("Rozwiązania", "Membrany RO", "/membrany-ro/"),
            ("Usługi", "Analiza wody", "/uslugi/analiza-wody/"),
            ("Baza wiedzy", "Parametry wody", "/baza-wiedzy/parametry-wody/"),
        ],
    },
]


def install_knowledge_pages(pages, custom, short):
    """Moduł jest właścicielem całej przestrzeni /baza-wiedzy/.

    Usuwa wcześniejsze (statyczne) definicje z tej przestrzeni, a następnie
    generuje hub, kategorie i wpisy z danych. `short` (C.SHORT) uzupełniamy
    o etykiety do breadcrumbów.
    """
    valid = {ROOT} | {cat_path(c) for c in CATEGORIES} | {art_path(a) for a in ARTICLES}
    for p in [p for p in pages if p.startswith(ROOT) and p not in valid]:
        del pages[p]

    pages[ROOT] = {
        "body_class": BODY_CLASS,
        "sections": [custom(render_hub())],
    }
    for c in CATEGORIES:
        path = cat_path(c)
        pages[path] = {
            "title": c["h1"],
            "meta": c["lead"],
            "h1": c["h1"],
            "og_image": c["image"],
            "body_class": f"{BODY_CLASS} knowledge-category-page knowledge-category--{c['slug']}",
            "sections": [custom(render_category(c))],
        }
        short[path] = c["title"]
    for a in ARTICLES:
        path = art_path(a)
        pages[path] = {
            "title": a["title"],
            "meta": a["lead"],
            "h1": a["title"],
            "og_type": "article",
            "og_image": art_image(a),
            "body_class": BODY_CLASS,
            "jsonld": [_faq_schema(a["faq"])],
            "sections": [custom(render_article(a))],
        }
        short[path] = a["short"]
