const nextBtn = document.getElementById("nextBtn");
const numOfSubs = document.getElementById("numOfSubs");
const numOfSessions = document.getElementById("numOfSessions");
const inputsDiv = document.getElementById("inputs");

let nextDebounce = false;

function appendTheElement(Location, element) {
    Location.appendChild(element);
}

function next() {
    if (nextDebounce) return;
    nextDebounce = true;

    const heading1 = document.createElement("h1");
    heading1.innerText = "Subjects:";
    appendTheElement(inputsDiv, heading1);

    for (let i = 0; i < numOfSubs.value; i++) {
        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = "Subject " + (i + 1);
        input.id = "subject" + (i + 1);
        const br = document.createElement("br");
        appendTheElement(inputsDiv, br);
        appendTheElement(inputsDiv, input);
    }

    appendTheElement(inputsDiv, document.createElement("br"));
    //appendTheElement(inputsDiv, document.createElement(""));
    const heading2 = document.createElement("h1");
    heading2.innerText = "Number of Sessions:";
    appendTheElement(inputsDiv, heading2);

    for (let i = 0; i < numOfSubs.value; i++) {
        const label = document.createElement("label");
        label.innerText = "Number of Sessions for Subject " + (i + 1) + " in a week: ";
        const input = document.createElement("input");
        input.type = "number";
        input.id = "sub" + (i + 1) + "Sessions";
        input.min = "1";
        const br = document.createElement("br");
        appendTheElement(inputsDiv, br);
        appendTheElement(inputsDiv, label);
        appendTheElement(inputsDiv, input);
    }

    appendTheElement(inputsDiv, document.createElement("br"));

    const generateBtn = document.getElementById("generateBtn");
    generateBtn.hidden = false;


}