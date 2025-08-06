# Link Checker User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Using the Application](#using-the-application)
3. [Understanding Results](#understanding-results)
4. [Troubleshooting Guide](#troubleshooting-guide)
5. [Advanced Features](#advanced-features)

## Getting Started

### Prerequisites
Before using the Link Checker application, ensure you have:
- Python 3.8 or higher installed
- Access to the internet
- API keys for Exa.AI and OpenRouter

### Installation Steps

1. **Download the Application**
   ```bash
   git clone https://github.com/yourusername/link-checker.git
   cd link-checker
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Keys**
   Create a `.env` file in the project directory:
   ```env
   EXA_API_KEY=your_exa_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

4. **Start the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the Web Interface**
   Open your browser and navigate to `http://localhost:8501`

### Getting API Keys

#### Exa.AI API Key
1. Visit [Exa.AI](https://exa.ai)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key
5. Add it to your `.env` file

#### OpenRouter API Key
1. Visit [OpenRouter](https://openrouter.ai)
2. Sign up for a free account
3. Navigate to your API keys section
4. Copy your API key
5. Add it to your `.env` file

## Using the Application

### Step 1: Prepare Your Data

Create a CSV file with the following structure:
```csv
business_name,URL
Apple Inc,https://www.apple.com
Tesla Inc,https://www.tesla.com
Google LLC,https://www.google.com
```

**Important Notes:**
- Column names must be exactly `business_name` and `URL`
- URLs must include the protocol (http:// or https://)
- Avoid empty cells in your data

### Step 2: Upload Your File

1. **Open the Application**
   - Launch the application in your browser
   - You should see the main interface

2. **Upload CSV File**
   - Click "Browse files" or drag and drop your CSV file
   - The application will validate your file format
   - You'll see a preview of your data

3. **Review the Preview**
   - Check that your data looks correct
   - Verify column names and data format
   - Ensure URLs are properly formatted

### Step 3: Process Your URLs

1. **Start Processing**
   - Click the "🚀 Process URLs" button
   - The application will begin processing your URLs

2. **Monitor Progress**
   - Watch the progress bar for overall completion
   - Check the status text for current activity
   - Expand the debug section for detailed information

3. **Wait for Completion**
   - Processing time depends on the number of URLs
   - Typically 1-5 seconds per URL
   - The application will show completion when done

### Step 4: Review Results

1. **View Results Table**
   - Results are displayed in a table format
   - Each row shows one URL and its classification
   - Use the scroll to see all results

2. **Check Summary Statistics**
   - Total URLs processed
   - Number of valid associations
   - Number of invalid associations
   - Number of errors
   - Processing time information

3. **Download Results**
   - Click "📥 Download Results CSV" to save your results
   - The file will include all processed data

## Understanding Results

### Result Columns

| Column | Description | Possible Values |
|--------|-------------|-----------------|
| `business_name` | Original business name from your CSV | Text |
| `URL` | The URL that was processed | URL |
| `scraped_content` | Content retrieved from the URL | Text (truncated) |
| `website_working` | Whether content was successfully retrieved | TRUE/FALSE |
| `result` | AI classification result | VALID/INVALID/ERROR |

### Understanding Classifications

#### VALID
- The AI determined that the scraped content is associated with the business
- Content mentions the business name or related information
- High confidence in the association

#### INVALID
- The AI determined that the scraped content is NOT associated with the business
- Content doesn't mention the business or is unrelated
- Low confidence in the association

#### ERROR
- The AI classification failed
- Usually due to API issues or network problems
- Check your API keys and internet connection

### Understanding Website Status

#### TRUE (Website Working)
- Content was successfully retrieved from the URL
- The website is accessible and responsive
- AI classification was attempted

#### FALSE (Website Not Working)
- Content retrieval failed
- Website may be down, blocked, or inaccessible
- No AI classification was performed

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: "Missing API keys" Error
**Symptoms:**
- Application shows error message about missing API keys
- Debug section shows ❌ Missing for API keys

**Solutions:**
1. Check that your `.env` file exists in the project root
2. Verify API keys are correctly formatted:
   ```env
   EXA_API_KEY=your_key_here
   OPENROUTER_API_KEY=your_key_here
   ```
3. Restart the application after adding keys
4. Check that keys are valid and have sufficient credits

#### Issue: CSV Upload Errors
**Symptoms:**
- "Error loading CSV" message
- File upload fails

**Solutions:**
1. Ensure your CSV has exactly two columns: `business_name` and `URL`
2. Check that column names match exactly (case-sensitive)
3. Verify CSV format is correct (comma-separated)
4. Remove any empty rows or cells
5. Ensure URLs include protocol (http:// or https://)

#### Issue: Content Retrieval Failures
**Symptoms:**
- `website_working` shows FALSE for many URLs
- Debug section shows content retrieval errors

**Solutions:**
1. Check if URLs are accessible in your browser
2. Some websites block automated access
3. Verify URLs are correctly formatted
4. Check if websites require authentication
5. Some URLs may be temporarily down

#### Issue: Classification Errors
**Symptoms:**
- `result` shows ERROR for many URLs
- Debug section shows classification failures

**Solutions:**
1. Check your OpenRouter API key is valid
2. Verify you have sufficient API credits
3. Check your internet connection
4. Some URLs may have insufficient content for classification
5. Try processing fewer URLs at once

#### Issue: Slow Processing
**Symptoms:**
- Processing takes much longer than expected
- Progress bar moves slowly

**Solutions:**
1. Check your internet connection speed
2. Some websites may be slow to respond
3. Large datasets take longer to process
4. Consider processing in smaller batches
5. Check if API rate limits are being hit

### Debug Information

The application includes comprehensive debug information:

1. **API Key Status**
   - Shows whether API keys are properly configured
   - Indicates if keys are missing or invalid

2. **Processing Debug**
   - Shows each URL being processed
   - Displays content retrieval results
   - Shows classification attempts and results

3. **Processing Summary**
   - Total URLs processed
   - Number of content retrieval errors
   - Number of LLM classifications performed

To access debug information:
1. Click the "🔧 Debug Information" expander
2. Review the processing details
3. Check for specific error messages

## Advanced Features

### Batch Processing
The application uses optimized batch processing:
- **Content Retrieval**: Processes URLs in batches of 10
- **AI Classification**: Processes one URL at a time for accuracy
- **Error Recovery**: Continues processing even if some URLs fail

### Rate Limiting
Built-in rate limiting prevents API overload:
- **Exa.AI**: 0.5 second delay between batches
- **OpenRouter**: Individual requests with timeout handling
- **Error Retries**: Automatic retry for failed requests

### Progress Tracking
Real-time progress monitoring:
- **Progress Bar**: Shows overall completion percentage
- **Status Text**: Shows current activity
- **Debug Information**: Detailed processing logs

### Error Handling
Comprehensive error handling:
- **Graceful Degradation**: Continues processing despite individual failures
- **Detailed Error Messages**: Specific information about what went wrong
- **Error Recovery**: Automatic retry for transient failures

## Best Practices

### Data Preparation
1. **Clean Your Data**
   - Remove duplicate entries
   - Ensure URLs are properly formatted
   - Check for typos in business names

2. **Test with Small Datasets**
   - Start with 5-10 URLs to test the process
   - Verify results before processing large datasets
   - Check that your API keys work correctly

3. **Monitor API Usage**
   - Keep track of your API credits
   - Exa.AI and OpenRouter have usage limits
   - Plan processing accordingly

### Processing Strategy
1. **Batch Size**
   - Process 50-100 URLs at a time for best performance
   - Larger batches may hit rate limits
   - Smaller batches are more reliable

2. **Error Handling**
   - Review results for ERROR classifications
   - Re-process failed URLs if needed
   - Check debug information for specific issues

3. **Result Validation**
   - Manually review a sample of results
   - Verify classifications make sense
   - Use results as a starting point, not final answer

## Support and Resources

### Getting Help
1. **Check This Manual**: Review the troubleshooting section
2. **Debug Information**: Use the built-in debug tools
3. **API Documentation**: 
   - [Exa.AI Documentation](https://docs.exa.ai)
   - [OpenRouter Documentation](https://openrouter.ai/docs)
4. **GitHub Issues**: Report bugs or request features

### Additional Resources
- **API Key Management**: Learn how to manage your API keys
- **CSV Format Guide**: Detailed CSV formatting requirements
- **Performance Tips**: Optimize processing speed and accuracy
- **Security Best Practices**: Keep your API keys secure

---

*This user manual covers the essential features and common issues. For technical details, refer to the main README.md file.* 