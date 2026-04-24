const { MongoClient } = require("mongodb");

const uri = "mongodb://localhost:27017";

const data = [
  {
    "name": "Ali Raza",
    "role": "Senior Backend Engineer",
    "skills": ["nodejs", "system design", "databases", "microservices"],
    "domains": ["fintech", "ecommerce"],
    "experience": ["Built onboarding system for fintech app", "Scaled payment API to 1M users"],
    "tags": ["backend", "scalability"],
    "availability": "high",
    "connections": ["Sara Khan"]
  },
  {
    "name": "Bilal Khan",
    "role": "DevOps Engineer",
    "skills": ["aws", "docker", "kubernetes", "ci/cd"],
    "domains": ["saas", "fintech"],
    "experience": ["Automated deployment pipelines", "Maintained onboarding infrastructure"],
    "tags": ["infra", "backend-support"],
    "availability": "medium",
    "connections": ["Ali Raza"]
  },
  {
    "name": "Sara Khan",
    "role": "Product Manager",
    "skills": ["product strategy", "roadmapping", "analytics"],
    "domains": ["ecommerce", "saas"],
    "experience": ["Led product roadmap for ecommerce platform", "Improved onboarding funnel by 30%"],
    "tags": ["product", "growth"],
    "availability": "high",
    "connections": ["Ali Raza"]
  },
  {
    "name": "Usman Ali",
    "role": "Frontend Engineer",
    "skills": ["react", "javascript", "ui design", "css"],
    "domains": ["saas", "ecommerce"],
    "experience": ["Built admin dashboard UI", "Optimized frontend performance"],
    "tags": ["frontend", "ui"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Hassan Ahmed",
    "role": "Full Stack Developer",
    "skills": ["nodejs", "react", "databases", "apis"],
    "domains": ["startup", "saas"],
    "experience": ["Developed MVP for startup", "Integrated REST APIs"],
    "tags": ["fullstack"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Zain Malik",
    "role": "AI Engineer",
    "skills": ["python", "machine learning", "nlp", "llms"],
    "domains": ["ai", "automation"],
    "experience": ["Built chatbot using NLP", "Automated document processing"],
    "tags": ["ai", "ml"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Ayesha Malik",
    "role": "UX Designer",
    "skills": ["figma", "user experience", "prototyping"],
    "domains": ["mobile", "ecommerce"],
    "experience": ["Designed mobile onboarding flow", "Improved UX retention"],
    "tags": ["design", "ux"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Noor Fatima",
    "role": "Data Analyst",
    "skills": ["sql", "excel", "reporting", "analytics"],
    "domains": ["marketing", "finance"],
    "experience": ["Created dashboards for marketing", "Analyzed campaign data"],
    "tags": ["data", "analytics"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Imran Shah",
    "role": "Security Engineer",
    "skills": ["cybersecurity", "encryption", "auth systems"],
    "domains": ["enterprise", "fintech"],
    "experience": ["Built secure auth system", "Conducted penetration testing"],
    "tags": ["security"],
    "availability": "low",
    "connections": []
  },
  {
    "name": "Fatima Noor",
    "role": "Growth Marketer",
    "skills": ["growth hacking", "funnels", "a/b testing"],
    "domains": ["marketing", "saas"],
    "experience": ["Optimized conversion funnel", "Ran growth experiments"],
    "tags": ["growth"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Hamza Tariq",
    "role": "Data Scientist",
    "skills": ["python", "ml", "statistics", "prediction models"],
    "domains": ["ai", "marketing"],
    "experience": ["Built churn prediction model", "Analyzed user onboarding success"],
    "tags": ["ml", "data"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Zara Ali",
    "role": "UI Designer",
    "skills": ["figma", "visual design", "branding"],
    "domains": ["ecommerce", "mobile"],
    "experience": ["Designed ecommerce UI", "Created brand identity"],
    "tags": ["design"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Usama Javed",
    "role": "Backend Engineer",
    "skills": ["python", "apis", "databases"],
    "domains": ["education", "saas"],
    "experience": ["Built LMS backend", "Handled API scaling"],
    "tags": ["backend"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Omar Siddiqui",
    "role": "Mobile App Developer",
    "skills": ["flutter", "react native", "apis"],
    "domains": ["mobile", "startup"],
    "experience": ["Built mobile app MVP", "Integrated APIs"],
    "tags": ["mobile"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Kashif Mehmood",
    "role": "Game Developer",
    "skills": ["unity", "c#", "game design"],
    "domains": ["gaming"],
    "experience": ["Developed 2D game", "Worked on game physics"],
    "tags": ["gaming"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Saad Qureshi",
    "role": "Automation Engineer",
    "skills": ["python", "automation", "scripting"],
    "domains": ["automation", "enterprise"],
    "experience": ["Automated workflows", "Reduced manual tasks"],
    "tags": ["automation"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Hira Aslam",
    "role": "HR Specialist",
    "skills": ["recruitment", "onboarding", "training"],
    "domains": ["hr"],
    "experience": ["Handled hiring pipeline", "Improved onboarding process"],
    "tags": ["hr"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Talha Nadeem",
    "role": "Cloud Engineer",
    "skills": ["aws", "cloud architecture", "devops"],
    "domains": ["enterprise", "saas"],
    "experience": ["Designed cloud infra", "Reduced downtime"],
    "tags": ["infra"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Rida Zahid",
    "role": "Content Strategist",
    "skills": ["content marketing", "seo", "branding"],
    "domains": ["marketing"],
    "experience": ["Built content strategy", "Improved SEO rankings"],
    "tags": ["marketing"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Danish Iqbal",
    "role": "Full Stack Developer",
    "skills": ["react", "nodejs", "databases"],
    "domains": ["startup", "saas"],
    "experience": ["Built SaaS MVP", "Handled backend APIs"],
    "tags": ["fullstack"],
    "availability": "high",
    "connections": []
  },

  {
    "name": "Farhan Malik",
    "role": "Blockchain Developer",
    "skills": ["solidity", "web3", "smart contracts"],
    "domains": ["fintech"],
    "experience": ["Built crypto wallet", "Developed smart contracts"],
    "tags": ["backend"],
    "availability": "low",
    "connections": []
  },
  {
    "name": "Maham Riaz",
    "role": "EdTech Specialist",
    "skills": ["instructional design", "lms", "content"],
    "domains": ["education"],
    "experience": ["Built LMS content", "Designed courses"],
    "tags": ["education"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Adnan Sheikh",
    "role": "QA Engineer",
    "skills": ["testing", "automation", "qa"],
    "domains": ["enterprise", "saas"],
    "experience": ["Automated test suites", "Improved QA process"],
    "tags": ["qa"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Nida Tariq",
    "role": "Product Designer",
    "skills": ["figma", "ux", "prototyping"],
    "domains": ["mobile", "startup"],
    "experience": ["Designed MVP UX", "User journey mapping"],
    "tags": ["design"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Yasir Khan",
    "role": "Systems Architect",
    "skills": ["system design", "microservices", "databases"],
    "domains": ["enterprise", "fintech"],
    "experience": ["Designed scalable systems", "Handled 10M users"],
    "tags": ["backend"],
    "availability": "low",
    "connections": []
  },
  {
    "name": "Laiba Noor",
    "role": "Marketing Analyst",
    "skills": ["analytics", "sql", "reporting"],
    "domains": ["marketing"],
    "experience": ["Analyzed campaign data", "Improved ROI"],
    "tags": ["analytics"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Rehan Butt",
    "role": "DevOps Specialist",
    "skills": ["docker", "ci/cd", "aws"],
    "domains": ["saas", "enterprise"],
    "experience": ["Managed deployments", "Reduced downtime"],
    "tags": ["infra"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Adeel Ahmed",
    "role": "Backend Developer",
    "skills": ["python", "django", "apis"],
    "domains": ["education", "saas"],
    "experience": ["Built LMS APIs", "Handled authentication"],
    "tags": ["backend"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Sana Khalid",
    "role": "UX Researcher",
    "skills": ["user research", "ux", "interviews"],
    "domains": ["mobile", "ecommerce"],
    "experience": ["Conducted user interviews", "Improved UX flows"],
    "tags": ["ux"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Fahad Raza",
    "role": "AI Researcher",
    "skills": ["ml", "nlp", "deep learning"],
    "domains": ["ai"],
    "experience": ["Published ML research", "Built NLP models"],
    "tags": ["ai"],
    "availability": "low",
    "connections": []
  },
  {
    "name": "Arslan Haider",
    "role": "Backend Engineer",
    "skills": ["python", "django", "apis", "databases"],
    "domains": ["education", "saas"],
    "experience": ["Built LMS backend", "Optimized API latency"],
    "tags": ["backend"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Muneeb Akhtar",
    "role": "AI Engineer",
    "skills": ["python", "ml", "nlp", "llms"],
    "domains": ["ai", "automation"],
    "experience": ["Built chatbot system", "Automated document parsing"],
    "tags": ["ai"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Hassan Rauf",
    "role": "Frontend Developer",
    "skills": ["react", "javascript", "css", "ui design"],
    "domains": ["ecommerce", "saas"],
    "experience": ["Developed ecommerce UI", "Improved page speed"],
    "tags": ["frontend"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Taha Qasim",
    "role": "DevOps Engineer",
    "skills": ["aws", "docker", "ci/cd", "kubernetes"],
    "domains": ["enterprise", "saas"],
    "experience": ["Built CI/CD pipelines", "Managed cloud infra"],
    "tags": ["infra"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Zubair Ahmed",
    "role": "Full Stack Developer",
    "skills": ["nodejs", "react", "apis", "databases"],
    "domains": ["startup", "mobile"],
    "experience": ["Built MVP apps", "Integrated REST APIs"],
    "tags": ["fullstack"],
    "availability": "high",
    "connections": []
  },

  {
    "name": "Faiza Noor",
    "role": "UX Designer",
    "skills": ["figma", "prototyping", "user research"],
    "domains": ["mobile", "ecommerce"],
    "experience": ["Designed onboarding flows", "Improved UX retention"],
    "tags": ["ux"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Ammar Iqbal",
    "role": "Data Analyst",
    "skills": ["sql", "excel", "analytics", "reporting"],
    "domains": ["marketing", "finance"],
    "experience": ["Built dashboards", "Analyzed campaign data"],
    "tags": ["analytics"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Shahzaib Khan",
    "role": "Security Engineer",
    "skills": ["cybersecurity", "encryption", "auth systems"],
    "domains": ["enterprise", "fintech"],
    "experience": ["Secured APIs", "Performed vulnerability scans"],
    "tags": ["security"],
    "availability": "low",
    "connections": []
  },
  {
    "name": "Noman Ali",
    "role": "Growth Specialist",
    "skills": ["growth hacking", "funnels", "a/b testing"],
    "domains": ["marketing", "saas"],
    "experience": ["Optimized funnel", "Ran growth experiments"],
    "tags": ["growth"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Areeba Khan",
    "role": "Product Manager",
    "skills": ["product strategy", "analytics", "roadmapping"],
    "domains": ["saas", "startup"],
    "experience": ["Defined product roadmap", "Improved onboarding"],
    "tags": ["product"],
    "availability": "medium",
    "connections": []
  },

  {
    "name": "Hamid Bashir",
    "role": "Cloud Architect",
    "skills": ["aws", "system design", "microservices"],
    "domains": ["enterprise", "fintech"],
    "experience": ["Designed scalable infra", "Handled 5M users"],
    "tags": ["infra"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Saima Javed",
    "role": "UI Designer",
    "skills": ["figma", "visual design", "branding"],
    "domains": ["ecommerce", "mobile"],
    "experience": ["Created brand systems", "Designed mobile UI"],
    "tags": ["design"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Owais Malik",
    "role": "Game Developer",
    "skills": ["unity", "c#", "game design"],
    "domains": ["gaming"],
    "experience": ["Built 3D games", "Worked on gameplay systems"],
    "tags": ["gaming"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Kiran Fatima",
    "role": "HR Manager",
    "skills": ["recruitment", "training", "onboarding"],
    "domains": ["hr"],
    "experience": ["Managed hiring", "Built onboarding flows"],
    "tags": ["hr"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Saad Ahmed",
    "role": "Automation Engineer",
    "skills": ["python", "automation", "scripting"],
    "domains": ["automation", "enterprise"],
    "experience": ["Automated workflows", "Reduced manual ops"],
    "tags": ["automation"],
    "availability": "high",
    "connections": []
  },

  {
    "name": "Usama Tariq",
    "role": "Backend Engineer",
    "skills": ["nodejs", "apis", "databases"],
    "domains": ["ecommerce", "saas"],
    "experience": ["Built payment APIs", "Optimized queries"],
    "tags": ["backend"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Iqra Hassan",
    "role": "Data Scientist",
    "skills": ["python", "ml", "statistics"],
    "domains": ["ai", "marketing"],
    "experience": ["Built prediction models", "Analyzed user behavior"],
    "tags": ["ml"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Daniyal Khan",
    "role": "Frontend Engineer",
    "skills": ["react", "ui design", "css"],
    "domains": ["saas", "startup"],
    "experience": ["Built dashboards", "Improved UX flows"],
    "tags": ["frontend"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Rameen Ali",
    "role": "UX Researcher",
    "skills": ["user research", "ux", "interviews"],
    "domains": ["mobile", "education"],
    "experience": ["Conducted UX interviews", "Improved usability"],
    "tags": ["ux"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Faraz Khan",
    "role": "DevOps Specialist",
    "skills": ["docker", "aws", "ci/cd"],
    "domains": ["saas", "enterprise"],
    "experience": ["Managed deployments", "Reduced downtime"],
    "tags": ["infra"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Junaid Abbas",
    "role": "Backend Engineer",
    "skills": ["go", "apis", "microservices", "databases"],
    "domains": ["fintech", "enterprise"],
    "experience": ["Built payment microservices", "Handled high-load APIs"],
    "tags": ["backend", "scalability"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Hafsa Malik",
    "role": "Product Designer",
    "skills": ["figma", "ux", "design systems"],
    "domains": ["saas", "mobile"],
    "experience": ["Designed SaaS dashboards", "Built design systems"],
    "tags": ["design", "ux"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Salman Raza",
    "role": "AI Engineer",
    "skills": ["python", "nlp", "machine learning", "llms"],
    "domains": ["ai", "automation"],
    "experience": ["Built NLP chatbot", "Automated workflows using AI"],
    "tags": ["ai", "ml"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Kashan Iqbal",
    "role": "DevOps Engineer",
    "skills": ["aws", "kubernetes", "docker", "ci/cd"],
    "domains": ["enterprise", "saas"],
    "experience": ["Managed cloud infra", "Automated deployments"],
    "tags": ["infra"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Nadia Sheikh",
    "role": "Growth Marketer",
    "skills": ["funnels", "a/b testing", "analytics"],
    "domains": ["marketing", "ecommerce"],
    "experience": ["Improved conversion rates", "Ran marketing experiments"],
    "tags": ["growth"],
    "availability": "high",
    "connections": []
  },

  {
    "name": "Bilawal Hussain",
    "role": "Frontend Developer",
    "skills": ["react", "javascript", "css", "ui design"],
    "domains": ["startup", "saas"],
    "experience": ["Built landing pages", "Optimized frontend UX"],
    "tags": ["frontend"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Saba Noor",
    "role": "Data Analyst",
    "skills": ["sql", "excel", "analytics"],
    "domains": ["finance", "marketing"],
    "experience": ["Analyzed revenue data", "Built reporting dashboards"],
    "tags": ["data"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Rizwan Haider",
    "role": "Cloud Engineer",
    "skills": ["aws", "cloud architecture", "system design"],
    "domains": ["enterprise", "fintech"],
    "experience": ["Designed cloud systems", "Handled scaling infra"],
    "tags": ["infra"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Aiman Tariq",
    "role": "UX Designer",
    "skills": ["figma", "prototyping", "user experience"],
    "domains": ["mobile", "ecommerce"],
    "experience": ["Designed mobile UX", "Improved onboarding flow"],
    "tags": ["ux"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Faisal Qureshi",
    "role": "Security Specialist",
    "skills": ["cybersecurity", "auth systems", "encryption"],
    "domains": ["enterprise", "fintech"],
    "experience": ["Secured payment systems", "Handled auth flows"],
    "tags": ["security"],
    "availability": "low",
    "connections": []
  },

  {
    "name": "Adeel Khan",
    "role": "Full Stack Developer",
    "skills": ["nodejs", "react", "databases", "apis"],
    "domains": ["startup", "mobile"],
    "experience": ["Built MVP apps", "Handled backend APIs"],
    "tags": ["fullstack"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Zoya Malik",
    "role": "Product Manager",
    "skills": ["roadmapping", "analytics", "product strategy"],
    "domains": ["saas", "ecommerce"],
    "experience": ["Led product launches", "Optimized onboarding"],
    "tags": ["product"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Kamran Shah",
    "role": "Automation Engineer",
    "skills": ["python", "automation", "scripting"],
    "domains": ["automation", "enterprise"],
    "experience": ["Automated manual tasks", "Improved workflows"],
    "tags": ["automation"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Rabia Ahmed",
    "role": "UI Designer",
    "skills": ["figma", "branding", "visual design"],
    "domains": ["ecommerce", "startup"],
    "experience": ["Designed ecommerce UI", "Built brand identity"],
    "tags": ["design"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Asad Mehmood",
    "role": "Backend Developer",
    "skills": ["java", "spring", "apis", "databases"],
    "domains": ["enterprise", "fintech"],
    "experience": ["Built enterprise APIs", "Handled data pipelines"],
    "tags": ["backend"],
    "availability": "medium",
    "connections": []
  },

  {
    "name": "Mariam Ali",
    "role": "Content Marketer",
    "skills": ["seo", "content marketing", "branding"],
    "domains": ["marketing"],
    "experience": ["Improved SEO rankings", "Built content strategy"],
    "tags": ["marketing"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Tariq Bashir",
    "role": "Game Developer",
    "skills": ["unity", "c#", "game design"],
    "domains": ["gaming"],
    "experience": ["Developed 2D games", "Worked on physics engine"],
    "tags": ["gaming"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Sana Riaz",
    "role": "HR Specialist",
    "skills": ["recruitment", "onboarding", "training"],
    "domains": ["hr"],
    "experience": ["Managed hiring pipeline", "Improved onboarding"],
    "tags": ["hr"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Usman Khalid",
    "role": "Data Engineer",
    "skills": ["python", "data pipelines", "sql"],
    "domains": ["ai", "enterprise"],
    "experience": ["Built ETL pipelines", "Handled big data"],
    "tags": ["data"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Hassan Tariq",
    "role": "Mobile Developer",
    "skills": ["flutter", "react native", "apis"],
    "domains": ["mobile", "startup"],
    "experience": ["Built mobile apps", "Integrated APIs"],
    "tags": ["mobile"],
    "availability": "high",
    "connections": []
  },

  {
    "name": "Ali Hassan",
    "role": "Backend Engineer",
    "skills": ["python", "flask", "databases"],
    "domains": ["education", "saas"],
    "experience": ["Built LMS backend", "Handled API integration"],
    "tags": ["backend"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Aqsa Noor",
    "role": "UX Researcher",
    "skills": ["user research", "ux", "testing"],
    "domains": ["mobile", "ecommerce"],
    "experience": ["Conducted UX studies", "Improved usability"],
    "tags": ["ux"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Imran Ali",
    "role": "DevOps Engineer",
    "skills": ["docker", "aws", "ci/cd"],
    "domains": ["saas", "enterprise"],
    "experience": ["Managed deployments", "Reduced downtime"],
    "tags": ["infra"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Zeeshan Malik",
    "role": "AI Researcher",
    "skills": ["ml", "deep learning", "nlp"],
    "domains": ["ai"],
    "experience": ["Built deep learning models", "Worked on NLP"],
    "tags": ["ai"],
    "availability": "low",
    "connections": []
  },
  {
    "name": "Fariha Khan",
    "role": "Product Designer",
    "skills": ["figma", "ux", "prototyping"],
    "domains": ["startup", "mobile"],
    "experience": ["Designed MVP UX", "Improved onboarding"],
    "tags": ["design"],
    "availability": "high",
    "connections": []
  },

  {
    "name": "Saif Ali",
    "role": "Cloud Engineer",
    "skills": ["aws", "cloud", "system design"],
    "domains": ["enterprise"],
    "experience": ["Handled cloud infra", "Optimized scaling"],
    "tags": ["infra"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Hina Zahid",
    "role": "Marketing Analyst",
    "skills": ["analytics", "reporting", "sql"],
    "domains": ["marketing"],
    "experience": ["Analyzed campaigns", "Improved ROI"],
    "tags": ["analytics"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Nabeel Ahmed",
    "role": "Full Stack Developer",
    "skills": ["nodejs", "react", "apis"],
    "domains": ["saas", "startup"],
    "experience": ["Built SaaS apps", "Handled frontend/backend"],
    "tags": ["fullstack"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Maha Rauf",
    "role": "UX Designer",
    "skills": ["figma", "user experience", "prototyping"],
    "domains": ["mobile", "education"],
    "experience": ["Designed learning UX", "Improved usability"],
    "tags": ["ux"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Rizwan Malik",
    "role": "Backend Developer",
    "skills": ["php", "laravel", "databases"],
    "domains": ["ecommerce", "startup"],
    "experience": ["Built ecommerce backend", "Handled payments"],
    "tags": ["backend"],
    "availability": "medium",
    "connections": []
  },

  {
    "name": "Sami Ullah",
    "role": "Automation Engineer",
    "skills": ["python", "automation", "testing"],
    "domains": ["automation"],
    "experience": ["Automated testing flows", "Improved efficiency"],
    "tags": ["automation"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Areej Khan",
    "role": "UI Designer",
    "skills": ["figma", "visual design"],
    "domains": ["ecommerce"],
    "experience": ["Designed UI systems", "Worked on branding"],
    "tags": ["design"],
    "availability": "high",
    "connections": []
  },
  {
    "name": "Fahad Ahmed",
    "role": "Security Engineer",
    "skills": ["cybersecurity", "risk analysis"],
    "domains": ["enterprise"],
    "experience": ["Handled security audits", "Mitigated threats"],
    "tags": ["security"],
    "availability": "low",
    "connections": []
  },
  {
    "name": "Usman Raza",
    "role": "Data Scientist",
    "skills": ["python", "ml", "analytics"],
    "domains": ["ai", "finance"],
    "experience": ["Built ML models", "Analyzed financial data"],
    "tags": ["ml"],
    "availability": "medium",
    "connections": []
  },
  {
    "name": "Laiba Ahmed",
    "role": "Product Manager",
    "skills": ["product strategy", "analytics"],
    "domains": ["startup", "saas"],
    "experience": ["Defined roadmap", "Improved product metrics"],
    "tags": ["product"],
    "availability": "high",
    "connections": []
  }
];

async function seed() {
  const client = new MongoClient(uri);
  await client.connect();

  const db = client.db("slack_co_pilot");
  const collection = db.collection("people");

  await collection.deleteMany({});
  await collection.insertMany(data);

  console.log("Mock data inserted successfully!");
  await client.close();
}

seed();
