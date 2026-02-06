# Contributing to Outreach Scraping Toolkit

Thank you for considering contributing to the Outreach Scraping Toolkit! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Adding New Features](#adding-new-features)

## Code of Conduct

### Our Standards

- **Be respectful:** Treat everyone with respect and kindness
- **Be constructive:** Provide helpful feedback and suggestions
- **Be collaborative:** Work together towards common goals
- **Be inclusive:** Welcome contributors of all backgrounds and skill levels

### Reporting Issues

If you encounter inappropriate behavior, please report it by creating an issue or contacting the maintainers.

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.9 or higher
- Node.js 16.x or higher
- Git installed and configured
- Apify API token (for testing scraping functionality)
- Basic knowledge of FastAPI and React

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/my-app.git
   cd my-app
   ```
3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/original-owner/my-app.git
   ```

## Development Setup

### 1. Install Dependencies

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your Apify token
```

### 3. Start Development Servers

**Option A: Use init script**
```bash
chmod +x init.sh
./init.sh
```

**Option B: Manual startup**
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 4. Verify Setup

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
my-app/
├── backend/                 # FastAPI backend
│   ├── main.py             # API endpoints
│   ├── scraper.py          # Apify integration
│   ├── database.py         # Data persistence
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main component
│   │   ├── components/     # Reusable components
│   │   └── pages/          # Page components
│   ├── public/             # Static assets
│   └── package.json        # Node dependencies
├── config/
│   └── audience.yaml       # Target audience config
├── data/                   # Storage for bookmarks/history
├── docs/                   # Documentation
├── screenshots/            # Test evidence
└── README.md               # Project overview
```

### Key Files

- **Backend:**
  - `main.py` - REST API endpoints
  - `scraper.py` - Web scraping logic
  - `database.py` - JSON file storage

- **Frontend:**
  - `App.jsx` - Main application component
  - `components/SidebarNav.jsx` - Navigation sidebar
  - `components/SearchForm.jsx` - Scraping form
  - `components/ResultsTable.jsx` - Results display
  - `components/DetailSidebar.jsx` - Lead detail panel
  - `pages/CostPage.jsx` - Cost insights page

## Development Workflow

### 1. Create a Feature Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write clean, readable code
- Follow the code style guidelines
- Add comments for complex logic
- Update documentation if needed

### 3. Test Your Changes

- Test in the browser (manual testing)
- Check console for errors
- Verify API endpoints work
- Test edge cases

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new feature description"
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

## Code Style Guidelines

### Python (Backend)

**Style:** Follow PEP 8

```python
# Good
def scrape_google_maps(keyword: str, city: str, max_results: int = 20) -> List[Dict]:
    """
    Scrape Google Maps using Apify API.

    Args:
        keyword: Search keyword
        city: City to search in
        max_results: Maximum results to return

    Returns:
        List of business records
    """
    results = []
    # Implementation...
    return results

# Bad
def scrape(k,c,m=20):
    r=[]
    return r
```

**Key principles:**
- Use type hints for function parameters and return types
- Write docstrings for all functions and classes
- Use meaningful variable names
- Keep functions focused and small (< 50 lines)
- Use list comprehensions when appropriate
- Handle exceptions gracefully

**Imports:**
```python
# Standard library imports first
import os
from typing import List, Dict

# Third-party imports second
from fastapi import FastAPI, HTTPException
import yaml

# Local imports last
from scraper import scrape_google_maps
import database as db
```

### JavaScript/React (Frontend)

**Style:** Follow Airbnb JavaScript Style Guide (adapted)

```javascript
// Good
function SearchForm({ onSubmit, isLoading }) {
  const [keyword, setKeyword] = useState('')
  const [city, setCity] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!keyword || !city) {
      alert('Please fill in all fields')
      return
    }
    await onSubmit({ keyword, city })
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  )
}

// Bad
function form(props){
  const [k,setK]=useState('')
  return <form>...</form>
}
```

**Key principles:**
- Use functional components with hooks
- Use meaningful component and variable names
- Keep components small and focused
- Use destructuring for props
- Add PropTypes or TypeScript types (future)
- Use const/let, never var
- Use arrow functions for callbacks
- Add comments for complex UI logic

**Component structure:**
```javascript
import React, { useState, useEffect } from 'react'
import { Icon } from 'lucide-react'

function MyComponent({ prop1, prop2 }) {
  // State
  const [state, setState] = useState(null)

  // Effects
  useEffect(() => {
    // Side effects
  }, [dependencies])

  // Event handlers
  const handleClick = () => {
    // Handle click
  }

  // Render
  return (
    <div className="...">
      {/* JSX */}
    </div>
  )
}

export default MyComponent
```

### Tailwind CSS

**Principles:**
- Use utility classes consistently
- Follow mobile-first approach
- Use design tokens (colors, spacing)
- Group related classes

```jsx
// Good
<div className="flex items-center justify-between p-4 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">
  <span className="text-white font-medium">Label</span>
  <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
    Click
  </button>
</div>

// Bad
<div style={{display: 'flex', backgroundColor: '#1f2937'}}>
  <span style={{color: 'white'}}>Label</span>
</div>
```

## Testing

### Manual Testing

For now, all testing is manual via the browser and API docs.

**Frontend testing checklist:**
- [ ] Navigation works (sidebar links)
- [ ] Scraping form submits successfully
- [ ] Results display in table
- [ ] Lead selection shows detail panel
- [ ] Bookmark/unbookmark works
- [ ] CSV export downloads file
- [ ] Cost insights page renders
- [ ] No console errors

**Backend testing checklist:**
- [ ] All endpoints return correct status codes
- [ ] API docs are accessible at /docs
- [ ] CORS headers are present
- [ ] Error messages are descriptive
- [ ] Data persists to JSON files

**Test using API docs:**

1. Go to http://localhost:8000/docs
2. Expand each endpoint
3. Click "Try it out"
4. Fill in parameters
5. Execute and verify response

### Future: Automated Testing

We plan to add:
- **Backend:** pytest for API tests
- **Frontend:** Vitest + React Testing Library
- **E2E:** Playwright for full workflow tests

If you'd like to contribute test infrastructure, please open an issue first to discuss.

## Commit Message Guidelines

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting, no logic change)
- **refactor:** Code refactoring
- **perf:** Performance improvements
- **test:** Adding or updating tests
- **chore:** Maintenance tasks (dependencies, build, etc.)

