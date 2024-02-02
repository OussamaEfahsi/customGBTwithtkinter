import os
from PIL import Image
import customtkinter
from openai import OpenAI
from customtkinter import CTk
import threading

class App(CTk):
    def __init__(self):
        super().__init__()
        self.api_key = "ur API code CHATGBT"
        self.client = OpenAI(api_key=self.api_key)
        self.title("ChatGBT Application")
        self.geometry("700x450")

        # Set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))

        # Create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="ChatGBT Application", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.chat_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="ChatGBT",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.chat_image, anchor="w", command=self.chat_button_event)
        self.chat_button.grid(row=1, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Create ChatGBT widget
        self.api_key = "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"
        self.client = OpenAI(api_key=self.api_key)
        self.chat_history = customtkinter.CTkTextbox(self.home_frame, state="disabled", height=380, width=450)
        self.chat_history.pack(padx=10, pady=10)

        # Create ChatGBT input and generate button
        self.chat_input = customtkinter.CTkEntry(self.home_frame, width=380, height=30)
        self.chat_input.pack(side="left", padx=10, pady=(0, 10))

        self.chat_run_button = customtkinter.CTkButton(self.home_frame, height=30, width=50, text="Run", command=self.send_message)
        self.chat_run_button.pack(side="right", padx=10, pady=(0, 10))

        self.home_frame.grid(row=0, column=1, sticky="nsew")

        # Create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Select default frame
        self.select_frame_by_name("ChatGBT")

    def select_frame_by_name(self, name):
        # Set button color for selected button
        self.chat_button.configure(fg_color=("gray75", "gray25") if name == "ChatGBT" else "transparent")

        # Show selected frame
        if name == "ChatGBT":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def chat_button_event(self):
        self.select_frame_by_name("ChatGBT")

    def get_chat_response(self, message):
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}],
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def update_chat_history(self, message):
        """
        Update the chat history with a new message.
        """
        self.chat_history.configure(state="normal")  # Enable editing the chat history
        self.chat_history.insert("end", message + "\n")  # Add the new message to the chat history
        self.chat_history.configure(state="disabled")  # Disable editing the chat history

    def send_message(self):
        message = self.chat_input.get()  # Get the message from the input field
        self.chat_input.delete(0, "end")  # Clear the input field
        self.update_chat_history("You: " + message)  # Update chat history with user's message
        self.update_chat_history("Bot is typing...")  # Indicate that the bot is typing

        # Start a new thread to process the response
        threading.Thread(target=self.process_chat_response, args=(message,)).start()

    def process_chat_response(self, message):
        response = self.get_chat_response(message)  # Get the response from the chatbot
        self.update_chat_history("Bot: " + response)  # Update chat history with bot's response

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
