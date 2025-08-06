# Link Checker Quick Reference

## 🚀 Quick Start

1. **Install**: `pip install -r requirements.txt`
2. **Configure**: Create `.env` with API keys
3. **Run**: `streamlit run app.py`
4. **Access**: `http://localhost:8501`

## 📋 CSV Format

```csv
business_name,URL
Apple Inc,https://www.apple.com
Tesla Inc,https://www.tesla.com
```

**Requirements:**
- Column names: `business_name`, `URL`
- URLs must include `http://` or `https://`
- No empty cells

## 🔑 API Keys

**Required in `.env` file:**
```env
EXA_API_KEY=your_exa_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

**Get API Keys:**
- Exa.AI: [exa.ai](https://exa.ai)
- OpenRouter: [openrouter.ai](https://openrouter.ai)

## 📊 Results Columns

| Column | Description | Values |
|--------|-------------|--------|
| `business_name` | Original business name | Text |
| `URL` | Processed URL | URL |
| `scraped_content` | Retrieved content | Text |
| `website_working` | Content retrieval success | TRUE/FALSE |
| `result` | AI classification | VALID/INVALID/ERROR |

## ⚡ Processing Time

- **Small batch (10 URLs)**: ~30-60 seconds
- **Medium batch (50 URLs)**: ~3-5 minutes
- **Large batch (100 URLs)**: ~6-10 minutes

## 🔧 Common Issues

### Missing API Keys
```bash
# Check .env file exists and has correct format
EXA_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
```

### CSV Upload Errors
- Ensure column names are exactly `business_name` and `URL`
- Check URLs include protocol (http:// or https://)
- Remove empty rows/cells

### Processing Errors
- Check internet connection
- Verify API keys have sufficient credits
- Some websites block automated access

## 📈 Performance Tips

1. **Batch Size**: Process 50-100 URLs at once
2. **Data Quality**: Clean URLs and business names
3. **API Credits**: Monitor usage to avoid limits
4. **Network**: Use stable internet connection

## 🆘 Debug Information

Access debug info by clicking "🔧 Debug Information" expander:
- API key status
- Processing details
- Error messages
- Performance metrics

## 📞 Support

- **Documentation**: Check README.md and docs/
- **Debug Info**: Use built-in debug tools
- **API Docs**: [Exa.AI](https://docs.exa.ai), [OpenRouter](https://openrouter.ai/docs)
- **Issues**: Report on GitHub

---

*For detailed information, see the full User Manual and README.md* 