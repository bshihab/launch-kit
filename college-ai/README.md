# Launch Kit 🚀

**Launch your future with AI-powered college and career tools.**

Launch Kit is a comprehensive suite of AI-powered tools designed to help high school and college students navigate their academic and professional journeys. The platform combines intelligent college search capabilities with automated networking and outreach tools.

## System Architecture

```mermaid
graph TB
    subgraph "Launch Kit - AI-Powered Student Tools"
        subgraph "College AI Module"
            CA1["College Data Fetcher<br/>fetch_colleges.py"]
            CA2["Embedding Generator<br/>generate_embeddings.py"]
            CA3["College Search Engine<br/>search_colleges.py"]
            CA4["Firestore Database<br/>College Data Storage"]
            
            CA1 --> CA4
            CA2 --> CA4
            CA4 --> CA3
        end
        
        subgraph "Email Outreach Module"
            subgraph "Frontend"
                UI1["Next.js Web App"]
                UI2["📝 Curation Tab<br/>Create & Edit Emails"]
                UI3["📊 Tracking Tab<br/>Monitor Responses"]
                UI4["⚙️ Settings Tab<br/>Profile Management"]
                
                UI1 --> UI2
                UI1 --> UI3
                UI1 --> UI4
            end
            
            subgraph "Backend Services"
                DB1["Supabase Database<br/>PostgreSQL + Auth"]
                ST1["Supabase Storage<br/>Resumes & Files"]
                N8N["n8n Workflow Engine<br/>Agent Orchestration"]
            end
            
            subgraph "A2A AI Agents"
                A1["Profile Analysis Agent<br/>LinkedIn Data Extraction"]
                A2["User Context Agent<br/>Resume & Background Analysis"]
                A3["Company Research Agent<br/>Company Intelligence"]
                A4["Connection Mapping Agent<br/>Find Commonalities"]
                A5["Email Composition Agent<br/>Generate Personalized Emails"]
                A6["Quality Assurance Agent<br/>Review & Optimize"]
                A7["Learning AI Agent<br/>Continuous Improvement"]
            end
            
            subgraph "External Integrations"
                LI["LinkedIn API<br/>Profile Data"]
                EM["Email Services<br/>Gmail/Outlook"]
                AI["OpenAI/Claude<br/>Language Models"]
            end
        end
    end
    
    subgraph "User Journey"
        U1["User Uploads Resume<br/>& LinkedIn Profile"]
        U2["User Adds Target<br/>LinkedIn URLs"]
        U3["AI Processes<br/>All Profiles"]
        U4["User Selects<br/>Personalization Options"]
        U5["AI Generates<br/>Final Emails"]
        U6["User Reviews<br/>& Sends Emails"]
        U7["System Tracks<br/>Responses & Learns"]
    end
    
    subgraph "Data Flow"
        UI2 --> N8N
        N8N --> A1
        N8N --> A2
        N8N --> A3
        A1 --> A4
        A2 --> A4
        A3 --> A4
        A4 --> A5
        A5 --> A6
        A6 --> UI2
        UI2 --> EM
        EM --> UI3
        UI3 --> A7
        A7 --> DB1
        
        A1 <--> LI
        A2 <--> ST1
        A5 <--> AI
        A6 <--> AI
        A7 <--> AI
        
        DB1 <--> UI1
        ST1 <--> UI1
    end
    
    U1 --> U2
    U2 --> U3
    U3 --> U4
    U4 --> U5
    U5 --> U6
    U6 --> U7
    U7 --> A7
```

## 🎯 Features

### College AI Module
- **Smart College Search**: AI-powered semantic search across thousands of colleges
- **Personalized Recommendations**: Tailored college suggestions based on student preferences
- **Real-time Data**: Up-to-date college information from official sources
- **Natural Language Queries**: Search using conversational language

### Email Outreach Module
- **Automated Networking**: AI-generated personalized outreach emails
- **LinkedIn Integration**: Extract and analyze professional profiles
- **Smart Personalization**: Find meaningful connections between sender and recipient
- **Campaign Management**: Track email performance and responses
- **Learning AI**: Continuously improves email effectiveness based on user data

