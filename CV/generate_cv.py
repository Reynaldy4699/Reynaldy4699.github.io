import pymupdf as fitz  # PyMuPDF
import os

# A4 dimensions in points: 595.28 x 841.89
W, H = fitz.paper_size("a4")

doc = fitz.open()
page = doc.new_page(width=W, height=H)

# Load Windows Calibri fonts (Industry-standard ATS font)
font_dir = r"C:\Windows\Fonts"
f_reg = os.path.join(font_dir, "calibri.ttf")
f_bold = os.path.join(font_dir, "calibrib.ttf")
f_ital = os.path.join(font_dir, "calibrii.ttf")

if not os.path.exists(f_reg):
    f_reg = os.path.join(font_dir, "segoeui.ttf")
    f_bold = os.path.join(font_dir, "segoeuib.ttf")
    f_ital = os.path.join(font_dir, "segoeuii.ttf")

font_reg_obj = fitz.Font(fontfile=f_reg)
font_bold_obj = fitz.Font(fontfile=f_bold)
font_ital_obj = fitz.Font(fontfile=f_ital)

page.insert_font(fontname="FReg", fontfile=f_reg)
page.insert_font(fontname="FBold", fontfile=f_bold)
page.insert_font(fontname="FItal", fontfile=f_ital)


def rgb(r, g, b):
    return (r / 255.0, g / 255.0, b / 255.0)


# Clean, Executive Blue & Teal-Green Palette (Recruiter & ATS Friendly)
C_NAVY = rgb(15, 23, 42)        # #0f172a - Headings & Primary Bold Text
C_BLUE = rgb(2, 132, 199)       # #0284c7 - Section Titles & Links
C_TEAL = rgb(5, 150, 105)       # #059669 - Secondary Accent
C_TEXT = rgb(30, 41, 59)        # #1e293b - Body Text
C_MUTED = rgb(71, 85, 105)      # #475569 - Dates / Subtitles
C_LINE = rgb(203, 213, 225)     # #cbd5e1 - Horizontal Divider

MARGIN_X = 40.0
CONTENT_W = W - (MARGIN_X * 2)  # 515.28 pt full single-column width

# Top subtle accent bar (4pt)
page.draw_rect(fitz.Rect(0, 0, W * 0.6, 4), color=None, fill=C_BLUE)
page.draw_rect(fitz.Rect(W * 0.6, 0, W, 4), color=None, fill=C_TEAL)


# Helper: Draw wrapped paragraph in strict top-to-bottom order (single spaces only)
def draw_wrapped_text(x, y, max_w, text, font_obj, fontname, fontsize, color, line_height=13.0):
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


# Helper: Draw Clean Plain-Text Section Heading + Horizontal Divider (Zero icon artifacts)
def draw_section_header(y, title):
    y += 6.5
    page.insert_text(
        fitz.Point(MARGIN_X, y + 10.5),
        title.upper(),
        fontname="FBold",
        fontsize=10.8,
        color=C_BLUE,
    )
    line_y = y + 14.5
    page.draw_line(
        fitz.Point(MARGIN_X, line_y),
        fitz.Point(MARGIN_X + 120, line_y),
        color=C_TEAL,
        width=1.8,
    )
    page.draw_line(
        fitz.Point(MARGIN_X + 120, line_y),
        fitz.Point(MARGIN_X + CONTENT_W, line_y),
        color=C_LINE,
        width=1.0,
    )
    return line_y + 6.5


# Helper: Draw Bullet Item (Vector dot so zero font glyph issues in ATS)
def draw_bullet(y, text, max_w=CONTENT_W):
    page.draw_circle(fitz.Point(MARGIN_X + 4.0, y + 6.2), 1.8, color=None, fill=C_BLUE)
    return draw_wrapped_text(
        MARGIN_X + 12.0,
        y,
        max_w - 12.0,
        text,
        font_reg_obj,
        "FReg",
        9.6,
        C_TEXT,
        line_height=12.4,
    )


