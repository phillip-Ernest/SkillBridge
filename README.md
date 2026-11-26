🌍 SkillBridge
### Unlocking Displaced Talent: Pathways for Skilled Refugees

**Connecting displaced professionals to opportunity through skills validation, inclusive employment pathways, and professional networks.**

---

## 📌 1. Project Overview

SkillBridge is a web-based platform designed to support skilled refugees and displaced professionals in accessing employment, professional development, and economic opportunities.

Many displaced professionals possess valuable academic qualifications, technical expertise, and years of work experience. However, they often face challenges such as difficulties verifying qualifications, limited access to professional networks, legal and regulatory barriers, and restricted financial opportunities.

SkillBridge seeks to bridge these gaps by providing a digital platform where displaced professionals can present their qualifications, demonstrate their skills, access mentorship opportunities, and connect with potential employers and professional networks.

The project promotes inclusive economic participation, human dignity, equal opportunity, and the recognition of talent regardless of displacement status.

## 🎯 2. Problem Statement

Skilled refugees and displaced professionals frequently experience barriers when attempting to enter or re-enter the labour market.

These challenges include:

- Difficulty obtaining recognition of foreign academic and professional qualifications.
- Limited opportunities to demonstrate professional competencies.
- Legal and regulatory barriers affecting access to employment.
- Financial exclusion and limited access to economic opportunities.
- Lack of local work experience and professional references.
- Limited access to mentors, employers, and professional networks.

These barriers can prevent highly skilled individuals from contributing meaningfully to their host communities and economies.

SkillBridge aims to address these challenges through an accessible, inclusive, and skills-focused digital platform.

## 💡 3. Project Objectives

The main objectives of SkillBridge are to:

1. Promote recognition and validation of qualifications and professional skills.
2. Improve access to employment-related information and opportunities.
3. Support displaced professionals in navigating legal and regulatory employment pathways.
4. Encourage mentorship, networking, and professional collaboration.
5. Connect skilled refugees with employers and relevant stakeholders.
6. Promote inclusion, economic independence, and sustainable livelihoods.

## 🚀 4. Core Project Pillars

### Pillar 1: Credential Recognition and Skills Validation

SkillBridge aims to help displaced professionals communicate their qualifications, professional experience, and competencies.

Key activities:
- Professional profile creation.
- Academic and professional qualification submissions.
- Skills and experience documentation.
- Support for credential recognition pathways.
- Skills-based assessment and validation opportunities.

### Pillar 2: Legal, Regulatory, and Financial Access

The platform seeks to improve access to relevant information and resources that can help displaced professionals navigate employment-related barriers.

Key activities:
- Access to employment-related legal information.
- Guidance on work authorization pathways.
- Information on professional registration requirements.
- Access to financial inclusion resources.
- Connections to relevant support organizations.

### Pillar 3: Local Experience and Professional Networks

SkillBridge promotes practical experience and connections within local professional communities.

Key activities:
- Mentorship opportunities.
- Professional networking.
- Internship and volunteering opportunities.
- Local experience development.
- Employer and professional organization connections.

## ✨ 5. Key Platform Features

The SkillBridge application is being developed with the following features:

| Feature | Description |
|---|---|
| User Registration | Allows users to create platform accounts. |
| User Login | Provides secure access to registered accounts. |
| Professional Profiles | Enables users to present their skills and experience. |
| Credential Management | Supports submission of qualification information. |
| Skills Validation | Supports the process of documenting and validating competencies. |
| Mentorship Requests | Enables users to request professional guidance. |
| Opportunity Access | Supports access to employment and development opportunities. |
| Notifications | Communicates relevant platform updates. |
| Administrative Functions | Supports platform administration and management. |

*Note: Features are subject to implementation and testing during development.*

## 🛠️ 6. Technology Stack

SkillBridge uses the following technologies:

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| SQLite | Database management |
| HTML5 | Web page structure |
| CSS3 | User interface styling |
| Werkzeug | Password hashing and security utilities |
| Git and GitHub | Version control and project collaboration |

## 📂 7. Project Structure

The current project includes:

```text
SkillBridge/
|
|-- app.py
|-- requirements.txt
|-- README.md
|-- SECURITY.md
|-- .gitignore
|
|-- check_qualifications.py
|-- check_review.py
|-- create_admin.py
|
|-- static/
|   |-- style.css
|
|-- templates/
|   |-- base.html
|   |-- index.html
|   |-- login.html
|   |-- register.html
|   |-- dashboard.html
|   |-- profile.html
|   |-- skills.html
|   |-- mentorship.html
|   |-- opportunities.html
|   |-- progress.html
|   |-- admin_certificates.html
|   |-- admin_certificate_history.html
|
|-- instance/
|-- .venv/
```

