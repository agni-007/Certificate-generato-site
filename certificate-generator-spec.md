# Certificate Generator — Complete Project Specification & Build Workflow

## 1. Project Overview

Build a simple, modern, fast, and reliable web application for generating personalized certificates in bulk.

The application must allow a user to:

- Upload a different certificate template every time
- Support PDF, PNG, and JPG/JPEG templates
- Enter names manually as text
- Upload names through Excel or CSV
- Preview the certificate
- Position the name visually on the certificate
- Configure basic text properties
- Generate certificates in bulk
- Download all generated certificates as a ZIP file

The goal is to replace the existing manual Python workflow in the repository with a proper web application.

The existing repository already contains certificate-generation logic using Python, pandas, PyMuPDF, and Excel input. Reuse the useful parts of that implementation instead of unnecessarily rewriting working PDF-generation logic.

---

## 2. Main Goal

The final application should provide this workflow:

```text
Upload Template
      ↓
PDF / PNG / JPG / JPEG
      ↓
Add Names
      ↓
Manual Text OR Excel/CSV
      ↓
Preview Certificate
      ↓
Position Name
      ↓
Configure Font / Size / Color / Alignment
      ↓
Generate Certificates
      ↓
Generate PDFs in Bulk
      ↓
Create ZIP
      ↓
Download ZIP
```

The user should never need to manually run the Python script.

---

## 3. Core Requirements

### 3.1 Template Upload

The application must accept:

- `.pdf`
- `.png`
- `.jpg`
- `.jpeg`

The user can upload a completely different template every time. There must be **no** dependency on a fixed `template.pdf` stored inside the repository. The uploaded template is processed temporarily.

### 3.2 Name Input

Provide two methods.

**Method A — Manual Names**

Allow the user to enter names in a text area. Each line represents one certificate.

```text
Agnivesh S
Rahul Kumar
Ananya Menon
Arjun Raj
```

**Method B — Excel / CSV**

Allow `.xlsx` and `.csv`.

Example Excel:

```text
Name
Agnivesh S
Rahul Kumar
Ananya Menon
Arjun Raj
```

The backend should:

1. Read the file.
2. Look for a column called `Name`, case-insensitive.
3. If `Name` is not found, use the first column.
4. Ignore empty rows.
5. Clean whitespace.
6. Return the extracted names to the frontend.

---

## 4. Certificate Template Processing

### PDF Template

If the uploaded template is a PDF:

- Open it using PyMuPDF.
- Use the first page as the certificate background.
- Preserve the original page dimensions.
- Add the personalized name on top.

Initially support the first page only. The architecture should make multi-page support possible later.

### Image Template

If the uploaded template is PNG, JPG, or JPEG:

- Convert the image into a PDF-compatible background using Pillow/PyMuPDF.
- Preserve the image's aspect ratio.
- Do not stretch the certificate unnecessarily.

---

## 5. Name Positioning

Do **not** require the user to put `NAME_PLACEHOLDER` inside the certificate. The new application should support visual positioning.

The uploaded certificate should appear in a preview/editor:

```text
+--------------------------------------+
|                                      |
|           CERTIFICATE                |
|                                      |
|                                      |
|             Agnivesh S               |
|                                      |
|        For participating in...       |
|                                      |
+--------------------------------------+
```

The user should be able to drag the name to the required position.

Store the position as normalized coordinates where possible (`x`, `y`). Prefer percentages or normalized coordinates rather than hardcoded browser pixels:

```json
{
  "x": 50,
  "y": 52
}
```

This allows the position to remain correct when the preview size changes.

---

## 6. Text Configuration

Provide basic controls:

- Font
- Font Size
- Text Color
- Alignment

Example:

```text
Font: Times Italic
Font Size: 37
Color: White
Alignment: Center
```

Keep the number of options small. Do not build an unnecessarily complicated graphics editor.

---

## 7. Preview

The user must be able to see approximately how the generated certificate will look before generating hundreds of certificates.

The preview should:

- Display the uploaded template.
- Display a sample name.
- Allow the sample name to be dragged.
- Reflect font size changes.
- Reflect font changes.
- Reflect text color.
- Reflect alignment.

