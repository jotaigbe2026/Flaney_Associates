#!/usr/bin/env python3
"""Generate 6 NEW Flaney Associates blog article PDFs — Round 2."""

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
    story.append(Paragraph("<b>Joshua U. Otaigbe, PhD</b>", styles['AuthorContact']))
    story.append(Paragraph("Founder &amp; Principal Consultant, Flaney Associates", styles['AuthorContact']))
    story.append(Paragraph("Email: info@flaneyassociates.com  |  Web: flaneyassociates.com", styles['AuthorContact']))
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="40%", thickness=1, color=ACCENT, spaceBefore=4, spaceAfter=12))
    story.append(Paragraph(
        "Schedule a free consultation at flaneyassociates.com/contact",
        ParagraphStyle('cta_link', fontName='Helvetica-Bold', fontSize=11, leading=15,
                       textColor=ACCENT, alignment=TA_CENTER, spaceAfter=8)
    ))
    story.append(Paragraph(
        "© 2026 Flaney Associates. All rights reserved. This article is provided for informational purposes only.",
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
# ARTICLE 7: AEROSPACE — Additive Manufacturing
# ─────────────────────────────────────────────────────────
def article_aerospace_additive(story, styles):
    add_header_block(story, styles,
        "Aerospace & Defense",
        "Metal 3D Printing in Aerospace: How Additive\nManufacturing Is Reinventing Aircraft Components",
        "From jet engine brackets to satellite structures, metal additive manufacturing is reshaping what is possible in aerospace design and production.",
        "April 28, 2026", "7 min read"
    )

    story.append(Paragraph("Introduction: Manufacturing's Quiet Revolution", styles['SectionHead']))
    story.append(Paragraph(
        "For most of aviation's history, if you wanted to make a metal aircraft part, you started with a large block of metal "
        "and machined away everything you did not need. For a complex aerospace component, this could mean removing 80 to 90 percent "
        "of the original material as chips and shavings. It is an expensive, time-consuming process that places hard limits on what "
        "shapes are possible to produce.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Metal additive manufacturing, commonly known as metal 3D printing, turns this approach upside down. Instead of removing "
        "material, it builds parts up layer by layer from metal powder or wire, adding only what is needed. This fundamental shift "
        "in how parts are made is enabling designs that were previously impossible to manufacture, dramatically reducing material "
        "waste, and opening up new possibilities for rapid iteration and customization in aerospace.",
        styles['BodyText2']
    ))

    story.append(Paragraph("How Metal 3D Printing Works", styles['SectionHead']))
    story.append(Paragraph(
        "Several different additive manufacturing processes are being used in aerospace, each with different capabilities and best "
        "applications. The two most widely adopted for structural metal parts are powder bed fusion and directed energy deposition.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Powder Bed Fusion", styles['SubHead']))
    story.append(Paragraph(
        "In powder bed fusion, a thin layer of metal powder is spread across a build platform. A high-powered laser or electron beam "
        "then selectively melts the powder according to the part's digital design file. The platform drops slightly, another layer of "
        "powder is spread, and the process repeats, building the part up layer by layer. The result is an extremely precise, fully "
        "dense metal part that can have internal features, channels, and lattice structures that no traditional machining process "
        "could produce.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Directed Energy Deposition", styles['SubHead']))
    story.append(Paragraph(
        "This process uses a focused energy source, typically a laser, to melt metal powder or wire as it is deposited onto a "
        "substrate. It is particularly useful for building up or repairing existing parts, and for producing large structural "
        "components that would be too big for a powder bed system. Some aerospace companies are using directed energy deposition "
        "to restore worn turbine blades, extending their service life rather than replacing them.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Design Freedom Advantage", styles['SectionHead']))
    story.append(Paragraph(
        "The most transformative aspect of metal additive manufacturing is not the process itself but the design freedom it enables. "
        "When engineers know that any shape can be manufactured, they stop designing for manufacturability and start designing purely "
        "for performance. This unleashes a set of design strategies that are simply not possible with conventional manufacturing.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"Additive manufacturing does not just change how we make parts. It changes what parts we can imagine making."',
        styles['Callout']
    ))
    story.append(Paragraph("Topology Optimization", styles['SubHead']))
    story.append(Paragraph(
        "Using sophisticated computer algorithms, engineers can specify the loads a part must carry and let the software determine "
        "the optimal material distribution to carry those loads. The resulting designs often look organic, resembling bones or coral "
        "rather than conventional machined parts. They use material only where it is structurally needed, achieving maximum strength "
        "with minimum weight. Topology-optimized brackets and structural fittings printed in titanium have achieved weight reductions "
        "of 40 to 60 percent compared to their conventionally manufactured predecessors.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Internal Cooling Channels", styles['SubHead']))
    story.append(Paragraph(
        "Jet engine components operate at temperatures that would melt many materials. Managing this heat requires sophisticated "
        "internal cooling systems that circulate cool air through channels inside the hot metal parts. Additive manufacturing allows "
        "engineers to create cooling channels with complex, optimized geometries that were previously impossible to machine. "
        "The result is better cooling with less weight and fewer parts.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Part Consolidation", styles['SubHead']))
    story.append(Paragraph(
        "Complex assemblies that previously required dozens of individual parts fastened together can often be redesigned as a "
        "single printed component. This eliminates the weight of fasteners, reduces the risk of joint failures, and simplifies "
        "assembly. GE Aviation famously consolidated a fuel nozzle for the LEAP jet engine from 20 separate parts into a single "
        "3D-printed component that is 25 percent lighter and five times more durable than its predecessor.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Materials at the Core", styles['SectionHead']))
    story.append(Paragraph(
        "The aerospace industry's demanding performance requirements have driven the development of an impressive portfolio of "
        "printable metal alloys. Each material family brings distinct advantages to specific applications.",
        styles['BodyText2']
    ))

    table_data = [
        ["Material", "Key Properties", "Typical Applications"],
        ["Titanium (Ti-6Al-4V)", "High strength-to-weight ratio, corrosion resistant", "Structural brackets, airframe fittings, medical implants"],
        ["Inconel 718", "Excellent high-temperature strength", "Turbine blades, combustor components, exhaust systems"],
        ["Aluminum (AlSi10Mg)", "Lightweight, good thermal properties", "Housings, brackets, heat exchangers"],
        ["17-4 PH Stainless", "High strength, good corrosion resistance", "Fittings, fasteners, tooling components"],
        ["Cobalt-Chrome", "Extreme wear and heat resistance", "Turbine components, bearings, cutting tools"],
    ]
    t = Table(table_data, colWidths=[1.6*inch, 2.0*inch, 2.6*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 13),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
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

    story.append(Paragraph("Certification: The Biggest Hurdle", styles['SectionHead']))
    story.append(Paragraph(
        "Despite its remarkable capabilities, metal additive manufacturing faces a significant challenge in aerospace: certification. "
        "Aviation regulators require extensive documentation and testing before any new manufacturing process can be used for "
        "flight-critical parts. This is not bureaucratic obstruction; it reflects the industry's commitment to safety. But it does "
        "mean that the path from a promising new additive technology to a certified, production-ready process can take years.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "The core challenge is process variability. Unlike machining, where the properties of the finished part are determined "
        "primarily by the starting material, additive manufacturing properties depend on a complex interplay of laser power, scan "
        "speed, powder characteristics, build orientation, and post-processing treatments. Demonstrating that these variables are "
        "sufficiently controlled to produce consistent, reliable parts is the central challenge in additive manufacturing certification.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Key certification requirements include:", styles['SubHead']))
    for bullet in [
        "Comprehensive characterization of the powder feedstock and its lot-to-lot variability",
        "Qualification of specific machine and parameter combinations for each alloy and part geometry",
        "Non-destructive inspection methods validated for additive-manufactured microstructures",
        "Fatigue and fracture testing that accounts for surface roughness and internal porosity",
        "In-process monitoring systems that detect and flag anomalies during build"
    ]:
        story.append(Paragraph(f"•  {bullet}", styles['BulletItem']))

    story.append(Paragraph("The Road Ahead", styles['SectionHead']))
    story.append(Paragraph(
        "The aerospace additive manufacturing market is growing rapidly, driven by the clear performance and efficiency advantages "
        "of the technology. Major engine manufacturers, airframers, and defense contractors are all investing heavily in additive "
        "capabilities. As certification frameworks mature and the technology matures, expect to see additive-manufactured components "
        "move from non-critical brackets and housings toward primary structural applications.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we help aerospace companies develop and qualify additive manufacturing processes, from alloy "
        "selection and process parameter development to microstructural characterization and certification testing support. "
        "Our team understands both the technical and regulatory dimensions of bringing additive parts to flight.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 8: AUTOMOTIVE — EV Battery Materials
# ─────────────────────────────────────────────────────────
def article_automotive_battery(story, styles):
    add_header_block(story, styles,
        "Automotive",
        "Engineering Polymers in EV Battery Systems:\nMaterials That Keep Your Battery Safe and Efficient",
        "The hidden materials science inside electric vehicle battery packs — and why getting it right is a matter of safety, range, and longevity.",
        "April 14, 2026", "7 min read"
    )

    story.append(Paragraph("Introduction: The Battery as a Materials Engineering Challenge", styles['SectionHead']))
    story.append(Paragraph(
        "When most people think about electric vehicle batteries, they think about chemistry: lithium-ion cells, cathode materials, "
        "electrolytes. But the battery pack in a modern EV is far more than a collection of cells. It is a sophisticated engineering "
        "system that must manage heat, withstand mechanical abuse, resist chemical exposure, and maintain structural integrity for "
        "hundreds of thousands of miles — all while keeping 400 to 800 volts of electricity safely contained.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Much of the engineering work that makes this possible is invisible to consumers. It lives in the materials that surround, "
        "support, and protect the cells: the polymers, composites, adhesives, and thermal interface materials that are just as "
        "critical to battery performance as the electrochemistry inside the cells themselves. Getting these materials right is one "
        "of the most demanding challenges in automotive materials engineering today.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Thermal Management Problem", styles['SectionHead']))
    story.append(Paragraph(
        "Lithium-ion cells are sensitive to temperature. They perform best in a relatively narrow window, typically between 15 and "
        "35 degrees Celsius. Too cold, and their power output drops dramatically. Too hot, and they degrade faster and, in extreme "
        "cases, can enter a dangerous condition called thermal runaway, where a single overheating cell triggers a chain reaction "
        "that can destroy the entire pack and create a fire that is extremely difficult to extinguish.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Every material in the battery pack plays a role in thermal management. Thermal interface materials, soft polymer pads "
        "or pastes placed between cells and cooling plates, must conduct heat efficiently while providing electrical insulation and "
        "accommodating the slight expansion and contraction that cells undergo during charge and discharge cycles. The wrong thermal "
        "interface material can create hot spots that accelerate cell degradation; the right one can extend battery life by years.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"In a battery pack, thermal management is not an afterthought. It is designed into every material choice from the very beginning."',
        styles['Callout']
    ))

    story.append(Paragraph("Key Polymer Applications in Battery Packs", styles['SectionHead']))

    story.append(Paragraph("Cell Holders and Module Frames", styles['SubHead']))
    story.append(Paragraph(
        "Individual cells are held in place by injection-molded polymer frames that must be dimensionally stable over a wide "
        "temperature range, flame retardant in case of thermal runaway, and chemically resistant to battery electrolyte. "
        "Engineering polymers like polyamide 6,6 (PA66), polyphenylene sulfide (PPS), and polybutylene terephthalate (PBT) "
        "are widely used for these applications, selected for their combination of mechanical performance, heat resistance, "
        "and processability.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Battery Enclosures", styles['SubHead']))
    story.append(Paragraph(
        "The outer casing of the battery pack must protect the cells from road debris, water intrusion, and mechanical impact, "
        "while contributing to the overall structural stiffness of the vehicle. Traditional aluminum enclosures are increasingly "
        "being supplemented or replaced by composite structures using carbon or glass fiber reinforced polymers. These materials "
        "can match the strength and stiffness of aluminum at 30 to 40 percent less weight, contributing directly to extended range.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Thermal Runaway Barriers", styles['SubHead']))
    story.append(Paragraph(
        "One of the most demanding material applications in the battery pack is the thermal runaway barrier placed between cell "
        "modules. If one module enters thermal runaway, these barriers must contain the heat, flames, and gases long enough for "
        "occupants to safely exit the vehicle, typically defined as a minimum of five minutes. The materials used — ceramic-filled "
        "intumescent sheets that expand when heated, high-performance aerogel composites, and ablative coatings — represent some "
        "of the most specialized materials in the automotive industry.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Seals and Gaskets", styles['SubHead']))
    story.append(Paragraph(
        "Every penetration in the battery enclosure, every cable entry point, every sensor port, must be sealed against water "
        "and dust to meet IP67 or IP68 ingress protection ratings. Fluorosilicone and EPDM rubber seals provide long-term sealing "
        "performance while remaining flexible across the pack's operating temperature range, from minus 40 degrees in arctic "
        "conditions to over 80 degrees Celsius during fast charging.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Degradation Challenge", styles['SectionHead']))
    story.append(Paragraph(
        "Battery pack materials face a punishing environment throughout the vehicle's life. They are exposed to repeated thermal "
        "cycling, vibration, mechanical shock from road impacts, and potential electrolyte exposure if a cell develops a leak. "
        "A material that performs well when new must continue to perform after 8 to 10 years and hundreds of thousands of miles.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Predicting this long-term behavior requires accelerated aging test protocols that compress years of service into weeks "
        "of laboratory testing. Thermal cycling tests, vibration tests, and electrolyte immersion tests are run in combination "
        "to simulate real-world conditions. Understanding how materials degrade under these conditions, and at what point "
        "degradation becomes a safety or performance concern, is one of the core challenges in battery materials engineering.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Next-Generation Battery Chemistries and New Material Demands", styles['SectionHead']))
    story.append(Paragraph(
        "The automotive industry is moving rapidly toward next-generation battery chemistries, including solid-state batteries "
        "that replace the liquid electrolyte with a solid ceramic or polymer material. These new chemistries promise higher energy "
        "density and improved safety but also create entirely new material challenges. The solid electrolyte itself must maintain "
        "intimate contact with the electrode materials throughout thousands of charge cycles, requiring polymer or composite "
        "components with precisely tailored mechanical compliance.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we work with EV manufacturers and their Tier 1 and Tier 2 suppliers on the full range of battery "
        "materials challenges. From material selection and qualification testing to failure analysis of field returns, our team "
        "provides the deep materials expertise you need to build battery systems that are safe, efficient, and durable.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 9: ENERGY — Renewable Energy Materials
# ─────────────────────────────────────────────────────────
def article_energy_renewable(story, styles):
    add_header_block(story, styles,
        "Energy",
        "Materials for the Energy Transition: What Wind Turbines\nand Solar Panels Are Really Made Of",
        "The materials science powering the clean energy revolution — and the engineering challenges that will determine how fast it can happen.",
        "April 1, 2026", "8 min read"
    )

    story.append(Paragraph("Introduction: The Energy Transition Is a Materials Challenge", styles['SectionHead']))
    story.append(Paragraph(
        "The world is in the midst of the most significant transformation of its energy systems in over a century. Solar and wind "
        "power are growing faster than any energy technology in history, driven by rapidly falling costs and urgent climate goals. "
        "But behind every solar panel and wind turbine is a story of materials innovation that rarely makes headlines — and some "
        "of the most demanding materials challenges in all of engineering.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Wind turbines must survive 20 to 25 years of continuous operation in some of the world's harshest environments, from "
        "offshore platforms battered by salt spray and storm waves to mountain ridges exposed to extreme temperature swings. Solar "
        "panels must maintain their performance through decades of UV exposure, thermal cycling, and weather events. Getting the "
        "materials right determines not just whether these systems work, but whether the economics of clean energy actually pencil out.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Wind Turbine Blades: The Composites Challenge", styles['SectionHead']))
    story.append(Paragraph(
        "A modern offshore wind turbine blade can reach over 100 meters in length, roughly the wingspan of an Airbus A380. "
        "These blades must be stiff enough to maintain their aerodynamic shape under tremendous wind loads, flexible enough to "
        "bend without breaking in gusts, and light enough that they do not impose excessive loads on the rest of the turbine structure. "
        "They must also withstand 20 years of rain erosion, lightning strikes, and fatigue from hundreds of millions of load cycles.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Glass fiber reinforced epoxy composites are the workhorse material for wind turbine blades, used for most of the blade "
        "structure. Carbon fiber reinforced polymers are increasingly used for the spar caps, the main load-carrying beams that "
        "run the length of the blade, because their higher stiffness allows longer blades without prohibitive weight penalties. "
        "Getting the resin infusion process right for a component this large, ensuring complete wet-out of the fiber reinforcement "
        "without voids or dry spots, is a major manufacturing challenge.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"A wind turbine blade is one of the largest composite structures ever routinely manufactured. The materials science required to build them reliably is extraordinary."',
        styles['Callout']
    ))

    story.append(Paragraph("The Leading Edge Erosion Problem", styles['SectionHead']))
    story.append(Paragraph(
        "The leading edges of wind turbine blades rotate at tip speeds of 80 to 100 meters per second. At these velocities, "
        "even small raindrops hit the blade surface with enormous impact energy. Over time, this continuous pitting and erosion "
        "damages the carefully engineered aerodynamic profile of the blade, reducing energy capture by as much as 5 percent "
        "annually on severely eroded blades. On a large offshore wind farm, this translates to millions of dollars in lost revenue.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Protecting against leading edge erosion requires specially formulated polyurethane or epoxy coatings that can absorb "
        "impact energy without cracking or delaminating. Developing these coatings requires deep expertise in polymer science, "
        "fatigue mechanics, and accelerated testing. Getting the formulation right means balancing toughness, adhesion, flexibility, "
        "and UV resistance across a 20-year service life.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Solar Panel Materials: More Than Silicon", styles['SectionHead']))
    story.append(Paragraph(
        "Most people know that solar panels convert sunlight into electricity using silicon. But the silicon cell is just one layer "
        "in a carefully engineered material stack designed to protect the cell and maximize its energy output over 25 to 30 years "
        "of outdoor exposure. Each material in this stack must perform its specific function while maintaining compatibility "
        "with all the others through thousands of thermal cycles and decades of UV radiation.",
        styles['BodyText2']
    ))

    table_data = [
        ["Layer", "Material", "Function"],
        ["Superstrate/Cover Glass", "Low-iron tempered glass", "Transmit maximum light, protect from impact and weather"],
        ["Front Encapsulant", "EVA or POE polymer film", "Adhere to glass, protect cell from moisture, transmit light"],
        ["Solar Cell", "Monocrystalline silicon", "Convert light to electricity"],
        ["Back Encapsulant", "EVA or POE polymer film", "Protect cell rear, provide electrical insulation"],
        ["Backsheet", "Multi-layer polymer film (TPT)", "Final moisture barrier, electrical insulation, UV resistance"],
        ["Frame", "Anodized aluminum alloy", "Structural support, mounting, grounding"],
    ]
    t = Table(table_data, colWidths=[1.4*inch, 1.7*inch, 3.1*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 13),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
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

    story.append(Paragraph("The Encapsulant: A Critical but Overlooked Material", styles['SectionHead']))
    story.append(Paragraph(
        "The encapsulant films that sandwich the solar cell are among the most technically demanding materials in the solar panel. "
        "They must be optically transparent to minimize light loss, thermally stable enough to withstand the elevated temperatures "
        "that panels can reach on hot days, moisture-resistant to prevent cell degradation, and adhesive enough to bond reliably "
        "to both the glass and cell surfaces throughout a 30-year life.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Ethylene-vinyl acetate (EVA) has been the dominant encapsulant material for decades, but it has a significant weakness: "
        "it can yellow and degrade with prolonged UV exposure, and it can release acetic acid that corrodes metal contacts on the "
        "solar cell. Polyolefin elastomers (POE) are gaining market share as an alternative with superior UV stability and moisture "
        "resistance, though they are harder to process and more expensive. Choosing between these materials requires careful "
        "consideration of the specific climate, panel design, and economic constraints of each project.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The End-of-Life Challenge", styles['SectionHead']))
    story.append(Paragraph(
        "Solar panels installed during the first major growth wave of the industry are beginning to reach the end of their service "
        "lives. The solar industry is facing a growing challenge: what to do with tens of millions of tons of panels that contain "
        "valuable materials, including silicon, silver, and aluminum, encapsulated in ways that make them difficult to separate "
        "and recover. Developing recycling processes that can efficiently separate and reclaim these materials is one of the most "
        "important unsolved problems in renewable energy.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we help energy companies across the renewable sector address materials challenges, from blade "
        "composite design and failure analysis to solar encapsulant selection and accelerated aging evaluation. The energy "
        "transition depends on getting these materials right.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 10: BIOMEDICAL — 3D Printed Implants
# ─────────────────────────────────────────────────────────
def article_biomedical_additive(story, styles):
    add_header_block(story, styles,
        "Biomedical",
        "3D-Printed Implants: How Additive Manufacturing\nIs Personalizing Orthopedic Medicine",
        "Patient-specific implants printed from titanium and PEEK are transforming bone repair — here is the materials science making it possible.",
        "March 17, 2026", "6 min read"
    )

    story.append(Paragraph("Introduction: The Problem With Standard Sizes", styles['SectionHead']))
    story.append(Paragraph(
        "Human anatomy does not come in standard sizes. Every person's bones are shaped differently, influenced by genetics, "
        "age, injury history, and disease. Yet for most of modern medicine's history, orthopedic implants have been manufactured "
        "in a limited range of standard sizes and shapes. Surgeons have had to select the closest available option and adapt "
        "the surgical procedure to make it fit, sometimes removing additional bone to accommodate a standardized implant.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Additive manufacturing is changing this equation fundamentally. By combining medical imaging data with advanced "
        "materials processing, surgeons and engineers can now design and print implants that match a specific patient's anatomy "
        "with sub-millimeter precision. This is not a futuristic concept. Patient-specific 3D-printed implants are already being "
        "used in thousands of surgeries annually, and the technology is advancing rapidly.",
        styles['BodyText2']
    ))

    story.append(Paragraph("From Scan to Implant: The Workflow", styles['SectionHead']))
    story.append(Paragraph(
        "The process of creating a patient-specific implant begins with high-resolution medical imaging, typically CT scanning "
        "that creates a three-dimensional map of the patient's anatomy. Engineers use specialized software to segment the images, "
        "identifying bone boundaries and defects, and design an implant that fills the defect precisely while accounting for "
        "the mechanical loads the implant will need to bear.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "This digital design is then transferred to a metal additive manufacturing system that builds the implant layer by layer "
        "from titanium or cobalt-chrome powder. The entire process from CT scan to finished implant can be completed in days, "
        "compared to weeks or months for custom implants made through conventional manufacturing. For patients with complex tumor "
        "resections, traumatic bone loss, or unusual anatomy, this speed can be the difference between a straightforward recovery "
        "and an extensive, complicated surgical procedure.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Why Titanium?", styles['SectionHead']))
    story.append(Paragraph(
        "Titanium alloys, particularly Ti-6Al-4V, have become the dominant material for orthopedic additive manufacturing, "
        "and for good reason. Titanium combines an excellent strength-to-weight ratio with exceptional corrosion resistance in "
        "the body's chemical environment. Critically, it is one of only a handful of metals that the human body accepts without "
        "a significant immune response, a property called osseointegration.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "But additive manufacturing does not just replicate what could be done with conventionally manufactured titanium. "
        "It enables a design strategy that is impossible with any other manufacturing method: porous structures that mimic "
        "the architecture of natural bone.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"A solid titanium implant and a porous printed implant of the same size can behave completely differently inside the body. The architecture is as important as the material."',
        styles['Callout']
    ))

    story.append(Paragraph("The Science of Osseointegration Through Porosity", styles['SectionHead']))
    story.append(Paragraph(
        "Natural bone is not solid. It has a hierarchical porous structure, from the large cavities of trabecular bone visible "
        "to the naked eye, to microscopic channels and pores that allow blood vessels and bone-forming cells to permeate the "
        "entire structure. When bone grows into and around an implant, this process is called osseointegration, and it is what "
        "gives a permanent implant its long-term stability.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Smooth, solid metal implants rely primarily on surface chemistry and mechanical fixation for stability. Porous additive "
        "manufactured implants can provide a three-dimensional scaffold into which bone actively grows, creating a biological bond "
        "far stronger than any mechanical fixation alone. Research shows that pore sizes between 300 and 600 micrometers, with "
        "interconnected porosity of 65 to 80 percent, are optimal for bone ingrowth. Additive manufacturing can produce these "
        "structures with precise, reproducible geometry.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Regulatory Considerations for Printed Implants", styles['SectionHead']))
    story.append(Paragraph(
        "The regulatory pathway for 3D-printed implants adds complexity to an already challenging field. The FDA classifies "
        "patient-specific 3D-printed implants as custom devices, which have a different regulatory pathway than standard "
        "manufactured implants. While custom devices can be exempt from full premarket approval, the manufacturer must still "
        "demonstrate that the device is safe and effective for its intended use.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Critical regulatory requirements for additively manufactured implants include:", styles['SubHead']))
    for bullet in [
        "Validation of the design software and the digital-to-physical manufacturing chain",
        "Demonstration that the material properties of printed parts meet the same standards as conventionally made implants",
        "Characterization of residual porosity, surface roughness, and subsurface defects",
        "Verification that post-processing steps (heat treatment, surface finishing, sterilization) do not degrade critical properties",
        "Traceability from patient imaging data through design, manufacturing, and implantation"
    ]:
        story.append(Paragraph(f"•  {bullet}", styles['BulletItem']))

    story.append(Paragraph("The Future: Bioprinting and Smart Implants", styles['SectionHead']))
    story.append(Paragraph(
        "The frontier of implant additive manufacturing extends beyond metals. Researchers are actively developing techniques "
        "for bioprinting, where living cells are printed into three-dimensional scaffolds to create tissues and ultimately organs. "
        "While fully bioprinted organs remain years away from clinical use, bioprinted cartilage patches, bone scaffolds, and "
        "vascular grafts are already in early clinical trials.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we support medical device companies at the intersection of additive manufacturing, advanced "
        "materials, and regulatory compliance. Whether you are developing a patient-specific implant program or scaling an "
        "existing additive manufacturing process, our team provides the materials expertise to help you move confidently "
        "from concept to clinical use.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 11: CONSTRUCTION — Smart Coatings
# ─────────────────────────────────────────────────────────
def article_construction_coatings(story, styles):
    add_header_block(story, styles,
        "Construction",
        "Smart Coatings for Infrastructure Protection:\nHow Nanotechnology Is Defeating Corrosion",
        "The science behind a new generation of protective coatings that can sense damage, respond to threats, and extend the life of steel structures by decades.",
        "March 3, 2026", "6 min read"
    )

    story.append(Paragraph("Introduction: The $2.5 Trillion Corrosion Problem", styles['SectionHead']))
    story.append(Paragraph(
        "Corrosion costs the global economy an estimated $2.5 trillion annually, roughly 3.4 percent of global GDP. In the "
        "construction and infrastructure sector alone, the cost of repainting bridges, repairing corroded structural steel, "
        "and replacing deteriorated components runs into hundreds of billions of dollars each year. A significant portion of "
        "this cost is preventable with better protective coatings.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "Traditional protective coatings work on a simple principle: create a physical barrier between the metal and its "
        "environment. Epoxy primers, zinc-rich coatings, and polyurethane topcoats have served this function reliably for "
        "decades. But they have a fundamental weakness: once a coating is scratched or damaged, the barrier is broken, and "
        "corrosion can begin and spread beneath the intact coating, often invisibly until significant damage has occurred.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "A new generation of smart coatings, incorporating nanotechnology and active corrosion inhibition, is addressing this "
        "weakness directly. These materials do not just passively block corrosion; they actively respond to damage and the "
        "early stages of corrosion, providing a level of protection that conventional coatings simply cannot match.",
        styles['BodyText2']
    ))

    story.append(Paragraph("What Makes a Coating 'Smart'?", styles['SectionHead']))
    story.append(Paragraph(
        "The term smart coating refers to a coating that can detect a change in its environment and respond in a way that "
        "reduces damage. In the context of corrosion protection, this typically means a coating that can detect mechanical "
        "damage or the onset of electrochemical corrosion reactions and release corrosion inhibitors in response. Think of "
        "it as a coating with a built-in immune system.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"A conventional coating waits to fail. A smart coating fights back."',
        styles['Callout']
    ))

    story.append(Paragraph("Microencapsulated Inhibitors", styles['SubHead']))
    story.append(Paragraph(
        "One of the most commercially advanced approaches to smart coatings involves embedding microcapsules containing corrosion "
        "inhibitors throughout the coating matrix. When a scratch or impact breaks the coating, it also ruptures the microcapsules "
        "in the damaged area, releasing the inhibitors directly where they are needed. The inhibitors react with the exposed metal "
        "surface to form a protective passivation layer that slows or stops corrosion at the damage site.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "This approach, inspired by biological systems like blood clotting, has shown remarkable results in laboratory testing "
        "and is beginning to appear in commercial products. Field trials on bridges and industrial structures have demonstrated "
        "significantly reduced corrosion at damaged areas compared to conventional coatings.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Nanoparticle-Enhanced Barrier Coatings", styles['SubHead']))
    story.append(Paragraph(
        "Incorporating nanoparticles into coating formulations can dramatically improve their barrier performance without "
        "compromising flexibility or adhesion. Platelet-shaped nanoparticles of clay, graphene, or zinc oxide orient themselves "
        "parallel to the coating surface during application, creating a tortuous path that moisture and corrosive ions must "
        "navigate to reach the metal substrate. This can reduce moisture permeability by an order of magnitude compared to "
        "conventional coatings of the same thickness.",
        styles['BodyText2']
    ))
    story.append(Paragraph("pH-Responsive Release Systems", styles['SubHead']))
    story.append(Paragraph(
        "Corrosion is an electrochemical process that changes the local pH of the coating-metal interface. Researchers have "
        "developed coating systems that use this pH change as a trigger to release inhibitors. Hollow nanoparticles or "
        "polymer nanocontainers loaded with inhibitors are formulated to release their contents only when the local pH "
        "drops to the level associated with active corrosion. This on-demand release ensures inhibitors are available when "
        "needed but are not depleted prematurely in non-corroding areas.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Real-World Applications and Results", styles['SectionHead']))
    story.append(Paragraph(
        "Smart coating technologies are moving from laboratory curiosity to commercial reality, with several applications "
        "already demonstrating significant performance advantages in the field.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Bridge and Highway Infrastructure", styles['SubHead']))
    story.append(Paragraph(
        "Transportation departments in several countries are piloting smart coatings on bridges and highway structures. Early "
        "results show that bridges coated with microcapsule-enhanced systems require recoating 30 to 50 percent less frequently "
        "than those using conventional coatings, representing substantial savings in both material and labor costs. For a major "
        "suspension bridge that might cost $5 to $10 million to repaint, even a 30 percent extension in coating life translates "
        "to millions of dollars in savings.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Marine and Offshore Structures", styles['SubHead']))
    story.append(Paragraph(
        "Offshore oil platforms, wind turbine foundations, and marine terminals face some of the most corrosive environments "
        "on earth. Accessing these structures for inspection and recoating is expensive and hazardous. Smart coatings that "
        "extend maintenance intervals are particularly valuable in these applications, where the cost of a single painting "
        "campaign can run into millions of dollars.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Implementation Considerations", styles['SectionHead']))
    story.append(Paragraph(
        "Smart coatings are not a drop-in replacement for conventional systems. They require careful consideration of surface "
        "preparation, application conditions, and compatibility with existing coating systems. The nanoparticles and "
        "microcapsules in these coatings can be sensitive to shear forces during application, requiring modified spray "
        "equipment settings or application techniques. Field applicators need training to handle these materials correctly.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we help infrastructure owners and coating specifiers evaluate and implement smart coating "
        "technologies. From material selection and specification through application quality control and long-term performance "
        "monitoring, our team provides the technical expertise to realize the full potential of these advanced materials.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# ARTICLE 12: CONSUMER PRODUCTS — Engineering Plastics
# ─────────────────────────────────────────────────────────
def article_consumer_plastics(story, styles):
    add_header_block(story, styles,
        "Consumer Products",
        "Engineering Plastics vs. Metals: The Smart Material\nSubstitution Strategy Reshaping Product Design",
        "Why the best-designed consumer products increasingly use high-performance polymers where metal used to be the default — and how to make the switch successfully.",
        "February 17, 2026", "6 min read"
    )

    story.append(Paragraph("Introduction: Why Plastics Keep Winning", styles['SectionHead']))
    story.append(Paragraph(
        "Pick up your smartphone. Look at a modern laptop. Examine the interior of a high-end appliance. In each case, you are "
        "looking at a product that has been shaped by one of the most important trends in modern manufacturing: the systematic "
        "substitution of metals with engineering plastics. Not cheap commodity plastics, but high-performance engineering-grade "
        "polymers with mechanical, thermal, and chemical properties that would have seemed impossible to achieve in a plastic "
        "material just two decades ago.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "This shift is not happening by accident. It is driven by a convergence of factors: improving polymer materials, "
        "advancing manufacturing processes, increasing pressure to reduce weight and cost, and growing consumer demand for "
        "thinner, lighter, more complex products. Understanding how and when to make the metal-to-plastic transition is one "
        "of the most valuable skills in modern product design.",
        styles['BodyText2']
    ))

    story.append(Paragraph("The Case for Engineering Plastics", styles['SectionHead']))
    story.append(Paragraph(
        "Engineering plastics offer a compelling set of advantages that explain their growing dominance in consumer product design:",
        styles['BodyText2']
    ))
    for bullet in [
        "Weight: Engineering plastics are typically 4 to 7 times lighter than steel and 1.5 to 2 times lighter than aluminum",
        "Design freedom: Injection molding can produce geometries impossible to machine from metal in a single step",
        "Part consolidation: Multiple metal parts can often be redesigned as a single plastic component",
        "Electrical insulation: Eliminates the need for additional insulating components in electrical assemblies",
        "Corrosion resistance: No surface treatment or coating required for most applications",
        "Noise and vibration damping: Superior vibration absorption compared to metals",
        "Cost: Typically lower part cost at high production volumes despite higher material cost"
    ]:
        story.append(Paragraph(f"•  {bullet}", styles['BulletItem']))

    story.append(Paragraph("A Guide to Key Engineering Plastics", styles['SectionHead']))

    table_data = [
        ["Material", "Key Properties", "Common Consumer Applications"],
        ["Polycarbonate (PC)", "Impact resistant, optically clear, heat resistant", "Phone cases, eyewear lenses, LED diffusers"],
        ["ABS", "Good impact strength, easy to process, paintable", "Appliance housings, toys, automotive trim"],
        ["Nylon (PA6, PA66)", "Strong, wear resistant, good fatigue life", "Gears, bearings, power tool housings"],
        ["POM (Acetal)", "Very stiff, low friction, dimensionally stable", "Precision gears, hinges, zippers, fasteners"],
        ["PEEK", "Extreme temperature and chemical resistance", "High-end electronics, medical devices"],
        ["PC/ABS Blend", "Balance of PC toughness and ABS processability", "Laptop and phone housings, power tools"],
    ]
    t = Table(table_data, colWidths=[1.3*inch, 2.0*inch, 2.9*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 13),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
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

    story.append(Paragraph("When Metal Still Wins", styles['SectionHead']))
    story.append(Paragraph(
        "Engineering plastics are not the right choice for every application. Understanding where metals retain their advantage "
        "is just as important as knowing where to substitute. Metals remain superior in applications requiring very high "
        "sustained loads over long periods, elevated temperature performance above the service temperature of most polymers "
        "(generally above 150 to 200 degrees Celsius), electrical conductivity, thermal conductivity for heat dissipation, "
        "or the premium feel and scratch resistance that consumers associate with high-end products.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        '"The best material is always the one that delivers the required performance at the lowest total cost. Sometimes that is plastic. Sometimes it is metal. Often, it is both."',
        styles['Callout']
    ))

    story.append(Paragraph("The Hidden Pitfalls of Material Substitution", styles['SectionHead']))
    story.append(Paragraph(
        "Metal-to-plastic substitution is not as simple as choosing an engineering plastic with similar tensile strength to the "
        "metal it replaces. Plastics and metals behave very differently under load, and designs that work well in metal often "
        "fail in plastic if they are not fundamentally rethought.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Creep and Relaxation", styles['SubHead']))
    story.append(Paragraph(
        "Unlike metals, plastics deform slowly over time under sustained loads, even at loads well below their short-term "
        "strength. This phenomenon, called creep, means that a plastic bracket holding a sustained load may slowly deform "
        "over months or years until it fails. Designing for creep resistance requires understanding the long-term viscoelastic "
        "behavior of the specific polymer under the specific loading conditions of the application.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Weld Line Weakness", styles['SubHead']))
    story.append(Paragraph(
        "When plastic flows around a core pin or through multiple gates in an injection mold, the flow fronts meet and create "
        "a weld line, a plane of weakness that can be 20 to 50 percent weaker than the surrounding material. Critical load-bearing "
        "features must be designed to avoid weld lines, or the mold must be engineered to ensure weld lines fall in non-critical areas.",
        styles['BodyText2']
    ))
    story.append(Paragraph("Environmental Stress Cracking", styles['SubHead']))
    story.append(Paragraph(
        "Many engineering plastics are susceptible to stress cracking when exposed to certain chemicals, cleaning agents, "
        "or assembly lubricants while under stress. This can cause sudden brittle fracture at stress levels far below the "
        "material's normal strength. Evaluating compatibility between the plastic material and all chemicals it might encounter "
        "in manufacture, assembly, and use is an essential step in the design process.",
        styles['BodyText2']
    ))

    story.append(Paragraph("A Framework for Successful Substitution", styles['SectionHead']))
    story.append(Paragraph(
        "Based on our experience helping product companies make successful metal-to-plastic transitions, we recommend "
        "a systematic approach that begins with a thorough understanding of the loads, environments, and performance "
        "requirements of the application before any material is selected. Key steps include detailed load analysis to "
        "understand peak, sustained, and fatigue loading; environmental analysis covering temperature range, chemical "
        "exposure, and UV; material screening against the full performance envelope; design optimization specifically "
        "for plastic processing and load paths; prototype testing under realistic conditions; and accelerated aging "
        "to validate long-term performance.",
        styles['BodyText2']
    ))
    story.append(Paragraph(
        "At Flaney Associates, we guide consumer product companies through every step of this process. From initial "
        "material screening and design review to failure analysis of field returns, our team ensures that your "
        "material substitution projects deliver the weight, cost, and performance improvements you are targeting.",
        styles['BodyText2']
    ))


# ─────────────────────────────────────────────────────────
# MAIN: BUILD ALL 6 NEW PDFs
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating 6 new Flaney Associates blog article PDFs (Round 2)...\n")
    articles = [
        ("aerospace-additive-manufacturing.pdf", article_aerospace_additive),
        ("automotive-ev-battery-materials.pdf", article_automotive_battery),
        ("energy-renewable-materials.pdf", article_energy_renewable),
        ("biomedical-3d-printed-implants.pdf", article_biomedical_additive),
        ("construction-smart-coatings.pdf", article_construction_coatings),
        ("consumer-engineering-plastics.pdf", article_consumer_plastics),
    ]
    for filename, func in articles:
        build_pdf(filename, func)
    print("\nAll 6 new PDFs generated successfully!")
