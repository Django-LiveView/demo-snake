from liveview.context_processors import get_global_context
from core import settings
from liveview.utils import (
    get_html,
    update_active_nav,
    enable_lang,
    loading,
)
from channels.db import database_sync_to_async
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext as _
from random import randint


template = "pages/home.html"

# Database


# Functions

async def get_context(consumer=None):
    context = get_global_context(consumer=consumer)
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("home"),
            "title": _("Home") + " | LiveSnake",
            "meta": {
                "description": _("Home page of the website"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "home",
            "page": template,
        }
    )
    return context


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    # Nav
    await update_active_nav(consumer, "home")
    # Main
    my_context = await get_context(consumer=consumer)
    html = await get_html(template, my_context)
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": html,
    }
    data.update(my_context)
    await consumer.send_html(data)

async def random_number(consumer, client_data, lang=None):
    my_context = await get_context(consumer=consumer)
    data = {
        "action": client_data["action"],
        "selector": "#output-random-number",
        "html": randint(0, 10),
    }
    data.update(my_context)
    await consumer.send_html(data)
