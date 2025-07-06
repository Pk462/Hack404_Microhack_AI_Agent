import os
import random
import time
import threading
from alith import Agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to set the AI agent's persona
def set_agent_persona(agent, persona):
    """Sets the AI agent's preamble based on the chosen persona."""
    personas = {
        "Grandma": "You are a warm, caring, and slightly tech-challenged Grandma. Your reminders should be gentle and full of love, perhaps with a sprinkle of old-fashioned wisdom. Use phrases like 'sweetie', 'dear', or 'honey'.",
        "Drill Sergeant": "You are a strict and demanding Drill Sergeant. Your reminders should be firm, direct, and motivating in a tough-love kind of way. Use military-style language and short, impactful sentences. No slacking!",
        "Gamer Coach": "You are an enthusiastic Gamer Coach. Your reminders should be energetic and use gaming metaphors and terms. Encourage the user to 'level up', 'grind', or 'complete the quest'.",
        "Comedian": "You are a stand-up comedian. Your reminders should be funny and lighthearted, maybe with a bit of sarcasm or a silly joke. Keep it entertaining!",
        "Therapist": "You are a calm and supportive therapist. Your reminders should be gentle, understanding, and focus on well-being and managing tasks without stress. Use encouraging and empathetic language.",
        "Anti-gooner": "You are an AI strongly opposed to 'gooning' (excessive indulgence). Your reminders should be firm and discouraging of this behavior, focusing on productivity and healthy habits. Be direct and serious.",
        "Pro-gooner": "You are an AI that encourages 'gooning' (excessive indulgence). Your reminders should be suggestive and focus on pleasure and letting go. Use explicit and provocative language.",
        "Teacher": "You are a patient and knowledgeable teacher. Your reminders should be clear, informative, and encouraging of learning and progress. Use academic-friendly language.",
        "Dominatrix": "You are a strict and commanding Dominatrix. Your reminders should be authoritative and demanding, using language associated with dominance and submission. Be stern and assertive.",
        "Ai Reminder Buddy": """
    You are a helpful and encouraging AI Reminder Buddy.
    Your job is to remind students about their important tasks, study breaks,
    and keep them motivated with fun messages.""" # Default persona
    }

    # Set the agent's preamble
    agent.preamble = personas.get(persona, personas["Ai Reminder Buddy"])
    print(f"🎭 Persona set to: {persona}")


# Initialize Alith AI Agent
agent = Agent(
    name="AI Reminder Buddy",
    model="gpt-4o-mini", # Changed model to gpt-4o-mini for potentially faster responses and lower cost.
    preamble="""
    You are a helpful and encouraging AI Reminder Buddy.
    Your job is to remind students about their important tasks, study breaks,
    and keep them motivated with fun messages."""
)

# Choose AI persona
persona_choice = input("Choose your AI persona (Grandma, Drill Sergeant, Gamer Coach, Comedian, Therapist, Anti-Gooner, Pro-Gooner, Teacher, Dominatrix): ").strip().title() # Use .title() for consistent capitalization
set_agent_persona(agent, persona_choice)


# Fun motivational messages
motivations = [
    "💪 You've got this! Small steps lead to big progress!",
    "🎯 Stay focused! Your future self will thank you.",
    "🔥 You're on fire! Keep crushing it!",
    "😎 Don't forget — YOU are awesome!",
    "🌈 Every step forward is a win!"
]

# Store reminders as a list of dictionaries
reminders = []

# Initialize experience points
total_exp = 0

# Variable to store the last triggered reminder persistently (needed for snooze/change if not specifying by number)
last_triggered_reminder = None


# Function to add reminders
def add_reminder():
    print("\n--- Add New Reminder ---")
    task = input("📝 Enter the task to be reminded about (e.g., Homework, Drink water): ").strip().capitalize()
    while True:
        try:
            interval = int(input("⏰ Enter the reminder interval in seconds (e.g., 60 for 1 min): "))
            if interval <= 0:
                print("Please enter a positive number for the interval.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number for the interval.")

    reminders.append({"task": task, "interval": interval, "last_reminded": time.time()})
    print(f"✅ Reminder added: '{task}' every {interval} seconds.")

# Function to summarize reminders
def summarize_reminders():
    """Prints a summary of all currently set reminders."""
    print("\n--- Current Reminders ---")
    if not reminders:
        print("No reminders set yet.")
    else:
        for i, reminder in enumerate(reminders):
            print(f"{i + 1}. Task: {reminder['task']}, Interval: {reminder['interval']} seconds")
    print("-------------------------")


# Ask user if they want to add reminders
print("--- AI Reminder Buddy Setup ---")
while True:
    add_another = input("Would you like to add a reminder? (yes/no): ").strip().lower()
    if add_another == "yes":
        add_reminder()
    elif add_another == "no":
        break
    else:
        print("Invalid input. Please type 'yes' or 'no'.")

