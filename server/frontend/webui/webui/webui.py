"""Welcome to Reflex! This file outlines the steps to create a basic app."""
# from rxconfig import config

import reflex as rx

from webui import styles  # noqa: F401
from webui.components import chat, navbar, sidebar, modal # noqa: F401
from webui.state import State  # noqa: F401


def error_text() -> rx.Component:
    """return a text component to show error."""
    return rx.text(State.error_texts, text_align="center", font_weight="bold", color="red",)

@rx.page(
    title="Scalian ChatBot",
    description="A chatbot application. for Scalian users",
)
def index() -> rx.Component:
    """The main app."""
    return rx.vstack(
        navbar(),
        chat.header(),
        chat.chat(),
        chat.action_bar(),
        sidebar(),
        modal(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0",
        # background_image="A-propos-listing.jpg",
        # background_size="top",
    )


# Create app instance and add index page.
app = rx.App(style=styles.base_style)
app.add_page(index)
