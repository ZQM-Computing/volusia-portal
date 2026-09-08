# Contributing to Project Volusia

## Overview

Project Volusia is an open-source public data portal and intelligence platform for Volusia County, Florida. We welcome contributions from the community, including:

- **Developers**: Code contributions, bug fixes, feature additions
- **Data contributors**: New datasets, API integrations, indicator updates
- **Documentation**: Improvements to docs, tutorials, examples
- **Community**: Issue reporting, testing, feedback

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 20+
- Python 3.11+
- Git

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/ZQM-Computing/volusia-portal.git
cd volusia-portal

# Build and start the project
docker compose up -d

# Verify the backend is healthy
curl http://localhost:8000/health

# Verify the frontend is running
curl http://localhost:8080
```

### TypeScript Compilation

```bash
npx tsc --noEmit
```

## Contribution Types

### 1. Code Contributions

- Fork the repository and create a feature branch
- Follow the existing code structure and patterns
- Ensure TypeScript compilation passes (`npx tsc --noEmit`)
- Ensure all tests pass (`npm test`)
- Submit a pull request with a clear description

### 2. Data Contributions

- Add new indicators to the `/indicators` endpoint
- Add new datasets to the `/datasets` catalog
- Add new map layers with GeoJSON geometry
- Follow the existing data format conventions

### 3. Documentation Contributions

- Improve README, ARCHITECTURE, or API docs
- Add tutorials or examples
- Fix typos or clarify instructions

### 4. Issue Reporting

- Use the issue templates (Bug Report, Feature Request)
- Include reproduction steps and environment details
- Search existing issues before creating new ones

## Code Standards

- **TypeScript**: Strict mode, no `any` types
- **Python**: PEP 8, type hints
- **SQL**: Parameterized queries only
- **API**: RESTful conventions, proper HTTP status codes
- **Docker**: Multi-stage builds, minimal images

## Branch Protection

- All PRs require review before merging
- CI must pass before merge
- Main branch is protected

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Security

Please report security vulnerabilities to security@zqm-computing.io. Do not open public issues for security concerns.

## Contact

- **Email**: zqmcomputing@gmail.com
- **GitHub**: [ZQM-Computing/volusia-portal](https://github.com/ZQM-Computing/volusia-portal)
- **Website**: [volusia.zqmlabs.com](https://volusia.zqmlabs.com)
