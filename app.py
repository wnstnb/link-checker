import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from utils.csv_handler import CSVHandler
from utils.exa_api import ExaAPI
from utils.openrouter_api import OpenRouterAPI
import datetime

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="Link Checker",
        page_icon="🔗",
        layout="wide"
    )
    
    st.title("🔗 Link Checker Application")
    st.markdown("Upload a CSV file with business names and URLs to validate and classify them.")
    
    # Debug: Check API keys
    debug_section = st.expander("🔧 Debug Information", expanded=False)
    with debug_section:
        exa_key = os.getenv('EXA_API_KEY')
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
        st.write("**API Keys Status:**")
        st.write(f"Exa.AI Key: {'✅ Set' if exa_key else '❌ Missing'}")
        st.write(f"OpenRouter Key: {'✅ Set' if openrouter_key else '❌ Missing'}")
        
        if not exa_key or not openrouter_key:
            st.error("❌ Missing API keys! Please set EXA_API_KEY and OPENROUTER_API_KEY in your .env file")
            return
    
    # Initialize components
    csv_handler = CSVHandler()
    exa_api = ExaAPI()
    openrouter_api = OpenRouterAPI()
    
    # File upload section
    st.header("📁 Upload CSV File")
    uploaded_file = st.file_uploader(
        "Choose a CSV file with 'business_name' and 'URL' columns",
        type=['csv'],
        help="The CSV should have two columns: business_name and URL"
    )
    
    if uploaded_file is not None:
        try:
            # Process the uploaded file
            df = csv_handler.load_csv(uploaded_file)
            st.success(f"✅ Successfully loaded {len(df)} rows")
            
            # Display preview
            st.subheader("📊 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Process button
            if st.button("🚀 Process URLs", type="primary"):
                process_urls_optimized(df, exa_api, openrouter_api)
                
        except Exception as e:
            st.error(f"❌ Error loading CSV: {str(e)}")

def process_urls_optimized(df, exa_api, openrouter_api):
    """Process URLs with optimized batch content retrieval + individual classification"""
    st.header("🔄 Processing URLs")
    
    # Record start time
    start_time = datetime.datetime.now()
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Extract all URLs for batch processing
    urls = df['URL'].tolist()
    business_names = df['business_name'].tolist()
    
    # Debug: Show URLs being processed
    debug_section = st.expander("🔧 Processing Debug", expanded=False)
    with debug_section:
        st.write("**URLs to process:**")
        for i, (url, business) in enumerate(zip(urls, business_names)):
            st.write(f"{i+1}. {business} → {url}")
    
    # Phase 1: Batch content retrieval (Exa.AI)
    status_text.text("📡 Phase 1/2: Retrieving content from URLs in batches...")
    
    try:
        # Get content for all URLs in batches (10 at a time)
        content_results = exa_api.process_urls_in_batches(urls)
        
        # Debug: Show content retrieval results
        with debug_section:
            st.write("**Content Retrieval Results:**")
            for url, content in content_results.items():
                status = "✅ Success" if not content.startswith("Error") else "❌ Error"
                st.write(f"{url}: {status}")
                if content.startswith("Error"):
                    st.write(f"  Error: {content}")
        
        # Update progress to 50%
        progress_bar.progress(0.5)
        status_text.text("🤖 Phase 2/2: Classifying business associations (one by one)...")
        
        # Phase 2: Individual classification (OpenRouter) - SKIP if no content
        results = []
        skipped_count = 0
        processed_count = 0
        
        for idx, (url, business_name) in enumerate(zip(urls, business_names)):
            # Get content for this URL
            content = content_results.get(url, "Error: No content retrieved")
            
            # Debug: Show classification attempt
            with debug_section:
                st.write(f"**Processing {idx+1}/{len(urls)}: {business_name}**")
                st.write(f"URL: {url}")
                st.write(f"Content length: {len(content)} chars")
                if content.startswith("Error"):
                    st.write(f"Content error: {content}")
            
            # Check if content was successfully retrieved
            if content.startswith("Error"):
                # Skip LLM classification for failed content retrieval
                result = "ERROR"
                skipped_count += 1
                
                # Debug: Show skipped classification
                with debug_section:
                    st.write(f"⏭️ Skipping LLM classification - no content retrieved")
                    
            else:
                # Proceed with LLM classification only if content was retrieved
                try:
                    result = openrouter_api.classify_business(
                        business_name=business_name,
                        content=content
                    )
                    processed_count += 1
                    
                    # Debug: Show classification result
                    with debug_section:
                        st.write(f"Classification result: {result}")
                        
                except Exception as e:
                    error_msg = f"ERROR: Classification failed - {str(e)}"
                    result = error_msg
                    processed_count += 1
                    
                    # Debug: Show classification error
                    with debug_section:
                        st.write(f"Classification error: {error_msg}")
            
            results.append({
                'business_name': business_name,
                'URL': url,
                'scraped_content': content,
                'website_working': not content.startswith("Error"),
                'result': result
            })
            
            # Update progress (50% to 100%)
            progress_bar.progress(0.5 + (idx + 1) / len(urls) * 0.5)
            status_text.text(f"🤖 Processing {idx + 1}/{len(urls)}: {business_name}")
        
        # Show processing summary
        with debug_section:
            st.write(f"**Processing Summary:**")
            st.write(f"Total URLs: {len(urls)}")
            st.write(f"Content retrieval errors: {skipped_count}")
            st.write(f"LLM classifications performed: {processed_count}")
        
        # Record end time
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        
        # Display results
        display_results(results, start_time, end_time, duration)
        
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        progress_bar.progress(0)
        
        # Debug: Show full error
        with debug_section:
            st.write(f"**Full error details:**")
            st.write(str(e))

def process_urls_batch(df, exa_api, openrouter_api):
    """Process URLs in batches for better efficiency"""
    st.header("🔄 Processing URLs")
    
    # Record start time
    start_time = datetime.datetime.now()
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Extract all URLs for batch processing
    urls = df['URL'].tolist()
    business_names = df['business_name'].tolist()
    
    # Create URL to business name mapping
    url_to_business = dict(zip(urls, business_names))
    
    status_text.text("📡 Retrieving content from URLs in batches...")
    
    try:
        # Get content for all URLs in batches
        content_results = exa_api.process_urls_in_batches(urls)
        
        # Update progress
        progress_bar.progress(0.5)
        status_text.text("🤖 Classifying business associations...")
        
        # Process results and classify
        results = []
        for idx, (url, business_name) in enumerate(zip(urls, business_names)):
            # Get content for this URL
            content = content_results.get(url, "Error: No content retrieved")
            
            # Classify with OpenRouter only if content was retrieved
            if not content.startswith("Error"):
                result = openrouter_api.classify_business(
                    business_name=business_name,
                    content=content
                )
            else:
                result = "ERROR"
            
            results.append({
                'business_name': business_name,
                'URL': url,
                'scraped_content': content,
                'website_working': not content.startswith("Error"),
                'result': result
            })
            
            # Update progress
            progress_bar.progress(0.5 + (idx + 1) / len(urls) * 0.5)
        
        # Record end time
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        
        # Display results
        display_results(results, start_time, end_time, duration)
        
    except Exception as e:
        st.error(f"❌ Error during batch processing: {str(e)}")
        progress_bar.progress(0)

def process_urls(df, exa_api, openrouter_api):
    """Legacy single URL processing (kept for reference)"""
    st.header("🔄 Processing URLs")
    
    # Record start time
    start_time = datetime.datetime.now()
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Process each row
    results = []
    for idx, row in df.iterrows():
        status_text.text(f"Processing {idx + 1}/{len(df)}: {row['business_name']}")
        
        try:
            # Get content from Exa.AI
            content = exa_api.get_content(row['URL'])
            
            # Classify with OpenRouter only if content was retrieved
            if not content.startswith("Error"):
                result = openrouter_api.classify_business(
                    business_name=row['business_name'],
                    content=content
                )
            else:
                result = "ERROR"
            
            results.append({
                'business_name': row['business_name'],
                'URL': row['URL'],
                'scraped_content': content,
                'website_working': not content.startswith("Error"),
                'result': result
            })
            
        except Exception as e:
            st.warning(f"Error processing {row['business_name']}: {str(e)}")
            results.append({
                'business_name': row['business_name'],
                'URL': row['URL'],
                'scraped_content': f"Error: {str(e)}",
                'website_working': False,
                'result': 'ERROR'
            })
        
        # Update progress
        progress_bar.progress((idx + 1) / len(df))
    
    # Record end time
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    
    # Display results
    display_results(results, start_time, end_time, duration)

def display_results(results, start_time, end_time, duration):
    """Display processing results"""
    st.header("📈 Results")
    
    if results:
        df_results = pd.DataFrame(results)
        
        # Reorder columns to match requested order
        column_order = ['business_name', 'URL', 'scraped_content', 'website_working', 'result']
        df_results = df_results[column_order]
        
        # Display results table
        st.dataframe(df_results, use_container_width=True)
        
        # Download button
        csv = df_results.to_csv(index=False)
        st.download_button(
            label="📥 Download Results CSV",
            data=csv,
            file_name="link_checker_results.csv",
            mime="text/csv"
        )
        
        # Summary statistics
        st.subheader("📊 Summary")
        
        # Timing information
        st.write("**⏱️ Processing Time:**")
        st.write(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"Duration: {duration}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total URLs", len(results))
        
        with col2:
            valid_count = len([r for r in results if r['result'] == 'VALID'])
            st.metric("Valid Associations", valid_count)
        
        with col3:
            invalid_count = len([r for r in results if r['result'] == 'INVALID'])
            st.metric("Invalid Associations", invalid_count)
        
        with col4:
            error_count = len([r for r in results if r['result'] == 'ERROR'])
            st.metric("Errors", error_count)

if __name__ == "__main__":
    main() 