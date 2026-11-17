import pymupdf as fitz  # PyMuPDF
import os

# A4 dimensions in points: 595.28 x 841.89
W, H = fitz.paper_size("a4")

doc = fitz.open()
page = doc.new_page(width=W, height=H)

# Use Windows Verdana font family:
# Clean modern sans-serif where uppercase 'I' has explicit top/bottom horizontal bars,
# so 'AI' and 'UI' are NEVER misread as 'Al' or 'Ul' by OCR or human readers.
font_dir = r"C:\Windows\Fonts"
f_reg = os.path.join(font_dir, "verdana.ttf")
f_bold = os.path.join(font_dir, "verdanab.ttf")
f_ital = os.path.join(font_dir, "verdanai.ttf")
f_bi = os.path.join(font_dir, "verdanaz.ttf")

font_reg_obj = fitz.Font(fontfile=f_reg)
font_bold_obj = fitz.Font(fontfile=f_bold)
font_ital_obj = fitz.Font(fontfile=f_ital)
font_bi_obj = fitz.Font(fontfile=f_bi)

page.insert_font(fontname="FReg", fontfile=f_reg)
page.insert_font(fontname="FBold", fontfile=f_bold)
page.insert_font(fontname="FItal", fontfile=f_ital)
page.insert_font(fontname="FBI", fontfile=f_bi)


def rgb(r, g, b):
    return (r / 255.0, g / 255.0, b / 255.0)


# Exact Color Palette Recommended by Recruiter Review:
C_NAVY = rgb(15, 23, 42)        # #0F172A - Full Name & Primary Bold Headers
C_BLUE_DARK = rgb(30, 58, 138)  # #1E3A8A - Section Headers, Divider Line & Tech Stack Accent
C_CHARCOAL = rgb(31, 41, 55)    # #1F2937 - Body Text / Bullet Points
C_MUTED = rgb(75, 85, 99)       # #4B5563 - Secondary Subtitle / Role
C_LINK = rgb(2, 132, 199)       # #0284C7 - Hyperlinks

# Page Margins: 38 pt (~1.34 cm) on all sides
MARGIN_X = 38.0
CONTENT_W = W - (MARGIN_X * 2)  # 519.28 pt


# Helper: Draw wrapped text paragraph (single-spaced words, strict top-to-bottom order)
def draw_wrapped_text(x, y, max_w, text, font_obj, fontname, fontsize, color, line_height=12.4):
    clean_text = " ".join(text.split())
    words = clean_text.split(" ")
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
            fitz.Point(x, y + fontsize + idx * line_height),
            ln,
            fontname=fontname,
            fontsize=fontsize,
            color=color,
        )
    return y + len(lines) * line_height


# Helper: Draw Section Header (11pt Bold ALL CAPS #1E3A8A + Crisp Full-Width Horizontal Rule)
def draw_section_header(y, title):
    y += 9.5  # 9.5pt whitespace before new section
    page.insert_text(
        fitz.Point(MARGIN_X, y + 10.5),
        title.upper(),
        fontname="FBold",
        fontsize=10.5,
        color=C_BLUE_DARK,
    )
    line_y = y + 14.5
    # Crisp full-width horizontal divider line in #1E3A8A
    page.draw_line(
        fitz.Point(MARGIN_X, line_y),
        fitz.Point(MARGIN_X + CONTENT_W, line_y),
        color=C_BLUE_DARK,
        width=1.35,
    )
    return line_y + 6.5


# Helper: Draw Bullet Point using real Unicode bullet character "•" so ATS & OCR always read it
def draw_bullet(y, text, fontsize=8.6, line_height=11.8):
    bullet_char = "\u2022"
    page.insert_text(
        fitz.Point(MARGIN_X + 2.0, y + fontsize),
        bullet_char,
        fontname="FBold",
        fontsize=fontsize,
        color=C_BLUE_DARK,
    )
    return draw_wrapped_text(
        MARGIN_X + 12.0,
        y,
        CONTENT_W - 12.0,
        text,
        font_reg_obj,
        "FReg",
        fontsize,
        C_CHARCOAL,
        line_height=line_height,
    )


