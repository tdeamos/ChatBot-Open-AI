from openai import OpenAI
import json
import time

client = OpenAI()

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

MATH_ASSISTANT_ID = 'asst_UDx63Wdov7RJ2Q99OMfBlOTR'  # or a hard-coded ID like "asst-..."

#Retrieve Assistant
assistant = client.beta.assistants.retrieve(MATH_ASSISTANT_ID)

#Create Thread
thread = client.beta.threads.create()

#Add message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

#Run Assistant
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

run = wait_on_run(run, thread)

#Display assistant response
messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print("\nThread messages:")

for thread_message in messages.data:
    # Iterate over the 'content' attribute of the ThreadMessage, which is a list
    for content_item in thread_message.content:
        # Assuming content_item is a MessageContentText object with a 'text' attribute
        # and that 'text' has a 'value' attribute, print it
        print(content_item.text.value)


