# PO Management System-

This is my ERP assignment - a Purchase Order Management System which I built using Flask, PostgreSQL, JavaScript and Node.js.

---

## Stack I used-
Python · Flask · PostgreSQL · HTML/CSS/JS · Bootstrap · Node.js · Socket.IO · JWT · Gemini API · MongoDB

---

## In Detail-

**Backend** - Flask REST API split into modular route files (vendors, products, orders, auth, AI). SQLAlchemy handles the database. Every PO also automatically calculates 5% tax on creation

**Database** - PostgreSQL with 5 tables which are vendors, products, purchase_orders, po_items, users and connected through foreign keys

**Frontend** - Single-page dashboard with sidebar navigation, live stat cards, data tables, and modals. It also includes a multi currency converter like USD, INR, EUR, GBP, AED

**Real-time** - Separate Node.js + Socket.IO server that pushes live notifications to the browser whenever a PO status changes

**Auth** - JWT-based login and register. passwords are hashed before storing

**AI** - Gemini API generates a short 2 Line product description on demand. And every result is logged to MongoDB

---

## What I could not finish-
- Spring Boot vendor microservice - planned to do, but not implemented
- Google OAuth - the button exists but isn't connected yet
