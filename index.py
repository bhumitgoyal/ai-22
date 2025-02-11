from flask import Flask, request, jsonify, session
import firebase_admin

from firebase_admin import credentials, firestore
import os
from flask_cors import CORS
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, AIMessage, HumanMessage

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import base64
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

import traceback
import random
import firebase_admin
from firebase_admin import credentials
import os
import json

openai_api_key = os.getenv("OPENAI_API_KEY")


firebase_creds ={
  "type": "service_account",
  "project_id": "ai-render-38beb",
  "private_key_id": "34ba8eb17424d076eef7b3ef7356fe46791ed32f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDA1kt839GoTLwQ\n3tjEOIBD75h8TQfTwnBv6jnKH1a2oUjb2D8UU4Zesbmq4HHSxkjhuty/sjnrEJ+q\noDwaRJIJXTg8kKgJ9uhhQEKi2r6HU8lm9+gcItomkGK0bDKpEg4z8Jr1m+FpMDCq\nLkhgwtEedQQn5c6yz0E8AjOF2J5WQ29elw08GkgDL9SrtZZMPy5h8apuiDhFX8sn\nVWrSOy8O6k8E0U8z/6oYZS/zVqH+1svQPc5bxeLrN92JhEi0sdRUPMgdvUul2RHE\nPp1X9/6/5FmW8DeJZ4rcHk+5Rqnlez1UTp6m+qLsmMOjJKNbGzX1B2IymVEtUVdC\nr9OC1O83AgMBAAECggEAAj3bex73nHRmkURN58YHs60i1tBnFrlBaQOjhVZ6Qb2R\nOmutRrVhL/5H5r/HgvLmy6efmPjflHxz0V4dz2kG+5CNA/iN2NkjwrxQ/1H5+gUU\nJ8bE+M1s6hrZPY4DxBRffDoVSw/zUwTfjp2Nc4Eq63w3vqZSEfZieenv+GPYFK+c\ndmONEHlFZFBTi1+Ks6w4nSlMrgpqEOIZ5j6EN+ujTVKhLg5rTG/quAuh7KufuoZC\n6+CjbjnwrFlFp8OcbR0N18oawa5QHuhQtmOoQ/CmhIm3IETUzDgCQL4Hv3Yhteb6\n5gYc95iOJ1obpPrDeBySdgiow+62pBcqCwmRuuqO6QKBgQD44DeiBeLX7EtAT3/G\nASywvPZOqPU3k7ZufJhEII+8a/ZYtxhJrNOTiUFt+zwa3+6PCn5h0y04mg1UMGWB\n12g9fmFc7z15Ava1WIHi1IriKXDt5pX2/p9JQcGFrYQIVBWu7QH9Q5kYmrA7nq/B\n5b9Ao9SX81Z/eKs5YpYWlFhZzwKBgQDGW2vBc5j8+FpLUXv2h1wY7jW2nCea1Rzc\noojMfaITfzBHZIojUKmnyx1+xegZ3FH+Vf9HR4/LUbBGk+RpUPHmTauEysleS5fy\nHDKRURsUAvd7YCrZa22mN05X2qDNWkeMYtCjRzPslZY0bZv9VcIkt9DK1RUJxtws\nQcq8mbW2GQKBgQD0KcVqx6uNet048sXAVFar7jcXZNtu8xP/wW0BKZDaonDFCJxj\na5MHI5l1dQ26sAczfnAPOUccSMba2cA8akByVBLhQjVlC2tO7s4+45Z923pXa+mk\nsJlFHaXmqBzortW3D/7roe4JHXnYhA6ag/PmTtS7Xph15sTVP8tPy6oCMQKBgQCs\nHoAuaUSDnm2blaVfkq1T5MAvKOkk7XAR8+eIqiuNh3w5NwC3DDNrKlD5xHlWl1t+\nuti83VflMYkodQRqbpa5JQSEQgLiE+5RZC5s8lfw0XI2WIhWCWYoKS2OBmQqTQBw\nzP4F8K8Zx+OCsun8tgG1ItvGZYfP6AL9VEm7xhVrYQKBgQDN28mQI9PvoDf03jx1\nq1LAbEPTNsn0lZTfTcJBS758oFaixUJjX5Hg1bAHfWo3dC8/ra9vbRD239GHtuu6\nEpcc2y3+eNAiGxnkl8TVidoaZZ6qx6edT/34yuy6IzMHI66U/1td4X+mCgd8BTi1\n+2B+qpVpyIaEGWFUUCAZkfETZA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@ai-render-38beb.iam.gserviceaccount.com",
  "client_id": "114644966291203884168",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40ai-render-38beb.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Initialize 
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)

