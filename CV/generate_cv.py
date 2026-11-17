import pymupdf as fitz  # PyMuPDF
import os

# A4 dimensions in points: 595.28 x 841.89
W, H = fitz.paper_size("a4")

doc = fitz.open()
page = doc.new_page(width=W, height=H)

# Load Windows Segoe UI fonts for crisp typography
font_dir = r"C:\Windows\Fonts"
f_reg = os.path.join(font_dir, "segoeui.ttf")
f_bold = os.path.join(font_dir, "segoeuib.ttf")
f_semi = os.path.join(font_dir, "seguisb.ttf")
f_ital = os.path.join(font_dir, "segoeuii.ttf")

font_reg_obj = fitz.Font(fontfile=f_reg)
font_semi_obj = fitz.Font(fontfile=f_semi)
font_bold_obj = fitz.Font(fontfile=f_bold)

page.insert_font(fontname="FReg", fontfile=f_reg)
page.insert_font(fontname="FBold", fontfile=f_bold)
page.insert_font(fontname="FSemi", fontfile=f_semi)
page.insert_font(fontname="FItal", fontfile=f_ital)

# Colors (RGB 0..1)
def rgb(r, g, b):
    return (r / 255.0, g / 255.0, b / 255.0)

C_BLUE_MAIN = rgb(2, 132, 199)      # #0284c7
C_BLUE_LIGHT = rgb(14, 165, 233)    # #0ea5e9
C_BLUE_PALE = rgb(240, 249, 255)    # #f0f9ff
C_GREEN_MAIN = rgb(16, 185, 129)    # #10b981
C_GREEN_DARK = rgb(4, 120, 87)      # #047857
C_GREEN_PALE = rgb(236, 253, 245)   # #ecfdf5
C_LIME = rgb(132, 204, 22)          # #84cc16
C_DARK = rgb(15, 23, 42)            # #0f172a
C_TEXT = rgb(51, 65, 85)            # #334155
C_MUTED = rgb(100, 116, 139)        # #64748b
C_LINE = rgb(203, 213, 225)         # #cbd5e1
C_TAG_BG = rgb(241, 245, 249)       # #f1f5f9
C_WHITE = (1, 1, 1)

# 1. Left vertical spine line (like the reference image)
SPINE_X = 32
page.draw_line(
    fitz.Point(SPINE_X, 0),
    fitz.Point(SPINE_X, H - 32),
    color=C_LINE,
    width=1.6,
)

# Helper: Draw Reference-Image-Style Blue Ribbon Section Header
def draw_ribbon(x, y, width_box, total_width, title, badge_char):
    box_h = 20.5
    rect_box = fitz.Rect(x - 10, y, x - 10 + width_box, y + box_h)

    # Subtle shadow
    page.draw_rect(
        fitz.Rect(rect_box.x0 + 2, rect_box.y0 + 2, rect_box.x1 + 2, rect_box.y1 + 2),
        color=None,
        fill=rgb(203, 213, 225),
    )
    # Main Blue Banner Box
    page.draw_rect(rect_box, color=None, fill=C_BLUE_LIGHT)
    # Left Green Accent Strip on Banner
    page.draw_rect(
        fitz.Rect(rect_box.x0, rect_box.y0, rect_box.x0 + 4.5, rect_box.y1),
        color=None,
        fill=C_GREEN_MAIN,
    )
    # Dark bottom border on ribbon box (just like reference image)
    page.draw_line(
        fitz.Point(rect_box.x0, rect_box.y1),
        fitz.Point(rect_box.x1, rect_box.y1),
        color=C_DARK,
        width=2.0,
    )
    # Extending horizontal blue line to the right of the ribbon box
    page.draw_line(
        fitz.Point(rect_box.x1, rect_box.y1 - 1),
        fitz.Point(x + total_width, rect_box.y1 - 1),
        color=C_BLUE_LIGHT,
        width=2.0,
    )

    # White circle icon inside ribbon
    cx = rect_box.x0 + 15.5
    cy = rect_box.y0 + box_h / 2
    page.draw_circle(fitz.Point(cx, cy), 6.4, color=C_WHITE, fill=C_WHITE)
    char_w = font_bold_obj.text_length(badge_char, fontsize=8.0)
    page.insert_text(
        fitz.Point(cx - char_w / 2.0, cy + 2.9),
        badge_char,
        fontname="FBold",
        fontsize=8.0,
        color=C_BLUE_MAIN,
    )

    # Ribbon Title Text
    page.insert_text(
        fitz.Point(rect_box.x0 + 27, rect_box.y0 + 14.2),
        title,
        fontname="FBold",
        fontsize=9.4,
        color=C_WHITE,
    )
    return y + box_h + 7