# Helper: Draw Inline Bold-Label + Regular-Text Paragraph (for Technical Skills without table/pipe '|')
def draw_inline_skill_bullet(y, bold_label, regular_items, fontsize=8.5, line_height=11.8):
    bullet_char = "\u2022"
    page.insert_text(
        fitz.Point(MARGIN_X + 2.0, y + fontsize),
        bullet_char,
        fontname="FBold",
        fontsize=fontsize,
        color=C_BLUE_DARK,
    )
    start_x = MARGIN_X + 12.0
    max_w = CONTENT_W - 12.0

    # Draw bold category title at the start of line 1
    label_str = bold_label.strip() + " "
    label_w = font_bold_obj.text_length(label_str, fontsize=fontsize)
    page.insert_text(
        fitz.Point(start_x, y + fontsize),
        label_str,
        fontname="FBold",
        fontsize=fontsize,
        color=C_NAVY,
    )

    # Wrap the rest of the text starting on line 1 right after label_w, then full width on line 2+
    words = " ".join(regular_items.split()).split(" ")
    line1 = ""
    idx_word = 0
    rem_w_line1 = max_w - label_w

    while idx_word < len(words):
        test = (line1 + " " + words[idx_word]).strip()
        if font_reg_obj.text_length(test, fontsize=fontsize) <= rem_w_line1:
            line1 = test
            idx_word += 1
        else:
            break

    if line1:
        page.insert_text(
            fitz.Point(start_x + label_w, y + fontsize),
            line1,
            fontname="FReg",
            fontsize=fontsize,
            color=C_CHARCOAL,
        )

    # Remaining words wrap onto subsequent lines starting at start_x
    rem_lines = []
    cur_ln = ""
    while idx_word < len(words):
        w = words[idx_word]
        test = (cur_ln + " " + w).strip()
        if font_reg_obj.text_length(test, fontsize=fontsize) <= max_w:
            cur_ln = test
        else:
            if cur_ln:
                rem_lines.append(cur_ln)
            cur_ln = w
        idx_word += 1
    if cur_ln:
        rem_lines.append(cur_ln)

    for r_idx, r_ln in enumerate(rem_lines):
        page.insert_text(
            fitz.Point(start_x, y + fontsize + (r_idx + 1) * line_height),
            r_ln,
            fontname="FReg",
            fontsize=fontsize,
            color=C_CHARCOAL,
        )

    total_lines = 1 + len(rem_lines)
    return y + total_lines * line_height


# ==============================================================================
# 1. HEADER SECTION (LEFT: NAME, TITLE, CONTACT | RIGHT: 3x4 PASSPORT PHOTO)
# ==============================================================================
cur_y = 32.0

# 3x4 Proportional Portrait Photo on Top Right (Aligned with Header)
PHOTO_W = 63.0   # 3x4 ratio
PHOTO_H = 84.0   # 3x4 ratio
PHOTO_X = MARGIN_X + CONTENT_W - PHOTO_W
PHOTO_Y = cur_y

page.draw_rect(
    fitz.Rect(PHOTO_X - 1.2, PHOTO_Y - 1.2, PHOTO_X + PHOTO_W + 1.2, PHOTO_Y + PHOTO_H + 1.2),
    color=C_BLUE_DARK,
    fill=(1, 1, 1),
    width=1.0,
)
photo_path = os.path.join(os.path.dirname(__file__), "profile_cropped_elbow.jpg")
page.insert_image(
    fitz.Rect(PHOTO_X, PHOTO_Y, PHOTO_X + PHOTO_W, PHOTO_Y + PHOTO_H),
    filename=photo_path,
)

# Full Name (20pt Bold Navy #0F172A)
page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 18.0),
    "REYNARD KAMADJAJA, S.Kom.",
    fontname="FBold",
    fontsize=19.5,
    color=C_NAVY,
)
cur_y += 24.5

