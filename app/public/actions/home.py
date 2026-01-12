from django.shortcuts import render


def send_page(request):
    """Render the home page"""
    return render(
        request,
        "pages/home.html",
        {
            "title": "LiveSnake - Django LiveView Demo",
        },
    )