# Helper: Draw crisp vector bullet dot
def draw_bullet_dot(x, y, color=C_BLUE_MAIN):
    page.draw_circle(fitz.Point(x + 2.5, y + 4.8), 2.1, color=None, fill=color)

# Helper: Draw wrapped text and return exact next Y coordinate
def draw_wrapped_text(x, y, max_w, text, font_obj, fontname, fontsize, color, line_height=11.0):
    words = text.split()
    lines = []
    cur_line = ""
    for w in words:
        test = (cur_line + " " + w).strip()
        if font_obj.text_length(test, fontsize=fontsize) <= max_w:
            cur_line = test
        else:
            if cur_line:
                lines.append(cur_line)
            cur_line = w
    if cur_line:
        lines.append(cur_line)

    for idx, ln in enumerate(lines):
        page.insert_text(
            fitz.Point(x, y + 8.0 + idx * line_height),
            ln,
            fontname=fontname,
            fontsize=fontsize,
            color=color,
        )
    return y + len(lines) * line_height

# Helper: Draw Horizontal Gradient Bar (Blue -> Green -> Lime like Reference Image)
def draw_gradient_bar(x, y, w, h, pct):
    page.draw_rect(fitz.Rect(x, y, x + w, y + h), color=None, fill=rgb(226, 232, 240))
    fill_w = w * pct
    steps = 36
    step_w = fill_w / steps
    for i in range(steps):
        t = i / float(steps - 1)
        if t < 0.55:
            u = t / 0.55
            c = (
                C_BLUE_MAIN[0] * (1 - u) + C_GREEN_MAIN[0] * u,
                C_BLUE_MAIN[1] * (1 - u) + C_GREEN_MAIN[1] * u,
                C_BLUE_MAIN[2] * (1 - u) + C_GREEN_MAIN[2] * u,
            )
        else:
            u = (t - 0.55) / 0.45
            c = (
                C_GREEN_MAIN[0] * (1 - u) + C_LIME[0] * u,
                C_GREEN_MAIN[1] * (1 - u) + C_LIME[1] * u,
                C_GREEN_MAIN[2] * (1 - u) + C_LIME[2] * u,
            )
        rx0 = x + i * step_w
        rx1 = rx0 + step_w + 0.4
        page.draw_rect(fitz.Rect(rx0, y, rx1, y + h), color=None, fill=c)

# ==============================================================================
# TOP HEADER SECTION (LEFT: NAME, TITLE, PROFILE | RIGHT: CROPPED ELBOW PHOTO)
# ==============================================================================
LEFT_X = 44
TOP_Y = 24

# Name & Subtitle
page.insert_text(
    fitz.Point(LEFT_X, TOP_Y + 18),
    "REYNARD KAMADJAJA, S.Kom.",
    fontname="FBold",
    fontsize=20.5,
    color=C_BLUE_MAIN,
)
page.insert_text(
    fitz.Point(LEFT_X, TOP_Y + 32.5),
    "AI-Augmented Full-Stack & Mobile App Developer  |  Software Engineer",
    fontname="FBold",
    fontsize=9.6,
    color=C_DARK,
)

# Photo Frame on Top Right (Cropped to Elbows!)
PHOTO_W = 122
PHOTO_H = 152
PHOTO_X = W - 26 - PHOTO_W
PHOTO_Y = TOP_Y + 2

