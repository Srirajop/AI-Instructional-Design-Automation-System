# e-Learning AI: Next-Generation Instructional Design Platform

Welcome to **e-Learning AI**, a state-of-the-art web application designed to revolutionize how instructional designers, educators, and corporate trainers create educational content.

By leveraging ultra-low latency AI models and a premium, highly interactive user interface, this platform automates the heavy lifting of drafting **Design Documents** and **Storyboards**, allowing creators to focus on strategy and learning outcomes rather than manual formatting.

---

## 🎯 The Pitch: Why This Platform?

For modern companies and educational institutions, speed and quality of training material are critical. 

**e-Learning AI** provides:
1. **Intelligent Automation:** Upload raw source materials or fill out a brief intake form, and the AI instantly generates structured, industry-standard Design Documents and Storyboards.
2. **Surgical AI Editing:** A proprietary cell-level, precision AI editor allows users to highlight specific parts of their storyboard and ask the AI to rewrite, expand, or fix them without breaking the document's structure.
3. **World-Class User Experience:** Unlike clunky legacy tools, this platform features a modern, "glassmorphic" UI with smooth staggered entrance animations, floating elements, and a dynamic twinkling particle interface. It feels like software from 2030.
4. **Cloud File Management:** A built-in, animated File Management System allows teams to upload, manage, and utilize their past projects securely.

---

## 🧠 AI Architecture & Models Used

This project is built for **speed**. To achieve real-time, surgical AI edits, we bypassed slower APIs and integrated directly with **Groq's LPU (Language Processing Unit) inference engine**.

### **API Keys Required:**
- `GROQ_API_KEY`: The core engine driving all AI interactions.

### **Models Deployed:**
- **Meta's `llama-3.1-8b-instant` (via Groq):** 
  - **Why this model?** We specifically chose the `8b-instant` model for its blistering speed. When a user highlights a cell to request an edit, they expect immediate feedback. By running this model on Groq's specialized hardware, the platform achieves instant token generation, making the AI feel like a paired co-worker rather than a slow chat bot.
  - **Use Cases:** Document generation, surgical cell-level edits, intent classification, and content beautification.

---

## 🏗️ Technical Stack

### **Frontend (The User Experience)**
- **Framework & Prototyping:** React + Vite, rapidly prototyped and accelerated using **  Apps** for structural generation and micro-app deployment strategies.
- **Routing:** React Router DOM (protected routes for authenticated dashboards).
- **Styling:** Custom, highly optimized vanilla CSS. Features a bespoke global animation framework (`.animate-shiny`, `.animate-morph-bg`, `.stagger-enter`) and Frosted Glass (Glassmorphism) UI elements.
- **Icons:** `lucide-react` for clean, professional iconography.

### **Backend (The Engine)**
- **Framework:** FastAPI (Python). Chosen for its asynchronous capabilities, auto-generated Swagger documentation, and incredible performance.
- **Database:** MySQL relational database accessed via `SQLAlchemy` ORM. Ensures robust, transactional data integrity for user's files and projects.
- **Authentication:** JWT (JSON Web Tokens) for stateless, secure session management. Password hashing handled by `passlib` & `bcrypt`.
- **Email Services:** `fastapi-mail` configured for secure, asynchronous password reset workflows via SMTP.

---

## 💰 Pricing & API Operational Costs

When pitching this to clients, one of the best selling points is the incredibly low operational cost.

**Does it work for free?**
Yes. For development, demos, and initial low-volume client usage, you can run this platform entirely for free using Groq's generous **Free Tier API Key**. It provides enough rate limits to comfortably test and demonstrate all features.

**What is the price if a client upgrades to a paid key?**
When the platform needs to scale to high-volume corporate usage, users can purchase a Groq API key. Because we are using the `llama-3.1-8b-instant` model, the pricing is aggressively cheap:
- **Price:** Approximately **$0.05 per 1 Million Tokens**.
- **Context:** To put that in perspective, formatting an entire, massive 10-page Storyboard Document typically uses fewer than 10,000 tokens. This means an instructional designer can generate **100 complete storyboards for only 5 cents.** The cost per user is virtually zero compared to traditional enterprise SaaS licensing.

---

## 🔐 Environment Variables (.env)

To run this application, the following environment variables must be configured in the backend `.env` file:

```env
# Database
DATABASE_URL=mysql+pymysql://<user>:<password>@localhost/storyboard_db

# Security
SECRET_KEY=<your_jwt_secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Engine
GROQ_API_KEY=<your_groq_api_key>

# Email Service (for Password Resets)
MAIL_USERNAME=<your_email>
MAIL_PASSWORD=<your_app_password>
MAIL_FROM=<your_email>
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

---

## 🚀 Future Roadmap
- Integration with LMS (Learning Management Systems) via SCORM export.
- Collaborative real-time editing (Multiplayer mode).
- Advanced AI media generation (images and TTS audio) directly embedded into storyboards.
