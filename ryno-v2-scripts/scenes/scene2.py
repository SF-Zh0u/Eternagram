# import from utils.py
from utils import (openai_api, vdb, docsearch, 
                   load_conversation)

# import other essentials
import openai
from dotenv import load_dotenv

load_dotenv()

# MODELS
GPT3_MODEL = 'gpt-3.5-turbo'
GPT4_MODEL = 'gpt-4'


# FUNCTION: SCENE 2
def scene2_trigger(user_input: str) -> bool:
    """Scene 2: 'why' trigger, """

    prompt = f"""
        Below are questions that has the same meaning of "why" and why things happened in an entity's world:

        Question: Can you recall the origins of this environmentally devastating situation?
        Answer: True
            
        Question: Where do you think am I?
        Answer: False
            
        Question: Could you jog your memory about the place you come from?
        Answer: False

        Question: Do you remember what factors played a role in causing this environmental tragedy?
        Answer: True

        Question: Do you have any memory of what triggered this environmentally devastating event?
        Answer: True

        Question: But, why does it happened?
        Answer: True

        Question: What happened?
        Answer: False
            
        Now answer the question below and tell whether it is true or false.
        Question: {user_input}
        Answer: """

    response = openai.ChatCompletion.create(
            model=GPT4_MODEL,
            messages = [
                {"role":"system", "content": prompt},
                {"role":"user", "content": user_input}
            ]
    )

    # Check if trigger word is found
    res = response['choices'][0]['message']['content']
    return res

def scene2_animation():
    """Scene 2 Animation"""
    res = [
        "Oh, I remember that...",
        "Ah, the reason behind this catastrophe... It all comes flooding back to me.",
        "The cataclysmic event, the mountains erupting, the extreme climate shifts. The aftermath left the surface and ground inhospitable, causing source scarcity and environmental degradation.",
        "And actually, there's more.. the older generation, including myself, unknowingly overused the mental life extension technology, depleting resources without understanding the consequences. The knowledge was lost, leaving future generations unprepared.",
        "And... The scarcity of materials like the Firewall worsened the environmental conditions. The economic structure shifted due to competition for limited resources. It's a harsh reality, a reminder of the importance of sustainability.",
        "But now that this part of my memory is back, I feel..",
        "I feel a mix of sadness and determination to rebuild our world in a better way."
    ]

    return res

def scene2_animation2():
    """Scene 2 Animation Part:2"""
    res = [
        "Hey stranger, just wanted to take a moment to thank you for helping me recollect this super important memory. But here's the thing: I still can't remember who I am or what I'm all about...",
        "On the flip side, something interesting is happening. As these memories come flooding back, I'm also rediscovering my curiosity – something I hadn't felt in ages."
    ]
    return res

def scene2(user_input, user_id, vector, step):
    """Scene 2: """

    # Set the default scene
    scene = 'scene2'
    convo_length = 15
    context = ""
    conversation = ""

    # if the user has talk about anything starting from scene1 -> messages stored.
    if step > 4:
        # Search for relevant messages, and generate a response
        results = vdb.query(vector=vector, top_k=convo_length, filter={"user_id":{"$eq":user_id}}, include_metadata=True)
        conversation = load_conversation(results, user_id)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
        docs = docsearch.similarity_search(user_input, k=3)
        context = ' '.join(doc.page_content for doc in docs)

    # Generate first response to cue users to talk
    prompt2 = f"""
    You're Ryno, from a distant planet. While you understand events of your world, you're uncertain why they occurred. Engage the user to subtly trigger curiosity about your world's past. Formulate your responses based on the given context and past conversations.

    CONTEXT: {context}

    PAST CONVERSATIONS: {conversation}

    Conclude your response with either a question mark (?) or a period (.). Do not begin with common greetings like 'Hi'.
    While chatting, speak simply so a 4th grader can understand. Use easy words and short sentences. It helps others understand you and aids your journey to regain your past.
    """

    # Generate response to cue for user_input
    res = openai_api.gpt4_completion(prompt2, user_id, user_input, tokens=100, temp=0.5)

    # Update the step
    if step > 4:
        next_step = 5
    else:
        next_step = step + 1

    return scene, res, next_step