document.addEventListener("DOMContentLoaded", loadEvents);

async function loadEvents(){
    try {
        const res = await fetch("http://localhost:8080/api/events-madrid"); 
        const data = await res.json();

        const events = data._embedded?.events || [];

        buildList(events);
        buildCalendar(events);

    } catch(err){
        console.error("Error loading events:", err);
    }
}

function buildList(events){
    const box = document.getElementById("event-list");
    box.innerHTML = "";

    events.forEach(ev=>{
        const start = ev.dates.start.localDate || "";
        const end = ev.dates.end?.localDate || start;

        const li = document.createElement("li");
        li.innerHTML = `
            <b>${ev.name}</b><br>
            <small>📅 ${start} → ${end}</small><br>
            <a href="${ev.url}" target="_blank">Open Event</a>
        `;
        box.appendChild(li);
    });
}

function buildCalendar(events){
    const calEl = document.getElementById("eventsCalendar");

    new FullCalendar.Calendar(calEl,{
        initialView:"dayGridMonth",
        height:"100%",
        events: events.map(ev => ({
            title: ev.name,
            start: ev.dates.start.localDate,
            end: ev.dates.end?.localDate,
            url: ev.url
        })),
        eventClick(info){
            if(info.event.url){
                info.jsEvent.preventDefault();
                window.open(info.event.url,"_blank");
            }
        }
    }).render();
}