# ==============================================================================
# 1. HEADER SECTION (LEFT: NAME, TITLE, CONTACT | RIGHT: 3x4 PASSPORT PHOTO)
# ==============================================================================
cur_y = 30.0

# 3x4 Proportional Portrait Photo on Top Right (Aligned with Header Only)
PHOTO_W = 66.0   # ~2.33 cm (3x4 ratio)
PHOTO_H = 88.0   # ~3.10 cm (3x4 ratio)
PHOTO_X = MARGIN_X + CONTENT_W - PHOTO_W
PHOTO_Y = cur_y

# Crisp thin frame around 3x4 photo
page.draw_rect(
    fitz.Rect(PHOTO_X - 1.5, PHOTO_Y - 1.5, PHOTO_X + PHOTO_W + 1.5, PHOTO_Y + PHOTO_H + 1.5),
    color=C_BLUE,
    fill=(1, 1, 1),
    width=1.2,
)
photo_path = os.path.join(os.path.dirname(__file__), "profile_cropped_elbow.jpg")
page.insert_image(
    fitz.Rect(PHOTO_X, PHOTO_Y, PHOTO_X + PHOTO_W, PHOTO_Y + PHOTO_H),
    filename=photo_path,
)

# Full Name & Degree
page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 20.0),
    "REYNARD KAMADJAJA, S.Kom.",
    fontname="FBold",
    fontsize=22.0,
    color=C_NAVY,
)
cur_y += 28.0

# Professional Title
page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 10.5),
    "AI-Augmented Full-Stack & Mobile App Developer | Software Engineer",
    fontname="FBold",
    fontsize=11.2,
    color=C_BLUE,
)
cur_y += 18.0

# Contact Line 1: Location, Phone/WhatsApp, Email
contact_line_1 = "Surabaya, East Java, Indonesia | +62 813-5300-2672 | reykamadjaya@gmail.com"
page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 9.5),
    contact_line_1,
    fontname="FReg",
    fontsize=9.5,
    color=C_TEXT,
)
page.insert_link(
    {
        "kind": fitz.LINK_URI,
        "from": fitz.Rect(MARGIN_X + 135, cur_y, MARGIN_X + 220, cur_y + 12),
        "uri": "https://wa.me/6281353002672",
    }
)
page.insert_link(
    {
        "kind": fitz.LINK_URI,
        "from": fitz.Rect(MARGIN_X + 228, cur_y, MARGIN_X + 355, cur_y + 12),
        "uri": "mailto:reykamadjaya@gmail.com",
    }
)
cur_y += 14.5

# Contact Line 2: Portfolio Website & Credly Link
c2_prefix = "Portfolio: "
c2_port = "reynaldy4699.github.io"
c2_sep = " | Credly Badges: "
c2_cred = "credly.com/users/rey-kamadjaya"

x_cursor = MARGIN_X
page.insert_text(fitz.Point(x_cursor, cur_y + 9.5), c2_prefix, fontname="FBold", fontsize=9.5, color=C_NAVY)
x_cursor += font_bold_obj.text_length(c2_prefix, fontsize=9.5)

page.insert_text(fitz.Point(x_cursor, cur_y + 9.5), c2_port, fontname="FBold", fontsize=9.5, color=C_BLUE)
w_port = font_bold_obj.text_length(c2_port, fontsize=9.5)
page.insert_link(
    {
        "kind": fitz.LINK_URI,
        "from": fitz.Rect(x_cursor, cur_y, x_cursor + w_port, cur_y + 12),
        "uri": "https://reynaldy4699.github.io/",
    }
)
x_cursor += w_port

page.insert_text(fitz.Point(x_cursor, cur_y + 9.5), c2_sep, fontname="FBold", fontsize=9.5, color=C_NAVY)
x_cursor += font_bold_obj.text_length(c2_sep, fontsize=9.5)