# Initialize Firestore




# Initialize Firestore Client
client = firebase_admin.firestore.client()


chat_model2 = ChatOpenAI(
    model="gpt-4o",
    temperature=0.85,  # Slightly higher for more creative responses
    max_tokens=150,
    frequency_penalty=0.5  # Reduce repetition,
    
)

# Initialize OpenAI GPT-4o model via LangChain
chat_model = ChatOpenAI(model="gpt-4o", temperature=0.7)


llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)


# Define Chat History Collection Name
COLLECTION_NAME = "journal_chat_history"

app = Flask(__name__)
app = Flask(__name__)

# Configure Flask session
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a secure value
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in files
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.secret_key="secret"
CORS(app)

### Route to Store Journal Entry ###
@app.route("/store_journal", methods=["POST"])
def store_journal():
    """Stores a journal entry for a user in Firestore using LangChain's FirestoreChatMessageHistory."""
    print("🔹 Received request at /store_journal")  # Debugging print

    try:
        data = request.get_json()
        print(f"Data received: {data}")  # Debugging print
        
        user_id = data.get("user_id")
        text = data.get("text")

        if not user_id or not text:
            print("Missing user_id or text in request!")
            return jsonify({"error": "Missing user_id or text"}), 400

        # Initialize Firestore Chat History for the user
        chat_history = FirestoreChatMessageHistory(
            session_id=user_id,
            collection=COLLECTION_NAME,
            client=client,
        )

        # Store the journal entry as a user message
        chat_history.add_user_message(text)

        print("Journal entry stored successfully!")
        return jsonify({"message": "Journal stored successfully!"}), 200

    except Exception as e:
        print(f" Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/analyze_journal", methods=["POST"])
def analyze_journal():
    """Analyzes journal entries to extract mental health metrics and burnout indicators."""
    print("Received request at /analyze_journal")

    try:
        data = request.get_json()
        print(f"Data received: {data}")
        
        user_id = data.get("user_id")

        if not user_id:
            print("Missing user_id in request!")
            return jsonify({"error": "Missing user_id"}), 400

        # Retrieve chat history from Firestore
        chat_history = FirestoreChatMessageHistory(
            session_id=user_id,
            collection=COLLECTION_NAME,
            client=client,
        )

        # Decode and collect journal entries
        journal_texts = []
        for msg in chat_history.messages:
            if msg.type == "human":
                content = msg.content
                if isinstance(content, bytes):
                    content = content.decode("utf-8")
                journal_texts.append(content)

        if not journal_texts:
            print("No journal entries found!")
            return jsonify({"error": "No journal entries found"}), 404

        journal_text = "\n".join(journal_texts)
        print("Journal data extracted, running metrics analysis...")

        metrics_prompt = ChatPromptTemplate.from_template(
        """Analyze the following journal entries and return specific numerical metrics and categorical assessments. Return the data in this exact JSON format:
        {{
            "emotional_metrics": {{
                "sentiment_score": <float -1 to 1>,
                "emotional_volatility": <float 0 to 1>,
                "primary_emotions": {{
                    "joy": <float 0 to 1>,
                    "sadness": <float 0 to 1>,
                    "anger": <float 0 to 1>,
                    "fear": <float 0 to 1>,
                    "surprise": <float 0 to 1>
                }},
                "emotional_trends": {{
                    "last_7_days": <float -1 to 1>,
                    "last_30_days": <float -1 to 1>
                }}
            }},
            "cognitive_metrics": {{
                "cognitive_distortions": {{
                    "catastrophizing": <float 0 to 1>,
                    "black_white_thinking": <float 0 to 1>,
                    "overgeneralization": <float 0 to 1>
                }},
                "resilience_score": <float 0 to 1>,
                "problem_solving_confidence": <float 0 to 1>
            }},
            "burnout_metrics": {{
                "overall_burnout_risk": <float 0 to 1>,
                "components": {{
                    "emotional_exhaustion": <float 0 to 1>,
                    "depersonalization": <float 0 to 1>,
                    "accomplishment_satisfaction": <float 0 to 1>
                }},
                "energy_levels": {{
                    "physical": <float 0 to 1>,
                    "mental": <float 0 to 1>,
                    "emotional": <float 0 to 1>
                }}
            }},
            "risk_flags": {{
                "immediate_attention_needed": <boolean>,
                "areas_of_concern": [<string>],
                "positive_indicators": [<string>]
            }},
            "temporal_analysis": {{
                "past_focus": <float 0 to 1>,
                "present_focus": <float 0 to 1>,
                "future_focus": <float 0 to 1>,
                "growth_trajectory": <float -1 to 1>
            }}
        }}

        Journal entries to analyze: {journal}
        
        Guidelines:
        - All numerical scores should be normalized between their specified ranges
        - Sentiment scores range from -1 (negative) to 1 (positive)
        - Risk scores and component scores range from 0 (low) to 1 (high)
        - Include specific areas of concern when risk scores exceed 0.7
        - Base temporal analysis on verb tense usage and time-related references
        - Calculate emotional volatility based on emotional state changes
        - Ensure growth trajectory reflects overall trend in emotional and cognitive metrics
        """
        )

        # Run metrics analysis
        metrics_chain = metrics_prompt | llm | JsonOutputParser()
        analysis_results = metrics_chain.invoke({"journal": journal_text})

        print("Metrics analysis completed, storing results...")

        # Store results in Firestore
        chat_history.add_ai_message(f"Metrics Analysis: {json.dumps(analysis_results)}")

        print("Analysis results successfully stored in Firestore!")

        return jsonify(analysis_results), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500



