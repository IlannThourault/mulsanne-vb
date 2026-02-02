// Mobile menu toggle
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Close menu when clicking on a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
    });
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.8s ease-out';
        }
    });
}, observerOptions);

document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
});

async function chargerMatchs() {
    const tbody = document.getElementById('liste-matchs');
    try {
        const response = await fetch('matchs.json');
        const data = await response.json();

        if (data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='4'>Aucun match à venir.</td></tr>";
            return;
        }

        tbody.innerHTML = data.map(match => {
            // Déterminer la classe CSS selon la catégorie (minuscule pour correspondre au CSS)
            const categorieClass = match.Categorie.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); 
            // Note : le code ci-dessus transforme "Féminin" en "feminin" pour le CSS

            // Déterminer si c'est à domicile (Mulsanne reçoit)
            const estADomicile = match.Equipe_domicile.toUpperCase().includes("MULSANNE");

            return `
                <tr class="${categorieClass}">
                    <td><span class="badge">${match.Categorie}</span></td>
                    <td>${match.Date}</td>
                    <td>${match.Heure}</td>
                    <td>
                        
                        <strong>${match.Equipe_domicile}</strong> vs <strong>${match.Equipe_exterieur}</strong>
                    </td>
                </tr>
            `;
        }).join('');

    } catch (error) {
        console.error("Erreur de chargement:", error);
        tbody.innerHTML = "<tr><td colspan='4' style='color:red;'>Erreur lors de la lecture du fichier JSON.</td></tr>";
    }
}

// Lancement au chargement de la page
window.onload = chargerMatchs;