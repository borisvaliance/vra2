# Disaster Plan Best Practices Analyzer

A web application for uploading local government disaster plans and extracting best practices for different types of disasters (fire, flood, hurricanes, earthquakes, tornadoes).

## Features

- 📤 **Upload Disaster Plans**: Support for PDF, TXT, and DOCX formats
- 🔍 **Smart Search**: Extract best practices based on disaster type
- 🎯 **Keyword Filtering**: Refine results with optional keyword search
- 📚 **Plan Management**: View all uploaded plans with metadata
- 🌐 **Web Interface**: User-friendly interface for easy interaction

## Installation

1. Clone the repository:
```bash
git clone https://github.com/borisvaliance/vra2.git
cd vra2
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. **Upload disaster plans**:
   - Enter the government/organization name
   - Select a PDF, TXT, or DOCX file containing the disaster plan
   - Click "Upload Document"

4. **Search for best practices**:
   - Select a disaster type (Fire, Flood, Hurricane, Earthquake, Tornado)
   - Optionally add a keyword to filter results
   - Click "Search Best Practices"

5. **View uploaded plans**:
   - Scroll down to see all uploaded plans
   - Click "Refresh Plans" to update the list

## How It Works

1. **Document Upload**: The system accepts disaster plan documents in multiple formats
2. **Text Extraction**: Content is extracted from uploaded documents using PyPDF2, python-docx, or plain text readers
3. **Best Practice Identification**: The system analyzes the text using keyword matching to identify relevant best practices for specific disaster types
4. **Results Display**: Matching practices are displayed with their source information

## Disaster Types Supported

- 🔥 **Fire**: Fire safety, evacuation procedures, fire suppression
- 🌊 **Flood**: Flood preparedness, drainage, water management
- 🌀 **Hurricane**: Storm preparation, shelter protocols, emergency supplies
- ⚡ **Earthquake**: Seismic safety, structural integrity, drop-cover-hold
- 🌪️ **Tornado**: Tornado warnings, shelter procedures, severe weather response

## API Endpoints

### Upload a Disaster Plan
```
POST /upload
Content-Type: multipart/form-data

Parameters:
- file: The disaster plan document (PDF, TXT, or DOCX)
- government_name: Name of the government/organization
```

### Get All Plans
```
GET /api/plans

Returns: JSON list of all uploaded plans with metadata
```

### Get Best Practices
```
GET /api/best-practices/<disaster_type>

Parameters:
- disaster_type: Type of disaster (fire, flood, hurricane, earthquake, tornado)

Returns: JSON array of best practices for the specified disaster type
```

### Search Best Practices
```
POST /api/search
Content-Type: application/json

Body:
{
  "disaster_type": "fire",
  "keyword": "evacuation" (optional)
}

Returns: Filtered best practices matching the criteria
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Document Processing**: PyPDF2, python-docx
- **Frontend**: HTML, CSS, JavaScript
- **Storage**: In-memory database (can be extended to use SQL/NoSQL)

## Future Enhancements

- Integration with AI/NLP models (OpenAI, LangChain) for more sophisticated analysis
- Vector database (ChromaDB) for semantic search
- User authentication and authorization
- Plan comparison features
- Export functionality for best practices
- Database persistence (SQLite, PostgreSQL)
- Advanced analytics and reporting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.