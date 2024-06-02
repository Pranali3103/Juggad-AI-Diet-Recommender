import os
from julep import Client

# Set your environment variables
os.environ['JULEP_API_URL'] = 'https://api-alpha.julep.ai/api'  # Or 'https://api-alpha.julep.ai' for Julep Cloud
os.environ['JULEP_API_KEY'] = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmMDVlZDM0NC01MjkyLTQ1NmUtODUxMS01ODZlNzU0ZmUzZmUiLCJlbWFpbCI6ImFkaXR5YWpldGh3YTYwQGdtYWlsLmNvbSIsImlhdCI6MTcxNzMxNTI1NywiZXhwaXJlc0luIjoiMXkiLCJyYXRlTGltaXRQZXJNaW51dGUiOjM1MDAsInF1b3RhUmVzZXQiOiIxaCIsImNsaWVudEVudmlyb25tZW50Ijoic2VydmVyIiwic2VydmVyRW52aXJvbm1lbnQiOiJwcm9kdWN0aW9uIiwidmVyc2lvbiI6InYwLjIiLCJleHAiOjE3NDg4NzI4NTd9.5IU9zQczdV1gFFpBbM4GT2wF6cRMr-Hz70x9FzfYWGB-qCzIxP1pkp3cg3of8rEg8GZTK-G3Z_U62PKgXOjGUQ'


# Initialize the client
base_url = os.environ.get("JULEP_API_URL")
api_key = os.environ.get("JULEP_API_KEY")
client = Client(api_key=api_key, base_url=base_url)

# Create a user
user = client.users.create(name="sid", about="An astronomy enthusiast.")

# Create an agent for comprehensive recommendations
agent = client.agents.create(
    name="Comprehensive Recommendations Agent",
    about="This agent provides recommendations for restaurants, breakfast, dinner, and workouts based on specified criteria.",
    instructions=[
        "Recommend 6 restaurant names based on specified criteria.",
        "Consider user preferences, dietary requirements, and regional context in recommendations."
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

# Create a session for the user and agent interaction
session = client.sessions.create(
    agent_id=agent.id,
    user_id=user.id,
    situation="You are providing recommendations for restaurants, breakfast, dinner, and workouts based on specified criteria."
)

# Define the input data directly
input_data = {
    'age': 25,
    'gender': 'male',
    'weight': '70 kg',
    'height': '175 cm',
    'veg_or_nonveg': 'non-veg',
    'disease': 'none',
    'region': 'India',
    'allergics': 'none',
    'foodtype': 'balanced'
}

# Format the user input into a message
user_message = (
    f"I am {input_data['age']} years old, {input_data['gender']}, my weight is {input_data['weight']} and my height is {input_data['height']}. "
    f"I prefer {input_data['veg_or_nonveg']} food. I have {input_data['disease']} and no allergies. "
    f"I live in {input_data['region']}. I prefer a {input_data['foodtype']} diet."
)

# Send the inputs to the session and get the recommendations
messages = [
    {"content": user_message, "role": "user"}
]

res = client.sessions.chat(
    session_id=session.id,
    messages=messages,
    recall=True,
    remember=True,
)

# Print the recommendations
recommendations = res.response[0][0].content
print(recommendations)
