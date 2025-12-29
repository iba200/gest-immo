# 🛣 Liste des Routes de l'Application ImmoGest

| Endpoint | Methods | Rule |
| :--- | :--- | :--- |
| `auth.login` | GET, POST | `/auth/login` |
| `auth.logout` | GET | `/auth/logout` |
| `auth.profile` | GET, POST | `/auth/profile` |
| `auth.register` | GET, POST | `/auth/register` |
| `auth.reset_password` | GET, POST | `/auth/reset_password/<token>` |
| `auth.reset_password_request` | GET, POST | `/auth/reset_password_request` |
| `main.dashboard` | GET | `/dashboard` |
| `main.dashboard` | GET | `/` |
| `main.export_monthly_report` | GET | `/export/monthly-report` |
| `payment.create` | GET, POST | `/payments/new` |
| `payment.email_receipt` | GET | `/payments/<int:id>/email` |
| `payment.export_csv` | GET | `/payments/export/csv` |
| `payment.index` | GET | `/payments/` |
| `payment.monthly_summary` | GET | `/payments/monthly-summary` |
| `payment.receipt` | GET | `/payments/<int:id>/receipt` |
| `payment.tenant_history` | GET | `/payments/tenant/<int:tenant_id>` |
| `property.create` | GET, POST | `/properties/new` |
| `property.delete` | POST | `/properties/<int:id>/delete` |
| `property.edit` | GET, POST | `/properties/<int:id>/edit` |
| `property.index` | GET | `/properties/` |
| `property.show` | GET | `/properties/<int:id>` |
| `static` | GET | `/static/<path:filename>` |
| `tenant.archive` | POST | `/tenants/<int:id>/archive` |
| `tenant.create` | GET, POST | `/tenants/new` |
| `tenant.edit` | GET, POST | `/tenants/<int:id>/edit` |
| `tenant.index` | GET | `/tenants/` |
| `tenant.show` | GET | `/tenants/<int:id>` |
