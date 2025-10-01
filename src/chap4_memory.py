from src.core.llm import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful document assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

from src.memory.session import SessionManager
from langchain_core.runnables import RunnableWithMessageHistory

manager = SessionManager(memory_type="file", token_limit=500)

conversation = RunnableWithMessageHistory(
    chain,
    lambda session_id: manager.create_session(session_id),
    input_messages_key="input",
    history_messages_key="history"
)

config = {"configurable": {"session_id": "alice"}}

response = conversation.invoke({"input": "Hello, my name is Alice."}, config=config)
print("IA:", response.content)

response = conversation.invoke({"input": "I am studying medicine."}, config=config)
print("IA:", response.content)

text = """
1. Origins and Milestones
The journey of AI from Alan Turing’s theoretical musings to today’s deep learning revolution is indeed remarkable. The "AI winters" you mentioned highlight how progress often hinges on technological breakthroughs—like the advent of GPUs, big data, and advanced algorithms. The current era of AI is defined by its ability to learn from vast datasets, but it’s also shaped by the interdisciplinary collaboration between computer science, neuroscience, and cognitive psychology.

2. Ubiquitous Applications
AI’s integration into daily life—healthcare, finance, entertainment, and beyond—is a testament to its versatility. However, its "invisibility" raises important questions about transparency and user awareness. For example, while AI-driven recommendations enhance convenience, they also create filter bubbles, limiting exposure to diverse perspectives. The challenge lies in balancing efficiency with ethical design, ensuring users understand how AI influences their choices.

3. Undeniable Benefits
AI’s potential to automate repetitive tasks and augment human capabilities is transformative. In fields like drug discovery or climate modeling, AI acts as a force multiplier, accelerating progress. Yet, as you noted, its benefits are unevenly distributed. The digital divide and access to AI tools could exacerbate global inequalities, making it crucial to democratize AI education and resources.

4. Ethical and Social Challenges
The ethical dilemmas you highlighted—job displacement, algorithmic bias, and surveillance—are among the most pressing issues today. For instance:

Bias: AI systems trained on biased data can perpetuate discrimination, as seen in hiring tools or facial recognition software. Addressing this requires diverse training datasets and ongoing audits of AI systems.
Privacy: The use of AI in surveillance, especially in authoritarian regimes, poses risks to civil liberties. Striking a balance between security and privacy is a global challenge.
Accountability: Who is responsible when an AI system makes a harmful decision? Legal frameworks are still catching up to the complexities of AI governance.


5. The Myth of Neutrality
AI is not neutral; it reflects the values and biases of its creators and the data it’s trained on. This underscores the need for ethical AI design, where interdisciplinary teams—including ethicists, sociologists, and policymakers—collaborate to mitigate harm. Initiatives like the EU’s AI Act and guidelines from organizations like the Partnership on AI are steps toward responsible AI development.

6. Human-Machine Cohabitation
The future of AI lies in augmentation, not replacement. AI can handle data-heavy tasks, but human creativity, empathy, and moral reasoning remain irreplaceable. For example, in healthcare, AI can assist in diagnostics, but the final decision—and the compassionate care—rests with human practitioners. The goal should be to design AI systems that empower, rather than diminish, human agency.

7. Conclusion: Promise and Vigilance
AI is a double-edged sword: it holds immense potential for progress but also risks if left unchecked. The key is proactive governance—shaping AI’s development through inclusive policies, public dialogue, and international cooperation. As you aptly put it, AI is a mirror of our humanity, reflecting our aspirations and flaws. The choices we make today will define whether AI becomes a tool for collective good or a source of division.
""" 

response = conversation.invoke({"input": text}, config=config)
print("IA:", response.content)

response = conversation.invoke({"input": "What is my name and my occupation ?"}, config=config)
print("IA:", response.content)

print("\n=== Alice's history ===")
print(manager.read_session("alice"))