### Examples

```bash
# Good
feat(backend): Add cost analysis endpoint
fix(frontend): Fix CSV export button not working
docs(readme): Update installation instructions
refactor(scraper): Simplify Apify error handling
chore(deps): Update FastAPI to 0.109.0

# Bad
fixed bug
update
changes
```

### Scope (optional but recommended)

- `backend` - Backend changes
- `frontend` - Frontend changes
- `docs` - Documentation
- `config` - Configuration files
- `deps` - Dependencies

## Pull Request Process

### Before Submitting

1. **Update from upstream:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test thoroughly:**
   - Run both backend and frontend
   - Test your changes in the browser
   - Check for console errors
   - Verify API endpoints work

3. **Update documentation:**
   - Update README.md if needed
   - Add comments to complex code
   - Update API.md for new endpoints
   - Update ARCHITECTURE.md for structural changes

4. **Clean up:**
   - Remove debug code
   - Remove unused imports
   - Format code consistently
   - Fix any linting errors

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How did you test these changes?

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings or errors
- [ ] Tested in browser
```

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, maintainers will merge

## Adding New Features

### Backend: New API Endpoint

1. **Define Pydantic model** (if needed):
   ```python
   # In main.py
   class MyRequest(BaseModel):
       field1: str
       field2: int = 10
   ```

2. **Create endpoint:**
   ```python
   @app.post("/my-endpoint")
   async def my_endpoint(request: MyRequest):
       try:
           # Implementation
           return {
               "status": "success",
               "data": result
           }
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))
   ```

3. **Update API docs:**
   - Add endpoint to `docs/API.md`
   - Include request/response examples
   - Document status codes

### Frontend: New Component

1. **Create component file:**
   ```bash
   touch frontend/src/components/MyComponent.jsx
   ```

2. **Implement component:**
   ```javascript
   import React, { useState } from 'react'

   function MyComponent({ prop1, prop2 }) {
     const [state, setState] = useState(null)

     return (
       <div className="p-4 bg-gray-800 rounded">
         {/* Component UI */}
       </div>
     )
   }

   export default MyComponent
   ```

3. **Import and use:**
   ```javascript
   // In App.jsx or parent component
   import MyComponent from './components/MyComponent'

   function App() {
     return (
       <div>
         <MyComponent prop1="value" prop2={123} />
       </div>
     )
   }
   ```

### Adding a New Page

1. **Create page component:**
   ```bash
   touch frontend/src/pages/MyPage.jsx
   ```

2. **Implement page:**
   ```javascript
   function MyPage() {
     return (
       <div className="p-6">
         <h1 className="text-2xl font-bold text-white mb-4">
           My Page
         </h1>
         {/* Page content */}
       </div>
     )
   }

   export default MyPage
   ```

3. **Add routing in App.jsx:**
   ```javascript
   const [view, setView] = useState('home') // Add 'mypage'

   // In render:
   {view === 'mypage' && <MyPage />}
   ```

4. **Add navigation in SidebarNav.jsx:**
   ```javascript
   <button onClick={() => setView('mypage')}>
     My Page
   </button>
   ```

### Configuration Changes

To add new audience targeting parameters:

1. **Edit `config/audience.yaml`:**
   ```yaml
   my_new_field:
     - Option 1
     - Option 2
   ```

2. **Backend automatically loads it:**
   - No code changes needed
   - Accessible via `/api/config/audience`

3. **Update frontend to use it:**
   ```javascript
   const [config, setConfig] = useState(null)

   useEffect(() => {
     fetch('http://localhost:8000/api/config/audience')
       .then(res => res.json())
       .then(data => setConfig(data.data))
   }, [])
   ```

## Questions?

If you have questions:

1. Check existing documentation in `docs/`
2. Search existing issues on GitHub
3. Create a new issue with the "question" label
4. Join our community chat (if available)

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

**Happy Contributing!** 🚀
