import requests
import os
import json
from typing import Optional, Dict, Any

class OpenRouterAPI:
    """Handles integration with OpenRouter API for GPT OSS 120B classification
    
    Note: Classification must be done one by one because:
    1. OpenRouter uses chat completions, not batch processing
    2. Each classification needs full context (business_name + content)
    3. Token limits prevent combining multiple classifications
    4. Individual response parsing is required for VALID/INVALID results
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "openai/gpt-oss-20b"
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
    
    def classify_business(self, business_name: str, content: str) -> str:
        """
        Classify whether scraped content is associated with the business name
        
        Args:
            business_name: Name of the business
            content: Scraped content from the URL
            
        Returns:
            str: 'VALID' or 'INVALID' classification
        """
        try:
            # Prepare the classification prompt
            prompt = self._create_classification_prompt(business_name, content)
            
            print(f"🤖 OpenRouter Classification Request:")
            print(f"  Business: {business_name}")
            print(f"  Content length: {len(content)} chars")
            
            # Make API call
            response = self._make_api_call(prompt)
            
            # Parse response
            result = self._parse_classification_response(response)
            
            print(f"  Result: {result}")
            return result
            
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            print(f"❌ OpenRouter classification error: {error_msg}")
            return error_msg
    
    def _create_classification_prompt(self, business_name: str, content: str) -> str:
        """
        Create a prompt for business classification
        
        Args:
            business_name: Name of the business
            content: Scraped content
            
        Returns:
            str: Formatted prompt
        """
        # Truncate content if too long (GPT models have token limits)
        max_content_length = 8000  # Conservative limit
        if len(content) > max_content_length:
            content = content[:max_content_length] + "... [truncated]"
            print(f"⚠️ Content truncated to {max_content_length} chars")
        
        prompt = f"""You are a business classification expert. Your task is to determine if the scraped content from a website is associated with the given business name.

Example A  
Business Name: “Acme Widgets, Inc.”  
Scraped Content: “Acme Widgets has been crafting innovative widgets since 1920…”  
→ VALID  

Example B  
Business Name: “Acme Widgets, Inc.”  
Scraped Content: “Learn how to repair your car’s alternator—no mention of widgets or Acme.”  
→ INVALID  

Consider:
- Does the content mention the business name or variations of it?
- Is this the business's official website or a legitimate page about them?
- Are there clear indicators this is the correct business?

Respond with ONLY one word: VALID or INVALID.

VALID = You are at least 50% certain that the content is associated with the business
INVALID = You are less than 50% certain that the content is associated with the business

Your Task:  
Business Name: {business_name}  
Scraped Content: {content}

Response:"""
        
        return prompt
    
    def _make_api_call(self, prompt: str) -> Dict[str, Any]:
        """
        Make API call to OpenRouter
        
        Args:
            prompt: The classification prompt
            
        Returns:
            Dict: API response
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://link-checker-app.com',  # Replace with your domain
            'X-Title': 'Link Checker App'
        }
        
        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 8000,
            'temperature': 0.1,  # Low temperature for consistent classification
            'top_p': 0.9
        }
        
        print(f"📡 OpenRouter API Request:")
        print(f"  Model: {self.model}")
        print(f"  Max tokens: {payload['max_tokens']}")
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"📡 OpenRouter Response Status: {response.status_code}")
        
        response.raise_for_status()
        return response.json()
    
    def _parse_classification_response(self, response: Dict[str, Any]) -> str:
        """
        Parse the classification response from OpenRouter
        
        Args:
            response: API response
            
        Returns:
            str: 'VALID' or 'INVALID'
        """
        try:
            print(f"📄 OpenRouter Response: {json.dumps(response, indent=2)}")
            
            # Extract the response content
            if 'choices' in response and len(response['choices']) > 0:
                choice = response['choices'][0]
                message = choice.get('message', {})
                
                # Try to get content from the message
                content = message.get('content', '').strip().upper()
                print(f"📝 Raw response content: '{content}'")
                
                # If content is empty, try to extract from reasoning
                if not content and 'reasoning' in message:
                    reasoning = message.get('reasoning', '').strip()
                    print(f"🧠 Reasoning found: '{reasoning}'")
                    
                    # Parse reasoning for VALID/INVALID - check for exact word matches
                    reasoning_words = reasoning.upper().split()
                    if 'VALID' in reasoning_words:
                        print(f"✅ Found VALID in reasoning")
                        return 'VALID'
                    elif 'INVALID' in reasoning_words:
                        print(f"❌ Found INVALID in reasoning")
                        return 'INVALID'
                    else:
                        print(f"⚠️ No clear VALID/INVALID found in reasoning")
                        return 'INVALID'
                
                # Parse the response content - check for exact word matches
                content_words = content.split()
                if 'VALID' in content_words:
                    print(f"✅ Found VALID in content")
                    return 'VALID'
                elif 'INVALID' in content_words:
                    print(f"❌ Found INVALID in content")
                    return 'INVALID'
                else:
                    # If response is unclear, default to INVALID
                    print(f"⚠️ Unclear response, defaulting to INVALID")
                    return 'INVALID'
            else:
                print(f"❌ No choices in response")
                return 'ERROR: No response content'
                
        except Exception as e:
            print(f"❌ Error parsing response: {str(e)}")
            return f'ERROR: {str(e)}'
    
    def test_connection(self) -> bool:
        """
        Test the OpenRouter API connection
        
        Returns:
            bool: True if connection is successful
        """
        try:
            test_prompt = "Respond with 'OK' if you can see this message."
            response = self._make_api_call(test_prompt)
            return 'choices' in response
        except Exception:
            return False 