# Dummy mentor data
mentors = {
    "Mental & Emotional Health Challenges": [
        {"name": "Dr. Sophia Matthews", "contact": "+1-555-1010"},
        {"name": "Ms. Rachel Green", "contact": "+1-555-2020"}
    ],
    "Workplace-Related Stress": [
        {"name": "Mr. Daniel Johnson", "contact": "+1-555-3030"},
        {"name": "Ms. Olivia White", "contact": "+1-555-4040"}
    ],
    "Relationship & Social Pressures": [
        {"name": "Dr. Emily Davis", "contact": "+1-555-5050"},
        {"name": "Mr. Kevin Brooks", "contact": "+1-555-6060"}
    ],
    "Health & Reproductive Challenges": [
        {"name": "Dr. Amanda Lewis", "contact": "+1-555-7070"},
        {"name": "Ms. Laura Mitchell", "contact": "+1-555-8080"}
    ],
    "Safety & Security Issues": [
        {"name": "Mr. Henry Adams", "contact": "+1-555-9090"},
        {"name": "Ms. Julia Carter", "contact": "+1-555-1111"}
    ],
    "Financial & Career Concerns": [
        {"name": "Dr. Robert Williams", "contact": "+1-555-2222"},
        {"name": "Ms. Sarah Thompson", "contact": "+1-555-3333"}
    ],
    "Others": [
        {"name": "Mr. Thomas Brown", "contact": "+1-555-4444"},
        {"name": "Dr. Linda Baker", "contact": "+1-555-5555"}
    ]
}


def message_to_dict(msg):
    "convert langchain msgs to dictionary format"
    return {"type":type(msg).name,"content":msg.content}

def dict_to_message(msg_dict):
    "converts dict to langchain msgs"
    
    content = msg_dict["content"]
    type = msg_dict["type"]
    if(type=="SystemMessage"):
        return SystemMessage(content=content)
    elif(type=="AIMessage"):
        return AIMessage(content=content)
    elif(type=="HumanMessage"):
        return HumanMessage(content=content)
    return None