# Professional Title
page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 10.0),
    "AI-Augmented Full-Stack & Mobile App Developer | Software Engineer",
    fontname="FBold",
    fontsize=9.8,
    color=C_BLUE_DARK,
)
cur_y += 16.0

# Contact Line 1
c_line1 = "Surabaya, East Java, Indonesia  •  +62 813-5300-2672  •  reykamadjaya@gmail.com"
page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 8.5),
    c_line1,
    fontname="FReg",
    fontsize=8.4,
    color=C_CHARCOAL,
)
page.insert_link(
    {
        "kind": fitz.LINK_URI,
        "from": fitz.Rect(MARGIN_X + 150, cur_y, MARGIN_X + 245, cur_y + 11),
        "uri": "https://wa.me/6281353002672",
    }
)
page.insert_link(
    {
        "kind": fitz.LINK_URI,
        "from": fitz.Rect(MARGIN_X + 255, cur_y, MARGIN_X + 390, cur_y + 11),
        "uri": "mailto:reykamadjaya@gmail.com",
    }
)
cur_y += 13.0

# Contact Line 2 (Portfolio & Credly)
c_line2 = "Portfolio: reynaldy4699.github.io  •  Credly: credly.com/users/rey-kamadjaya"
page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 8.5),
    c_line2,
    fontname="FBold",
    fontsize=8.4,
    color=C_BLUE_DARK,
)
page.insert_link(
    {
        "kind": fitz.LINK_URI,
        "from": fitz.Rect(MARGIN_X + 45, cur_y, MARGIN_X + 170, cur_y + 11),
        "uri": "https://reynaldy4699.github.io/",
    }
)
page.insert_link(
    {
        "kind": fitz.LINK_URI,
        "from": fitz.Rect(MARGIN_X + 215, cur_y, MARGIN_X + 385, cur_y + 11),
        "uri": "https://www.credly.com/users/rey-kamadjaya",
    }
)
cur_y += 13.0

# Contact Line 3 (Status & Languages)
c_line3 = "Status: Open to Work (Full-Time, Remote, Freelance)  •  Languages: Indonesian (Native), English (Pro)"
page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 8.5),
    c_line3,
    fontname="FReg",
    fontsize=7.9,
    color=C_MUTED,
)
cur_y = max(cur_y + 13.0, PHOTO_Y + PHOTO_H + 2.0)


# ==============================================================================
# 2. PROFESSIONAL SUMMARY
# ==============================================================================
cur_y = draw_section_header(cur_y, "PROFESSIONAL SUMMARY")

summary_text = (
    "Software Developer and Informatics graduate (S.Kom.) from Institut Sains dan Teknologi Terpadu Surabaya (iSTTS) "
    "who leverages AI-augmented development workflows to deliver high-quality, end-to-end software at rapid speed. "
    "By combining solid software architecture fundamentals with advanced Prompt Engineering and Large Language Models (LLMs), "
    "I efficiently bridge the gap between complex business ideas and production-ready code. Hands-on experience spans "
    "cross-platform mobile applications with real-time payment integrations, full-stack web apps, custom desktop POS systems, "
    "and Gemini AI chatbot integrations."
)
cur_y = draw_wrapped_text(
    MARGIN_X,
    cur_y,
    CONTENT_W,
    summary_text,
    font_reg_obj,
    "FReg",
    8.6,
    C_CHARCOAL,
    line_height=12.0,
)
cur_y += 1.5


# ==============================================================================
# 3. PROJECT EXPERIENCE (JAKE'S RESUME STYLE: TITLE LEFT | TECH STACK RIGHT)
# ==============================================================================
cur_y = draw_section_header(cur_y, "PROJECT EXPERIENCE")

