How Your Gemini Chatbot Works
Your project is a Memory-Augmented Chatbot. While often called a RAG (Retrieval-Augmented Generation) system, it specifically focuses on Conversational Retrieval.

 Step-by-Step Breakdown
1. The Request (FastAPI)
When you send a message via Postman or a frontend, it hits the /chat endpoint. It expects a message and an optional session_id.

2. Conversation Retrieval (Upstash Redis)
Instead of the model "forgetting" who you are after every message, the HistoryService queries Upstash Redis using your session_id.

If this is a new chat, it starts fresh.
If you've talked before, it pulls the last few messages (context).
3. Context Construction
The ChatbotService assembles a "Prompt" that looks like this:

System Message: Your predefined personality/rules (from config.py).
History: "User: My name is Lokesh. AI: Hello Lokesh!"
Current Message: "What is my name?"
4. The Intelligence (Gemini 3.1)
The entire context is sent to the Gemini 3.1 model. Because it sees the history, it "knows" what you've said before.

5. Persistent Memory
Before sending the response back to you, the service saves the new interaction into Redis. This ensures the next time you ask something, it still remembers.

🔄 Model Update
I have updated the system to use Gemini 3.1 as requested.

Configuration: The model name is now centralized in src/core/config.py.
Flexibility: You can now change the model easily by updating the GEMINI_MODEL environment variable or changing the default in config.py.
🛠️ Why this is powerful
Stateless Backend: Your server doesn't store anything. If your server restarts, the memory is safe in Redis.
Infinite Context: By using a dedicated database, you can handle thousands of concurrent users with unique memories.
Industry Standard: This modular approach (separating API, Services, and Core) is how production-grade AI applications are built.
