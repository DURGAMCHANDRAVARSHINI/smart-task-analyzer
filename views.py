from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scoring import analyze_tasks

@api_view(["POST"])
def analyze(request):
    tasks = request.data.get("tasks", [])
    strategy = request.data.get("strategy", "smart")

    analyzed, cycles = analyze_tasks(tasks, strategy)
    return Response({
        "analyzed": analyzed,
        "cycles": cycles
    })

