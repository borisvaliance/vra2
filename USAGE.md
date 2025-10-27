# Running the Application

Follow these steps to set up and run the Disaster Plan Best Practices Analyzer:

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/borisvaliance/vra2.git
   cd vra2
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Testing

Run the test suite to verify the installation:

```bash
python test_app.py
```

## Usage Example

1. **Upload a disaster plan**:
   - Enter the government/organization name (e.g., "City of Springfield")
   - Select a PDF, TXT, or DOCX file containing the disaster plan
   - Click "Upload Document"

2. **Search for best practices**:
   - Select a disaster type from the dropdown (Fire, Flood, Hurricane, Earthquake, Tornado)
   - Optionally add a keyword to filter results (e.g., "evacuation", "shelter")
   - Click "Search Best Practices"

3. **View results**:
   - Best practices will be displayed with their source information
   - Each practice shows which government plan it came from

## Sample Data

A sample disaster plan is included in `sample_plans/springfield_disaster_plan.txt` for testing purposes.

## Supported File Formats

- **PDF**: Portable Document Format
- **TXT**: Plain text files
- **DOCX**: Microsoft Word documents

## Features

- ✅ Upload disaster plans from local governments
- ✅ Extract text from PDF, TXT, and DOCX files
- ✅ Search for best practices by disaster type
- ✅ Filter results by keyword
- ✅ View all uploaded plans with metadata
- ✅ Beautiful, responsive web interface

## Technology Stack

- **Backend**: Flask (Python)
- **Document Processing**: PyPDF2, python-docx
- **Frontend**: HTML5, CSS3, JavaScript
- **Storage**: In-memory (can be extended to SQL/NoSQL databases)