# Outer Blue Frame
page.draw_rect(
    fitz.Rect(PHOTO_X - 4, PHOTO_Y - 4, PHOTO_X + PHOTO_W + 4, PHOTO_Y + PHOTO_H + 4),
    color=C_BLUE_LIGHT,
    fill=C_BLUE_PALE,
    width=2.4,
)
# Inner Green Accent Line
page.draw_rect(
    fitz.Rect(PHOTO_X - 1.2, PHOTO_Y - 1.2, PHOTO_X + PHOTO_W + 1.2, PHOTO_Y + PHOTO_H + 1.2),
    color=C_GREEN_MAIN,
    fill=C_WHITE,
    width=1.0,
)
photo_path = os.path.join(os.path.dirname(__file__), "profile_cropped_elbow.jpg")
page.insert_image(fitz.Rect(PHOTO_X, PHOTO_Y, PHOTO_X + PHOTO_W, PHOTO_Y + PHOTO_H), filename=photo_path)

# PROFILE Ribbon Banner
PROFILE_W = PHOTO_X - LEFT_X - 14
cur_y = draw_ribbon(LEFT_X, TOP_Y + 41, 155, PROFILE_W, "PROFILE & SUMMARY", "P")

# Executive Summary Text (Rendered cleanly line-by-line)
summary_text = (
    "Software Developer and Informatics graduate (S.Kom.) from iSTTS Surabaya who leverages AI-augmented "
    "development workflows and advanced Prompt Engineering (LLMs) to deliver high-quality, end-to-end software at "
    "rapid speed. Proven experience building cross-platform Flutter mobile apps with real-time Midtrans QRIS "
    "payments, React & Node.js web apps, custom Python desktop POS systems, and Gemini AI chatbot integrations."
)
cur_y = draw_wrapped_text(
    LEFT_X, cur_y, PROFILE_W, summary_text, font_reg_obj, "FReg", 8.2, C_TEXT, line_height=11.0
)
cur_y += 6

# Structured Profile Key-Value Table (Zero overlap between columns)
meta_h = 50
meta_box = fitz.Rect(LEFT_X, cur_y, LEFT_X + PROFILE_W, cur_y + meta_h)
page.draw_rect(meta_box, color=None, fill=C_BLUE_PALE)
page.draw_rect(fitz.Rect(LEFT_X, cur_y, LEFT_X + 3, cur_y + meta_h), color=None, fill=C_BLUE_MAIN)

meta_left = [
    ("Degree", ": S.Kom. (Bachelor of Informatics)"),
    ("Location", ": Surabaya, East Java, Indonesia"),
    ("Work Status", ": Open to Work (Full-Time / Remote)"),
    ("Languages", ": Indonesian (Native), English (Pro)"),
]
meta_right = [
    ("Portfolio Web", ": reynaldy4699.github.io", "https://reynaldy4699.github.io/"),
    ("Credly Badges", ": credly.com/users/rey-kamadjaya", "https://www.credly.com/users/rey-kamadjaya"),
    ("Email", ": reykamadjaya@gmail.com", "mailto:reykamadjaya@gmail.com"),
    ("Phone / WA", ": +62 813-5300-2672", "https://wa.me/6281353002672"),
]

for idx, (k, v) in enumerate(meta_left):
    my = cur_y + 11.0 + idx * 11.4
    page.insert_text(fitz.Point(LEFT_X + 8, my), k, fontname="FBold", fontsize=7.6, color=C_DARK)
    page.insert_text(fitz.Point(LEFT_X + 58, my), v, fontname="FSemi", fontsize=7.6, color=C_TEXT)

col2_meta_x = LEFT_X + 196
for idx, (k, v, url) in enumerate(meta_right):
    my = cur_y + 11.0 + idx * 11.4
    page.insert_text(fitz.Point(col2_meta_x, my), k, fontname="FBold", fontsize=7.6, color=C_DARK)
    val_x = col2_meta_x + 54
    is_link = url.startswith("https://reynaldy") or url.startswith("https://www.credly")
    page.insert_text(
        fitz.Point(val_x, my),
        v,
        fontname="FBold" if is_link else "FSemi",
        fontsize=7.6,
        color=C_BLUE_MAIN if is_link else C_TEXT,
    )
    page.insert_link(
        {
            "kind": fitz.LINK_URI,
            "from": fitz.Rect(val_x, my - 8, val_x + 125, my + 2),
            "uri": url,
        }
    )

