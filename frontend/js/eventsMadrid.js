document.addEventListener("DOMContentLoaded", loadEvents);

function deduplicateEvents(events) {
  const seen = new Set();
  const uniqueEvents = [];

  for (const ev of events) {
    const key = ev.name + '_' + ev.dates.start.localDate;

    if (!seen.has(key)) {
      seen.add(key);
      uniqueEvents.push(ev);
    }
  }

  return uniqueEvents;
}


async function loadEvents() {
  try {
    const res = await fetch("http://localhost:8080/api/events-madrid");
    const data = await res.json();

    let events = data._embedded?.events || [];
    events = deduplicateEvents(events);

    buildList(events);
    buildCalendar(events);
  } catch (err) {
    console.error("Error loading events:", err);
  }
}


function buildList(events) {
  const box = document.getElementById("event-list");
  box.innerHTML = "";

  events.forEach(ev => {
    const start = ev.dates.start.localDate || "";
    const end = ev.dates.end?.localDate || start;

    const dateDisplay = (start === end) ? start : `${start} → ${end}`;

    const li = document.createElement("li");
    li.innerHTML = `
      <div class="event-card">
        <h4>${ev.name}</h4>
        <p>📅 ${dateDisplay}</p>
        <a href="${ev.url}" target="_blank" rel="noopener noreferrer">Open Event</a>
      </div>
    `;
    box.appendChild(li);
  });
}


function buildCalendar(events){
    const calEl = document.getElementById("eventsCalendar");

    new FullCalendar.Calendar(calEl, {
        initialView:"dayGridMonth",
        height:"100%",
        events: events.map(ev => {
            const start = ev.dates.start.localDate;
            const end = ev.dates.end?.localDate;

            return {
                title: ev.name,
                start,
                end: (start !== end) ? end : null, 
                allDay: true,                      
                url: ev.url,
                backgroundColor: "#627e9e",
                borderColor: "#2c5777",
                textColor: "white"
            };
        }),

        eventClick(info){
            info.jsEvent.preventDefault();
            window.open(info.event.url,"_blank");
        }
    }).render();
}