Use the first entered name as the preview name. If no name has been entered yet, use `Sample Name`.

---

## 8. Generation

When the user clicks **Generate Certificates**, the frontend sends the following to the backend:

- Template
- Names
- Position
- Font
- Font size
- Text color
- Alignment

The backend should:

1. Validate the template.
2. Validate the names.
3. Convert image templates if necessary.
4. Load the template once.
5. Generate one PDF per name.
6. Save generated PDFs temporarily.
7. Create a ZIP file.
8. Return the ZIP to the frontend.

---

## 9. Generated Files

For the names `Agnivesh S`, `Rahul Kumar`, `Ananya Menon`, generate:

```text
certificate_Agnivesh_S.pdf
certificate_Rahul_Kumar.pdf
certificate_Ananya_Menon.pdf
```

- Remove unsafe filename characters.
- Avoid overwriting files unexpectedly.

---

## 10. ZIP Download

After generation, the ZIP should contain:

```text
certificates/
├── certificate_Agnivesh_S.pdf
├── certificate_Rahul_Kumar.pdf
└── certificate_Ananya_Menon.pdf
```

Create `certificates.zip`. The user should be able to download the ZIP with one click.

---

## 11. Progress Indicator

Bulk generation can take some time. The frontend should show a simple progress state:

```text
Generating certificates...

████████████████░░░░ 80%

80 / 100 certificates
```

The exact implementation can be simple. Do not introduce complicated job queues for the first version unless genuinely required.

---

## 12. Error Handling

The application should provide clear errors.

| Case | Message |
|---|---|
| No template | Please upload a certificate template. |
| Invalid template | Unsupported template format. Please upload PDF, PNG, JPG, or JPEG. |
| No names | Please enter at least one name. |
| Empty Excel | No valid names were found in the uploaded file. |
| Invalid Excel | Unable to read the uploaded Excel file. Please check the file and try again. |
| Generation failure | Something went wrong while generating the certificates. Please try again. |

Do not expose Python stack traces to the user. Log technical errors on the backend.

---

## 13. Technology Stack

### Frontend

- **Next.js** — web application
- **React** — interactive components
- **TypeScript** — frontend development
- **Tailwind CSS** — styling

Keep the interface clean and minimal.

### Backend

- **Python** — certificate generation
- **FastAPI** — the API. It should handle:
  - File uploads
  - Name extraction
  - Certificate generation
  - ZIP creation
  - Validation
  - Temporary files

---

## 14. Python Libraries

Use:

- PyMuPDF
- Pillow
- pandas
- openpyxl

For ZIP generation use Python's built-in `zipfile`. Do not add unnecessary dependencies.

---

## 15. Frontend Architecture

Recommended structure:

```text
frontend/
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   └── globals.css
│
├── components/
│   ├── TemplateUpload.tsx
│   ├── NameInput.tsx
│   ├── CertificatePreview.tsx
│   ├── TextSettings.tsx
│   ├── PositionEditor.tsx
│   ├── GenerateButton.tsx
│   └── DownloadButton.tsx
│
├── lib/
│   └── api.ts
│
├── public/
│
├── package.json
└── tsconfig.json
```

The exact component structure can be simplified if the coding agent determines that fewer files are cleaner. Do not create unnecessary abstractions.

---

## 16. Backend Architecture

Recommended structure:

```text
backend/
├── app/
│   ├── main.py
│   ├── generator.py
│   ├── parser.py
│   └── utils.py
│
├── requirements.txt
└── README.md
```

Responsibilities:

- `main.py` — FastAPI application and endpoints.
- `generator.py` — Certificate generation logic.
- `parser.py` — Excel/CSV/name extraction.
- `utils.py` — Temporary files, filenames, validation, and helper functions.

The exact structure can be adjusted if there is a simpler implementation.

---

## 17. API

Keep the API simple.

### Health

`GET /health`

```json
{
  "status": "ok"
}
```

### Extract Names

`POST /api/names`

Accepts `.xlsx` and `.csv`. Returns:

```json
{
  "names": [
    "Agnivesh S",
    "Rahul Kumar",
    "Ananya Menon"
  ]
}
```

### Generate Certificates

`POST /api/generate`