# ==============================================================================
# MAIN TWO-COLUMN SECTION
# ==============================================================================
BODY_TOP_Y = cur_y + meta_h + 10
COL1_X = LEFT_X
COL1_W = 278
COL2_X = COL1_X + COL1_W + 18
COL2_W = W - COL2_X - 24

# ------------------------------------------------------------------------------
# LEFT COLUMN: 1) FEATURED PROJECTS  2) EDUCATION  3) CORE CAPABILITIES
# ------------------------------------------------------------------------------
y1 = draw_ribbon(COL1_X, BODY_TOP_Y, 162, COL1_W, "PROJECT EXPERIENCE", "E")

projects = [
    {
        "title": "Sprout Tycoon – 2D Mobile Simulation & Idle Game",
        "link_text": "",
        "link_url": "",
        "role": "Lead Developer (Undergraduate Thesis Project)",
        "stack": "Flutter  |  Dart  |  Flame Engine  |  Firebase  |  Midtrans API (QRIS)",
        "bullets": [
            "Engineered a 2D mobile simulation & idle farming game with custom game loop, resource mechanics, and responsive UI using Flutter & Flame Engine.",
            "Integrated real-time in-app purchases via Midtrans QRIS payment gateway and cloud player progress synchronization using Firebase.",
        ],
    },
    {
        "title": "Toko Gembira – Desktop POS & Inventory System",
        "link_text": "",
        "link_url": "",
        "role": "Full-Stack Desktop Software Developer",
        "stack": "Python  |  CustomTkinter  |  SQLite  |  Thermal Printer ESC/POS",
        "bullets": [
            "Built a custom desktop Point-of-Sale (POS) and warehouse inventory app with real-time stock tracking, sales reporting, and local SQLite database.",
            "Implemented direct ESC/POS hardware integration to print transaction receipts automatically via physical thermal printers.",
        ],
    },
    {
        "title": "Juanda City Park – Real Estate Portal & AI App",
        "link_text": "[juandacitypark.com]",
        "link_url": "https://juandacitypark.com/",
        "role": "Mobile & Frontend Developer",
        "stack": "Flutter  |  Gemini AI API  |  Google Drive API  |  Firebase Auth  |  SQLite",
        "bullets": [
            "Integrated a real-time Gemini AI Chatbot assistant to answer prospective buyers' property inquiries and assist with catalog details.",
            "Built secure Firebase Authentication, local SQLite activity logging, and dynamic property asset management via Google Drive API.",
        ],
    },
]

for proj in projects:
    page.insert_text(fitz.Point(COL1_X, y1 + 8), proj["title"], fontname="FBold", fontsize=9.0, color=C_BLUE_MAIN)
    if proj["link_text"]:
        lx = COL1_X + 204
        page.insert_text(fitz.Point(lx, y1 + 8), proj["link_text"], fontname="FBold", fontsize=7.5, color=C_GREEN_DARK)
        page.insert_link(
            {
                "kind": fitz.LINK_URI,
                "from": fitz.Rect(lx, y1 - 1, lx + 74, y1 + 10),
                "uri": proj["link_url"],
            }
        )
    y1 += 11
    page.insert_text(fitz.Point(COL1_X, y1 + 8), proj["role"], fontname="FBold", fontsize=8.0, color=C_DARK)
    y1 += 11.5

    # Tech stack pill badge
    stk_rect = fitz.Rect(COL1_X, y1 - 1, COL1_X + COL1_W, y1 + 11.5)
    page.draw_rect(stk_rect, color=rgb(167, 243, 208), fill=C_GREEN_PALE, width=0.7)
    page.insert_text(fitz.Point(COL1_X + 5, y1 + 8.0), proj["stack"], fontname="FBold", fontsize=7.3, color=C_GREEN_DARK)
    y1 += 14.5

    for b in proj["bullets"]:
        draw_bullet_dot(COL1_X, y1, C_BLUE_MAIN)
        y1 = draw_wrapped_text(
            COL1_X + 9, y1, COL1_W - 9, b, font_reg_obj, "FReg", 7.9, C_TEXT, line_height=10.5
        )
        y1 += 1.5
    y1 += 4.5

