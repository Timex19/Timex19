"""Generate self-contained SVG artwork and the GitHub profile README."""

from html import escape
from pathlib import Path
from urllib.parse import quote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def text(x, y, value, size=24, color="#E2E8F0", weight=400):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" font-family="Arial, Helvetica, sans-serif">'
            f'{escape(value)}</text>')


def canvas(name, height, content, title):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0B1220"/><stop offset="1" stop-color="#15263D"/></linearGradient>
<linearGradient id="accent"><stop stop-color="#5EEAD4"/><stop offset="1" stop-color="#60A5FA"/></linearGradient></defs>
<rect width="1000" height="{height}" rx="22" fill="url(#bg)"/>
<rect x="1" y="1" width="998" height="{height-2}" rx="21" fill="none" stroke="#334155"/>
{content}</svg>'''
    ET.fromstring(svg)
    (ASSETS / name).write_text(svg, encoding="utf-8")


hero = '<path d="M720 0V360M780 0V360M840 0V360M900 0V360M960 0V360M680 60H1000M680 120H1000M680 180H1000M680 240H1000M680 300H1000" stroke="#23364D" fill="none"/>'
hero += '<circle cx="866" cy="178" r="93" fill="#132A3B" stroke="#2D5363"/><circle cx="866" cy="178" r="72" fill="none" stroke="#5EEAD4" stroke-opacity=".35"/>'
hero += text(811, 197, "</>", 58, "#5EEAD4", 700)
hero += '<rect x="44" y="40" width="4" height="22" rx="2" fill="#5EEAD4"/>'
hero += text(60, 57, "SOFTWARE ENGINEERING / PRODUCT THINKING", 15, "#5EEAD4", 700)
hero += text(44, 128, "Ojo Timilehin", 55, "#F8FAFC", 700)
hero += text(44, 190, "Joseph", 55, "#F8FAFC", 700)
hero += text(46, 235, "Senior Software Engineer", 26, "#CBD5E1", 400)
hero += text(46, 272, "Backend  /  Mobile  /  Cloud", 22, "#5EEAD4", 700)
hero += '<rect x="44" y="306" width="604" height="1" fill="#334155"/>'
hero += text(46, 335, "NIGERIA   ·   REMOTE & INTERNATIONAL OPPORTUNITIES", 14, "#CBD5E1", 700)
canvas("hero.svg", 360, hero, "Ojo Timilehin Joseph — Senior Software Engineer. Backend, mobile and cloud. Based in Nigeria, open to remote and international opportunities.")

metrics = ""
for i, (value, label, sub) in enumerate([
    ("5+", "YEARS OF EXPERIENCE", "Web, mobile & backend"),
    ("30%", "PERFORMANCE GAIN", "Backend optimization"),
    ("25%+", "FASTER API RESPONSES", "Latency improvements"),
    ("5,000+", "USERS SERVED", "Applications built")
]):
    x = 32 + i * 244
    metrics += f'<rect x="{x}" y="24" width="224" height="166" rx="14" fill="#111F32" stroke="#2B4058"/>'
    metrics += text(x+18, 86, value, 44, "#5EEAD4", 700)
    metrics += text(x+18, 121, label, 12, "#F8FAFC", 700)
    metrics += text(x+18, 155, sub, 13, "#CBD5E1")
canvas("impact.svg", 214, metrics, "5+ years of experience; 30% performance improvement; 25%+ faster API responses; applications serving 5,000+ users.")

for filename, number, title, subtitle in [
    ("expertise.svg", "01", "ENGINEERING EXPERTISE", "From product requirements to dependable production systems"),
    ("technology.svg", "02", "TECHNOLOGY & TOOLKIT", "The tools I use across the full product lifecycle"),
    ("work.svg", "03", "SELECTED WORK", "Healthcare platforms, music experiences & systems foundations"),
    ("principles.svg", "04", "HOW I ENGINEER", "Clear decisions. Maintainable code. Measurable outcomes.")
]:
    body = text(28, 57, number, 32, "#5EEAD4", 700)
    body += '<path d="M96 25V76" stroke="#334155"/>'
    body += text(118, 44, title, 22, "#F8FAFC", 700)
    body += text(118, 73, subtitle, 16, "#CBD5E1")
    canvas(filename, 102, body, title + ". " + subtitle)

for filename, label, title, subtitle, tags, color in [
    ("mycyberclinics.svg", "HEALTHCARE / WEB & MOBILE", "MyCyberClinics", "Connecting patients, providers, and care operations.", "TELEHEALTH   /   PAYMENTS   /   ROLE-BASED ACCESS", "#5EEAD4"),
    ("shedtracks.svg", "MUSIC / WEB & MOBILE", "ShedTracks", "Music practice, playback, and purchase experiences.", "AUDIO PLAYBACK   /   METRONOME   /   SUBSCRIPTIONS", "#93C5FD")
]:
    body = f'<rect x="28" y="28" width="5" height="144" rx="2" fill="{color}"/>'
    body += text(52, 48, label, 14, color, 700)
    body += text(50, 103, title, 40, "#F8FAFC", 700)
    body += text(52, 140, subtitle, 20, "#CBD5E1")
    body += text(52, 180, tags, 13, color, 700)
    body += '<path d="M916 58L944 86L916 114M880 58L852 86L880 114" fill="none" stroke="#334D69" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    canvas(filename, 208, body, title + ". " + subtitle)

footer = text(36, 62, "LET'S BUILD SOMETHING USEFUL.", 32, "#F8FAFC", 700)
footer += text(36, 106, "Backend  ·  Full-stack  ·  Mobile  ·  Cloud", 22, "#5EEAD4")
footer += '<path d="M36 132H964" stroke="#334155"/>'
footer += text(36, 167, "OPEN TO REMOTE ROLES, INTERNATIONAL TEAMS & COLLABORATIONS", 14, "#CBD5E1", 700)
canvas("connect.svg", 198, footer, "Let's build something useful. Open to remote and international backend, full-stack, mobile and cloud roles and collaborations.")


def badges(names, color):
    result = ['<p>']
    for name in names:
        label = quote(name.replace("-", "--").replace("_", "__").replace(" ", "_"), safe="")
        result.append(f'  <img src="https://img.shields.io/badge/{label}-{color}?style=for-the-badge" alt="{escape(name, quote=True)}" />')
    return "\n".join(result + ['</p>'])


groups = [
    ("Languages & foundations", "334155", ["TypeScript", "JavaScript", "Python", "C", "HTML5", "CSS3", "Shell scripting", "Git", "GitHub"]),
    ("Frontend & mobile", "155E75", ["React", "React Native", "Expo", "Expo Router", "React Navigation", "Vite", "Tailwind CSS", "NativeWind", "Radix UI", "Zustand", "TanStack Query", "React Hook Form", "Zod", "i18next", "Reanimated", "Gesture Handler"]),
    ("Backend & asynchronous systems", "166534", ["Node.js", "Koa", "REST APIs", "Firebase Admin SDK", "Firebase Functions", "BullMQ", "node-cron", "Webhooks"]),
    ("Databases & storage", "1E40AF", ["MongoDB", "Mongoose", "PostgreSQL", "MySQL", "Cloud Firestore", "Redis", "Firebase Storage", "Google Cloud Storage"]),
    ("Cloud, infrastructure & delivery", "5B21B6", ["AWS", "Microsoft Azure", "Google Cloud", "Cloud Run", "Firebase Hosting", "Cloud Build", "Docker", "Docker Compose", "GitHub Actions", "Expo EAS", "Vercel", "Netlify", "Heroku"]),
    ("Payments & communication", "9A3412", ["Paystack", "Stripe", "RevenueCat", "SendGrid", "OneSignal", "Daily", "WebRTC"]),
    ("AI & content", "115E59", ["OpenAI API", "Sanity"]),
    ("Testing, quality & observability", "374151", ["Jest", "Vitest", "React Testing Library", "React Native Testing Library", "Playwright", "Maestro", "Supertest", "ESLint", "Prettier", "Sentry", "Firebase Analytics"])
]

readme = '''<p align="center">
  <img src="./assets/hero.svg" width="100%" alt="Ojo Timilehin Joseph — Senior Software Engineer. Backend, mobile and cloud. Based in Nigeria, open to remote and international opportunities." />