Accepts: `template`, `names`, `x`, `y`, `font`, `fontSize`, `color`, `alignment`.

Returns the generated ZIP file.

---

## 18. Temporary Storage

Do not permanently store uploaded files. Use temporary directories:

```text
temporary/
├── template/
├── input/
└── output/
```

Lifecycle:

```text
Upload → Process → Generate → ZIP → Download → Delete temporary files
```

The backend must clean up temporary files after the request is completed. Also ensure temporary files are not accidentally committed to Git.

---

## 19. No Database Initially

Do **not** add any of the following for the first version:

- PostgreSQL
- MongoDB
- Firebase
- Supabase
- Redis
- S3
- Cloud storage

There is no requirement to permanently store templates, names, generated certificates, user accounts, or generation history. The application processes the user's current request and returns the result.

---

## 20. Hosting Architecture

```text
             GitHub
                |
       +--------+--------+
       |                 |
       v                 v
    Vercel             Render
       |                 |
       v                 v
   Next.js             FastAPI
   Frontend            Backend
```

### Frontend Hosting — Vercel

- Connect the GitHub repository.
- Automatically deploy the Next.js frontend.
- Enable HTTPS.
- Configure the backend API URL using environment variables:

```text
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

Do not hardcode production URLs inside components.

### Backend Hosting — Render

Deploy the FastAPI backend from GitHub.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The exact command should match the final project structure. Use a production-capable paid instance if continuous availability is required. The application should not depend on the developer's personal computer being online.

### HTTPS

HTTPS should be handled by the hosting platforms. Do **not** manually generate SSL certificates. Do **not** configure Nginx unless there is an actual requirement.

---

## 21. Environment Variables

- Frontend: `NEXT_PUBLIC_API_URL`
- Backend: only use environment variables if necessary.

Do not put secrets directly into source code. No API keys are required for the basic application.

---

## 22. Security Requirements

Implement basic security.

**File validation** — check file extension, MIME type where practical, file size, and valid PDF/image structure.

**Filename sanitization** — never directly use user-uploaded filenames as filesystem paths.

**Temporary storage** — never expose temporary server paths to the frontend.

**Limits** — add reasonable, easily configurable limits for:

- Maximum template size
- Maximum number of names
- Maximum Excel/CSV size

**No arbitrary file execution** — uploaded files must only be processed as data. Never execute uploaded files.

---

## 23. Performance Requirements

Optimize for normal bulk certificate generation. Load/process the template efficiently and do not repeatedly perform expensive template conversion.

```text
Image template → Convert once → Reusable PDF/template representation → Generate all certificates
```

```text
PDF template → Open once → Reuse template → Generate certificates
```

Avoid unnecessary disk operations.

---

## 24. UI Design

The UI should be modern but simple. Do not make it look like an enterprise dashboard.

```text
------------------------------------------------

             Certificate Generator

  Create personalized certificates in seconds.

------------------------------------------------

  1. Certificate Template

  [ Upload Template ]

  PDF, PNG, JPG, JPEG

------------------------------------------------

  2. Names

  [ Enter names manually ]

  OR

  [ Upload Excel / CSV ]

------------------------------------------------

  3. Certificate Preview

  +------------------------------------------+
  |                                          |
  |             CERTIFICATE                  |
  |                                          |
  |              Sample Name                 |
  |                                          |
  |                                          |
  +------------------------------------------+

  Drag the name to position it.

------------------------------------------------

  Text Settings

  Font:       [ Times Italic ]
  Size:       [ 37 ]
  Color:      [ White ]
  Alignment:  [ Center ]

------------------------------------------------

             [ Generate Certificates ]

------------------------------------------------

             Generation Progress

             80 / 100

             [ Download ZIP ]

------------------------------------------------
```

Make it responsive for desktop, laptop, tablet, and mobile.

### Design Principles

Use:

- Clean layout
- Good spacing
- Clear buttons
- Minimal colors
- Simple typography
- Clear status messages
- Drag-and-drop upload where useful

Avoid:

- Excessive animations
- Unnecessary pages
- Complex dashboards
- Login systems
- User accounts
- Unnecessary settings
- Overengineering

---

## 25. Existing Repository Integration

The existing project contains a Python certificate generator.

Existing workflow:

```text
template.pdf
      +
