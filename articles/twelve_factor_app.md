# The twelve-factor app

Personal notes based on the twelve-factor app methodology.
See the original site, Written by Adam Wiggins: https://12factor.net

## Introduction

- Methodology for building SaaS apps.
- Automation to reduce friction for new contributors.
- Offer maximum portability between environments.
- Minimize divergence between development and production.
- Scale up without significant changes.

## 1. Codebase

- Use a version control system (Git, Mercurial, Subversion)
- Codebase is a single or set of code repositories.
- Multiple codebases: distributed system $\ne$ app.
  - Each codebase can comply with 12FA.
- Multiple apps sharing code is not allowed.
  - Factor shared code into libraries.
  - Include libraries via dependency manager.
- An app will have many deploys
  - Deploy: Running instance of the app.
  - Normally production, staging and development in local environments.
  - Codebase is the same for all deploys.
  - Different versions may be active in each deployment.

## 2. Dependencies

- Packing system for distributing support libraries.
- Libraries can be system-wide (site packages) or scoped into the directory (vendoring/bundling).
- The 12FA must declare dependencies via a dependency declaration manifest.
  - E.g Pip for Python
- Must use a dependency isolation tool to avoid leaked in dependencies.
  - E.g Virtualenv for Python.
- Dependency specification is applied uniformly to both production and development.
- This simplifies setup for new developers.
- 12FA app must also vendor system tools that could not be installed on the system (e.g curl).

## 3. Config

- Config is everything that may vary between deploys.
  - Credentials to external service, a host name for a deploy, database handles.
- Configuration must be separate from code.
  - Code should not substantially vary across deploys.
  - Ask yourself: Can the codebase be made open source without compromising credentials/secrets?
- Configs that don't vary between deploys can be done in code.
- For configs that do vary, can be done in code but not checked into revision control.
- A better alternative is to store using environment variables.
  - Hard to check into a repo.
  - Language and OS agnostic.
- Don't group env vars by deploys (development, test, production, etc.)
  - Won't scale well, hard to track.
  - Declare env vars as granular controls.

## 4. Backing services

- Backing service is any service the app consumers over the network.
  - Databases, messaging queues, email service or caching systems.
- Can be locally managed services or third-party services.
- The 12FA must not make any distinction between local or third-party services.
  - Both are attached resources accessed via URL or credentials on config.
  - Should be able to swap locally managed service for third-party service without code changes (e.g local MySQL for RDS).
- Each service is a resource.
- The app should treat resources as attached, indicating loose coupling.
- The app should be able to handle resources being attached and detached from deploys without code changes.
  - E.g Database goes down, a new instance is attached via env config change.

