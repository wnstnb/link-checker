# Link Checker Application

A Streamlit-based web application for validating and classifying business URLs against their associated business names using AI-powered content analysis.

## Features

- 📁 **CSV Upload**: Upload files with business names and URLs
- 🔍 **Content Retrieval**: Automatically scrape and extract content from URLs using Exa.AI
- 🤖 **AI Classification**: Use GPT OSS 120B to classify if content matches the business
- 📊 **Results Analysis**: View detailed results with website working status and classification
- ⏱️ **Processing Time**: Track start time, end time, and duration
- 📥 **Export Results**: Download processed results as CSV
- 🔧 **Debug Information**: Built-in debugging tools for troubleshooting

## Installation

### Prerequisites

- Python 3.8 or higher
- API keys for Exa.AI and OpenRouter

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/link-checker.git
   cd link-checker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   EXA_API_KEY=your_exa_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Access the application:**
   Open your browser and go to `http://localhost:8501`

## Usage

### Preparing Your CSV File

Create a CSV file with the following columns:
- `business_name`: The name of the business
- `URL`: The URL associated with the business

**Example CSV:**
```csv
business_name,URL
Apple Inc,https://www.apple.com
Tesla Inc,https://www.tesla.com
Google LLC,https://www.google.com
```

### Processing URLs

1. **Upload CSV File**: Use the file upload component to select your CSV file
2. **Review Preview**: Check the data preview to ensure it's correct
3. **Start Processing**: Click "Process URLs" to begin
4. **Monitor Progress**: Watch the progress bar and status updates
5. **View Results**: Review the processed results table
6. **Download Results**: Export the results as a CSV file

### Understanding Results

The application provides the following columns in the results:

- **business_name**: The original business name from your CSV
- **URL**: The URL that was processed
- **scraped_content**: The content retrieved from the URL (truncated for display)
- **website_working**: TRUE if content was successfully scraped, FALSE if there was an error
- **result**: VALID if content matches the business, INVALID if it doesn't match

### Processing Summary

The application shows:
- **Total URLs**: Number of URLs processed
- **Valid Associations**: URLs where content matches the business
- **Invalid Associations**: URLs where content doesn't match the business
- **Errors**: URLs that couldn't be processed
- **Processing Time**: Start time, end time, and total duration

## Configuration

### API Keys

You need two API keys:

1. **Exa.AI API Key**: For content retrieval from URLs
   - Sign up at [Exa.AI](https://exa.ai)
   - Get your API key from the dashboard

2. **OpenRouter API Key**: For AI classification
   - Sign up at [OpenRouter](https://openrouter.ai)
   - Get your API key from the dashboard

### Environment Variables

Set these in your `.env` file:
```env
EXA_API_KEY=your_exa_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Troubleshooting

### Common Issues

**❌ Missing API Keys**
- **Problem**: "Missing API keys" error
- **Solution**: Ensure both `EXA_API_KEY` and `OPENROUTER_API_KEY` are set in your `.env` file

**❌ CSV Upload Errors**
- **Problem**: "Error loading CSV" message
- **Solution**: Ensure your CSV has exactly two columns: `business_name` and `URL`

**❌ Content Retrieval Errors**
- **Problem**: `website_working` shows FALSE
- **Solution**: Check if the URL is accessible and not blocked by robots.txt

**❌ Classification Errors**
- **Problem**: `result` shows ERROR
- **Solution**: Check your OpenRouter API key and internet connection

### Debug Information

The application includes a debug section that shows:
- API key status
- Processing details for each URL
- Content retrieval results
- Classification attempts and results

To access debug information:
1. Click the "🔧 Debug Information" expander
2. Review the processing details
3. Check for specific error messages

## FAQ

**Q: How many URLs can I process at once?**
A: The application can handle hundreds of URLs, but processing time increases with larger datasets. For best performance, process 50-100 URLs at a time.

**Q: How accurate is the classification?**
A: The classification uses GPT OSS 120B, which provides high accuracy but may not be perfect in all cases. Review results manually for critical applications.

**Q: What if a website is down or inaccessible?**
A: The application will mark `website_working` as FALSE and skip classification for that URL.

**Q: Can I customize the classification criteria?**
A: Currently, the classification uses a fixed prompt. Future versions may allow customization.

**Q: How long does processing take?**
A: Processing time depends on the number of URLs and website response times. Typically 1-5 seconds per URL.

**Q: What if my CSV has different column names?**
A: The application requires exactly `business_name` and `URL` columns. Rename your columns to match.

## Technical Details

### Architecture

- **Frontend**: Streamlit web interface
- **Content Retrieval**: Exa.AI API for web scraping
- **AI Classification**: OpenRouter API with GPT OSS 120B model
- **Data Processing**: Pandas for CSV handling
- **Error Handling**: Comprehensive error catching and logging

### Batch Processing

The application uses optimized batch processing:
- **Content Retrieval**: Processes URLs in batches of 10 for efficiency
- **AI Classification**: Processes one URL at a time for accuracy
- **Progress Tracking**: Real-time progress updates
- **Error Recovery**: Continues processing even if some URLs fail

### Rate Limiting

The application includes built-in rate limiting:
- **Exa.AI**: 0.5 second delay between batches
- **OpenRouter**: Individual requests with timeout handling
- **Error Retries**: Automatic retry for failed requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the debug information in the application