@app.route('/start_mentor', methods=['POST'])
def start_session():
    data = request.get_json()
    user_id = data["user_id"]

    scenario_history = FirestoreChatMessageHistory(session_id=user_id, collection="Mentor", client=client)

    content = """You are an AI mentor assistant. Ask up to 4 questions to understand the user's concern. 
    Categorize it into one of the following:
    - Mental & Emotional Health Challenges
    - Workplace-Related Stress
    - Relationship & Social Pressures
    - Health & Reproductive Challenges
    - Safety & Security Issues
    - Financial & Career Concerns
    - Others

    Ask one question at a time and wait for a user response before proceeding. 
    Once 4 questions are asked, categorize the concern."""

    scenario_history.add_user_message(content)

    question_no_history = FirestoreChatMessageHistory(session_id=user_id, collection="question_no_history", client=client)
    question_no_history.add_user_message("0")

    category_no_history = FirestoreChatMessageHistory(session_id=user_id, collection="category_no_history", client=client)
    category_no_history.add_user_message("None")

    return jsonify({"message": "Session Started, Please use /ask to answer questions."})

@app.route('/ask_mentor', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_id = data["user_id"]

    scenario_history = FirestoreChatMessageHistory(session_id=user_id, collection="Mentor", client=client)
    messages = scenario_history.messages

    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Message cannot be empty"})

    messages.append(HumanMessage(content=user_input))

    # Fetch the question count history
    question_no_history = FirestoreChatMessageHistory(session_id=user_id, collection="question_no_history", client=client)
    question_countt = int(question_no_history.messages[-1].content) if question_no_history.messages else 0

    question_countt += 1
    question_no_history.add_user_message(str(question_countt))

    if question_countt < 4:
        ai_response = chat_model.invoke(messages)
        ai_text = ai_response.content

        scenario_history.add_ai_message(ai_text)
        return jsonify({
    "response": ai_text,
    "question_count": question_no_history.messages[-1].content if question_no_history.messages else "0"
})

    
    else:
        # AI determines the category
        categorization_prompt = SystemMessage(content="Based on the conversation so far, determine which category the user's problem falls into:\n"
                                                      "- Mental & Emotional Health Challenges\n"
                                                      "- Workplace-Related Stress\n"
                                                      "- Relationship & Social Pressures\n"
                                                      "- Health & Reproductive Challenges\n"
                                                      "- Safety & Security Issues\n"
                                                      "- Financial & Career Concerns\n"
                                                      "- Others\n"
                                                      "Respond with just the category name.")
        messages.append(categorization_prompt)
        category_response = chat_model.invoke(messages).content.strip()

        if category_response not in mentors:
            category_response = "Others"
        
        category_no_history = FirestoreChatMessageHistory(session_id=user_id, collection="category_no_history", client=client)
        category_no_history.add_user_message(category_response)

        mentor = random.choice(mentors[category_response])
        question_no_history.add_user_message("0")
        return jsonify({"Category": category_response, "Mentor": mentor})
        
         

SCENARIOS = {
    "Workplace Negotiation": {
        "description": "Practice salary negotiation techniques with a simulated manager",
        "competencies": ["Active listening", "Value proposition framing", "Anchor positioning"],
        "difficulty_levels": ["Junior", "Mid-level", "Executive"],
        "cultural_context": ["US Corporate", "EU Startup", "Asian Conglomerate"]
    },
    "Conflict Resolution": {
        "description": "Resolve team conflicts using principled negotiation strategies",
        "competencies": ["Emotional regulation", "Interest-based bargaining", "Solution brainstorming"],
        "difficulty_levels": ["Peer", "Cross-functional", "Client-facing"]
    }
}

CONVERSATION_HISTORY = []
MAX_TURNS = 8  # Increased for more substantive dialogues

@app.route('/select_scenario', methods=['POST'])
def select_scenario():
    """Handle scenario selection with enhanced validation and session setup"""
    data = request.get_json()
    
    if not data or "scenario_id" not in data or "difficulty" not in data:
        return jsonify({"error": "Missing required parameters: scenario_id and difficulty"}), 400
    
    scenario_id = data["scenario_id"]
    user_id= data["user_id"]
    difficulty = data["difficulty"]
    
    scenario_history = FirestoreChatMessageHistory(session_id=user_id,collection="Scenario",client=client)
    scenario_history.add_user_message(scenario_id)
    
    if scenario_id not in SCENARIOS:
        return jsonify({"error": "Invalid scenario ID"}), 400
    
    if difficulty not in SCENARIOS[scenario_id]["difficulty_levels"]:
        return jsonify({"error": "Invalid difficulty level"}), 400
    
    # Initialize session with metadata
    session.clear()
    session.update({
        "scenario": scenario_id,
        "difficulty": difficulty,
        "cultural_context": data.get("cultural_context", "Default"),
        "turn_count": 0,
        "performance_metrics": {
            "assertiveness": 0,
            "empathy": 0,
            "clarity": 0
        }
    })
    
    return jsonify({
        "scenario": SCENARIOS[scenario_id]["description"],
        "competencies": SCENARIOS[scenario_id]["competencies"],
        "instructions": "The simulation will begin with your first response"
    })

def generate_system_prompt(scenario):
    """Create detailed roleplay prompt using scenario metadata"""
    base_template = f"""
    Role: Expert Communication Coach specializing in {scenario}
    
    Primary Objective:
    - Conduct realistic  roleplay simulation


    
    Interaction Guidelines:
    1. Start with an authentic opening statement reflecting scenario context
    2. Gradually escalate complexity based on user's performance
    3. Introduce realistic objections/conflicts at turn 3 and 5
    4. Mirror user's communication style (formal/casual) with 80% fidelity
    5. Provide subtle non-verbal cues through descriptive actions
    
    Adaptation Protocol:
    - If user struggles: Offer Socratic questioning
    - If user excels: Introduce advanced negotiation tactics
    - Track emotional valence and adjust pressure accordingly
    
    Feedback Framework:
    - Flag missed opportunities in real-time through probing questions
    - Maintain 70/30 practice/guidance ratio during simulation
    """
    return base_template.strip()

@app.route('/start_scene', methods=['POST'])
def start_prog():
    """Initialize conversation with sophisticated prompt engineering"""
    data = request.get_json()
    
    if not data or "scenario_id" not in data or "difficulty" not in data:
        return jsonify({"error": "Missing required parameters: scenario_id and difficulty"}), 400
    

    user_id= data["user_id"]

    
    scenario_history = FirestoreChatMessageHistory(session_id=user_id,collection="Scenario",client=client)
    scenarioo = scenario_history.messages
    if scenarioo:
        last_message = scenarioo[-1]

    
    system_prompt = generate_system_prompt(last_message)
    
    
    # Initialize conversation history with context
    CONVERSATION_HISTORY.clear()
    CONVERSATION_HISTORY.extend([
        SystemMessage(content=system_prompt),
        AIMessage(content="Simulation Start\nProvide your first response to begin the roleplay:")
    ])
    
    return jsonify({
        "status": "ready",
        "first_prompt": "Enter your opening statement to begin the simulation",
        "scenario":last_message.content
    })

def generate_feedback():
    """Create structured performance assessment using conversation history"""
    feedback_template = """
    Performance Evaluation Report
    
    Competency Development:
    {competency_analysis}
    
    Communication Patterns:
    - Strength Highlight: {top_strength}
    - Growth Opportunity: {main_improvement}
    
    Strategic Recommendations:
    1. {rec_1}
    2. {rec_2}
    3. {rec_3}
    
    Simulation Score: {score}/10
    """
    
    feedback_prompt = [
        SystemMessage(content="Analyze this roleplay conversation and generate structured feedback:"),
        HumanMessage(content="\n".join([msg.content for msg in CONVERSATION_HISTORY]))
    ]
    
    analysis = chat_model.invoke(feedback_prompt).content
    return analysis

@app.route('/chat_scene', methods=['POST'])
def chat():
    data = request.get_json()
    
    # if not data or "scenario_id" not in data or "difficulty" not in data:
    #     return jsonify({"error": "Missing required parameters: scenario_id and difficulty"}), 400
    

    user_id= data["user_id"]

    
    scenario_history = FirestoreChatMessageHistory(session_id=user_id,collection="Turn",client=client)
    scenarioo = scenario_history.messages
    last_turn = None
    if scenarioo:
        last_turn = scenarioo[-1]
        ll = last_turn.content
        turn = int(ll)
    else:
        turn = 0

    turn = turn+1
    scenario_history.add_user_message(str(turn))

    """Handle conversation turns with adaptive prompting"""
   
    
    data = request.get_json()
    user_input = data.get("message", "").strip()
    
    if not user_input:
        return jsonify({"error": "Empty message received"}), 400
    
    # Store user input with behavioral metadata
    CONVERSATION_HISTORY.append(HumanMessage(content=user_input))
    
    # Generate AI response with contextual adaptation
    ai_response = chat_model.invoke(CONVERSATION_HISTORY).content
    CONVERSATION_HISTORY.append(AIMessage(content=ai_response))
    
    
    
    if turn >= MAX_TURNS:
        feedback = generate_feedback()

        return jsonify({
            "type": "final_feedback",
            "content": feedback,
            "recommendations": ["Practice mirroring techniques", "Review anchoring strategies"]
        })
    
    return jsonify({
        "type": "response",
        "content": ai_response,
        "turn": turn,
        "remaining": MAX_TURNS - turn
    })
def decode_firestore_message(blob_data):
    """Decodes Firestore blob messages (Base64 encoded JSON)"""
    try:
        return json.loads(base64.b64decode(blob_data).decode("utf-8"))
    except Exception as e:
        print(f"[ERROR] Failed to decode Firestore message: {e}")
        return None

def get_journal_and_analysis_history(user_id):
    """Retrieve only AI analyses and user journal entries"""
    history = FirestoreChatMessageHistory(
        session_id=user_id,
        collection=COLLECTION_NAME,
        client=client
    )
    
    relevant_messages = []
    for msg in history.messages:
        content = msg.content
        if isinstance(content, bytes):
            content = content.decode("utf-8") 
            
        if msg.type == "human" or msg.type == "ai":
            relevant_messages.append(content) 
        
    return relevant_messages

def generate_personalized_prompt(user_id, current_message):
    """Create optimized prompts using proven engineering techniques"""
    history = get_journal_and_analysis_history(user_id)
    
    return SystemMessage(content=f"""
Role: Emotional Intelligence Analyst (CBT and Positive Psychology Certified)
Context: User {user_id}'s Journal History Analysis. History: {history}

Analysis Framework:
1. Emotional Continuity Check:
- Compare current message to {len(history)} previous entries
- Map emotional trajectory using Plutchik's Wheel
- Flag deviations from baseline sentiment

2. Cognitive Pattern Detection:
- Identify Beck's cognitive distortions in current message
- Cross-reference with previous journal patterns
- Calculate cognitive flexibility score

3. Narrative Analysis:
- Story arc classification (Growth/Stagnation/Regression)
- Agentic language density vs previous entries
- Temporal focus distribution (Past/Present/Future)

Response Protocol:
Insight Generation
- Connect to 1-2 specific historical entries (date/theme)
- Highlight emerging patterns using STAR method
- Provide psychometrically-validated feedback

Actionable Guidance:
- Suggest micro-interventions (<5 mins daily)
- Offer narrative reframing exercises
- Propose journal prompts for deeper exploration

Risk Mitigation:
- Monitor linguistic burnout markers
- Track self-compassion index trends
- Flag cognitive rigidity patterns

Output Format:
{base64.b64encode(json.dumps({
    "emotional_profile": ["emotion1", "emotion2", "emotion3"],
    "cognitive_biases": ["bias1", "confidence_score"],
    "narrative_arc": {"type": "growth/stagnation/regression", "confidence": 0.8},
    "recommended_actions": ["action1", "action2"]
}).encode()).decode()}

Tone Matrix:
- Primary: Compassionate yet analytical  
- Secondary: Curious collaborator  
- Tertiary: Strengths-based coach

Special Instructions:
1. Use Feynman Technique for complex concepts
2. Apply Socratic questioning for self-reflection
3. Maintain 65:35 insight-to-question ratio
4. Reference 2+ historical data points per response
5. You don't have access to dates of user entries. But you can reference to a previous entry and people mentioned in it.
6. You HAVE access to past entries of a user just not the dates. 
7. Don't overwhelm the user and talk like a friend when needed.
""")

@app.route('/chat', methods=['POST'])
def journal_based_chat():
    """Chatbot using only AI-generated insights & journal entries"""
    try:
        data = request.get_json()
        user_id = data['user_id']
        message = data['message']
        
        history = FirestoreChatMessageHistory(
            session_id=user_id,
            collection=COLLECTION_NAME,
            client=client
        )

        # Generate system prompt using only journal & AI analysis
        system_prompt = generate_personalized_prompt(user_id, message)

        # Build conversation history
        messages = [
            system_prompt,
            *get_journal_and_analysis_history(user_id)[-10:],  # Last 10 relevant entries
            HumanMessage(content=message)
        ]

        # Generate response
        response = llm.invoke(messages).content

        # Store interaction
        history.add_user_message(json.dumps({"role": "human", "content": message}))
        history.add_ai_message(json.dumps({"role": "ai", "content": response}))

        return jsonify({
            "response": response,
            "context_used": system_prompt.content[:500] + "..."
        })
    
    except Exception as e:
        print("[ERROR] Chat failed:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/plan-tasks", methods=["POST", "OPTIONS"])
def plan_tasks():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    try:
        data = request.json
        print("Received data:", data)
        
        user_id = data.get("user_id")
        tasks = data.get("tasks")
        
        if not user_id or not tasks:
            return jsonify({"error": "User ID and tasks are required."}), 400

        # Define the prompt template with properly escaped JSON formatting
        prompt_template = ChatPromptTemplate.from_template(
"""You are an AI assistant specializing in personalized productivity and well-being optimization.
Your goal is to analyze the user's past journal entries {journal_texts} to understand their emotional patterns, energy levels, stress triggers, and productivity cycles.
Based on this analysis, create an optimal schedule for the tasks {tasks} in a way that maximizes efficiency while preventing burnout.

Instructions:
- Identify the user's peak energy hours and low-energy periods from journal patterns.
- Detect any stress patterns, triggers, and relaxation methods the user naturally follows.
- Categorize tasks based on their cognitive load, emotional impact, and urgency.
- Suggest a balanced schedule that:
    - Assigns high-focus tasks to peak energy hours.
    - Places low-energy tasks during downtime.
    - Includes breaks and self-care recommendations based on stress patterns.
- Suggest best practices for completing the tasks effectively (e.g., deep work strategies, task batching, or mindful breaks).
- Format the output strictly as a JSON array where each task follows this structure:

Instructions:
1. Analyze each task
2. Create an optimized schedule with a rough timeline for each with the words "around X to Y", X and Y are times. it is manadatory to give a time range with X and Y since 
3. Return ONLY a JSON array string following this exact format IN DESCENDING ORDER OF PRIORITY.
[
    {{
        "title": "Task Title",
        "description": "Optimized task description with scheduling recommendation"
    }}
]"""
        )
        data = request.get_json()
        user_id = data['user_id']
        
        journal = FirestoreChatMessageHistory(
            session_id=user_id,
            collection=COLLECTION_NAME,
            client=client
        )

        # Create the chain
        chain = prompt_template | llm | JsonOutputParser()

        # Execute the chain
        
        response = chain.invoke({"journal_texts":journal,"tasks": json.dumps(tasks)})
        print("LLM Response:", response)
        return response
            # Try to parse the response as JSON
    #         try:
    #             parsed_response = json.loads(response)
    #             if isinstance(parsed_response, list):
    #                 # Add IDs to the tasks if they don't have them
    #                 for i, task in enumerate(parsed_response):
    #                     if 'id' not in task:
    #                         task['id'] = tasks[i].get('id', f"generated_{i}")
    #                 return jsonify({"optimized_schedule": parsed_response})
    #             else:
    #                 raise ValueError("Response is not a JSON array")

    #         except json.JSONDecodeError as e:
    #             print(f"JSON Parse Error: {e}")
    #             print(f"Raw Response: {response}")
    #             # Fallback response
    #             formatted_tasks = []
    #             for task in tasks:
    #                 formatted_tasks.append({
    #                     "id": task.get("id"),
    #                     "title": task.get("title"),
    #                     "description": f"{task.get('description')}"
    #                 })
    #             return jsonify({"optimized_schedule": formatted_tasks})

    #     except Exception as e:
    #         print(f"Chain Execution Error: {e}")
    #         return jsonify({"error": f"Error generating schedule: {str(e)}"}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT from environment, default to 5000
    app.run(host='0.0.0.0', port=port)