projects = [
    {
        "title": "Sprout Tycoon – 2D Mobile Simulation & Idle Game",
        "stack": "Flutter, Dart, Flame Engine, Firebase, Midtrans QRIS",
        "role": "Lead Developer (Undergraduate Thesis Project)",
        "live_label": "",
        "live_url": "",
        "bullets": [
            "Built a 2D mobile simulation and idle farming game with a custom game loop, resource management mechanics, and responsive mobile UI using Flutter and Flame Engine.",
            "Integrated real-time in-app purchases using Midtrans QRIS payment gateway for premium currency transactions.",
            "Implemented cloud data synchronization and real-time player progress management via Firebase.",
        ],
    },
    {
        "title": "Toko Gembira – Desktop POS & Inventory System",
        "stack": "Python, CustomTkinter, SQLite, Thermal Printer ESC/POS",
        "role": "Full-Stack Desktop Software Developer",
        "live_label": "",
        "live_url": "",
        "bullets": [
            "Developed a custom desktop Point-of-Sale (POS) and warehouse inventory management application to streamline retail operations.",
            "Engineered real-time stock tracking, sales reporting, and local relational database management using SQLite.",
            "Built direct hardware integration to print transaction receipts automatically via physical ESC/POS thermal printers inside an intuitive cashier GUI.",
        ],
    },
    {
        "title": "Juanda City Park – Real Estate Portal & AI App",
        "stack": "Flutter, Gemini AI API, Google Drive API, Firebase, SQLite",
        "role": "Mobile & Frontend Developer",
        "live_label": "Live Web: juandacitypark.com",
        "live_url": "https://juandacitypark.com/",
        "bullets": [
            "Integrated a Gemini AI chatbot assistant to answer prospective buyers' inquiries and assist with property information in real time.",
            "Implemented secure user authentication via Firebase Auth and local user activity logging using SQLite.",
            "Built dynamic property asset and document management connected directly to Google Drive API.",
        ],
    },
]

for proj in projects:
    # Line 1: Project Name (Bold Left) + Tech Stack (Bold-Italic Blue Right on same baseline!)
    baseline_y = cur_y + 9.2
    page.insert_text(
        fitz.Point(MARGIN_X, baseline_y),
        proj["title"],
        fontname="FBold",
        fontsize=9.0,
        color=C_NAVY,
    )
    stack_w = font_ital_obj.text_length(proj["stack"], fontsize=8.0)
    page.insert_text(
        fitz.Point(MARGIN_X + CONTENT_W - stack_w, baseline_y),
        proj["stack"],
        fontname="FItal",
        fontsize=8.0,
        color=C_BLUE_DARK,
    )
    cur_y += 12.0

    # Line 2: Role (Italic Muted Left) + Optional Live URL (Right)
    role_baseline = cur_y + 8.5
    page.insert_text(
        fitz.Point(MARGIN_X, role_baseline),
        proj["role"],
        fontname="FItal",
        fontsize=8.3,
        color=C_MUTED,
    )
    if proj["live_label"]:
        lw = font_bold_obj.text_length(proj["live_label"], fontsize=8.2)
        lx = MARGIN_X + CONTENT_W - lw
        page.insert_text(
            fitz.Point(lx, role_baseline),
            proj["live_label"],
            fontname="FBold",
            fontsize=8.2,
            color=C_LINK,
        )
        page.insert_link(
            {
                "kind": fitz.LINK_URI,
                "from": fitz.Rect(lx, cur_y, lx + lw, cur_y + 10),
                "uri": proj["live_url"],
            }
        )
    cur_y += 11.5

    # Bullets
    for b in proj["bullets"]:
        cur_y = draw_bullet(cur_y, b, fontsize=8.5, line_height=11.6)
        cur_y += 1.2
    cur_y += 4.5


# ==============================================================================
# 4. TECHNICAL SKILLS (INLINE PARAGRAPH PER CATEGORY - NO TABLE / NO '|' PIPE)
# ==============================================================================
cur_y = draw_section_header(cur_y, "TECHNICAL SKILLS")