# EDUCATION Section in Left Column
y1 += 2
y1 = draw_ribbon(COL1_X, y1, 150, COL1_W, "EDUCATION", "A")

page.insert_text(
    fitz.Point(COL1_X, y1 + 8.5),
    "Institut Sains dan Teknologi Terpadu Surabaya (iSTTS)",
    fontname="FBold",
    fontsize=9.1,
    color=C_BLUE_MAIN,
)
y1 += 11.5
page.insert_text(
    fitz.Point(COL1_X, y1 + 8.5),
    "Bachelor of Informatics / Sarjana Komputer (S.Kom.)",
    fontname="FBold",
    fontsize=8.3,
    color=C_DARK,
)
y1 += 11
page.insert_text(
    fitz.Point(COL1_X, y1 + 8.5),
    "Surabaya, Indonesia  |  Graduated: Nov 2026  |  147 Credits (GPA: 2.97 / 4.00)",
    fontname="FSemi",
    fontsize=7.8,
    color=C_MUTED,
)
y1 += 13

edu_highlights = [
    "Focus: Cross-Platform Mobile Engineering, Full-Stack Web Systems, Database Architecture, and AI-Augmented Software Development.",
    "Thesis Project: Built Sprout Tycoon (Flutter & Flame 2D simulation game with real-time Midtrans QRIS payment gateway integration).",
]
for eh in edu_highlights:
    draw_bullet_dot(COL1_X, y1, C_GREEN_MAIN)
    y1 = draw_wrapped_text(
        COL1_X + 9, y1, COL1_W - 9, eh, font_reg_obj, "FReg", 7.8, C_TEXT, line_height=10.4
    )
    y1 += 2

# CORE CAPABILITIES Section (Bottom of Left Column)
y1 += 4
y1 = draw_ribbon(COL1_X, y1, 158, COL1_W, "CORE CAPABILITIES", "S")
caps = [
    (
        "AI-Accelerated Full-Stack & Rapid Prototyping:",
        "Transforming business wireframes into functional MVPs & production apps via structured AI prompting & rigorous debugging.",
    ),
    (
        "Cross-Platform Mobile & Web Dashboards:",
        "End-to-end Flutter Android/iOS APK deployment and responsive React & Node.js web apps with Firebase & SQLite.",
    ),
    (
        "Custom POS & LLM API Integration:",
        "Tailored Python desktop POS with thermal receipt printing, Gemini AI smart assistants, and Midtrans QRIS payments.",
    ),
]
for c_title, c_desc in caps:
    draw_bullet_dot(COL1_X, y1, C_BLUE_MAIN)
    page.insert_text(fitz.Point(COL1_X + 9, y1 + 8), c_title, fontname="FBold", fontsize=7.9, color=C_DARK)
    y1 += 10.5
    y1 = draw_wrapped_text(
        COL1_X + 9, y1, COL1_W - 9, c_desc, font_reg_obj, "FReg", 7.6, C_TEXT, line_height=10.0
    )
    y1 += 3

# ------------------------------------------------------------------------------
# RIGHT COLUMN: 1) KEY TECHNICAL SKILLS  2) COMPETENCY BARS  3) CERTIFICATIONS
# ------------------------------------------------------------------------------
y2 = draw_ribbon(COL2_X, BODY_TOP_Y, 158, COL2_W, "KEY TECHNICAL SKILLS", "K")

