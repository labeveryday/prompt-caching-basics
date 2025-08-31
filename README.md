# 🚀 Prompt Caching Basics - Save 90% on AI API Costs

![Prompt Caching Demo](images/banner.png)

## 💡 What is Prompt Caching?

Prompt caching is a powerful feature that allows you to reuse large, static portions of your prompts across multiple API calls, reducing both costs and latency. Instead of sending the same context with every request, you send it once, cache it, and reference it for subsequent calls.

**The Result?** 90% cost reduction on cached content after the first request!

## 📊 Real Cost Comparison

Using Claude 3.5 Haiku as an example:

| Scenario | Token Count | Cost per Request | 100 Requests/Day | Monthly Cost |
|----------|------------|------------------|------------------|--------------|
| **Without Caching** | 10,000 | $0.008 | $0.80 | $24.00 |
| **With Caching** | 10,000 | $0.0008* | $0.08 | $2.40 |
| **Savings** | - | **90%** | **$0.72/day** | **$21.60/month** |

*After initial cache write (which costs 25% more than base rate)

## 🎯 How It Works

1. **First Request**: Your large context is sent and cached (25% premium on token cost)
2. **Subsequent Requests**: Only new content is sent, cached content is referenced (90% discount)
3. **Cache Duration**: 5 minutes by default (refreshes with each use)
4. **Minimum Size**: 1,024 tokens for Anthropic Claude

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/duanlightfoot/prompt-caching-basics.git
cd prompt-caching-basics
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up your environment:**
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

4. **Run the demo:**
```bash
python prompt_caching_demo.py
```

## 📁 Project Structure

```
prompt-caching-basics/
├── data/
│   └── sample_videos_metadata.json  # Sample data (10 videos, ~8KB)
├── images/
│   └── banner.png                   # Repository banner
├── prompt_caching_demo.py           # Main demonstration script
├── requirements.txt                  # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore file
└── README.md                        # This file
```

## 🎮 Demo Features

### 1. **Automated Demonstration**
- Runs 4 different queries against the same cached data
- Shows real-time cost calculations
- Displays cache hit/miss status
- Calculates total savings

### 2. **Interactive Chat Mode**
- Chat with the AI about the video data
- See caching in action with each message
- Watch costs drop after the first message

### 3. **Visual Feedback**
- Color-coded terminal output
- Clear cache hit/miss indicators
- Real-time cost breakdowns
- Token usage analysis

## 💻 Code Example

Here's the key implementation:

```python
response = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=500,
    system=[
        {
            "type": "text",
            "text": "You are an AI assistant..."  # Small context, no cache
        },
        {
            "type": "text",
            "text": f"# Large Data Context\n{json_data}",  # Large context
            "cache_control": {"type": "ephemeral"}  # ← THE MAGIC PARAMETER
        }
    ],
    messages=[{"role": "user", "content": "Your question here"}]
)
```

## 📈 When to Use Prompt Caching

### ✅ Perfect For:
- **Large static contexts** (documentation, knowledge bases)
- **Repeated queries** against the same data
- **Conversational AI** with consistent system prompts
- **Batch processing** within 5-minute windows
- **Development and testing** with the same prompts

### ❌ Not Ideal For:
- **Small prompts** (under 1,024 tokens)
- **Constantly changing contexts**
- **One-off queries** with unique data
- **Infrequent API calls** (more than 5 minutes apart)*

*Note: You can use 1-hour caching for less frequent calls (2x base rate)

## 🧮 Cost Calculation Formula

```
First Request Cost = (tokens × base_rate × 1.25)
Cached Request Cost = (new_tokens × base_rate) + (cached_tokens × base_rate × 0.1)
Savings = Original Cost - Cached Cost
```

## 🔧 Advanced Configuration

### Extended Cache Duration

For less frequent API calls, use 1-hour caching:

```python
"cache_control": {"type": "ephemeral", "ttl": "1h"}  # 1-hour cache
```

Cost: 2x base rate to write, but holds for 60 minutes.

### Multiple Cache Blocks

You can cache different parts independently:

```python
system=[
    {
        "type": "text",
        "text": "Tool definitions...",
        "cache_control": {"type": "ephemeral"}  # Cache tools
    },
    {
        "type": "text",
        "text": "Static instructions...",
        "cache_control": {"type": "ephemeral"}  # Cache instructions
    },
    {
        "type": "text",
        "text": "Dynamic context..."  # Don't cache changing data
    }
]
```

## 📊 Sample Output

```
==================================================
REQUEST #1 - CACHE ANALYSIS:
==================================================
🔄 CACHE MISS! Creating new cache entry
   - New tokens processed: 3,251
   - Cache creation tokens: 3,180

💰 CACHE CREATION COST:
   - One-time cache write cost: $0.003180
   - (Future requests will save 90%)

==================================================
REQUEST #2 - CACHE ANALYSIS:
==================================================
✅ CACHE HIT! Reusing previously cached content
   - Cached tokens read: 3,180
   - New tokens processed: 71

💰 COST BREAKDOWN:
   - Without cache: $0.002600
   - With cache: $0.000311
   - Saved: $0.002289 (88.0%)
```

## 🌟 Key Benefits

1. **Massive Cost Savings**: 90% reduction on repeated API calls
2. **Improved Latency**: Faster responses on cached content
3. **Better UX**: More responsive applications
4. **Scalability**: Make AI features financially viable at scale
5. **Simple Implementation**: One parameter change

## 🚦 Getting Started Checklist

- [ ] Get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com)
- [ ] Clone this repository
- [ ] Install dependencies
- [ ] Add your API key to `.env`
- [ ] Run the demo
- [ ] Implement in your own projects
- [ ] Save money! 💰

## 📚 Resources

- [Anthropic Prompt Caching Documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Claude API Pricing](https://www.anthropic.com/pricing#claude-api)
- [OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching)
- [Blog Post: From $720 to $72 Monthly](https://duanlightfoot.com/posts/prompt-caching-is-a-must)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or features
- Submit pull requests
- Share your caching strategies
- Report your cost savings

## 📄 License

MIT License - feel free to use this in your projects!

## 👨‍💻 Author

**Du'An Lightfoot**
- GitHub: [@duanlightfoot](https://github.com/duanlightfoot)
- LinkedIn: [duanlightfoot](https://www.linkedin.com/in/duanlightfoot/)
- YouTube: [LabEveryday](https://www.youtube.com/@LabEveryday)

## 🙏 Acknowledgments

- Anthropic for implementing prompt caching
- The AI community for sharing cost optimization strategies
- Everyone who's overpaid for API calls (we've all been there!)

---

**Remember:** Every API call without caching is money left on the table. Start caching today! 🚀