## 🏗️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Supabase Auth** - User authentication

### Backend & Database
- **Supabase** - PostgreSQL database with real-time capabilities
- **Supabase Storage** - File storage for resumes and assets
- **Google Firestore** - College data storage (existing)
- **n8n** - Workflow automation and agent orchestration

### AI & Agents
- **Google Cloud A2A Protocol** - Agent-to-agent communication
- **OpenAI GPT-4** / **Anthropic Claude** - Language models
- **LangChain** - AI application framework
- **Vector Embeddings** - Semantic search capabilities

### Infrastructure
- **Vercel** - Frontend hosting
- **Google Cloud Run** - A2A agent hosting
- **Google Cloud Functions** - Serverless functions

## 📁 Project Structure

```
launch-kit/
├── README.md
├── .gitignore
├── package.json
├── 
├── college-ai/                 # College AI Module
│   ├── src/
│   │   ├── fetch_colleges.py
│   │   ├── generate_embeddings.py
│   │   ├── search_colleges.py
│   │   └── upload_to_firestore.py
│   └── data/
│       └── college_test_data.csv
│
├── email-outreach/             # Email Outreach Module
│   ├── frontend/               # Next.js Web Application
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── public/
│   │
│   ├── agents/                 # A2A AI Agents
│   │   ├── profile-analysis/
│   │   ├── user-context/
│   │   ├── company-research/
│   │   ├── connection-mapping/
│   │   ├── email-composition/
│   │   ├── quality-assurance/
│   │   └── learning-ai/
│   │
│   ├── workflows/              # n8n Workflows
│   │   ├── email-generation.json
│   │   ├── profile-processing.json
│   │   └── tracking-updates.json
│   │
│   └── database/               # Database Schemas & Migrations
│       ├── supabase/
│       └── migrations/
│
└── shared/                     # Shared Utilities
    ├── types/
    ├── utils/
    └── constants/
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- Supabase account
- Google Cloud Platform account
- OpenAI/Anthropic API keys

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bshihab/launch-kit.git
   cd launch-kit
   ```

2. **Install dependencies:**
   ```bash
   # Frontend dependencies
   cd email-outreach/frontend
   npm install
   
   # Python dependencies for College AI
   cd ../../college-ai
   pip install -r requirements.txt
   ```

3. **Environment Setup:**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Add your API keys and configuration
   ```

4. **Database Setup:**
   ```bash
   # Run Supabase migrations
   npx supabase db reset
   ```

5. **Start Development:**
   ```bash
   # Start frontend
   cd email-outreach/frontend
   npm run dev
   
   # Start n8n (in another terminal)
   npx n8n start
   ```

## 📖 Module Documentation

### College AI Module

The College AI module provides intelligent college search and recommendation capabilities:

- **Data Pipeline**: Automated fetching and processing of college data
- **Semantic Search**: Vector-based search using OpenAI embeddings
- **Natural Language Interface**: Query colleges using conversational language

**Usage:**
```bash
# Fetch latest college data
python college-ai/src/fetch_colleges.py

# Generate embeddings
python college-ai/src/generate_embeddings.py

# Interactive search
python college-ai/src/search_colleges.py
```

### Email Outreach Module

The Email Outreach module automates professional networking through AI-generated personalized emails:

**Key Features:**
- Upload resume and LinkedIn profile
- Bulk LinkedIn URL processing
- AI-powered email personalization
- Response tracking and analytics
- Continuous learning from user interactions

**User Flow:**
1. **Setup**: Upload resume and LinkedIn profile
2. **Import**: Add target LinkedIn URLs
3. **Process**: AI analyzes all profiles and finds connections
4. **Personalize**: Select personalization options
5. **Generate**: AI creates tailored emails
6. **Review**: Edit and approve emails
7. **Send**: Bulk send with tracking
8. **Track**: Monitor responses and engagement

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For questions and support:
- Create an [Issue](https://github.com/bshihab/launch-kit/issues)
- Join our [Discord Community](https://discord.gg/launch-kit)
- Email: support@launch-kit.dev

---

**Built with ❤️ for students, by students.**