"use strict";

document.addEventListener("DOMContentLoaded", async () => {
  const baseUrl = "http://127.0.0.1:8000";
  const sheltersElement = document.getElementById("shelters");
  const response = await fetch(`${baseUrl}/shelters`);
  const shelters = await response.json();
  shelters.map((shelter) => {
    const shelterCard = createShelterCard(shelter);
    sheltersElement.appendChild(shelterCard);
});
});

function createShelterCard(shelter) {
    const [ addressStreet, addressCity, addressStateZip ] = shelter.address.split(",");
    console.log(addressStreet, addressCity, addressStateZip);
    const contentElement = document.createElement("section");
    contentElement.innerHTML += `
    <div class="shelter-card">
        <h3 class="shelter-card-name">${shelter.name}</h3>
        <address>
        <p class="shelter-card-address">${addressStreet}<br>${addressCity}, ${addressStateZip}</p>
        </address>
        <div class="shelter-card-animal-counts">
            <div class="shelter-card-animal-count">
                <p class="shelter-card-animal-label dog-label">Dogs</p>
                <p class="shelter-card-animal-number dog-number">${shelter.animals.dogs}</p>
            </div>
            <div>
                <p class="shelter-card-animal-label cat-label">Cats</p>
                <p class="shelter-card-animal-number cat-number">${shelter.animals.cats}</p>
            </div>
        </div>
    </div>
    `
    return contentElement;
}
