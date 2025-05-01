# AI Voice Assistant

This project is an AI voice assistant that utilizes the VAPI API and the ChatGPT-4o model to provide an interactive voice experience. Users can interact with the assistant via voice commands, making it ideal for various applications.

## Features

- Voice interaction using VAPI API
- Natural language processing with ChatGPT-4o model
- Easy setup with environment variables

## Prerequisites

Before you begin, ensure you have the following:

- A [VAPI](https://vapi.ai/) account
- Create a custom AI agent on the VAPI dashboard OR hard code the AI agent into main.py with desired prompts
- A [Twilio](https://www.twilio.com/) account
- A Twilio phone number
- .env file containing respective API keys and Twilio phone number

## Requirements
```pip install vapi os dotenv```

## What main.py does
We access the VAPI API to retrieve the AI Agent and calls the Twilio phone number.  
The user will then converse with the AI agent which follows a given prompt in the dashboard/code.  
Summary and Transcript of the conversation will be produced in their respective text files. New conversations will override old data.