v.xlsx
      ↓
script.py
      ↓
certificates_output/
```

The new application should transform this into:

```text
Web Interface
      ↓
Upload Template
      +
Names
      +
Settings
      ↓
FastAPI
      ↓
Certificate Generator
      ↓
ZIP
      ↓
Download
```

Reuse the existing PyMuPDF generation approach where appropriate. Do not preserve limitations such as:

```python
PDF_TEMPLATE = "template.pdf"
EXCEL_FILE = "v.xlsx"
PLACEHOLDER_TEXT = "NAME_PLACEHOLDER"
```

The new application must accept these dynamically from the user.

---

## 26. Implementation Order

### Phase 1 — Repository Setup

Create `frontend/` and `backend/`, then set up Next.js, TypeScript, Tailwind, FastAPI, a Python virtual environment, and `requirements.txt`. Verify both applications run locally.

### Phase 2 — Backend Generator

Implement:

1. PDF template loading
2. PNG/JPG/JPEG conversion
3. Name extraction
4. Text insertion
5. Positioning
6. Font settings
7. PDF output
8. ZIP creation

Test with multiple names.

### Phase 3 — Backend API

Implement `GET /health`, `POST /api/names`, and `POST /api/generate`. Test the API independently.

### Phase 4 — Frontend

Implement:

1. Template upload
2. Manual name input
3. Excel/CSV upload
4. Preview
5. Position controls
6. Text controls
7. Generate button
8. Progress state
9. ZIP download

### Phase 5 — Integration

Connect Next.js to FastAPI and test the complete workflow.

### Phase 6 — Error Handling

Test:

- No template
- Unsupported template
- Corrupt PDF
- Corrupt image
- Empty name list
- Empty Excel
- Excel without names
- Large file
- Special characters in names
- Duplicate names
- Very long names

### Phase 7 — Performance

Test with 10, 50, 100, and 500 names. Optimize only where necessary. Do not prematurely introduce complex infrastructure.

### Phase 8 — Deployment

Deploy the frontend to Vercel and the backend to Render. Configure `NEXT_PUBLIC_API_URL` and test the production API connection.

### Phase 9 — Production Testing

Test the complete production workflow:

```text
Open website → Upload PDF → Enter names → Position name → Generate → Download ZIP
```

Then:

```text
Upload PNG → Upload Excel → Generate 100 certificates → Download ZIP
```

Then:

```text
Upload JPG → Upload CSV → Generate certificates → Download ZIP
```

---

## 27. Definition of Done

The project is complete only when:

- [ ] Frontend works locally
- [ ] Backend works locally
- [ ] PDF templates work
- [ ] PNG templates work
- [ ] JPG/JPEG templates work
- [ ] Manual names work
- [ ] Excel works
- [ ] CSV works
- [ ] Name column detection works
- [ ] Preview works
- [ ] Name can be positioned
- [ ] Font settings work
- [ ] Bulk generation works
- [ ] ZIP generation works
- [ ] ZIP download works
- [ ] Temporary files are cleaned
- [ ] Error handling works
- [ ] Production frontend is deployed
- [ ] Production backend is deployed
- [ ] HTTPS works
- [ ] Frontend/backend communication works
- [ ] Production generation has been tested
- [ ] README contains setup instructions
- [ ] No unnecessary files or dependencies remain

---

## 28. Future Features

Do **not** implement these in the first version unless they become necessary:

- User accounts
- Saved templates
- Generation history
- Custom domains
- Multiple text fields
- QR codes
- Logos
- Signatures
- Multiple pages
- Custom fonts
- Cloud storage
- PostgreSQL
- Batch history
- Certificate verification links
- Unique certificate IDs
- Email delivery

The first version should remain focused on:

```text
Template + Names + Position + Generate + Download
```

---

## 29. Complete Build Instruction for Coding Agent

### Agent Prompt

You are the implementation agent for this project.

Build the complete Certificate Generator web application described in this document.

### Important Instructions

- Do NOT stop after creating a plan.
- Do NOT ask me for permission to implement individual features.
- Do NOT ask me whether you should create files.
- Do NOT repeatedly ask for confirmation.
- Do NOT wait for approval between implementation phases.

You have authorization to build the entire application according to this specification. Make reasonable implementation decisions yourself when something is not explicitly specified. If a minor implementation detail is ambiguous, choose the simplest reliable solution and continue. Only stop when the application is fully implemented and tested. After implementation is complete, present the finished project for my review.

### Agent Objectives

Build with: **Next.js + React + TypeScript + Tailwind CSS + FastAPI + Python + PyMuPDF + Pillow + pandas + openpyxl**, with a **Vercel** frontend and **Render** backend as the intended deployment architecture.

### Agent Workflow

Follow this process automatically.

**1. Inspect Existing Repository**

Understand the current files, the existing Python generator, the README, existing dependencies, and the existing certificate generation logic. Reuse working logic where practical. Do not unnecessarily rewrite working functionality.

**2. Build Backend**

Create the FastAPI backend with `/health`, `/api/names`, and `/api/generate`. Implement dynamic template handling (PDF, PNG, JPG, JPEG), manual names, Excel, and CSV support, certificate generation, ZIP generation, and temporary file cleanup.

**3. Build Frontend**

Create the Next.js frontend with: template upload, name input, Excel/CSV upload, certificate preview, draggable name, font controls, size controls, color controls, alignment controls, generate button, progress state, and ZIP download. Keep the UI simple.

**4. Integrate**

Connect frontend and backend. Do not use mock data once the backend is available. The actual certificate generation workflow must work end-to-end.

**5. Test**

Test every combination:

```text
PDF + manual names      PDF + Excel      PDF + CSV
PNG + manual names      PNG + Excel      PNG + CSV
JPG + manual names      JPG + Excel      JPG + CSV
```

Also test 10 names and 100 names where practical. Check that the generated certificates contain the correct names and that the ZIP opens correctly.

**6. Fix Problems**

If tests fail: identify the cause, fix the implementation, run the test again, and continue until working. Do not stop and ask me to fix something that you can reasonably fix yourself.

**7. Clean the Project**

Before finishing, remove unused dependencies, temporary test files, debug code, hardcoded local paths, old fixed-template assumptions, and unnecessary files.

Ensure the following are not committed, and create appropriate `.gitignore` files:

- `.env`
- `node_modules/`
- `__pycache__/`
- temporary files
- generated certificates

**8. Documentation**

Update the README with: project description, features, architecture, local setup, frontend setup, backend setup, environment variables, running locally, deployment, Vercel configuration, and Render configuration. Keep documentation practical and concise.

**9. Final Verification**

Before declaring the project finished, verify: frontend starts, backend starts, API responds, template uploads, names load, preview works, position works, generation works, ZIP works, download works. Do not declare completion until the core workflow is functional.

---

## 30. Final Expected User Experience

```text
                 CERTIFICATE GENERATOR

        Create personalized certificates quickly.


       ┌─────────────────────────────────┐
       │                                 │
       │      Upload Certificate         │
       │                                 │
       │        [ Choose File ]          │
       │                                 │
       │      PDF / PNG / JPG / JPEG     │
       │                                 │
       └─────────────────────────────────┘


       Add Names

       ○ Enter manually
       ○ Upload Excel / CSV


       ┌─────────────────────────────────┐
       │ Agnivesh S                      │
       │ Rahul Kumar                     │
       │ Ananya Menon                    │
       │ Arjun Raj                       │
       └─────────────────────────────────┘


       Certificate Preview

       ┌─────────────────────────────────┐
       │                                 │
       │          CERTIFICATE            │
       │                                 │
       │           Agnivesh S            │
       │                                 │
       │      For participating in...    │
       │                                 │
       └─────────────────────────────────┘

       Drag the name to position it.


       Font: [ Times Italic ]

       Size: [ 37 ]

       Color: [ White ]

       Alignment: [ Center ]


             [ GENERATE CERTIFICATES ]


             Generating...

             ████████████████░░░░

             80 / 100


             [ DOWNLOAD ZIP ]
```

The final goal is a simple certificate-generation tool that can be opened from anywhere, accepts a new template and name list for every job, generates certificates automatically, and requires no manual Python execution.