</p>

<h1 align="center">Ojo Timilehin Joseph</h1>
<p align="center"><strong>Reliable systems. Thoughtful experiences. Software with purpose.</strong></p>

<p align="center">
  <a href="https://www.linkedin.com/in/timex19/"><img src="https://img.shields.io/badge/LinkedIn-CONNECT-0A66C2?style=for-the-badge" alt="Connect on LinkedIn" /></a>
  <a href="mailto:joseph@mycyberclinics.com"><img src="https://img.shields.io/badge/Email-GET_IN_TOUCH-115E59?style=for-the-badge" alt="Email Joseph" /></a>
  <a href="https://github.com/Timex19?tab=repositories"><img src="https://img.shields.io/badge/GitHub-EXPLORE_MY_WORK-334155?style=for-the-badge&logo=github&logoColor=white" alt="Explore my repositories" /></a>
</p>

<p align="center">
  <a href="#about-me">About</a> &nbsp; / &nbsp;
  <a href="#engineering-expertise">Expertise</a> &nbsp; / &nbsp;
  <a href="#technology--tools">Technology</a> &nbsp; / &nbsp;
  <a href="#selected-work">Projects</a> &nbsp; / &nbsp;
  <a href="#lets-connect">Connect</a>
</p>

## About me

I'm a **Senior Software Engineer with 5+ years of experience** building web applications, cross-platform mobile products, and dependable backend services. My core stack is **TypeScript, Node.js, React, and React Native**, with cloud experience across **AWS, Microsoft Azure, and Google Cloud**.

My work spans **healthcare, payments, subscriptions, and music applications**. With a background in **Business Administration**, I connect engineering decisions to user needs and business outcomes, from the first interface to deployment and ongoing support.

<p><img src="./assets/impact.svg" width="100%" alt="5+ years of experience; 30% application performance improvement; 25%+ faster API responses; applications serving 5,000+ users." /></p>

