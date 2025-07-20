# Smart Financial Assistant

## Overview

This is a full-stack MVP web application built with Streamlit that provides users with an AI-powered financial assistant. The application helps users track their portfolios, manage financial reminders, receive AI-driven insights, and interact with market data through a conversational interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit with multi-page application structure
- **UI Components**: Plotly for interactive charts, native Streamlit components for forms and data display
- **Page Structure**: Main app.py with modular pages in the `/pages` directory
- **State Management**: Streamlit session state for user authentication and application state

### Backend Architecture
- **Core Framework**: Python with Streamlit as the web framework
- **Modular Utilities**: Separate utility modules for authentication, database operations, AI assistance, and financial data
- **Data Processing**: Pandas for data manipulation, NumPy for numerical operations
- **API Integration**: OpenAI API for AI responses, Yahoo Finance API for market data

## Key Components

### Authentication System
- **Implementation**: File-based user storage with SHA-256 password hashing
- **Session Management**: Streamlit session state for maintaining user sessions
- **Security**: Password hashing and authentication checks on protected pages

### AI Assistant
- **LLM Integration**: OpenAI GPT-4o model for financial advice and insights
- **Context Awareness**: Uses user's financial profile and portfolio data for personalized responses
- **Chat Interface**: Conversational UI with chat history and example prompts

### Financial Data Management
- **Market Data**: Yahoo Finance integration for real-time stock prices and market indices
- **Portfolio Tracking**: User portfolio management with performance calculations
- **Data Visualization**: Interactive charts using Plotly for portfolio performance and market trends

### User Preferences System
- **Profile Management**: Risk tolerance, investment timeline, and goal tracking
- **Personalization**: AI responses tailored to user's financial profile
- **Persistent Storage**: JSON-based file storage for user preferences

### Reminder System
- **Types**: SIP investments, tax filing, portfolio reviews, bill payments, insurance premiums
- **Scheduling**: Date-based reminders with descriptions and frequency options
- **Management**: Add, view, and delete reminders functionality

## Data Flow

1. **User Authentication**: Login/registration → session state management → protected page access
2. **Portfolio Data**: Yahoo Finance API → data processing → visualization and metrics
3. **AI Interactions**: User query → context gathering → OpenAI API → personalized response
4. **Preferences**: User input → validation → JSON file storage → AI context integration
5. **Reminders**: User creation → JSON storage → display and management interface

## External Dependencies

### APIs and Services
- **OpenAI API**: For AI-powered financial advice and insights
- **Yahoo Finance (yfinance)**: For real-time stock data and market information
- **Plotly**: For interactive financial charts and visualizations

### Python Libraries
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **yfinance**: Yahoo Finance API wrapper
- **OpenAI**: Official OpenAI API client
- **Plotly**: Interactive visualization library

## Deployment Strategy

### Development Environment
- **Platform**: Replit-ready structure with requirements.txt
- **File Structure**: Modular organization with separate utilities and pages
- **Configuration**: Environment variables for API keys (OpenAI)

### Data Storage
- **Current Implementation**: PostgreSQL database with comprehensive schema
- **Database Tables**: Users, user_preferences, portfolio_holdings, transactions, reminders, ai_chat_history, portfolio_performance, market_data_cache
- **Data Persistence**: Full relational database with proper foreign keys and indexing

### Scalability Considerations
- **Database Migration**: Utilities structured to easily switch from file-based to PostgreSQL
- **API Rate Limits**: Error handling for external API limitations
- **Session Management**: Streamlit session state with logout functionality

### Security Features
- **Password Security**: SHA-256 hashing for user passwords
- **Session Protection**: Authentication checks on all protected pages
- **API Key Management**: Environment variable configuration for sensitive data

The application is designed as an MVP with a clear path to production scaling, utilizing file-based storage for simplicity while maintaining an architecture that supports database migration and enhanced security features.