skill_groups = [
    (
        "1. AI & LLM Engineering Workflow",
        True,
        [
            "Prompt Engineering",
            "AI-Assisted Full-Stack Dev",
            "ChatGPT & Google Gemini",
            "LLM / Gemini API Integration",
            "Rapid MVP Prototyping",
            "AI Debugging & Optimization",
        ],
    ),
    (
        "2. Mobile & Desktop Development",
        False,
        [
            "Flutter",
            "Dart",
            "Flame 2D Engine",
            "Android APK Build",
            "Python (CustomTkinter)",
            "ESC/POS Thermal Printer",
        ],
    ),
    (
        "3. Web Frontend, Backend & APIs",
        True,
        [
            "React.js",
            "JavaScript (ES6+)",
            "HTML5 & CSS3",
            "Node.js & Express.js",
            "RESTful APIs",
            "Midtrans QRIS API",
            "Google Drive API",
        ],
    ),
    (
        "4. Databases, Cloud & DevOps Tools",
        False,
        [
            "Firebase (Auth, Firestore, RTDB)",
            "SQLite",
            "MongoDB",
            "Git & GitHub",
            "Linux (RHEL & Mint)",
            "AWS & GCP Cloud Labs",
            "VS Code",
        ],
    ),
]

for grp_title, is_green, tags in skill_groups:
    page.insert_text(fitz.Point(COL2_X, y2 + 7.5), grp_title.upper(), fontname="FBold", fontsize=7.8, color=C_BLUE_MAIN)
    y2 += 11

    cur_tx = COL2_X
    row_h = 13.5
    for tag in tags:
        tw = font_semi_obj.text_length(tag, fontsize=7.3) + 10.5
        if cur_tx + tw > COL2_X + COL2_W:
            cur_tx = COL2_X
            y2 += row_h + 2
        t_rect = fitz.Rect(cur_tx, y2 - 1, cur_tx + tw, y2 + 11.5)
        bg = C_GREEN_PALE if is_green else C_TAG_BG
        accent = C_GREEN_MAIN if is_green else C_BLUE_LIGHT
        page.draw_rect(t_rect, color=None, fill=bg)
        page.draw_rect(fitz.Rect(cur_tx, y2 - 1, cur_tx + 2.5, y2 + 11.5), color=None, fill=accent)
        page.insert_text(fitz.Point(cur_tx + 5.2, y2 + 7.9), tag, fontname="FSemi", fontsize=7.3, color=C_DARK)
        cur_tx += tw + 3.5
    y2 += row_h + 5

# Visual Core Competency Bars (Directly Inspired by Reference Image Bottom-Right Bars)
y2 += 1
page.insert_text(
    fitz.Point(COL2_X, y2 + 7.5),
    "CORE ENGINEERING PROFICIENCY",
    fontname="FBold",
    fontsize=7.9,
    color=C_DARK,
)
y2 += 11

bars = [
    ("Prompt Engineering & AI-Augmented Coding", 0.96),
    ("Flutter & Cross-Platform Mobile Development", 0.94),
    ("Full-Stack Web (React, Node.js, REST APIs)", 0.89),
    ("Python Desktop POS & SQLite Database Systems", 0.92),
    ("Cloud, Firebase & Payment Gateway Integration", 0.90),
]

for label, pct in bars:
    page.insert_text(fitz.Point(COL2_X, y2 + 7.0), label, fontname="FSemi", fontsize=7.4, color=C_DARK)
    y2 += 9.2
    draw_gradient_bar(COL2_X, y2, COL2_W, 5.8, pct)
    y2 += 9.2

# CERTIFICATIONS & CREDENTIALS Section in Right Column
y2 += 5
y2 = draw_ribbon(COL2_X, y2, 158, COL2_W, "CERTIFICATIONS & BADGES", "C")

certs = [
    (
        "Google Cloud Skills Boost",
        "Generative AI Leader Learning Path & Load Balancers Lab",
        "Hands-on enterprise Generative AI workflows & cloud load balancing infrastructure.",
    ),
    (
        "AWS SimuLearn",
        "Cloud Architecture & Practical Labs",
        "Applied AWS cloud architecture scenarios, compute provisioning & resilient cloud design.",
    ),
    (
        "Google Developer Groups (GDG on Campus iSTTS)",
        "Future Builders Workshop Participant",
        "Collaborative software engineering & modern AI-augmented developer workflows.",
    ),
]

