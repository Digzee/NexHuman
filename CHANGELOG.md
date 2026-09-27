# Changelog

All notable changes to NexHuman will be documented in this file.

## [Unreleased]

### Planned

- Static hero visual
- Animated wave background
- Interactive 3D brain
- Orbiting cryptocurrency icons
- Landing-page polish

## [0.2.0] - 2026-08-05

### Added

- Responsive landing-page hero section
- Primary and secondary call-to-action buttons
- Hero visual placeholder
- Investment-platform value indicators
- Financial guidance disclaimer

### Changed

- Improved landing-page typography and visual hierarchy

## [0.1.0] - 2026-08-05

### Added

- React and Vite frontend
- Tailwind CSS integration
- Framer Motion and Three.js dependencies
- Reusable container and button components
- Responsive navigation bar
- Git and GitHub repository setup

### Changed

- Expanded the hero visual area
- Refined the hero description
- Updated the hero category label
- Added animated arrow indicators to hero call-to-action buttons
- Improved desktop spacing between hero content and visual

### Added

- Project architecture documentation
- NexHuman design-system documentation
- Development milestone tracker
- Static digital-brain hero visual
- Cryptocurrency icons for Bitcoin, Ethereum, Solana and Cardano
- Holographic platform and orbital visual elements

### Changed

- Replaced the generic hero placeholder with a branded investment-intelligence visual

### Added

- Animated flowing energy-wave layer behind the hero visual
- Multiple layered wave paths with independent motion
- Reduced-motion accessibility support for hero animations

### Added

- Independent floating motion for cryptocurrency icons
- Click interaction allowing cryptocurrency icons to spin
- Hover and keyboard focus states for interactive crypto elements
- Reduced-motion support for cryptocurrency animations

### Added

- Interactive brain component
- Subtle breathing and glow animation
- Mouse-responsive brain tilt
- Reduced-motion handling for brain animation

### Added

- React Three Fiber hero scene
- Procedural three-dimensional neural brain visual
- Dynamic 3D lighting
- Pointer-responsive brain orientation
- Subtle floating motion and neural particles

### Changed

- Replaced the interactive 2D brain prototype with a WebGL-rendered 3D visual

### Added

- Progressive hero entrance sequence
- Staggered landing-page content reveal
- Delayed brain materialisation
- Holographic platform entrance
- Delayed energy-wave activation
- Cryptocurrency asset entrance animation
- Reduced-motion handling for the landing-page sequence

### Added

- Responsive hero visual sizing across mobile, tablet and desktop
- Pointer-responsive ambient lighting
- Subtle hero depth and parallax effects
- Reduced-motion support for the Three.js brain scene

### Changed

- Improved mobile sizing of the Three.js hero visual
- Improved accessibility of decorative hero graphics
- Limited WebGL pixel density for more predictable rendering performance

### Architecture

- Defined domain-oriented Django backend architecture
- Selected PostgreSQL as the primary database
- Defined email-based JWT authentication architecture
- Defined backend-mediated market-data architecture
- Defined persistent optimisation-run history
- Defined investment profiling as a separate backend domain
- Defined persistent, context-aware AI advisor architecture

### Backend
- Added Django 5.2 backend with Django REST Framework.
- Added PostgreSQL database integration using Psycopg.
- Added environment-based configuration for application secrets and database credentials.
- Added CORS configuration for local frontend development.
- Added a custom email-based user model and user manager.
- Added initial database migrations.
- Added Django Admin support for the custom user model.

### Authentication
- Added user registration API with email-based account creation.
- Added Django password validation and secure password hashing.
- Added validation for required names, unique email addresses and password strength.
- Added automated registration API tests.
- Added React registration page with field-level validation feedback.
- Integrated the React registration flow with the Django REST API.
- Added loading, success and API error states to registration.
- Added JWT-based email and password login.
- Added access and refresh token generation.
- Added refresh-token endpoint and token rotation.
- Added automated tests for successful login, invalid credentials and token refresh.
- Added React login page with loading, success and error states.
- Integrated the login page with the Django REST API.
- Added Login and Register navigation to the landing page.
- Improved reusable Button component to support internal navigation.
- Added authenticated current-user API endpoint.
- Added central React authentication state using AuthContext.
- Added JWT session restoration using refresh-token rotation.
- Added protected frontend routes for authenticated users.
- Added session persistence across page refreshes.
- Added server-side logout with refresh-token blacklisting.
- Added a protected dashboard placeholder for Phase 3.
- Added automated tests for authenticated-user access and refresh-token invalidation.
- Added secure password-reset request and confirmation endpoints.
- Added Django token-based password-reset workflow.
- Added account-enumeration protection for password-reset requests.
- Added development password-reset email delivery.
- Added forgot-password and new-password frontend flows.
- Added password-strength validation to password resets.
- Added automated password-reset tests.
- Centralised the frontend API base URL using Vite environment configuration.
- Improved logout security using server-side refresh-token blacklisting.
- Completed authentication accessibility, security and integration testing.

### Portfolio Management

- Added portfolio and portfolio asset database models.
- Added authenticated portfolio REST API endpoints.
- Added user ownership protection for portfolio resources.
- Added portfolio API test coverage.
- Added portfolio creation and selection interface.
- Added cryptocurrency holding creation, editing and deletion.
- Added persistent portfolio management backed by PostgreSQL.
- Refactored portfolio interface into reusable React components.
- Added reusable authenticated API requests.
- Added automatic JWT access-token refresh and request retry.
- Improved portfolio editing and error-handling behaviour.

### Market Data and Portfolio Analytics

- Added provider-agnostic cryptocurrency market-data service.
- Added CoinGecko integration for current and historical cryptocurrency prices.
- Added supported cryptocurrency registry and authenticated API.
- Restricted portfolio holdings to supported active cryptocurrencies.
- Added supported-asset selector to portfolio management.
- Added tested portfolio valuation service using live market prices.
- Added cost-basis-aware profit, return and coverage calculations.
- Added authenticated ownership-protected portfolio valuation endpoint.
- Added live portfolio overview with automatic valuation refresh.
- Added market-value-based asset allocation calculations.
- Added asset allocation table and composition summary.
- Added responsive portfolio allocation visualisation.

### Portfolio Dashboard

- Added authenticated dashboard application shell with responsive navigation.
- Added persistent user-owned cryptocurrency portfolios and holdings.
- Added portfolio creation, selection and asset management.
- Added supported cryptocurrency registry backed by CoinGecko identifiers.
- Added provider-independent market data service architecture.
- Added live cryptocurrency valuation using CoinGecko market data.
- Added portfolio value, profit/loss, return and cost-basis coverage metrics.
- Added portfolio allocation calculations and interactive allocation visualisation.
- Added historical portfolio performance analysis across 1M, 3M, 6M and 1Y periods.
- Added total return and annualised return calculations.
- Added annualised volatility using a 365-day cryptocurrency convention.
- Added maximum drawdown calculation.
- Added historical performance visualisation using current portfolio holdings.
- Added portfolio risk analysis using volatility, drawdown and concentration.
- Added HHI-style portfolio concentration and diversification analysis.
- Added transparent portfolio risk classification.
- Added responsive portfolio Risk Summary interface.
- Added current-price and historical-price market data caching.
- Added deterministic tests for portfolio analytics and market data caching.
- Added authenticated and ownership-protected valuation, performance and risk APIs.
- Completed end-to-end Portfolio Dashboard integration testing.
- Completed responsive and accessibility review.