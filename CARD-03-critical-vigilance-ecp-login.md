# Finding Card 03 — vigilance.ndda.kz: ECP-логин без криптопроверки (CRITICAL)

## Title
Вход по ЭЦП принимает самоподписанный сертификат с невалидной подписью — аутентификация сводится к знанию ИИН — vigilance.ndda.kz

## Severity / CVSS
- **Critical (9.8)** — `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
  (для approved-аккаунтов: полный захват учётки; KZ ИИН — квазипубличные данные)
- CWE-347 Improper Verification of Cryptographic Signature + CWE-204 Observable Response Discrepancy

## Affected component
- `POST https://vigilance.ndda.kz/api/auth/ecp-login` `{"data":"auth","signature":"<XML-DSig>"}` (анонимно)
- `POST https://vigilance.ndda.kz/api/auth/ecp-registration-info` `{"data":"registration","signature":"…"}` (анонимный user-enum)

## Summary
Бекенд парсит XML-DSig и берёт **ИИН из subject сертификата** (`serialNumber=IIN<12 цифр>`), не проверяя ни саму подпись, ни цепочку издателя. SignatureValue может быть мусором (`AAAA`). Дальше — лукап пользователя в БД по ИИН. Для любого одобренного (approved) пользователя вход = знание его ИИН, без пароля и без владения ключом ЭЦП. Этим же механизмом логинятся сотрудники портала (эксперты МЗ).

## PoC (03.09, оракул-прогон, non-destructive)
Прогрессия ошибок выжимает формат парсера:
```
{}                                  → "XML is empty"
signature без <Signature>           → "Signature not found"
без KeyInfo/серт                    → "Certificate not found"
серт без serialNumber=IIN…          → "IIN not found in certificate subject"
serialNumber=IIN<12цифр> (self-signed, SignatureValue=AAAA)
                                    → "Пользователь не подтвержден" (ИИН есть в БД)
                                    → "Пользователь не найден" (ИИНа нет)
```
Дифференциация ответов = user-enum по ИИН + доказательство, что лукап дошёл до БД.
Дополнительно `POST /api/auth/ecp-registration-info` → 200 `{"userExists":true,"organizationExists":false,…}` — анонимная проверка наличия ИИН/организации в БД.

## Impact
1. Захват учёток approved-пользователей по ИИН (квазипубличен: документооборот, реестры; в самой системе принимается без верификации при регистрации)
2. Компрометация учёток экспертов фармаконадзора = доступ к медицинским данным надзора
3. User-enum по ИИН (ecp-login + ecp-registration-info)

## Recommendation
1. Проверять подпись (XML-DSig валидация SignatureValue против KeyInfo-сертификата и подписанных данных) и цепочку к KZ-CA
2. Единая generic-ошибка аутентификации (без «не подтвержден»/«не найден»)
3. Привязать сертификат к учётке (fingerprint при привязке), а не лукап по subject

## Примечание
Вход в ЧУЖИЕ реальные учётки не проводился (вне ангажемента). End-to-end подтверждается на собственной тестовой учётке (user 6a631ece-…) после её одобрения: серт `t8.pem` (ИИН 123456789014) в scratchpad, приватный ключ третьим лицам не передавался.
