from openai import OpenAI
import json
import time

client = OpenAI()

CV_ASSISTANT_ID = 'ASSISTANT_ID'  # or a hard-coded ID like "asst-..."

#Create Assistant
def create_assistant(v_name, v_instructions, v_model):
    assistant = client.beta.assistants.create(
        name = v_name, # "Math Tutor",
        instructions = v_instructions, #"You are a personal math tutor. Answer questions briefly, in a sentence or less.",
        model = v_model, #"gpt-3.5-turbo",
    )

#Create thread and run and return them
def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(CV_ASSISTANT_ID, thread, user_input)
    return thread, run

def not_create_thread_and_run(user_input):
    thread = client.beta.threads.retrieve('thread_vHK64OkfmNUDHqyOMwNVZgLb')
    run = submit_message(CV_ASSISTANT_ID, thread, user_input)
    return thread, run

#Submit message and create run
def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        #instructions="Eres un bot especializado en el LMS Moodle. Contesta de forma pormenorizada preguntas de este producto."
    )

#Wait till the run is completed
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

#Get the response from Assistant
def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

# Emulating concurrent user requests
#thread1, run1 = create_thread_and_run(
#    "Pensaba en un foro donde pueda comunicar como docente novedades de la materia"
#)

# Emulating next message from same thread
thread1, run1 = not_create_thread_and_run(
    "Si, gracias. Puedes guiarme?"
)

# Wait for Run 1
run1 = wait_on_run(run1, thread1)
pretty_print(get_response(thread1))

print(thread1)