<details>
<summary><strong>Impact in detail</strong></summary>

- Improved application performance by **30%** through backend optimization.
- Reduced API response times by **25%+**.
- Built applications serving **5,000+ users**.
- Designed scalable APIs handling **10,000+ requests**.

</details>

## Engineering expertise

<p><img src="./assets/expertise.svg" width="100%" alt="Engineering expertise — From product requirements to dependable production systems" /></p>

<table>
  <tr>
    <td width="50%" valign="top"><h3>Backend & architecture</h3><p>REST APIs, modular services, background jobs, webhook processing, caching, and database optimization.</p></td>
    <td width="50%" valign="top"><h3>Web & mobile products</h3><p>Responsive React applications, React Native and Expo, accessible interfaces, state management, and complete product flows.</p></td>
  </tr>
  <tr>
    <td valign="top"><h3>Cloud & delivery</h3><p>Containerized applications, cloud deployment, automated delivery, secrets management, and release validation.</p></td>
    <td valign="top"><h3>Reliability & security</h3><p>Authentication, role-based access, input validation, payment verification, idempotency, retries, and observability.</p></td>
  </tr>
</table>

## Technology & tools

<p><img src="./assets/technology.svg" width="100%" alt="Technology and toolkit — Tools across the full product lifecycle" /></p>

'''

for title, color, names in groups:
    readme += f"### {title}\n\n{badges(names, color)}\n\n"

readme += '''## Selected work

<p><img src="./assets/work.svg" width="100%" alt="Selected work — Healthcare platforms, music experiences and systems foundations" /></p>

### MyCyberClinics

<p><img src="./assets/mycyberclinics.svg" width="100%" alt="MyCyberClinics — Healthcare platform connecting patients, providers and care operations. Telehealth, payments and role-based access." /></p>

- **Patient experience:** Onboarding, appointment booking, consultations, and health records across web and mobile.
- **Platform services:** Payments, subscriptions, transactional notifications, and administrative operations.
- **Reliability:** Payment verification, background reconciliation, access control, and backend performance improvements.

'''
readme += badges(["React Native", "Expo", "Koa", "MongoDB", "Redis", "Firebase", "Google Cloud", "Paystack"], "155E75")
readme += '''

### ShedTracks

<p><img src="./assets/shedtracks.svg" width="100%" alt="ShedTracks — Music practice and playback across web and mobile. Audio, metronome and subscription experiences." /></p>

- **Playback experience:** Responsive player interfaces, accessible controls, and mobile tempo adjustments.
- **Mobile reliability:** Work on the iOS background audio lifecycle and playback continuity.
- **Commerce:** Catalog browsing, store, subscription, and payment workflows with focused regression testing.

'''
readme += badges(["React", "React Native", "TypeScript", "Vite", "Radix UI", "Firebase", "Stripe", "RevenueCat"], "1E40AF")
readme += '''

<details>
<summary><strong>Explore my systems and web foundations</strong></summary>

| Project | Focus | Technology |
| :--- | :--- | :--- |
| [System Engineering & DevOps](https://github.com/Timex19/alx-system_engineering-devops) | System engineering coursework and command-line tooling | Shell |
| [Simple Shell](https://github.com/Timex19/simple_shell) | A command-line interpreter | C |
| [Responsive Restaurant Website](https://github.com/Timex19/Restaurant_Website) | Responsive frontend development | HTML, CSS, JavaScript |

</details>

## Engineering approach

<p><img src="./assets/principles.svg" width="100%" alt="How I engineer — Clear decisions, maintainable code and measurable outcomes" /></p>

| Understand | Build | Validate | Deliver |
| :--- | :--- | :--- | :--- |
| Connect requirements to user needs and business outcomes. | Use clear boundaries, strong typing, and established patterns. | Test behavior, measure performance, and plan recovery paths. | Consider deployment, monitoring, and ongoing support. |

<details>
<summary><strong>GitHub activity</strong></summary>

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=Timex19&show_icons=true&theme=github_dark&hide_border=true" alt="Timex19's public GitHub statistics" width="480" />
</p>

Public GitHub activity represents part of my work; professional projects also include private repositories.

</details>

## Let's connect

<p><img src="./assets/connect.svg" width="100%" alt="Let's build something useful — Open to remote and international backend, full-stack, mobile and cloud roles and collaborations" /></p>

<p align="center"><strong>Open to remote and international roles, meaningful products, and engineering collaborations.</strong></p>

<p align="center">
  <a href="https://www.linkedin.com/in/timex19/"><img src="https://img.shields.io/badge/LinkedIn-LET'S_TALK-0A66C2?style=for-the-badge" alt="Let's talk on LinkedIn" /></a>
  <a href="mailto:joseph@mycyberclinics.com"><img src="https://img.shields.io/badge/Email-JOSEPH-115E59?style=for-the-badge" alt="Email joseph@mycyberclinics.com" /></a>
</p>
'''
(ROOT / "README.md").write_text(readme, encoding="utf-8")
print(f"Generated README and {len(list(ASSETS.glob('*.svg')))} SVG assets.")