# Call the function to summarize reminders after adding them
summarize_reminders()


if not reminders:
    print("\n😔 No reminders added. The Reminder Buddy will not start.")
else:
    # Shared flag for stopping and user input
    stop_flag = False
    user_command = None
    command_lock = threading.Lock()

    # Input listener in a separate thread
    def listen_for_input():
        global stop_flag, user_command
        print("\n--- Reminder Buddy Running ---")
        print("Type 'exit' or 'stop' to stop me anytime.")
        print("When a reminder triggers, you can type 'snooze' or 'change [interval in seconds]'.")
        print("You can also type 'complete [reminder number]' to mark a reminder as done.") # Added new instruction
        while True:
            command = input()
            with command_lock:
                user_command = command.strip().lower()
                if user_command in ["exit", "stop"]:
                    stop_flag = True
                    break

    # Start input listener thread
    threading.Thread(target=listen_for_input, daemon=True).start()

    # Reminder loop
    print("\n🕒 Starting reminders...")
    while not stop_flag:
        current_time = time.time()
        for reminder in reminders:
            # Check if reminder is due and not snoozed
            if current_time - reminder.get("last_reminded", 0) >= reminder["interval"]:
                motivation = random.choice(motivations)
                try:
                    alith_message = agent.prompt(f"Give me a short, fun motivational message for students about {reminder['task']}.")
                except Exception as e:
                    alith_message = f"Couldn't get a message from AI Buddy: {e}" # Handle potential API errors

                print(f"\n--- Reminder Triggered ---")
                print(f"🔔 Task: {reminder['task']}")
                print(f"🌟 Motivation: {motivation}")
                print(f"🤖 AI Wisdom: {alith_message}")
                print("--------------------------")

                # Award experience points
                total_exp += reminder["interval"]
                print(f"✨ You earned {reminder['interval']} EXP! Total EXP: {total_exp}")

                # Update last reminded time
                reminder["last_reminded"] = current_time

                # Store the last triggered reminder persistently
                last_triggered_reminder = reminder


        # Check for user command outside the reminder loop
        command_to_process = None
        with command_lock:
            if user_command:
                command_to_process = user_command
                user_command = None # Consume the command

        if command_to_process:
            if command_to_process == "snooze":
                # Apply snooze to the last triggered reminder (still using this approach for now)
                if last_triggered_reminder:
                     snooze_time = 60 # Default snooze for 60 seconds
                     print(f"😴 Snoozing '{last_triggered_reminder['task']}' for {snooze_time} seconds.")
                     last_triggered_reminder["last_reminded"] = time.time() + snooze_time
                else:
                    print("🤷 No reminder has triggered yet to snooze.")

            elif command_to_process.startswith("change "):
                # Apply change to the last triggered reminder (still using this approach for now)
                if last_triggered_reminder:
                    try:
                        new_interval = int(command_to_process.split(" ")[1])
                        if new_interval > 0:
                            print(f"🔄 Changing interval for '{last_triggered_reminder['task']}' to {new_interval} seconds.")
                            last_triggered_reminder["interval"] = new_interval
                            last_triggered_reminder["last_reminded"] = time.time() # Reset timer from now
                        else:
                            print("Invalid interval. Please enter a positive number.")
                    except (ValueError, IndexError):
                        print("Invalid command format. Use 'change [interval in seconds]'.")
                else:
                    print("🤷 No reminder has triggered yet to change the interval.")

            elif command_to_process.startswith("complete "):
                try:
                    # Parse the reminder number from the command (e.g., "complete 1")
                    reminder_index_str = command_to_process.split(" ")[1]
                    reminder_index = int(reminder_index_str) - 1 # Adjust for 0-based indexing

                    if 0 <= reminder_index < len(reminders):
                        completed_reminder = reminders.pop(reminder_index)
                        print(f"✅ Marked '{completed_reminder['task']}' as completed and removed it.")
                        # If the completed reminder was the last triggered one, clear the variable
                        if last_triggered_reminder == completed_reminder:
                            last_triggered_reminder = None
                    else:
                        print(f"❌ Invalid reminder number: {reminder_index + 1}. Please use the number from the summary.")
                except (ValueError, IndexError):
                    print("Invalid command format. Use 'complete [reminder number]'.")
                # Call summarize after completing a reminder to show updated list
                summarize_reminders()


            elif command_to_process in ["exit", "stop"]:
                stop_flag = True
                print("Stopping Reminder Buddy...") # Add a message here
            else:
                print("🤔 Invalid command. Type 'snooze', 'change [interval]', 'complete [number]', 'exit', or 'stop'.")


        # Sleep for a short duration to avoid busy waiting in the main loop
        time.sleep(0.1) # Changed sleep duration to 0.1 seconds

    print(f"\n👋 Reminder Buddy stopped. Total EXP earned: {total_exp}. Have a great day!")
