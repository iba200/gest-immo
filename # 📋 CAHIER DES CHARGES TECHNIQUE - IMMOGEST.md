\# 📋 CAHIER DES CHARGES TECHNIQUE \- IMMOGEST

\*\*Version:\*\* 1.0    
\*\*Date:\*\* Décembre 2025   
\*\*Client:\*\* Nexatech (produit interne)    
\*\*Stack:\*\* Flask \+ TailwindCSS \+ JavaScript

\---

\#\# 1\. PRÉSENTATION DU PROJET

\#\#\# 1.1 Contexte  
ImmoGest est un logiciel SaaS de gestion immobilière destiné aux bailleurs et agences immobilières au Sénégal. L'application permet d'automatiser la gestion des biens, locataires, loyers et documents.

\#\#\# 1.2 Objectifs  
\- Digitaliser la gestion locative des bailleurs sénégalais  
\- Automatiser les relances de paiements par SMS  
\- Générer automatiquement les quittances de loyer  
\- Fournir des rapports financiers pour la comptabilité  
\- Offrir une solution 100% adaptée au marché sénégalais

\#\#\# 1.3 Public Cible  
\- \*\*Primaire:\*\* Bailleurs individuels (3-50 biens)  
\- \*\*Secondaire:\*\* Agences immobilières  
\- \*\*Tertiaire:\*\* Diaspora investissant au Sénégal

\---

\#\# 2\. SPÉCIFICATIONS TECHNIQUES

\#\#\# 2.1 Stack Technologique

\*\*Backend:\*\*  
\- Framework: Flask 3.0+  
\- Langage: Python 3.11+  
\- ORM: SQLAlchemy 3.1+  
\- Migrations: Alembic (Flask-Migrate)  
\- Authentification: Flask-Login \+ JWT  
\- Validation: WTForms  
\- Tasks asynchrones: Celery \+ Redis

\*\*Frontend:\*\*  
\- CSS Framework: TailwindCSS 3.4+  
\- JavaScript: Vanilla JS (ES6+)  
\- Charts: Chart.js 4.0+  
\- PDF côté client: jsPDF  
\- Icons: Lucide Icons / Heroicons

\*\*Base de Données:\*\*  
\- Développement: SQLite  
\- Production: PostgreSQL 15+

\*\*APIs Externes:\*\*  
\- Orange SMS API (notifications)  
\- Wave API (paiements \- Version 2\)  
\- Orange Money API (paiements \- Version 2\)

\*\*Hébergement:\*\*  
\- Serveur: DigitalOcean / VPS Ubuntu 22.04  
\- Reverse Proxy: Nginx  
\- WSGI: Gunicorn  
\- SSL: Let's Encrypt  
\- Monitoring: Sentry

\---

\#\# 3\. ARCHITECTURE APPLICATIVE

\#\#\# 3.1 Structure Projet