page.insert_text(fitz.Point(x_cursor, cur_y + 9.5), c2_cred, fontname="FBold", fontsize=9.5, color=C_BLUE)
w_cred = font_bold_obj.text_length(c2_cred, fontsize=9.5)
page.insert_link(
    {
        "kind": fitz.LINK_URI,
        "from": fitz.Rect(x_cursor, cur_y, x_cursor + w_cred, cur_y + 12),
        "uri": "https://www.credly.com/users/rey-kamadjaya",
    }
)
cur_y += 14.5

# Contact Line 3: Work Status & Languages (Comfortable margin from photo)
contact_line_3 = "Status: Open to Work (Full-Time, Remote, Freelance) | Languages: Indonesian (Native), English (Pro)"
page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 9.5),
    contact_line_3,
    fontname="FReg",
    fontsize=9.2,
    color=C_MUTED,
)
cur_y = max(cur_y + 15.0, PHOTO_Y + PHOTO_H + 4.0)


# ==============================================================================
# 2. PROFESSIONAL SUMMARY (FULL SINGLE-COLUMN WIDTH)
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
    9.7,
    C_TEXT,
    line_height=13.2,
)
cur_y += 2.0


# ==============================================================================
# 3. PROJECT EXPERIENCE (FULL SINGLE-COLUMN WIDTH)
# ==============================================================================
cur_y = draw_section_header(cur_y, "PROJECT EXPERIENCE")

projects = [
    {
        "title": "Sprout Tycoon - 2D Mobile Simulation & Idle Farming Game",
        "role": "Lead Developer (Undergraduate Thesis Project)",
        "live_label": "",
        "live_url": "",
        "stack": "Tech Stack: Flutter, Dart, Flame Engine, Firebase, Midtrans API (QRIS)",
        "bullets": [
            "Built a 2D mobile simulation and idle farming game with a custom game loop, resource management mechanics, and responsive mobile UI using Flutter and Flame Engine.",
            "Integrated real-time in-app purchases using Midtrans QRIS payment gateway for premium currency transactions.",
            "Implemented cloud data synchronization and real-time player progress management via Firebase.",
        ],
    },
    {
        "title": "Toko Gembira - Desktop POS & Inventory System",
        "role": "Full-Stack Desktop Software Developer",
        "live_label": "",
        "live_url": "",
        "stack": "Tech Stack: Python, CustomTkinter, SQLite, Thermal Printer ESC/POS Integration",
        "bullets": [
            "Developed a custom desktop Point-of-Sale (POS) and warehouse inventory management application to streamline retail operations.",
            "Engineered real-time stock tracking, sales reporting, and local relational database management using SQLite.",
            "Built direct hardware integration to print transaction receipts automatically via physical ESC/POS thermal printers inside an intuitive cashier GUI.",
        ],
    },
    {
        "title": "Juanda City Park - Multiplatform Real Estate Portal & AI Assistant App",
        "role": "Mobile & Frontend Developer",
        "live_label": "juandacitypark.com",
        "live_url": "https://juandacitypark.com/",
        "stack": "Tech Stack: Flutter, SQLite, Google Drive API, Firebase Authentication, Gemini AI API",
        "bullets": [
            "Integrated a Gemini AI chatbot assistant to answer prospective buyers' inquiries and assist with property information in real time.",
            "Implemented secure user authentication via Firebase Auth and local user activity logging using SQLite.",
            "Built dynamic property asset and document management connected directly to Google Drive API.",
        ],
    },
]

