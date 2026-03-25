#!/usr/bin/env python3
"""Generate all 6 Flaney Associates blog article PDFs."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)

PRIMARY = HexColor("#1a3a5c")
ACCENT = HexColor("#2d8cf0")
DARK = HexColor("#0f2740")
LIGHT_BG = HexColor("#f7f9fc")
TEXT_COLOR = HexColor("#333333")
MUTED = HexColor("#666666")
WHITE = HexColor("#ffffff")

def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ArticleTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=PRIMARY,
        spaceAfter=6,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        name='Subtitle',
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=MUTED,
        spaceAfter=20,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        name='CategoryTag',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=ACCENT,
        spaceAfter=10,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        name='SectionHead',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=24,
        spaceAfter=10,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        name='SubHead',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=DARK,
        spaceBefore=16,
        spaceAfter=8,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        name='BodyText2',
        fontName='Helvetica',
        fontSize=11,
        leading=17,
        textColor=TEXT_COLOR,
        spaceAfter=10,
        alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        name='BulletItem',
        fontName='Helvetica',
        fontSize=11,
        leading=17,
        textColor=TEXT_COLOR,
        spaceAfter=6,
        leftIndent=24,
        bulletIndent=12,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        name='Callout',
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=18,
        textColor=ACCENT,
        spaceBefore=14,
        spaceAfter=14,
        leftIndent=20,
        rightIndent=20,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        name='AuthorContact',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name='FooterStyle',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=MUTED,
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name='MetaInfo',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=MUTED,
        spaceAfter=4,
        alignment=TA_LEFT
    ))
    return styles


def add_header_block(story, styles, category, title, subtitle, date, read_time):
    story.append(Paragraph(category.upper(), styles['CategoryTag']))
    story.append(Paragraph(title, styles['ArticleTitle']))
    story.append(Paragraph(subtitle, styles['Subtitle']))
    story.append(Paragraph(f"By Joshua U. Otaigbe, PhD  |  {date}  |  {read_time}", styles['MetaInfo']))
    story.append(Paragraph("Flaney Associates  |  Materials Engineering &amp; Innovation", styles['MetaInfo']))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=16))


def add_contact_footer(story, styles):
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#e2e8f0"), spaceBefore=10, spaceAfter=16))
    story.append(Paragraph(
        "For more information or if you have any questions, please contact the author:",
        styles['AuthorContact']
    ))
    story.append(Paragraph(
        "<b>Joshua U. Otaigbe, PhD</b>",
        styles['AuthorContact']
    ))
    story.append(Paragraph(
        "Founder &amp; Principal Consultant, Flaney Associates",
        styles['AuthorContact']
    ))
    story.append(Paragraph(
        "Email: info@flaneyassociates.com  |  Web: flaneyassociates.com",
        styles['AuthorContact']
    ))
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="40%", thickness=1, color=ACCENT, spaceBefore=4, spaceAfter=12))
    story.append(Paragraph(
        "Schedule a free consultation at flaneyassociates.com/contact",
        ParagraphStyle('cta_link', fontName='Helvetica-Bold', fontSize=11, leading=15,
                       textColor=ACCENT, alignment=TA_CENTER, spaceAfter=8)
    ))
    story.append(Paragraph(
        "\u00a9 2026 Flaney Associates. All rights reserved. This article is provided for informational purposes only.",
        styles['FooterStyle']
    ))


def build_pdf(filename, build_func):
    path = f"/Users/otaigbe2013/Claude Coding/Flaney_Associates/articles/{filename}"
    doc = SimpleDocTemplate(
        path,
        pagesize=letter,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=0.85*inch,
        rightMargin=0.85*inch,
        title="Flaney Associates",
        author="Joshua U. Otaigbe"
    )
    styles = get_styles()
    story = []
    build_func(story, styles)
    add_contact_footer(story, styles)
    doc.build(story)
    print(f"  Created: {path}")


# ─────────────────────────────────────────────────────────
# ARTICLE 1: AEROSPACE
# ─────────────────────────────────────────────────────────
def article_aerospace(story, styles):
    add_header_block(story, styles,
        "Aerospace & Defense",
        "Next-Gen Composite Materials: How Carbon Fiber\nThermoplastics Are Reshaping Aircraft Design",
        "A plain-language guide to the materials revolution making aircraft lighter, stronger, and more fuel-efficient.",
        "March 12, 2026", "6 min read"
    )

    story.append(Paragraph("Introduction: Why Aircraft Materials Matter to Everyone", styles['SectionHead']))
    story.append(Paragraph(
        "Every time you board a commercial flight, you are trusting your safety to the materials that make up the aircraft. "
        "For decades, aluminum has been the backbone of aviation. It is relatively light, strong, and well understood by engineers. "
        "But the aerospace industry is in the middle of a quiet revolution. A new generation of composite materials, specifically "
        "carbon fiber-reinforced thermoplastics, is changing the way aircraft are designed, built, and maintained. These materials "
        "are not just incremental improvements. They represent a fundamental shift in what is possible in flight.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "For passengers, this revolution means safer, more fuel-efficient flights. For airlines, it means lower operating costs. "
        "For the planet, it means significantly reduced carbon emissions. This article explains what these new materials are, "
        "why they matter, and what the future of aircraft design looks like.",
        styles['BodyText2']
    ))

    story.append(Paragraph("What Are Carbon Fiber Thermoplastics?", styles['SectionHead']))
    story.append(Paragraph(
        "To understand this innovation, it helps to know a little about how composite materials work. A composite is simply a "
        "material made from two or more different substances that, when combined, create something stronger or lighter than either "
        "one alone. Think of it like reinforced concrete: the concrete provides bulk and compression strength, while the steel rebar "
        "inside provides tensile strength. Together, they outperform either material on its own.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Carbon fiber composites work on the same principle. Extremely thin strands of carbon, each one about ten times thinner than "
        "a human hair, are woven together and then embedded in a plastic matrix that holds them in place. The carbon fibers provide "
        "remarkable strength and stiffness, while the plastic matrix gives the material its shape and protects the fibers.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "The key innovation here is the type of plastic used. Traditional aerospace composites use thermoset plastics, which harden "
        "permanently when heated during manufacturing, like an egg that cannot be uncooked. Thermoplastic composites, on the other hand, "
        "use plastics that can be softened by heat and reshaped multiple times, more like candle wax. This single difference opens up "
        "enormous advantages in manufacturing speed, repairability, and recyclability.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Weight Advantage: Why Every Pound Matters", styles['SectionHead']))
    story.append(Paragraph(
        "Weight is the single most important factor in aircraft economics. Every extra pound of structural weight means more fuel "
        "burned on every flight for the entire life of the aircraft. Industry estimates suggest that removing just one pound from "
        "an aircraft saves an airline roughly $10,000 to $30,000 in fuel costs over the plane's lifetime.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Carbon fiber thermoplastics offer weight savings of 20 to 40 percent compared to the aluminum parts they replace. On a "
        "large commercial aircraft, this can translate to thousands of pounds of weight reduction. The Boeing 787 Dreamliner, for "
        "example, uses about 50 percent composite materials by weight, contributing to fuel efficiency improvements of roughly 20 "
        "percent over comparable older aircraft.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"The shift to thermoplastic composites is not just about making lighter parts. It is about reimagining how we build aircraft entirely."',
        styles['Callout']
    ))

    story.append(Paragraph("Faster Manufacturing, Lower Costs", styles['SectionHead']))
    story.append(Paragraph(
        "One of the biggest drawbacks of traditional thermoset composites is how long they take to manufacture. A thermoset part "
        "might need to cure in a massive, expensive oven called an autoclave for hours at high temperature and pressure. "
        "Thermoplastic composites can be formed in minutes rather than hours because they do not need a chemical curing reaction. "
        "They simply need to be heated, shaped, and cooled.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "This speed advantage has enormous implications for production rates. As airlines around the world order more fuel-efficient "
        "aircraft, manufacturers need to build them faster. Thermoplastic processing techniques like stamp forming and automated tape "
        "laying can produce structural components at rates that would be impossible with traditional composites.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Key advantages of thermoplastic manufacturing:", styles['SubHead']))
    for bullet in [
        "Production cycle times reduced from hours to minutes",
        "Parts can be welded together, eliminating thousands of fasteners",
        "Scrap material can be remelted and reused, reducing waste",
        "Lower energy consumption during manufacturing",
        "Easier to automate, improving consistency and quality"
    ]:
        story.append(Paragraph(f"\u2022  {bullet}", styles['BulletItem']))

    story.append(Paragraph("Meeting Safety Standards", styles['SectionHead']))
    story.append(Paragraph(
        "No material enters an aircraft without rigorous testing and certification. The Federal Aviation Administration and its "
        "international counterparts require extensive proof that any new material can withstand the extreme conditions of flight, "
        "including temperature swings from scorching ground heat to minus 60 degrees at cruising altitude, constant vibration, "
        "lightning strikes, bird impacts, and decades of repeated pressurization cycles.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Carbon fiber thermoplastics have been meeting these standards with impressive results. Their damage tolerance, meaning "
        "their ability to absorb an impact without catastrophic failure, is actually superior to many thermoset composites. "
        "When a thermoset part is damaged, the damage often spreads invisibly beneath the surface. Thermoplastic parts tend to "
        "show damage more visibly and contain it more effectively, making inspection and repair more straightforward.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Sustainability Factor", styles['SectionHead']))
    story.append(Paragraph(
        "Aviation accounts for roughly 2.5 percent of global carbon dioxide emissions, a number the industry is working hard to reduce. "
        "Lighter aircraft burn less fuel, which directly reduces emissions. But thermoplastic composites offer an additional sustainability "
        "benefit: recyclability. Unlike thermoset composites, which are extremely difficult to recycle and typically end up in landfills, "
        "thermoplastic composites can be melted down and reformed into new parts or other products at the end of their service life.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "This cradle-to-cradle approach to aircraft materials aligns with the industry's ambitious sustainability goals. "
        "The International Air Transport Association has committed to achieving net-zero carbon emissions by 2050, and advanced materials "
        "are a critical part of reaching that target.",
        styles['BodyText2']
    ))

    story.append(Paragraph("What This Means for the Future", styles['SectionHead']))
    story.append(Paragraph(
        "We are still in the early stages of this materials transition. Today, thermoplastic composites are being used for secondary "
        "structures like brackets, clips, and interior panels. But the technology is advancing rapidly toward primary structural "
        "applications, including fuselage sections and wing components. Several major aircraft programs currently in development are "
        "expected to feature significantly higher thermoplastic content than any aircraft flying today.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "For manufacturers and their supply chains, the message is clear: the companies that invest in thermoplastic composite "
        "capabilities now will be best positioned to win contracts on the next generation of aircraft programs. Those that wait may "
        "find themselves playing catch-up in an increasingly competitive market.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we help aerospace companies navigate this transition, from material selection and testing strategy "
        "to process optimization and certification support. Whether you are evaluating thermoplastic composites for the first time or "
        "looking to scale up an existing program, our team brings the deep materials expertise you need to make confident decisions.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 2: AUTOMOTIVE
# ─────────────────────────────────────────────────────────
def article_automotive(story, styles):
    add_header_block(story, styles,
        "Automotive",
        "The Lightweighting Imperative: How EV Manufacturers\nAre Cutting Vehicle Mass by 15%",
        "Why your next electric car will be built from a surprising mix of materials, and what it means for range, safety, and cost.",
        "February 28, 2026", "7 min read"
    )

    story.append(Paragraph("Introduction: The Range Anxiety Problem", styles['SectionHead']))
    story.append(Paragraph(
        "If you have ever considered buying an electric vehicle, chances are you have thought about range. How far can it go on a "
        "single charge? Will I make it to my destination? This concern, commonly known as range anxiety, remains one of the biggest "
        "barriers to widespread EV adoption. While battery technology continues to improve, there is another powerful lever that "
        "automakers are pulling to extend driving range: making the car itself lighter.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "The relationship between vehicle weight and range is straightforward. A lighter vehicle requires less energy to move, which "
        "means the same battery can take you farther. Industry data shows that reducing a vehicle's weight by 10 percent can improve "
        "its range by 6 to 8 percent. For an EV with a 300-mile range, that translates to an extra 18 to 24 miles per charge, "
        "achieved without adding a single extra battery cell.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Multi-Material Revolution", styles['SectionHead']))
    story.append(Paragraph(
        "Traditional cars were built almost entirely from steel. It is strong, inexpensive, and easy to work with. But steel is heavy. "
        "Today's most advanced EVs use what engineers call a multi-material strategy, combining several different materials throughout "
        "the vehicle, each chosen for the specific job it needs to do.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Think of it like building a house. You would not use the same material for the foundation, the walls, the roof, and the "
        "windows. Each part of the structure has different requirements, and using the right material in the right place gives you "
        "the best combination of strength, weight, and cost. Modern EVs work the same way.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Here is how different materials are being deployed:", styles['SubHead']))

    # Material table
    table_data = [
        ["Material", "Where It's Used", "Why It's Chosen"],
        ["Advanced High-Strength Steel", "Safety cage, structural frame", "Exceptional crash protection at moderate weight"],
        ["Aluminum Alloys", "Body panels, doors, hood, suspension", "40% lighter than steel with good formability"],
        ["Carbon Fiber Composites", "Roof panels, battery enclosures", "Extremely light and stiff for premium applications"],
        ["Engineering Polymers", "Interior structures, brackets, trim", "Very light, design flexibility, noise reduction"],
        ["Magnesium Alloys", "Instrument panels, seat frames", "Lightest structural metal, 75% lighter than steel"],
    ]
    t = Table(table_data, colWidths=[1.6*inch, 1.9*inch, 2.7*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 13),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]))
    story.append(Spacer(1, 10))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Real-World Results: What the Numbers Show", styles['SectionHead']))
    story.append(Paragraph(
        "The results of multi-material lightweighting are already visible in production vehicles. Leading EV manufacturers have "
        "achieved weight reductions of 10 to 15 percent compared to equivalent vehicles built with conventional materials. "
        "Some specific examples are striking.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Aluminum-intensive body structures have reduced body-in-white weight by up to 40 percent in some luxury EVs. Composite "
        "battery enclosures are saving 25 to 30 percent weight compared to steel equivalents while providing superior thermal "
        "protection. Even seemingly small changes, like replacing steel seat frames with magnesium, can save 5 to 8 pounds per seat, "
        "which adds up to 20 to 32 pounds across a four-seat vehicle.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"Every pound you remove from the vehicle is a pound you do not need to carry for 200,000 miles. The cumulative energy savings are enormous."',
        styles['Callout']
    ))

    story.append(Paragraph("The Hidden Challenge: When Materials Meet", styles['SectionHead']))
    story.append(Paragraph(
        "Using multiple materials in a single vehicle creates engineering challenges that did not exist when everything was steel. "
        "The most significant is galvanic corrosion. When two different metals are in direct contact in the presence of moisture, "
        "an electrochemical reaction can cause one of them to corrode rapidly. Joining aluminum to steel, for example, requires "
        "careful engineering to prevent this type of degradation.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Automakers address this through several strategies: adhesive bonding that separates dissimilar metals, specialized coatings "
        "and sealants, mechanical fasteners with insulating barriers, and clever design that minimizes direct metal-to-metal contact. "
        "Getting these joining techniques right is critical. A poorly designed joint between aluminum and steel can fail in just a "
        "few years, turning a lightweight design advantage into a costly warranty problem.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Crashworthiness: Lighter Does Not Mean Less Safe", styles['SectionHead']))
    story.append(Paragraph(
        "One common concern about lightweighting is safety. If the car is lighter, is it less protective in a crash? The answer, "
        "perhaps surprisingly, is no. Modern multi-material designs often perform better in crash tests than their heavier predecessors. "
        "The key is using the right material in the right location.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Advanced high-strength steels used in the passenger safety cage can absorb enormous amounts of energy during a collision. "
        "These steels are two to three times stronger than the mild steel used in older vehicles, so engineers can use thinner, "
        "lighter sheets while actually improving crash performance. Aluminum crumple zones at the front and rear of the vehicle are "
        "specifically designed to deform in a controlled manner, absorbing impact energy before it reaches the passenger compartment.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Cost Equation", styles['SectionHead']))
    story.append(Paragraph(
        "Advanced materials cost more than conventional steel. Aluminum costs roughly twice as much per pound, and carbon fiber "
        "can cost ten times as much. This is why the multi-material approach is so important. Rather than making the entire vehicle "
        "from expensive materials, engineers use premium materials only where the weight savings justify the cost.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "For EVs, the cost equation is different than for conventional vehicles. Because batteries are the most expensive component "
        "in an EV, any weight reduction that allows a smaller battery pack can actually save money overall. A lighter vehicle that "
        "achieves the same range with a smaller battery can offset the higher cost of advanced materials. This is why lightweighting "
        "is not just an engineering exercise but a financial strategy.",
        styles['BodyText2']
    ))

    story.append(Paragraph("What This Means for the Industry", styles['SectionHead']))
    story.append(Paragraph(
        "The transition to multi-material vehicle architectures is accelerating. As EV production scales up and competition "
        "intensifies, the automakers that master lightweight design will have a significant advantage in range, performance, "
        "and cost. For suppliers, this creates both opportunities and challenges. Companies that can provide advanced materials, "
        "innovative joining solutions, and robust failure analysis capabilities will find growing demand for their expertise.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we work with automotive manufacturers and their suppliers on every aspect of the lightweighting "
        "journey. From material selection and testing to failure analysis and process optimization, our team helps you make the "
        "right materials decisions for your specific application and production requirements.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 3: ENERGY & OIL/GAS
# ─────────────────────────────────────────────────────────
def article_energy(story, styles):
    add_header_block(story, styles,
        "Energy & Oil/Gas",
        "Corrosion-Resistant Alloys for Deepwater Pipelines:\nSelecting Materials That Survive 30+ Years Subsea",
        "A practical guide to understanding why pipeline materials matter and how the right choices prevent billion-dollar failures.",
        "February 10, 2026", "8 min read"
    )

    story.append(Paragraph("Introduction: The Invisible Threat Beneath the Ocean", styles['SectionHead']))
    story.append(Paragraph(
        "Miles beneath the surface of the ocean, in complete darkness and under crushing pressure, a vast network of pipelines "
        "carries oil and natural gas from the seabed to platforms and processing facilities. These pipelines are engineering marvels, "
        "designed to operate continuously for decades in one of the most hostile environments on Earth. And their greatest enemy is "
        "not the pressure or the cold. It is corrosion.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Corrosion, the gradual destruction of metal by chemical reactions with its environment, costs the global oil and gas "
        "industry an estimated $1.3 billion annually in pipeline failures, repairs, and lost production. A single deepwater pipeline "
        "failure can cost hundreds of millions of dollars to repair and cause devastating environmental damage. The materials chosen "
        "for these pipelines are quite literally the thin line between safe operation and catastrophe.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Understanding Subsea Corrosion", styles['SectionHead']))
    story.append(Paragraph(
        "The ocean is an extraordinarily corrosive environment. Seawater contains dissolved salts, primarily sodium chloride, along "
        "with dissolved oxygen and other aggressive chemicals. When metals are exposed to this environment, they naturally want to "
        "return to their original ore state through corrosion reactions. But the challenge goes beyond simple seawater exposure.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "The fluids flowing inside deepwater pipelines often contain carbon dioxide, hydrogen sulfide, and chloride ions at high "
        "temperatures and pressures. This combination creates what corrosion engineers call a sour service environment, one of the "
        "most aggressive conditions any metal can face. The internal environment can be just as damaging as the external seawater, "
        "meaning pipeline materials must resist attack from both sides simultaneously.",
        styles['BodyText2']
    ))
    story.append(Paragraph("The main types of corrosion threatening subsea pipelines include:", styles['SubHead']))
    for bullet in [
        "Uniform corrosion: a gradual, even thinning of the pipe wall over time",
        "Pitting corrosion: localized, deep attacks that can penetrate the pipe wall rapidly",
        "Stress corrosion cracking: cracks that form under the combined action of stress and a corrosive environment",
        "Sulfide stress cracking: a particularly dangerous form of cracking caused by hydrogen sulfide",
        "Microbiologically influenced corrosion: attack accelerated by bacteria living on the pipe surface"
    ]:
        story.append(Paragraph(f"\u2022  {bullet}", styles['BulletItem']))

    story.append(Paragraph("The Materials Toolbox", styles['SectionHead']))
    story.append(Paragraph(
        "Engineers have several families of corrosion-resistant alloys (CRAs) to choose from, each with different strengths "
        "and cost profiles. The choice depends on the specific combination of temperature, pressure, fluid chemistry, and "
        "required service life for each project.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Duplex Stainless Steels", styles['SubHead']))
    story.append(Paragraph(
        "These steels get their name from their dual-phase microstructure, containing roughly equal parts of two different "
        "crystal structures called austenite and ferrite. This combination gives duplex steels excellent resistance to pitting "
        "and stress corrosion cracking, along with roughly twice the strength of standard stainless steels. They are the workhorse "
        "CRA for many subsea applications, offering a good balance of performance and cost.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Super Duplex Stainless Steels", styles['SubHead']))
    story.append(Paragraph(
        "For more aggressive environments, super duplex steels offer enhanced corrosion resistance through higher levels of chromium, "
        "molybdenum, and nitrogen. They can handle higher temperatures and more corrosive fluid chemistries than standard duplex grades. "
        "While more expensive, they are significantly cheaper than nickel-based alternatives.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Nickel-Based Superalloys", styles['SubHead']))
    story.append(Paragraph(
        "At the extreme end of the performance spectrum are nickel-based alloys. These materials can withstand the most severe "
        "combinations of temperature, pressure, and corrosive chemistry found in deepwater production. They are the most expensive "
        "option but are essential for the harshest service conditions where no other material will survive.",
        styles['BodyText2']
    ))

    story.append(Paragraph(
        '"Choosing the right alloy is not just an engineering decision. It is a risk management decision with implications measured in billions of dollars."',
        styles['Callout']
    ))

    story.append(Paragraph("Testing for a 30-Year Life", styles['SectionHead']))
    story.append(Paragraph(
        "When a pipeline is designed for a 30-year service life, you cannot simply install it and hope for the best. Extensive "
        "testing is required to validate that the chosen material will perform as expected over decades of continuous service. "
        "This testing program typically includes laboratory corrosion testing in simulated service environments, full-scale "
        "pressure testing of welded pipe sections, fracture toughness testing at service temperatures, and hydrogen embrittlement "
        "testing for sour service applications.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Perhaps most importantly, the welds that join pipe sections together must be tested just as rigorously as the base metal. "
        "Welds are often the weakest link in a pipeline, because the welding process changes the metal's microstructure and can "
        "introduce defects. Ensuring that weld procedures produce joints with the same corrosion resistance as the parent material "
        "is one of the most critical steps in pipeline engineering.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Economics of Material Selection", styles['SectionHead']))
    story.append(Paragraph(
        "CRAs cost significantly more than conventional carbon steel. A super duplex stainless steel pipeline might cost three to "
        "five times more than a carbon steel alternative on a per-foot basis. Nickel alloys can cost ten times more. These numbers "
        "can make CRAs seem prohibitively expensive, but the full economic picture tells a different story.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "A carbon steel pipeline in a corrosive environment requires extensive corrosion management throughout its life: chemical "
        "inhibitor injection systems, regular inspection programs using intelligent pigs, and eventual repairs or replacement of "
        "corroded sections. These ongoing costs can easily exceed the upfront premium for CRAs over a 30-year life. More importantly, "
        "a single pipeline failure can cost hundreds of millions of dollars in repair costs, lost production, environmental cleanup, "
        "and regulatory penalties. The CRA premium is essentially an insurance policy against catastrophic failure.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Looking Ahead", styles['SectionHead']))
    story.append(Paragraph(
        "As the energy industry moves into ever deeper and more challenging environments, the demands on pipeline materials will "
        "only increase. Higher temperatures, higher pressures, and more corrosive fluid chemistries are pushing the boundaries of "
        "what current materials can handle. At the same time, the transition to hydrogen as an energy carrier is creating entirely "
        "new material challenges, since hydrogen can cause embrittlement and cracking in many conventional pipeline steels.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we help energy companies make material selection decisions that balance performance, cost, and "
        "risk. From initial feasibility studies through qualification testing and failure analysis, our team provides the materials "
        "expertise you need to build pipelines that last.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 4: BIOMEDICAL
# ─────────────────────────────────────────────────────────
def article_biomedical(story, styles):
    add_header_block(story, styles,
        "Biomedical",
        "Biocompatible Polymers for Implantable Devices:\nNavigating FDA Material Requirements in 2026",
        "What every medical device innovator needs to know about choosing materials that are safe for the human body and approvable by regulators.",
        "January 22, 2026", "7 min read"
    )

    story.append(Paragraph("Introduction: Materials That Live Inside Us", styles['SectionHead']))
    story.append(Paragraph(
        "Right now, millions of people around the world are living with medical devices implanted inside their bodies. Hip joints, "
        "knee replacements, spinal fusion cages, heart valves, dental implants, and pacemakers are just a few examples. Each of "
        "these devices must be made from materials that can coexist with living tissue, sometimes for decades, without causing harm. "
        "The stakes could not be higher. A material that triggers an adverse reaction inside the body can cause pain, infection, "
        "organ damage, or even death.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "This is why the selection of materials for implantable medical devices is one of the most demanding disciplines in all of "
        "engineering. It requires a deep understanding of both materials science and human biology, combined with a thorough knowledge "
        "of regulatory requirements. This article provides a plain-language overview of how biocompatible polymers are selected, "
        "tested, and approved for use in implantable devices.",
        styles['BodyText2']
    ))

    story.append(Paragraph("What Does Biocompatible Actually Mean?", styles['SectionHead']))
    story.append(Paragraph(
        "Biocompatibility is the ability of a material to perform its intended function within the body without causing an unacceptable "
        "adverse reaction. It is important to understand that biocompatibility is not a single property, like strength or hardness. "
        "It is a complex set of interactions between the material and the biological environment, and it depends heavily on how and "
        "where the material is used.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "A material that is perfectly biocompatible for a skin-contact application might be completely unsuitable for a blood-contact "
        "device. A polymer that works well as a temporary bone scaffold might fail as a permanent implant. Context is everything in "
        "biocompatibility, and this is a concept that regulators take very seriously.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Polymers Leading the Way", styles['SectionHead']))
    story.append(Paragraph("Several families of polymers have established strong track records in implantable device applications:", styles['BodyText2']))

    story.append(Paragraph("PEEK (Polyether Ether Ketone)", styles['SubHead']))
    story.append(Paragraph(
        "PEEK has become one of the most important polymers in orthopedic and spinal surgery. It is strong, stiff, and resistant to "
        "the body's chemical environment. Crucially, its mechanical properties are much closer to human bone than metal implants, which "
        "helps prevent a problem called stress shielding, where a too-rigid implant causes the surrounding bone to weaken over time. "
        "PEEK spinal fusion cages, for example, have become a standard of care in spine surgery.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Ultra-High Molecular Weight Polyethylene (UHMWPE)", styles['SubHead']))
    story.append(Paragraph(
        "This specialized form of polyethylene has been used in joint replacements for over 50 years. It serves as the bearing surface "
        "in hip and knee replacements, providing a low-friction, wear-resistant interface between the metal or ceramic components. "
        "Modern cross-linked versions of UHMWPE have dramatically reduced wear rates, extending the life of joint replacements and "
        "reducing the need for revision surgeries.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Bioresorbable Polymers", styles['SubHead']))
    story.append(Paragraph(
        "Perhaps the most exciting development in biomedical polymers is the emergence of materials that are designed to dissolve "
        "safely inside the body after they have served their purpose. Polymers like polylactic acid (PLA) and polyglycolic acid (PGA) "
        "can be used to create temporary scaffolds that support tissue healing and then gradually break down into harmless natural "
        "byproducts that the body absorbs. This eliminates the need for a second surgery to remove the device.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"The ideal implant material does not just avoid causing harm. It actively supports the body\'s natural healing processes."',
        styles['Callout']
    ))

    story.append(Paragraph("The FDA Approval Pathway", styles['SectionHead']))
    story.append(Paragraph(
        "In the United States, the Food and Drug Administration requires extensive evidence that a medical device material is safe "
        "and effective before it can be used in patients. The biocompatibility testing framework is defined by ISO 10993, an "
        "international standard that specifies a systematic approach to evaluating the biological effects of medical device materials.",
        styles['BodyText2']
    ))
    story.append(Paragraph("The required tests depend on the nature and duration of body contact, but typically include:", styles['BodyText2']))
    for bullet in [
        "Cytotoxicity testing: Does the material kill or damage cells?",
        "Sensitization testing: Does the material cause allergic reactions?",
        "Irritation testing: Does the material cause inflammation?",
        "Systemic toxicity: Does the material release harmful substances?",
        "Genotoxicity: Does the material damage DNA?",
        "Implantation testing: How does tissue respond to the implanted material?",
        "Hemocompatibility: How does the material interact with blood?",
    ]:
        story.append(Paragraph(f"\u2022  {bullet}", styles['BulletItem']))
    story.append(Paragraph(
        "For permanent implants, additional long-term testing is required, including chronic toxicity studies and carcinogenicity "
        "assessments. The entire testing program can take 12 to 24 months and cost hundreds of thousands of dollars. This is why "
        "making smart material choices early in the design process is so critical. Changing materials late in development can mean "
        "starting the testing program over from scratch.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Common Pitfalls in Material Selection", styles['SectionHead']))
    story.append(Paragraph(
        "In our consulting work, we frequently see medical device companies make material selection mistakes that could have been "
        "avoided with earlier expert input. The most common pitfalls include selecting a material based solely on mechanical properties "
        "without considering long-term biological interaction, underestimating the effects of sterilization on polymer properties, "
        "overlooking how the manufacturing process can alter material behavior, and failing to account for material degradation over "
        "the intended implant lifetime.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Each of these issues can delay regulatory approval by months or years and add significant cost to the development program. "
        "The most cost-effective approach is always to involve materials expertise from the very beginning of the design process.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Looking Ahead: The Future of Biomedical Polymers", styles['SectionHead']))
    story.append(Paragraph(
        "The field of biomedical polymers is advancing rapidly. Researchers are developing smart polymers that can respond to "
        "conditions inside the body, releasing drugs or changing their properties in response to temperature, pH, or other biological "
        "signals. Three-dimensional printing is enabling patient-specific implants tailored to individual anatomy. And new surface "
        "modification techniques are creating implants that actively promote tissue integration and resist bacterial colonization.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we help medical device companies navigate the complex intersection of materials science, "
        "biocompatibility, and regulatory requirements. From early-stage material screening through FDA submission support, "
        "our team provides the expertise you need to bring safe, effective implantable devices to market efficiently.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 5: CONSTRUCTION
# ─────────────────────────────────────────────────────────
def article_construction(story, styles):
    add_header_block(story, styles,
        "Construction",
        "Fiber-Reinforced Concrete: How Advanced Additives\nAre Extending Infrastructure Lifespan by Decades",
        "Why the concrete in tomorrow's bridges and buildings will be fundamentally different from what we use today, and why that matters for everyone.",
        "January 8, 2026", "5 min read"
    )

    story.append(Paragraph("Introduction: The Infrastructure Crisis Hiding in Plain Sight", styles['SectionHead']))
    story.append(Paragraph(
        "Drive across any bridge in America, and there is roughly a one-in-three chance that it has been classified as structurally "
        "deficient or in need of major repair. The American Society of Civil Engineers gives U.S. infrastructure an overall grade of "
        "C-minus, estimating that the country needs to invest $2.6 trillion over the next decade just to bring existing structures up "
        "to acceptable condition. At the heart of this crisis is a materials problem: conventional concrete, the most widely used "
        "building material on Earth, has a fundamental weakness. It cracks.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Cracking is not a defect in concrete. It is an inherent property. Concrete is exceptionally strong in compression, meaning "
        "it can support enormous loads pressing down on it. But it is weak in tension, meaning it cracks easily when pulled or bent. "
        "Steel reinforcing bars (rebar) have traditionally addressed this weakness, but rebar corrodes over time, especially when "
        "cracks allow water and road salt to reach the steel. This corrosion expands the rebar, creating more cracks, which allows "
        "more water in, accelerating the cycle of deterioration.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Fiber Solution", styles['SectionHead']))
    story.append(Paragraph(
        "Fiber-reinforced concrete (FRC) takes a different approach to the cracking problem. Instead of relying solely on large steel "
        "bars placed at specific locations, FRC distributes millions of tiny fibers throughout the entire concrete mixture. These fibers "
        "act like miniature reinforcing elements, bridging across cracks as they form and preventing them from growing into the large "
        "fissures that lead to structural failure.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "The concept is inspired by nature. Adobe bricks, one of humanity's oldest building materials, use straw fibers to prevent "
        "cracking. Modern FRC applies the same principle with engineered fibers that deliver dramatically better performance.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Types of fibers used in modern concrete:", styles['SubHead']))
    for bullet in [
        "Steel fibers: short, hooked or crimped steel wires that provide excellent crack resistance and structural strength",
        "Glass fibers: alkali-resistant glass strands used primarily in architectural panels and facades",
        "Synthetic fibers: polypropylene or nylon fibers that control early-age shrinkage cracking and improve fire resistance",
        "Carbon fibers: ultra-high-performance fibers for specialized applications requiring maximum strength and durability",
        "Natural fibers: plant-based fibers like cellulose being explored for sustainable construction applications"
    ]:
        story.append(Paragraph(f"\u2022  {bullet}", styles['BulletItem']))

    story.append(Paragraph("How Fiber Reinforcement Works", styles['SectionHead']))
    story.append(Paragraph(
        "When conventional concrete begins to crack under stress, the crack propagates freely through the material until it reaches "
        "a piece of rebar or the edge of the structure. In fiber-reinforced concrete, each crack encounters thousands of fibers "
        "bridging across its path. These fibers absorb energy and redistribute stress, slowing crack growth by up to 90 percent "
        "in some formulations.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "This does not mean FRC never cracks. It means that when cracks do form, they stay much smaller, often less than a tenth "
        "of a millimeter wide. Cracks this small are effectively self-sealing: natural mineral deposits from the concrete fill them "
        "in over time, a process engineers call autogenous healing. The result is a material that can partially repair itself, "
        "dramatically extending its useful life.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"Fiber-reinforced concrete does not just resist cracking. It fundamentally changes how concrete fails, turning a brittle material into one that bends before it breaks."',
        styles['Callout']
    ))

    story.append(Paragraph("Real-World Impact", styles['SectionHead']))
    story.append(Paragraph(
        "The performance benefits of FRC are translating into real cost savings on infrastructure projects around the world. Bridge "
        "decks made with fiber-reinforced concrete are lasting 50 to 75 years instead of the typical 25 to 30 years for conventional "
        "concrete. Industrial floors reinforced with steel fibers require 60 to 80 percent fewer joints, reducing maintenance costs "
        "and improving vehicle traffic flow. Tunnel linings made with FRC have shown dramatically improved fire resistance, a critical "
        "safety requirement after several high-profile tunnel fire disasters.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "The economic case is compelling. While fiber-reinforced concrete costs 10 to 20 percent more than conventional concrete per "
        "cubic yard, the total lifecycle cost is often 30 to 50 percent lower when you factor in reduced maintenance, fewer repairs, "
        "and extended service life. For infrastructure owners managing tight budgets, this long-term value proposition is increasingly "
        "persuasive.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Self-Healing Frontier", styles['SectionHead']))
    story.append(Paragraph(
        "Researchers are pushing the boundaries even further with self-healing concrete technologies. These advanced materials contain "
        "embedded capsules of healing agents, typically bacteria that produce limestone or chemical compounds that react with water "
        "to form mineral deposits. When a crack reaches one of these capsules, it breaks open, releasing the healing agent directly "
        "into the crack. The result is active crack repair without any human intervention.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "While self-healing concrete is still in the early stages of commercial adoption, field trials on bridges, parking structures, "
        "and water treatment facilities have shown promising results. The combination of fiber reinforcement to control crack width "
        "and self-healing agents to seal those cracks represents a new paradigm in durable construction.",
        styles['BodyText2']
    ))

    story.append(Paragraph("What This Means for Your Projects", styles['SectionHead']))
    story.append(Paragraph(
        "Whether you are designing a new bridge, renovating a commercial building, or specifying materials for an industrial facility, "
        "fiber-reinforced concrete deserves serious consideration. The technology is mature, widely available, and supported by decades "
        "of field performance data. The key is choosing the right fiber type, dosage, and concrete mix design for your specific application.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we help construction professionals and facility owners select and specify advanced concrete systems "
        "that deliver maximum durability and long-term value. From material testing and mix design optimization to structural integrity "
        "analysis and failure investigation, our team provides the expertise you need to build structures that last.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 6: CONSUMER PRODUCTS
# ─────────────────────────────────────────────────────────
def article_consumer(story, styles):
    add_header_block(story, styles,
        "Consumer Products",
        "Sustainable Packaging Materials: Moving Beyond\nSingle-Use Plastics Without Sacrificing Performance",
        "A practical look at the materials science behind the packaging revolution and how brands can make the switch successfully.",
        "December 15, 2025", "6 min read"
    )

    story.append(Paragraph("Introduction: The Plastic Problem Everyone Knows About", styles['SectionHead']))
    story.append(Paragraph(
        "Plastic packaging is everywhere. It wraps our food, protects our electronics, and lines our shipping boxes. It is cheap, "
        "lightweight, and remarkably effective at its job. It is also creating an environmental crisis that is impossible to ignore. "
        "An estimated 8 million tons of plastic waste enters the world's oceans every year, and only about 9 percent of all plastic "
        "ever produced has been recycled. The rest sits in landfills, floats in waterways, or breaks down into microplastics that "
        "have been found in everything from Arctic ice to human blood.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Consumers are demanding change, and brands are responding. Major companies have made public commitments to reduce plastic "
        "packaging, increase recycled content, and transition to sustainable alternatives. But making this switch is far more "
        "challenging than it might appear. The materials science behind packaging is complex, and getting it wrong can lead to "
        "product spoilage, customer complaints, and even safety issues.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Why Plastic Packaging Is So Hard to Replace", styles['SectionHead']))
    story.append(Paragraph(
        "To understand the challenge, it helps to appreciate what conventional plastic packaging actually does. A typical food "
        "packaging film is not just a simple wrapper. It is an engineered barrier system that simultaneously prevents oxygen from "
        "reaching the food and causing spoilage, keeps moisture in or out depending on the product, blocks light that can degrade "
        "nutrients and flavors, resists punctures and tears during shipping and handling, seals reliably on high-speed packaging "
        "machines, and remains food-safe throughout the product's shelf life.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Achieving all of these properties simultaneously, at a cost of pennies per package, is a remarkable engineering feat. "
        "Any sustainable alternative must match most or all of these capabilities to be commercially viable.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"The challenge is not finding alternatives to plastic. The challenge is finding alternatives that work as well as plastic in the real world."',
        styles['Callout']
    ))

    story.append(Paragraph("The Sustainable Materials Landscape", styles['SectionHead']))
    story.append(Paragraph(
        "The good news is that materials science has advanced significantly in recent years, and several promising sustainable "
        "packaging options are now commercially available or nearing market readiness.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Bio-Based Polymers", styles['SubHead']))
    story.append(Paragraph(
        "These plastics are made from renewable biological sources like corn starch, sugarcane, or cellulose rather than petroleum. "
        "Polylactic acid (PLA) is the most well-known example. It looks and feels like conventional plastic and can be processed "
        "on existing packaging equipment. However, PLA has limitations: it is not heat resistant, has poor barrier properties against "
        "moisture, and requires industrial composting facilities to biodegrade properly. Newer bio-based polymers like "
        "polyhydroxyalkanoates (PHAs) offer improved properties and can biodegrade in marine and soil environments, but they "
        "currently cost several times more than conventional plastics.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Recycled-Content Materials", styles['SubHead']))
    story.append(Paragraph(
        "Using recycled plastic to make new packaging is one of the most practical near-term solutions. Post-consumer recycled "
        "PET (rPET) is already widely used in beverage bottles, and the technology is expanding to other packaging formats. Advanced "
        "chemical recycling processes can break down mixed plastic waste into its basic building blocks, producing recycled material "
        "that is chemically identical to virgin plastic. This approach keeps plastic in the economy rather than in the environment, "
        "though it requires significant investment in collection and processing infrastructure.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Paper and Fiber-Based Solutions", styles['SubHead']))
    story.append(Paragraph(
        "Paper packaging is experiencing a renaissance, driven by advances in barrier coatings that allow paper to replace plastic "
        "in applications previously thought impossible. Modern paper packaging can incorporate water-based or mineral barrier coatings "
        "that provide the moisture and oxygen resistance needed for food packaging, while remaining recyclable in standard paper "
        "recycling streams. Molded fiber packaging, made from recycled paper pulp, is replacing expanded polystyrene for protective "
        "packaging and food service containers.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Compostable Films and Coatings", styles['SubHead']))
    story.append(Paragraph(
        "For applications where recycling is impractical, such as food-contaminated packaging or small flexible packets, compostable "
        "materials offer a promising end-of-life pathway. These materials are designed to break down completely in industrial or home "
        "composting systems, returning nutrients to the soil. The key challenge is ensuring that compostable packaging is clearly "
        "labeled and that adequate composting infrastructure exists in the communities where it is sold.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Testing: The Critical Step Most Brands Skip", styles['SectionHead']))
    story.append(Paragraph(
        "In our consulting work, we frequently encounter brands that have switched to sustainable packaging materials without "
        "adequate testing, only to face problems in the market. Common issues include shorter shelf life than expected, leading "
        "to increased food waste that actually worsens the environmental impact. Package failures during shipping, causing product "
        "damage and customer returns. Incompatibility with existing packaging machinery, requiring costly equipment modifications. "
        "Consumer confusion about disposal, with compostable packaging ending up in recycling bins and contaminating the recycling stream.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Rigorous testing before launch is essential. This includes accelerated shelf life studies, mechanical performance testing "
        "under realistic supply chain conditions, compatibility testing with packaging equipment, and consumer research on disposal behavior.",
        styles['BodyText2']
    ))

    story.append(Paragraph("A Practical Framework for Making the Switch", styles['SectionHead']))
    story.append(Paragraph("Based on our experience helping brands transition to sustainable packaging, we recommend a five-step approach:", styles['BodyText2']))
    for i, bullet in enumerate([
        "Audit your current packaging: Understand exactly what each material does and why it is there",
        "Identify the highest-impact opportunities: Focus first on the packaging formats that use the most material or are most visible to consumers",
        "Evaluate alternatives rigorously: Test sustainable options against the full range of performance requirements, not just environmental attributes",
        "Pilot before scaling: Run a limited market test to identify real-world issues before committing to a full rollout",
        "Communicate clearly: Help consumers understand what the new packaging is made from and how to dispose of it properly"
    ], 1):
        story.append(Paragraph(f"<b>{i}.</b>  {bullet}", styles['BulletItem']))

    story.append(Paragraph("The Business Case for Sustainable Packaging", styles['SectionHead']))
    story.append(Paragraph(
        "Beyond the environmental imperative, there is a growing business case for sustainable packaging. Consumer surveys "
        "consistently show that 60 to 70 percent of shoppers are willing to pay more for products in sustainable packaging. "
        "Retailers are increasingly requiring sustainability commitments from their suppliers. And regulatory pressure is mounting, "
        "with the European Union, Canada, and several U.S. states implementing extended producer responsibility laws that make "
        "brands financially responsible for the end-of-life management of their packaging.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we help consumer brands navigate the complex materials science behind sustainable packaging. "
        "From material evaluation and testing to supplier qualification and performance optimization, our team ensures that your "
        "packaging transition delivers both environmental benefits and commercial success.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# MAIN: BUILD ALL 6 PDFs
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating 6 Flaney Associates blog article PDFs...\n")
    articles = [
        ("aerospace-composite-materials.pdf", article_aerospace),
        ("automotive-lightweighting-ev.pdf", article_automotive),
        ("energy-corrosion-resistant-alloys.pdf", article_energy),
        ("biomedical-biocompatible-polymers.pdf", article_biomedical),
        ("construction-fiber-reinforced-concrete.pdf", article_construction),
        ("consumer-sustainable-packaging.pdf", article_consumer),
    ]
    for filename, func in articles:
        build_pdf(filename, func)
    print("\nAll 6 PDFs generated successfully!")
