from datetime import date, datetime
from collections import defaultdict, deque

def clamp(x, a, b):
    return max(a, min(b, x))

def parse_date(s):
    if isinstance(s, (date, datetime)):
        return s.date() if isinstance(s, datetime) else s
    return datetime.strptime(s, "%Y-%m-%d").date()

def compute_subscores(tasks):
    today = date.today()
    graph = {t['id']: t.get('dependencies', []) for t in tasks}

    visited, recstack = set(), set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        recstack.add(node)
        for dep in graph.get(node, []):
            if dep not in graph:
                continue
            if dep not in visited:
                if dfs(dep, path + [dep]):
                    return True
            elif dep in recstack:
                cycles.append(path[path.index(dep):] + [dep])
                return True
        recstack.remove(node)
        return False

    for t in graph:
        if t not in visited:
            dfs(t, [t])

    reverse = defaultdict(list)
    for t, deps in graph.items():
        for d in deps:
            reverse[d].append(t)

    dependent_counts = {}
    for node in graph:
        q = deque(reverse.get(node, []))
        seen = set()
        while q:
            c = q.popleft()
            if c in seen:
                continue
            seen.add(c)
            q.extend(reverse.get(c, []))
        dependent_counts[node] = len(seen)

    results = []
    for t in tasks:
        due = parse_date(t['due_date'])
        days_left = (due - today).days

        urgency_score = 100 if days_left <= 0 else clamp(100 - clamp(days_left, 0, 100), 0, 100)
        importance_score = clamp((t['importance'] / 10) * 100, 0, 100)
        effort_score = clamp(100 - clamp(t['estimated_hours'] * 10, 0, 100), 0, 100)
        dep_score = clamp(dependent_counts.get(t['id'], 0) * 25, 0, 100)

        results.append({
            "task": t,
            "urgency_score": urgency_score,
            "importance_score": importance_score,
            "effort_score": effort_score,
            "dependency_score": dep_score,
            "cycle": any(t['id'] in c for c in cycles)
        })

    return results, cycles

def compute_score(s, w):
    score = (
        s["urgency_score"] * w["urgency"] +
        s["importance_score"] * w["importance"] +
        s["effort_score"] * w["effort"] +
        s["dependency_score"] * w["dependency"]
    )
    return int(round(score))

def analyze_tasks(tasks, strategy='smart'):
    strategies = {
        "smart": {"urgency":0.35, "importance":0.35, "effort":0.20, "dependency":0.10},
        "fastest": {"urgency":0.15, "importance":0.2, "effort":0.6, "dependency":0.05},
        "impact": {"urgency":0.2, "importance":0.7, "effort":0.05, "dependency":0.05},
        "deadline": {"urgency":0.8, "importance":0.1, "effort":0.05, "dependency":0.05},
    }

    for i, t in enumerate(tasks):
        t.setdefault("id", str(i+1))
        t.setdefault("dependencies", [])

    subscores, cycles = compute_subscores(tasks)
    weights = strategies.get(strategy, strategies["smart"])

    analyzed = []
    for s in subscores:
        score = compute_score(s, weights)
        explanation = (
            f"Urgency {s['urgency_score']}, "
            f"Importance {s['importance_score']}, "
            f"Effort {s['effort_score']}, "
            f"Dependency {s['dependency_score']}"
        )
        analyzed.append({
            "id": s["task"]["id"],
            "title": s["task"]["title"],
            "score": score,
            "explanation": explanation,
            "task": s["task"],
            "cycle": s["cycle"]
        })

    analyzed.sort(key=lambda x: x["score"], reverse=True)
    return analyzed, cycles