for proj in projects:
    # Row 1: Project Title (Left) + Role (Right)
    page.insert_text(
        fitz.Point(MARGIN_X, cur_y + 10.0),
        proj["title"],
        fontname="FBold",
        fontsize=10.4,
        color=C_NAVY,
    )
    role_w = font_bold_obj.text_length(proj["role"], fontsize=9.4)
    page.insert_text(
        fitz.Point(MARGIN_X + CONTENT_W - role_w, cur_y + 10.0),
        proj["role"],
        fontname="FBold",
        fontsize=9.4,
        color=C_TEAL,
    )
    cur_y += 13.5

    # Row 2: Tech Stack (+ optional live website link)
    page.insert_text(
        fitz.Point(MARGIN_X, cur_y + 9.2),
        proj["stack"],
        fontname="FItal",
        fontsize=9.2,
        color=C_MUTED,
    )
    if proj["live_label"]:
        lbl = "Live Web: " + proj["live_label"]
        lw = font_bold_obj.text_length(lbl, fontsize=9.0)
        lx = MARGIN_X + CONTENT_W - lw
        page.insert_text(
            fitz.Point(lx, cur_y + 9.2),
            lbl,
            fontname="FBold",
            fontsize=9.0,
            color=C_BLUE,
        )
        page.insert_link(
            {
                "kind": fitz.LINK_URI,
                "from": fitz.Rect(lx, cur_y, lx + lw, cur_y + 11),
                "uri": proj["live_url"],
            }
        )
    cur_y += 13.0

    # Bullets
    for b in proj["bullets"]:
        cur_y = draw_bullet(cur_y, b)
        cur_y += 1.5
    cur_y += 5.5


# ==============================================================================
# 4. TECHNICAL SKILLS (SINGLE CONSOLIDATED SECTION - 4 CLEAR CATEGORIES)
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

LABEL_COL_W = 122.0
for cat_label, cat_items in skill_rows:
    page.draw_circle(fitz.Point(MARGIN_X + 4.0, cur_y + 6.5), 1.9, color=None, fill=C_TEAL)
    page.insert_text(
        fitz.Point(MARGIN_X + 12.0, cur_y + 9.7),
        cat_label,
        fontname="FBold",
        fontsize=9.6,
        color=C_NAVY,
    )
    cur_y = draw_wrapped_text(
        MARGIN_X + 12.0 + LABEL_COL_W,
        cur_y,
        CONTENT_W - 12.0 - LABEL_COL_W,
        cat_items,
        font_reg_obj,
        "FReg",
        9.6,
        C_TEXT,
        line_height=12.8,
    )
    cur_y += 3.5


# ==============================================================================
# 5. EDUCATION (SINGLE-COLUMN, SIMPLIFIED CREDITS WITHOUT SUB-3.0 GPA)
# ==============================================================================
cur_y = draw_section_header(cur_y, "EDUCATION")

edu_inst = "Institut Sains dan Teknologi Terpadu Surabaya (iSTTS) - Surabaya, Indonesia"
edu_date = "Graduated: Nov 2026 | 147 Credits"

page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 10.0),
    edu_inst,
    fontname="FBold",
    fontsize=10.2,
    color=C_NAVY,
)
dw = font_bold_obj.text_length(edu_date, fontsize=9.4)
page.insert_text(
    fitz.Point(MARGIN_X + CONTENT_W - dw, cur_y + 10.0),
    edu_date,
    fontname="FBold",
    fontsize=9.4,
    color=C_TEAL,
)
cur_y += 13.5

page.insert_text(
    fitz.Point(MARGIN_X, cur_y + 9.5),
    "Bachelor of Informatics / Sarjana Komputer (S.Kom.)",
    fontname="FReg",
    fontsize=9.7,
    color=C_TEXT,
)
cur_y += 14.0


# ==============================================================================
# 6. CERTIFICATIONS & CREDENTIALS (FULL SINGLE-COLUMN WIDTH)
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
    cur_y = draw_bullet(cur_y, c_text)
    if "credly.com" in c_text:
        page.insert_link(
            {
                "kind": fitz.LINK_URI,
                "from": fitz.Rect(MARGIN_X + 12.0, y_before, MARGIN_X + 360, cur_y),
                "uri": "https://www.credly.com/users/rey-kamadjaya",
            }
        )
    cur_y += 2.0

out_pdf = os.path.join(os.path.dirname(__file__), "CV_Reynard_Kamadjaja.pdf")
doc.save(out_pdf)

# Save high-resolution preview PNG
pix = page.get_pixmap(dpi=180)
preview_png = os.path.join(os.path.dirname(__file__), "CV_Preview.png")
pix.save(preview_png)
doc.close()

print("Saved PDF successfully:", out_pdf)
print("Final Y coordinate:", round(cur_y, 1), "/ Page Height:", round(H, 1))
