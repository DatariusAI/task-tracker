# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

DatariusAI is a Node.js/Express API (CommonJS modules).

## Commands

- **Install dependencies:** `npm install`
- **Start server:** `npm start` (runs on port 3000 by default, configurable via `PORT` env var)
- **Run tests:** `npm test` (not yet configured)

## Architecture

- `index.js` — entry point, starts the Express server
- `src/app.js` — Express app setup and middleware registration
- `src/routes/` — route definitions (maps URLs to controllers)
- `src/controllers/` — request handlers (business logic)
