let tasks = [];

document.getElementById("form").addEventListener("submit", e => {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const due = document.getElementById("due_date").value;
    const hours = parseFloat(document.getElementById("hours").value);
    const importance = parseInt(document.getElementById("importance").value);
    const deps = document.getElementById("deps").value.split(",").map(x => x.trim()).filter(x => x);

    const task = {
        id: (tasks.length + 1).toString(),
        title,
        due_date: due,
        estimated_hours: hours,
        importance,
        dependencies: deps
    };

    tasks.push(task);

    document.getElementById("taskDisplay").innerText = JSON.stringify(tasks, null, 2);

    document.getElementById("form").reset();
});

async function analyze() {
    const strategy = document.getElementById("strategy").value;

    const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tasks, strategy})
    });

    const data = await response.json();

    const out = document.getElementById("results");
    out.innerHTML = "";

    data.analyzed.forEach(t => {
        const div = document.createElement("div");
        div.className = "task " + (t.score >= 75 ? "high" : t.score >= 40 ? "medium" : "low");
        div.innerHTML = `<strong>${t.title}</strong> — Score: ${t.score}<br>${t.explanation}`;
        out.appendChild(div);
    });
}
