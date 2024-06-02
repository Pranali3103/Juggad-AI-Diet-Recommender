import os
import uuid
from flask import Flask, render_template, request
from julep import Client

app = Flask(__name__)

# Set up Julep client
os.environ['JULEP_API_URL'] = 'https://api-alpha.julep.ai/api'
os.environ['JULEP_API_KEY'] = 'YOUR_API_KEY'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    # Set up Julep client
    base_url = os.environ.get("JULEP_API_URL")
    api_key = os.environ.get("JULEP_API_KEY")
    client = Client(api_key=api_key, base_url=base_url)

    # Create an agent for comprehensive recommendations
    agent = client.agents.create(
        name="Comprehensive Recommendations Agent",
        about="This agent provides recommendations for restaurants, breakfast, dinner, and workouts based on specified criteria.",
        instructions=[
            "Recommend a restaurant name based on specified criteria.",
            "Recommend a breakfast name based on specified criteria.",
            "Recommend a dinner name based on specified criteria.",
            "Recommend a workout name based on specified criteria.",
            "Recommend another workout name based on specified criteria."
        ],
        model="gpt-4-turbo",
        default_settings={
            "temperature": 0.7,
            "top_p": 1,
            "min_p": 0.01,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "length_penalty": 1.0,
        },
        metadata={"db_uuid": "1234"}
    )

    # Generate UUID v4 for user_id
    user_id = str(uuid.uuid4())

    # Create a session for the user and agent interaction
    session = client.sessions.create(
        agent_id=agent.id,
        user_id=user_id,
        situation="You are providing recommendations for restaurants, breakfast, dinner, and workouts based on specified criteria."
    )

    # Retrieve form data
    age = request.form['age']
    gender = request.form['gender']
    weight = request.form['weight']
    height = request.form['height']
    veg_or_nonveg = request.form['veg_or_nonveg']
    disease = request.form['disease']
    region = request.form['region']
    allergics = request.form['allergics']
    foodtype = request.form['foodtype']

    # Format user input message
    user_message = (
        f"I am {age} years old, {gender}, my weight is {weight} and my height is {height}. "
        f"I prefer {veg_or_nonveg} food. I have {disease} and no allergies. "
        f"I live in {region}. I prefer a {foodtype} diet."
    )

    # Send message to Julep API for each recommendation
    recommendations = []
    for instruction in agent.instructions:
        res = client.sessions.chat(
            session_id=session.id,
            messages=[{"content": user_message, "role": "user", "agent_id": agent.id}],
            recall=True,
            remember=True
        )
        recommendation = res.response[0][0].content
        recommendations.append(recommendation)

    # Render recommendations template
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
