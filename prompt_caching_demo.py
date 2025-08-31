"""
Prompt Caching Demo - Anthropic Claude API
This script demonstrates how to use prompt caching to reduce API costs by 90%
Author: Du'An Lightfoot
"""

import os
import json
from dotenv import load_dotenv
import anthropic
from datetime import datetime
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print a nice header for the demo"""
    print("\n" + "="*60)
    print(f"{Colors.BOLD}{Colors.CYAN}🚀 PROMPT CACHING DEMONSTRATION{Colors.END}")
    print(f"{Colors.CYAN}Reduce your AI API costs by 90%!{Colors.END}")
    print("="*60 + "\n")

def load_sample_data() -> Dict[str, Any]:
    """Load sample video metadata from JSON file"""
    with open("data/sample_videos_metadata.json", "r") as f:
        return json.load(f)

def calculate_token_cost(tokens: int, rate_per_million: float) -> float:
    """Calculate cost based on token count and rate"""
    return (tokens / 1_000_000) * rate_per_million

def print_cache_analysis(response, request_number: int):
    """Analyze and display cache usage information with cost calculations"""
    usage = response.usage
    
    print(f"\n{Colors.BOLD}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}REQUEST #{request_number} - CACHE ANALYSIS:{Colors.END}")
    print(f"{'='*50}")
    
    # Determine cache hit or miss
    if hasattr(usage, 'cache_read_input_tokens') and usage.cache_read_input_tokens > 0:
        print(f"{Colors.GREEN}✅ CACHE HIT! Reusing previously cached content{Colors.END}")
        print(f"   - Cached tokens read: {Colors.GREEN}{usage.cache_read_input_tokens:,}{Colors.END}")
        print(f"   - New tokens processed: {usage.input_tokens:,}")
        print(f"   - Total input tokens: {usage.input_tokens + usage.cache_read_input_tokens:,}")
        
        # Calculate cost savings (using Claude 3.5 Haiku rates)
        base_rate = 0.80  # $0.80 per million tokens
        cache_read_rate = 0.08  # $0.08 per million tokens (10% of base)
        
        cost_without_cache = calculate_token_cost(
            usage.input_tokens + usage.cache_read_input_tokens, base_rate
        )
        cost_with_cache = (
            calculate_token_cost(usage.input_tokens, base_rate) +
            calculate_token_cost(usage.cache_read_input_tokens, cache_read_rate)
        )
        
        savings = cost_without_cache - cost_with_cache
        savings_percent = (savings / cost_without_cache) * 100
        
        print(f"\n{Colors.YELLOW}💰 COST BREAKDOWN:{Colors.END}")
        print(f"   - Without cache: ${cost_without_cache:.6f}")
        print(f"   - With cache: ${cost_with_cache:.6f}")
        print(f"   - {Colors.GREEN}Saved: ${savings:.6f} ({savings_percent:.1f}%){Colors.END}")
        
    else:
        print(f"{Colors.YELLOW}🔄 CACHE MISS! Creating new cache entry{Colors.END}")
        print(f"   - New tokens processed: {usage.input_tokens:,}")
        
        if hasattr(usage, 'cache_creation_input_tokens') and usage.cache_creation_input_tokens > 0:
            print(f"   - Cache creation tokens: {Colors.YELLOW}{usage.cache_creation_input_tokens:,}{Colors.END}")
            
            # Calculate cache creation cost (25% premium)
            base_rate = 0.80
            cache_write_rate = 1.00  # $1.00 per million tokens (125% of base)
            
            creation_cost = calculate_token_cost(usage.cache_creation_input_tokens, cache_write_rate)
            print(f"\n{Colors.YELLOW}💰 CACHE CREATION COST:{Colors.END}")
            print(f"   - One-time cache write cost: ${creation_cost:.6f}")
            print(f"   - {Colors.CYAN}(Future requests will save 90%){Colors.END}")
    
    print(f"   - Output tokens: {usage.output_tokens:,}")
    print(f"{'='*50}\n")

def demonstrate_caching():
    """Main demonstration of prompt caching"""
    print_header()
    
    # Initialize client
    print(f"{Colors.BLUE}Initializing Anthropic client...{Colors.END}")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Load sample data
    print(f"{Colors.BLUE}Loading sample video metadata...{Colors.END}")
    video_metadata = load_sample_data()
    metadata_json = json.dumps(video_metadata, indent=2)
    
    print(f"Loaded {len(video_metadata)} sample videos")
    print(f"Total metadata size: {len(metadata_json):,} characters\n")
    
    # Test prompts to demonstrate caching
    test_prompts = [
        "What are the main topics covered in these videos?",
        "Which video has the most views?",
        "List all videos about Python programming.",
        "What's the average duration of these videos?"
    ]
    
    print(f"{Colors.BOLD}Running {len(test_prompts)} test prompts to demonstrate caching...{Colors.END}\n")
    
    total_saved = 0
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"{Colors.CYAN}Prompt {i}: '{prompt}'{Colors.END}")
        
        try:
            # Create request with caching
            response = client.messages.create(
                model=MODEL,
                max_tokens=500,
                system=[
                    {
                        "type": "text",
                        "text": "You are an AI assistant analyzing YouTube video metadata. "
                               "Provide concise, helpful responses based on the video data provided."
                    },
                    {
                        "type": "text",
                        "text": f"# Video Metadata Repository\n{metadata_json}",
                        "cache_control": {"type": "ephemeral"}  # Enable caching here!
                    }
                ],
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Display response
            print(f"\n{Colors.BOLD}Response:{Colors.END}")
            print(response.content[0].text[:200] + "..." if len(response.content[0].text) > 200 
                  else response.content[0].text)
            
            # Analyze cache performance
            print_cache_analysis(response, i)
            
            # Track savings
            if hasattr(response.usage, 'cache_read_input_tokens') and response.usage.cache_read_input_tokens > 0:
                base_cost = calculate_token_cost(
                    response.usage.cache_read_input_tokens, 0.80
                )
                cache_cost = calculate_token_cost(
                    response.usage.cache_read_input_tokens, 0.08
                )
                total_saved += (base_cost - cache_cost)
            
            # Small delay between requests
            if i < len(test_prompts):
                print(f"{Colors.CYAN}Continuing to next request...{Colors.END}\n")
        
        except Exception as e:
            print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
    
    # Final summary
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}DEMONSTRATION COMPLETE!{Colors.END}")
    print(f"{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"\n{Colors.BOLD}Summary:{Colors.END}")
    print(f"  - Requests made: {len(test_prompts)}")
    print(f"  - Total saved from caching: ${total_saved:.6f}")
    print(f"  - Cache window: 5 minutes (ephemeral)")
    print(f"\n{Colors.CYAN}💡 Key Takeaway:{Colors.END}")
    print(f"After the first request, all subsequent requests within 5 minutes")
    print(f"save 90% on the cached content tokens!")
    print(f"\n{Colors.YELLOW}⚡ Imagine the savings on production workloads!{Colors.END}\n")

def interactive_mode():
    """Interactive chat mode with caching enabled"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}INTERACTIVE MODE{Colors.END}")
    print("Chat with the AI about the video data. Type 'exit' to quit.")
    print("Watch how caching reduces costs with each message!\n")
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    video_metadata = load_sample_data()
    metadata_json = json.dumps(video_metadata, indent=2)
    
    conversation_history = []
    request_count = 0
    
    while True:
        user_input = input(f"{Colors.CYAN}You: {Colors.END}").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print(f"{Colors.GREEN}Thanks for trying the demo! 👋{Colors.END}")
            break
        
        if not user_input:
            continue
        
        request_count += 1
        
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=[
                    {
                        "type": "text",
                        "text": "You are an AI assistant analyzing YouTube video metadata. "
                               "Be conversational and helpful."
                    },
                    {
                        "type": "text",
                        "text": f"# Video Metadata Repository\n{metadata_json}",
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                messages=conversation_history + [{"role": "user", "content": user_input}]
            )
            
            ai_response = response.content[0].text
            print(f"\n{Colors.GREEN}AI: {ai_response}{Colors.END}")
            
            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Keep history manageable
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]
            
            # Show cache analysis
            print_cache_analysis(response, request_count)
            
        except Exception as e:
            print(f"{Colors.RED}Error: {str(e)}{Colors.END}")

def main():
    """Main entry point"""
    print_header()
    
    if not ANTHROPIC_API_KEY:
        print(f"{Colors.RED}❌ ERROR: ANTHROPIC_API_KEY not found in environment variables!{Colors.END}")
        print(f"\nPlease create a .env file with your API key:")
        print(f"  ANTHROPIC_API_KEY=your_api_key_here")
        print(f"  ANTHROPIC_MODEL=claude-3-5-haiku-20241022")
        return
    
    print(f"{Colors.BOLD}Choose a demo mode:{Colors.END}")
    print("1. Automated demonstration (recommended for first time)")
    print("2. Interactive chat mode")
    print("3. Exit")
    
    choice = input(f"\n{Colors.CYAN}Enter your choice (1-3): {Colors.END}").strip()
    
    if choice == "1":
        demonstrate_caching()
    elif choice == "2":
        interactive_mode()
    elif choice == "3":
        print(f"{Colors.GREEN}Goodbye! 👋{Colors.END}")
    else:
        print(f"{Colors.RED}Invalid choice. Please run the script again.{Colors.END}")

if __name__ == "__main__":
    main()