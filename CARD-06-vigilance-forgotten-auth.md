# Finding Card 06 — vigilance.ndda.kz: забытая авторизация на части API (MEDIUM-HIGH)

## Title
Справочники, данные организаций и POST-создание заявок обрабатываются анонимно; стектрейс .NET наружу — vigilance.ndda.kz

## Severity / CVSS
- **Medium-High (6.5)** — `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N`
- CWE-306 Missing Authentication for Critical Function + CWE-209 Information Exposure Through Error Message

## Affected component
- `https://vigilance.ndda.kz/api/*` (ASP.NET Core + EF Core, Docker `/app/Pharm.*`), nginx проксирует весь `/api/`

## Summary
Часть API портала фармаконадзора не закрыта авторизацией: анонимные справочники, лукап организаций по БИН и — критичнее — POST-эндпоинты создания заявок, которые анонимно проходят auth-мидлварь и доходят до бизнес-логики (падают 500 на null-данных, но не 401).

## PoC / наблюдения (03.09, 64+ запроса, non-destructive)
- **10 анонимных справочников**: users/roles (6 ролей с GUID), countries (39 КБ), organization_forms (41 КБ), document_types, organization_types, currencies, contact_types и др.
- `GET /api/organizations/GetDataByLegalNumber?legalNumber=<БИН>` → 200: юрданные + внутренний GUID + флаг is_Expert (проверено на БИН самой НЦЭЛС: org `fa304980-11c9-45a7-8032-0fb48ece85a2`, is_Expert:true); `GetHolderData` тоже анонимен
- **POST-создания доходят до бизнес-логики анонимно** (500, не 401): `/api/mf_applications`, `/api/psur`, `/api/auth/register`, `/api/organizations/register` (multipart), `/api/mf_application_products`, `/api/psur/product`. Записей не создано (тела только `{}`/пустые формы)
- **Стектрейс наружу** (POST /api/organizations/register, 3054 Б): `System.InvalidOperationException → NullReferenceException` в EF Core LINQ → `Pharm.Account.Logic.Data.Organization.OrganizationLogic.Register(RegisterRequest) at /app/Pharm.Account.Logic/Data/Organization/OrganizationLogic.cs:line 976` — пути исходников в контейнере раскрыты
- Кастомный middleware глотает тела ошибок (400-валидацию не получить); `users/createHolder` нестабилен (500→401)
- Закрыто: ExternalService/* (Damumed) — 401

## Impact
- Утечка структуры/данных портала (роли, GUID-ы, организации по любому публичному БИН)
- Пути к созданию заявок без авторизации — при подборе модели валидные записи создаются анонимно (создание заявок в проде = изменение данных, не тестировалось)
- Раскрытие внутренней структуры кода (стектрейс)

## Recommendation
1. `[Authorize]` на все контроллеры по умолчанию, анонимные — явным белым списком
2. Убрать подробные стектрейсы из ответов (customErrors/ProblemDetails без stack)
3. Запретить nginx-проксирование /api/ мимо auth-мидлвари приложения

## Evidence
R/summary.tsv, R/org_register_500_stacktrace.json, R/*.json (справочники) — scratchpad субагента
