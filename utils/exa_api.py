import requests
import os
import time
from typing import Optional, Dict, Any, List
import json

class ExaAPI:
    """Handles integration with Exa.AI content retrieval API with batch processing"""
    
    def __init__(self):
        self.api_key = os.getenv('EXA_API_KEY')
        self.base_url = "https://api.exa.ai"
        self.endpoint = "/contents"
        self.batch_size = 10  # Process 10 URLs at a time
        
        if not self.api_key:
            raise ValueError("EXA_API_KEY environment variable is required")
    
    def get_content_batch(self, urls: List[str]) -> Dict[str, str]:
        """
        Retrieve content from multiple URLs in a single batch request
        
        Args:
            urls: List of URLs to retrieve content from (max 10 per batch)
            
        Returns:
            Dict[str, str]: URL to content mapping
        """
        if not urls:
            return {}
        
        try:
            # Prepare request
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'ids': urls,
                'text': True,
                'livecrawl': 'always'
            }
            
            print(f"🔍 Exa.AI Batch Request:")
            print(f"  URLs: {urls}")
            print(f"  Payload: {json.dumps(payload, indent=2)}")
            
            # Make API call
            response = requests.post(
                f"{self.base_url}{self.endpoint}",
                headers=headers,
                json=payload,
                timeout=60  # Increased timeout for batch requests
            )
            
            print(f"📡 Exa.AI Response Status: {response.status_code}")
            
            # Check response
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            print(f"📄 Exa.AI Response Data: {json.dumps(data, indent=2)}")
            
            # Extract results - FIXED: results are at top level, not under 'data'
            results = {}
            
            # Handle successful results
            if 'results' in data:
                for result in data['results']:
                    url = result.get('id', '')
                    text = result.get('text', 'No content available')
                    results[url] = text
                    print(f"✅ Content retrieved for {url}: {len(text)} chars")
            
            # Handle errors from statuses
            if 'statuses' in data:
                for status in data['statuses']:
                    url = status.get('id', '')
                    if status.get('status') == 'error':
                        error_msg = f"Error: {status.get('error', {}).get('tag', 'Unknown error')}"
                        if url not in results:  # Only add if not already processed
                            results[url] = error_msg
                            print(f"❌ Error for {url}: {error_msg}")
            
            # Handle URLs that weren't in results or statuses (shouldn't happen but just in case)
            for url in urls:
                if url not in results:
                    results[url] = "Error: URL not found in response"
                    print(f"⚠️ URL not found in response: {url}")
            
            return results
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Exa.AI API error: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def process_urls_in_batches(self, urls: List[str]) -> Dict[str, str]:
        """
        Process URLs in batches of 10
        
        Args:
            urls: List of all URLs to process
            
        Returns:
            Dict[str, str]: URL to content mapping for all URLs
        """
        all_results = {}
        
        print(f"🚀 Processing {len(urls)} URLs in batches of {self.batch_size}")
        
        # Process URLs in batches
        for i in range(0, len(urls), self.batch_size):
            batch = urls[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (len(urls) + self.batch_size - 1) // self.batch_size
            
            print(f"📦 Processing batch {batch_num}/{total_batches}: {batch}")
            
            try:
                batch_results = self.get_content_batch(batch)
                all_results.update(batch_results)
                
                print(f"✅ Batch {batch_num} completed: {len(batch_results)} results")
                
                # Small delay between batches to respect rate limits
                if i + self.batch_size < len(urls):
                    print("⏳ Waiting 0.5s before next batch...")
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"❌ Batch {batch_num} failed: {str(e)}")
                # If batch fails, mark all URLs in batch as failed
                for url in batch:
                    all_results[url] = f"Batch error: {str(e)}"
        
        print(f"🎉 All batches completed. Total results: {len(all_results)}")
        return all_results
    
    def get_content(self, url: str) -> str:
        """
        Retrieve content from a single URL (for backward compatibility)
        
        Args:
            url: URL to retrieve content from
            
        Returns:
            str: Retrieved content text
        """
        results = self.get_content_batch([url])
        return results.get(url, 'No content available')
    
    def validate_url(self, url: str) -> bool:
        """
        Basic URL validation
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if URL is valid
        """
        if not url or not isinstance(url, str):
            return False
        
        url = url.strip()
        return url.startswith(('http://', 'https://'))
    
    def get_batch_status(self, urls: List[str]) -> Dict[str, Any]:
        """
        Get processing status for a batch of URLs
        
        Args:
            urls: List of URLs to check
            
        Returns:
            Dict: Processing status information
        """
        try:
            results = self.get_content_batch(urls)
            
            status = {
                'total_urls': len(urls),
                'successful': len([r for r in results.values() if not r.startswith('Error')]),
                'failed': len([r for r in results.values() if r.startswith('Error')]),
                'results': results
            }
            
            return status
            
        except Exception as e:
            return {
                'total_urls': len(urls),
                'successful': 0,
                'failed': len(urls),
                'error': str(e),
                'results': {url: f"Batch error: {str(e)}" for url in urls}
            } 