skill_rows = [
    (
        "AI & LLM Workflow:",
        "Prompt Engineering, AI-Assisted Full-Stack Development (ChatGPT, Google Gemini, AI Code Generation), LLM API Integration, Rapid MVP Prototyping, AI-Driven Debugging & Code Optimization",
    ),
    (
        "Mobile & Desktop:",
        "Flutter, Dart, Flame Engine, Python (CustomTkinter), Android APK Build, Thermal Printer ESC/POS Integration",
    ),
    (
        "Frontend & Backend Web:",
        "React, JavaScript (ES6+), HTML5, CSS3, Responsive UI Design, Node.js, Express.js, RESTful APIs, Midtrans Payment Gateway (QRIS), Google Drive API, Gemini API",
    ),
    (
        "Databases, Cloud & Tools:",
        "Firebase (Auth, Firestore, Realtime DB, Hosting), SQLite, MongoDB, Git, GitHub, Linux (Red Hat Enterprise Linux, Linux Mint), AWS Cloud Labs, Google Cloud Skills Boost, VS Code",
    ),
]

for cat_label, cat_items in skill_rows:
    cur_y = draw_inline_skill_bullet(cur_y, cat_label, cat_items, fontsize=8.5, line_height=11.6)
    cur_y += 2.2


# ==============================================================================
# 5. EDUCATION (STRICT TOP-TO-BOTTOM ORDER: HEADER -> SCHOOL & DATE -> DEGREE)
# ==============================================================================
cur_y = draw_section_header(cur_y, "EDUCATION")

edu_inst = "Institut Sains dan Teknologi Terpadu Surabaya (iSTTS)"
edu_date = "Graduated: Nov 2026 | 147 Credits"

edu_base_y = cur_y + 9.2
page.insert_text(
    fitz.Point(MARGIN_X, edu_base_y),
    edu_inst,
    fontname="FBold",
    fontsize=9.0,
    color=C_NAVY,
)
dw = font_bold_obj.text_length(edu_date, fontsize=8.4)
page.insert_text(
    fitz.Point(MARGIN_X + CONTENT_W - dw, edu_base_y),
    edu_date,
    fontname="FBold",
    fontsize=8.4,
    color=C_BLUE_DARK,
)
cur_y += 12.5

page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 8.8),
    "Bachelor of Informatics / Sarjana Komputer (S.Kom.) – Surabaya, Indonesia",
    fontname="FItal",
    fontsize=8.6,
    color=C_CHARCOAL,
)
cur_y += 12.0


# ==============================================================================
# 6. CERTIFICATIONS & CREDENTIALS (UNIFORM TEXT BULLETS "•" ON EVERY ROW)
# ==============================================================================
cur_y = draw_section_header(cur_y, "CERTIFICATIONS & CREDENTIALS")

certs = [
    "Google Cloud Skills Boost: Generative AI Leader Learning Path, Set Up Application Load Balancers Lab",
    "AWS SimuLearn: Cloud Architecture & Practical Labs",
    "Google Developer Groups (GDG on Campus iSTTS): Future Builders Workshop Participant",
    "Verified Digital Badges (Credly): https://www.credly.com/users/rey-kamadjaya",
]

for c_text in certs:
    y_before = cur_y
    cur_y = draw_bullet(cur_y, c_text, fontsize=8.5, line_height=11.6)
    if "credly.com" in c_text:
        page.insert_link(
            {
                "kind": fitz.LINK_URI,
                "from": fitz.Rect(MARGIN_X + 12.0, y_before, MARGIN_X + 380, cur_y),
                "uri": "https://www.credly.com/users/rey-kamadjaya",
            }
        )
    cur_y += 1.8

out_pdf = os.path.join(os.path.dirname(__file__), "CV_Reynard_Kamadjaja.pdf")
doc.save(out_pdf)

# Save high-resolution preview PNG
pix = page.get_pixmap(dpi=180)
preview_png = os.path.join(os.path.dirname(__file__), "CV_Preview.png")
pix.save(preview_png)

extracted_text = page.get_text("text")
doc.close()

print("Saved PDF successfully:", out_pdf)
print("Final Y coordinate:", round(cur_y, 1), "/ Page Height:", round(H, 1))
print("\n--- ATS EXTRACTED TEXT ORDER ---")
print(extracted_text)