\`\`\`  
immogest/  
├── app/  
│   ├── models/          \# Modèles de données  
│   ├── routes/          \# Controllers/Routes  
│   ├── forms/           \# Formulaires WTForms  
│   ├── services/        \# Business logic  
│   ├── utils/           \# Utilitaires  
│   ├── static/          \# Assets (CSS, JS, images)  
│   └── templates/       \# Templates Jinja2  
├── migrations/          \# Migrations DB  
├── tests/               \# Tests unitaires  
├── config.py           \# Configuration  
├── requirements.txt    \# Dépendances Python  
└── run.py             \# Point d'entrée  
\`\`\`

\#\#\# 3.2 Modèle de Données Principal

\*\*Entités:\*\*  
\- \*\*User\*\* (Bailleur)  
\- \*\*Property\*\* (Bien immobilier)  
\- \*\*Tenant\*\* (Locataire)  
\- \*\*Payment\*\* (Paiement de loyer)  
\- \*\*Contract\*\* (Contrat de bail)  
\- \*\*Maintenance\*\* (Demandes de maintenance \- V2)

\---

\#\# 4\. FONCTIONNALITÉS MVP (Version 1\)

\#\#\# 4.1 Module Authentification

\*\*Pages:\*\*  
\- Inscription (email, téléphone, mot de passe)  
\- Connexion (email/téléphone \+ mot de passe)  
\- Mot de passe oublié (reset par email)  
\- Profil utilisateur

\*\*Règles:\*\*  
\- Email unique  
\- Téléphone format \+221XXXXXXXXX  
\- Mot de passe minimum 8 caractères (1 maj, 1 chiffre)  
\- Vérification email obligatoire  
\- Rate limiting: 5 tentatives / 15 min

\---

\#\#\# 4.2 Module Dashboard

\*\*Affichage:\*\*  
\- Statistiques clés (nombre de biens, locataires, taux occupation)  
\- Revenus du mois (loyers payés vs attendus)  
\- Graphique évolution revenus (12 mois)  
\- Liste loyers du mois (statut: payé/impayé/en retard)  
\- Alertes (loyers en retard, baux expirant, maintenance)  
\- Raccourcis actions rapides

\*\*Données calculées:\*\*  
\- Total biens  
\- Taux d'occupation (%)  
\- Loyers attendus mois actuel  
\- Loyers perçus mois actuel  
\- Nombre paiements en retard  
\- Contrats expirant (60 jours)

\---

\#\#\# 4.3 Module Gestion des Biens

\*\*Fonctionnalités:\*\*  
\- Ajouter un bien (formulaire multi-champs)  
\- Lister tous les biens (vue grille \+ liste)  
\- Détails d'un bien  
\- Modifier un bien  
\- Supprimer un bien (soft delete)  
\- Upload photos (max 10, 5MB chacune)  
\- Filtres (type, statut, ville)  
\- Recherche par adresse/nom

\*\*Informations collectées:\*\*  
\- Nom, type, adresse, ville, quartier  
\- Chambres, salles de bain, surface (m²)  
\- Équipements (parking, jardin, meublé, etc.)  
\- Loyer mensuel, charges, caution  
\- Statut (vacant, occupé, maintenance)  
\- Photos, description

\*\*Validations:\*\*  
\- Nom obligatoire (max 100 caractères)  
\- Adresse obligatoire  
\- Loyer obligatoire (\> 0\)  
\- Photos: JPG/PNG, max 5MB

\---

\#\#\# 4.4 Module Gestion des Locataires

\*\*Fonctionnalités:\*\*  
\- Ajouter un locataire  
\- Lier locataire à un bien  
\- Lister tous les locataires  
\- Fiche détaillée locataire  
\- Modifier locataire  
\- Historique paiements  
\- Archiver locataire (départ)  
\- Upload documents (CNI, contrat)

\*\*Informations collectées:\*\*  
\- Identité (nom, prénom, email, téléphone)  
\- Documents (CNI, numéro)  
\- Professionnel (métier, employeur, revenus)  
\- Contact d'urgence  
\- Date entrée/sortie  
\- Notes privées

\*\*Règles:\*\*  
\- Un locataire \= un bien à la fois  
\- Téléphone obligatoire (+221)  
\- Email optionnel mais validé

\---

\#\#\# 4.5 Module Paiements & Loyers

\*\*Fonctionnalités:\*\*  
\- Enregistrer un paiement  
\- Générer quittance PDF automatiquement  
\- Lister tous les paiements  
\- Filtres (statut, date, bien, locataire)  
\- Historique complet par locataire  
\- Marquer comme payé/en retard  
\- Envoyer quittance par email  
\- Tableau récapitulatif mensuel

\*\*Informations collectées:\*\*  
\- Bien/Locataire  
\- Période (mois/année)  
\- Montant loyer, charges, pénalités, remise  
\- Date de paiement  
\- Mode de paiement (cash, Wave, OM, virement)  
\- Référence transaction  
\- Notes

\*\*Génération Quittance:\*\*  
\- Format: PDF  
\- Numéro unique: IMO-2025-0001  
\- Contenu: Infos bailleur, locataire, détail paiement  
\- Téléchargement \+ envoi email

\*\*Règles:\*\*  
\- Numéro quittance unique et séquentiel  
\- Pas de doublon (même bien \+ même mois)  
\- Alerte automatique J+5 si impayé  
\- Statut "late" si J+10

\---

\#\#\# 4.6 Module Relances SMS Automatiques

\*\*Fonctionnalités:\*\*  
\- Configuration date limite mensuelle (ex: 5 de chaque mois)  
\- Envoi automatique SMS J+3 si impayé  
\- Rappel SMS J+10 si toujours impayé  
\- Personnalisation templates SMS  
\- Historique SMS envoyés  
\- Désactivation par locataire

\*\*Templates SMS:\*\*  
\`\`\`  
J+3:   
"Bonjour \[Prénom\], nous n'avons pas encore reçu   
le loyer de \[Mois\]. Montant: \[X\] FCFA.   
Merci de régulariser. \[Bailleur\] \[Tél\]"

J+10:  
"Bonjour \[Prénom\], le loyer de \[Mois\] est en   
retard depuis 10 jours. Merci de nous contacter.   
\[Bailleur\] \[Tél\]"  
\`\`\`

\*\*Implémentation:\*\*  
\- Tâche Celery quotidienne (9h)  
\- Intégration Orange SMS API  
\- Logs envois

\---

\#\#\# 4.7 Module Rapports & Statistiques

\*\*Rapports disponibles:\*\*

1\. \*\*Rapport Mensuel:\*\*  
   \- Total loyers collectés  
   \- Loyers en attente  
   \- Taux de recouvrement  
   \- Dépenses maintenance  
   \- Résultat net

2\. \*\*Rapport Annuel:\*\*  
   \- Revenus locatifs totaux  
   \- Dépenses par catégorie  
   \- Taux d'occupation moyen  
   \- Graphique évolution 12 mois

3\. \*\*Rapport par Bien:\*\*  
   \- Historique paiements  
   \- Rentabilité  
   \- Temps de vacance

\*\*Exports:\*\*  
\- PDF (via ReportLab)  
\- Excel/CSV  
\- Graphiques Chart.js

\---

\#\#\# 4.8 Module Paramètres

\*\*Fonctionnalités:\*\*  
\- Modifier profil utilisateur  
\- Changer mot de passe  
\- Configurer date limite loyer (1-28)  
\- Personnaliser templates SMS  
\- Activer/désactiver notifications  
\- Gérer abonnement (upgrade/downgrade)  
\- Export données (RGPD)  
\- Supprimer compte

\---

\#\# 5\. FONCTIONNALITÉS VERSION 2 (Post-MVP)

\*\*Non incluses dans MVP mais à prévoir:\*\*  
\- Portail locataire (connexion, consultation, paiement)  
\- Paiements automatiques Wave/OM (API)  
\- Gestion maintenance (tickets, fournisseurs)  
\- Contrats de bail digitaux (signature électronique)  
\- Multi-utilisateurs (délégation agences)  
\- Application mobile (React Native)  
\- Rappels WhatsApp  
\- Comptabilité avancée  
\- Intégration logiciels comptables

\---

\#\# 6\. RÈGLES MÉTIER

\#\#\# 6.1 Plans d'Abonnement

\*\*Starter (5,000 FCFA/mois):\*\*  
\- Jusqu'à 5 biens  
\- Locataires illimités  
\- Quittances automatiques  
\- 10 SMS inclus/mois  
\- Support email

\*\*Professionnel (15,000 FCFA/mois):\*\*  
\- Jusqu'à 20 biens  
\- SMS illimités  
\- Rapports avancés  
\- Support prioritaire WhatsApp

\*\*Premium (35,000 FCFA/mois):\*\*  
\- Jusqu'à 50 biens  
\- Multi-utilisateurs  
\- API intégrations  
\- Gestionnaire dédié

\#\#\# 6.2 Limites Techniques

\- Photos: Max 10 par bien, 5MB chacune  
\- Documents: Max 16MB par fichier  
\- Quittances: Conservées 5 ans  
\- Backup: Quotidien automatique  
\- Sessions: Expiration 7 jours

\#\#\# 6.3 Sécurité

\- Mots de passe hashés (Werkzeug)  
\- HTTPS obligatoire (production)  
\- CSRF protection (Flask-WTF)  
\- Rate limiting (Flask-Limiter)  
\- Validation inputs (WTForms)  
\- SQL injection protection (SQLAlchemy ORM)  
\- XSS protection (Jinja2 auto-escape)

\---

\#\# 7\. INTERFACE UTILISATEUR

\#\#\# 7.1 Design System

\*\*Couleurs:\*\*  
\- Primaire: Orange (\#FF6B35) \- Énergie, tech  
\- Secondaire: Bleu nuit (\#1A1F3A) \- Professionnalisme  
\- Accent: Vert (\#2ECC71) \- Succès  
\- Neutre: Gris clair (\#F5F5F5)

\*\*Typographie:\*\*  
\- Titres: Montserrat Bold / Poppins Bold  
\- Corps: Inter Regular / Open Sans

\*\*Composants TailwindCSS:\*\*  
\- Boutons: Primary, Secondary, Danger  
\- Cards: Statistiques, Liste items  
\- Tables: Responsive, sortable  
\- Forms: Validation inline  
\- Modals: Confirmation, Info  
\- Alerts: Success, Error, Warning, Info

\#\#\# 7.2 Responsive Design

\*\*Breakpoints:\*\*  
\- Mobile: \< 640px  
\- Tablet: 640px \- 1024px  
\- Desktop: \> 1024px

\*\*Priorités:\*\*  
\- Mobile-first approach  
\- Touch-friendly (boutons min 44px)  
\- Navigation adaptative  
\- Tables scrollables sur mobile

\#\#\# 7.3 Accessibilité

\- Contraste WCAG AA minimum  
\- Labels sur tous les inputs  
\- Navigation clavier  
\- Attributs ARIA  
\- Focus visible

\---

\#\# 8\. PERFORMANCE

\#\#\# 8.1 Objectifs

\- Temps de chargement: \< 3 secondes (3G)  
\- First Contentful Paint: \< 1.5s  
\- Time to Interactive: \< 3.5s  
\- Lighthouse Score: \> 85

\#\#\# 8.2 Optimisations

\*\*Backend:\*\*  
\- Database indexing (email, phone, property\_id, etc.)  
\- Query optimization (eager loading)  
\- Caching (Redis) pour stats dashboard  
\- Pagination (max 50 items/page)

\*\*Frontend:\*\*  
\- Images optimisées (WebP, compression)  
\- Lazy loading images  
\- Minification CSS/JS  
\- CDN pour assets statiques (optionnel)  
\- Code splitting (si SPA)

\*\*Database:\*\*  
\- Connection pooling  
\- Query caching  
\- Regular VACUUM (PostgreSQL)

\---

\#\# 9\. INTÉGRATIONS EXTERNES

\#\#\# 9.1 Orange SMS API

\*\*Utilisation:\*\*  
\- Rappels de loyer automatiques  
\- Notifications contrat expirant  
\- SMS bienvenue

\*\*Endpoints:\*\*  
\`\`\`  
POST /smsmessaging/v1/outbound/{senderAddress}/requests  
Authorization: Bearer {token}  
\`\`\`

\*\*Limites:\*\*  
\- 160 caractères par SMS  
\- Rate limit: 100 SMS/minute  
\- Coût: \~25 FCFA/SMS

\#\#\# 9.2 Wave API (Version 2\)

\*\*Utilisation:\*\*  
\- Paiements en ligne locataires  
\- Collecte automatique loyers

\*\*Intégration:\*\*  
\- Webhook pour notifications paiement  
\- Réconciliation automatique

\#\#\# 9.3 Email (SMTP)

\*\*Utilisation:\*\*  
\- Vérification email inscription  
\- Reset mot de passe  
\- Envoi quittances  
\- Notifications importantes

\*\*Configuration:\*\*  
\- SMTP Gmail / SendGrid  
\- Templates HTML responsive

\---

\#\# 10\. TESTS & QUALITÉ

\#\#\# 10.1 Tests Unitaires

\*\*Couverture minimum: 70%\*\*

\*\*À tester:\*\*  
\- Modèles (création, relations, méthodes)  
\- Services (business logic)  
\- Validations (forms, inputs)  
\- Utilitaires (formatage, calculs)

\*\*Framework:\*\* unittest / pytest

\#\#\# 10.2 Tests d'Intégration

\*\*Scénarios critiques:\*\*  
\- Cycle complet: Inscription → Ajout bien → Locataire → Paiement  
\- Génération quittance  
\- Envoi SMS  
\- Calculs financiers

\#\#\# 10.3 Tests Manuels

\*\*Checklist avant release:\*\*  
\- \[ \] Tous les formulaires fonctionnent  
\- \[ \] Upload fichiers (photos, documents)  
\- \[ \] Génération PDF quittances  
\- \[ \] Envoi SMS (mode test)  
\- \[ \] Responsive mobile/tablet/desktop  
\- \[ \] Navigation complète  
\- \[ \] Gestion erreurs  
\- \[ \] Performance (Lighthouse)

\---

\#\# 11\. DÉPLOIEMENT

\#\#\# 11.1 Environnements

\*\*Development:\*\*  
\- SQLite  
\- Debug mode ON  
\- Local server (Flask dev server)

\*\*Staging:\*\*  
\- PostgreSQL  
\- Debug mode OFF  
\- Gunicorn \+ Nginx  
\- Données de test

\*\*Production:\*\*  
\- PostgreSQL (réplication)  
\- HTTPS obligatoire  
\- Gunicorn (3-5 workers)  
\- Nginx reverse proxy  
\- Monitoring Sentry  
\- Backups quotidiens automatiques

\#\#\# 11.2 Variables d'Environnement

\`\`\`  
\# Flask  
SECRET\_KEY=  
FLASK\_ENV=production

\# Database  
DATABASE\_URL=postgresql://user:pass@host:5432/immogest

\# APIs  
ORANGE\_SMS\_API\_KEY=  
WAVE\_API\_KEY=

\# Email  
MAIL\_SERVER=  
MAIL\_USERNAME=  
MAIL\_PASSWORD=

\# Redis  
REDIS\_URL=redis://localhost:6379/0  
\`\`\`

\#\#\# 11.3 Serveur Production

\*\*Spécifications minimales:\*\*  
\- 2 vCPU  
\- 4GB RAM  
\- 40GB SSD  
\- Ubuntu 22.04 LTS

\*\*Services:\*\*  
\- Nginx (reverse proxy)  
\- Gunicorn (WSGI)  
\- PostgreSQL  
\- Redis  
\- Celery Worker  
\- Celery Beat (cron)

\#\#\# 11.4 SSL/HTTPS

\- Certificat Let's Encrypt (gratuit)  
\- Auto-renouvellement (Certbot)  
\- Redirection HTTP → HTTPS  
\- HSTS header

\#\#\# 11.5 Monitoring

\*\*Logs:\*\*  
\- Application logs: \`/var/log/immogest/\`  
\- Nginx logs: \`/var/log/nginx/\`  
\- Rotation automatique

\*\*Alertes:\*\*  
\- Erreurs 500 (Sentry)  
\- Serveur down (UptimeRobot)  
\- Disque \> 80% (monitoring serveur)

\---

\#\# 12\. MAINTENANCE & ÉVOLUTION

\#\#\# 12.1 Backups

\*\*Base de données:\*\*  
\- Fréquence: Quotidien (2h du matin)  
\- Rétention: 30 jours  
\- Stockage: Externe (AWS S3 / DigitalOcean Spaces)

\*\*Fichiers utilisateurs:\*\*  
\- Fréquence: Hebdomadaire  
\- Rétention: 60 jours

\*\*Test restoration:\*\* Mensuel

\#\#\# 12.2 Mises à Jour

\*\*Sécurité:\*\*  
\- Patches critiques: Immédiatement  
\- Dépendances: Mensuel

\*\*Fonctionnalités:\*\*  
\- Releases: Bi-mensuel  
\- Hotfixes: Si nécessaire

\*\*Process:\*\*  
1\. Backup complet  
2\. Tests en staging  
3\. Déploiement production (maintenance courte)  
4\. Monitoring post-déploiement

\#\#\# 12.3 Support Utilisateurs

\*\*Canaux:\*\*  
\- Email: support@immogest.sn  
\- WhatsApp: \+221 XX XXX XX XX  
\- FAQ intégrée

\*\*SLA:\*\*  
\- Réponse: \< 24h  
\- Résolution bugs critiques: \< 48h  
\- Nouvelles fonctionnalités: Sprint planning

\---

\#\# 13\. DOCUMENTATION

\#\#\# 13.1 Documentation Technique

\*\*À produire:\*\*  
\- Architecture système  
\- Modèle de données (diagramme ERD)  
\- API interne (si création API REST)  
\- Guide installation développeur  
\- Conventions de code

\#\#\# 13.2 Documentation Utilisateur

\*\*À produire:\*\*  
\- Guide de démarrage rapide  
\- Tutoriels vidéo (3-5 min)  
\- FAQ  
\- Cas d'usage courants  
\- Glossaire

\#\#\# 13.3 Documentation Admin

\*\*À produire:\*\*  
\- Procédures de déploiement  
\- Gestion backups/restoration  
\- Monitoring et alertes  
\- Troubleshooting commun

\---

\#\# 14\. PLANNING & BUDGET

\#\#\# 14.1 Phases de Développement

\*\*Phase 1: Fondations (2 semaines)\*\*  
\- Setup projet  
\- Modèles de données  
\- Authentification  
\- Layout de base

\*\*Phase 2: Modules CRUD (4 semaines)\*\*  
\- Gestion biens  
\- Gestion locataires  
\- Gestion paiements  
\- Quittances PDF

\*\*Phase 3: Automatisation (2 semaines)\*\*  
\- Dashboard stats  
\- Relances SMS automatiques  
\- Celery tasks

\*\*Phase 4: Rapports & Finitions (2 semaines)\*\*  
\- Module rapports  
\- Settings utilisateur  
\- Tests complets  
\- Documentation

\*\*Phase 5: Déploiement (1 semaine)\*\*  
\- Setup serveur production  
\- Migration données test  
\- Tests production  
\- Formation équipe

\*\*TOTAL: 11 semaines (\~3 mois)\*\*

\#\#\# 14.2 Budget Estimatif

\*\*Développement:\*\* (Équipe de 5\)  
\- 3 mois développement  
\- Ressources internes Nexatech

\*\*Infrastructure (Mensuel):\*\*  
\- Serveur DigitalOcean: 30,000 FCFA  
\- Nom de domaine: 20,000 FCFA/an  
\- SMS API: Variable (usage)  
\- Email API: Gratuit (Gmail) / 10,000 FCFA (SendGrid)  
\- Monitoring: Gratuit (Sentry tier free)

\*\*TOTAL Mensuel: \~35,000 FCFA\*\*

\*\*Coûts One-Time:\*\*  
\- SSL: Gratuit (Let's Encrypt)  
\- Design assets: Interne  
\- Tests beta: Gratuit (utilisateurs volontaires)

\---

\#\# 15\. RISQUES & MITIGATION

\#\#\# 15.1 Risques Techniques

\*\*Risque:\*\* Intégration SMS API complexe    
\*\*Mitigation:\*\* Prévoir fallback email, tests approfondis

\*\*Risque:\*\* Performance avec données volumineuses    
\*\*Mitigation:\*\* Indexation DB, pagination, caching

\*\*Risque:\*\* Génération PDF lente    
\*\*Mitigation:\*\* Celery tasks asynchrones, templates optimisés

\#\#\# 15.2 Risques Business

\*\*Risque:\*\* Adoption faible    
\*\*Mitigation:\*\* MVP rapide, feedback utilisateurs, prix attractif

\*\*Risque:\*\* Concurrence    
\*\*Mitigation:\*\* Être premiers au Sénégal, service client excellent

\*\*Risque:\*\* Paiements (monétisation)    
\*\*Mitigation:\*\* Plusieurs options (Wave, OM, virement, cash)

\#\#\# 15.3 Risques Légaux

\*\*Risque:\*\* RGPD / Protection données    
\*\*Mitigation:\*\* Conformité dès conception, export données, suppression compte

\*\*Risque:\*\* Données sensibles (CNI, revenus)    
\*\*Mitigation:\*\* Chiffrement, accès restreint, logs audit

\---

\#\# 16\. CRITÈRES DE SUCCÈS

\#\#\# 16.1 KPIs Techniques

\- ✅ Uptime: \> 99.5%  
\- ✅ Temps réponse: \< 2s (médiane)  
\- ✅ Couverture tests: \> 70%  
\- ✅ Lighthouse score: \> 85  
\- ✅ Zero critical security issues

\#\#\# 16.2 KPIs Business (6 mois post-launch)

\- ✅ 100+ utilisateurs actifs  
\- ✅ 500+ biens enregistrés  
\- ✅ 80%+ taux rétention mensuel  
\- ✅ NPS (Net Promoter Score): \> 50  
\- ✅ 90%+ paiements automatiques

\#\#\# 16.3 KPIs Utilisateurs

\- ✅ Temps onboarding: \< 15 min  
\- ✅ Génération 1ère quittance: \< 5 min  
\- ✅ Satisfaction: \> 4/5  
\- ✅ Support tickets: \< 5% utilisateurs/mois

\---

\#\# 17\. LIVRABLES

\#\#\# 17.1 Livrables Techniques

\- \[ \] Code source complet (GitHub)  
\- \[ \] Base de données (schéma \+ migrations)  
\- \[ \] Tests unitaires \+ intégration  
\- \[ \] Documentation technique  
\- \[ \] Scripts déploiement  
\- \[ \] Configuration serveurs

\#\#\# 17.2 Livrables Fonctionnels

\- \[ \] Application web complète  
\- \[ \] Module dashboard  
\- \[ \] Module biens immobiliers  
\- \[ \] Module locataires  
\- \[ \] Module paiements  
\- \[ \] Génération quittances PDF  
\- \[ \] Relances SMS automatiques  
\- \[ \] Rapports & exports

\#\#\# 17.3 Livrables Utilisateur

\- \[ \] Guide utilisateur (PDF)  
\- \[ \] Tutoriels vidéo  
\- \[ \] FAQ  
\- \[ \] Accès plateforme production  
\- \[ \] Formation équipe support

\---

\#\# 18\. VALIDATION & RECETTE

\#\#\# 18.1 Tests de Recette Fonctionnels

\*\*Scénarios à valider:\*\*

1\. \*\*Inscription & Connexion\*\*  
   \- Créer compte  
   \- Vérifier email  
   \- Se connecter  
   \- Reset mot de passe

2\. \*\*Gestion Biens\*\*  
   \- Ajouter 5 biens avec photos  
   \- Modifier informations  
   \- Filtrer et rechercher  
   \- Supprimer un bien

3\. \*\*Gestion Locataires\*\*  
   \- Ajouter 5 locataires  
   \- Lier à des biens  
   \- Upload documents  
   \- Consulter historique

4\. \*\*Paiements\*\*  
   \- Enregistrer 10 paiements  
   \- Générer quittances PDF  
   \- Envoyer par email  
   \- Filtrer liste

5\. \*\*Automatisation\*\*  
   \- Vérifier rappels SMS J+3  
   \- Vérifier rappels SMS J+10  
   \- Consulter logs envois

6\. \*\*Rapports\*\*  
   \- Générer rapport mensuel  
   \- Exporter CSV  
   \- Exporter PDF  
   \- Vérifier calculs

\#\#\# 18.2 Critères d'Acceptation

\- \[ \] Toutes les fonctionnalités MVP opérationnelles  
\- \[ \] Aucun bug bloquant  
\- \[ \] Performance conforme (\< 3s chargement)  
\- \[ \] Responsive testé (mobile/tablet/desktop)  
\- \[ \] Génération PDF fonctionnelle  
\- \[ \] Envoi SMS testé (mode sandbox puis production)  
\- \[ \] Documentation complète fournie

\---

\#\# 19\. MAINTENANCE POST-LANCEMENT

\#\#\# 19.1 Support Niveau 1 (Utilisateurs)

\*\*Engagement:\*\*  
\- Disponibilité: Lun-Ven 9h-18h  
\- Réponse: \< 4h  
\- Canaux: Email, WhatsApp

\#\#\# 19.2 Support Niveau 2 (Technique)

\*\*Engagement:\*\*  
\- Disponibilité: 24/7 (alertes critiques)  
\- Intervention: \< 2h (critique), \< 24h (majeur)  
\- Monitoring continu

\#\#\# 19.3 Évolutions

\*\*Roadmap Année 1:\*\*  
\- Trimestre 1: MVP Launch  
\- Trimestre 2: Portail locataire  
\- Trimestre 3: Paiements automatiques  
\- Trimestre 4: Application mobile

\---

\#\# 20\. ANNEXES

\#\#\# 20.1 Glossaire

\- \*\*Bailleur:\*\* Propriétaire qui loue un bien  
\- \*\*Locataire:\*\* Personne qui occupe un bien en location  
\- \*\*Quittance:\*\* Document attestant du paiement du loyer  
\- \*\*Caution:\*\* Dépôt de garantie (généralement 2-3 mois)  
\- \*\*Charges:\*\* Frais mensuels (eau, électricité, etc.)  
\- \*\*Taux d'occupation:\*\* % de biens occupés vs total  
\- \*\*FCFA:\*\* Franc CFA (devise)

\#\#\# 20.2 Références

\- Flask Documentation: https://flask.palletsprojects.com/  
\- TailwindCSS: https://tailwindcss.com/  
\- Chart.js: https://www.chartjs.org/  
\- Orange SMS API: Documentation Orange Developer  
\- SQLAlchemy: https://www.sqlalchemy.org/

\#\#\# 20.3 Contacts

\*\*Nexatech:\*\*  
\- Email: contact@nexatech-sn.online  
\- Téléphone: \+221 XX XXX XX XX  
\- Adresse: \[Adresse Dakar\]

\*\*Chef de Projet:\*\* \[Nom Personne 4\]    
\*\*Lead Developer:\*\* \[Nom Personne 1\]    
\*\*Product Owner:\*\* \[Nom Personne 5\]

\---

\*\*FIN DU CAHIER DES CHARGES\*\*

\---

\*\*Signatures:\*\*

Chef de Projet: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_/\_\_\_/\_\_\_\_

Lead Developer: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_/\_\_\_/\_\_\_\_

Product Owner: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_/\_\_\_/\_\_\_\_

\---

\*Ce document est confidentiel et propriété de Nexatech Sénégal SARL.\*