for issuer, cname, cdesc in certs:
    page.insert_text(fitz.Point(COL2_X, y2 + 7.8), issuer, fontname="FBold", fontsize=8.0, color=C_BLUE_MAIN)
    y2 += 10
    y2 = draw_wrapped_text(COL2_X, y2, COL2_W, cname, font_bold_obj, "FBold", 7.6, C_DARK, line_height=9.8)
    y2 = draw_wrapped_text(COL2_X, y2, COL2_W, cdesc, font_reg_obj, "FReg", 7.3, C_MUTED, line_height=9.5)
    y2 += 2.5
    page.draw_line(fitz.Point(COL2_X, y2), fitz.Point(COL2_X + COL2_W, y2), color=C_LINE, width=0.6)
    y2 += 2.5

# Official Credly Verification Highlight Box
cred_box = fitz.Rect(COL2_X, y2 + 1, COL2_X + COL2_W, y2 + 25)
page.draw_rect(cred_box, color=C_GREEN_MAIN, fill=C_GREEN_PALE, width=1.0)
page.insert_text(
    fitz.Point(COL2_X + 7, y2 + 10.5),
    "VERIFIED DIGITAL BADGES (CREDLY):",
    fontname="FBold",
    fontsize=7.2,
    color=C_GREEN_DARK,
)
page.insert_text(
    fitz.Point(COL2_X + 7, y2 + 20.5),
    "https://www.credly.com/users/rey-kamadjaya",
    fontname="FBold",
    fontsize=7.6,
    color=C_BLUE_MAIN,
)
page.insert_link(
    {
        "kind": fitz.LINK_URI,
        "from": cred_box,
        "uri": "https://www.credly.com/users/rey-kamadjaya",
    }
)

# ==============================================================================
# BOTTOM CONTACT FOOTER BAR (Matches Reference Image Bottom Blue Strip)
# ==============================================================================
BAR_H = 30
BAR_Y = H - BAR_H
page.draw_rect(fitz.Rect(0, BAR_Y, W, H), color=None, fill=C_BLUE_MAIN)
page.draw_rect(fitz.Rect(W * 0.68, BAR_Y, W, H), color=None, fill=C_GREEN_DARK)

footer_items = [
    ("WA", "+62 813-5300-2672", "https://wa.me/6281353002672", 26),
    ("@", "reykamadjaya@gmail.com", "mailto:reykamadjaya@gmail.com", 160),
    ("WEB", "reynaldy4699.github.io", "https://reynaldy4699.github.io/", 318),
    ("CREDLY", "credly.com/users/rey-kamadjaya", "https://www.credly.com/users/rey-kamadjaya", 436),
]

for badge, text, url, fx in footer_items:
    by = BAR_Y + 8
    bw = font_bold_obj.text_length(badge, fontsize=6.8) + 8
    page.draw_rect(fitz.Rect(fx, by, fx + bw, by + 14), color=C_WHITE, fill=None, width=1.1)
    page.insert_text(fitz.Point(fx + 4, by + 9.8), badge, fontname="FBold", fontsize=6.8, color=C_WHITE)
    tx = fx + bw + 5
    page.insert_text(fitz.Point(tx, by + 10.2), text, fontname="FBold", fontsize=7.8, color=C_WHITE)
    tw_link = font_bold_obj.text_length(text, fontsize=7.8)
    page.insert_link(
        {
            "kind": fitz.LINK_URI,
            "from": fitz.Rect(fx, BAR_Y, tx + tw_link + 4, H),
            "uri": url,
        }
    )

out_pdf = os.path.join(os.path.dirname(__file__), "CV_Reynard_Kamadjaja.pdf")
doc.save(out_pdf)

# Also save a preview PNG to verify visually
pix = page.get_pixmap(dpi=180)
preview_png = os.path.join(os.path.dirname(__file__), "CV_Preview.png")
pix.save(preview_png)
doc.close()
print("Saved PDF successfully:", out_pdf)