The instance directory and virtual environment are local development resources and should not be published when they contain private data or unnecessary files.

## ⚙️ 8. Installation and Setup

Follow these instructions to install and run SkillBridge on your local computer.

### Prerequisites

Ensure that you have installed:

- Python 3
- pip (Python package manager)
- Visual Studio Code
- Git (optional, for version control)

### Step 1: Open the project directory

Open PowerShell and navigate to the project:

```powershell
cd "$HOME\Desktop\SkillBridge"
```

### Step 2: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 3: Activate the virtual environment

```powershell
.venv\Scripts\Activate
```

### Step 4: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Start the application

```powershell
python app.py
```

### Step 6: Access the application

Open your browser and visit:

http://127.0.0.1:5000

The SkillBridge application should now be accessible locally.



🔐 9. Security and Privacy

SkillBridge is designed with user security and privacy in mind.

Security considerations include:

Password hashing rather than storing plain-text passwords.

Session-based authentication.

Input validation and appropriate error handling.

Access control for protected application functions.

Secure handling of uploaded documents.

Protection of sensitive user information.

Appropriate configuration of application secrets.

Security controls should be reviewed and tested before deployment in a production environment.

🌱 10. Expected Social Impact

SkillBridge aims to contribute to a more inclusive labour market by helping displaced professionals access opportunities and demonstrate their capabilities.

Expected outcomes include:

Improved recognition of displaced professionals' qualifications.

Increased access to employment and professional development.

Stronger connections between displaced professionals and employers.

Improved access to mentorship and professional networks.

Greater economic participation and self-reliance.

Increased awareness of the skills and contributions of displaced communities.

🌍 11. Alignment with the Sustainable Development Goals

SkillBridge supports the following United Nations Sustainable Development Goals:

SDG

Contribution

SDG 4 – Quality Education

Promotes skills recognition and lifelong learning.

SDG 8 – Decent Work and Economic Growth

Supports inclusive employment and economic participation.

SDG 10 – Reduced Inequalities

Addresses barriers faced by displaced professionals.

SDG 16 – Peace, Justice and Strong Institutions

Promotes access to relevant legal and institutional information.

SDG 17 – Partnerships for the Goals

Encourages collaboration among employers, institutions, mentors, and support organizations.

🧪 12. Testing and Quality Assurance

The application should be tested to verify:

Successful user registration.

Successful login and logout.

Appropriate password security.

Correct database operations.

Proper access restrictions.

Successful mentorship request submission.

Appropriate handling of invalid inputs.

Secure document upload handling.

Correct application navigation.

Testing results should be documented during development.

🔮 13. Future Development

Potential future improvements include:

Employer recruitment portal.

Verified credential assessment partnerships.

AI-assisted skills matching.

Professional mentorship matching.

Integration with learning and certification providers.

Multilingual user interface.

Mobile-friendly application experience.

Analytics and impact reporting.

Integration with relevant refugee-support organizations.

🤝 14. Partnerships and Collaboration

SkillBridge recognizes that meaningful inclusion requires collaboration.

Potential partners include:

Refugee-led organizations.

Universities and educational institutions.

Employers and recruitment agencies.

Professional regulatory bodies.

Mentors and industry experts.

Non-governmental organizations.

Government institutions and development partners.

📌 15. Project Status

Development Status: Active Development

SkillBridge is being developed as a practical digital solution to address barriers affecting skilled refugees and displaced professionals.

The application is undergoing feature development, database verification, security testing, and documentation.

👨‍💻 16. Developer and Project Information

Project Name: SkillBridge

Project Theme: Unlocking Displaced Talent: Pathways for Skilled Refugees

Project Category: Social Impact Technology / Employment Inclusion

Primary Technologies: Python, Flask, SQLite, HTML, CSS

Repository: Add your GitHub repository URL here.

❤️ 17. Our Vision

We believe displacement should not mean the loss of professional identity, dignity, or opportunity.

SkillBridge envisions a world where every skilled individual, regardless of displacement status, has a fair opportunity to demonstrate their abilities, access meaningful work, and contribute to society.

SkillBridge — Skills Recognized. Opportunities Connected. Futures Empowered.