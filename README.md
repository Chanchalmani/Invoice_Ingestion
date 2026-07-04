# Local AI Invoice Processing Workflow

This repository contains the complete configuration and code to build an automated, locally hosted invoice processing system using **n8n**, **Ollama (Llama 3.2:3b)**, and **NocoDB**.

## Prerequisites
- Docker & Docker Compose (or direct installations of the services below)
- Python 3.9+ (for running the synthetic invoice generator and test scripts)
- Node.js (optional, for running JS tests)

## Setup Instructions

### 1. Start Services
Ensure you have the following running on your local machine:
1. **Ollama**: Download and install from [ollama.com](https://ollama.com). 
   - Pull the model: `ollama run llama3.2:3b`
2. **n8n**: The easiest way is via Docker:
   ```bash
   docker run -it --rm --name n8n -p 5678:5678 -e N8N_HOST=localhost -e WEBHOOK_URL=http://localhost:5678/ -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
   ```
3. **NocoDB**: Via Docker:
   ```bash
   docker run -d --name nocodb -v nocodb:/usr/app/data/ -p 8080:8080 nocodb/nocodb:latest
   ```

### 2. Configure NocoDB
1. Navigate to `http://localhost:8080` and complete the initial setup.
2. Create a new Base/Project.
3. If using Postgres, run the SQL script located in `database/nocodb_schema.sql`. Otherwise, manually create the `invoices` table with columns matching the schema (Vendor, Amount, Status, etc.).
4. Generate an API Key (Auth Token) from NocoDB settings and note the Project ID.

### 3. Import n8n Workflows
1. Navigate to `http://localhost:5678`.
2. Go to **Workflows -> Add Workflow**.
3. Use the **Import from File** option to load the 4 workflows found in the `n8n_workflows` directory:
   - `workflow_1_ingestion.json`
   - `workflow_2_manual_review.json`
   - `workflow_3_approval_scheduler.json`
   - `workflow_4_approval_handler.json`
4. Update the nodes with your environment variables & configurations:
   - **IMAP Node**: Enter your email address and password/app password. **CRITICAL:** Ensure **"Download Attachments"** is toggled **ON** in the options. (If using a dedicated invoice inbox, you can delete any "Has Attachment?" IF node and connect directly to the PDF extractor).
   - **Extract Text from PDF Node**: Ensure the "Binary Property" is set to `attachment_0` (not `data`).
   - **Ollama HTTP Node**: Ensure the URL points to your local Ollama instance. **CRITICAL:** Change **"Specify Body"** to **JSON** and paste the raw JSON payload to ensure `stream: false` is sent as a strict boolean (avoiding hidden newline characters).
   - **Clean Data Node**: If testing via "Execute step" manually, comment out any lines referencing previous nodes (like `$('Email Read')`) to avoid "Referenced node doesn't exist" errors.
   - **NocoDB Node**: Setup the NocoDB credentials. Ensure **"Data to Send"** is set to **Auto-Map Input Data to Columns** so the AI's JSON output perfectly maps to your database schema.

## Environment Variables / Secrets Needed
- `IMAP_USER`: Your test email address
- `IMAP_PASS`: Your email password (or App Password)
- `NOCODB_API_TOKEN`: NocoDB authentication token
- `OLLAMA_URL`: Typically `http://localhost:11434`

## Workflow Explanations
1. **Ingestion**: Listens to an IMAP inbox. If an email has a PDF attachment, it extracts the text using n8n's native PDF extractor, passes the text to Ollama with a strict JSON prompt, parses/cleans the JSON using a Code Node, and saves the record in NocoDB.
2. **Manual Review**: A webhook that serves an HTML form. It pulls the invoice from NocoDB, displays it for editing, and allows a user to check "Send for Approval". When submitted, it updates the database.
3. **Approval Scheduler**: A cron job that runs every 5 minutes. It queries NocoDB for invoices where `send_for_approval=true` and `status='Draft'`, sets their status to `Pending Approval`, and sends an email to the approver with Approve/Reject links.
4. **Approval Handler**: A webhook that processes the Approve/Reject clicks and updates the final status in NocoDB.

## Assumptions
- The target email inbox is accessible via standard IMAP.
- Invoices are native, text-based PDFs (not scanned images requiring Tesseract, although n8n can integrate with external OCR APIs if needed later).
- You are running on a local Windows machine. If n8n runs in Docker and Ollama on Windows host, `host.docker.internal` is used to map to localhost.

---

## Screen Recording Walkthrough Script

**[Scene 1: Starting Services]**
- **Action**: Open terminal, start Ollama (`ollama run llama3.2:3b`).
- **Narrator**: "First, we ensure our local Llama 3.2 model is running via Ollama."
- **Action**: Switch to browser showing NocoDB running at localhost:8080.
- **Narrator**: "Here is our NocoDB instance, showing the empty `invoices` table created using the provided SQL schema."

**[Scene 2: Sending the Test Invoice]**
- **Action**: Run `python tests/generate_sample_invoice.py` in the terminal to generate `sample_invoice.pdf`.
- **Narrator**: "We generate a synthetic PDF invoice using our Python script."
- **Action**: Open an email client and send an email to the monitored inbox with the PDF attached.
- **Narrator**: "We send this PDF to the monitored IMAP inbox."

**[Scene 3: n8n Workflow Execution]**
- **Action**: Switch to the n8n UI, showing the "Ingestion" workflow. Click "Execute Workflow" (or wait for trigger).
- **Narrator**: "The n8n workflow triggers upon receiving the email. It extracts the text and sends it to local Ollama. Notice how the AI responds with perfectly structured JSON, which our Code node cleans and validates."

**[Scene 4: Verifying the Record]**
- **Action**: Switch to the NocoDB tab and refresh.
- **Narrator**: "Looking at NocoDB, the invoice data is populated perfectly. Vendor, amounts, and the status is set to 'Draft'."

**[Scene 5: Manual Review UI]**
- **Action**: Open a new browser tab and navigate to `http://localhost:5678/webhook-test/review-invoice?id=1` (or whichever ID).
- **Narrator**: "Next, an operator accesses the manual review UI served directly by an n8n webhook. Here, they can adjust any misread fields, select a department, and check the 'Send for Approval' box. Let's submit this."

**[Scene 6: Approval Routing]**
- **Action**: Switch back to n8n, open the "Approval Scheduler" workflow, and manually execute it to simulate the 5-minute cron.
- **Narrator**: "The scheduled workflow runs, finds our pending invoice, updates its status to 'Pending', and sends an approval email."
- **Action**: Show a mocked email (or console log) with the Approve/Reject links. Click "Approve".
- **Narrator**: "The manager clicks 'Approve'."

**[Scene 7: Final Status]**
- **Action**: Switch back to NocoDB and refresh.
- **Narrator**: "Finally, in NocoDB, we can see the status is now updated to 'Fully Approved'."

**[Scene 8: Error Handling / Duplicates]**
- **Action**: Resend the same PDF.
- **Narrator**: "If we process the same invoice again, our database schema's unique constraint on Vendor + Invoice Number causes NocoDB to reject the insert, preventing duplicates. If the AI is unconfident, our cleaning script flags it with anomalies and sets the status to 'Needs Review'."
